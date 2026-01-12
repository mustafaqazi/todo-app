"use client"

import { useEffect, useState } from "react"
import { SessionProvider } from "next-auth/react"
import { ChatProvider } from "./chat/ChatProvider"

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

  return (
    <SessionProvider>
      <ChatProvider>
        <div className={theme}>{children}</div>
      </ChatProvider>
    </SessionProvider>
  )
}
