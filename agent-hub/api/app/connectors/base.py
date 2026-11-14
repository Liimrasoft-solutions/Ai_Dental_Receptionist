"""A connector turns one outside system's payload into our EventIn format.

To plug in a new server (a vendor, or another of our agents):
  1. If it can send our normalized format, give it a Source with kind="signed". No code needed.
  2. If it has its own webhook format (like Retell), add a module here with
     verify() and to_events(), register it in registry.py, and add a route in routers/ingest.py.
"""
from typing import Protocol

from sqlalchemy.orm import Session

from ..schemas import EventIn


class Connector(Protocol):
    kind: str

    def verify(self, raw_body: bytes, headers: dict[str, str]) -> bool: ...

    def to_events(self, payload: dict, db: Session) -> list[EventIn]: ...
