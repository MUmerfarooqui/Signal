# Graph Report - C:\Users\umerf\Signal  (2026-05-08)

## Corpus Check
- 39 files · ~24,888 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 186 nodes · 276 edges · 36 communities detected
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 65 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]

## God Nodes (most connected - your core abstractions)
1. `Signal Product Research Document v1.0` - 18 edges
2. `ZendeskClient` - 13 edges
3. `Base` - 13 edges
4. `Connector` - 12 edges
5. `RawEvent` - 12 edges
6. `SyncCursor` - 12 edges
7. `Signal System Architecture Overview` - 11 edges
8. `Signal Tech Stack` - 9 edges
9. `raw_events table (core fact table)` - 9 edges
10. `MVP Goal: End-to-End Loop (Zendesk+Linear â†’ Ingest â†’ Brief â†’ Email)` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Next.js 15 + TypeScript + Tailwind CSS (Frontend)` --conceptually_related_to--> `Next.js Wordmark SVG (Next.js logo text)`  [INFERRED]
  CLAUDE.md → frontend/public/next.svg
- `zendesk_authorize()` --calls--> `build_authorize_url()`  [INFERRED]
  C:\Users\umerf\Signal\backend\app\api\routes\connectors.py → C:\Users\umerf\Signal\backend\app\connectors\zendesk.py
- `zendesk_callback()` --calls--> `exchange_code_for_token()`  [INFERRED]
  C:\Users\umerf\Signal\backend\app\api\routes\connectors.py → C:\Users\umerf\Signal\backend\app\connectors\zendesk.py
- `trigger_sync()` --calls--> `run_sync()`  [INFERRED]
  C:\Users\umerf\Signal\backend\app\api\routes\connectors.py → C:\Users\umerf\Signal\backend\app\connectors\zendesk.py
- `Base` --uses--> `Connector`  [INFERRED]
  backend\app\models\base.py → backend\app\models\connector.py

## Hyperedges (group relationships)
- **Signal Ingestion Pipeline (Connectors â†’ Celery Workers â†’ PostgreSQL+pgvector)** — arch_connectors, arch_ingestion_jobs, claude_celery_redis, claude_postgresql_pgvector, arch_rawevent, db_raw_events [EXTRACTED 1.00]
- **Signal Reasoning Pipeline (HDBSCAN â†’ Cross-source Correlation â†’ Insight Generation)** — arch_reasoning_layer, claude_hdbscan, claude_claude_api, claude_prompt_caching, db_raw_events, db_insights [EXTRACTED 1.00]
- **Signal Delivery Pipeline (Brief Assembly â†’ Email/Slack)** — arch_brief_assembly, arch_brief_schema, claude_resend, db_briefs, db_brief_deliveries [EXTRACTED 1.00]
- **Evidence Chain (RawEvents â†’ EvidenceRefs â†’ Insights â†’ Briefs)** — db_raw_events, db_evidence_refs, db_insights, db_briefs [EXTRACTED 1.00]
- **Signal MVP Build Plan (Phase 1â€“6)** — mvp_phase1, mvp_phase2, mvp_phase3, mvp_phase4, mvp_phase5, mvp_phase6 [EXTRACTED 1.00]
- **Frontend Public SVG Assets (Next.js default icons)** — fe_icon_file, fe_icon_globe, fe_icon_next, fe_icon_vercel, fe_icon_window [EXTRACTED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (32): REST API Endpoints (backend/app/api/), Brief Assembly (backend/app/brief/), Frontend Pages (Next.js App Router), Ingestion Jobs (Celery Workers), Signal System Architecture Overview, Reasoning Layer (backend/app/reasoning/), Scaling Considerations (post-MVP), Security Notes (OAuth token encryption, JWT, no raw content in API) (+24 more)

### Community 1 - "Community 1"
Cohesion: 0.23
Nodes (21): BaseModel, Connector, AuthorizeResponse, ConnectorOut, list_connectors(), List all connectors for an org., Trigger an immediate sync for a connector. Runs synchronously for MVP., Return the Zendesk OAuth URL. Frontend opens this in a new window/tab. (+13 more)

### Community 2 - "Community 2"
Cohesion: 0.18
Nodes (11): Base, Base, Brief, BriefDelivery, DeclarativeBase, EvidenceRef, InsightFeedItem, Insight (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (24): Brief / Insight / EvidenceRef Data Classes, Connectors (backend/app/connectors/), Database Schema (key tables), RawEvent Schema, brief_deliveries table (audit log), briefs table, connectors table, evidence_refs table (citations) (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (22): Signal Core Loop (Ingest â†’ Reason â†’ Deliver), Signal Core Principles (cite sources, push-first, fewer insights, no manual input, express uncertainty), Signal â€” AI-Native Product Intelligence System, MVP Open Questions (data volume threshold, cadence, pricing, conflicting signals), Central Bet: AI agents shift bottleneck from building to deciding what to build, Competitor Landscape (Dovetail, Productboard, Amplitude, Intercom AI, Kraftful), Signal vs Dashboard Analogy: Signal is the co-pilot, not the cockpit gauges, Signal Defensibility: Cross-source data layer + workflow embedding + historical intelligence (+14 more)

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (7): build_authorize_url(), exchange_code_for_token(), normalize_ticket(), Map a raw Zendesk ticket dict to the RawEvent insert schema., Fetch all tickets since start_time and return normalized RawEvent dicts.     Han, Pull tickets via Zendesk's incremental export.         Returns (tickets, next_st, run_sync()

### Community 6 - "Community 6"
Cohesion: 0.67
Nodes (3): BaseSettings, get_settings(), Settings

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (3): _get_clerk_jwks(), get_current_user_id(), Fetch Clerk's public keys once and cache for the process lifetime.

### Community 8 - "Community 8"
Cohesion: 0.5
Nodes (1): enable_pgvector  Revision ID: 3121f341f537 Revises:  Create Date: 2026-05-08 15:

### Community 9 - "Community 9"
Cohesion: 0.5
Nodes (1): create_all_tables  Revision ID: cc441d76abde Revises: 3121f341f537 Create Date:

### Community 10 - "Community 10"
Cohesion: 0.67
Nodes (0): 

### Community 11 - "Community 11"
Cohesion: 0.67
Nodes (3): Database Normalization Strategy (3NF + deliberate denormalizations), Intentional Omissions: clusters table, CorrelationPatterns table, soft deletes, Rationale: Denormalization for query performance (vector search filter, cross-brief queries, UI speed)

### Community 12 - "Community 12"
Cohesion: 1.0
Nodes (0): 

### Community 13 - "Community 13"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Community 14"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Community 15"
Cohesion: 1.0
Nodes (2): ORM Choice: SQLAlchemy + Alembic (not Prisma), Rationale: Prisma Python client lags official, incompatible with Python 3.12+

### Community 16 - "Community 16"
Cohesion: 1.0
Nodes (2): Database Indexes (HNSW vector index, composite indexes), Rationale: HNSW over IVFFlat (no training step required, incremental inserts, higher accuracy)

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): File Icon SVG (document/file icon, grey)

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Globe Icon SVG (world/internet icon, grey)

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Window Icon SVG (browser window / desktop app icon, grey)

## Knowledge Gaps
- **40 isolated node(s):** `Fetch Clerk's public keys once and cache for the process lifetime.`, `Pull tickets via Zendesk's incremental export.         Returns (tickets, next_st`, `Quick check that credentials are valid.`, `Map a raw Zendesk ticket dict to the RawEvent insert schema.`, `Fetch all tickets since start_time and return normalized RawEvent dicts.     Han` (+35 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (2 nodes): `main.py`, `health()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (2 nodes): `session.py`, `get_db()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 14`** (2 nodes): `layout.tsx`, `RootLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (2 nodes): `ORM Choice: SQLAlchemy + Alembic (not Prisma)`, `Rationale: Prisma Python client lags official, incompatible with Python 3.12+`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (2 nodes): `Database Indexes (HNSW vector index, composite indexes)`, `Rationale: HNSW over IVFFlat (no training step required, incremental inserts, higher accuracy)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 17`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (1 nodes): `router.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (1 nodes): `eslint.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (1 nodes): `next-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (1 nodes): `next.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (1 nodes): `postcss.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (1 nodes): `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `File Icon SVG (document/file icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Globe Icon SVG (world/internet icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Window Icon SVG (browser window / desktop app icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Signal â€” AI-Native Product Intelligence System` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `Signal System Architecture Overview` connect `Community 0` to `Community 3`, `Community 4`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `ZendeskClient` (e.g. with `AuthorizeResponse` and `ConnectorOut`) actually correct?**
  _`ZendeskClient` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Base` (e.g. with `Brief` and `BriefDelivery`) actually correct?**
  _`Base` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Connector` (e.g. with `AuthorizeResponse` and `ConnectorOut`) actually correct?**
  _`Connector` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `RawEvent` (e.g. with `AuthorizeResponse` and `ConnectorOut`) actually correct?**
  _`RawEvent` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Fetch Clerk's public keys once and cache for the process lifetime.`, `Pull tickets via Zendesk's incremental export.         Returns (tickets, next_st`, `Quick check that credentials are valid.` to the rest of the system?**
  _40 weakly-connected nodes found - possible documentation gaps or missing edges._