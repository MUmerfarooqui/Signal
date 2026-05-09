import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class EvidenceRef(Base):
    __tablename__ = "evidence_refs"
    __table_args__ = (
        Index("idx_evidence_refs_insight", "insight_id"),
        Index("idx_evidence_refs_event", "raw_event_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    insight_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("insights.id", ondelete="CASCADE"), nullable=False)
    raw_event_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("raw_events.id", ondelete="SET NULL"), nullable=True)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=True)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
