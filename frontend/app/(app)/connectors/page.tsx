import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import { api, type Connector } from "@/lib/api"
import ConnectZendesk from "./connect-zendesk"
import { Badge } from "@/components/ui/badge"
import { CheckCircle2, Circle, RefreshCw } from "lucide-react"
import SyncButton from "./sync-button"

function formatDate(iso: string | null) {
  if (!iso) return "Never"
  return new Date(iso).toLocaleDateString("en-US", {
    month: "short", day: "numeric", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  })
}

export default async function ConnectorsPage() {
  const { getToken } = await auth()
  const token = await getToken()
  if (!token) redirect("/sign-in")

  let orgId: string | null = null
  let connectors: Connector[] = []

  try {
    const org = await api.orgs.me(token)
    orgId = org.org_id
    connectors = await api.connectors.list(token, orgId)
  } catch {
    redirect("/onboarding")
  }

  const zendesk = connectors.find((c) => c.connector_type === "zendesk")

  return (
    <div className="flex flex-col flex-1 px-8 py-8 max-w-4xl w-full mx-auto">
      <div className="mb-8">
        <h1 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">Connectors</h1>
        <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-400">
          Connect your tools. Signal syncs automatically.
        </p>
      </div>

      <div className="space-y-3">
        {/* Zendesk */}
        <div className="flex items-center justify-between rounded-lg border border-zinc-200 bg-white px-5 py-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-950">
          <div className="flex items-center gap-4">
            <div className="flex h-9 w-9 items-center justify-center rounded-md bg-zinc-50 dark:bg-zinc-900 text-lg font-bold text-zinc-700 dark:text-zinc-300">
              Z
            </div>
            <div>
              <p className="text-sm font-medium text-zinc-900 dark:text-zinc-50">Zendesk</p>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                {zendesk
                  ? `${zendesk.config.subdomain}.zendesk.com · Last synced ${formatDate(zendesk.last_synced_at)}`
                  : "Support tickets"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {zendesk ? (
              <>
                <div className="flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  Connected
                </div>
                <SyncButton connectorId={zendesk.id} orgId={orgId!} token={token} />
              </>
            ) : (
              <>
                <div className="flex items-center gap-1.5 text-xs text-zinc-400">
                  <Circle className="h-3.5 w-3.5" />
                  Not connected
                </div>
                {orgId && <ConnectZendesk orgId={orgId} token={token} />}
              </>
            )}
          </div>
        </div>

        {/* Coming soon */}
        {[
          { name: "Linear", description: "Issues and projects", initial: "L" },
          { name: "Slack", description: "Customer feedback channels", initial: "S" },
        ].map(({ name, description, initial }) => (
          <div
            key={name}
            className="flex items-center justify-between rounded-lg border border-zinc-100 bg-white px-5 py-4 opacity-50 dark:border-zinc-900 dark:bg-zinc-950"
          >
            <div className="flex items-center gap-4">
              <div className="flex h-9 w-9 items-center justify-center rounded-md bg-zinc-50 dark:bg-zinc-900 text-lg font-bold text-zinc-400">
                {initial}
              </div>
              <div>
                <p className="text-sm font-medium text-zinc-900 dark:text-zinc-50">{name}</p>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">{description}</p>
              </div>
            </div>
            <Badge variant="secondary">Coming soon</Badge>
          </div>
        ))}
      </div>
    </div>
  )
}
