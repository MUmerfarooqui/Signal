import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.db.session import get_db
from app.models.insight_feed_item import InsightFeedItem

router = APIRouter()


class FeedItemOut(BaseModel):
    id: uuid.UUID
    signal_type: str
    category: str | None
    title: str
    description: str
    severity: str
    ticket_count: int | None
    detected_at: datetime
    acknowledged_at: datetime | None

    model_config = {"from_attributes": True}


@router.get("", response_model=list[FeedItemOut])
def list_feed(
    org_id: uuid.UUID = Query(...),
    _user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return non-expired pulse feed items for an org, newest first."""
    now = datetime.now(timezone.utc)
    items = db.execute(
        select(InsightFeedItem)
        .where(
            InsightFeedItem.org_id == org_id,
            InsightFeedItem.expires_at > now,
        )
        .order_by(InsightFeedItem.detected_at.desc())
    ).scalars().all()
    return items
