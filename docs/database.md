# Signal — Database Design

## ORM: SQLAlchemy, not Prisma

Quick flag before the schema: **Prisma is TypeScript-native**. It works beautifully with Next.js but its Python client (`prisma-client-py`) is a community project that lags behind the official version and has known issues with Python 3.12+. Our backend is Python — the standard stack there is **SQLAlchemy + Alembic** (migrations). That's what we'll use.

Prisma never comes into play here. The frontend (Next.js) calls our FastAPI — it never touches the DB directly.

---

## Normalization — What We Did and Why

Normalization is the process of structuring a database to reduce redundancy and ensure data integrity. The standard forms are:

- **1NF** — no repeating groups; every cell holds one atomic value
- **2NF** — every non-key column depends on the *whole* primary key (matters for composite PKs)
- **3NF** — every non-key column depends *only* on the primary key, not on another non-key column (eliminates transitive dependencies)

We designed to **3NF** as the baseline, then made **deliberate, documented denormalizations** where query performance required it. Blind normalization can produce schemas that are theoretically clean but painfully slow in production.

### Deliberate denormalizations (and why)

| What | Where | Why |
|---|---|---|
| `source` on `raw_events` | `raw_events.source` duplicates `connectors.connector_type` | Vector similarity searches filter by source constantly. Adding a JOIN on every vector query would be expensive. We accept the redundancy. |
| `org_id` on `insights` | Also derivable via `brief → org_id` | Insights will eventually be queried across briefs (trend tracking). Putting `org_id` directly avoids a join on those queries. |
| `excerpt` + `url` on `evidence_refs` | Also on the source `raw_event` | The evidence drill-down UI needs these without fetching the full raw event. Avoids a second query per citation. |

Everything else is fully normalized.

---

## Tables

### `organizations`
The top-level tenant. Every piece of data in Signal is scoped to an org.

```
id              UUID        PK, default gen_random_uuid()
name            TEXT        NOT NULL
plan            TEXT        NOT NULL, default 'free'  -- free | pro | enterprise
settings        JSONB       NOT NULL, default '{}'    -- brief_frequency, delivery prefs, etc.
created_at      TIMESTAMPTZ NOT NULL, default now()
updated_at      TIMESTAMPTZ NOT NULL, default now()
```

---

### `users`
People who log into Signal. A user can belong to multiple orgs (future).

```
id              UUID        PK
email           TEXT        NOT NULL, UNIQUE
name            TEXT        NOT NULL
created_at      TIMESTAMPTZ NOT NULL, default now()
last_login_at   TIMESTAMPTZ
```

**Why email is on users, not org_members:** Email is a property of the person, not the membership. If someone joins two orgs they have one email, not two.

---

### `organization_members`
Junction table: which users belong to which orgs, and with what role.

```
org_id          UUID        FK → organizations, NOT NULL
user_id         UUID        FK → users, NOT NULL
role            TEXT        NOT NULL, default 'member'  -- owner | admin | member
joined_at       TIMESTAMPTZ NOT NULL, default now()

PRIMARY KEY (org_id, user_id)
```

**Why a junction table, not just `org_id` on users?** A user may be invited to multiple orgs. If we put `org_id` directly on `users`, a user is locked to one org forever. The junction table handles the many-to-many cleanly with no redundancy.

---

### `connectors`
A configured data source integration per org (e.g., "Acme Corp's Zendesk account").

```
id              UUID        PK
org_id          UUID        FK → organizations, NOT NULL
connector_type  TEXT        NOT NULL  -- zendesk | linear | slack | amplitude | gong | intercom | jira
status          TEXT        NOT NULL, default 'configuring'
                            -- configuring | active | syncing | error | disconnected
config          JSONB       NOT NULL, default '{}'  -- subdomain, channel IDs, etc. (non-secret)
last_synced_at  TIMESTAMPTZ
sync_error      TEXT        -- last error message if status = 'error'
created_at      TIMESTAMPTZ NOT NULL, default now()
updated_at      TIMESTAMPTZ NOT NULL, default now()

UNIQUE (org_id, connector_type)  -- one Zendesk per org, one Linear per org, etc.
```

**Why `config` is separate from `oauth_credentials`:** Config (subdomain, which Slack channels to monitor) is non-sensitive and queried often. Credentials (access/refresh tokens) are sensitive and queried rarely (only during sync). Keeping them in separate tables enforces least-privilege access — you can read connector status without ever touching the credentials table.

---

### `oauth_credentials`
Encrypted OAuth tokens. One row per connector.

