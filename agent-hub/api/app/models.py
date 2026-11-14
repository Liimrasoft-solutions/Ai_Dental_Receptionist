"""Tables. Every agent writes to the same `events` table in one normalized shape."""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, DateTime, Float, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def now() -> datetime:
    return datetime.now(timezone.utc)


class Location(Base):
    """A clinic office, e.g. Garland or Plano."""
    __tablename__ = "locations"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    # Inbound number, used to tell which office a Retell call belongs to (E.164, e.g. +19725550100)
    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True)


class Source(Base):
    """Anything allowed to send events: Retell, our insurance agent, a future vendor.

    kind="retell"  -> verified with the Retell SDK signature
    kind="signed"  -> verified with our own HMAC signature (see security.py)
    callback_url   -> optional; we POST staff actions (approve, pause) back to it
    """
    __tablename__ = "sources"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    kind: Mapped[str] = mapped_column(String(32))
    agent: Mapped[str] = mapped_column(String(64))
    secret: Mapped[str] = mapped_column(String(256), default="")
    callback_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    enabled: Mapped[bool] = mapped_column(default=True)


class AgentState(Base):
    __tablename__ = "agent_states"
    agent: Mapped[str] = mapped_column(String(64), primary_key=True)
    paused: Mapped[bool] = mapped_column(default=False)
    updated_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_event_source_external"),
        Index("ix_events_agent_time", "agent", "occurred_at"),
        Index("ix_events_status", "status"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(64))
    external_id: Mapped[str] = mapped_column(String(200))
    agent: Mapped[str] = mapped_column(String(64))
    location_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    type: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))  # done | needs_staff | failed | waiting | transferred
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    summary: Mapped[str] = mapped_column(Text, default="")
    patient_ref: Mapped[str | None] = mapped_column(String(16), nullable=True)  # initials only
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    resolved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, onupdate=now)


class AuditLog(Base):
    """Who looked at what and who changed what."""
    __tablename__ = "audit_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    actor: Mapped[str] = mapped_column(String(128))
    action: Mapped[str] = mapped_column(String(64))
    target: Mapped[str] = mapped_column(String(256))
    detail: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
