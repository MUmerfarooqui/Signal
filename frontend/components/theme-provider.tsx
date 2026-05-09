"use client"

import { createContext, useContext, useEffect, useState } from "react"

type Theme = "light" | "dark"

const ThemeContext = createContext<{ theme: Theme; setTheme: (t: Theme) => void }>({
  theme: "light",
  setTheme: () => {},
})

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme>("light")
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem("signal-theme") as Theme | null
    const resolved = stored ?? "light"
    setThemeState(resolved)
    document.documentElement.classList.toggle("dark", resolved === "dark")
    setMounted(true)
  }, [])

  function setTheme(next: Theme) {
    setThemeState(next)
    localStorage.setItem("signal-theme", next)
    document.documentElement.classList.toggle("dark", next === "dark")
  }

  if (!mounted) return <>{children}</>

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  return useContext(ThemeContext)
}
