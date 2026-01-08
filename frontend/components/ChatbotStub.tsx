'use client'

/**
 * Chatbot Stub Component (Phase 3 Ready)
 * Floating bubble at bottom-right with drawer
 * Displays sample messages and "coming soon" messaging
 * Doesn't interfere with task list
 *
 * Acceptance Criteria:
 * ✅ Floating bubble at bottom-right (z-50)
 * ✅ Click opens drawer with messages
 * ✅ "Coming soon" message displays
 * ✅ Close button works
 * ✅ No layout shift on open/close
 * ✅ Responsive (full-width mobile, 400px desktop)
 * ✅ Dark/light mode styling
 */

import { useState } from 'react'
import { X, MessageCircle } from 'lucide-react'

export function ChatbotStub() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Floating Bubble Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-12 h-12 bg-emerald-600 hover:bg-emerald-700 dark:bg-emerald-600 dark:hover:bg-emerald-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-110 animate-scale-in"
        aria-label="Open chat"
        title="Chat (Coming soon)"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Drawer Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/30 dark:bg-black/50 animate-fade-in"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Drawer Panel */}
      {isOpen && (
        <div className="fixed bottom-0 right-0 z-45 w-full md:w-96 h-96 md:h-auto md:max-h-96 bg-white dark:bg-slate-800 border-t md:border md:border-slate-200 dark:md:border-slate-700 md:rounded-lg md:shadow-2xl animate-slide-in-right">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-slate-200 dark:border-slate-700">
            <h3 className="font-semibold text-slate-900 dark:text-slate-50">
              Task Assistant
            </h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
              aria-label="Close"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-72 md:max-h-64">
            {/* Assistant message */}
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-emerald-100 dark:bg-emerald-900 rounded-full flex items-center justify-center">
                <span className="text-emerald-600 dark:text-emerald-400 text-sm">AI</span>
              </div>
              <div className="bg-slate-100 dark:bg-slate-700 rounded-lg p-3 max-w-xs">
                <p className="text-sm text-slate-900 dark:text-slate-50">
                  Hello! I'm your task assistant. I'm coming soon in Phase 3!
                </p>
              </div>
            </div>

            {/* User message */}
            <div className="flex gap-3 justify-end">
              <div className="bg-emerald-600 dark:bg-emerald-600 rounded-lg p-3 max-w-xs">
                <p className="text-sm text-white">
                  What can you help me with?
                </p>
              </div>
            </div>

            {/* Assistant message */}
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-emerald-100 dark:bg-emerald-900 rounded-full flex items-center justify-center">
                <span className="text-emerald-600 dark:text-emerald-400 text-sm">AI</span>
              </div>
              <div className="bg-slate-100 dark:bg-slate-700 rounded-lg p-3 max-w-xs">
                <p className="text-sm text-slate-900 dark:text-slate-50">
                  In Phase 3, I'll help you with intelligent task suggestions, priority recommendations, and smart task organization!
                </p>
              </div>
            </div>
          </div>

          {/* Footer: Coming Soon Banner */}
          <div className="border-t border-slate-200 dark:border-slate-700 p-4 bg-emerald-50 dark:bg-slate-700">
            <p className="text-xs text-emerald-800 dark:text-emerald-200 font-medium text-center">
              🚀 Chat Support Coming Soon in Phase 3
            </p>
          </div>
        </div>
      )}
    </>
  )
}
