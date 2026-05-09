import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.db.session import get_db
from app.models.brief import Brief
from app.models.evidence_ref import EvidenceRef
from app.models.insight import Insight

router = APIRouter()


# --------------------------------------------------------------------------- #
# Schemas                                                                      #
# --------------------------------------------------------------------------- #

class EvidenceOut(BaseModel):
    id: uuid.UUID
    excerpt: str
    url: str | None
    relevance_score: float

    model_config = {"from_attributes": True}


class InsightOut(BaseModel):
    id: uuid.UUID
    rank: int
    title: str
    explanation: str
    suggested_action: str
    confidence: float
    category: str | None = None
    affected_count: int | None = None
    evidence: list[EvidenceOut] = []

    model_config = {"from_attributes": True}


class BriefSummary(BaseModel):
    id: uuid.UUID
    status: str
    period_start: datetime
    period_end: datetime
    generated_at: datetime | None
    insight_count: int

    model_config = {"from_attributes": True}


class BriefDetail(BriefSummary):
    insights: list[InsightOut] = []


class GenerateRequest(BaseModel):
    org_id: uuid.UUID


# --------------------------------------------------------------------------- #
# Endpoints                                                                    #
# --------------------------------------------------------------------------- #

@router.get("", response_model=list[BriefSummary])
def list_briefs(
    org_id: uuid.UUID = Query(...),
    _user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """List all briefs for an org, newest first."""
    briefs = db.execute(
        select(Brief)
        .where(Brief.org_id == org_id)
        .order_by(Brief.generated_at.desc().nullslast())
    ).scalars().all()

    result = []
    for brief in briefs:
        count = db.execute(
            select(Insight).where(Insight.brief_id == brief.id)
        ).scalars().all()
        result.append(BriefSummary(
            id=brief.id,
            status=brief.status,
            period_start=brief.period_start,
            period_end=brief.period_end,
            generated_at=brief.generated_at,
            insight_count=len(count),
        ))

    return result


@router.get("/{brief_id}", response_model=BriefDetail)
def get_brief(
    brief_id: uuid.UUID,
    _user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Get a brief with all its insights and evidence."""
    brief = db.get(Brief, brief_id)
    if brief is None:
        raise HTTPException(status_code=404, detail="Brief not found")

    insights = db.execute(
        select(Insight)
        .where(Insight.brief_id == brief_id)
        .order_by(Insight.rank)
    ).scalars().all()

    insights_out = []
    for insight in insights:
        evidence = db.execute(
            select(EvidenceRef).where(EvidenceRef.insight_id == insight.id)
        ).scalars().all()
        insights_out.append(InsightOut(
            id=insight.id,
            rank=insight.rank,
            title=insight.title,
            explanation=insight.explanation,
            suggested_action=insight.suggested_action,
            confidence=insight.confidence,
            evidence=[
                EvidenceOut(
                    id=e.id,
                    excerpt=e.excerpt,
                    url=e.url,
                    relevance_score=e.relevance_score,
                )
                for e in evidence
            ],
        ))

    insight_count = len(insights_out)
    return BriefDetail(
        id=brief.id,
        status=brief.status,
        period_start=brief.period_start,
        period_end=brief.period_end,
        generated_at=brief.generated_at,
        insight_count=insight_count,
        insights=insights_out,
    )


@router.post("/generate", status_code=202)
def trigger_generate(
    body: GenerateRequest,
    _user_id: str = Depends(get_current_user_id),
):
    """Manually trigger brief generation for an org. Returns immediately — runs in background."""
    from workers.brief import generate_brief
    generate_brief.delay(str(body.org_id))
    return {"status": "queued", "org_id": str(body.org_id)}
