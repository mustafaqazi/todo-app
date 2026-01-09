'use client'

/**
 * Desktop Task Table Component
 * Displays tasks in professional table format (desktop only)
 * Features:
 * - Zebra striping (alternating row colors)
 * - Hover row highlighting with emerald background
 * - Status checkbox (clickable)
 * - Title, description (truncated), date, actions (edit/delete)
 * - Smooth transitions (300ms)
 * - Sort by created date (most recent first)
 * - Dark/light mode styling
 * - Responsive table with horizontal scroll fallback
 *
 * Acceptance Criteria:
 * ✅ Zebra striping with slate-50/white rows
 * ✅ Hover row highlighting (light emerald)
 * ✅ Smooth transitions (300ms)
 * ✅ Status checkbox clickable
 * ✅ Date formatted nicely
 * ✅ Actions (edit/delete) with icons
 * ✅ Perfect dark mode styling
 * ✅ Responsive with horizontal scroll
 */

import { Edit2, Trash2, Calendar, CheckCircle2, Circle } from 'lucide-react'
import { formatDate, truncateText } from '@/lib/utils'
import type { Task } from '@/lib/types'

interface TaskTableProps {
  tasks: Task[]
  onEdit: (task: Task) => void
  onDelete: (task: Task) => void
  onToggleComplete: (task: Task) => void
}

export function TaskTable({
  tasks,
  onEdit,
  onDelete,
  onToggleComplete,
}: TaskTableProps) {
  // Sort tasks by created date (most recent first)
  const sortedTasks = [...tasks].sort(
    (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  )

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm">
      <table className="w-full text-sm">
        {/* Table Header */}
        <thead>
          <tr className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
            <th className="px-4 py-3 text-left font-semibold text-slate-700 dark:text-slate-300 w-12">
              Status
            </th>
            <th className="px-4 py-3 text-left font-semibold text-slate-700 dark:text-slate-300">
              Task
            </th>
            <th className="px-4 py-3 text-left font-semibold text-slate-700 dark:text-slate-300 hidden md:table-cell">
              Description
            </th>
            <th className="px-4 py-3 text-left font-semibold text-slate-700 dark:text-slate-300 w-28">
              Created
            </th>
            <th className="px-4 py-3 text-right font-semibold text-slate-700 dark:text-slate-300 w-20">
              Actions
            </th>
          </tr>
        </thead>

        {/* Table Body */}
        <tbody>
          {sortedTasks.map((task, index) => (
            <tr
              key={task.id}
              className={`border-b border-slate-200 dark:border-slate-700 transition-colors duration-300 hover:bg-emerald-50 dark:hover:bg-slate-700 ${
                index % 2 === 0
                  ? 'bg-white dark:bg-slate-900'
                  : 'bg-slate-50 dark:bg-slate-800/50'
              }`}
            >
              {/* Status Checkbox */}
              <td className="px-4 py-4 text-center">
                <button
                  onClick={() => onToggleComplete(task)}
                  className="inline-flex items-center justify-center p-1 hover:bg-emerald-100 dark:hover:bg-emerald-900/30 rounded transition-colors"
                  aria-label={`Mark task "${task.title}" as ${
                    task.status === 'completed' ? 'incomplete' : 'complete'
                  }`}
                  title={
                    task.status === 'completed'
                      ? 'Mark incomplete'
                      : 'Mark complete'
                  }
                >
                  {task.status === 'completed' ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                  ) : (
                    <Circle className="w-5 h-5 text-slate-400 dark:text-slate-500" />
                  )}
                </button>
              </td>

              {/* Task Title */}
              <td className="px-4 py-4">
                <span
                  className={`font-medium ${
                    task.status === 'completed'
                      ? 'line-through text-slate-400 dark:text-slate-500'
                      : 'text-slate-900 dark:text-slate-50'
                  }`}
                >
                  {task.title}
                </span>
              </td>

              {/* Description */}
              <td className="px-4 py-4 hidden md:table-cell text-slate-600 dark:text-slate-400">
                {task.description ? truncateText(task.description, 60) : '—'}
              </td>

              {/* Created Date */}
              <td className="px-4 py-4 text-slate-600 dark:text-slate-400">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>{formatDate(task.createdAt)}</span>
                </div>
              </td>

              {/* Actions */}
              <td className="px-4 py-4">
                <div className="flex justify-end gap-2">
                  <button
                    onClick={() => onEdit(task)}
                    className="p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 rounded transition-colors"
                    aria-label={`Edit task "${task.title}"`}
                    title="Edit task"
                  >
                    <Edit2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => onDelete(task)}
                    className="p-2 text-rose-600 dark:text-rose-400 hover:bg-rose-100 dark:hover:bg-slate-700 rounded transition-colors"
                    aria-label={`Delete task "${task.title}"`}
                    title="Delete task"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
