# Feature Specification: Secure FastAPI Backend with JWT & PostgreSQL

**Feature Branch**: `003-fastapi-backend`  
**Created**: 2026-01-05  
**Status**: Draft  
**Input**: Complete secure, production-ready FastAPI backend for Phase II

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and View Tasks (Priority: P1)

User creates tasks and only they can view their own tasks.

**Why this priority**: Core CRUD and user isolation are foundational.

**Independent Test**: (1) Create task → (2) GET /api/tasks shows it → (3) Other user cannot see it. Delivers: working creation with isolation.

**Acceptance Scenarios**:

1. **Given** authenticated, **When** POST /api/tasks, **Then** returns 201
2. **Given** 3 tasks created, **When** GET /api/tasks, **Then** returns 3
3. **Given** own task ID, **When** GET /api/tasks/{id}, **Then** returns 200
4. **Given** other user's task, **When** GET /api/tasks/{id}, **Then** returns 404
5. **Given** no token, **When** GET /api/tasks, **Then** returns 401

---

### User Story 2 - Update & Complete Tasks (Priority: P1)

Update task and toggle completion. Only owner can modify.

**Why this priority**: Core Phase II requirement.

**Independent Test**: (1) Create → (2) PUT → (3) PATCH → (4) Verify persisted. Delivers: full mutation.

**Acceptance Scenarios**:

1. **Given** owner, **When** PUT /api/tasks/{id}, **Then** returns 200
2. **Given** completed: false, **When** PATCH /api/tasks/{id}/complete, **Then** returns 200 with true
3. **Given** completed: true, **When** PATCH again, **Then** returns 200 with false
4. **Given** not owner, **When** PUT, **Then** returns 404
5. **Given** empty title, **When** PUT, **Then** returns 422

---

### User Story 3 - Delete Tasks (Priority: P1)

Delete only owned tasks.

**Why this priority**: Essential for CRUD lifecycle.

**Independent Test**: (1) Create → (2) DELETE → (3) Verify 404. Delivers: lifecycle control.

**Acceptance Scenarios**:

1. **Given** owner, **When** DELETE /api/tasks/{id}, **Then** returns 204
2. **Given** deleted task, **When** GET /api/tasks/{id}, **Then** returns 404
3. **Given** not owner, **When** DELETE, **Then** returns 404

---

### User Story 4 - Multi-User Isolation (Priority: P1)

Multiple users with complete data isolation.

**Why this priority**: Critical security requirement.

**Independent Test**: (1) Two sessions → (2) Create tasks → (3) Each sees only own → (4) Cross-access 404 → (5) Restart verify. Delivers: proven safety.

**Acceptance Scenarios**:

1. **Given** two authenticated users, **When** create tasks, **Then** each sees only own
2. **Given** A has task 100, B has 200, **When** A accesses /api/tasks/200, **Then** returns 404
3. **Given** A tries to modify B's task, **When** sent, **Then** returns 404
4. **Given** restart, **When** reconnect, **Then** tasks isolated

---

### User Story 5 - Filter Tasks by Status (Priority: P2)

Filter tasks by completion status.

**Why this priority**: Required in API spec.

**Independent Test**: (1) Create mixed → (2) ?status=pending → (3) ?status=completed → (4) ?status=all. Delivers: filtered views.

**Acceptance Scenarios**:

1. **Given** 2 pending + 1 completed, **When** ?status=pending, **Then** returns 2
2. **Given** same, **When** ?status=completed, **Then** returns 1
3. **Given** same, **When** ?status=all, **Then** returns 3

---

### Edge Cases

- Malformed JWT → 401
- Non-existent task → 404
- Title > 200 → 422
- Different secret → 401
- Null description → Accepted
- Concurrent requests (50+) → All succeed, no data loss

## Clarifications

### Session 2026-01-08 (Initial)

