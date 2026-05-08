# Signal — MVP Scope

## Goal

Ship a working end-to-end loop: connect Zendesk + Linear → ingest data → generate an Intelligence Brief with Claude → deliver via email. A PM at a real company should be able to onboard, connect their tools, and receive a brief within 24 hours.

## Out of Scope for MVP

- Slack integration
- Amplitude / Mixpanel / Gong integrations
- Natural language Q&A
- Trend tracking over time
- Roadmap push (Jira/Linear ticket creation from insights)
- Team collaboration features
- Custom signal weightings
- SOC 2 / compliance certifications
- Mobile

## Phases

---

### Phase 1 — Backend Foundation

**Goal:** Runnable FastAPI app with database, auth, and one working connector.

Tasks:
- [ ] Scaffold FastAPI project (`backend/`)
- [ ] PostgreSQL schema + Alembic migrations (orgs, users, oauth_credentials, raw_events)
- [ ] JWT auth middleware
- [ ] Zendesk connector: OAuth flow + full sync + incremental sync
- [ ] RawEvent normalization and storage
- [ ] Basic API: `/orgs`, `/connectors`, `/events`

Deliverable: Can connect a Zendesk account, pull tickets, and query them via API.

---

### Phase 2 — Second Connector + Embeddings

**Goal:** Multi-source ingestion working. Events embedded and searchable.

Tasks:
- [ ] Linear connector: OAuth flow + full sync + incremental sync
- [ ] pgvector setup + embedding pipeline (embed RawEvents on ingest)
- [ ] Celery + Redis: scheduled sync jobs for both connectors
- [ ] Vector similarity search endpoint (internal use, for reasoning layer)

Deliverable: Zendesk tickets and Linear issues both in the database, embedded, and queryable by semantic similarity.

---

### Phase 3 — Reasoning + Brief Generation

**Goal:** Claude generates a real Intelligence Brief from the ingested data.

Tasks:
- [ ] Clustering: group semantically similar events per source using pgvector
- [ ] Cross-source correlation prompt: identify patterns that span Zendesk + Linear
- [ ] Insight scoring: frequency, recency, source diversity
- [ ] Insight generation: Claude produces title, explanation, suggested action, confidence, evidence citations (EvidenceRef)
- [ ] Brief assembly: top 3–7 insights → structured Brief object stored in DB
- [ ] Manual trigger endpoint: `POST /orgs/{id}/briefs/generate`

Prompt caching: cached prefix = RawEvent summaries, variable suffix = reasoning instructions.

Deliverable: Hit the endpoint, get back a real brief with cited sources. Validate output quality against a test dataset.

---

### Phase 4 — Delivery

**Goal:** Brief sent via email. Celery job runs weekly.

Tasks:
- [ ] Resend integration: HTML email template for the brief
- [ ] Celery beat: scheduled weekly brief generation + delivery per org
- [ ] Delivery log: track sent_at, opened_at (via Resend webhooks)
- [ ] Org settings: configure delivery email, schedule (day + time)

Deliverable: Brief arrives in inbox every Monday morning with clickable evidence links.

---

### Phase 5 — Frontend

**Goal:** Web dashboard for brief viewing, evidence drill-down, and connector setup.

Tasks:
- [ ] Scaffold Next.js project (`frontend/`)
- [ ] Auth: NextAuth.js (email magic link or Google OAuth)
- [ ] `/settings/integrations` — connect Zendesk + Linear via OAuth
- [ ] `/briefs` — list view of past briefs
- [ ] `/briefs/[id]` — brief detail page: insights with evidence drawer
- [ ] `/dashboard` — insight feed (recent high-signal events between briefs)
- [ ] Responsive design, Tailwind

Deliverable: A PM can sign up, connect tools, view their brief in the browser, and click into any insight to see the source evidence.

---

### Phase 6 — Polish + Design Partner Onboarding

**Goal:** Stable enough to give to 3–5 real companies.

Tasks:
- [ ] Error handling: failed syncs, empty data, low-confidence briefs
- [ ] Onboarding flow: new org setup wizard (connect sources → configure delivery → generate first brief)
- [ ] Brief quality review: human review step before sending (toggle per org)
- [ ] Basic admin dashboard: org list, connector status, brief history
- [ ] Logging + alerting: Sentry, structured logs
- [ ] Rate limiting on API

---

## Success Criteria for MVP

1. A PM can connect Zendesk + Linear in under 5 minutes with no technical help.
2. The weekly brief contains at least 3 insights with evidence citations.
3. At least one insight per brief is cross-source (cites both Zendesk and Linear evidence).
4. A PM reviewing the brief says the insights are "things I wouldn't have caught myself this week."
5. Brief arrives via email on schedule without manual intervention.

## Open Questions (from research doc §9)

These need answers before or during Phase 3:

1. What is the minimum viable data volume for the brief to be substantive? (Define a threshold for onboarding gating.)
2. Weekly default cadence or anomaly-triggered? (Start with weekly; add anomaly detection in V2.)
3. How does Signal handle conflicting signals? (Document the tie-breaking logic in the reasoning prompt.)
4. Pricing model: per-seat vs per-org vs consumption? (Decide before Phase 6 / design partner conversations.)
