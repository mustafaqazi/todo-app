'use client'

/**
 * Mobile Task Card Component
 * Displays task in card format for mobile/tablet views
 * Includes: title, description (truncated), date, status checkbox, edit/delete buttons
 * Hover effect with shadow lift
 *
 * Acceptance Criteria:
 * ✅ Shows task title (bold, lg)
 * ✅ Shows truncated description (2 lines)
 * ✅ Shows created date badge
 * ✅ Has checkbox to toggle status
 * ✅ Has edit/delete icon buttons
 * ✅ Hover lift animation
 * ✅ Perfect dark mode styling
 */

import { Trash2, Edit2, Calendar } from 'lucide-react'
import { formatDate } from '@/lib/utils'
import type { Task } from '@/lib/types'

interface TaskCardProps {
  task: Task
  onEdit: (task: Task) => void
  onDelete: (task: Task) => void
  onToggleComplete: (task: Task) => void
}

export function TaskCard({ task, onEdit, onDelete, onToggleComplete }: TaskCardProps) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-4 hover:shadow-md transition-shadow duration-300 hover:hover-lift">
      <div className="flex gap-3">
        {/* Checkbox */}
        <div className="flex-shrink-0 pt-1">
          <input
            type="checkbox"
            checked={task.status === 'completed'}
            onChange={() => onToggleComplete(task)}
            className="w-5 h-5 accent-emerald-600 rounded cursor-pointer"
            aria-label={`Mark task "${task.title}" as ${
              task.status === 'completed' ? 'incomplete' : 'complete'
            }`}
          />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`font-semibold text-base line-clamp-2 ${
              task.status === 'completed'
                ? 'line-through text-slate-400 dark:text-slate-500'
                : 'text-slate-900 dark:text-slate-50'
            }`}
          >
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 mt-1">
              {task.description}
            </p>
          )}

          {/* Date */}
          <div className="flex items-center gap-1 mt-2 text-xs text-slate-500 dark:text-slate-400">
            <Calendar className="w-3 h-3" />
            <span>{formatDate(task.createdAt)}</span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex-shrink-0 flex gap-2">
          <button
            onClick={() => onEdit(task)}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-md transition-colors"
            aria-label={`Edit task "${task.title}"`}
            title="Edit task"
          >
            <Edit2 className="w-4 h-4 text-slate-600 dark:text-slate-400" />
          </button>
          <button
            onClick={() => onDelete(task)}
            className="p-2 hover:bg-rose-50 dark:hover:bg-slate-700 rounded-md transition-colors"
            aria-label={`Delete task "${task.title}"`}
            title="Delete task"
          >
            <Trash2 className="w-4 h-4 text-rose-500 dark:text-rose-400" />
          </button>
        </div>
      </div>
    </div>
  )
}
