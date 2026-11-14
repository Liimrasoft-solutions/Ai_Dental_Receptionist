"""Fills the database with made-up sample data so the screens have something to show.

    python -m app.seed            # add locations, sources and 30 days of sample events
    python -m app.seed --clear    # remove sample events first

Every sample event carries data.sample = true and the dashboard shows a banner while any are present.
"""
import random
import sys
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select

from .db import Base, SessionLocal, engine
from .models import Event, Location, Source
from .schemas import EventIn
from .services.ingest import upsert_event

rnd = random.Random(7)
NOW = datetime.now(timezone.utc)
LOCS = ["garland", "plano"]
INITIALS = ["J. M.", "R. S.", "A. K.", "L. P.", "D. T.", "M. R.", "S. H.", "C. V.", "E. G."]


def at(days_ago: float, hour: int | None = None) -> datetime:
    t = NOW - timedelta(days=days_ago)
    if hour is not None:
        t = t.replace(hour=hour, minute=rnd.randint(0, 59))
    return min(t, NOW)


def ev(source: str, **kw) -> tuple[str, EventIn]:
    kw.setdefault("location_id", rnd.choice(LOCS))
    kw["data"] = {**kw.get("data", {}), "sample": True}
    return source, EventIn(**kw)


def calls():
    outcomes = ["booked_new"] * 14 + ["booked_followup"] * 18 + ["info"] * 46 + ["transferred"] * 14 + ["emergency"] * 2 + ["failed"] * 6
    summaries = {
        "booked_new": "New patient booked for a cleaning",
        "booked_followup": "Follow-up visit booked",
        "info": "Asked about hours and accepted insurance",
        "transferred": "Billing question, sent to front desk",
        "emergency": "Severe tooth pain, sent to staff right away",
        "failed": "Caller hung up during greeting",
    }
    for d in range(30):
        for i in range(rnd.randint(30, 52)):
            o = rnd.choice(outcomes)
            hour = rnd.choice([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
            dur = rnd.randint(40, 300) if o != "failed" else rnd.randint(5, 30)
            yield ev("retell", external_id=f"call_{d}_{i}", agent="receptionist", type="call",
                     status={"transferred": "transferred", "emergency": "needs_staff" if d < 1 else "transferred",
                             "failed": "failed"}.get(o, "done"),
                     occurred_at=at(d, hour), summary=summaries[o], cost_usd=round(dur / 60 * 0.174, 3),
                     data={"outcome": o, "language": "es" if rnd.random() < 0.3 else "en", "duration_s": dur,
                           "after_hours": hour < 8 or hour >= 17,
                           "disconnection_reason": "user_hangup" if o != "failed" else rnd.choice(["user_hangup", "error_llm_websocket_open", "dial_no_answer"])})


def checks():
    insurers = ["Delta Dental PPO", "MetLife", "Cigna Dental", "Aetna Dental", "Guardian"]
    for i in range(300):
        d = rnd.uniform(0, 30)
        ins = rnd.choice(insurers)
        method = "phone" if rnd.random() < 0.17 else "electronic"
        r = rnd.random() - (0.15 if ins == "Guardian" else 0)
        status, result = ("done", f"Active, annual max ${rnd.choice([1000, 1200, 1500, 2000]):,}") if r > 0.08 else \
            ("needs_staff", "Plan inactive, call the patient") if r > 0.03 else ("failed", "Insurer did not answer")
        if d < 0.5 and rnd.random() < 0.3:
            status, result = "waiting", "Check in progress"
        yield ev("insurance-agent", external_id=f"chk_{i}", agent="verification", type="check", status=status,
                 occurred_at=at(d), patient_ref=rnd.choice(INITIALS), summary=result,
                 cost_usd=0.30 if method == "electronic" else 3.48,
                 data={"insurer": ins, "method": method, "duration_s": 60 if method == "electronic" else 1080,
                       "visit_at": at(d - 2, rnd.randint(8, 16)).isoformat() if d > 2 else (NOW + timedelta(days=rnd.randint(1, 3))).replace(hour=rnd.randint(8, 16), minute=0).isoformat(),
                       "before_visit_day": rnd.random() < 0.92})


def marketing():
    srcs = ["Google search"] * 24 + ["Google Business"] * 18 + ["Ads"] * 12 + ["Social"] * 6 + ["Referral"] * 4
    for i in range(64):
        yield ev("marketing-agent", external_id=f"lead_{i}", agent="marketing", type="lead", occurred_at=at(rnd.uniform(0, 30)),
                 summary="New lead", data={"source": rnd.choice(srcs), "booked": rnd.random() < 0.27})
    for w in range(4):
        yield ev("marketing-agent", external_id=f"spend_{w}", agent="marketing", type="ad_spend", occurred_at=at(w * 7 + 1),
                 summary="Weekly ad spend", data={"amount": 607.5})
    posts = [("Spanish new-patient offer", "Facebook", "needs_staff"), ("Holiday hours post", "Google Business", "needs_staff"),
             ("Whitening ad text", "Google Ads", "done"), ("Reply to 4-star review", "Google", "needs_staff"),
             ("Teeth cleaning tips", "Instagram", "done")]
    for i, (title, ch, st) in enumerate(posts):
        yield ev("marketing-agent", external_id=f"post_{i}", agent="marketing", type="post", status=st, occurred_at=at(i * 0.7),
                 summary=title, data={"channel": ch, "state": "draft" if st == "needs_staff" else "published"})
    for i, (r, text) in enumerate([(5, "Easy to book, they spoke Spanish with my mother."), (5, "Quick visit, clear price before treatment."),
                                   (3, "Waited 20 minutes."), (5, "Friendly front desk and fast cleaning.")]):
        yield ev("marketing-agent", external_id=f"review_{i}", agent="marketing", type="review", occurred_at=at(i * 2 + 0.2),
                 summary=text, data={"rating": r})


def forms():
    kinds = ["New patient", "Medical history", "Consent"]
    flags = [None] * 30 + ["Takes a blood thinner", "Allergy: penicillin", "Pregnant"]
    for i in range(198):
        d = rnd.uniform(0, 30)
        state = rnd.choices(["completed", "opened", "sent"], [171, 13, 14])[0]
        flag = rnd.choice(flags) if state == "completed" else None
        yield ev("forms-agent", external_id=f"form_{i}", agent="health_records", type="form",
                 status="needs_staff" if flag and d < 3 else "done" if state == "completed" else "waiting",
                 occurred_at=at(d), patient_ref=rnd.choice(INITIALS), summary=flag or f"{state.capitalize()} form",
                 cost_usd=0.02,
                 data={"form": rnd.choice(kinds), "language": "es" if rnd.random() < 0.32 else "en", "state": state,
                       "saved": state == "completed" and rnd.random() > 0.02, "before_visit": rnd.random() < 0.88,
                       "fill_seconds": rnd.randint(200, 560), "flag": flag,
                       "visit_at": (at(d - 1, rnd.randint(8, 16))).isoformat()})


def alerts():
    for i, (agent, text, lvl) in enumerate([
        ("receptionist", "Plano: Open Dental slow to respond", "warning"),
        ("verification", "Guardian failing 3x more than usual", "warning"),
        ("receptionist", "Retell minutes at 80% of budget", "info"),
    ]):
        yield ev({"receptionist": "retell", "verification": "insurance-agent"}[agent], external_id=f"alert_{i}", agent=agent,
                 type="alert", status="needs_staff", occurred_at=at(i * 0.2), summary=text, data={"level": lvl})


def main() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if "--clear" in sys.argv:
            ids = [e.id for e in db.scalars(select(Event)) if (e.data or {}).get("sample")]
            if ids:
                db.execute(delete(Event).where(Event.id.in_(ids)))
                db.commit()
            print(f"Removed {len(ids)} sample events")
        for loc in [Location(id="garland", name="Garland", phone_number="+19725550100"),
                    Location(id="plano", name="Plano", phone_number="+19725550200")]:
            db.merge(loc)
        for src in [Source(id="retell", kind="retell", agent="receptionist"),
                    Source(id="insurance-agent", kind="signed", agent="verification", secret="dev-secret-insurance"),
                    Source(id="marketing-agent", kind="signed", agent="marketing", secret="dev-secret-marketing"),
                    Source(id="forms-agent", kind="signed", agent="health_records", secret="dev-secret-forms")]:
            if not db.get(Source, src.id):
                db.add(src)
        db.commit()
        n = 0
        for gen in (calls, checks, marketing, forms, alerts):
            for source, e in gen():
                upsert_event(db, source, e)
                n += 1
        print(f"Saved {n} sample events")


if __name__ == "__main__":
    main()
