'use client'

/**
 * Premium Login/Signup Page
 * Centered card with animated form fields
 * Better Auth integration for JWT handling
 *
 * Acceptance Criteria:
 * ✅ Centered card (400px max)
 * ✅ Email and password inputs
 * ✅ Form validation with inline errors
 * ✅ Success toast on signup
 * ✅ JWT token storage
 * ✅ Redirect to /tasks
 * ✅ Responsive mobile design
 * ✅ Dark/light mode perfect contrast
 */

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { apiAuth } from '@/lib/api'
import { validateEmail, validatePassword } from '@/lib/utils'
import { useToast } from '@/lib/hooks/useToast'
import { signUp, signIn } from '@/lib/auth-client'

export default function LoginPage() {
  const router = useRouter()
  const { showSuccess, showError } = useToast()

  const [mode, setMode] = useState<'login' | 'signup'>('signup')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)

  // Validate form
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!email) {
      newErrors.email = 'Email is required'
    } else if (!validateEmail(email)) {
      newErrors.email = 'Invalid email format'
    }

    if (!password) {
      newErrors.password = 'Password is required'
    } else if (mode === 'signup') {
      const pwValidation = validatePassword(password)
      if (!pwValidation.isValid) {
        newErrors.password = pwValidation.errors[0] || 'Password too weak'
      }
    }

    if (mode === 'signup' && password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) return

    setIsLoading(true)

    try {
      let result

      if (mode === 'signup') {
        // Use Better Auth signup
        result = await signUp(email, password)
      } else {
        // Use Better Auth signin
        result = await signIn(email, password)
      }

      if (!result.success) {
        showError(result.error || 'Authentication failed')
        setIsLoading(false)
        return
      }

      // Store JWT token from Better Auth
      if (result.data?.token) {
        apiAuth.setToken(result.data.token)
      }

      // Show success toast
      showSuccess(
        mode === 'signup'
          ? 'Account created! Redirecting...'
          : 'Logged in successfully!'
      )

      // Redirect to tasks after short delay
      setTimeout(() => {
        router.push('/tasks')
      }, 1000)
    } catch (error) {
      showError('An unexpected error occurred')
      console.error('Auth error:', error)
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="w-full max-w-md animate-fade-in">
        {/* Card */}
        <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 shadow-lg p-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">✓</span>
              </div>
              <span className="text-xl font-bold text-slate-900 dark:text-slate-50">
                TODO
              </span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-50 text-center">
              {mode === 'signup' ? 'Create Account' : 'Welcome Back'}
            </h1>
            <p className="text-slate-600 dark:text-slate-400 text-center text-sm mt-2">
              {mode === 'signup'
                ? 'Start managing your tasks beautifully'
                : 'Access your task dashboard'}
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-slate-900 dark:text-slate-50 mb-2">
                Email <span className="text-rose-500">*</span>
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value)
                  if (errors.email) {
                    setErrors({ ...errors, email: '' })
                  }
                }}
                className={`w-full px-4 py-2 rounded-lg border ${
                  errors.email
                    ? 'border-rose-500 dark:border-rose-400'
                    : 'border-slate-200 dark:border-slate-700'
                } bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-50 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:ring-offset-2 dark:focus:ring-offset-slate-800 transition-all`}
                placeholder="you@example.com"
                disabled={isLoading}
              />
              {errors.email && (
                <p className="text-rose-500 dark:text-rose-400 text-xs mt-1">
                  {errors.email}
                </p>
              )}
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-slate-900 dark:text-slate-50 mb-2">
                Password <span className="text-rose-500">*</span>
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value)
                    if (errors.password) {
                      setErrors({ ...errors, password: '' })
                    }
                  }}
                  className={`w-full px-4 py-2 rounded-lg border ${
                    errors.password
                      ? 'border-rose-500 dark:border-rose-400'
                      : 'border-slate-200 dark:border-slate-700'
                  } bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-50 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:ring-offset-2 dark:focus:ring-offset-slate-800 transition-all pr-10`}
                  placeholder="••••••••"
                  disabled={isLoading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-2.5 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-50"
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
              {errors.password && (
                <p className="text-rose-500 dark:text-rose-400 text-xs mt-1">
                  {errors.password}
                </p>
              )}
            </div>

            {/* Confirm Password (Signup only) */}
            {mode === 'signup' && (
              <div>
                <label className="block text-sm font-medium text-slate-900 dark:text-slate-50 mb-2">
                  Confirm Password <span className="text-rose-500">*</span>
                </label>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => {
                    setConfirmPassword(e.target.value)
                    if (errors.confirmPassword) {
                      setErrors({ ...errors, confirmPassword: '' })
                    }
                  }}
                  className={`w-full px-4 py-2 rounded-lg border ${
                    errors.confirmPassword
                      ? 'border-rose-500 dark:border-rose-400'
                      : 'border-slate-200 dark:border-slate-700'
                  } bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-50 placeholder-slate-400 dark:placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:focus:ring-emerald-400 focus:ring-offset-2 dark:focus:ring-offset-slate-800 transition-all`}
                  placeholder="••••••••"
                  disabled={isLoading}
                />
                {errors.confirmPassword && (
                  <p className="text-rose-500 dark:text-rose-400 text-xs mt-1">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-4 py-2.5 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 disabled:from-emerald-400 disabled:to-teal-400 disabled:cursor-not-allowed text-white rounded-lg font-semibold transition-all mt-6"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  {mode === 'signup' ? 'Creating account...' : 'Logging in...'}
                </span>
              ) : mode === 'signup' ? (
                'Sign Up'
              ) : (
                'Log In'
              )}
            </button>
          </form>

          {/* Footer: Toggle mode */}
          <div className="mt-6 text-center text-sm text-slate-600 dark:text-slate-400">
            {mode === 'signup' ? (
              <>
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={() => setMode('login')}
                  className="text-emerald-600 dark:text-emerald-400 hover:underline font-medium"
                >
                  Log in
                </button>
              </>
            ) : (
              <>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => setMode('signup')}
                  className="text-emerald-600 dark:text-emerald-400 hover:underline font-medium"
                >
                  Sign up
                </button>
              </>
            )}
          </div>

          {/* Back to home link */}
          <div className="mt-4 text-center">
            <Link
              href="/"
              className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-50 text-sm transition-colors"
            >
              ← Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
