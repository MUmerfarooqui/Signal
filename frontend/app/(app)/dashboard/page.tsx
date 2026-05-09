import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import Link from "next/link"
import { api, type BriefSummary } from "@/lib/api"
import { Badge } from "@/components/ui/badge"
import { FileText, ArrowRight } from "lucide-react"
import GenerateBriefButton from "./generate-button"

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })
}

function statusVariant(status: string): "success" | "warning" | "secondary" {
  if (status === "ready") return "success"
  if (status === "generating") return "warning"
  return "secondary"
}

export default async function DashboardPage() {
  const { userId, getToken } = await auth()
  if (!userId) redirect("/sign-in")

  const token = await getToken()
  if (!token) redirect("/sign-in")

  let orgId: string | null = null
  let briefs: BriefSummary[] = []

  try {
    const org = await api.orgs.me(token)
    orgId = org.org_id
    briefs = await api.briefs.list(token, orgId)
  } catch {
    redirect("/onboarding")
  }

  return (
    <div className="flex flex-col flex-1 px-8 py-8 max-w-4xl w-full mx-auto">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">Intelligence Briefs</h1>
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
            Weekly summaries of what matters across your product.
          </p>
        </div>
        {orgId && <GenerateBriefButton orgId={orgId} token={token} />}
      </div>

      {/* Briefs list */}
      {briefs.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center text-center py-24">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-zinc-100 dark:bg-zinc-800 mb-4">
            <FileText className="h-5 w-5 text-zinc-400" />
          </div>
          <h2 className="text-sm font-medium text-zinc-900 dark:text-zinc-50">No briefs yet</h2>
          <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400 max-w-xs">
            Connect Zendesk, run a sync, then generate your first brief.
          </p>
          <Link
            href="/connectors"
            className="mt-4 text-sm font-medium text-zinc-900 underline-offset-4 hover:underline dark:text-zinc-50"
          >
            Go to Connectors →
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {briefs.map((brief) => (
            <Link
              key={brief.id}
              href={`/briefs/${brief.id}`}
              className="group flex items-center justify-between rounded-lg border border-zinc-200 bg-white px-5 py-4 shadow-sm transition-colors hover:border-zinc-300 hover:shadow dark:border-zinc-800 dark:bg-zinc-950 dark:hover:border-zinc-700"
            >
              <div className="flex items-center gap-4">
                <div className="flex h-9 w-9 items-center justify-center rounded-md bg-zinc-50 dark:bg-zinc-900">
                  <FileText className="h-4 w-4 text-zinc-400" />
                </div>
                <div>
                  <p className="text-sm font-medium text-zinc-900 dark:text-zinc-50">
                    {formatDate(brief.period_start)} – {formatDate(brief.period_end)}
                  </p>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                    {brief.insight_count} {brief.insight_count === 1 ? "insight" : "insights"}
                    {brief.generated_at && ` · Generated ${formatDate(brief.generated_at)}`}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Badge variant={statusVariant(brief.status)}>
                  {brief.status === "ready" ? "Ready" : brief.status === "generating" ? "Generating…" : brief.status}
                </Badge>
                <ArrowRight className="h-4 w-4 text-zinc-300 group-hover:text-zinc-500 transition-colors" />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
