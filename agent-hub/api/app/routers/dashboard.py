"""People-facing routes the dashboard reads."""
from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import AgentState, AuditLog, Event, Location, Source
from ..schemas import PauseIn, ResolveIn
from ..security import User, current_user, require_role
from ..services.live import broadcaster
from ..services.notify import send_action
from ..services.summaries import AGENTS, agent_def

router = APIRouter(prefix="/v1", tags=["dashboard"])


def audit(db: Session, user: User, action: str, target: str, **detail) -> None:
    db.add(AuditLog(actor=user.email, action=action, target=target, detail=detail))
    db.commit()


def window(db: Session, user: User, location: str | None, days: int, agent: str | None = None):
    since = datetime.now(timezone.utc) - timedelta(days=days)
    q = select(Event).where(Event.occurred_at >= since)
    if agent:
        q = q.where(Event.agent == agent)
    if location:
        q = q.where(Event.location_id == location)
    if user.location_ids is not None:
        q = q.where(Event.location_id.in_(user.location_ids))
    return list(db.scalars(q))


def known_agents(db: Session) -> list[str]:
    seen = set(db.scalars(select(Event.agent).distinct())) | set(db.scalars(select(Source.agent).distinct()))
    return list(AGENTS) + sorted(seen - set(AGENTS))


def paused_map(db: Session) -> dict[str, bool]:
    return {s.agent: s.paused for s in db.scalars(select(AgentState))}


def month_cost(db: Session) -> float:
    start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return float(db.scalar(select(func.coalesce(func.sum(Event.cost_usd), 0)).where(Event.occurred_at >= start)))


@router.get("/meta")
def meta(db: Session = Depends(get_db), user: User = Depends(current_user)):
    return {
        "user": {"email": user.email, "role": user.role},
        "locations": [{"id": l.id, "name": l.name} for l in db.scalars(select(Location).order_by(Location.name))],
        "agents": [{"key": k, "label": agent_def(k).label} for k in known_agents(db)],
    }


@router.get("/overview")
def overview(
    location: str | None = None,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    events = window(db, user, location, days)
    by_agent: dict[str, list[Event]] = {}
    for e in events:
        by_agent.setdefault(e.agent, []).append(e)
    paused = paused_map(db)

    tiles = []
    summaries = {}
    for key in known_agents(db):
        d = agent_def(key)
        s = d.summarize([e for e in by_agent.get(key, []) if e.type != "alert"], days)
        summaries[key] = s
        problems = sum(1 for e in by_agent.get(key, []) if e.status in ("failed", "needs_staff") and not e.resolved_at)
        tiles.append({
            "agent": key, "label": d.label, "kpi": s["kpis"][0], "second": s["kpis"][1] if len(s["kpis"]) > 1 else None,
            "paused": paused.get(key, False), "open_items": problems,
            "has_data": bool(by_agent.get(key)),
        })

    people = sorted(
        (e for e in events if e.type != "alert" and e.status in ("needs_staff", "transferred") and not e.resolved_at),
        key=lambda e: e.occurred_at, reverse=True,
    )[:12]
    alerts = sorted((e for e in events if e.type == "alert" and not e.resolved_at), key=lambda e: e.occurred_at, reverse=True)

    audit(db, user, "view", "overview", location=location, days=days)
    return {
        "tiles": tiles,
        "calls": summaries.get("receptionist", {}).get("series"),
        "side_breakdowns": [
            {**summaries["verification"]["breakdowns"][1], "agent": "verification", "title": "Insurance checks by method"} if by_agent.get("verification") else None,
            {**summaries["marketing"]["breakdowns"][0], "agent": "marketing", "title": "Marketing leads by source"} if by_agent.get("marketing") else None,
        ],
        "needs_person": [
            {"id": e.id, "agent": e.agent, "agent_label": agent_def(e.agent).label, "when": e.occurred_at.isoformat(),
             "summary": e.summary, "status": e.status, "location_id": e.location_id,
             "action_label": agent_def(e.agent).action_label}
            for e in people
        ],
        "alerts": [{"id": e.id, "agent": e.agent, "summary": e.summary, "level": e.data.get("level", "warning"),
                    "when": e.occurred_at.isoformat()} for e in alerts],
        "cost_month": round(month_cost(db), 2),
        "budget": settings.monthly_budget_usd,
        "status_counts": dict(Counter(e.status for e in events if e.type != "alert")),
        "sample_data": any(e.data.get("sample") for e in events[:500]),
    }


@router.get("/agents/{agent}")
def agent_page(
    agent: str,
    location: str | None = None,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    if agent not in known_agents(db):
        raise HTTPException(404, f"No agent called '{agent}' has reported yet")
    d = agent_def(agent)
    events = [e for e in window(db, user, location, days, agent) if e.type != "alert"]
    s = d.summarize(events, days)
    audit(db, user, "view", f"agent:{agent}", location=location, days=days)
    return {
        "agent": agent, "label": d.label, "action_label": d.action_label,
        "paused": paused_map(db).get(agent, False),
        "sample_data": any(e.data.get("sample") for e in events[:200]),
        **s,
    }


@router.post("/events/{event_id}/resolve")
def resolve(event_id: int, body: ResolveIn, tasks: BackgroundTasks,
            db: Session = Depends(get_db), user: User = Depends(current_user)):
    e = db.get(Event, event_id)
    if not e:
        raise HTTPException(404, "Event not found")
    e.resolved_by, e.resolved_at = user.email, datetime.now(timezone.utc)
    if e.status == "needs_staff":
        e.status = "done"
    db.commit()
    audit(db, user, "resolve", f"event:{event_id}", note=body.note)
    src = db.get(Source, e.source)
    if src and src.callback_url:
        tasks.add_task(send_action, src.callback_url, src.secret,
                       {"action": "resolved", "external_id": e.external_id, "by": user.email, "note": body.note})
    broadcaster.publish({"kind": "resolved", "id": e.id, "agent": e.agent})
    return {"ok": True}


@router.post("/agents/{agent}/pause")
def pause(agent: str, body: PauseIn, tasks: BackgroundTasks,
          db: Session = Depends(get_db), user: User = Depends(current_user)):
    require_role(user, "admin", "manager")
    state = db.get(AgentState, agent) or AgentState(agent=agent)
    state.paused, state.updated_by, state.updated_at = body.paused, user.email, datetime.now(timezone.utc)
    db.merge(state)
    db.commit()
    audit(db, user, "pause" if body.paused else "resume", f"agent:{agent}")
    # Each source decides what pausing means for it. For Retell, a small service
    # behind callback_url can switch the phone number to forward to staff.
    for src in db.scalars(select(Source).where(Source.agent == agent, Source.callback_url.is_not(None))):
        tasks.add_task(send_action, src.callback_url, src.secret, {"action": "pause", "paused": body.paused, "by": user.email})
    broadcaster.publish({"kind": "paused", "agent": agent, "paused": body.paused})
    return {"agent": agent, "paused": body.paused}


@router.get("/stream")
async def stream():
    return StreamingResponse(broadcaster.subscribe(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
