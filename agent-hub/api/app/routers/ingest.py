"""Machine-facing routes. Agents and vendors send events here; no user login, signatures instead."""
import json

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import TypeAdapter, ValidationError
from sqlalchemy.orm import Session

from ..connectors.registry import CONNECTORS
from ..db import get_db
from ..models import Source
from ..schemas import EventIn
from ..security import verify_signed
from ..services.ingest import upsert_event

router = APIRouter(prefix="/v1", tags=["ingest"])
EventsIn = TypeAdapter(EventIn | list[EventIn])


@router.post("/webhooks/retell", status_code=204)
async def retell_webhook(request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    connector = CONNECTORS["retell"]
    if not connector.verify(raw, {k.lower(): v for k, v in request.headers.items()}):
        raise HTTPException(401, "Retell signature check failed")
    for ev in connector.to_events(json.loads(raw), db):
        upsert_event(db, "retell", ev)


@router.post("/ingest/{source_id}")
async def ingest(
    source_id: str,
    request: Request,
    db: Session = Depends(get_db),
    x_hub_timestamp: str | None = Header(None),
    x_hub_signature: str | None = Header(None),
):
    """Any agent that speaks our format: one event or a list, signed with its source secret."""
    source = db.get(Source, source_id)
    if not source or not source.enabled or source.kind != "signed":
        raise HTTPException(404, f"No enabled source called '{source_id}'")
    raw = await request.body()
    verify_signed(source.secret, x_hub_timestamp, x_hub_signature, raw)
    try:
        parsed = EventsIn.validate_json(raw)
    except ValidationError as exc:
        raise HTTPException(422, exc.errors(include_url=False))
    events = parsed if isinstance(parsed, list) else [parsed]
    for ev in events:
        if ev.agent != source.agent:
            raise HTTPException(403, f"Source '{source_id}' may only send events for agent '{source.agent}'")
    ids = [upsert_event(db, source_id, ev).id for ev in events]
    return {"saved": len(ids), "ids": ids}
