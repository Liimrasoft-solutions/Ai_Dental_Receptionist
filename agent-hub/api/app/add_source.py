"""Register a new server that is allowed to send events.

    python -m app.add_source --id stedi-agent --agent verification [--callback https://...]

Prints the secret once. Store it in the sender's secrets, never in git.
"""
import argparse
import secrets

from .db import SessionLocal
from .models import Source

p = argparse.ArgumentParser()
p.add_argument("--id", required=True)
p.add_argument("--agent", required=True, help="e.g. verification, marketing, or a new agent key")
p.add_argument("--callback", default=None, help="Where we POST staff actions (optional)")
a = p.parse_args()
secret = secrets.token_urlsafe(32)
with SessionLocal() as db:
    db.merge(Source(id=a.id, kind="signed", agent=a.agent, secret=secret, callback_url=a.callback))
    db.commit()
print(f"Source '{a.id}' can now send events for agent '{a.agent}' to POST /v1/ingest/{a.id}")
print(f"Secret (shown once): {secret}")
