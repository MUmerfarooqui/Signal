# Graph Report - .  (2026-05-08)

## Corpus Check
- Corpus is ~10,511 words - fits in a single context window. You may not need a graph.

## Summary
- 142 nodes · 188 edges · 30 communities detected
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.69)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_SQLAlchemy Models|SQLAlchemy Models]]
- [[_COMMUNITY_Product Strategy & Vision|Product Strategy & Vision]]
- [[_COMMUNITY_Application Tech Stack|Application Tech Stack]]
- [[_COMMUNITY_Database Schema|Database Schema]]
- [[_COMMUNITY_AI Reasoning Pipeline|AI Reasoning Pipeline]]
- [[_COMMUNITY_System Architecture|System Architecture]]
- [[_COMMUNITY_pgvector Migration|pgvector Migration]]
- [[_COMMUNITY_Schema Migration|Schema Migration]]
- [[_COMMUNITY_Alembic Config|Alembic Config]]
- [[_COMMUNITY_DB Normalization Design|DB Normalization Design]]
- [[_COMMUNITY_Next.js Root Layout|Next.js Root Layout]]
- [[_COMMUNITY_ORM Decision|ORM Decision]]
- [[_COMMUNITY_Index Strategy|Index Strategy]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_Module Init|Module Init]]
- [[_COMMUNITY_ESLint Config|ESLint Config]]
- [[_COMMUNITY_TS Declarations|TS Declarations]]
- [[_COMMUNITY_Next.js Config|Next.js Config]]
- [[_COMMUNITY_PostCSS Config|PostCSS Config]]
- [[_COMMUNITY_Frontend Homepage|Frontend Homepage]]
- [[_COMMUNITY_File Icon|File Icon]]
- [[_COMMUNITY_Globe Icon|Globe Icon]]
- [[_COMMUNITY_Window Icon|Window Icon]]

## God Nodes (most connected - your core abstractions)
1. `Signal Product Research Document v1.0` - 18 edges
2. `Base` - 13 edges
3. `Signal System Architecture Overview` - 11 edges
4. `Signal Tech Stack` - 9 edges
5. `raw_events table (core fact table)` - 9 edges
6. `MVP Goal: End-to-End Loop (Zendesk+Linear â†’ Ingest â†’ Brief â†’ Email)` - 9 edges
7. `Signal â€” AI-Native Product Intelligence System` - 8 edges
8. `Database Schema (key tables)` - 7 edges
9. `Reasoning Layer (backend/app/reasoning/)` - 6 edges
10. `Next.js 15 + TypeScript + Tailwind CSS (Frontend)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Next.js Wordmark SVG (Next.js logo text)` --conceptually_related_to--> `Next.js 15 + TypeScript + Tailwind CSS (Frontend)`  [INFERRED]
  frontend/public/next.svg → CLAUDE.md
- `Signal â€” AI-Native Product Intelligence System` --conceptually_related_to--> `ICP: B2B/B2C software, 20-500 employees, 2+ tools, no dedicated research ops`  [INFERRED]
  CLAUDE.md → docs/Signal_Product_Research_Document.md
- `Rationale: vector(1536) matches OpenAI text-embedding-3-small output dimensions` --references--> `OpenAI text-embedding-3-small (Embeddings)`  [EXTRACTED]
  docs/database.md → CLAUDE.md
- `Frontend Pages (Next.js App Router)` --conceptually_related_to--> `Frontend README (Next.js bootstrapped via create-next-app)`  [INFERRED]
  docs/architecture.md → frontend/README.md
- `Brief` --uses--> `Base`  [INFERRED]
  backend\app\models\brief.py → backend\app\models\base.py

