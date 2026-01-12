# Frontend Authentication Migration Guide

**Status**: Critical Fix Required
**Date**: 2026-01-09
**Root Cause**: Spec clarification revealed frontend incorrectly calling non-existent backend auth endpoints

## Problem Summary

The frontend is currently trying to call `/auth/signup` and `/auth/login` endpoints on the backend (`http://localhost:8000/auth/signup`), but these endpoints **do not exist** according to the clarified spec.

**Error observed**:
```
POST http://localhost:8000/auth/signup 404 (Not Found)
```

## Root Cause Analysis

**Spec Clarification (2026-01-09)** resolved contradictory statements:

| Statement | Source | Verdict |
|-----------|--------|---------|
| "Frontend calls backend endpoints with credentials and receives JWT token" | Original Better Auth Integration Details (line 186) | ❌ **INCORRECT** - Contradicted later clarifications |
| "Better Auth on frontend only. Frontend (Next.js) uses Better Auth for UI and token generation" | Root Cause Investigation (line 120) | ✅ **CORRECT** - Confirmed in clarification |

**Backend Implementation**: Correct
- ✅ Main.py only registers `/api/tasks` router (line 67)
- ✅ No auth endpoints implemented
- ✅ JWT validation only (dependency: `get_current_user` on task routes)
- ✅ Spec explicitly states: "Backend does NOT implement /api/auth/*"

**Frontend Implementation**: Incorrect
- ❌ Constants define `/auth/login` and `/auth/signup` endpoints (frontend/lib/constants.ts:36-37)
- ❌ Login page calls these endpoints via `apiPost()` (frontend/app/login/page.tsx:86)
- ❌ Should be using Better Auth library directly for signup/login

## How Better Auth Should Work

### Current (Incorrect) Flow:
```
Frontend (login form)
  └─> apiPost('/auth/signup', {email, password})
       └─> HTTP POST to http://localhost:8000/auth/signup
            └─> 404 ❌ (endpoint doesn't exist)
```

### Correct Flow (Per Spec):
```
Frontend (login form)
  └─> Better Auth library (client-side)
       ├─> Handles signup UI
       ├─> Generates JWT with 'sub' claim
       └─> Returns JWT to frontend
            └─> Frontend stores in localStorage
                 └─> Backend validates JWT on API calls
```

## Migration Steps

### Step 1: Install Better Auth Library

```bash
cd frontend
npm install better-auth
# or
yarn add better-auth
# or
pnpm add better-auth
```

### Step 2: Create Better Auth Client Configuration

Create `frontend/lib/auth-client.ts`:

```typescript
import { createAuthClient } from 'better-auth/client'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3000', // Frontend URL, not backend
  // Better Auth will issue JWT tokens automatically
})
```

### Step 3: Update Login Page Component

Replace `frontend/app/login/page.tsx` to use Better Auth instead of backend endpoints:

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authClient } from '@/lib/auth-client'
import { apiAuth } from '@/lib/api'
import { useToast } from '@/lib/hooks/useToast'
import { validateEmail, validatePassword } from '@/lib/utils'
// ... other imports

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

  const validate = (): boolean => {
    // ... existing validation code ...
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!validate()) return

    setIsLoading(true)

    try {
      let result

      if (mode === 'signup') {
        // Use Better Auth signup
        result = await authClient.signUp.email({
          email,
          password,
          name: email.split('@')[0], // Optional: use email prefix as name
        })
      } else {
        // Use Better Auth login
        result = await authClient.signIn.email({
          email,
          password,
        })
      }

      if (result.error) {
        showError(result.error.message || 'Authentication failed')
        setIsLoading(false)
        return
      }

      // Better Auth returns session + token
      if (result.data?.user) {
        // Store JWT token from Better Auth session
        if (result.data.token) {
          apiAuth.setToken(result.data.token)
        }

        showSuccess(
          mode === 'signup'
            ? 'Account created! Redirecting...'
            : 'Logged in successfully!'
        )

        setTimeout(() => {
          router.push('/tasks')
        }, 1000)
      }
    } catch (error) {
      showError('An unexpected error occurred')
      console.error('Auth error:', error)
      setIsLoading(false)
    }
  }

  // ... rest of component (JSX unchanged) ...
}
```

### Step 4: Remove Backend Auth Endpoints from Constants

Update `frontend/lib/constants.ts`:

```typescript
// API Endpoints
export const API_ENDPOINTS = {
  // ❌ REMOVE THESE - Auth is handled by Better Auth library
  // AUTH: {
  //   LOGIN: '/auth/login',
  //   SIGNUP: '/auth/signup',
  //   LOGOUT: '/auth/logout',
  //   REFRESH: '/auth/refresh',
  //   VERIFY: '/auth/verify',
  // },

  // ✅ KEEP THESE - Backend API endpoints
  TASKS: {
    LIST: '/api/tasks',
    CREATE: '/api/tasks',
    GET: (id: string) => `/api/tasks/${id}`,
    UPDATE: (id: string) => `/api/tasks/${id}`,
    DELETE: (id: string) => `/api/tasks/${id}`,
    TOGGLE_COMPLETE: (id: string) => `/api/tasks/${id}/complete`,
  },
  // ... rest unchanged
} as const
```

### Step 5: Update Token Handling in API Client

The token storage is already correct in `frontend/lib/api.ts`:
- ✅ `getToken()` retrieves from localStorage
- ✅ `setToken()` stores in localStorage
- ✅ JWT is attached to all API requests via Authorization header

No changes needed here.

### Step 6: Test the Flow

1. **Start backend**:
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```

