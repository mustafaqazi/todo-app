'use client'

/**
 * Empty State Component
 * Displays when user has no tasks
 * Shows inspirational message and encourages action
 *
 * Acceptance Criteria:
 * ✅ Displays centered icon and text
 * ✅ Fade-in animation on mount
 * ✅ Perfect dark/light mode styling
 * ✅ Responsive padding
 */

import { CheckCircle2 } from 'lucide-react'

interface EmptyStateProps {
  onAddTask?: () => void
}

export function EmptyState({ onAddTask }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-96 py-12 px-4 animate-fade-in">
      {/* Icon */}
      <div className="mb-4">
        <CheckCircle2 className="w-12 h-12 sm:w-16 sm:h-16 text-emerald-500 dark:text-emerald-400 opacity-50" />
      </div>

      {/* Heading */}
      <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-50 text-center mb-2">
        No tasks yet
      </h2>

      {/* Subtitle */}
      <p className="text-slate-600 dark:text-slate-400 text-center mb-6 max-w-sm">
        Start your productive day! Click "Add Task" to create your first task.
      </p>

      {/* Optional CTA Button */}
      {onAddTask && (
        <button
          onClick={onAddTask}
          className="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 dark:bg-emerald-600 dark:hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors"
        >
          Create First Task
        </button>
      )}
    </div>
  )
}
