"use client"

import { useEffect, useState } from "react"
import { ChatProvider } from "./chat/ChatProvider"

interface Props {
  children: React.ReactNode
}

/**
 * RootLayoutClient
 * Wraps root layout with client-side providers:
 * - ChatProvider: Manages chatbot conversation state
 * - Dark mode detection for theme persistence
 *
 * Authentication via JWT (Better Auth):
 * - JWT tokens are stored by Better Auth
 * - Centralized API client (/lib/api.ts) automatically attaches JWT to requests
 * - No SessionProvider needed for JWT-based auth
 */
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

  return (
    <ChatProvider>
      <div className={theme}>{children}</div>
    </ChatProvider>
  )
}
