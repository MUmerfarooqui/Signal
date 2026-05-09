const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

async function request<T>(path: string, token: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}/api/v1${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options?.headers,
    },
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? "Request failed")
  }
  return res.json()
}

export const api = {
  orgs: {
    me: (token: string) => request<OrgResponse>("/orgs/me", token),
    create: (token: string, body: CreateOrgBody) =>
      request<OrgResponse>("/orgs", token, { method: "POST", body: JSON.stringify(body) }),
  },
  connectors: {
    list: (token: string, orgId: string) =>
      request<Connector[]>(`/connectors?org_id=${orgId}`, token),
    authorize: (token: string, orgId: string, subdomain: string) =>
      request<{ authorize_url: string }>(
        `/connectors/zendesk/authorize?org_id=${orgId}&subdomain=${subdomain}`,
        token
      ),
    sync: (token: string, connectorId: string, orgId: string) =>
      request<SyncResponse>("/connectors/sync", token, {
        method: "POST",
        body: JSON.stringify({ connector_id: connectorId, org_id: orgId }),
      }),
  },
  pulse: {
    list: (token: string, orgId: string) =>
      request<FeedItem[]>(`/pulse?org_id=${orgId}`, token),
  },
  briefs: {
    list: (token: string, orgId: string) =>
      request<BriefSummary[]>(`/briefs?org_id=${orgId}`, token),
    get: (token: string, briefId: string) =>
      request<BriefDetail>(`/briefs/${briefId}`, token),
    generate: (token: string, orgId: string) =>
      request<{ status: string }>("/briefs/generate", token, {
        method: "POST",
        body: JSON.stringify({ org_id: orgId }),
      }),
  },
}

// Types
export interface OrgResponse {
  org_id: string
  org_name: string
  user_id: string
  email: string
  role: string
}

export interface CreateOrgBody {
  org_name: string
  email: string
  user_name: string
}

export interface Connector {
  id: string
  org_id: string
  connector_type: string
  status: string
  config: Record<string, string>
  last_synced_at: string | null
}

export interface SyncResponse {
  events_ingested: number
  cursor: number | null
}

export interface FeedItem {
  id: string
  signal_type: string
  category: string | null
  title: string
  description: string
  severity: "low" | "medium" | "high"
  ticket_count: number | null
  detected_at: string
  acknowledged_at: string | null
}

export interface BriefSummary {
  id: string
  status: string
  period_start: string
  period_end: string
  generated_at: string | null
  insight_count: number
}

export interface Evidence {
  id: string
  excerpt: string
  url: string | null
  relevance_score: number
}

export interface Insight {
  id: string
  rank: number
  title: string
  explanation: string
  suggested_action: string
  confidence: number
  category: string | null
  affected_count: number | null
  evidence: Evidence[]
}

export interface BriefDetail extends BriefSummary {
  insights: Insight[]
}
