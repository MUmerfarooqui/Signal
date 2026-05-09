import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from app.db.session import get_db
from app.models.organization import Organization
from app.models.organization_member import OrganizationMember
from app.models.user import User

router = APIRouter()


# --------------------------------------------------------------------------- #
# Schemas                                                                      #
# --------------------------------------------------------------------------- #

class CreateOrgRequest(BaseModel):
    org_name: str
    email: EmailStr
    user_name: str


class OrgResponse(BaseModel):
    org_id: uuid.UUID
    org_name: str
    user_id: uuid.UUID
    email: str
    role: str


# --------------------------------------------------------------------------- #
# Helpers                                                                      #
# --------------------------------------------------------------------------- #

def _get_or_create_user(db: Session, clerk_id: str, email: str, name: str) -> User:
    user = db.execute(
        select(User).where(User.clerk_id == clerk_id)
    ).scalar_one_or_none()

    if user is None:
        # Check if email exists from a previous signup without clerk_id
        user = db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    if user is None:
        user = User(clerk_id=clerk_id, email=email, name=name)
        db.add(user)
        db.flush()
    else:
        user.clerk_id = clerk_id
        user.last_login_at = datetime.now(timezone.utc)

    return user


# --------------------------------------------------------------------------- #
# Endpoints                                                                    #
# --------------------------------------------------------------------------- #

@router.post("", response_model=OrgResponse, status_code=status.HTTP_201_CREATED)
def create_org(
    body: CreateOrgRequest,
    clerk_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Called once when a user first signs up.
    Creates the org, the user record, and links them as owner.
    """
    # Prevent duplicate orgs for the same Clerk user
    existing_user = db.execute(
        select(User).where(User.clerk_id == clerk_id)
    ).scalar_one_or_none()

    if existing_user:
        member = db.execute(
            select(OrganizationMember).where(OrganizationMember.user_id == existing_user.id)
        ).scalar_one_or_none()
        if member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already belongs to an org. Use GET /orgs/me.",
            )

    user = _get_or_create_user(db, clerk_id, body.email, body.user_name)

    org = Organization(name=body.org_name, settings={})
    db.add(org)
    db.flush()

    db.add(OrganizationMember(org_id=org.id, user_id=user.id, role="owner"))
    db.commit()

    return OrgResponse(
        org_id=org.id,
        org_name=org.name,
        user_id=user.id,
        email=user.email,
        role="owner",
    )


@router.get("/me", response_model=OrgResponse)
def get_my_org(
    clerk_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return the org for the currently authenticated user."""
    user = db.execute(
        select(User).where(User.clerk_id == clerk_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found. Call POST /orgs first.")

    member = db.execute(
        select(OrganizationMember).where(OrganizationMember.user_id == user.id)
    ).scalar_one_or_none()

    if member is None:
        raise HTTPException(status_code=404, detail="No org found for this user.")

    org = db.get(Organization, member.org_id)

    return OrgResponse(
        org_id=org.id,
        org_name=org.name,
        user_id=user.id,
        email=user.email,
        role=member.role,
    )
