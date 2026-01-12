'use client'

/**
 * MessageBubble Component
 * Individual chat message display with role-based styling
 *
 * Features:
 * - User messages: right-aligned, teal background
 * - Assistant messages: left-aligned, slate background
 * - Smooth fade-in and slide animations
 * - Dark/light mode aware
 * - Optional tool call badges
 */

import { cn } from '@/lib/utils'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  tool_calls?: unknown[]
}

interface MessageBubbleProps {
  message: Message
  userEmail?: string
}

export function MessageBubble({ message, userEmail }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div
      className={cn('flex w-full gap-2 mb-3 animate-fadeInUp', isUser ? 'justify-end' : 'justify-start')}
    >
      <div
        className={cn(
          'max-w-xs px-3 py-2 rounded-lg shadow-sm',
          isUser
            ? 'bg-teal-600 text-white dark:bg-teal-700'
            : 'bg-slate-100 text-slate-900 dark:bg-slate-800 dark:text-slate-100',
        )}
      >
        <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>

        {/* Tool call badges (if assistant message) */}
        {!isUser && message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {message.tool_calls.map((toolCall: any, idx: number) => (
              <span
                key={idx}
                className="text-xs px-2 py-1 rounded bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100"
              >
                ✓ {toolCall.name || 'Tool executed'}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Timestamp (subtle, optional) */}
      <div className="text-xs text-slate-400 dark:text-slate-500 self-end mb-1">
        {new Date(message.timestamp).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        })}
      </div>

      {/* Fade and slide animation */}
      <style>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fadeInUp {
          animation: fadeInUp 0.3s ease-out;
        }
      `}</style>
    </div>
  )
}
