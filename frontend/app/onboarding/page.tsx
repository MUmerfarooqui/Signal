"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth, useUser } from "@clerk/nextjs"
import { api } from "@/lib/api"
import { Button } from "@/components/ui/button"

export default function OnboardingPage() {
  const router = useRouter()
  const { getToken } = useAuth()
  const { user } = useUser()
  const [orgName, setOrgName] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!orgName.trim()) return
    setLoading(true)
    setError("")
    try {
      const token = await getToken()
      if (!token) throw new Error("Not authenticated")
      await api.orgs.create(token, {
        org_name: orgName.trim(),
        email: user?.primaryEmailAddress?.emailAddress ?? "",
        user_name: user?.fullName ?? user?.username ?? "User",
      })
      router.push("/connectors")
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-50 dark:bg-zinc-950 px-4">
      <div className="w-full max-w-md">
        <div className="mb-8">
          <h1 className="text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            Set up your workspace
          </h1>
          <p className="mt-2 text-sm text-zinc-500 dark:text-zinc-400">
            Signal organises everything under your company name.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1.5">
              Company name
            </label>
            <input
              type="text"
              value={orgName}
              onChange={(e) => setOrgName(e.target.value)}
              placeholder="Acme Inc."
              className="w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-900 dark:border-zinc-800 dark:bg-zinc-950 dark:text-zinc-50 dark:focus:ring-zinc-300"
              autoFocus
            />
          </div>

          {error && <p className="text-sm text-red-500">{error}</p>}

          <Button type="submit" className="w-full" disabled={loading || !orgName.trim()}>
            {loading ? "Creating…" : "Continue"}
          </Button>
        </form>
      </div>
    </div>
  )
}
