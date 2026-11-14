"""Retell AI webhooks -> receptionist events.

Retell posts call_started, call_ended and call_analyzed for the same call_id.
We upsert on call_id, so the event fills in as each one arrives.
Field names follow Retell's webhook docs; check them against your account before go-live.

Outcome and language come from Retell "post-call analysis" fields that we define
on the Retell agent: `outcome` (booked_new | booked_followup | info | transferred |
emergency | failed) and `language` (en | es).
"""
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..models import Location
from ..schemas import EventIn

STATUS_BY_OUTCOME = {
    "booked_new": "done",
    "booked_followup": "done",
    "info": "done",
    "transferred": "transferred",
    "emergency": "transferred",
    "failed": "failed",
}


class RetellConnector:
    kind = "retell"

    def verify(self, raw_body: bytes, headers: dict[str, str]) -> bool:
        signature = headers.get("x-retell-signature")
        if not settings.retell_api_key or not signature:
            return False
        from retell.lib.webhook_auth import verify  # retell-sdk; checks the HMAC and a 5-minute window

        # Retell's docs verify against the compact JSON of the parsed body.
        body = json.dumps(json.loads(raw_body), separators=(",", ":"), ensure_ascii=False)
        return verify(body, settings.retell_api_key, signature)

    def to_events(self, payload: dict, db: Session) -> list[EventIn]:
        kind = payload.get("event")
        call = payload.get("call") or {}
        if kind not in ("call_started", "call_ended", "call_analyzed") or not call.get("call_id"):
            return []

        start_ms = call.get("start_timestamp")
        end_ms = call.get("end_timestamp")
        started = (
            datetime.fromtimestamp(start_ms / 1000, tz=timezone.utc) if start_ms else datetime.now(timezone.utc)
        )
        duration_s = round((end_ms - start_ms) / 1000) if start_ms and end_ms else None

        analysis = call.get("call_analysis") or {}
        custom = analysis.get("custom_analysis_data") or {}
        reason = call.get("disconnection_reason") or ""

        outcome = custom.get("outcome")
        if not outcome:
            if kind == "call_started":
                outcome = None
            elif reason == "call_transfer":
                outcome = "transferred"
            elif reason.startswith("error") or reason in ("dial_failed", "dial_no_answer"):
                outcome = "failed"
            else:
                outcome = "info"

        status = "waiting" if outcome is None else STATUS_BY_OUTCOME.get(outcome, "done")
        if outcome == "emergency":
            status = "needs_staff"

        cost = call.get("call_cost") or {}
        cost_usd = (cost.get("combined_cost") or 0) / 100  # Retell reports cents

        inbound = call.get("direction", "inbound") == "inbound"
        office_number = call.get("to_number") if inbound else call.get("from_number")
        caller_number = call.get("from_number") if inbound else call.get("to_number")
        location_id = (call.get("metadata") or {}).get("location_id")
        if not location_id and office_number:
            location_id = db.scalar(select(Location.id).where(Location.phone_number == office_number))

        local = started.astimezone(ZoneInfo(settings.clinic_timezone))
        after_hours = local.weekday() >= 5 or not (
            settings.office_open_hour <= local.hour < settings.office_close_hour
        )

        return [
            EventIn(
                external_id=call["call_id"],
                agent="receptionist",
                type="call",
                status=status,
                occurred_at=started,
                location_id=location_id,
                summary=(analysis.get("call_summary") or "Call in progress")[:500],
                cost_usd=cost_usd,
                data={
                    "outcome": outcome or "in_progress",
                    "language": custom.get("language", "en"),
                    "direction": call.get("direction", "inbound"),
                    "caller_last4": (caller_number or "")[-4:],
                    "duration_s": duration_s,
                    "after_hours": after_hours,
                    "disconnection_reason": reason,
                    "sentiment": analysis.get("user_sentiment"),
                    "recording_url": call.get("recording_url"),
                    "has_transcript": bool(call.get("transcript")),
                    "retell_agent_id": call.get("agent_id"),
                },
            )
        ]
