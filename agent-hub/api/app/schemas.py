from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

Status = Literal["done", "needs_staff", "failed", "waiting", "transferred"]


class EventIn(BaseModel):
    """The one format every agent reports in. See docs/EVENTS.md."""
    external_id: str = Field(max_length=200, description="Your own id for this job; resending it updates the event")
    agent: str = Field(max_length=64, pattern=r"^[a-z][a-z0-9_]*$")
    type: str = Field(max_length=64)
    status: Status = "done"
    occurred_at: datetime
    location_id: str | None = None
    summary: str = Field("", max_length=500)
    patient_ref: str | None = Field(None, max_length=16, description="Initials only. Never send names.")
    cost_usd: float = Field(0.0, ge=0)
    data: dict[str, Any] = Field(default_factory=dict)

    @field_validator("occurred_at")
    @classmethod
    def must_have_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("occurred_at needs a timezone, e.g. 2026-11-13T10:42:00Z")
        return v


class ResolveIn(BaseModel):
    note: str = Field("", max_length=500)


class PauseIn(BaseModel):
    paused: bool