## Hyperedges (group relationships)
- **Signal Ingestion Pipeline (Connectors â†’ Celery Workers â†’ PostgreSQL+pgvector)** — arch_connectors, arch_ingestion_jobs, claude_celery_redis, claude_postgresql_pgvector, arch_rawevent, db_raw_events [EXTRACTED 1.00]
- **Signal Reasoning Pipeline (HDBSCAN â†’ Cross-source Correlation â†’ Insight Generation)** — arch_reasoning_layer, claude_hdbscan, claude_claude_api, claude_prompt_caching, db_raw_events, db_insights [EXTRACTED 1.00]
- **Signal Delivery Pipeline (Brief Assembly â†’ Email/Slack)** — arch_brief_assembly, arch_brief_schema, claude_resend, db_briefs, db_brief_deliveries [EXTRACTED 1.00]
- **Evidence Chain (RawEvents â†’ EvidenceRefs â†’ Insights â†’ Briefs)** — db_raw_events, db_evidence_refs, db_insights, db_briefs [EXTRACTED 1.00]
- **Signal MVP Build Plan (Phase 1â€“6)** — mvp_phase1, mvp_phase2, mvp_phase3, mvp_phase4, mvp_phase5, mvp_phase6 [EXTRACTED 1.00]
- **Frontend Public SVG Assets (Next.js default icons)** — fe_icon_file, fe_icon_globe, fe_icon_next, fe_icon_vercel, fe_icon_window [EXTRACTED 1.00]

## Communities

### Community 0 - "SQLAlchemy Models"
Cohesion: 0.17
Nodes (14): Base, Base, Brief, BriefDelivery, Connector, DeclarativeBase, EvidenceRef, InsightFeedItem (+6 more)

### Community 1 - "Product Strategy & Vision"
Cohesion: 0.12
Nodes (22): Signal Core Loop (Ingest â†’ Reason â†’ Deliver), Signal Core Principles (cite sources, push-first, fewer insights, no manual input, express uncertainty), Signal â€” AI-Native Product Intelligence System, MVP Open Questions (data volume threshold, cadence, pricing, conflicting signals), Central Bet: AI agents shift bottleneck from building to deciding what to build, Competitor Landscape (Dovetail, Productboard, Amplitude, Intercom AI, Kraftful), Signal vs Dashboard Analogy: Signal is the co-pilot, not the cockpit gauges, Signal Defensibility: Cross-source data layer + workflow embedding + historical intelligence (+14 more)

### Community 2 - "Application Tech Stack"
Cohesion: 0.13
Nodes (21): Brief Assembly (backend/app/brief/), Ingestion Jobs (Celery Workers), Celery + Redis (Queue), FastAPI + Python 3.12+ (Backend), NextAuth.js (Frontend Auth), Next.js 15 + TypeScript + Tailwind CSS (Frontend), OpenAI text-embedding-3-small (Embeddings), PostgreSQL + pgvector (Database) (+13 more)

### Community 3 - "Database Schema"
Cohesion: 0.16
Nodes (15): Database Schema (key tables), brief_deliveries table (audit log), briefs table, connectors table, insight_feed_items table, oauth_credentials table (encrypted Fernet tokens), organization_members table (junction), organizations table (+7 more)

### Community 4 - "AI Reasoning Pipeline"
Cohesion: 0.22
Nodes (13): Brief / Insight / EvidenceRef Data Classes, Reasoning Layer (backend/app/reasoning/), Signal AI Strategy (Embeddings / Clustering / Reasoning layers), Anthropic Claude API â€” claude-sonnet-4-6 (AI Reasoning), HDBSCAN Clustering, Prompt Caching Strategy (cluster summaries as cached prefix), evidence_refs table (citations), insights table (+5 more)

### Community 5 - "System Architecture"
Cohesion: 0.33
Nodes (7): REST API Endpoints (backend/app/api/), Connectors (backend/app/connectors/), Frontend Pages (Next.js App Router), Signal System Architecture Overview, RawEvent Schema, Scaling Considerations (post-MVP), Security Notes (OAuth token encryption, JWT, no raw content in API)

### Community 6 - "pgvector Migration"
Cohesion: 0.5
Nodes (1): enable_pgvector  Revision ID: 3121f341f537 Revises:  Create Date: 2026-05-08 15:

