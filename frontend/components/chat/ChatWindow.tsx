'use client'

/**
 * ChatWindow Component
 * Main chat interface using shadcn/ui Sheet
 *
 * Features:
 * - Sliding drawer from right side
 * - Glassmorphism backdrop
 * - Message history display
 * - Welcome message with user email
 * - Dark/light mode support
 * - Responsive on mobile and desktop
 */

import { useState, useEffect } from 'react'
import { useSession } from 'next-auth/react'
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetClose } from '@/components/ui/sheet'
import { X } from 'lucide-react'
import { ChatMessageList } from './ChatMessageList'

interface ChatWindowProps {
  isOpen: boolean
  onOpenChange: (open: boolean) => void
}

export function ChatWindow({ isOpen, onOpenChange }: ChatWindowProps) {
  const { data: session } = useSession()
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  if (!isClient) return null

  const userEmail = session?.user?.email || 'User'

  return (
    <Sheet open={isOpen} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="w-full sm:max-w-md p-0 border-l bg-white dark:bg-slate-950"
      >
        {/* Glassmorphism backdrop effect */}
        <div className="absolute inset-0 bg-black/40 backdrop-blur-sm pointer-events-none z-0" />

        <div className="relative z-10 h-full flex flex-col">
          {/* Header */}
          <SheetHeader className="border-b border-slate-200 dark:border-slate-800 p-4 sm:border-b">
            <div className="flex items-center justify-between w-full">
              <SheetTitle className="text-lg font-semibold text-slate-900 dark:text-white">
                Smart TODO Assistant
              </SheetTitle>
              <SheetClose className="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 disabled:pointer-events-none data-[state=open]:bg-slate-100 dark:data-[state=open]:bg-slate-800">
                <X className="h-4 w-4" />
                <span className="sr-only">Close</span>
              </SheetClose>
            </div>
          </SheetHeader>

          {/* Content Area */}
          <ChatMessageList userEmail={userEmail} />
        </div>
      </SheetContent>
    </Sheet>
  )
}
