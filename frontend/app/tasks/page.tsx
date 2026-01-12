/**
 * Main Tasks Dashboard Page
 * Responsive layout: mobile cards, desktop table
 * Shows task list with filters, add dialog, edit/delete actions
 * Perfect dark/light mode styling, zero layout shift
 *
 * Acceptance Criteria:
 * ✅ Tasks fetched and displayed
 * ✅ Responsive: cards on mobile, table on desktop
 * ✅ Empty state shows when no tasks
 * ✅ Add Task FAB on mobile, button on desktop
 * ✅ Filter dropdown works
 * ✅ Loading skeletons during fetch
 * ✅ Perfect alignment, zero CLS
 */

import { Suspense } from 'react'
import type { Metadata } from 'next'
import { TasksContent } from '@/components/TasksContent'
import { LoadingSkeletons } from '@/components/LoadingSkeletons'

export const metadata: Metadata = {
  title: 'My Tasks - TODO App',
  description: 'Manage your tasks beautifully',
}

export default function TasksPage() {
  return (
    <div className="container-max py-8">
      <Suspense fallback={<LoadingSkeletons />}>
        <TasksContent />
      </Suspense>
    </div>
  )
}