```
id              UUID        PK
connector_id    UUID        FK → connectors, NOT NULL, UNIQUE
access_token    TEXT        NOT NULL  -- encrypted (Fernet)
refresh_token   TEXT                  -- encrypted, nullable
expires_at      TIMESTAMPTZ           -- nullable; some tokens don't expire
scopes          TEXT                  -- space-separated OAuth scopes granted
updated_at      TIMESTAMPTZ NOT NULL, default now()
```

**Why 1-to-1 with connectors?** Each connector has exactly one active token set. If a token is refreshed, we UPDATE this row — we don't insert a new one. History isn't needed here; the current token is all that matters.

---

### `sync_cursors`
Tracks where each connector's incremental sync is up to. Prevents re-ingesting old data.

```
id              UUID        PK
connector_id    UUID        FK → connectors, NOT NULL, UNIQUE
cursor_value    TEXT        NOT NULL  -- timestamp, page token, or last event ID (varies by API)
last_synced_at  TIMESTAMPTZ NOT NULL
events_ingested INTEGER     NOT NULL, default 0  -- count from last run (for monitoring)
created_at      TIMESTAMPTZ NOT NULL, default now()
updated_at      TIMESTAMPTZ NOT NULL, default now()
```

**Why separate from connectors?** Single responsibility. The connector record describes the integration config; the cursor describes where sync is up to. Mixing them violates 3NF — `cursor_value` depends on the sync state, not on the connector's identity.

---

### `raw_events`
**The core fact table.** Every piece of data ingested from any source lands here, normalized into a common schema. This will be the largest table by far.

```
id                      UUID        PK
org_id                  UUID        FK → organizations, NOT NULL
connector_id            UUID        FK → connectors, NOT NULL
source                  TEXT        NOT NULL  -- denormalized from connector_type (see note above)
source_id               TEXT        NOT NULL  -- original ID in the source system
event_type              TEXT        NOT NULL  -- ticket | issue | message | transcript_segment | analytics_event
content                 TEXT        NOT NULL  -- normalized plain-text content
metadata                JSONB       NOT NULL, default '{}'  -- source-specific fields (priority, status, author, tags, etc.)
url                     TEXT                  -- deep link back to source tool
embedding               vector(1536)          -- pgvector; NULL until embed job runs
embedding_generated_at  TIMESTAMPTZ
created_at              TIMESTAMPTZ NOT NULL  -- when it happened in the source system
ingested_at             TIMESTAMPTZ NOT NULL, default now()

UNIQUE (connector_id, source_id)  -- prevents duplicate ingestion on re-sync
```

**Why `content` as TEXT, not VARCHAR(n)?** We don't know the max length of a Zendesk ticket or Gong transcript segment upfront. Artificially capping it with VARCHAR would truncate real data. TEXT in PostgreSQL has no meaningful performance difference from VARCHAR.

**Why `metadata` as JSONB, not columns?** Each source has completely different fields (Zendesk has `ticket_status`, Linear has `priority`, Slack has `thread_ts`, etc.). Encoding all of these as columns would produce a very wide, mostly-null table — a clear normalization smell. JSONB keeps the schema clean while still allowing indexed lookups into the JSON fields.

**Why `vector(1536)`?** OpenAI `text-embedding-3-small` produces 1536-dimensional vectors. pgvector stores this natively and supports ANN (approximate nearest neighbour) search directly.

---

### `briefs`
The Intelligence Brief artifact. Generated weekly per org.

```
id              UUID        PK
org_id          UUID        FK → organizations, NOT NULL
period_start    TIMESTAMPTZ NOT NULL  -- analysis window start
period_end      TIMESTAMPTZ NOT NULL  -- analysis window end
status          TEXT        NOT NULL, default 'generating'
                            -- generating | ready | sent | failed
generated_at    TIMESTAMPTZ
created_at      TIMESTAMPTZ NOT NULL, default now()
updated_at      TIMESTAMPTZ NOT NULL, default now()
```

**Why no `insights` JSON blob in briefs?** Storing insights as a JSON array inside `briefs` is tempting (simpler!) but breaks the moment you want to:
- Query "all insights about churn across all briefs" (trend tracking, V2)
- Link evidence citations to specific insights (needed for MVP)
- Count or filter insights without JSON parsing

Insights are a first-class entity with their own table.

---

### `insights`
A single prioritized recommendation within a brief.

```
id                UUID        PK
brief_id          UUID        FK → briefs, NOT NULL
org_id            UUID        FK → organizations, NOT NULL  -- denormalized for cross-brief queries
rank              INTEGER     NOT NULL  -- 1–7, position within the brief
title             TEXT        NOT NULL
explanation       TEXT        NOT NULL
suggested_action  TEXT        NOT NULL
confidence        REAL        NOT NULL  -- 0.0–1.0, Claude-generated
created_at        TIMESTAMPTZ NOT NULL, default now()
```

---

