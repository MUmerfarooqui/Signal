import uuid
from datetime import datetime, timezone
from urllib.parse import urlencode

import httpx

# --------------------------------------------------------------------------- #
# OAuth helpers                                                                #
# --------------------------------------------------------------------------- #

def build_authorize_url(subdomain: str, client_id: str, redirect_uri: str, state: str) -> str:
    params = urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "read",
        "state": state,
    })
    return f"https://{subdomain}.zendesk.com/oauth/authorizations/new?{params}"


def exchange_code_for_token(
    subdomain: str,
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
) -> dict:
    resp = httpx.post(
        f"https://{subdomain}.zendesk.com/oauth/tokens",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "scope": "read",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


# --------------------------------------------------------------------------- #
# API client                                                                   #
# --------------------------------------------------------------------------- #

class ZendeskClient:
    def __init__(self, subdomain: str, access_token: str):
        self.subdomain = subdomain
        self.base_url = f"https://{subdomain}.zendesk.com/api/v2"
        self._headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def fetch_tickets_incremental(
        self, start_time: int = 0
    ) -> tuple[list[dict], int | None, bool]:
        """
        Pull tickets via Zendesk's incremental export.
        Returns (tickets, next_start_time, has_more).
        start_time=0 fetches from the beginning of the account.
        """
        resp = httpx.get(
            f"{self.base_url}/incremental/tickets.json",
            params={"start_time": start_time, "include": "comment_count"},
            headers=self._headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        tickets = data.get("tickets", [])
        end_time = data.get("end_time")
        end_of_stream = data.get("end_of_stream", True)
        return tickets, end_time, not end_of_stream

    def verify_connection(self) -> bool:
        """Quick check that credentials are valid."""
        try:
            resp = httpx.get(
                f"{self.base_url}/account.json",
                headers=self._headers,
                timeout=10,
            )
            return resp.status_code == 200
        except httpx.HTTPError:
            return False


# --------------------------------------------------------------------------- #
# Normalization                                                                #
# --------------------------------------------------------------------------- #

def normalize_ticket(
    ticket: dict,
    org_id: uuid.UUID,
    connector_id: uuid.UUID,
    subdomain: str,
) -> dict:
    """Map a raw Zendesk ticket dict to the RawEvent insert schema."""
    subject = ticket.get("subject") or ""
    description = ticket.get("description") or ""
    content = f"{subject}\n\n{description}".strip() if description else subject

    raw_created = ticket.get("created_at", "")
    created_at = (
        datetime.fromisoformat(raw_created.replace("Z", "+00:00"))
        if raw_created
        else datetime.now(timezone.utc)
    )

    return {
        "org_id": org_id,
        "connector_id": connector_id,
        "source": "zendesk",
        "source_id": str(ticket["id"]),
        "event_type": "ticket",
        "content": content,
        "metadata_": {
            "status": ticket.get("status"),
            "priority": ticket.get("priority"),
            "ticket_type": ticket.get("type"),
            "tags": ticket.get("tags", []),
            "requester_id": ticket.get("requester_id"),
            "assignee_id": ticket.get("assignee_id"),
            "subject": subject,
            "via": ticket.get("via", {}).get("channel"),
            "comment_count": ticket.get("comment_count"),
        },
        "url": f"https://{subdomain}.zendesk.com/agent/tickets/{ticket['id']}",
        "created_at": created_at,
    }


# --------------------------------------------------------------------------- #
# Sync                                                                         #
# --------------------------------------------------------------------------- #

def run_sync(
    client: ZendeskClient,
    org_id: uuid.UUID,
    connector_id: uuid.UUID,
    start_time: int = 0,
) -> tuple[list[dict], int | None]:
    """
    Fetch all tickets since start_time and return normalized RawEvent dicts.
    Handles pagination automatically.
    Returns (raw_event_dicts, final_cursor).
    """
    all_events: list[dict] = []
    cursor = start_time
    has_more = True

    while has_more:
        tickets, end_time, has_more = client.fetch_tickets_incremental(cursor)

        for ticket in tickets:
            # Skip deleted tickets
            if ticket.get("status") == "deleted":
                continue
            all_events.append(
                normalize_ticket(ticket, org_id, connector_id, client.subdomain)
            )

        if end_time:
            cursor = end_time

        # Safety: if no tickets returned, stop to avoid infinite loop
        if not tickets:
            break

    return all_events, cursor
