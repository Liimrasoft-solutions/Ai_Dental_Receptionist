"""Turns events into what each dashboard page shows.

Each agent has an AgentDef. An agent we have never heard of still gets a page,
built by `generic`, as soon as it starts sending events. Add a summarizer here
when you want that page to show agent-specific numbers.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable

from ..models import Event

Rows = list[dict]


@dataclass
class AgentDef:
    key: str
    label: str
    action_label: str
    summarize: Callable[[list[Event], int], dict]


# ---------- helpers ----------

def pct(part: float, whole: float) -> int:
    return round(100 * part / whole) if whole else 0


def money(v: float) -> str:
    return f"${v:,.2f}" if v < 10 else f"${v:,.0f}"


def mmss(seconds: float | None) -> str:
    if not seconds:
        return "–"
    s = int(seconds)
    return f"{s // 60}:{s % 60:02d}"


def kpi(label: str, value, sub: str = "", tone: str = "neutral") -> dict:
    return {"label": label, "value": str(value), "sub": sub, "tone": tone}


def daily(events: list[Event], days: int, group: Callable[[Event], str | None], keys: list[str]) -> dict:
    today = datetime.now(timezone.utc).date()
    buckets: dict = defaultdict(Counter)
    for e in events:
        k = group(e)
        if k in keys:
            buckets[e.occurred_at.astimezone(timezone.utc).date()][k] += 1
    points = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        points.append({"date": d.isoformat(), **{k: buckets[d][k] for k in keys}})
    return {"keys": keys, "points": points}


def when(e: Event) -> str:
    return e.occurred_at.isoformat()


def row(e: Event, **cols) -> dict:
    return {
        "id": e.id,
        "status": e.status,
        "actionable": e.status == "needs_staff" and e.resolved_at is None,
        "resolved_by": e.resolved_by,
        "location_id": e.location_id,
        "when": when(e),
        **{k: ("–" if v in (None, "") else v) for k, v in cols.items()},
    }


def bars(counter: Counter, total: int | None = None, as_pct: bool = False) -> list[dict]:
    total = total if total is not None else sum(counter.values())
    return [
        {"label": k, "value": v, "display": f"{pct(v, total)}%" if as_pct else str(v)}
        for k, v in counter.most_common()
    ]


# ---------- receptionist ----------

OUTCOME_LABEL = {
    "booked_new": "Booked, new patient",
    "booked_followup": "Booked, follow-up",
    "info": "Answered a question",
    "transferred": "Sent to staff",
    "emergency": "Emergency, sent to staff",
    "failed": "Failed",
    "in_progress": "In progress",
}


def receptionist(events: list[Event], days: int) -> dict:
    calls = [e for e in events if e.type == "call"]
    n = len(calls)
    outcomes = Counter(e.data.get("outcome") for e in calls)
    failed = outcomes["failed"]
    booked = outcomes["booked_new"] + outcomes["booked_followup"]
    transferred = outcomes["transferred"] + outcomes["emergency"]
    durations = [e.data.get("duration_s") for e in calls if e.data.get("duration_s")]
    cost = sum(e.cost_usd for e in calls)

    def group(e: Event):
        o = e.data.get("outcome")
        return {"booked_new": "Booked", "booked_followup": "Booked", "info": "Info",
                "transferred": "Transferred", "emergency": "Transferred", "failed": "Failed"}.get(o)

    lang = Counter({"en": "English", "es": "Spanish"}.get(e.data.get("language"), "Other") for e in calls)
    hours = Counter("After hours" if e.data.get("after_hours") else "Office hours" for e in calls)
    reasons = Counter(e.data.get("disconnection_reason") or "unknown" for e in calls if e.status == "failed")

    return {
        "kpis": [
            kpi("Calls answered", n - failed, f"{pct(n - failed, n)}% answer rate"),
            kpi("Appointments booked", booked, f"{outcomes['booked_new']} new patients"),
            kpi("Sent to staff", transferred, f"{outcomes['emergency']} emergencies", "staff" if outcomes["emergency"] else "neutral"),
            kpi("Failed or dropped", failed, f"{pct(failed, n)}% of calls", "failed" if failed else "neutral"),
            kpi("Average call", mmss(sum(durations) / len(durations) if durations else None), f"{money(cost / n if n else 0)} per call"),
        ],
        "series": {"title": "Calls per day", **daily(calls, days, group, ["Booked", "Info", "Transferred", "Failed"])},
        "breakdowns": [
            {"title": "Language", "items": bars(lang, as_pct=True)},
            {"title": "When people call", "items": bars(hours, as_pct=True)},
            {"title": "Why calls failed", "items": bars(reasons)},
        ],
        "table": {
            "title": "Every call",
            "columns": [
                {"key": "when", "label": "Time", "format": "datetime"},
                {"key": "location_id", "label": "Office"},
                {"key": "outcome", "label": "Outcome"},
                {"key": "language", "label": "Language"},
                {"key": "length", "label": "Length"},
                {"key": "summary", "label": "Summary", "wide": True},
            ],
            "rows": [
                row(e, outcome=OUTCOME_LABEL.get(e.data.get("outcome"), e.data.get("outcome")),
                    language=(e.data.get("language") or "").upper(), length=mmss(e.data.get("duration_s")),
                    summary=e.summary, recording_url=e.data.get("recording_url"))
                for e in sorted(calls, key=when, reverse=True)[:200]
            ],
        },
        "cost": cost,
    }


# ---------- insurance verification ----------

def verification(events: list[Event], days: int) -> dict:
    checks = [e for e in events if e.type == "check"]
    n = len(checks)
    st = Counter(e.status for e in checks)
    phone = [e for e in checks if e.data.get("method") == "phone"]
    elec = [e for e in checks if e.data.get("method") == "electronic"]

    def avg_min(es):
        d = [e.data.get("duration_s") or 0 for e in es]
        return round(sum(d) / len(d) / 60) if d else 0

    by_insurer: dict = defaultdict(lambda: [0, 0])
    for e in checks:
        s = by_insurer[e.data.get("insurer", "Unknown")]
        s[1] += 1
        s[0] += e.status == "done"
    insurer_items = sorted(
        ({"label": k, "value": pct(ok, tot), "display": f"{pct(ok, tot)}%"} for k, (ok, tot) in by_insurer.items()),
        key=lambda i: -i["value"],
    )
    before = [e for e in checks if e.data.get("before_visit_day")]
    cost = sum(e.cost_usd for e in checks)
    status_label = {"done": "Verified", "needs_staff": "Needs staff", "failed": "Failed", "waiting": "Waiting"}

    return {
        "kpis": [
            kpi("Requested", n, f"last {days} days"),
            kpi("Verified", st["done"], f"{pct(st['done'], n)}%", "done"),
            kpi("Needs staff", st["needs_staff"], "plan or data issue", "staff" if st["needs_staff"] else "neutral"),
            kpi("Failed", st["failed"], "no answer from insurer", "failed" if st["failed"] else "neutral"),
            kpi("Average time", f"{avg_min(checks)} min", f"electronic {avg_min(elec)} min, phone {avg_min(phone)} min"),
        ],
        "series": {"title": "Checks per day", **daily(checks, days, lambda e: status_label.get(e.status), list(status_label.values()))},
        "breakdowns": [
            {"title": "Success by insurer", "items": insurer_items},
            {"title": "Method", "items": bars(Counter("Electronic check" if e.data.get("method") == "electronic" else "Phone call" for e in checks), as_pct=True)},
            {"title": "Before the visit day", "items": [
                {"label": "Verified before the visit day", "value": pct(len(before), n), "display": f"{pct(len(before), n)}%"},
                {"label": "Cost per check", "value": 0, "display": money(cost / n if n else 0)},
            ]},
        ],
        "table": {
            "title": "Verification queue",
            "columns": [
                {"key": "visit", "label": "Visit", "format": "datetime"},
                {"key": "patient", "label": "Patient"},
                {"key": "insurer", "label": "Insurer"},
                {"key": "method", "label": "Method"},
                {"key": "result", "label": "Result", "wide": True},
            ],
            "rows": [
                row(e, visit=e.data.get("visit_at"), patient=e.patient_ref, insurer=e.data.get("insurer"),
                    method=(e.data.get("method") or "").capitalize(), result=e.summary)
                for e in sorted(checks, key=lambda e: e.data.get("visit_at") or "", reverse=True)[:200]
            ],
        },
        "cost": cost,
    }


# ---------- marketing ----------

def marketing(events: list[Event], days: int) -> dict:
    leads = [e for e in events if e.type == "lead"]
    items = [e for e in events if e.type in ("post", "ad_text", "review_reply")]
    reviews = [e for e in events if e.type == "review"]
    spend = sum(e.data.get("amount", 0) for e in events if e.type == "ad_spend")
    booked = sum(1 for e in leads if e.data.get("booked"))
    waiting = sum(1 for e in items if e.status == "needs_staff" and not e.resolved_at)
    ratings = [e.data.get("rating", 0) for e in reviews]
    sources = Counter(e.data.get("source", "Other") for e in leads)
    top = [s for s, _ in sources.most_common(3)]

    return {
        "kpis": [
            kpi("New leads", len(leads), f"last {days} days"),
            kpi("Cost per lead", money(spend / len(leads)) if leads else "–", f"ad spend {money(spend)}"),
            kpi("Booked from marketing", booked, f"{pct(booked, len(leads))}% of leads", "done"),
            kpi("Reviews", f"{sum(ratings) / len(ratings):.1f} ★" if ratings else "–", f"{len(reviews)} new"),
            kpi("Waiting for approval", waiting, "posts and ad text", "staff" if waiting else "neutral"),
        ],
        "series": {"title": "Leads per day by source", **daily(leads, days, lambda e: e.data.get("source"), top)},
        "breakdowns": [
            {"title": "Leads by source", "items": bars(sources)},
            {"title": "Latest reviews", "items": [
                {"label": e.summary, "value": e.data.get("rating", 0), "display": "★" * int(e.data.get("rating", 0))}
                for e in sorted(reviews, key=when, reverse=True)[:4]
            ]},
        ],
        "table": {
            "title": "Approval queue (nothing goes out without staff)",
            "columns": [
                {"key": "when", "label": "Drafted", "format": "datetime"},
                {"key": "item", "label": "Item", "wide": True},
                {"key": "channel", "label": "Channel"},
                {"key": "state", "label": "State"},
            ],
            "rows": [
                row(e, item=e.summary, channel=e.data.get("channel"), state=e.data.get("state", "draft").capitalize())
                for e in sorted(items, key=lambda e: (e.status != "needs_staff", e.occurred_at.timestamp() * -1))[:200]
            ],
        },
        "cost": sum(e.cost_usd for e in events),
    }


# ---------- health records ----------

def health_records(events: list[Event], days: int) -> dict:
    forms = [e for e in events if e.type == "form"]
    n = len(forms)
    states = Counter(e.data.get("state") for e in forms)
    completed = [e for e in forms if e.data.get("state") == "completed"]
    saved = sum(1 for e in completed if e.data.get("saved"))
    before = sum(1 for e in completed if e.data.get("before_visit"))
    flagged = sum(1 for e in forms if e.status == "needs_staff" and not e.resolved_at)
    times = [e.data.get("fill_seconds") for e in completed if e.data.get("fill_seconds")]
    opened = states["opened"] + len(completed)

    return {
        "kpis": [
            kpi("Forms sent", n, f"last {days} days"),
            kpi("Completed", len(completed), f"{pct(len(completed), n)}%", "done"),
            kpi("Before the visit", f"{pct(before, len(completed))}%", "target 90%"),
            kpi("Flagged for staff", flagged, "need review", "staff" if flagged else "neutral"),
            kpi("Average time", mmss(sum(times) / len(times) if times else None), "to fill in"),
        ],
        "series": {"title": "Forms completed per day", **daily(completed, days, lambda e: "Completed", ["Completed"])},
        "breakdowns": [
            {"title": "Form funnel", "items": [
                {"label": "Sent", "value": n, "display": str(n)},
                {"label": "Opened", "value": opened, "display": str(opened)},
                {"label": "Completed", "value": len(completed), "display": str(len(completed))},
                {"label": "Saved to record", "value": saved, "display": str(saved)},
            ]},
            {"title": "Language", "items": bars(Counter({"en": "English", "es": "Spanish"}.get(e.data.get("language"), "Other") for e in forms), as_pct=True)},
        ],
        "table": {
            "title": "Forms by visit",
            "columns": [
                {"key": "visit", "label": "Visit", "format": "datetime"},
                {"key": "patient", "label": "Patient"},
                {"key": "form", "label": "Form"},
                {"key": "language", "label": "Lang"},
                {"key": "state", "label": "State"},
                {"key": "flag", "label": "Flag", "wide": True},
            ],
            "rows": [
                row(e, visit=e.data.get("visit_at"), patient=e.patient_ref, form=e.data.get("form"),
                    language=(e.data.get("language") or "").upper(), state=(e.data.get("state") or "").capitalize(),
                    flag=e.data.get("flag"))
                for e in sorted(forms, key=lambda e: e.data.get("visit_at") or "", reverse=True)[:200]
            ],
        },
        "cost": sum(e.cost_usd for e in forms),
    }


# ---------- any other agent ----------

def generic(events: list[Event], days: int) -> dict:
    jobs = [e for e in events if e.type != "alert"]
    n = len(jobs)
    st = Counter(e.status for e in jobs)
    labels = {"done": "Done", "needs_staff": "Needs staff", "failed": "Failed", "waiting": "Waiting", "transferred": "Transferred"}
    return {
        "kpis": [
            kpi("Jobs", n, f"last {days} days"),
            kpi("Done", st["done"], f"{pct(st['done'], n)}%", "done"),
            kpi("Needs staff", st["needs_staff"], "", "staff" if st["needs_staff"] else "neutral"),
            kpi("Failed", st["failed"], "", "failed" if st["failed"] else "neutral"),
        ],
        "series": {"title": "Jobs per day", **daily(jobs, days, lambda e: labels.get(e.status), list(labels.values()))},
        "breakdowns": [{"title": "Job types", "items": bars(Counter(e.type for e in jobs))}],
        "table": {
            "title": "Latest jobs",
            "columns": [
                {"key": "when", "label": "Time", "format": "datetime"},
                {"key": "type", "label": "Type"},
                {"key": "summary", "label": "Summary", "wide": True},
            ],
            "rows": [row(e, type=e.type, summary=e.summary) for e in sorted(jobs, key=when, reverse=True)[:200]],
        },
        "cost": sum(e.cost_usd for e in jobs),
    }


AGENTS: dict[str, AgentDef] = {
    "receptionist": AgentDef("receptionist", "AI receptionist", "Mark handled", receptionist),
    "verification": AgentDef("verification", "Insurance verification", "Mark resolved", verification),
    "marketing": AgentDef("marketing", "Marketing", "Approve", marketing),
    "health_records": AgentDef("health_records", "Health records", "Mark reviewed", health_records),
}


def agent_def(key: str) -> AgentDef:
    return AGENTS.get(key) or AgentDef(key, key.replace("_", " ").capitalize(), "Mark resolved", generic)
