'use client'

import { X } from 'lucide-react'

interface DeleteConfirmationProps {
  isOpen: boolean
  taskTitle: string
  onOpenChange: (open: boolean) => void
  onConfirm: () => Promise<void>
}

export function DeleteConfirmation({
  isOpen,
  taskTitle,
  onOpenChange,
  onConfirm,
}: DeleteConfirmationProps) {
  const handleConfirm = async () => {
    await onConfirm()
    onOpenChange(false)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 dark:bg-black/70 animate-fade-in">
      <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 shadow-2xl max-w-sm w-full animate-scale-in">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-700">
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-50">
            Delete Task
          </h2>
          <button
            onClick={() => onOpenChange(false)}
            className="text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          <p className="text-slate-600 dark:text-slate-400">
            Are you sure you want to delete this task?
          </p>
          <p className="text-slate-900 dark:text-slate-50 font-semibold break-words">
            "{taskTitle}"
          </p>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            This action cannot be undone.
          </p>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              onClick={() => onOpenChange(false)}
              className="flex-1 px-4 py-2 border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-900 dark:text-slate-50 rounded-lg font-medium transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleConfirm}
              className="flex-1 px-4 py-2 bg-rose-600 hover:bg-rose-700 dark:bg-rose-600 dark:hover:bg-rose-700 text-white rounded-lg font-medium transition-colors"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
