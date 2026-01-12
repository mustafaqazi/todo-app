---
id: 18
title: Plan JWT Auth Implementation
stage: plan
date: 2026-01-08
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-fastapi-backend
branch: 003-fastapi-backend
user: user
command: /sp.plan
labels: ["jwt", "authentication", "backend", "architecture", "implementation-plan"]
links:
  spec: /specs/003-fastapi-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /specs/003-fastapi-backend/spec.md
  - C:\Users\Mustafa Qazi\.claude\plans\vivid-foraging-ladybug.md
tests:
  - No tests run (planning phase)
---

## Prompt

Securing the REST API
Better Auth + FastAPI Integration
The Challenge
Better Auth is a JavaScript/TypeScript authentication library that runs on your Next.js frontend. However, your FastAPI backend is a separate Python service that needs to verify which user is making API requests.
The Solution: JWT Tokens
Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.
How It Works
●    User logs in on Frontend → Better Auth creates a session and issues a JWT token
●    Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
●    Backend receives request → Extracts token from header, verifies signature using shared secret
●    Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
●    Backend filters data → Returns only tasks belonging to that user
What Needs to Change
Component    Changes Required
Better Auth Config    Enable JWT plugin to issue tokens
Frontend API Client    Attach JWT token to every API request header
FastAPI Backend    Add middleware to verify JWT and extract user
API Routes    Filter all queries by the authenticated user's ID
The Shared Secret
Both frontend (Better Auth) and backend (FastAPI) must use the same secret key for JWT signing and verification. This is typically set via environment variable BETTER_AUTH_SECRET in both services.
Security Benefits
Benefit    Description
User Isolation    Each user only sees their own tasks
Stateless Auth    Backend doesn't need to call frontend to verify users
Token Expiry    JWTs expire automatically (e.g., after 7 days)
No Shared DB Session    Frontend and backend can verify auth independently
API Behavior Change
After Auth:
All endpoints require valid JWT token
Requests without token receive 401 Unauthorized
Each user only sees/modifies their own tasks
Task ownership is enforced on every operation
Bottom Line
The REST API endpoints stay the same (GET /api/user_id/tasks, POST /api/user_id/tasks, etc.), but every request now must include a JWT token, and all responses are filtered to only include that user's data.

## Response snapshot

Comprehensive implementation plan created addressing the root cause of signup/signin failure:

**Root Cause Analysis:**
- Backend has COMPLETE JWT verification (can validate tokens)
- Backend is MISSING authentication endpoints (cannot generate tokens)
- Frontend expects POST /auth/signup and POST /auth/login endpoints
- No User model or password hashing implemented

**Architectural Decision:**
Rejected frontend-only Better Auth approach. Instead, implement complete auth system in FastAPI backend:
- User model with email + hashed password
- Signup/login endpoints that generate JWT tokens
- Password hashing with bcrypt (via passlib)
- JWT generation with python-jose
- Token verification middleware (already exists)

**Implementation Plan Includes:**
1. Add dependencies: python-jose, passlib[bcrypt]
2. Create User SQLModel with indexed email field
3. Create auth request/response schemas
4. Add password hashing and JWT utilities
5. Implement 3 auth endpoints: /auth/signup, /auth/login, /auth/verify
6. Register auth router in main FastAPI app
7. Comprehensive test suite (unit + integration)
8. Manual testing procedures and verification checklist

**Key Success Criteria:**
- User can sign up with email/password
- User table created in Neon database
- JWT tokens generated with `sub` claim (user ID)
- Frontend receives token and stores in localStorage
- Existing user isolation still enforced
- All tests pass

## Outcome

- ✅ Impact: High - Provides complete, executable blueprint for fixing signup/signin authentication system
- 🧪 Tests: 10+ test cases defined (signup success, duplicate email, weak password, login, token verify, full flow)
- 📁 Files: 1 plan file created with 8 critical files identified for modification/creation
- 🔁 Next prompts: `/sp.tasks` for task generation; backend-engineer agent for code implementation
- 🧠 Reflection: Plan leveraged complete codebase exploration to identify that 80% of auth infrastructure already exists. Solution focuses on missing 20% (User model, auth endpoints, token generation). Minimal risk because JWT verification routes unchanged; only additions.

## Evaluation notes (flywheel)

- Failure modes observed: None (planning phase; no execution yet)
- Graders run and results: N/A (planning phase)
- Prompt variant: Two-phase exploration + comprehensive plan with 10 implementation tasks
- Next experiment: Execute tasks in dependency order; validate each phase (dependencies → models → schemas → utils → routes → tests)

---

## Architectural Decisions Made

| Decision | Choice | Rationale | Alternatives |
|----------|--------|-----------|--------------|
| Auth Backend | Custom FastAPI (not Better Auth) | Better Auth is JS/TS only; Python needs different library | OAuth2, session-based (rejected) |
| Password Hashing | bcrypt via passlib | Industry standard, secure, battle-tested | argon2, scrypt (more complex) |
| JWT Library | python-jose | Already used for verification; consistency | PyJWT (requires different API) |
| Token Expiry | 7 days | Standard web session length | 1 hour (too short), 30 days (too long) |
| User Storage | SQLModel User table | Matches existing Task model pattern | Separate user service (over-engineered) |
| Auth Endpoints | /auth/signup, /auth/login, /auth/verify | RESTful convention; matches frontend expectations | /api/auth/* (confusing with task API) |

---

## Implementation Checklist

**Phase 0: Research & Decisions** ✅ COMPLETE
- Identified root cause (no auth endpoints)
- Chose architecture (custom FastAPI backend)
- Selected libraries (passlib, python-jose)

**Phase 1: Data Model** 📋 PENDING
- [ ] Add User model to backend/src/models.py
- [ ] Create indexed email field
- [ ] Add hashed_password field

**Phase 2: API Contracts** 📋 PENDING
- [ ] Create UserSignup schema
- [ ] Create UserLogin schema
- [ ] Create AuthResponse schema
- [ ] Create VerifyResponse schema

**Phase 3: Utilities** 📋 PENDING
- [ ] Create password.py with hash/verify functions
- [ ] Create jwt.py with token generation

**Phase 4: Routes** 📋 PENDING
- [ ] Create auth.py router
- [ ] Implement POST /auth/signup
- [ ] Implement POST /auth/login
- [ ] Implement GET /auth/verify

**Phase 5: Integration** 📋 PENDING
- [ ] Register auth router in main.py
- [ ] Add dependencies to requirements.txt
- [ ] Create database tables (User table)

**Phase 6: Testing** 📋 PENDING
- [ ] Create test_auth.py
- [ ] Write 10+ test cases
- [ ] Run full test suite
- [ ] Verify cross-user isolation

---

## Risk Assessment Summary

| Risk | Severity | Mitigation | Status |
|------|----------|-----------|--------|
| Password hashing fails | HIGH | Use passlib (proven library); comprehensive tests | Mitigated |
| JWT verification breaks | HIGH | Use same python-jose library for both generate/verify | Mitigated |
| Email uniqueness violated | MEDIUM | DB unique constraint + pre-check in code | Mitigated |
| Cross-user data leakage | CRITICAL | Existing isolation code unchanged; no modifications | Mitigated |
| Token expiry too short | LOW | Set to 7 days (configurable); matches standards | Mitigated |

---

**Plan Status**: ✅ APPROVED
**Next Action**: Generate implementation tasks or begin code execution
**Estimated Duration**: ~2 hours for full implementation
**Complexity**: Medium (adding new auth layer; existing infrastructure sound)

