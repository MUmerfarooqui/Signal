import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import Link from "next/link"
import { Zap, ArrowRight, PlugZap, BrainCircuit, FileText } from "lucide-react"
import { ThemeToggle } from "@/components/theme-toggle"

export default async function RootPage() {
  const { userId } = await auth()
  if (userId) redirect("/dashboard")

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900 flex flex-col">
      {/* Nav */}
      <header className="flex h-14 items-center justify-between px-8 border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950">
        <div className="flex items-center gap-2">
          <div className="flex h-6 w-6 items-center justify-center rounded bg-zinc-900 dark:bg-white">
            <Zap className="h-3.5 w-3.5 text-white dark:text-zinc-900" />
          </div>
          <span className="text-sm font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">Signal</span>
        </div>
        <div className="flex items-center gap-3">
          <ThemeToggle />
          <Link
            href="/sign-in"
            className="text-sm text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 transition-colors"
          >
            Sign in
          </Link>
          <Link
            href="/sign-up"
            className="inline-flex h-8 items-center gap-1.5 rounded-md bg-zinc-900 dark:bg-white px-4 text-xs font-medium text-white dark:text-zinc-900 hover:bg-zinc-700 dark:hover:bg-zinc-100 transition-colors"
          >
            Get started <ArrowRight className="h-3 w-3" />
          </Link>
        </div>
      </header>

      {/* Hero */}
      <main className="flex flex-1 flex-col items-center justify-center px-8 py-24 text-center bg-white dark:bg-zinc-950">
        <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-zinc-200 dark:border-zinc-800 px-3.5 py-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          <span className="text-xs text-zinc-500 dark:text-zinc-400 tracking-wide">Now in private beta</span>
        </div>

        <h1 className="max-w-2xl text-[2.75rem] font-semibold tracking-tight text-zinc-900 dark:text-zinc-50 leading-[1.13]">
          Product intelligence,<br />
          <span className="text-zinc-400 dark:text-zinc-500">without the noise.</span>
        </h1>

        <p className="mt-6 max-w-md text-[0.9375rem] text-zinc-500 dark:text-zinc-400 leading-relaxed">
          Signal connects to your tools, reasons across all of it, and delivers a weekly Intelligence Brief — prioritised, evidence-backed, no dashboard required.
        </p>

        <div className="mt-9 flex items-center gap-3">
          <Link
            href="/sign-up"
            className="inline-flex h-10 items-center gap-2 rounded-md bg-zinc-900 dark:bg-white px-6 text-sm font-medium text-white dark:text-zinc-900 hover:bg-zinc-700 dark:hover:bg-zinc-100 transition-colors"
          >
            Get started free <ArrowRight className="h-3.5 w-3.5" />
          </Link>
          <Link
            href="/sign-in"
            className="inline-flex h-10 items-center rounded-md border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-transparent px-6 text-sm text-zinc-600 dark:text-zinc-300 hover:border-zinc-300 hover:text-zinc-900 dark:hover:border-zinc-600 dark:hover:text-zinc-50 transition-colors"
          >
            Sign in
          </Link>
        </div>
      </main>

      {/* How it works */}
      <section className="px-8 py-16 bg-zinc-50 dark:bg-zinc-900 border-t border-zinc-100 dark:border-zinc-800">
        <div className="mx-auto max-w-4xl">
          <p className="mb-12 text-center text-[0.65rem] font-semibold uppercase tracking-[0.15em] text-zinc-400">
            How it works
          </p>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            {[
              {
                icon: PlugZap,
                step: "01",
                title: "Connect your tools",
                body: "One-click OAuth for Zendesk and Linear. Signal syncs automatically — no exports, no uploads, no manual steps.",
              },
              {
                icon: BrainCircuit,
                step: "02",
                title: "AI reasons across sources",
                body: "Claude identifies patterns that span tickets and issues. Cross-source signals surface automatically with confidence scoring.",
              },
              {
                icon: FileText,
                step: "03",
                title: "Brief delivered weekly",
                body: "Every Monday, a prioritised Intelligence Brief lands in your inbox. Each insight links back to the exact evidence behind it.",
              },
            ].map(({ icon: Icon, step, title, body }) => (
              <div key={step} className="flex flex-col gap-4 rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950 p-6">
                <div className="flex items-center justify-between">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-100 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900">
                    <Icon className="h-4 w-4 text-zinc-500 dark:text-zinc-400" />
                  </div>
                  <span className="text-xs font-mono font-medium text-zinc-300 dark:text-zinc-700">{step}</span>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-50 mb-1.5">{title}</h3>
                  <p className="text-sm text-zinc-500 dark:text-zinc-400 leading-relaxed">{body}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-100 dark:border-zinc-800 bg-white dark:bg-zinc-950 px-8 py-5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-5 w-5 items-center justify-center rounded bg-zinc-900 dark:bg-white">
            <Zap className="h-3 w-3 text-white dark:text-zinc-900" />
          </div>
          <span className="text-xs text-zinc-400">Signal</span>
        </div>
        <p className="text-xs text-zinc-400">Built for PMs who ship.</p>
      </footer>
    </div>
  )
}