### `evidence_refs`
Citations linking an insight to the specific raw events that support it. This is the "show your work" table.

```
id              UUID        PK
insight_id      UUID        FK → insights, NOT NULL
raw_event_id    UUID        FK → raw_events, NOT NULL
excerpt         TEXT        NOT NULL  -- the specific passage that supports this insight
url             TEXT                  -- deep link back to source (denormalized for UI speed)
relevance_score REAL        NOT NULL  -- 0.0–1.0, how strongly this event supports the insight
created_at      TIMESTAMPTZ NOT NULL, default now()
```

**Many-to-many:** An insight cites multiple events. An event can be cited by multiple insights (across briefs). The junction table is the right model here.

---

### `brief_deliveries`
Immutable audit log of every delivery attempt.

```
id                  UUID        PK
brief_id            UUID        FK → briefs, NOT NULL
channel             TEXT        NOT NULL  -- email | slack
recipient           TEXT        NOT NULL  -- email address or Slack channel ID
status              TEXT        NOT NULL, default 'pending'
                                -- pending | sent | failed | bounced
external_message_id TEXT                  -- Resend email ID or Slack message ts
sent_at             TIMESTAMPTZ
opened_at           TIMESTAMPTZ           -- from webhook (email) or not tracked (Slack)
error_message       TEXT                  -- populated on failure
created_at          TIMESTAMPTZ NOT NULL, default now()
```

---

### `insight_feed_items`
Real-time signals surfaced between brief cycles — spikes, anomalies, emerging patterns.

```
id              UUID        PK
org_id          UUID        FK → organizations, NOT NULL
signal_type     TEXT        NOT NULL  -- spike | anomaly | emerging_pattern
title           TEXT        NOT NULL
description     TEXT        NOT NULL
severity        TEXT        NOT NULL  -- low | medium | high | critical
detected_at     TIMESTAMPTZ NOT NULL, default now()
acknowledged_at TIMESTAMPTZ           -- when a user dismissed/actioned it
created_at      TIMESTAMPTZ NOT NULL, default now()
```

---

## Indexes

Beyond the primary keys and FK indexes that Alembic will create automatically:

```sql
-- raw_events: the hot path — almost every query hits these
CREATE INDEX idx_raw_events_org_ingested   ON raw_events (org_id, ingested_at DESC);
CREATE INDEX idx_raw_events_org_created    ON raw_events (org_id, created_at DESC);
CREATE INDEX idx_raw_events_connector_dedup ON raw_events (connector_id, source_id);
CREATE INDEX idx_raw_events_unembedded     ON raw_events (org_id) WHERE embedding IS NULL;

-- pgvector HNSW index for ANN search (better than IVFFlat for our scale: no training needed)
CREATE INDEX idx_raw_events_embedding ON raw_events USING hnsw (embedding vector_cosine_ops);

-- briefs: history + feed
CREATE INDEX idx_briefs_org_generated ON briefs (org_id, generated_at DESC);

-- insights: evidence drill-down + trend queries
CREATE INDEX idx_insights_brief        ON insights (brief_id);
CREATE INDEX idx_insights_org_created  ON insights (org_id, created_at DESC);

-- evidence_refs: the other side of drill-down
CREATE INDEX idx_evidence_refs_insight  ON evidence_refs (insight_id);
CREATE INDEX idx_evidence_refs_event    ON evidence_refs (raw_event_id);

-- feed: per-org, ordered by recency
CREATE INDEX idx_feed_org_detected ON insight_feed_items (org_id, detected_at DESC);
```

**Why HNSW over IVFFlat for the vector index?** IVFFlat requires a training step (needs existing data to build clusters before the index is usable). HNSW builds incrementally — inserts work from day one with no training, and query accuracy is higher at our data volumes. The tradeoff is slightly more memory, which is fine.

---

## What We Left Out (Intentionally)

**Clusters table** — The HDBSCAN clustering step produces intermediate clusters that feed into Claude's reasoning. For MVP, these are computed in-memory at brief-generation time and not persisted. We can add a `clusters` table when trend tracking (V2) requires comparing cluster membership over time.

**CorrelationPatterns table** — Same reasoning. Claude's cross-source correlation is an intermediate step whose output lands in `insights`. Persisting the patterns adds complexity without MVP value.

**Soft deletes** — Not added yet. For MVP, deletes are hard. We'll add `deleted_at` columns when compliance or undo requirements emerge.

---

## Entity Relationship Summary

```
organizations
    ├── organization_members ──── users
    ├── connectors
    │       ├── oauth_credentials  (1-to-1)
    │       ├── sync_cursors       (1-to-1)
    │       └── raw_events ────── evidence_refs ──── insights
    │                                                    └── briefs ── brief_deliveries
    └── insight_feed_items
```
