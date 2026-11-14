# Agent Hub

One dashboard for every AI agent at the practice: the Retell receptionist now, then insurance verification, marketing and health records.
Built to the November 2026 implementation plan (Next.js + FastAPI + Postgres, hosted on AWS).

```
Retell ──webhook──▶ ┐
Insurance agent ──▶ ├─ api/ (FastAPI) ── Postgres ──▶ web/ (Next.js) ── staff browser
Marketing agent ──▶ │   one event format          live updates (SSE)
Any new server ───▶ ┘   signed, per source        Approve / Mark reviewed / Pause ──▶ back to the agent
```

## Run it on your laptop

```bash
cp .env.example api/.env && cp .env.example .env
cp web/.env.example web/.env.local
docker compose up -d                       # Postgres and Redis

cd api
pip install -r requirements.txt
alembic upgrade head                       # create tables
python -m app.seed                         # 30 days of SAMPLE data (clearly bannered)
uvicorn app.main:app --reload              # API on :8000, docs at /docs

cd ../web
npm install && npm run dev                 # dashboard on :3001
```

Tests: `cd api && pytest`.

## Screens

- **Overview**: is every agent on (with a pause switch), what each did, calls per day, the "Needs a person" list, alerts and cost against budget.
- **One page per agent** at `/receptionist`, `/verification`, `/marketing`, `/health-records`: headline numbers, a daily chart, breakdowns, and a table with an action button on rows that need staff.

Filters (office, date range) live in the URL, so a link shows exactly what you saw.

## Keeping it open to other servers

- **New server, existing agent** (e.g. Stedi checks for verification): `python -m app.add_source`, then it sends signed events. No dashboard code. See `docs/EVENTS.md`.
- **New agent** (e.g. recall calls): register a source with a new agent key. It appears in the sidebar and gets a generic page from its first event. Add a summarizer in `api/app/services/summaries.py` when it needs its own numbers.
- **Vendor with its own webhook format**: add a connector in `api/app/connectors/` (see `retell.py`).
- **Swapping Retell** for another voice platform: write that platform's connector. Events, pages and history stay the same.

## Before real patient data

These are open on purpose in this first version and must be closed before Shifa goes live:

1. **Sign-in.** `AUTH_MODE=dev` lets anyone in as admin. Wire Cognito in `api/app/security.py` (`current_user`) and forward the token from `web/lib/api.ts`. Roles and per-office access are already enforced from the `User` object.
2. **BAAs** with every provider in the chain (AWS, Retell, any eligibility service), as the plan says.
3. **One API container for live updates.** The live stream is in-memory; use Redis pub/sub when you run more than one.
4. **Callbacks** run as background tasks with no retry; move them to Celery or SQS.
5. Restrict CORS to the real dashboard address and serve everything over HTTPS behind the load balancer.

Patient data rule built into the format: events carry initials only. Names, charts and full transcripts stay in Open Dental and Retell; the dashboard links to recordings rather than copying them.
