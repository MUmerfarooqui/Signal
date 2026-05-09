# Signal — MVP Scope

## Goal

Ship a working end-to-end loop: connect Zendesk → ingest data → generate an Intelligence Brief with Claude → deliver via email. A PM at a real company should be able to onboard, connect their tools, and receive a brief within 24 hours.

## Status Key
- ✅ Built and working
- 🔧 Built, needs testing with real data
- 🚧 In progress / partially built
- ⬜ Not started

## Out of Scope for MVP

- Linear connector (coming soon — UI placeholder exists)
- Slack integration
- Amplitude / Mixpanel / Gong integrations
- Natural language Q&A
- Trend tracking over time
- Roadmap push (Jira/Linear ticket creation from insights)
- Team collaboration features
- Custom signal weightings
- SOC 2 / compliance certifications
- Mobile

---

## Phase 1 — Backend Foundation ✅

- ✅ FastAPI project scaffolded (`backend/`)
- ✅ PostgreSQL schema + Alembic migrations
- ✅ Clerk JWT auth middleware
- ✅ Zendesk connector: OAuth flow + full sync + incremental sync
- ✅ RawEvent normalization and storage
- ✅ API routes: `/orgs`, `/connectors`, `/briefs`, `/pulse`

---

## Phase 2 — Embeddings Pipeline ✅

- ✅ pgvector setup + embedding pipeline (OpenAI `text-embedding-3-small`)
- ✅ Celery + Redis: async embed jobs triggered after every sync
- ✅ Pulse detection triggered after every embed run (1.5× threshold)

---

## Phase 3 — Reasoning + Brief Generation ✅

- ✅ HDBSCAN clustering over pgvector embeddings
- ✅ Insight generation: Claude Sonnet produces title, explanation, suggested action, confidence, evidence citations
- ✅ Insight categories: recurring_pain, feature_gap, onboarding_friction, reliability_issue, workflow_blocker, churn_signal
- ✅ Brief assembly: top 3–7 insights → structured Brief stored in DB
- ✅ Manual trigger: `POST /briefs/generate`
- ✅ Weekly Celery beat schedule (Monday 08:00)
- 🔧 Prompt caching on cluster summaries

---

## Phase 4 — Delivery ✅ / 🚧

- ✅ Resend integration: HTML email with brief content
- ✅ Celery beat: weekly brief generation + delivery
- ✅ Delivery log: BriefDelivery rows per send
- 🚧 Org settings UI: configure delivery email (backend supports it via `org.settings.brief_email`; no frontend settings page yet)

---

## Phase 5 — Frontend ✅

- ✅ Next.js 16 App Router with Clerk auth
- ✅ Landing page with sign-up / sign-in CTAs
- ✅ Onboarding: create org
- ✅ Connectors page: connect Zendesk via OAuth, manual sync, status display
- ✅ Briefs list: `/dashboard`
- ✅ Brief detail: `/briefs/[id]` — insights with rank, category, confidence, evidence
- ✅ Pulse feed: `/pulse` — live signals between briefs
- ✅ Dark mode toggle (class-based, persists to localStorage)
- ✅ Sidebar: Signal logo + org name, nav (Briefs / Pulse / Connectors), UserButton

---

## Phase 6 — Polish + Design Partner Onboarding ⬜

- ⬜ Settings page: configure brief delivery email
- ⬜ Error handling: failed syncs, empty data, low-confidence briefs
- ⬜ Onboarding flow improvements: connect sources → configure delivery → generate first brief
- ⬜ Brief quality review toggle per org
- ⬜ Logging + alerting: Sentry, structured logs
- ⬜ Rate limiting on API

---

## Success Criteria for MVP

1. A PM can connect Zendesk in under 5 minutes with no technical help.
2. The weekly brief contains at least 3 insights with evidence citations.
3. Brief arrives via email on schedule without manual intervention.
4. Pulse surfaces live signals within 24h of a support spike.
5. A PM reviewing the brief says the insights are "things I wouldn't have caught myself this week."

## Open Questions

1. Minimum viable data volume for the brief to be substantive — define gating threshold before design partner onboarding.
2. Weekly cadence is hardcoded — make configurable in Phase 6.
3. Pricing model: per-seat vs per-org vs consumption — decide before design partner conversations.
4. Linear connector: scope and prioritise for next sprint.
