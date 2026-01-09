"use client"

import { useToast } from "@/components/ui/use-toast"

export function Toaster() {
  const { toasts } = useToast()

  return (
    <div className="fixed top-0 left-0 right-0 z-100 flex flex-col gap-2 pointer-events-none p-4 max-w-md mx-auto md:max-w-sm md:right-4 md:left-auto md:top-4">
      {toasts.map(function (toast) {
        return (
          <div
            key={toast.id}
            className={`p-4 rounded-lg shadow-lg text-white animate-slide-in-up pointer-events-auto ${
              toast.className || "bg-slate-900 dark:bg-slate-950"
            }`}
          >
            <div className="flex flex-col gap-1">
              {toast.title && <div className="font-semibold">{toast.title}</div>}
              {toast.description && <div className="text-sm opacity-90">{toast.description}</div>}
            </div>
          </div>
        )
      })}
    </div>
  )
}
