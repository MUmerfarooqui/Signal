# Graph Report - .  (2026-05-09)

## Corpus Check
- 61 files · ~99,999 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 428 nodes · 642 edges · 84 communities detected
- Extraction: 70% EXTRACTED · 30% INFERRED · 0% AMBIGUOUS · INFERRED: 192 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Architecture Overview|Architecture Overview]]
- [[_COMMUNITY_Database Schema & Data Flow|Database Schema & Data Flow]]
- [[_COMMUNITY_Auth & Frontend Routes|Auth & Frontend Routes]]
- [[_COMMUNITY_Brief Generation|Brief Generation]]
- [[_COMMUNITY_Connectors & Embedding|Connectors & Embedding]]
- [[_COMMUNITY_Product Roadmap & V2|Product Roadmap & V2]]
- [[_COMMUNITY_Reasoning & Email Delivery|Reasoning & Email Delivery]]
- [[_COMMUNITY_Pulse Detection & Clustering|Pulse Detection & Clustering]]
- [[_COMMUNITY_Org & User Models|Org & User Models]]
- [[_COMMUNITY_DB Schema Docs|DB Schema Docs]]
- [[_COMMUNITY_SQLAlchemy Models|SQLAlchemy Models]]
- [[_COMMUNITY_Frontend Dashboard Pages|Frontend Dashboard Pages]]
- [[_COMMUNITY_Backend Launcher|Backend Launcher]]
- [[_COMMUNITY_App Configuration|App Configuration]]
- [[_COMMUNITY_Dark Mode Theme|Dark Mode Theme]]
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
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]

## God Nodes (most connected - your core abstractions)
1. `EvidenceRef` - 21 edges
2. `Insight` - 21 edges
3. `RawEvent` - 19 edges
4. `Connector` - 18 edges
5. `Signal Product Research Document v1.0` - 18 edges
6. `ZendeskClient` - 17 edges
7. `SyncCursor` - 16 edges
8. `GET()` - 16 edges
9. `Brief` - 14 edges
10. `Base` - 13 edges

## Surprising Connections (you probably didn't know these)
- `Next.js 15 + TypeScript + Tailwind CSS (Frontend)` --conceptually_related_to--> `Next.js Wordmark SVG (Next.js logo text)`  [INFERRED]
  CLAUDE.md → frontend/public/next.svg
- `get_brief()` --calls--> `GET()`  [INFERRED]
  backend\app\api\routes\briefs.py → frontend\app\api\auth\zendesk\callback\route.ts
- `zendesk_authorize()` --calls--> `build_authorize_url()`  [INFERRED]
  backend\app\api\routes\connectors.py → C:\Users\umerf\Signal\backend\app\connectors\zendesk.py
- `zendesk_callback()` --calls--> `exchange_code_for_token()`  [INFERRED]
  backend\app\api\routes\connectors.py → C:\Users\umerf\Signal\backend\app\connectors\zendesk.py
- `zendesk_callback()` --calls--> `GET()`  [INFERRED]
  backend\app\api\routes\connectors.py → frontend\app\api\auth\zendesk\callback\route.ts

## Hyperedges (group relationships)
- **Three AI Layers: Embeddings, Clustering, Reasoning** — claude_ai_layer_embeddings, claude_ai_layer_clustering, claude_ai_layer_reasoning [EXTRACTED 1.00]
- **Core Data Pipeline: Ingest â†’ Embed â†’ Cluster â†’ Reason â†’ Deliver** — arch_connectors, arch_worker_embed, arch_reasoning_cluster, arch_reasoning_reason, readme_worker_deliver [EXTRACTED 1.00]
- **Completed MVP Phases 1-5** — mvp_phase1_backend, mvp_phase2_embeddings, mvp_phase3_reasoning, mvp_phase4_delivery, mvp_phase5_frontend [EXTRACTED 1.00]
- **Backend Celery Worker Set** — readme_worker_embed, readme_worker_cluster, readme_worker_pulse, readme_worker_reason, readme_worker_deliver, readme_worker_brief [EXTRACTED 1.00]
- **Database Schema â€” 12 Tables** — arch_db_organizations, arch_db_users, arch_db_oauth_credentials, arch_db_connectors, arch_db_raw_events, arch_db_insight_feed_items, arch_db_briefs, arch_db_insights, arch_db_evidence_refs, arch_db_brief_deliveries [EXTRACTED 1.00]
- **Required Environment Variables** — readme_env_database_url, readme_env_redis_url, readme_env_clerk, readme_env_zendesk, readme_env_openai, readme_env_anthropic [EXTRACTED 1.00]

