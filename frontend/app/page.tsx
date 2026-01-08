/**
 * Landing Page
 * Inspirational hero page with CTA to signup
 *
 * Acceptance Criteria:
 * ✅ Shows hero heading "Transform Your Tasks Into Achievements"
 * ✅ Clear CTA button "Get Started" with emerald gradient
 * ✅ Responsive layout (mobile: full-width, desktop: two-column)
 * ✅ Perfect dark/light mode styling
 * ✅ Fade-in entrance animation
 */

import Link from 'next/link'

export const metadata = {
  title: 'Premium TODO App - Transform Your Tasks',
  description: 'Beautiful, minimalist task management for professionals',
}

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="max-w-4xl w-full animate-fade-in">
        {/* Main Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          {/* Left: Text Content */}
          <div className="flex flex-col gap-6">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">✓</span>
              </div>
              <span className="text-2xl font-bold text-slate-900 dark:text-slate-50">
                TODO
              </span>
            </div>

            {/* Heading */}
            <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-50 leading-tight">
              Transform Your Tasks Into{' '}
              <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                Achievements
              </span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg text-slate-600 dark:text-slate-300 leading-relaxed">
              Experience a beautifully designed task management app that combines simplicity with power.
              Get started in seconds and focus on what matters.
            </p>

            {/* Features */}
            <ul className="space-y-3 text-slate-600 dark:text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">✓</span>
                <span>Elegant, minimalist design with dark mode</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">✓</span>
                <span>Instant sync with beautiful animations</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">✓</span>
                <span>Smart filtering and organization</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-600 dark:text-emerald-400 font-bold mt-1">✓</span>
                <span>Premium experience, completely free</span>
              </li>
            </ul>

            {/* CTA Button */}
            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <Link
                href="/login"
                className="px-8 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white rounded-lg font-semibold transition-all hover:shadow-lg transform hover:scale-105 text-center"
              >
                Get Started
              </Link>
              <Link
                href="/tasks"
                className="px-8 py-3 border-2 border-emerald-600 dark:border-emerald-400 text-emerald-600 dark:text-emerald-400 rounded-lg font-semibold hover:bg-emerald-50 dark:hover:bg-slate-700 transition-colors text-center"
              >
                View Dashboard
              </Link>
            </div>
          </div>

          {/* Right: Visual Element */}
          <div className="hidden md:flex items-center justify-center">
            <div className="relative w-full h-96">
              {/* Gradient background */}
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-3xl blur-3xl dark:from-emerald-500/10 dark:to-teal-500/10" />

              {/* Card preview */}
              <div className="relative bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 space-y-4">
                {/* Mock task 1 */}
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    className="w-5 h-5 accent-emerald-600 rounded mt-0.5"
                    defaultChecked
                    disabled
                  />
                  <div className="flex-1">
                    <p className="line-through text-slate-400 dark:text-slate-500 font-medium">
                      Design landing page
                    </p>
                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                      Create beautiful hero section
                    </p>
                  </div>
                </div>

                <div className="h-px bg-slate-200 dark:bg-slate-700" />

                {/* Mock task 2 */}
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    className="w-5 h-5 accent-emerald-600 rounded mt-0.5"
                    disabled
                  />
                  <div className="flex-1">
                    <p className="text-slate-900 dark:text-slate-50 font-medium">
                      Implement dark mode
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                      Support system preference detection
                    </p>
                  </div>
                </div>

                <div className="h-px bg-slate-200 dark:bg-slate-700" />

                {/* Mock task 3 */}
                <div className="flex items-start gap-3">
                  <input
                    type="checkbox"
                    className="w-5 h-5 accent-emerald-600 rounded mt-0.5"
                    disabled
                  />
                  <div className="flex-1">
                    <p className="text-slate-900 dark:text-slate-50 font-medium">
                      Add animations
                    </p>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                      Smooth transitions and micro-interactions
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Stats */}
        <div className="mt-20 grid grid-cols-3 gap-8 text-center">
          <div>
            <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">100%</p>
            <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">Responsive Design</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">&lt;300ms</p>
            <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">All Animations</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">A+</p>
            <p className="text-slate-600 dark:text-slate-400 text-sm mt-2">Accessibility</p>
          </div>
        </div>
      </div>
    </div>
  )
}