### Community 7 - "Schema Migration"
Cohesion: 0.5
Nodes (1): create_all_tables  Revision ID: cc441d76abde Revises: 3121f341f537 Create Date:

### Community 8 - "Alembic Config"
Cohesion: 0.67
Nodes (0): 

### Community 9 - "DB Normalization Design"
Cohesion: 0.67
Nodes (3): Database Normalization Strategy (3NF + deliberate denormalizations), Intentional Omissions: clusters table, CorrelationPatterns table, soft deletes, Rationale: Denormalization for query performance (vector search filter, cross-brief queries, UI speed)

### Community 10 - "Next.js Root Layout"
Cohesion: 1.0
Nodes (0): 

### Community 11 - "ORM Decision"
Cohesion: 1.0
Nodes (2): ORM Choice: SQLAlchemy + Alembic (not Prisma), Rationale: Prisma Python client lags official, incompatible with Python 3.12+

### Community 12 - "Index Strategy"
Cohesion: 1.0
Nodes (2): Database Indexes (HNSW vector index, composite indexes), Rationale: HNSW over IVFFlat (no training step required, incremental inserts, higher accuracy)

### Community 13 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 14 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 15 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 16 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 17 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 18 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 19 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Module Init"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "ESLint Config"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "TS Declarations"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Next.js Config"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "PostCSS Config"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Frontend Homepage"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "File Icon"
Cohesion: 1.0
Nodes (1): File Icon SVG (document/file icon, grey)

### Community 28 - "Globe Icon"
Cohesion: 1.0
Nodes (1): Globe Icon SVG (world/internet icon, grey)

### Community 29 - "Window Icon"
Cohesion: 1.0
Nodes (1): Window Icon SVG (browser window / desktop app icon, grey)

## Knowledge Gaps
- **35 isolated node(s):** `enable_pgvector  Revision ID: 3121f341f537 Revises:  Create Date: 2026-05-08 15:`, `create_all_tables  Revision ID: cc441d76abde Revises: 3121f341f537 Create Date:`, `Signal Core Loop (Ingest â†’ Reason â†’ Deliver)`, `Security Notes (OAuth token encryption, JWT, no raw content in API)`, `Scaling Considerations (post-MVP)` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Next.js Root Layout`** (2 nodes): `layout.tsx`, `RootLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ORM Decision`** (2 nodes): `ORM Choice: SQLAlchemy + Alembic (not Prisma)`, `Rationale: Prisma Python client lags official, incompatible with Python 3.12+`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Index Strategy`** (2 nodes): `Database Indexes (HNSW vector index, composite indexes)`, `Rationale: HNSW over IVFFlat (no training step required, incremental inserts, higher accuracy)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Module Init`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ESLint Config`** (1 nodes): `eslint.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `TS Declarations`** (1 nodes): `next-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Next.js Config`** (1 nodes): `next.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `PostCSS Config`** (1 nodes): `postcss.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend Homepage`** (1 nodes): `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `File Icon`** (1 nodes): `File Icon SVG (document/file icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Globe Icon`** (1 nodes): `Globe Icon SVG (world/internet icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Window Icon`** (1 nodes): `Window Icon SVG (browser window / desktop app icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Signal â€” AI-Native Product Intelligence System` connect `Product Strategy & Vision` to `Application Tech Stack`, `AI Reasoning Pipeline`, `System Architecture`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `Signal System Architecture Overview` connect `System Architecture` to `Product Strategy & Vision`, `Application Tech Stack`, `Database Schema`, `AI Reasoning Pipeline`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `Base` (e.g. with `Brief` and `BriefDelivery`) actually correct?**
  _`Base` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `enable_pgvector  Revision ID: 3121f341f537 Revises:  Create Date: 2026-05-08 15:`, `create_all_tables  Revision ID: cc441d76abde Revises: 3121f341f537 Create Date:`, `Signal Core Loop (Ingest â†’ Reason â†’ Deliver)` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Product Strategy & Vision` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._
- **Should `Application Tech Stack` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._