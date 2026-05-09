import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import { api, type FeedItem } from "@/lib/api"
import { Activity, AlertCircle, Puzzle, GitBranch, Zap, TrendingDown } from "lucide-react"

function timeAgo(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const h = Math.floor(diff / 3_600_000)
  const d = Math.floor(diff / 86_400_000)
  if (d > 0) return `${d}d ago`
  if (h > 0) return `${h}h ago`
  return "Just now"
}

const SEVERITY_DOT: Record<string, string> = {
  high:   "bg-red-500",
  medium: "bg-amber-400",
  low:    "bg-zinc-400 dark:bg-zinc-500",
}

const SEVERITY_LABEL: Record<string, string> = {
  high:   "High",
  medium: "Medium",
  low:    "Low",
}

const CATEGORY_META: Record<string, { label: string; icon: React.ElementType }> = {
  recurring_pain:       { label: "Recurring Pain",      icon: AlertCircle },
  feature_gap:          { label: "Feature Gap",         icon: Puzzle },
  onboarding_friction:  { label: "Onboarding Friction", icon: GitBranch },
  reliability_issue:    { label: "Reliability Issue",   icon: Zap },
  workflow_blocker:     { label: "Workflow Blocker",    icon: TrendingDown },
  churn_signal:         { label: "Churn Signal",        icon: TrendingDown },
}

function FeedCard({ item }: { item: FeedItem }) {
  const dot = SEVERITY_DOT[item.severity] ?? SEVERITY_DOT.low
  const severityLabel = SEVERITY_LABEL[item.severity] ?? "Low"
  const meta = item.category ? CATEGORY_META[item.category] : null
  const Icon = meta?.icon

  return (
    <div className="flex gap-4 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-5 py-4">
      {/* Severity dot */}
      <div className="flex flex-col items-center pt-1 gap-1.5">
        <span className={`h-2 w-2 rounded-full shrink-0 ${dot}`} />
        <div className="w-px flex-1 bg-zinc-100 dark:bg-zinc-800" />
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0 pb-1">
        <div className="flex items-start justify-between gap-3 mb-1.5">
          <h3 className="text-sm font-medium text-zinc-900 dark:text-zinc-50 leading-snug">
            {item.title}
          </h3>
          <span className="text-xs text-zinc-400 dark:text-zinc-500 shrink-0">
            {timeAgo(item.detected_at)}
          </span>
        </div>

        <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed mb-3">
          {item.description}
        </p>

        <div className="flex items-center gap-2.5 flex-wrap">
          {/* Severity chip */}
          <span className="inline-flex items-center gap-1.5 text-xs text-zinc-500 dark:text-zinc-400">
            <span className={`h-1.5 w-1.5 rounded-full ${dot}`} />
            {severityLabel} signal
          </span>

          {/* Category chip */}
          {meta && Icon && (
            <>
              <span className="text-zinc-200 dark:text-zinc-700">·</span>
              <span className="inline-flex items-center gap-1 text-xs text-zinc-500 dark:text-zinc-400">
                <Icon className="h-3 w-3" />
                {meta.label}
              </span>
            </>
          )}

          {/* Ticket count */}
          {item.ticket_count != null && (
            <>
              <span className="text-zinc-200 dark:text-zinc-700">·</span>
              <span className="text-xs text-zinc-400 dark:text-zinc-500">
                {item.ticket_count} {item.ticket_count === 1 ? "ticket" : "tickets"}
              </span>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default async function PulsePage() {
  const { getToken } = await auth()
  const token = await getToken()
  if (!token) redirect("/sign-in")

  let items: FeedItem[] = []
  let orgId: string | null = null

  try {
    const org = await api.orgs.me(token)
    orgId = org.org_id
    items = await api.pulse.list(token, orgId)
  } catch {
    redirect("/onboarding")
  }

  const high   = items.filter(i => i.severity === "high")
  const medium = items.filter(i => i.severity === "medium")
  const low    = items.filter(i => i.severity === "low")

  return (
    <div className="flex flex-col flex-1 px-8 py-8 max-w-3xl w-full mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-1">
          <h1 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">Pulse</h1>
          {items.length > 0 && (
            <span className="inline-flex h-5 items-center rounded-full bg-zinc-100 dark:bg-zinc-800 px-2 text-xs font-medium text-zinc-600 dark:text-zinc-400">
              {items.length}
            </span>
          )}
        </div>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          Live signals between briefs — spikes, new patterns, anomalies.
        </p>

        {/* Summary bar */}
        {items.length > 0 && (
          <div className="mt-4 flex items-center gap-4">
            {high.length > 0 && (
              <span className="inline-flex items-center gap-1.5 text-xs font-medium text-red-600 dark:text-red-400">
                <span className="h-1.5 w-1.5 rounded-full bg-red-500" />
                {high.length} high
              </span>
            )}
            {medium.length > 0 && (
              <span className="inline-flex items-center gap-1.5 text-xs font-medium text-amber-600 dark:text-amber-400">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-400" />
                {medium.length} medium
              </span>
            )}
            {low.length > 0 && (
              <span className="inline-flex items-center gap-1.5 text-xs text-zinc-500 dark:text-zinc-400">
                <span className="h-1.5 w-1.5 rounded-full bg-zinc-400" />
                {low.length} low
              </span>
            )}
          </div>
        )}
      </div>

      {/* Feed */}
      {items.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center py-24 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 mb-4">
            <Activity className="h-5 w-5 text-zinc-400" />
          </div>
          <p className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">No signals yet</p>
          <p className="text-sm text-zinc-400 dark:text-zinc-500 max-w-xs leading-relaxed">
            Once your connectors are syncing, Pulse will surface emerging patterns in real time — before the next brief.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map(item => (
            <FeedCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  )
}
