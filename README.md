# Signal

Signal is an AI-native product intelligence system for software teams. It connects to your tools (Zendesk, Linear), ingests data continuously, and delivers a weekly **Intelligence Brief** — a prioritized, evidence-backed set of product insights — without anyone having to ask for it.

The core loop: **Ingest → Embed → Cluster → Reason → Deliver**

Tickets come in, get converted to vectors, grouped into themes by HDBSCAN, reasoned over by Claude Sonnet, and sent to your inbox every Monday.

Between briefs, **Pulse** surfaces real-time signals — spikes above 1.5× your daily average — with no LLM cost, minutes after they appear in your support queue.

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

ZENDESK_CLIENT_ID=       # Signal's OAuth app client ID (register once at developer.zendesk.com)
ZENDESK_CLIENT_SECRET=   # Signal's OAuth app client secret

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
| GET | `/pulse` | Live Pulse feed (non-expired signals, newest first) |

Interactive docs available at `http://localhost:8000/docs` (development only).

---

## Project Structure

```
signal/
├── frontend/
│   ├── app/
│   │   ├── page.tsx                    # Landing page
│   │   ├── (auth)/
│   │   │   ├── sign-in/[[...rest]]/    # Clerk sign-in
│   │   │   └── sign-up/[[...rest]]/    # Clerk sign-up
│   │   └── (app)/
│   │       ├── layout.tsx              # Sidebar + auth guard
│   │       ├── dashboard/              # Briefs list
│   │       ├── briefs/[id]/            # Brief detail: insights + evidence
│   │       ├── pulse/                  # Live Pulse feed
│   │       └── connectors/             # Connector setup + OAuth
│   ├── components/
│   │   ├── sidebar.tsx                 # Navigation + org name + dark mode toggle
│   │   └── theme-provider.tsx          # Class-based dark mode (light default)
│   └── lib/
│       └── api.ts                      # Typed API client
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── orgs.py
│   │   │   │   ├── connectors.py
│   │   │   │   ├── briefs.py
│   │   │   │   └── pulse.py            # GET /pulse live feed
│   │   │   └── deps.py                 # Clerk JWT auth dependency
│   │   ├── connectors/                 # Zendesk OAuth + sync logic
│   │   ├── models/                     # SQLAlchemy models (12 tables)
│   │   └── db/
│   │       └── migrations/             # Alembic migration versions
│   ├── workers/
│   │   ├── celery_app.py               # Celery instance + beat schedule
│   │   ├── embed.py                    # OpenAI embedding task → chains pulse
│   │   ├── cluster.py                  # HDBSCAN clustering
│   │   ├── pulse.py                    # Spike detection (1.5× threshold, no LLM)
│   │   ├── reason.py                   # Claude reasoning
│   │   ├── deliver.py                  # Resend email delivery
│   │   └── brief.py                    # Brief orchestration task
│   ├── seed.py                         # Idempotent mock data seed
│   ├── start.py                        # Single-command launcher
│   └── requirements.txt
└── docs/                               # Architecture, product research, MVP scope
```

---

## Mock data (development)

To populate the dashboard with realistic briefs and Pulse signals without connecting a live Zendesk account:

```bash
cd backend
python seed.py              # seeds first org found
python seed.py <org_id>     # seeds a specific org
```

The script is **idempotent** — it checks whether briefs and pulse items already exist for the org before inserting anything. Running it multiple times is safe.

What it seeds:
- **3 Intelligence Briefs** (1, 2, and 3 weeks ago) with 9 total insights across all six categories (recurring pain, feature gap, onboarding friction, reliability issue, workflow blocker, churn signal), each with evidence excerpts and mock ticket URLs
- **5 Pulse feed items** (2 high severity, 2 medium, 1 low) spread across the last 24 hours

---

## Adding a schema change

1. Edit the relevant model in `backend/app/models/`
2. Generate a migration: `alembic revision --autogenerate -m "description"`
3. Apply it: `alembic upgrade head`
4. Verify nothing is pending: `alembic check`
