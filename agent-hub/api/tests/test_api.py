import json
import os
import time

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["RETELL_API_KEY"] = "test-retell-key"
if os.path.exists("test.db"):
    os.remove("test.db")

from fastapi.testclient import TestClient  # noqa: E402
from retell.lib.webhook_auth import symmetric  # noqa: E402

from app import seed  # noqa: E402
from app.main import app  # noqa: E402
from app.security import sign  # noqa: E402

seed.main()
client = TestClient(app)


def test_overview_has_all_four_agents():
    r = client.get("/v1/overview").json()
    assert {t["agent"] for t in r["tiles"]} >= {"receptionist", "verification", "marketing", "health_records"}
    assert r["sample_data"] is True
    assert r["needs_person"]


def test_every_agent_page_renders():
    for agent in ["receptionist", "verification", "marketing", "health_records"]:
        r = client.get(f"/v1/agents/{agent}?location=garland&days=7")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["kpis"] and body["table"]["rows"]


def test_signed_ingest_and_new_agent_gets_a_page():
    from app.db import SessionLocal
    from app.models import Source
    with SessionLocal() as db:
        db.merge(Source(id="recall-bot", kind="signed", agent="recalls", secret="s3cret"))
        db.commit()
    body = json.dumps({"external_id": "r1", "agent": "recalls", "type": "recall_call", "status": "needs_staff",
                       "occurred_at": "2026-11-13T10:00:00Z", "summary": "Patient asked for a callback"}).encode()
    ts = str(int(time.time()))
    bad = client.post("/v1/ingest/recall-bot", content=body, headers={"X-Hub-Timestamp": ts, "X-Hub-Signature": "sha256=nope"})
    assert bad.status_code == 401
    ok = client.post("/v1/ingest/recall-bot", content=body, headers={"X-Hub-Timestamp": ts, "X-Hub-Signature": sign("s3cret", ts, body)})
    assert ok.status_code == 200, ok.text
    assert any(a["key"] == "recalls" for a in client.get("/v1/meta").json()["agents"])
    assert client.get("/v1/agents/recalls?days=365").status_code == 200


def test_source_cannot_write_for_another_agent():
    body = json.dumps({"external_id": "x", "agent": "receptionist", "type": "call",
                       "occurred_at": "2026-11-13T10:00:00Z"}).encode()
    ts = str(int(time.time()))
    r = client.post("/v1/ingest/insurance-agent", content=body,
                    headers={"X-Hub-Timestamp": ts, "X-Hub-Signature": sign("dev-secret-insurance", ts, body)})
    assert r.status_code == 403


def test_retell_webhook_upserts_one_call():
    start = int(time.time() * 1000) - 120_000
    payload = {"event": "call_ended", "call": {
        "call_id": "abc123", "direction": "inbound", "from_number": "+12145551234", "to_number": "+19725550200",
        "start_timestamp": start, "end_timestamp": start + 95_000, "disconnection_reason": "user_hangup",
        "call_cost": {"combined_cost": 17}}}
    for event in ("call_ended", "call_analyzed"):
        payload["event"] = event
        if event == "call_analyzed":
            payload["call"]["call_analysis"] = {"call_summary": "Booked a cleaning",
                                                "custom_analysis_data": {"outcome": "booked_new", "language": "es"}}
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
        sig = symmetric["sign"](body, "test-retell-key")
        r = client.post("/v1/webhooks/retell", content=body, headers={"x-retell-signature": sig})
        assert r.status_code == 204, r.text
    rows = [r for r in client.get("/v1/agents/receptionist?location=plano&days=1").json()["table"]["rows"]
            if r["summary"] == "Booked a cleaning"]
    assert len(rows) == 1 and rows[0]["outcome"] == "Booked, new patient"


def test_retell_rejects_bad_signature():
    r = client.post("/v1/webhooks/retell", content=b'{"event":"call_ended","call":{"call_id":"z"}}',
                    headers={"x-retell-signature": "v=1,d=" + "0" * 64})
    assert r.status_code == 401


def test_resolve_and_pause():
    item = client.get("/v1/overview").json()["needs_person"][0]
    assert client.post(f"/v1/events/{item['id']}/resolve", json={"note": "called back"}).status_code == 200
    assert client.post("/v1/agents/marketing/pause", json={"paused": True}).json()["paused"] is True
    tiles = {t["agent"]: t for t in client.get("/v1/overview").json()["tiles"]}
    assert tiles["marketing"]["paused"] is True
