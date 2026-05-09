"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"

export default function SyncButton({ connectorId, orgId, token }: { connectorId: string; orgId: string; token: string }) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<string | null>(null)

  async function handleSync() {
    setLoading(true)
    setResult(null)
    try {
      const data = await api.connectors.sync(token, connectorId, orgId)
      setResult(`${data.events_ingested} new tickets`)
      router.refresh()
    } catch {
      setResult("Sync failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center gap-2">
      {result && <span className="text-xs text-zinc-500">{result}</span>}
      <Button size="sm" variant="outline" onClick={handleSync} disabled={loading}>
        <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
        {loading ? "Syncing…" : "Sync now"}
      </Button>
    </div>
  )
}
