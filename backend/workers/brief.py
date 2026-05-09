import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.connector import Connector
from app.models.brief import Brief
from app.models.brief_delivery import BriefDelivery
from app.models.evidence_ref import EvidenceRef
from app.models.insight import Insight
from app.models.organization import Organization
from app.models.raw_event import RawEvent
from workers.celery_app import celery
from workers.cluster import cluster_events, summarize_clusters
from workers.deliver import send_brief_email
from workers.reason import generate_insights


@celery.task
def dispatch_all_orgs() -> dict:
    """Fan-out: fire generate_brief for every org that has an active connector."""
    db = SessionLocal()
    try:
        org_ids = db.execute(
            select(Connector.org_id)
            .where(Connector.status == "active")
            .distinct()
        ).scalars().all()

        for org_id in org_ids:
            generate_brief.delay(str(org_id))

        return {"dispatched": len(org_ids)}
    finally:
        db.close()


@celery.task(bind=True, max_retries=2, default_retry_delay=300)
def generate_brief(self, org_id: str) -> dict:
    """
    Full pipeline: cluster → reason → assemble → deliver.
    Runs weekly via Celery beat, or manually via POST /briefs/generate.
    """
    db = SessionLocal()
    org_uuid = uuid.UUID(org_id)

    try:
        # ------------------------------------------------------------------ #
        # 1. Fetch all embedded events from the last 7 days                  #
        # ------------------------------------------------------------------ #
        period_end = datetime.now(timezone.utc)
        period_start = period_end - timedelta(days=7)

        events = db.execute(
            select(RawEvent)
            .where(
                RawEvent.org_id == org_uuid,
                RawEvent.embedding != None,  # noqa: E711
                RawEvent.created_at >= period_start,
            )
            .order_by(RawEvent.created_at.desc())
        ).scalars().all()

        if not events:
            return {"status": "skipped", "reason": "no_embedded_events"}

        # ------------------------------------------------------------------ #
        # 2. Cluster                                                          #
        # ------------------------------------------------------------------ #
        clusters = cluster_events(events)

        if not clusters:
            return {"status": "skipped", "reason": "no_clusters_found"}

        cluster_summaries = summarize_clusters(clusters)

        # ------------------------------------------------------------------ #
        # 3. Create brief row (status = generating)                          #
        # ------------------------------------------------------------------ #
        brief = Brief(
            org_id=org_uuid,
            period_start=period_start,
            period_end=period_end,
            status="generating",
        )
        db.add(brief)
        db.flush()

        # ------------------------------------------------------------------ #
        # 4. Reason with Claude                                               #
        # ------------------------------------------------------------------ #
        period_start_str = period_start.strftime("%b %d, %Y")
        period_end_str = period_end.strftime("%b %d, %Y")

        try:
            raw_insights = generate_insights(cluster_summaries, period_start_str, period_end_str)
        except Exception as exc:
            brief.status = "failed"
            db.commit()
            raise self.retry(exc=exc)

        # ------------------------------------------------------------------ #
        # 5. Assemble — write Insight + EvidenceRef rows                     #
        # ------------------------------------------------------------------ #

        # Build a lookup: source_id → RawEvent for evidence linking
        event_by_source: dict[str, RawEvent] = {e.source_id: e for e in events}

        saved_insights = []
        for raw in raw_insights:
            insight = Insight(
                brief_id=brief.id,
                org_id=org_uuid,
                rank=raw["rank"],
                title=raw["title"],
                explanation=raw["explanation"],
                suggested_action=raw["suggested_action"],
                confidence=float(raw["confidence"]),
            )
            db.add(insight)
            db.flush()

            for ev in raw.get("evidence", []):
                source_id = str(ev.get("source_id", ""))
                raw_event = event_by_source.get(source_id)
                if raw_event is None:
                    continue
                db.add(EvidenceRef(
                    insight_id=insight.id,
                    raw_event_id=raw_event.id,
                    excerpt=ev.get("excerpt", "")[:500],
                    url=ev.get("url", raw_event.url or ""),
                    relevance_score=1.0,
                ))

            saved_insights.append(raw)

        brief.status = "ready"
        brief.generated_at = datetime.now(timezone.utc)
        db.commit()

        # ------------------------------------------------------------------ #
        # 6. Deliver — send email if org has a brief_email set               #
        # ------------------------------------------------------------------ #
        org = db.get(Organization, org_uuid)
        recipient = (org.settings or {}).get("brief_email") if org else None

        if recipient:
            try:
                message_id = send_brief_email(
                    recipient=recipient,
                    brief_id=str(brief.id),
                    insights=saved_insights,
                    period_start=period_start_str,
                    period_end=period_end_str,
                )
                db.add(BriefDelivery(
                    brief_id=brief.id,
                    channel="email",
                    recipient=recipient,
                    status="sent",
                    external_message_id=message_id,
                    sent_at=datetime.now(timezone.utc),
                ))
            except Exception:
                db.add(BriefDelivery(
                    brief_id=brief.id,
                    channel="email",
                    recipient=recipient,
                    status="failed",
                ))
            db.commit()

        return {
            "status": "ok",
            "brief_id": str(brief.id),
            "insights": len(saved_insights),
            "delivered_to": recipient,
        }

    finally:
        db.close()
