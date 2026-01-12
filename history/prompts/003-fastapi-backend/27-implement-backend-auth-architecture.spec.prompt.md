---
id: 27
title: Implement backend auth architecture - Better Auth full-stack
stage: spec
date: 2026-01-09
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-fastapi-backend
branch: 003-fastapi-backend
user: user
command: Architectural decision - implement backend auth endpoints
labels: ["authentication", "architecture", "better-auth", "full-stack", "critical-decision"]
links:
  spec: specs/003-fastapi-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-fastapi-backend/spec.md
tests:
  - Better Auth backend endpoints registered
  - Signup endpoint returns JWT with 'sub' claim
  - Login endpoint returns JWT with 'sub' claim
  - Token validation still works for task endpoints
  - User isolation maintained
---

## Prompt

User discovered critical architectural issue during testing and chose to implement full Backend Auth with Better Auth integration (Option A).

## Critical Discovery

While testing frontend authentication, logs revealed: `POST /api/auth/sign-up/email 404`

Investigation found: Better Auth's JavaScript client (`createAuthClient` from "better-auth/react") automatically makes API calls to backend auth endpoints like `/api/auth/sign-up/email` and `/api/auth/login/email`. These endpoints did NOT exist per the earlier specification.

This revealed a fundamental constraint: Better Auth is designed as a full-stack authentication solution and CANNOT work with backend auth endpoints removed.

## Architectural Decision: Option A Selected

**User Choice**: Implement Backend Auth with Better Auth integration

**Reasoning**: Better Auth is a full-stack solution that requires backend endpoints to function properly.

**Decision Details**:
- Install `better-auth` Python package on FastAPI backend
- Implement complete Better Auth backend integration
- Register `/api/auth/*` endpoints in backend
- Generate JWT tokens on backend (not frontend)
- JWT tokens still use 'sub' claim for user isolation
- Backend continues to validate JWT with BETTER_AUTH_SECRET
- Users stored in PostgreSQL via Better Auth backend

## Response Summary

Spec updated to reflect new architecture:

1. **Clarifications Section** - Added Session 2026-01-09 (Critical Architectural Decision):
   - Marked previous "frontend-only" sessions as SUPERSEDED
   - Documented discovery of Better Auth's full-stack requirement
   - Added Q&A explaining backend auth endpoint implementation

2. **Assumptions Section** - Updated to reflect backend integration:
   - Changed: "Better Auth on frontend only" → "Better Auth on BOTH frontend and backend"
   - Added: Backend implements `/api/auth/*` endpoints
   - Added: Users stored in PostgreSQL via Better Auth backend
   - Added: BETTER_AUTH_SECRET shared between frontend and backend

3. **Better Auth Integration Details** - Updated to describe backend-centric approach:
   - Changed: Backend DOES implement `/api/auth/*` endpoints
   - Changed: Backend generates JWT tokens (not frontend)
   - Updated: Backend manages user storage in PostgreSQL
   - Clarified: JWT generation and validation flow

## Key Architectural Implications

### What Changed
- Better Auth now runs on BOTH frontend and backend (full-stack)
- Backend generates and signs JWT tokens
- Frontend calls backend auth endpoints instead of generating tokens locally
- User records stored in PostgreSQL (managed by Better Auth backend)

### What Stays the Same
- JWT tokens contain 'sub' claim for user ID
- Backend validates JWT with BETTER_AUTH_SECRET
- User isolation enforced via 'sub' claim extraction
- Task endpoints remain unchanged (`/api/tasks/*`)
- CORS configuration unchanged

### Why This Matters
- Resolves 404 errors on auth endpoints
- Better Auth works as designed (full-stack)
- Users properly persisted in database
- Clear separation: frontend UI, backend auth+API
- Production-ready authentication flow

## Outcome

✅ **Status**: Spec updated with architectural decision recorded

✅ **Architecture Clarified**: Better Auth full-stack integration documented

✅ **Ready for Implementation**: Backend auth endpoints can now be implemented per Option A

## Next Steps

1. Install `better-auth` Python package in backend
2. Integrate Better Auth backend with FastAPI
3. Register auth routes in `backend/main.py`
4. Update user model in SQLModel if needed
5. Test complete auth flow: signup → login → task creation → isolation
6. Update frontend to call backend auth endpoints (already mostly done)
7. Create comprehensive test cases for auth flow

## Files Modified

- `specs/003-fastapi-backend/spec.md` - Updated Clarifications, Assumptions, and Better Auth Integration Details sections

## Related PHRs

- PHR #24: Clarification of frontend auth flow ambiguity
- PHR #25: Frontend auth migration implementation
- PHR #26: Auth flow testing and issue discovery

---

**Status**: ✅ Architectural decision documented and spec updated
**Next Stage**: Green (implementation) - Backend auth endpoints
**Blocker Resolution**: Identified and resolved - Better Auth full-stack integration now clear

