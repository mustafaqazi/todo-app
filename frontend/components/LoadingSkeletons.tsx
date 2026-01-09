'use client'

/**
 * Loading Skeleton Components
 * Shows shimmer effect while data loads
 */

export function LoadingSkeletons() {
  return (
    <div className="space-y-4">
      {/* Header Skeleton */}
      <div className="space-y-3 mb-8">
        <div className="h-10 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-1/3 shimmer-bg" />
        <div className="h-4 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-1/4 shimmer-bg" />
      </div>

      {/* Task Card Skeletons */}
      {[...Array(5)].map((_, i) => (
        <div key={i} className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-4 animate-fade-in" style={{ animationDelay: `${i * 50}ms` }}>
          <div className="flex gap-3">
            {/* Checkbox */}
            <div className="w-5 h-5 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded shimmer-bg flex-shrink-0" />

            {/* Content */}
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-3/4 shimmer-bg" />
              <div className="h-3 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-full shimmer-bg" />
              <div className="h-3 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-2/3 shimmer-bg" />
            </div>

            {/* Actions */}
            <div className="flex gap-2 flex-shrink-0">
              <div className="w-9 h-9 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded shimmer-bg" />
              <div className="w-9 h-9 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded shimmer-bg" />
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export function TaskCardSkeleton() {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-4">
      <div className="flex gap-3">
        <div className="w-5 h-5 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded shimmer-bg flex-shrink-0" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-3/4 shimmer-bg" />
          <div className="h-3 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-full shimmer-bg" />
          <div className="h-3 bg-gradient-to-r from-slate-200 to-slate-100 dark:from-slate-700 dark:to-slate-800 rounded-lg w-2/3 shimmer-bg" />
        </div>
      </div>
    </div>
  )
}
