# Signal — System Architecture

## Overview

Signal is a two-service application: a Next.js frontend and a FastAPI backend. The backend does all the heavy lifting — ingestion, AI reasoning, and brief generation. The frontend is a thin layer that displays briefs and the insight feed.

## High-Level Data Flow

```
External Tools                  Backend                           Frontend
─────────────                  ───────                           ────────
Zendesk   ──┐                  ┌─────────────────────────┐
Linear    ──┤  OAuth + Webhooks │  Connectors             │
Slack     ──┤ ────────────────> │  (normalize → RawEvent) │
Amplitude ──┤                  └───────────┬─────────────┘
Gong      ──┘                              │
                                           ▼
                                  ┌─────────────────┐
                                  │  Ingestion Jobs  │  (Celery)
                                  │  - Scheduled     │
                                  │  - Webhook-driven│
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │  PostgreSQL      │
                                  │  + pgvector      │
                                  │  (events,        │
                                  │   embeddings,    │
                                  │   briefs)        │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │  Reasoning Layer │
                                  │  - HDBSCAN cluster│
                                  │  - Cross-source  │  ← Claude Sonnet
                                  │    correlation   │
                                  │  - Insight gen   │  ← Claude Sonnet
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │  Brief Generator │
                                  │  - Assemble      │
                                  │  - Attach sources│
                                  │  - Store + send  │
                                  └────────┬────────┘
                                           │
                               ┌───────────┴──────────┐
                               ▼                      ▼
                          Email (Resend)        REST API  ──────> Next.js Dashboard
                          Slack (webhook)                         - Brief viewer
                                                                  - Insight feed
                                                                  - Evidence drill-down
                                                                  - Q&A (V2)
```

## Backend Components

### Connectors (`backend/app/connectors/`)

Each connector is responsible for:
- OAuth flow (authorize, callback, token storage)
- Initial full sync (paginated historical pull)
- Incremental sync (delta since last cursor)
- Normalizing raw API responses into `RawEvent` schema

`RawEvent` is the common schema all connectors write to:
```python
class RawEvent(Base):
    id: UUID
    org_id: UUID
    source: str          # "zendesk", "linear", "slack", etc.
    source_id: str       # original ID in the source system
    event_type: str      # "ticket", "issue", "message", "transcript_segment"
    content: str         # normalized text content
    metadata: dict       # source-specific fields (status, priority, author, url)
    created_at: datetime
    ingested_at: datetime
    embedding: vector    # pgvector — generated after ingestion
```

MVP connectors: `zendesk.py`, `linear.py`

### Ingestion Jobs (`backend/workers/`)

Celery tasks:
- `sync_connector(org_id, connector)` — scheduled every 6 hours, pulls deltas
- `embed_events(org_id, batch)` — vectorizes new RawEvents using OpenAI `text-embedding-3-small`; stores vectors in pgvector
- `generate_brief(org_id)` — weekly scheduled task that triggers the reasoning pipeline

### Reasoning Layer (`backend/app/reasoning/`)

Three distinct stages — only the last two touch Claude:

1. **Clustering (no LLM)** — HDBSCAN over pgvector embeddings. Groups semantically similar RawEvents into themes per source. Pure math: fast, cheap, no API calls. Each cluster gets a centroid and a list of member event IDs.

2. **Cross-source correlation (Claude Sonnet)** — given a set of cluster summaries from Zendesk + Linear, Claude identifies patterns that span sources (e.g., "Zendesk cluster about invite flow" correlates with "Linear backlog of permissions issues"). Called once per brief cycle. Prompt caching: cluster summaries are the cached prefix, reasoning instructions are the variable suffix.

3. **Insight scoring + generation (Claude Sonnet)** — for each correlated pattern, Claude produces a ranked insight: title, plain-language explanation, suggested action, confidence score (0–1), and EvidenceRef citations. Scores are weighted by: frequency of corroborating events, recency, and source diversity (multi-source > single-source).

### Brief Assembly (`backend/app/brief/`)

Takes the top 3–7 scored insights and assembles a structured `Brief` object:
```python
class Brief(Base):
    id: UUID
    org_id: UUID
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    insights: list[Insight]  # JSON
    status: str              # "draft", "sent"

class Insight:
    rank: int
    title: str
    explanation: str
    suggested_action: str
    confidence: float        # 0–1
    evidence: list[EvidenceRef]

class EvidenceRef:
    raw_event_id: UUID
    source: str
    excerpt: str
    url: str                 # deep link back to source tool
```

### API (`backend/app/api/`)

RESTful endpoints:
- `POST /orgs/{id}/connectors` — connect a new integration
- `GET /orgs/{id}/briefs` — list briefs
- `GET /orgs/{id}/briefs/{brief_id}` — brief detail with full evidence
- `GET /orgs/{id}/insights/feed` — real-time insight feed
- `POST /orgs/{id}/briefs/generate` — manual trigger (admin/dev use)
- `GET /orgs/{id}/events` — raw event search (for Q&A, V2)

## Frontend Components

Pages (Next.js App Router):
- `/` — landing / onboarding
- `/dashboard` — insight feed (between briefs)
- `/briefs` — list of past briefs
- `/briefs/[id]` — brief detail: insights + evidence drill-down
- `/settings/integrations` — connect/manage data sources
- `/settings/delivery` — configure email/Slack brief delivery

## Database Schema (key tables)

```
organizations       — org config, plan, settings
users               — members, roles
oauth_credentials   — encrypted tokens per connector per org
raw_events          — all ingested data (+ pgvector embeddings)
briefs              — generated briefs (JSON insights payload)
brief_deliveries    — delivery log (email/Slack, sent_at, opened_at)
```

## Security Notes

- OAuth tokens encrypted at rest (Fernet/AES-256)
- All API endpoints require org-scoped JWT
- Slack ingestion: only configured channels, never DMs
- No raw event content exposed in API responses — only excerpts via EvidenceRef
- SOC 2 Type II is a V2 milestone

## Scaling Considerations (post-MVP)

- Ingestion jobs are already async (Celery) — scale workers independently
- Embeddings can be batched and offloaded
- Brief generation is compute-heavy but infrequent — can run on a beefy single worker
- pgvector handles moderate scale; migrate to Pinecone/Weaviate if vector search becomes a bottleneck
