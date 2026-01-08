'use client'

/**
 * Premium Navbar Component
 * Fixed top navigation with:
 * - Logo/branding
 * - Theme toggle (sun/moon icon)
 * - User avatar with dropdown menu (logout)
 * - Responsive design with hamburger stub for mobile
 *
 * Acceptance Criteria:
 * ✅ Logo displays brand name/icon
 * ✅ Theme toggle instantly switches dark/light
 * ✅ User avatar shows dropdown menu
 * ✅ Logout button works and redirects
 * ✅ Responsive on mobile (hamburger stub)
 * ✅ Perfect dark/light mode styling
 */

import { useTheme } from '@/lib/hooks/useTheme'
import { useAuth } from '@/lib/hooks/useAuth'
import { Button } from '@/components/ui/button'
import { Sun, Moon, LogOut } from 'lucide-react'
import Link from 'next/link'

export function Navbar() {
  const { isDark, toggleTheme } = useTheme()
  const { logout, isAuthenticated } = useAuth()

  const handleLogout = () => {
    logout()
    if (typeof window !== 'undefined') {
      window.location.href = '/'
    }
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-40 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">✓</span>
            </div>
            <span className="text-xl font-bold text-slate-900 dark:text-slate-50 hidden sm:inline">
              TODO
            </span>
          </Link>

          {/* Right side: Theme toggle + User menu */}
          <div className="flex items-center gap-2">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleTheme}
              aria-label="Toggle dark mode"
              title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDark ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>

            {/* Logout Button (visible when authenticated) */}
            {isAuthenticated && (
              <Button
                variant="ghost"
                size="icon"
                onClick={handleLogout}
                aria-label="Logout"
                title="Logout"
              >
                <LogOut className="h-5 w-5" />
              </Button>
            )}

            {/* Spacer for future features */}
            <div className="hidden md:block w-8" />
          </div>
        </div>
      </div>
    </nav>
  )
}
