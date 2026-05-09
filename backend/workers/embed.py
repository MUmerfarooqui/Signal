import uuid
from datetime import datetime, timezone

from openai import OpenAI
from sqlalchemy import select, update

from app.config import get_settings
from app.db.session import SessionLocal
from app.models.raw_event import RawEvent
from workers.celery_app import celery

settings = get_settings()

BATCH_SIZE = 500
EMBEDDING_MODEL = "text-embedding-3-small"


@celery.task(bind=True, max_retries=3, default_retry_delay=60)
def embed_events(self, org_id: str) -> dict:
    """
    Embed all unembedded raw events for an org.
    Runs after every sync. Safe to call multiple times (idempotent).
    """
    client = OpenAI(api_key=settings.openai_api_key)
    db = SessionLocal()
    total_embedded = 0

    try:
        while True:
            rows = db.execute(
                select(RawEvent)
                .where(
                    RawEvent.org_id == uuid.UUID(org_id),
                    RawEvent.embedding == None,  # noqa: E711
                )
                .limit(BATCH_SIZE)
            ).scalars().all()

            if not rows:
                break

            texts = [row.content for row in rows]
            ids = [row.id for row in rows]

            try:
                response = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=texts,
                )
            except Exception as exc:
                raise self.retry(exc=exc)

            now = datetime.now(timezone.utc)
            vectors = [item.embedding for item in response.data]

            for row_id, vector in zip(ids, vectors):
                db.execute(
                    update(RawEvent)
                    .where(RawEvent.id == row_id)
                    .values(embedding=vector, embedding_generated_at=now)
                )

            db.commit()
            total_embedded += len(rows)

    finally:
        db.close()

    return {"org_id": org_id, "embedded": total_embedded}
