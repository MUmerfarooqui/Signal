"use client"

import { useEffect } from "react"

export function TouchInit() {
  useEffect(() => {
    document.addEventListener("touchstart", () => {}, true)
  }, [])
  return null
}
