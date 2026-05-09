"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"
import { Sparkles } from "lucide-react"

export default function GenerateBriefButton({ orgId, token }: { orgId: string; token: string }) {
  const router = useRouter()
  const [loading, setLoading] = useState(false)

  async function handleGenerate() {
    setLoading(true)
    try {
      await api.briefs.generate(token, orgId)
      router.refresh()
    } finally {
      setLoading(false)
    }
  }

  return (
    <Button onClick={handleGenerate} disabled={loading} size="sm" variant="outline">
      <Sparkles className="h-3.5 w-3.5" />
      {loading ? "Queuing…" : "Generate brief"}
    </Button>
  )
}
