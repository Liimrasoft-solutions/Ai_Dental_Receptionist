"""Server-sent events for the live panel. One process only; use Redis pub/sub when you run several API containers."""
import asyncio
import json


class Broadcaster:
    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop | None = None
        self.queues: set[asyncio.Queue] = set()

    def bind(self, loop: asyncio.AbstractEventLoop) -> None:
        self.loop = loop

    def publish(self, message: dict) -> None:
        """Safe to call from sync route handlers running in the thread pool."""
        if not self.loop:
            return
        data = json.dumps(message, default=str)
        for q in list(self.queues):
            self.loop.call_soon_threadsafe(q.put_nowait, data)

    async def subscribe(self):
        q: asyncio.Queue = asyncio.Queue(maxsize=100)
        self.queues.add(q)
        try:
            while True:
                try:
                    yield f"data: {await asyncio.wait_for(q.get(), timeout=15)}\n\n"
                except asyncio.TimeoutError:
                    yield ": keep-alive\n\n"
        finally:
            self.queues.discard(q)


broadcaster = Broadcaster()
