'use client'

/**
 * ChatInput Component
 * Text input area with send button
 *
 * Features:
 * - Auto-focus on mount
 * - Enter to send, Shift+Enter for newline
 * - Loading state during message sending
 * - Character count / validation
 * - Disabled during API calls
 * - Responsive textarea
 */

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ChatInputProps {
  isLoading?: boolean
  onSendMessage: (message: string) => Promise<void>
  disabled?: boolean
  placeholder?: string
}

export function ChatInput({
  isLoading = false,
  onSendMessage,
  disabled = false,
  placeholder = 'Type a message... (Shift+Enter for newline)',
}: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [isLocalLoading, setIsLocalLoading] = useState(false)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-focus on mount
  useEffect(() => {
    textareaRef.current?.focus()
  }, [])

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px'
    }
  }, [message])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!message.trim() || isLoading || isLocalLoading || disabled) {
      return
    }

    const messageToSend = message.trim()
    setMessage('')
    setIsLocalLoading(true)

    try {
      await onSendMessage(messageToSend)
    } finally {
      setIsLocalLoading(false)
      textareaRef.current?.focus()
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Send on Enter (unless Shift is pressed)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e as unknown as React.FormEvent)
    }
  }

  const isDisabled = isLoading || isLocalLoading || disabled
  const charCount = message.length
  const maxChars = 5000

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-slate-200 dark:border-slate-800 p-4 bg-white dark:bg-slate-950"
    >
      <div className="flex flex-col gap-2">
        {/* Textarea */}
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value.slice(0, maxChars))}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isDisabled}
          className={cn(
            'w-full min-h-10 max-h-30 p-2 border rounded-lg bg-white dark:bg-slate-900 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 resize-none',
            'focus:outline-none focus:ring-2 focus:ring-teal-500 dark:focus:ring-teal-400 focus:border-transparent',
            isDisabled && 'opacity-50 cursor-not-allowed'
          )}
        />

        {/* Character count and send button */}
        <div className="flex items-center justify-between gap-2">
          <span className={cn(
            'text-xs',
            charCount > maxChars * 0.9
              ? 'text-red-500 dark:text-red-400'
              : 'text-slate-400 dark:text-slate-500'
          )}>
            {charCount} / {maxChars}
          </span>

          <Button
            type="submit"
            disabled={isDisabled || !message.trim()}
            className="bg-teal-600 hover:bg-teal-700 dark:bg-teal-700 dark:hover:bg-teal-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isDisabled ? (
              <>
                <span className="inline-block animate-spin mr-1">⏳</span>
                Sending...
              </>
            ) : (
              <>
                <Send className="w-4 h-4 mr-1" />
                Send
              </>
            )}
          </Button>
        </div>
      </div>
    </form>
  )
}