2. **Start frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test signup**:
   - Navigate to `http://localhost:3000/login`
   - Click "Sign up"
   - Fill in email and password
   - Should see: Better Auth handles signup (no 404 error)
   - JWT token stored in localStorage

4. **Test task creation** (verify JWT is sent):
   - After login, navigate to `/tasks`
   - Create a task
   - Backend receives JWT in Authorization header: `Authorization: Bearer <token>`
   - Backend extracts `sub` claim for user isolation
   - Task created with correct user_id

5. **Test task isolation**:
   - Open another browser/incognito window
   - Login with different email
   - Create different task
   - First user should NOT see second user's task (404 on cross-user access)

## Key Points

| Aspect | Details |
|--------|---------|
| **Who handles signup/login?** | Better Auth library (frontend-only) |
| **Does backend have auth endpoints?** | No - spec explicitly forbids them |
| **How does backend validate users?** | Extracts `sub` claim from JWT in Authorization header |
| **What does `sub` contain?** | User identifier (string, issued by Better Auth) |
| **Where is JWT stored?** | Frontend localStorage (via `apiAuth.setToken()`) |
| **Which endpoints does backend expose?** | `/api/tasks/*` only (JWT validated on all) |

## Files to Modify

| File | Change | Priority |
|------|--------|----------|
| `frontend/lib/auth-client.ts` | **CREATE** - Better Auth client config | 🔴 Critical |
| `frontend/app/login/page.tsx` | Update to use `authClient` instead of `apiPost` | 🔴 Critical |
| `frontend/lib/constants.ts` | Remove/comment out `AUTH` endpoints | 🟡 Important |
| `frontend/lib/api.ts` | No changes needed (token handling correct) | ✅ OK |
| Backend spec | Already clarified (✅ Complete) | ✅ Done |
| Backend code | No changes needed (correct implementation) | ✅ OK |

## Verification Checklist

After migration:

- [ ] Better Auth library installed in frontend
- [ ] `auth-client.ts` created with Better Auth configuration
- [ ] Login page updated to use `authClient.signUp` and `authClient.signIn`
- [ ] Auth endpoints removed from `API_ENDPOINTS` in constants
- [ ] Frontend signup flow works without 404 errors
- [ ] JWT token stored in localStorage after signup
- [ ] Backend receives JWT in Authorization header on task API calls
- [ ] Backend extracts `sub` claim correctly
- [ ] Task isolation works (user A cannot see user B's tasks)
- [ ] Concurrent users (signup + login) work correctly
- [ ] Tests pass (if applicable)

## Related Documentation

- **Backend Spec**: `specs/003-fastapi-backend/spec.md` (lines 123-192)
- **Clarification Session**: `history/prompts/003-fastapi-backend/24-clarify-frontend-auth-flow.spec.prompt.md`
- **Backend Tests**: `backend/tests/test_auth.py` (currently test non-existent endpoints - should be removed/updated)

## Next Steps

1. ✅ **Clarifications complete** - Spec ambiguity resolved
2. 🔄 **Frontend migration** - Implement Better Auth integration (THIS GUIDE)
3. 🔄 **Integration testing** - Verify signup → task creation → task isolation flow
4. 🔄 **Backend auth tests** - Update/remove tests for non-existent auth endpoints
5. 🔄 **End-to-end testing** - Full user flow across frontend + backend

---

**Questions?** Refer to the Backend Spec or Clarification Session linked above.