- Q: Who is responsible for creating and issuing the JWT token? → A: Better Auth is configured to issue JWT tokens when users log in. These tokens are self-contained and verified by the backend using the secret key.
- Q: Where is the Better Auth server running? → A: Same FastAPI backend. Better Auth is integrated as a library (better-auth Python package) within the FastAPI application. The /api/auth/* endpoints are automatically mounted by Better Auth when configured in main.py. No separate server required.
- Q: How does the signup/login flow work? → A: Better Auth provides frontend-agnostic endpoints at /api/auth/signup and /api/auth/login. Frontend calls these endpoints with email/password, receives JWT token in response. Backend stores user records; JWT is self-contained and stateless. See `Backend Standards (FastAPI + SQLModel)` section and plan.md for implementation details.
- Q: What claim in the Better Auth JWT contains the user identifier? → A: user_id claim (custom claim, not 'sub').
- Q: How should the frontend store the JWT for subsequent API calls? → A: localStorage (persistent).
- Q: What is the specific sign-in failure? → A: Unable to sign in using better-auth (specific error/behavior needs investigation).

### Session 2026-01-08 (Root Cause Investigation)

- Q: Is Better Auth initialized in the backend? → A: **No** - Better Auth is not initialized in the backend yet (missing library integration).
- Q: Is the `better-auth` package installed in backend dependencies? → A: **No** - Package not installed yet; needs to be added to requirements.
- Q: What database is the backend connected to? → A: PostgreSQL (Neon) with `postgresql+asyncpg://...`
- Q: How should Better Auth be integrated? → A: **Better Auth on frontend only**. Frontend (Next.js) uses Better Auth for UI and token generation. Backend (FastAPI) validates JWT tokens using shared secret and stores users in PostgreSQL via SQLModel.
- Q: What JWT claim contains user ID? → A: **`sub` claim** (standard JWT) - Backend extracts `sub` as the user identifier, not custom `user_id` claim. **CORRECTS EARLIER SPEC STATEMENT**.

### Session 2026-01-09 (Frontend Auth Flow Clarification - SUPERSEDED)

- Q: Where does signup/login occur - frontend or backend? → A: **Frontend only**. Frontend (Next.js) uses Better Auth library directly for signup/login UI and token generation. Backend does NOT have `/api/auth/*` endpoints. ~~SUPERSEDED BY SESSION 2026-01-09 DECISION BELOW~~
- Q: How does frontend get JWT token? → A: Frontend calls Better Auth library (not backend). Better Auth handles user registration and login, generates JWT with `sub` claim containing user ID. Frontend stores token in localStorage, then includes it in `Authorization: Bearer <token>` header for all backend API calls. ~~SUPERSEDED BY SESSION 2026-01-09 DECISION BELOW~~

### Session 2026-01-09 (Critical Architectural Decision - Better Auth Backend Integration)

**DECISION**: After user testing revealed that Better Auth's `createAuthClient()` from "better-auth/react" requires backend auth endpoints (`/api/auth/sign-up/email`, `/api/auth/login/email`, etc.), the team decided to **implement full Better Auth backend integration** instead of frontend-only auth.

**Rationale**: Better Auth is designed as a full-stack authentication solution. The JavaScript client automatically attempts to call backend endpoints. Removing these endpoints causes 404 errors. Option A was chosen to leverage Better Auth's complete feature set.

**Updated Auth Architecture**:
- Q: Will the backend implement auth endpoints? → A: **YES** - Backend will implement complete Better Auth integration with `/api/auth/*` endpoints
- Q: How will Better Auth be integrated on the backend? → A: Install `better-auth` Python package on FastAPI. Configure Better Auth middleware/routes. Frontend calls `/api/auth/signup`, `/api/auth/login` endpoints directly.
- Q: Will users be stored in the backend database? → A: **YES** - Better Auth will manage user records in PostgreSQL via SQLModel (users table with email, hashed_password, etc.)
- Q: How will frontend get JWT tokens? → A: Frontend calls `/api/auth/signup` or `/api/auth/login` endpoints. Backend returns JWT token with `sub` claim. Frontend stores token in localStorage.
- Q: Will JWT validation change? → A: No - Backend still validates JWT using BETTER_AUTH_SECRET (HS256) and extracts `sub` claim. User isolation still enforced.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Validate JWT using BETTER_AUTH_SECRET (HS256)
- **FR-002**: Extract `sub` claim (standard JWT claim from Better Auth), reject invalid with 401
- **FR-003**: Create with required title (1-200), optional description
- **FR-004**: GET /api/tasks returns user's tasks, 200
- **FR-005**: Support ?status=all|pending|completed filtering:
  - Default (no ?status param): Returns all tasks (equivalent to ?status=all)
  - ?status=pending: Returns tasks where completed=false
  - ?status=completed: Returns tasks where completed=true
  - ?status=all: Returns all tasks (explicit)
  - Invalid status value (e.g., ?status=archive): Returns 400 Bad Request with message "Invalid status filter: must be 'pending', 'completed', or 'all'"
- **FR-006**: GET /api/tasks/{id} returns 404 if not owned
- **FR-007**: PUT /api/tasks/{id} updates with validation
- **FR-008**: PATCH /api/tasks/{id}/complete toggles
- **FR-009**: DELETE /api/tasks/{id} returns 204 or 404
- **FR-010**: Enforce user_id == current_user_id on all queries
- **FR-011**: Persist in Neon PostgreSQL, survive restarts
- **FR-012**: Auto-manage created_at and updated_at
- **FR-013**: Return 201, 200, 204, 400, 401, 404, 422
- **FR-014**: Clear JSON error messages
- **FR-015**: No user/account endpoints
- **FR-016**: No file uploads, email, WebSocket, pagination

### Key Entities

- **Task**: id (PK), user_id (indexed, max 255 chars), title (1-200), description (optional), completed (bool), created_at, updated_at
  - user_id: VARCHAR(255) NOT NULL, format: alphanumeric + hyphens (e.g., "user_abc123def456"), extracted from JWT `sub` claim
- **User**: Managed by Better Auth on frontend; backend uses JWT `sub` claim (standard JWT), stored as string in token payload

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: JWT validation < 10ms p95 per request (cold connection pool)
- **SC-002**: User A cannot view/modify/delete User B's tasks (404 isolation verified)
- **SC-003**: Create task < 200ms p95, retrieve < 100ms p95 (includes database operations)
- **SC-004**: All endpoints return correct codes matching /lib/api.ts
- **SC-005**: Validates JWT tokens from Better Auth frontend with correct `sub` claim extraction for user isolation
- **SC-006**: Concurrent users (50+) without data loss or cross-user leakage; all creates/updates/deletes succeed
- **SC-007**: Tasks persist across application restarts
- **SC-008**: Swagger fully functional with all 6 endpoints documented
- **SC-009**: Correct error codes (422, 401, 404) with clear JSON messages
- **SC-010**: Production-ready, Phase 3 compatible

### Assumptions

- Better Auth is integrated on BOTH frontend (Next.js) and backend (FastAPI with `better-auth` Python package)
- Backend implements `/api/auth/*` endpoints for signup, login, and token generation
- Better Auth issues self-contained JWT tokens with `sub` claim (standard JWT)
- JWT is generated by backend auth endpoints, signed with BETTER_AUTH_SECRET (HS256)
- Frontend stores JWT in localStorage for persistence and includes in Authorization header
- Frontend sends JWT in Authorization header: `Authorization: Bearer <token>`
- Users are stored in PostgreSQL database managed by Better Auth backend
- Neon PostgreSQL stable
- `sub` claim (user identifier from JWT) is a non-empty string
- BETTER_AUTH_SECRET environment variable is shared between frontend client config and backend JWT verification

### Better Auth Integration Details

- **Auth Endpoints**: Backend implements complete Better Auth integration with `/api/auth/*` endpoints. Frontend's Better Auth library client calls these endpoints directly for signup/login. Backend has `/api/auth/sign-up/email`, `/api/auth/login/email`, and related endpoints.
- **JWT Generation**: Backend's Better Auth integration generates JWT tokens with `sub` claim containing user identifier. JWT is signed with BETTER_AUTH_SECRET (HS256).
- **JWT Validation**: Backend validates JWT signature using BETTER_AUTH_SECRET (HS256) before processing task API requests. Backend extracts `sub` claim for user isolation.
- **Token Claim**: JWT payload contains standard `sub` claim (NOT custom `user_id`), which backend extracts to enforce user isolation and filter tasks by user.
- **Token Expiration**: Token validity and expiration handled by Better Auth backend; backend returns 401 on expired/invalid tokens during task operations.
- **User Records**: Better Auth backend manages user storage in PostgreSQL. Backend stores user records with email, hashed password, and other auth metadata. Task isolation enforced via extracted `sub` from JWT.
- **Backend Auth Endpoints**: Backend DOES implement `/api/auth/*` endpoints with full Better Auth integration. Frontend's Better Auth client calls these endpoints directly for signup/login/logout operations.

## Acceptance Checklist

- [ ] Backend runs: uvicorn main:app --reload --port 8000
- [ ] Swagger lists all 6 endpoints
- [ ] Frontend includes JWT in header
- [ ] User A sees own tasks; User B cannot
- [ ] All CRUD return correct codes
- [ ] Data matches /lib/api.ts
- [ ] Database filters by user_id
- [ ] Restart preserves tasks
- [ ] Invalid JWT→401, bad title→422, wrong user→404
- [ ] No HTML/SQL/exceptions in responses
