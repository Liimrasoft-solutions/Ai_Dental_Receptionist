# Sending events to Agent Hub

Every agent, ours or a vendor's, tells the dashboard what it did by sending **events** in one shared format.
The dashboard never calls agents to ask; agents report in. That is what lets us add or swap a server without touching the screens.

## Two ways in

**1. Our format, signed (any new server).** Register the server once:

```bash
cd api && python -m app.add_source --id stedi-agent --agent verification --callback https://insurance.internal/hub-actions
```

It prints a secret. The server then POSTs to `/v1/ingest/stedi-agent` with two headers:

- `X-Hub-Timestamp`: Unix seconds
- `X-Hub-Signature`: `sha256=` + hex HMAC-SHA256 of `{timestamp}.{raw body}` using the secret

Requests more than 5 minutes old are refused. A source can only send events for the agent it was registered for.

**2. A vendor's own webhook format (like Retell).** Write a connector in `api/app/connectors/` with `verify()` and `to_events()`, and add a route in `routers/ingest.py`. `retell.py` is the example.

## The event

| Field | Required | Notes |
|---|---|---|
| `external_id` | yes | Your id for the job. Sending the same id again updates the event, so retries are safe. |
| `agent` | yes | `receptionist`, `verification`, `marketing`, `health_records`, or a new key such as `recalls`. A new key gets its own page automatically. |
| `type` | yes | What happened: `call`, `check`, `form`, `lead`, `post`, `review`, `ad_spend`, `alert`, … |
| `status` | no | `done` (default), `needs_staff`, `failed`, `waiting`, `transferred`. `needs_staff` puts it in the "Needs a person" list. |
| `occurred_at` | yes | ISO 8601 with a timezone. |
| `location_id` | no | `garland`, `plano`, … |
| `summary` | no | One line staff will read. Max 500 characters. |
| `patient_ref` | no | Initials only, never a name. Full details stay in Open Dental. |
| `cost_usd` | no | What this job cost us, for the monthly budget bar. |
| `data` | no | Anything agent-specific. See below. |

Fields in `data` that the built-in pages read:

- **verification** (`type: check`): `insurer`, `method` (`electronic` or `phone`), `duration_s`, `visit_at`, `before_visit_day`
- **marketing**: `lead` → `source`, `booked`; `post` → `channel`, `state`; `review` → `rating`; `ad_spend` → `amount`
- **health_records** (`type: form`): `form`, `language`, `state` (`sent`, `opened`, `completed`), `saved`, `before_visit`, `fill_seconds`, `flag`, `visit_at`
- **alerts** (`type: alert`, any agent): `level` (`info` or `warning`)

## Example sender (Python)

```python
import hashlib, hmac, json, time, httpx

SECRET = "..."  # from add_source, kept in the sender's secrets store
event = {
    "external_id": "chk_8812",
    "agent": "verification",
    "type": "check",
    "status": "needs_staff",
    "occurred_at": "2026-11-13T15:31:00Z",
    "location_id": "plano",
    "summary": "Plan inactive, call the patient",
    "patient_ref": "A. K.",
    "cost_usd": 0.30,
    "data": {"insurer": "Cigna Dental", "method": "electronic", "duration_s": 48},
}
body = json.dumps(event).encode()
ts = str(int(time.time()))
sig = "sha256=" + hmac.new(SECRET.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()
httpx.post("https://hub.example.com/v1/ingest/stedi-agent", content=body,
           headers={"Content-Type": "application/json", "X-Hub-Timestamp": ts, "X-Hub-Signature": sig})
```

## Actions coming back

If a source has a `callback_url`, the hub POSTs to it, signed the same way, when staff act:

- `{"action": "resolved", "external_id": "...", "by": "...", "note": "..."}` when staff press Approve, Mark reviewed, etc.
- `{"action": "pause", "paused": true, "by": "..."}` when staff pause the agent.

The marketing agent should publish a post only after it receives `resolved` for it.

## Setting up Retell

1. In Retell, set the agent's webhook URL to `https://<hub address>/v1/webhooks/retell`.
2. Put the Retell API key that has the webhook badge in `RETELL_API_KEY`.
3. Add two post-call analysis fields to the Retell agent: `outcome` (one of `booked_new`, `booked_followup`, `info`, `transferred`, `emergency`, `failed`) and `language` (`en` or `es`).
4. Give each office its Retell number in the `locations` table (`phone_number`), or pass `location_id` in the call metadata.

Check the field names in `connectors/retell.py` against Retell's current webhook docs before go-live.
