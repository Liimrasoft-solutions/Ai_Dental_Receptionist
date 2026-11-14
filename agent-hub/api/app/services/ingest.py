from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Event
from ..schemas import EventIn
from .live import broadcaster

FIELDS = ("agent", "location_id", "type", "status", "occurred_at", "summary", "patient_ref", "cost_usd")


def upsert_event(db: Session, source_id: str, ev: EventIn) -> Event:
    """Insert, or update the event with the same (source, external_id). Resending is safe."""
    row = db.scalar(select(Event).where(Event.source == source_id, Event.external_id == ev.external_id))
    if row is None:
        row = Event(source=source_id, external_id=ev.external_id, data={})
        db.add(row)
    for f in FIELDS:
        setattr(row, f, getattr(ev, f))
    row.data = {**(row.data or {}), **ev.data}
    db.commit()
    db.refresh(row)
    broadcaster.publish({"kind": "event", "agent": row.agent, "id": row.id, "status": row.status})
    return row
