import { auth } from "@clerk/nextjs/server"
import { redirect, notFound } from "next/navigation"
import Link from "next/link"
import { api, type Insight } from "@/lib/api"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, ExternalLink, Lightbulb, Zap, AlertCircle, TrendingDown, Puzzle, GitBranch } from "lucide-react"

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
}

function formatDateShort(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" })
}

const CATEGORY_META: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  recurring_pain:       { label: "Recurring Pain Point",  color: "bg-red-50 text-red-700 border-red-100 dark:bg-red-950 dark:text-red-300 dark:border-red-900",       icon: AlertCircle },
  feature_gap:          { label: "Feature Gap",           color: "bg-violet-50 text-violet-700 border-violet-100 dark:bg-violet-950 dark:text-violet-300 dark:border-violet-900", icon: Puzzle },
  onboarding_friction:  { label: "Onboarding Friction",   color: "bg-amber-50 text-amber-700 border-amber-100 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-900",   icon: GitBranch },
  reliability_issue:    { label: "Reliability Issue",     color: "bg-orange-50 text-orange-700 border-orange-100 dark:bg-orange-950 dark:text-orange-300 dark:border-orange-900", icon: Zap },
  workflow_blocker:     { label: "Workflow Blocker",      color: "bg-rose-50 text-rose-700 border-rose-100 dark:bg-rose-950 dark:text-rose-300 dark:border-rose-900",     icon: TrendingDown },
  churn_signal:         { label: "Churn Signal",          color: "bg-zinc-100 text-zinc-700 border-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:border-zinc-700",     icon: TrendingDown },
}

const ACCENT: Record<string, string> = {
  recurring_pain:      "border-l-red-400",
  feature_gap:         "border-l-violet-400",
  onboarding_friction: "border-l-amber-400",
  reliability_issue:   "border-l-orange-400",
  workflow_blocker:    "border-l-rose-400",
  churn_signal:        "border-l-zinc-400",
}

function confidenceLabel(score: number) {
  if (score >= 0.8) return { label: "High confidence", variant: "success" as const }
  if (score >= 0.6) return { label: "Medium confidence", variant: "warning" as const }
  return { label: "Low confidence", variant: "secondary" as const }
}

function InsightCard({ insight, index }: { insight: Insight; index: number }) {
  const meta = insight.category ? CATEGORY_META[insight.category] : null
  const accent = insight.category ? (ACCENT[insight.category] ?? "border-l-zinc-300") : "border-l-zinc-200"
  const { label: confLabel, variant: confVariant } = confidenceLabel(insight.confidence)
  const CategoryIcon = meta?.icon ?? Lightbulb

  return (
    <div className={`border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 rounded-xl border-l-4 ${accent} overflow-hidden`}>
      {/* Card header */}
      <div className="px-6 pt-5 pb-4">
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex items-center gap-2.5 flex-wrap">
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800 text-xs font-semibold text-zinc-600 dark:text-zinc-400 shrink-0">
              {insight.rank}
            </span>
            {meta && (
              <span className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-xs font-medium ${meta.color}`}>
                <CategoryIcon className="h-3 w-3" />
                {meta.label}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2 shrink-0">
            {insight.affected_count != null && (
              <span className="text-xs text-zinc-400 dark:text-zinc-500">
                {insight.affected_count} {insight.affected_count === 1 ? "ticket" : "tickets"}
              </span>
            )}
            <Badge variant={confVariant}>{confLabel}</Badge>
          </div>
        </div>

        <h2 className="text-base font-semibold text-zinc-900 dark:text-zinc-50 leading-snug mb-3">
          {insight.title}
        </h2>

        <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
          {insight.explanation}
        </p>
      </div>

      {/* Suggested action */}
      <div className="mx-6 mb-5 rounded-lg bg-zinc-50 dark:bg-zinc-900 border border-zinc-100 dark:border-zinc-800 px-4 py-3.5">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 mb-1.5">Suggested action</p>
        <p className="text-sm text-zinc-800 dark:text-zinc-200 leading-relaxed">{insight.suggested_action}</p>
      </div>

      {/* Evidence */}
      {insight.evidence.length > 0 && (
        <div className="border-t border-zinc-100 dark:border-zinc-800 px-6 py-4">
          <p className="text-[10px] font-semibold uppercase tracking-widest text-zinc-400 mb-3">
            Evidence · {insight.evidence.length} {insight.evidence.length === 1 ? "source" : "sources"}
          </p>
          <div className="space-y-2.5">
            {insight.evidence.map((ev) => (
              <div key={ev.id} className="flex items-start gap-2.5 group">
                <div className="mt-0.5 h-1.5 w-1.5 shrink-0 rounded-full bg-zinc-300 dark:bg-zinc-600" />
                <p className="flex-1 text-xs text-zinc-500 dark:text-zinc-400 italic leading-relaxed line-clamp-2">
                  "{ev.excerpt}"
                </p>
                {ev.url && (
                  <a
                    href={ev.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="shrink-0 text-zinc-300 dark:text-zinc-600 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors"
                  >
                    <ExternalLink className="h-3.5 w-3.5" />
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default async function BriefPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const { getToken } = await auth()
  const token = await getToken()
  if (!token) redirect("/sign-in")

  let brief
  try {
    brief = await api.briefs.get(token, id)
  } catch {
    notFound()
  }

  const categoryCounts = brief.insights.reduce<Record<string, number>>((acc, i) => {
    if (i.category) acc[i.category] = (acc[i.category] ?? 0) + 1
    return acc
  }, {})

  return (
    <div className="flex flex-col flex-1 px-8 py-8 max-w-3xl w-full mx-auto">
      {/* Back */}
      <Link
        href="/dashboard"
        className="inline-flex items-center gap-1.5 text-sm text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 mb-8 transition-colors w-fit"
      >
        <ArrowLeft className="h-3.5 w-3.5" />
        All briefs
      </Link>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">
          {formatDateShort(brief.period_start)} – {formatDate(brief.period_end)}
        </h1>
        <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
          {brief.insight_count} {brief.insight_count === 1 ? "insight" : "insights"}
          {brief.generated_at && ` · Generated ${formatDate(brief.generated_at)}`}
        </p>

        {/* Category breakdown */}
        {Object.keys(categoryCounts).length > 0 && (
          <div className="mt-4 flex flex-wrap gap-2">
            {Object.entries(categoryCounts).map(([cat, count]) => {
              const meta = CATEGORY_META[cat]
              if (!meta) return null
              const Icon = meta.icon
              return (
                <span key={cat} className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-xs font-medium ${meta.color}`}>
                  <Icon className="h-3 w-3" />
                  {count}× {meta.label}
                </span>
              )
            })}
          </div>
        )}
      </div>

      {/* Insights */}
      {brief.insights.length === 0 ? (
        <p className="text-sm text-zinc-500">No insights in this brief yet.</p>
      ) : (
        <div className="space-y-5">
          {brief.insights.map((insight, i) => (
            <InsightCard key={insight.id} insight={insight} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}
