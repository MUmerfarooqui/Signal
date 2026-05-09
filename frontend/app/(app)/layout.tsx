import { auth } from "@clerk/nextjs/server"
import { api } from "@/lib/api"
import Sidebar from "@/components/sidebar"

export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const { getToken } = await auth()
  const token = await getToken()

  let orgName: string | undefined
  try {
    if (token) {
      const org = await api.orgs.me(token)
      orgName = org.org_name
    }
  } catch {
    // not onboarded yet — sidebar falls back to "Signal"
  }

  return (
    <div className="flex h-screen overflow-hidden bg-zinc-50 dark:bg-zinc-950">
      <Sidebar orgName={orgName} />
      <main className="flex flex-1 flex-col overflow-y-auto">
        {children}
      </main>
    </div>
  )
}
