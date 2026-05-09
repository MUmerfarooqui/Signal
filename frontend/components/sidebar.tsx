"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, Plug, Activity, Zap } from "lucide-react"
import { UserButton } from "@clerk/nextjs"
import { cn } from "@/lib/utils"
import { ThemeToggle } from "./theme-toggle"

const nav = [
  { href: "/dashboard", label: "Briefs", icon: LayoutDashboard },
  { href: "/pulse", label: "Pulse", icon: Activity },
  { href: "/connectors", label: "Connectors", icon: Plug },
]

export default function Sidebar({ orgName }: { orgName?: string }) {
  const pathname = usePathname()

  return (
    <aside className="flex h-full w-56 flex-col border-r border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-950">
      {/* Logo + org */}
      <div className="flex h-14 items-center gap-2.5 border-b border-zinc-200 px-4 dark:border-zinc-800">
        <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded bg-zinc-900 dark:bg-zinc-50">
          <Zap className="h-3.5 w-3.5 text-white dark:text-zinc-900" />
        </div>
        <div className="min-w-0">
          <p className="text-xs font-semibold tracking-tight text-zinc-900 dark:text-zinc-50 truncate">
            {orgName ?? "Signal"}
          </p>
          {orgName && (
            <p className="text-[10px] text-zinc-400 dark:text-zinc-500 leading-none mt-0.5">Workspace</p>
          )}
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-0.5 p-2">
        {nav.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href)
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm transition-colors",
                active
                  ? "bg-zinc-100 font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-50"
                  : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-900 dark:hover:text-zinc-50"
              )}
            >
              <Icon className="h-4 w-4 shrink-0" />
              {label}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-zinc-200 p-3 dark:border-zinc-800">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <UserButton />
            <span className="text-xs text-zinc-500 dark:text-zinc-400">Account</span>
          </div>
          <ThemeToggle />
        </div>
      </div>
    </aside>
  )
}
