'use client'

import { useState, useCallback } from 'react'
import { useTasks } from '@/lib/hooks/useTasks'
import { TaskCard } from '@/components/TaskCard'
import { TaskTable } from '@/components/TaskTable'
import { TaskFilters } from '@/components/TaskFilters'
import { EmptyState } from '@/components/EmptyState'
import { AddTaskDialog } from '@/components/AddTaskDialog'
import { EditTaskDialog } from '@/components/EditTaskDialog'
import { DeleteConfirmation } from '@/components/DeleteConfirmation'
import { LoadingSkeletons } from '@/components/LoadingSkeletons'
import { Plus } from 'lucide-react'
import { calculateTaskStats } from '@/lib/utils'
import type { Task, CreateTaskPayload, UpdateTaskPayload, TaskFilter } from '@/lib/types'

export function TasksContent() {
  const {
    tasks,
    filteredTasks,
    filter,
    isLoading,
    addTask,
    updateTask,
    deleteTask,
    toggleComplete,
    setFilter,
  } = useTasks()

  const [showAddDialog, setShowAddDialog] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deletingTask, setDeletingTask] = useState<Task | null>(null)

  // Handle add task
  const handleAddTask = useCallback(
    async (payload: CreateTaskPayload) => {
      await addTask(payload)
      setShowAddDialog(false)
    },
    [addTask]
  )

  // Handle edit task
  const handleEditTask = useCallback(
    async (payload: UpdateTaskPayload) => {
      if (!editingTask) return
      await updateTask(editingTask.id, payload)
      setEditingTask(null)
    },
    [editingTask, updateTask]
  )

  // Handle delete task
  const handleDeleteTask = useCallback(
    async (taskId: string) => {
      await deleteTask(taskId)
      setDeletingTask(null)
    },
    [deleteTask]
  )

  // Handle toggle complete
  const handleToggleComplete = useCallback(
    (task: Task) => {
      toggleComplete(task.id)
    },
    [toggleComplete]
  )

  if (isLoading) {
    return <LoadingSkeletons />
  }

  // Calculate task statistics
  const stats = calculateTaskStats(tasks)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold text-slate-900 dark:text-slate-50">
            My Tasks
          </h1>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            {filteredTasks.length} {filteredTasks.length === 1 ? 'task' : 'tasks'}
            {filter !== 'all' && ` (${filter})`}
          </p>
        </div>

        {/* Add Task Button (Desktop) */}
        <button
          onClick={() => setShowAddDialog(true)}
          className="hidden sm:flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 dark:bg-emerald-600 dark:hover:bg-emerald-700 text-white rounded-lg font-medium transition-colors"
        >
          <Plus className="w-5 h-5" />
          Add Task
        </button>
      </div>

      {/* Filter Controls */}
      {tasks.length > 0 && (
        <TaskFilters
          currentFilter={filter as TaskFilter}
          onFilterChange={(newFilter) => setFilter(newFilter)}
          pendingCount={stats.pending}
          completedCount={stats.completed}
        />
      )}

      {/* Content */}
      {filteredTasks.length === 0 ? (
        <EmptyState onAddTask={() => setShowAddDialog(true)} />
      ) : (
        <>
          {/* Mobile: Card View */}
          <div className="md:hidden space-y-3">
            {filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={setEditingTask}
                onDelete={setDeletingTask}
                onToggleComplete={handleToggleComplete}
              />
            ))}
          </div>

          {/* Desktop: Table View */}
          <div className="hidden md:block">
            <TaskTable
              tasks={filteredTasks}
              onEdit={setEditingTask}
              onDelete={setDeletingTask}
              onToggleComplete={handleToggleComplete}
            />
          </div>
        </>
      )}

      {/* Mobile FAB (Floating Action Button) */}
      {filteredTasks.length > 0 && (
        <button
          onClick={() => setShowAddDialog(true)}
          className="sm:hidden fixed bottom-6 right-6 z-40 w-14 h-14 bg-emerald-600 hover:bg-emerald-700 dark:bg-emerald-600 dark:hover:bg-emerald-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-110"
          aria-label="Add task"
        >
          <Plus className="w-6 h-6" />
        </button>
      )}

      {/* Dialogs */}
      {showAddDialog && (
        <AddTaskDialog
          isOpen={showAddDialog}
          onOpenChange={setShowAddDialog}
          onSubmit={handleAddTask}
        />
      )}

      {editingTask && (
        <EditTaskDialog
          isOpen={true}
          task={editingTask}
          onOpenChange={(open) => !open && setEditingTask(null)}
          onSubmit={handleEditTask}
        />
      )}

      {deletingTask && (
        <DeleteConfirmation
          isOpen={true}
          taskTitle={deletingTask.title}
          onOpenChange={(open) => !open && setDeletingTask(null)}
          onConfirm={() => handleDeleteTask(deletingTask.id)}
        />
      )}
    </div>
  )
}
