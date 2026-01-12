'use client'

/**
 * ChatProvider Component
 * Provides chat trigger and window at the root level
 * Manages chat window open/close state
 */

import { useState } from 'react'
import { ChatTrigger } from './ChatTrigger'
import { ChatWindow } from './ChatWindow'

interface ChatProviderProps {
  children: React.ReactNode
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [isChatOpen, setIsChatOpen] = useState(false)

  return (
    <>
      {children}
      <ChatTrigger onOpen={() => setIsChatOpen(true)} />
      <ChatWindow isOpen={isChatOpen} onOpenChange={setIsChatOpen} />
    </>
  )
}
