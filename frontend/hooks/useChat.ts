'use client'

/**
 * useChat Hook
 * Manages chat state and conversation persistence for the AI todo chatbot.
 *
 * Features:
 * - Multi-conversation support with Map-based state
 * - localStorage coordination for persistence across sessions
 * - Message history with role-based storage
 * - Conversation ID management (UUID from backend)
 * - Loading and error states
 */

import { useState, useCallback, useEffect } from 'react'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  tool_calls?: unknown[]
}

export interface Conversation {
  id: string
  messages: Message[]
  created_at: number
  updated_at: number
}

interface UseChatReturn {
  // State
  currentConversationId: string | null
  messages: Message[]
  conversations: Map<string, Conversation>
  isLoading: boolean
  error: string | null

  // Actions
  sendMessage: (message: string) => Promise<void>
  loadConversation: (conversationId: string) => void
  createNewConversation: () => string
  addAssistantMessage: (content: string, toolCalls?: unknown[]) => Message

  // Utilities
  clearError: () => void
  deleteConversation: (conversationId: string) => void
}

const STORAGE_KEY_CONVERSATION = 'chat_conversation_id'
const STORAGE_KEY_CONVERSATIONS = 'chat_conversations'

export function useChat(): UseChatReturn {
  // State
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null)
  const [conversations, setConversations] = useState<Map<string, Conversation>>(new Map())
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Initialize from localStorage on mount
  useEffect(() => {
    if (typeof window === 'undefined') return

    // Load last conversation ID
    const savedConversationId = localStorage.getItem(STORAGE_KEY_CONVERSATION)
    if (savedConversationId) {
      setCurrentConversationId(savedConversationId)
      // Also load the message history for this conversation
      const savedConversations = localStorage.getItem(STORAGE_KEY_CONVERSATIONS)
      if (savedConversations) {
        try {
          const parsed = JSON.parse(savedConversations)
          const conversationMap = new Map<string, Conversation>(Object.entries(parsed))
          setConversations(conversationMap)

          if (conversationMap.has(savedConversationId)) {
            const conv = conversationMap.get(savedConversationId)!
            setMessages(conv.messages)
          }
        } catch (e) {
          console.error('Failed to load conversations from storage:', e)
        }
      }
    }
  }, [])

  // Save conversation ID to localStorage
  const saveConversationId = useCallback((id: string | null) => {
    if (typeof window === 'undefined') return
    if (id) {
      localStorage.setItem(STORAGE_KEY_CONVERSATION, id)
    } else {
      localStorage.removeItem(STORAGE_KEY_CONVERSATION)
    }
  }, [])

  // Save all conversations to localStorage
  const saveConversations = useCallback((convMap: Map<string, Conversation>) => {
    if (typeof window === 'undefined') return
    const obj = Object.fromEntries(convMap)
    localStorage.setItem(STORAGE_KEY_CONVERSATIONS, JSON.stringify(obj))
  }, [])

  // Create new conversation
  const createNewConversation = useCallback(() => {
    const newId = crypto.randomUUID()
    const newConversation: Conversation = {
      id: newId,
      messages: [],
      created_at: Date.now(),
      updated_at: Date.now(),
    }

    const newConversations = new Map(conversations)
    newConversations.set(newId, newConversation)

    setConversations(newConversations)
    setCurrentConversationId(newId)
    setMessages([])
    saveConversationId(newId)
    saveConversations(newConversations)

    return newId
  }, [conversations, saveConversationId, saveConversations])

  // Load conversation
  const loadConversation = useCallback(
    (conversationId: string) => {
      const conversation = conversations.get(conversationId)
      if (conversation) {
        setCurrentConversationId(conversationId)
        setMessages(conversation.messages)
        saveConversationId(conversationId)
      } else {
        console.warn(`Conversation ${conversationId} not found`)
        setError('Conversation not found')
      }
    },
    [conversations, saveConversationId],
  )

  // Add user message (handled by component, we just track it)
  const addUserMessage = useCallback(
    (content: string): Message => {
      const message: Message = {
        id: crypto.randomUUID(),
        role: 'user',
        content,
        timestamp: Date.now(),
      }

      const newMessages = [...messages, message]
      setMessages(newMessages)

      // Update conversation
      if (currentConversationId) {
        const newConversations = new Map(conversations)
        const conv = newConversations.get(currentConversationId)!
        conv.messages = newMessages
        conv.updated_at = Date.now()
        newConversations.set(currentConversationId, conv)
        setConversations(newConversations)
        saveConversations(newConversations)
      }

      return message
    },
    [messages, currentConversationId, conversations, saveConversations],
  )

  // Add assistant message
  const addAssistantMessage = useCallback(
    (content: string, toolCalls?: unknown[]): Message => {
      const message: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content,
        timestamp: Date.now(),
        tool_calls: toolCalls,
      }

      const newMessages = [...messages, message]
      setMessages(newMessages)

      // Update conversation
      if (currentConversationId) {
        const newConversations = new Map(conversations)
        const conv = newConversations.get(currentConversationId)!
        conv.messages = newMessages
        conv.updated_at = Date.now()
        newConversations.set(currentConversationId, conv)
        setConversations(newConversations)
        saveConversations(newConversations)
      }

      return message
    },
    [messages, currentConversationId, conversations, saveConversations],
  )

  // Send message to backend
  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) {
        setError('Message cannot be empty')
        return
      }

      // Create conversation if needed
      let convId = currentConversationId
      if (!convId) {
        convId = createNewConversation()
      }

      // Add user message
      addUserMessage(content)

      setIsLoading(true)
      setError(null)

      try {
        // This will be called by the component with chatWithAssistant
        // Here we just track the state; actual API call happens in the component
        // Return control to component to call API with proper userId context
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to send message'
        setError(errorMessage)
      } finally {
        setIsLoading(false)
      }
    },
    [currentConversationId, createNewConversation, addUserMessage],
  )

  // Clear error
  const clearError = useCallback(() => {
    setError(null)
  }, [])

  // Delete conversation
  const deleteConversation = useCallback(
    (conversationId: string) => {
      const newConversations = new Map(conversations)
      newConversations.delete(conversationId)
      setConversations(newConversations)

      if (currentConversationId === conversationId) {
        setCurrentConversationId(null)
        setMessages([])
        saveConversationId(null)
      }

      saveConversations(newConversations)
    },
    [conversations, currentConversationId, saveConversationId, saveConversations],
  )

  return {
    // State
    currentConversationId,
    messages,
    conversations,
    isLoading,
    error,

    // Actions
    sendMessage,
    loadConversation,
    createNewConversation,
    addAssistantMessage,

    // Utilities
    clearError,
    deleteConversation,
  }
}
