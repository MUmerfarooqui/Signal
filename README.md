# Signal

Signal is an AI-native product intelligence system for software teams. It connects to your tools (Zendesk, Linear), ingests data continuously, and delivers a weekly **Intelligence Brief** — a prioritized, evidence-backed set of product insights — without anyone having to ask for it.

The core loop: **Ingest → Embed → Cluster → Reason → Deliver**

Tickets come in, get converted to vectors, grouped into themes by HDBSCAN, reasoned over by Claude Sonnet, and sent to your inbox every Monday.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Frontend | Next.js 16, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.14 |
| Database | PostgreSQL + pgvector on Neon |
| Queue | Celery + Redis |
| Embeddings | OpenAI `text-embedding-3-small` |
| Reasoning | Anthropic Claude Sonnet |
| Auth | Clerk |
| Email | Resend |

---

## Prerequisites

- Python 3.12+
- Node.js 18+
- Docker Desktop (for Redis — must be running before starting the backend)
- A [Neon](https://neon.tech) PostgreSQL database
- A [Clerk](https://clerk.com) account (free tier)
- A Zendesk account with an OAuth app configured

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/MUmerfarooqui/Signal.git
cd Signal
```

### 2. Backend environment

```bash
cd backend
cp .env.example .env
```

Fill in `.env`:

```env
DATABASE_URL=            # Neon connection string (include ?sslmode=require&channel_binding=require)
REDIS_URL=redis://localhost:6379/0

CLERK_SECRET_KEY=        # from clerk.com → your app → API Keys
CLERK_PUBLISHABLE_KEY=   # from clerk.com → your app → API Keys

ZENDESK_CLIENT_ID=       # from your Zendesk OAuth app
ZENDESK_CLIENT_SECRET=   # from your Zendesk OAuth app
ZENDESK_SUBDOMAIN=       # e.g. yourcompany (without .zendesk.com)

OPENAI_API_KEY=          # from platform.openai.com
ANTHROPIC_API_KEY=       # from console.anthropic.com
```

### 3. Backend dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### 4. Run database migrations

```bash
cd backend
alembic upgrade head
```

### 5. Frontend environment

```bash
cd frontend
cp .env.local.example .env.local   # if it exists, otherwise create it
```

`.env.local` contents:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=   # same as backend CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY=                    # same as backend CLERK_SECRET_KEY
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 6. Frontend dependencies

```bash
cd frontend
npm install
```

---

## Running

### Backend (one command)

Make sure **Docker Desktop is open**, then:

```bash
cd backend
python start.py
```

This starts four processes together:
- **Redis** — via Docker, message broker for Celery
- **FastAPI** — API server on `http://localhost:8000`
- **Celery worker** — processes background jobs (embedding, brief generation)
- **Celery beat** — weekly brief schedule (Mondays 8am UTC)

You'll see `✓ Backend up and running` once all four are healthy.

`Ctrl+C` shuts everything down.

### Frontend

```bash
cd frontend
npm run dev
```

Runs on `http://localhost:3000`.

---

## API

Base URL: `http://localhost:8000/api/v1`

| Method | Route | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/orgs` | Create org (first-time signup) |
| GET | `/orgs/me` | Get current user's org |
| GET | `/connectors/zendesk/authorize` | Start Zendesk OAuth |
| GET | `/connectors/zendesk/callback` | Finish Zendesk OAuth |
| GET | `/connectors` | List connected integrations |
| POST | `/connectors/sync` | Trigger manual sync |
| GET | `/briefs` | List briefs for an org |
| GET | `/briefs/{id}` | Get brief with insights + evidence |
| POST | `/briefs/generate` | Manually trigger brief generation |

Interactive docs available at `http://localhost:8000/docs` (development only).

---

## Project Structure

```
signal/
├── frontend/                  # Next.js app
│   ├── app/                   # App router pages
│   ├── components/            # UI components
│   └── lib/                   # API client, types, utils
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/        # HTTP route handlers
│   │   │   └── deps.py        # Clerk JWT auth dependency
│   │   ├── connectors/        # Zendesk OAuth + sync logic
│   │   ├── models/            # SQLAlchemy models (12 tables)
│   │   └── db/
│   │       └── migrations/    # Alembic migration versions
│   ├── workers/
│   │   ├── celery_app.py      # Celery instance + beat schedule
│   │   ├── embed.py           # OpenAI embedding task
│   │   ├── cluster.py         # HDBSCAN clustering
│   │   ├── reason.py          # Claude reasoning
│   │   ├── deliver.py         # Resend email delivery
│   │   └── brief.py           # Orchestration task
│   ├── start.py               # Single-command launcher
│   └── requirements.txt
└── docs/                      # Architecture, product research, MVP scope
```

---

## Adding a schema change

1. Edit the relevant model in `backend/app/models/`
2. Generate a migration: `alembic revision --autogenerate -m "description"`
3. Apply it: `alembic upgrade head`
4. Verify nothing is pending: `alembic check`
