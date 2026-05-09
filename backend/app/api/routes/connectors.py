import hashlib
import hmac
import json
import uuid
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_id
from workers.embed import embed_events
from app.config import get_settings
from app.connectors.zendesk import (
    ZendeskClient,
    build_authorize_url,
    exchange_code_for_token,
    run_sync,
)
from app.db.session import get_db
from app.models.connector import Connector
from app.models.oauth_credential import OAuthCredential
from app.models.raw_event import RawEvent
from app.models.sync_cursor import SyncCursor

router = APIRouter()
settings = get_settings()

# --------------------------------------------------------------------------- #
# State token helpers (HMAC-signed, prevents CSRF)                            #
# --------------------------------------------------------------------------- #

def _sign_state(payload: dict) -> str:
    raw = json.dumps(payload, separators=(",", ":")).encode()
    body = urlsafe_b64encode(raw).rstrip(b"=").decode()
    sig = hmac.new(
        settings.zendesk_client_secret.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()[:16]
    return f"{body}.{sig}"


def _verify_state(state: str) -> dict:
    try:
        body, sig = state.rsplit(".", 1)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state")

    expected = hmac.new(
        settings.zendesk_client_secret.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()[:16]

    if not hmac.compare_digest(sig, expected):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State mismatch")

    padding = 4 - len(body) % 4
    raw = urlsafe_b64decode(body + "=" * padding)
    return json.loads(raw)


def _redirect_uri() -> str:
    return f"{settings.frontend_url.rstrip('/')}/api/auth/zendesk/callback"


# --------------------------------------------------------------------------- #
# Endpoints                                                                    #
# --------------------------------------------------------------------------- #

class AuthorizeResponse(BaseModel):
    authorize_url: str


@router.get("/zendesk/authorize", response_model=AuthorizeResponse)
def zendesk_authorize(
    org_id: uuid.UUID = Query(...),
    subdomain: str = Query(...),
    _user_id: str = Depends(get_current_user_id),
):
    """Return the Zendesk OAuth URL. Frontend opens this in a new window/tab."""
    state = _sign_state({"org_id": str(org_id), "subdomain": subdomain})
    redirect_uri = _redirect_uri()
    url = build_authorize_url(subdomain, settings.zendesk_client_id, redirect_uri, state)
    return AuthorizeResponse(authorize_url=url)


@router.get("/zendesk/callback")
def zendesk_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db),
):
    """
    Zendesk redirects here after user grants access.
    No Bearer token — this is a browser redirect from Zendesk.
    """
    payload = _verify_state(state)
    org_id = uuid.UUID(payload["org_id"])
    subdomain = payload["subdomain"]

    try:
        token_data = exchange_code_for_token(
            subdomain=subdomain,
            client_id=settings.zendesk_client_id,
            client_secret=settings.zendesk_client_secret,
            code=code,
            redirect_uri=_redirect_uri(),
        )
    except Exception:
        return RedirectResponse(
            url=f"{settings.frontend_url}/connectors?error=token_exchange_failed",
            status_code=302,
        )

    access_token = token_data.get("access_token")
    if not access_token:
        return RedirectResponse(
            url=f"{settings.frontend_url}/connectors?error=no_access_token",
            status_code=302,
        )

    # Upsert connector row (one Zendesk connector per org)
    connector = db.execute(
        select(Connector).where(
            Connector.org_id == org_id,
            Connector.connector_type == "zendesk",
        )
    ).scalar_one_or_none()

    if connector is None:
        connector = Connector(
            org_id=org_id,
            connector_type="zendesk",
            status="active",
            config={"subdomain": subdomain},
        )
        db.add(connector)
        db.flush()
    else:
        connector.status = "active"
        connector.config = {"subdomain": subdomain}

    # Upsert credential
    cred = db.execute(
        select(OAuthCredential).where(OAuthCredential.connector_id == connector.id)
    ).scalar_one_or_none()

    if cred is None:
        cred = OAuthCredential(
            connector_id=connector.id,
            access_token=access_token,
            scopes=token_data.get("scope"),
        )
        db.add(cred)
    else:
        cred.access_token = access_token
        cred.scopes = token_data.get("scope")

    db.commit()

    return RedirectResponse(
        url=f"{settings.frontend_url}/connectors?connected=zendesk",
        status_code=302,
    )


class ConnectorOut(BaseModel):
    id: uuid.UUID
    org_id: uuid.UUID
    connector_type: str
    status: str
    config: dict
    last_synced_at: datetime | None

    model_config = {"from_attributes": True}


@router.get("", response_model=list[ConnectorOut])
def list_connectors(
    org_id: uuid.UUID = Query(...),
    _user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """List all connectors for an org."""
    rows = db.execute(
        select(Connector).where(Connector.org_id == org_id)
    ).scalars().all()
    return rows


class SyncRequest(BaseModel):
    connector_id: uuid.UUID
    org_id: uuid.UUID


class SyncResponse(BaseModel):
    events_ingested: int
    cursor: int | None


@router.post("/sync", response_model=SyncResponse)
def trigger_sync(
    body: SyncRequest,
    _user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Trigger an immediate sync for a connector. Runs synchronously for MVP."""
    connector = db.execute(
        select(Connector).where(
            Connector.id == body.connector_id,
            Connector.org_id == body.org_id,
        )
    ).scalar_one_or_none()

    if connector is None:
        raise HTTPException(status_code=404, detail="Connector not found")

    cred = db.execute(
        select(OAuthCredential).where(OAuthCredential.connector_id == connector.id)
    ).scalar_one_or_none()

    if cred is None:
        raise HTTPException(status_code=400, detail="Connector has no credentials")

    subdomain = connector.config.get("subdomain", settings.zendesk_subdomain)

    # Fetch existing cursor
    cursor_row = db.execute(
        select(SyncCursor).where(SyncCursor.connector_id == connector.id)
    ).scalar_one_or_none()
    start_time = int(cursor_row.cursor_value) if cursor_row else 0

    client = ZendeskClient(subdomain=subdomain, access_token=cred.access_token)
    raw_events, new_cursor = run_sync(
        client=client,
        org_id=body.org_id,
        connector_id=connector.id,
        start_time=start_time,
    )

    # Bulk-insert events, skip duplicates via ON CONFLICT DO NOTHING
    inserted = 0
    for event in raw_events:
        existing = db.execute(
            select(RawEvent.id).where(
                RawEvent.connector_id == connector.id,
                RawEvent.source_id == event["source_id"],
            )
        ).scalar_one_or_none()
        if existing is None:
            db.add(RawEvent(**event))
            inserted += 1

    now = datetime.now(timezone.utc)

    # Update cursor
    if cursor_row is None:
        cursor_row = SyncCursor(
            connector_id=connector.id,
            cursor_value=str(new_cursor or 0),
            last_synced_at=now,
            events_ingested=inserted,
        )
        db.add(cursor_row)
    else:
        cursor_row.cursor_value = str(new_cursor or cursor_row.cursor_value)
        cursor_row.last_synced_at = now
        cursor_row.events_ingested += inserted

    connector.last_synced_at = now
    if inserted == 0 and len(raw_events) == 0:
        pass  # keep status active
    else:
        connector.status = "active"

    db.commit()

    if inserted > 0:
        embed_events.delay(str(body.org_id))

    return SyncResponse(events_ingested=inserted, cursor=new_cursor)