## Communities

### Community 0 - "Architecture Overview"
Cohesion: 0.08
Nodes (43): REST API Endpoints (backend/app/api/), Brief Assembly (backend/app/brief/), Brief / Insight / EvidenceRef Data Classes, Connectors Component (backend/app/connectors/), Frontend Pages (Next.js App Router), Ingestion Jobs (Celery Workers), Architecture â€” Two-Service Application Overview, RawEvent Schema (+35 more)

### Community 1 - "Database Schema & Data Flow"
Cohesion: 0.06
Nodes (38): Architecture â€” High-Level Data Flow Diagram, DB Table â€” brief_deliveries (delivery log), DB Table â€” briefs, DB Table â€” connectors, DB Table â€” evidence_refs (insight â†’ raw_event citation), DB Table â€” insight_feed_items (Pulse signals), DB Table â€” insights (rank, category, confidence, evidence), DB Table â€” oauth_credentials (Fernet/AES-256 encrypted) (+30 more)

### Community 2 - "Auth & Frontend Routes"
Cohesion: 0.06
Nodes (37): Auth â€” Clerk JWT Verification via JWKS, DB Table â€” users (clerk_id, email, name), Frontend Routes â€” Next.js App Router Pages, Design Decision â€” Pulse vs Brief Comparison Table, AI Layer â€” Embeddings (OpenAI, cheap vectorization), Backend â€” FastAPI Python 3.12+, Email Delivery â€” Resend, Embeddings â€” OpenAI text-embedding-3-small (+29 more)

### Community 3 - "Brief Generation"
Cohesion: 0.16
Nodes (28): Brief, BriefDelivery, dispatch_all_orgs(), generate_brief(), Fan-out: fire generate_brief for every org that has an active connector., Full pipeline: cluster → reason → assemble → deliver.     Runs weekly via Celery, BriefDetail, BriefSummary (+20 more)

### Community 4 - "Connectors & Embedding"
Cohesion: 0.17
Nodes (28): BaseModel, Connector, AuthorizeResponse, ConnectorOut, list_connectors(), List all connectors for an org., List all connectors for an org., Trigger an immediate sync for a connector. Runs synchronously for MVP. (+20 more)

### Community 5 - "Product Roadmap & V2"
Cohesion: 0.09
Nodes (29): AI Layer â€” Q&A Interface V2 (RAG + Claude), Connector â€” Amplitude, Connector â€” Gong, Connector â€” Linear, Connector â€” Slack, Core Ingest-Reason-Deliver Loop, Signal Core Principles (cite sources, push-first, fewer insights, no manual input, express uncertainty), Signal â€” AI-Native Product Intelligence System (+21 more)

### Community 6 - "Reasoning & Email Delivery"
Cohesion: 0.11
Nodes (16): _build_email_html(), Send the brief as an email. Returns the Resend message ID., send_brief_email(), _get_clerk_jwks(), get_current_user_id(), Fetch Clerk's public keys once and cache for the process lifetime., generate_insights(), Call Claude with cluster summaries and return structured insights.     Uses prom (+8 more)

### Community 7 - "Pulse Detection & Clustering"
Cohesion: 0.16
Nodes (14): Cluster, cluster_events(), Run HDBSCAN over raw_event embeddings.     Returns one Cluster per theme found., Convert clusters into plain dicts suitable for sending to Claude.     Caps each, summarize_clusters(), InsightFeedItem, detect_pulse(), FeedItemOut (+6 more)

### Community 8 - "Org & User Models"
Cohesion: 0.31
Nodes (13): Base, Base, DeclarativeBase, OrganizationMember, Organization, create_org(), CreateOrgRequest, get_my_org() (+5 more)

