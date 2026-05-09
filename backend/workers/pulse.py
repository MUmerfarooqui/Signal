import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.insight_feed_item import InsightFeedItem
from app.models.raw_event import RawEvent
from workers.celery_app import celery
from workers.cluster import cluster_events


def _severity(count: int) -> str:
    if count >= 20:
        return "high"
    if count >= 10:
        return "medium"
    return "low"


def _title_from_text(text: str) -> str:
    """Extract a short label from the most representative ticket text."""
    first_line = text.strip().split("\n")[0]
    return first_line[:80].rstrip(".,;: ")


@celery.task
def detect_pulse(org_id: str) -> dict:
    """
    Cluster the last 24 h of embedded events. For any cluster >= 1.5x the
    daily average size, write an InsightFeedItem. No LLM calls.
    """
    db = SessionLocal()
    org_uuid = uuid.UUID(org_id)
    now = datetime.now(timezone.utc)

    try:
        window_24h = now - timedelta(hours=24)
        window_7d = now - timedelta(days=7)

        # ------------------------------------------------------------------ #
        # 1. Fetch recent events                                               #
        # ------------------------------------------------------------------ #
        recent_events = db.execute(
            select(RawEvent).where(
                RawEvent.org_id == org_uuid,
                RawEvent.embedding.is_not(None),
                RawEvent.created_at >= window_24h,
            )
        ).scalars().all()

        if len(recent_events) < 3:
            return {"status": "skipped", "reason": "insufficient_events"}

        # ------------------------------------------------------------------ #
        # 2. Compute 7-day daily average                                      #
        # ------------------------------------------------------------------ #
        total_7d = db.execute(
            select(func.count(RawEvent.id)).where(
                RawEvent.org_id == org_uuid,
                RawEvent.embedding.is_not(None),
                RawEvent.created_at >= window_7d,
            )
        ).scalar() or 0

        daily_average = total_7d / 7

        # ------------------------------------------------------------------ #
        # 3. Cluster 24h events                                               #
        # ------------------------------------------------------------------ #
        clusters = cluster_events(recent_events)
        items_created = 0

        for cluster in clusters:
            size = len(cluster.event_ids)

            # Must hit absolute minimum AND 1.5x daily average
            if size < 3:
                continue
            if daily_average > 0 and size < daily_average * 1.5:
                continue

            title = _title_from_text(cluster.texts[0])
            if not title:
                continue

            # De-duplicate: skip if identical title surfaced in last 24h
            exists = db.execute(
                select(InsightFeedItem).where(
                    InsightFeedItem.org_id == org_uuid,
                    InsightFeedItem.title == title,
                    InsightFeedItem.detected_at >= window_24h,
                )
            ).scalar_one_or_none()

            if exists:
                continue

            multiplier = round(size / max(daily_average, 1), 1)
            description = (
                f"{size} tickets on this topic in the last 24 hours"
                + (f" — {multiplier}× your daily average." if daily_average > 0 else ".")
            )

            db.add(InsightFeedItem(
                org_id=org_uuid,
                signal_type="spike",
                title=title,
                description=description,
                severity=_severity(size),
                ticket_count=size,
                detected_at=now,
                expires_at=now + timedelta(days=7),
            ))
            items_created += 1

        db.commit()
        return {"status": "ok", "items_created": items_created}

    finally:
        db.close()
