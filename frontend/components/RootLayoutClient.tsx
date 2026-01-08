"use client"

import { useEffect, useState } from "react"

interface Props {
  children: React.ReactNode
}

export default function RootLayoutClient({ children }: Props) {
  const [mounted, setMounted] = useState(false)
  const [theme, setTheme] = useState<"light" | "dark">("light")

  useEffect(() => {
    setMounted(true) // mark client as mounted

    // Detect system dark mode
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
    setTheme(prefersDark ? "dark" : "light")
  }, [])

  if (!mounted) return null // prevent SSR mismatch

  return <div className={theme}>{children}</div>
}
