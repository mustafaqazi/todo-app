'use client'

/**
 * ChatMessageList Component
 * Displays welcome message, message history, and input area
 *
 * Authentication:
 * - Uses JWT token from Better Auth (stored in localStorage or auth state)
 * - Centralized API client handles JWT attachment automatically
 * - User ID extracted from JWT by backend
 */

import { useEffect, useRef, useState } from 'react'
import { useChat, type Message as ChatMessage } from '@/hooks/useChat'
import { chatWithAssistant, type ChatRequest } from '@/lib/api'
import { MessageBubble } from './MessageBubble'
import { ChatInput } from './ChatInput'
import { useToast } from '@/components/ui/use-toast'

interface ChatMessageListProps {
  userEmail: string
}

export function ChatMessageList({ userEmail }: ChatMessageListProps) {
  const {
    messages,
    currentConversationId,
    createNewConversation,
    addAssistantMessage,
  } = useChat()
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const scrollContainerRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  // Create new conversation and show welcome message on mount
  useEffect(() => {
    if (messages.length === 0) {
      createNewConversation()

      // Add welcome message
      const welcomeMessage = `Hi ${userEmail}! 👋 I'm your smart TODO assistant. I can help you manage your tasks using natural language.

Try saying things like:
- "Add a task to buy milk"
- "Show my pending tasks"
- "Mark the groceries task complete"
- "Delete my meeting task"
- "Who am I?" (for user info)`

      addAssistantMessage(welcomeMessage)
    }
  }, [userEmail, messages.length, createNewConversation, addAssistantMessage])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Handle sending a message to the API
  const handleSendMessage = async (messageText: string) => {
    if (!currentConversationId) {
      toast({
        title: 'Error',
        description: 'Conversation not initialized. Please refresh the page.',
        variant: 'destructive',
      })
      return
    }

    setIsLoading(true)

    try {
      // Send to backend
      // User ID is extracted from JWT by the API client and backend
      const payload: ChatRequest = {
        conversation_id: currentConversationId,
        message: messageText,
      }

      const response = await chatWithAssistant(payload)

      if (response.error) {
        toast({
          title: 'Error',
          description: response.error.message || 'Failed to send message',
          variant: 'destructive',
        })
        return
      }

      if (response.data) {
        const data = response.data
        // Add assistant response
        addAssistantMessage(data.response, data.tool_calls || undefined)
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error'
      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="relative h-full flex flex-col bg-white dark:bg-slate-950">
      {/* Message area */}
      <div
        ref={scrollContainerRef}
        className="flex-1 overflow-y-auto p-4 bg-gradient-to-b from-white to-slate-50 dark:from-slate-950 dark:to-slate-900"
      >
        {messages.length === 0 ? (
          // Empty state with welcome
          <div className="flex flex-col items-center justify-center h-full text-center gap-4">
            <div className="text-5xl">🤖</div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
              Welcome to Smart TODO!
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 max-w-xs">
              Type a message to get started. I can help you manage your tasks!
            </p>
          </div>
        ) : (
          // Message list
          <div className="flex flex-col gap-4">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} userEmail={userEmail} />
            ))}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input area */}
      <ChatInput
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
        placeholder="Ask me to manage your tasks..."
      />
    </div>
  )
}
