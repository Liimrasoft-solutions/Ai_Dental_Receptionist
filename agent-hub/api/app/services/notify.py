"""Tell a source about a staff action (approve, mark reviewed, pause), signed like inbound events.
Runs as a FastAPI background task; move to Celery/SQS when you need retries."""
import json
import logging
import time

import httpx

from ..security import sign

log = logging.getLogger("agent_hub.notify")


def send_action(callback_url: str, secret: str, action: dict) -> None:
    body = json.dumps(action, default=str).encode()
    ts = str(int(time.time()))
    try:
        httpx.post(
            callback_url,
            content=body,
            timeout=10,
            headers={
                "Content-Type": "application/json",
                "X-Hub-Timestamp": ts,
                "X-Hub-Signature": sign(secret, ts, body),
            },
        ).raise_for_status()
    except httpx.HTTPError as exc:
        log.warning("Callback to %s failed: %s", callback_url, exc)
