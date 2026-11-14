import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import Base, engine
from .routers import dashboard, ingest
from .services.live import broadcaster


@asynccontextmanager
async def lifespan(app: FastAPI):
    broadcaster.bind(asyncio.get_running_loop())
    if settings.database_url.startswith("sqlite"):
        Base.metadata.create_all(engine)  # tests and quick demos; Postgres uses Alembic
    yield


app = FastAPI(title="Agent Hub API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(ingest.router)
app.include_router(dashboard.router)


@app.get("/health")
def health():
    return {"ok": True}