### Community 9 - "DB Schema Docs"
Cohesion: 0.16
Nodes (15): Database Schema (key tables), brief_deliveries table (audit log), briefs table, connectors table, insight_feed_items table, oauth_credentials table (encrypted Fernet tokens), organization_members table (junction), organizations table (+7 more)

### Community 10 - "SQLAlchemy Models"
Cohesion: 0.32
Nodes (0): 

### Community 11 - "Frontend Dashboard Pages"
Cohesion: 0.33
Nodes (2): formatDate(), formatDateShort()

### Community 12 - "Backend Launcher"
Cohesion: 0.33
Nodes (1): Single-command backend launcher. Starts Redis, FastAPI, Celery worker, and Celer

### Community 13 - "App Configuration"
Cohesion: 0.6
Nodes (3): BaseSettings, get_settings(), Settings

### Community 14 - "Dark Mode Theme"
Cohesion: 0.4
Nodes (2): useTheme(), ThemeToggle()

### Community 15 - "Community 15"
Cohesion: 0.5
Nodes (1): add clerk_id to users  Revision ID: 1df21e0b607b Revises: cc441d76abde Create Da

### Community 16 - "Community 16"
Cohesion: 0.5
Nodes (1): enable_pgvector  Revision ID: 3121f341f537 Revises:  Create Date: 2026-05-08 15:

### Community 17 - "Community 17"
Cohesion: 0.5
Nodes (1): create_all_tables  Revision ID: cc441d76abde Revises: 3121f341f537 Create Date:

### Community 18 - "Community 18"
Cohesion: 0.5
Nodes (1): add_pulse_fields_to_feed_items  Revision ID: 4e0e576f4929 Revises: fd09b2ab17f2

### Community 19 - "Community 19"
Cohesion: 0.5
Nodes (1): add_category_affected_count_to_insights  Revision ID: c415207d3cc8 Revises: 1df2

### Community 20 - "Community 20"
Cohesion: 0.5
Nodes (1): make_raw_event_id_nullable_on_evidence_refs  Revision ID: fd09b2ab17f2 Revises:

### Community 21 - "Community 21"
Cohesion: 0.67
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (3): Database Normalization Strategy (3NF + deliberate denormalizations), Intentional Omissions: clusters table, CorrelationPatterns table, soft deletes, Rationale: Denormalization for query performance (vector search filter, cross-brief queries, UI speed)

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
Nodes (2): ORM Choice: SQLAlchemy + Alembic (not Prisma), Rationale: Prisma Python client lags official, incompatible with Python 3.12+

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (2): Database Indexes (HNSW vector index, composite indexes), Rationale: HNSW over IVFFlat (no training step required, incremental inserts, higher accuracy)

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
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (0): 

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (0): 

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (0): 

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (0): 

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (0): 

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (0): 

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (0): 

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (0): 

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (1): File Icon SVG (document/file icon, grey)

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (1): Globe Icon SVG (world/internet icon, grey)

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (1): Window Icon SVG (browser window / desktop app icon, grey)

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (0): 

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (0): 

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (0): 

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (0): 

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): Auth â€” NextAuth.js + JWT tokens

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Principle â€” No Manual Input Required

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Principle â€” Express Uncertainty

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Frontend â€” Next.js 16 + Tailwind CSS

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (1): seed.py â€” Idempotent Mock Data Seeder

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (1): API Route â€” GET /health

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (1): API Routes â€” /orgs (POST + GET /orgs/me)

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): Env Var â€” DATABASE_URL (Neon connection string)

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): Env Var â€” REDIS_URL

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): Env Vars â€” CLERK_SECRET_KEY + CLERK_PUBLISHABLE_KEY

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): Env Vars â€” ZENDESK_CLIENT_ID + ZENDESK_CLIENT_SECRET

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Env Var â€” OPENAI_API_KEY

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): Env Var â€” ANTHROPIC_API_KEY

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Dependency â€” pydantic==2.13.4

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Dependency â€” uvicorn==0.46.0

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): Dependency â€” httpx==0.28.1

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (1): Dependency â€” numpy==2.4.4

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Security â€” No Raw Event Content in API Responses

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (1): MVP Phase 6 â€” Polish + Design Partner Onboarding (Not Started)

