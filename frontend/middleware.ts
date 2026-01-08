import { NextRequest, NextResponse } from 'next/server'

/**
 * Middleware for authentication guard
 * Protects /tasks route from unauthenticated users
 * Allows /login and / without auth
 * Handles 401 responses by redirecting to login
 */

const protectedRoutes = ['/tasks']
const publicRoutes = ['/', '/login']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Check if route is protected
  const isProtected = protectedRoutes.some((route) => pathname.startsWith(route))

  if (isProtected) {
    // Check for authentication token
    const token = request.cookies.get('todo_auth_token')?.value ||
                 (typeof window !== 'undefined' && localStorage.getItem('todo_auth_token'))

    // If no token, redirect to login
    if (!token) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('returnUrl', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!api|_next/static|_next/image|favicon.ico|public).*)',
  ],
}
