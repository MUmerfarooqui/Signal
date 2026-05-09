# Signal — System Architecture

## Overview

Signal is a two-service application: a Next.js 16 frontend and a FastAPI backend. The backend handles all ingestion, AI reasoning, and brief generation. The frontend displays briefs, the Pulse feed, and connector setup.

## High-Level Data Flow

```
External Tools               Backend (FastAPI + Celery)          Frontend (Next.js)
──────────────               ──────────────────────────          ──────────────────
Zendesk  ──┐  OAuth + sync   ┌──────────────────────┐
Linear   ──┤ ──────────────> │  Connectors          │
Slack    ──┤                 │  zendesk.py          │
           └                 └──────────┬───────────┘
                                        │ normalize → RawEvent
                                        ▼
                             ┌──────────────────────┐
                             │  embed_events (Celery)│  OpenAI text-embedding-3-small
                             │  Batches of 500       │  → pgvector
                             └──────────┬────────────┘
                                        │
                              ┌─────────┴─────────┐
                              ▼                   ▼
                  ┌───────────────────┐  ┌──────────────────┐
                  │  detect_pulse     │  │  generate_brief  │
                  │  (after every     │  │  (weekly Celery  │
                  │   embed run)      │  │   beat, or POST) │
                  │  HDBSCAN, 1.5×    │  │                  │
                  │  threshold, no    │  │  cluster → Claude│
                  │  LLM              │  │  → Insight rows  │
                  └────────┬──────────┘  └────────┬─────────┘
                           │                      │
                           ▼                      ▼
                  InsightFeedItems           Brief + Insights
                                            + EvidenceRefs
                                                  │
                                          ┌───────┴───────┐
                                          ▼               ▼
                                    REST API          Resend email
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │  Next.js Dashboard  │
                              │  /dashboard  Briefs │
                              │  /pulse      Feed   │
                              │  /connectors Setup  │
                              └─────────────────────┘
```

## Backend Components

### Connectors (`backend/app/connectors/`)

Each connector handles OAuth, full sync, incremental sync, and normalises responses into `RawEvent`.

`RawEvent` is the common schema all connectors write to:
```python
source: str        # "zendesk", "linear", "slack"
source_id: str     # original ID in source system
event_type: str    # "ticket", "issue", "message"
content: str       # normalised text
metadata_: dict    # source-specific fields (status, priority, url)
embedding: vector  # pgvector — populated by embed_events
```

Built: `zendesk.py` · Planned: `linear.py`

### Workers (`backend/workers/`)

| Task | Trigger | Description |
|---|---|---|
| `embed_events` | After every sync | Vectorise new RawEvents in batches of 500 |
| `detect_pulse` | After every embed | Cluster 24h events, surface spikes ≥ 1.5× daily average |
| `generate_brief` | Weekly (Mon 08:00) or manual POST | Full reasoning pipeline → Brief |
| `dispatch_all_orgs` | Celery beat | Fan-out: fires `generate_brief` per active org |

### Reasoning Pipeline (`backend/workers/`)

Three stages — only the last touches Claude:

1. **Clustering** (`cluster.py`) — HDBSCAN over pgvector embeddings. Groups similar RawEvents into themes. No LLM, no API cost. Used by both `detect_pulse` and `generate_brief`.

2. **Pulse detection** (`pulse.py`) — Compares 24h cluster sizes to 7-day daily average. Threshold: ≥ 1.5×. Writes `InsightFeedItem` rows. Runs after every embed, not just weekly.

3. **Insight generation** (`reason.py`) — Claude Sonnet with prompt caching. Receives cluster summaries, returns ranked insights with category, title, explanation, suggested action, confidence (0–1), affected ticket count, and evidence citations.

### API Routes (`backend/app/api/routes/`)

| Route | Description |
|---|---|
| `POST /orgs` | Create org + owner membership |
| `GET /orgs/me` | Get caller's org |
| `GET /connectors?org_id=` | List connectors |
| `GET /connectors/zendesk/authorize` | Start Zendesk OAuth |
| `GET /connectors/zendesk/callback` | Complete OAuth, store tokens |
| `POST /connectors/sync` | Trigger manual sync |
| `GET /briefs?org_id=` | List briefs |
| `GET /briefs/{id}` | Brief detail with insights + evidence |
| `POST /briefs/generate` | Manually trigger brief generation |
| `GET /pulse?org_id=` | Live feed items (non-expired, newest first) |

### Auth

Clerk-issued JWTs verified via JWKS on every request. `get_current_user_id` dependency extracts the `sub` claim (Clerk user ID).

## Frontend Components (`frontend/app/`)

| Route | Type | Description |
|---|---|---|
| `/` | Server | Landing page — sign up / sign in CTAs |
| `/sign-in/[[...rest]]` | Static | Clerk sign-in component |
| `/sign-up/[[...rest]]` | Static | Clerk sign-up component |
| `/onboarding` | Client | Create org form |
| `/(app)/dashboard` | Server | Briefs list |
| `/(app)/briefs/[id]` | Server | Brief detail: insights + evidence |
| `/(app)/pulse` | Server | Live Pulse feed |
| `/(app)/connectors` | Server | Connector status + Zendesk OAuth |

## Database Schema

```
organizations       — name, plan, settings (JSON — includes brief_email)
users               — clerk_id, email, name
organization_members — org_id, user_id, role
oauth_credentials   — connector tokens (encrypted)
connectors          — per-org connector config, status, last_synced_at
sync_cursors        — incremental sync state per connector
raw_events          — all ingested data + pgvector embeddings
insight_feed_items  — pulse signals (severity, ticket_count, expires_at)
briefs              — generated briefs (status, period, generated_at)
insights            — per-brief: rank, category, title, confidence, affected_count
evidence_refs       — insight → raw_event citation (excerpt, url)
brief_deliveries    — delivery log (channel, recipient, status, sent_at)
```

## Pulse vs Brief — Key Difference

| | Pulse | Brief |
|---|---|---|
| Frequency | After every sync (≤6h) | Weekly |
| Latency | Minutes after a spike | Up to 7 days |
| LLM cost | Zero | Claude Sonnet call |
| Depth | Headline + count | Full insight + evidence + action |
| Purpose | Catch fast-moving issues | Structured weekly review |

## Security Notes

- OAuth tokens stored encrypted via Fernet/AES-256 in `oauth_credentials`
- All endpoints require Clerk JWT
- No raw event content in API responses — only excerpts via `EvidenceRef`
- SOC 2 Type II is a post-MVP milestone
