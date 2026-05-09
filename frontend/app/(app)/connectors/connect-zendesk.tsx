"use client"

import { useState } from "react"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"

export default function ConnectZendesk({ orgId, token }: { orgId: string; token: string }) {
  const [subdomain, setSubdomain] = useState("")
  const [showInput, setShowInput] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleConnect() {
    if (!subdomain.trim()) return
    setLoading(true)
    setError("")
    try {
      const { authorize_url } = await api.connectors.authorize(token, orgId, subdomain.trim())
      window.location.href = authorize_url
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to connect")
      setLoading(false)
    }
  }

  if (!showInput) {
    return (
      <Button size="sm" variant="outline" onClick={() => setShowInput(true)}>
        Connect
      </Button>
    )
  }

  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center rounded-md border border-zinc-200 bg-white overflow-hidden dark:border-zinc-800 dark:bg-zinc-950">
        <input
          type="text"
          value={subdomain}
          onChange={(e) => setSubdomain(e.target.value)}
          placeholder="yourcompany"
          className="w-36 px-3 py-1.5 text-sm text-zinc-900 placeholder:text-zinc-400 focus:outline-none dark:text-zinc-50 bg-transparent"
          autoFocus
          onKeyDown={(e) => e.key === "Enter" && handleConnect()}
        />
        <span className="pr-3 text-xs text-zinc-400">.zendesk.com</span>
      </div>
      <Button size="sm" onClick={handleConnect} disabled={loading || !subdomain.trim()}>
        {loading ? "Redirecting…" : "Authorise"}
      </Button>
      <Button size="sm" variant="ghost" onClick={() => { setShowInput(false); setError("") }}>
        Cancel
      </Button>
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  )
}