## Knowledge Gaps
- **104 isolated node(s):** `Single-command backend launcher. Starts Redis, FastAPI, Celery worker, and Celer`, `Fetch Clerk's public keys once and cache for the process lifetime.`, `Pull tickets via Zendesk's incremental export.         Returns (tickets, next_st`, `Quick check that credentials are valid.`, `Map a raw Zendesk ticket dict to the RawEvent insert schema.` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 23`** (2 nodes): `main.py`, `health()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (2 nodes): `session.py`, `get_db()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (2 nodes): `layout.tsx`, `RootLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (2 nodes): `ORM Choice: SQLAlchemy + Alembic (not Prisma)`, `Rationale: Prisma Python client lags official, incompatible with Python 3.12+`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (2 nodes): `Database Indexes (HNSW vector index, composite indexes)`, `Rationale: HNSW over IVFFlat (no training step required, incremental inserts, higher accuracy)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `layout.tsx`, `AppLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `ConnectZendesk()`, `connect-zendesk.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `sync-button.tsx`, `SyncButton()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `generate-button.tsx`, `GenerateBriefButton()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `page.tsx`, `timeAgo()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (2 nodes): `page.tsx`, `SignInPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (2 nodes): `page.tsx`, `SignUpPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (2 nodes): `page.tsx`, `OnboardingPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `touch-init.tsx`, `TouchInit()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (2 nodes): `Badge()`, `badge.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `request()`, `api.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (2 nodes): `utils.ts`, `cn()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `router.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `celery_app.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `eslint.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `next-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `next.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `postcss.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `File Icon SVG (document/file icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `Globe Icon SVG (world/internet icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Window Icon SVG (browser window / desktop app icon, grey)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `router.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `proxy.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `sidebar.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `button.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `card.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `Auth â€” NextAuth.js + JWT tokens`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `Principle â€” No Manual Input Required`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `Principle â€” Express Uncertainty`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `Frontend â€” Next.js 16 + Tailwind CSS`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `seed.py â€” Idempotent Mock Data Seeder`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `API Route â€” GET /health`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `API Routes â€” /orgs (POST + GET /orgs/me)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `Env Var â€” DATABASE_URL (Neon connection string)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `Env Var â€” REDIS_URL`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `Env Vars â€” CLERK_SECRET_KEY + CLERK_PUBLISHABLE_KEY`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `Env Vars â€” ZENDESK_CLIENT_ID + ZENDESK_CLIENT_SECRET`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `Env Var â€” OPENAI_API_KEY`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `Env Var â€” ANTHROPIC_API_KEY`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Dependency â€” pydantic==2.13.4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Dependency â€” uvicorn==0.46.0`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Dependency â€” httpx==0.28.1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `Dependency â€” numpy==2.4.4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Security â€” No Raw Event Content in API Responses`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `MVP Phase 6 â€” Polish + Design Partner Onboarding (Not Started)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Signal â€” AI-Native Product Intelligence System` connect `Auth & Frontend Routes` to `Architecture Overview`, `Database Schema & Data Flow`, `Product Roadmap & V2`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `Architecture â€” Two-Service Application Overview` connect `Architecture Overview` to `DB Schema Docs`, `Auth & Frontend Routes`, `Product Roadmap & V2`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `Signal â€” AI-Native Product Intelligence System` connect `Product Roadmap & V2` to `Architecture Overview`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `EvidenceRef` (e.g. with `EvidenceOut` and `InsightOut`) actually correct?**
  _`EvidenceRef` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `Insight` (e.g. with `EvidenceOut` and `InsightOut`) actually correct?**
  _`Insight` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `RawEvent` (e.g. with `AuthorizeResponse` and `ConnectorOut`) actually correct?**
  _`RawEvent` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Connector` (e.g. with `AuthorizeResponse` and `zendesk_callback()`) actually correct?**
  _`Connector` has 16 INFERRED edges - model-reasoned connections that need verification._