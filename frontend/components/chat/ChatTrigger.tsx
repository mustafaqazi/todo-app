'use client'

/**
 * ChatTrigger Component
 * Floating chat bubble in bottom-right corner
 *
 * Features:
 * - Only visible when authenticated
 * - Gradient teal/emerald colors (light/dark mode aware)
 * - Pulse animation for subtle attention
 * - Smooth open/close animations
 * - Responsive positioning
 */

import { useEffect, useState } from 'react'
import { useSession } from 'next-auth/react'
import { MessageCircle } from 'lucide-react'

interface ChatTriggerProps {
  onOpen?: () => void
}

export function ChatTrigger({ onOpen }: ChatTriggerProps) {
  const { data: session, status } = useSession()
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  // Only show when authenticated and client-side rendered
  if (!isClient || status !== 'authenticated') {
    return null
  }

  return (
    <button
      onClick={onOpen}
      className="fixed bottom-8 right-8 h-14 w-14 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 transform hover:scale-105 active:scale-95 z-40"
      style={{
        background: 'linear-gradient(135deg, #14b8a6 0%, #06b6d4 100%)',
        animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }}
      aria-label="Open chat"
      title="Chat with your todo assistant"
    >
      <div className="flex items-center justify-center h-full w-full">
        <MessageCircle className="w-6 h-6 text-white" />
      </div>

      {/* Pulse animation keyframes */}
      <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.7;
          }
        }
      `}</style>
    </button>
  )
}
