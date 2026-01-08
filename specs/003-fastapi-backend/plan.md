# Implementation Plan: Secure FastAPI Backend with JWT & PostgreSQL

**Branch**: `003-fastapi-backend` | **Date**: 2026-01-08 | **Spec**: `/specs/003-fastapi-backend/spec.md`
**Input**: Feature specification from `/specs/003-fastapi-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a production-ready FastAPI backend with JWT authentication (Better Auth), SQLModel ORM, Neon PostgreSQL, and strict user isolation. Design middleware for JWT validation, data models for task persistence, and comprehensive API contracts with security-focused error handling. All endpoints require valid JWT tokens with user_id claim extraction; backend filters all queries by user_id to enforce data isolation.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (latest), SQLModel (ORM), Pydantic v2, PyJWT (JWT validation), python-dotenv
**Storage**: Neon Serverless PostgreSQL (async connection via asyncpg)
**Testing**: pytest with async support, pytest-httpx (HTTP mocking)
**Target Platform**: Linux/Cloud (Docker-ready)
**Project Type**: Web backend (FastAPI) + frontend (Next.js)
**Performance Goals**:
  - JWT validation < 10ms p95 per request
  - Task CRUD operations < 100-200ms p95
  - Support 50+ concurrent users without data loss
**Constraints**:
  - Strict user isolation: user_id must be present in JWT user_id claim
  - All database queries filtered by user_id
  - No cross-user data leakage (401/404 for unauthorized access)
  - No session storage; stateless JWT validation
**Scale/Scope**:
  - Phase II: Multi-user task management (core CRUD)
  - 6 API endpoints (list, create, get, update, toggle, delete)
  - Task table with user_id indexing
  - No pagination initially; simple filtering by status

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development (Non-Negotiable)
✅ **PASS**: Specification exists at `/specs/003-fastapi-backend/spec.md` with user stories, acceptance criteria, and functional requirements. All code will be generated from this spec via /sp.implement.

### Strict User Isolation (Security-Critical)
⚠️ **CONDITIONAL PASS**: Spec requires user_id extraction from JWT user_id claim and filtering all queries by user_id. Implementation must:
  - Verify JWT contains user_id claim
  - Inject user_id into every route handler via dependency injection
  - Filter all database queries by user_id
  - Return 401 for missing token, 404 for non-owned resources
  - Cross-user access tests mandatory

### JWT-Based Stateless Auth
✅ **PASS**: Constitution specifies `Authorization: Bearer <token>` header with `BETTER_AUTH_SECRET` verification. No session storage. User_id extraction from user_id claim (clarified in spec).

### Technology Stack Fidelity
✅ **PASS**: Stack adheres to constitution:
  - Python 3.11+ with FastAPI ✓
  - SQLModel ORM ✓
  - PostgreSQL (Neon) ✓
  - No additional external dependencies ✓

### Modular Architecture & Monorepo
✅ **PASS**: Backend in `/backend/`, specs in `/specs/003-fastapi-backend/`, history in `/history/prompts/` and `/history/adr/`.

### Testability & Quality Gates
⚠️ **CONDITIONAL PASS**: Integration tests must cover:
  - JWT validation (valid, invalid, expired tokens)
  - User isolation (cross-user 404 scenarios)
  - All CRUD operations with correct status codes
  - Concurrent requests (50+ users)

### API Design Standards
✅ **PASS**: RESTful `/api/tasks` endpoints match constitution:
  - GET, POST, PUT, PATCH, DELETE with correct codes
  - Query parameters for filtering (?status=pending)
  - JSON-only responses
  - No user_id in URL path

### Database Design & Normalization
⚠️ **CONDITIONAL PASS**: Schema must match constitution:
  - Task table: id, user_id (indexed), title, description, completed, created_at, updated_at
  - Foreign key on user_id (Better Auth user table)
  - Compound indexes on (user_id, created_at) and (user_id, completed)
  - No NULL titles, default completed=false

### Code Quality & Simplicity
✅ **PASS**: Minimal viable code, no premature abstractions, type hints on all functions, comments only for non-obvious logic.

### Traceability & Documentation
✅ **PASS**: PHR created for this planning session; ADR will be created for JWT architecture decisions post-plan.

---

**GATE RESULT**: ✅ **PASS WITH CONDITIONS** — All critical paths align with constitution. Conditions are implementation details (user_id injection, query filtering, test coverage) that will be verified during code generation.

## Project Structure

### Documentation (this feature)

```text
specs/003-fastapi-backend/
├── spec.md              # Feature specification (existing, clarified)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output: OpenAPI/JSON schemas (to be created)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Backend (FastAPI)**:
```text
backend/
├── main.py              # FastAPI app, CORS, middleware, routes
├── db.py                # PostgreSQL connection, session management, async setup
├── models.py            # SQLModel tables (Task, User reference)
├── schemas.py           # Pydantic request/response schemas
├── dependencies/
│   └── auth.py          # JWT verification, current_user injection
├── routes/
│   └── tasks.py         # Task CRUD endpoints (/api/tasks/*)
├── tests/
│   ├── test_auth.py     # JWT validation, 401/403 scenarios
│   ├── test_tasks.py    # CRUD operations, user isolation
│   └── test_integration.py  # Full flows, concurrent requests
├── pyproject.toml       # UV dependencies (FastAPI, SQLModel, PyJWT, etc.)
├── .env.example         # Template (BETTER_AUTH_SECRET, DATABASE_URL, etc.)
├── .env                 # Local secrets (not in git)
└── Dockerfile           # Production-ready (future)
```

**Frontend (Next.js 16+)** - Already exists, references backend `/api/tasks`:
```text
frontend/
├── app/
│   ├── (auth)/          # Better Auth signup/login pages
│   ├── (app)/
│   │   └── tasks/       # Task CRUD pages
│   └── layout.tsx       # Root layout with auth guard
├── lib/
│   ├── api.ts           # JWT-authenticated API client
│   ├── auth.ts          # Better Auth client config
│   └── types.ts         # TypeScript types
└── components/          # shadcn/ui components
```

**History & Governance**:
```text
history/
├── prompts/
│   ├── constitution/    # Constitution amendments
│   ├── 003-fastapi-backend/  # Feature-specific PHRs
│   │   ├── 12-clarify-better-auth-integration.spec.prompt.md
│   │   ├── 13-plan-jwt-auth-middleware.plan.prompt.md (this session)
│   │   └── ...
│   └── general/         # Cross-feature discussions
└── adr/                 # Architecture Decision Records (to be created)
```

**Structure Decision**: Web application structure (Option 2) with separate backend (FastAPI) and frontend (Next.js). Backend will be in `/backend/` with clear separation of concerns: models, schemas, dependencies (auth), routes (CRUD). Tests co-located in `/backend/tests/`. Frontend already in `/frontend/` with API client configured in `/lib/api.ts` for JWT attachment.

## Complexity Tracking

> No violations with unjustified complexity. Stack is minimal and aligned with constitution.

---

## Phase 0: Research & Design Validation

### Unknowns to Resolve

None identified. Technical context is fully specified:
- ✅ JWT library: PyJWT (standard library for HS256)
- ✅ ORM: SQLModel (specified in constitution)
- ✅ Database: Neon PostgreSQL (serverless, async via asyncpg)
- ✅ Testing: pytest with async support
- ✅ API structure: FastAPI with dependency injection
- ✅ Auth flow: Better Auth on frontend → JWT to backend
- ✅ User_id claim: Clarified in spec as custom claim (not sub)

### Research Output

**research.md** (to be created):
- JWT validation patterns in FastAPI (PyJWT + dependency injection)
- SQLModel async setup with Neon PostgreSQL
- User isolation query filtering best practices
- Error response standards for 401/403/404
- Concurrent request handling in FastAPI
- Integration test patterns for auth-protected endpoints

---

## Phase 1: Design & Contracts

### 1.1 Data Model (Task Entity)

**Output**: `data-model.md`

Entity: **Task**
- **Fields**:
  - `id` (int, primary key, auto-increment)
  - `user_id` (str, indexed, required) — extracted from JWT user_id claim
  - `title` (str, 1-200 chars, required)
  - `description` (str, optional)
  - `completed` (bool, default=false)
  - `created_at` (datetime, immutable, UTC)
  - `updated_at` (datetime, updated on insert/update, UTC)
- **Relationships**:
  - Foreign key: user_id → Better Auth user table (reference only, no enforcement in schema)
- **Indexes**:
  - Primary: id
  - Unique: none
  - Compound: (user_id, created_at), (user_id, completed)
- **Constraints**:
  - title NOT NULL, length > 0 and <= 200
  - user_id NOT NULL, non-empty string
  - completed NOT NULL, defaults to false
- **Lifecycle**:
  - Create: user_id injected from JWT, created_at set to now, completed=false
  - Read: Filtered by user_id in all queries
  - Update: user_id immutable, updated_at set to now
  - Delete: Full row removal (no soft deletes)

### 1.2 API Contracts

**Output**: `contracts/openapi.json` (OpenAPI 3.0 schema)

**Endpoints** (all require `Authorization: Bearer <token>` header):

| Method | Path | Description | Status | Request Body | Response |
|--------|------|-------------|--------|--------------|----------|
| GET | /api/tasks | List user's tasks | 200 | (query params: ?status=all\|pending\|completed) | Task[] |
| POST | /api/tasks | Create task | 201/422 | {title, description?} | Task |
| GET | /api/tasks/{id} | Get task | 200/404 | none | Task |
| PUT | /api/tasks/{id} | Update task | 200/404/422 | {title, description?} | Task |
| PATCH | /api/tasks/{id}/complete | Toggle completion | 200/404 | none | Task |
| DELETE | /api/tasks/{id} | Delete task | 204/404 | none | (empty body) |

**Error Responses**:
- **401 Unauthorized**: Missing/invalid/expired JWT
  ```json
  {"detail": "Invalid authentication credentials"}
  ```
- **403 Forbidden**: Valid token but insufficient permissions (reserved for future)
- **404 Not Found**: Task not owned by user or doesn't exist
  ```json
  {"detail": "Task not found"}
  ```
- **422 Unprocessable Entity**: Validation error (title, length)
  ```json
  {"detail": [{"loc": ["body", "title"], "msg": "string too long"}]}
  ```

**Request/Response Schemas**:

**Create Task** (POST /api/tasks):
```json
Request: {
  "title": "string (required, 1-200)",
  "description": "string (optional)"
}
Response (201): {
  "id": 42,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T10:30:00Z",
  "updated_at": "2026-01-08T10:30:00Z"
}
```

**List Tasks** (GET /api/tasks?status=pending):
```json
Response (200): [
  {
    "id": 42,
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-08T10:30:00Z",
    "updated_at": "2026-01-08T10:30:00Z"
  }
]
```

**Update Task** (PUT /api/tasks/{id}):
```json
Request: {
  "title": "string (required, 1-200)",
  "description": "string (optional)"
}
Response (200): { task object }
```

**Toggle Completion** (PATCH /api/tasks/{id}/complete):
```json
Response (200): { task object with completed toggled }
```

### 1.3 Quickstart Guide

**Output**: `quickstart.md`

- Environment setup (BETTER_AUTH_SECRET, DATABASE_URL)
- Database migrations (SQLModel create_all)
- Running the server (uvicorn main:app --reload --port 8000)
- Testing endpoints via curl with JWT
- Common errors and troubleshooting

### 1.4 Agent Context Update

After Phase 1 design, update agent-specific context files:
- `.claude/agents/backend-engineer.md` with FastAPI patterns
- Technology stack confirmation: FastAPI, SQLModel, PyJWT, asyncpg

---

## Phase 2: Tasks (NOT created by /sp.plan)

**Next Command**: `/sp.tasks` will break Phase 1 design into actionable, dependency-ordered tasks:
1. Set up FastAPI + SQLModel project structure
2. Implement JWT verification middleware
3. Create Task model and Pydantic schemas
4. Implement task routes (CRUD)
5. Write unit and integration tests
6. Add Swagger/OpenAPI documentation
7. Environment configuration and secrets management

---

## Decision Log

### JWT Claim Extraction Strategy

**Decision**: Extract `user_id` claim from JWT (custom claim, not standard `sub`)
**Rationale**: Better Auth JWT structure uses `user_id` claim; spec clarified this in session 2026-01-08
**Alternatives Considered**:
- Use `sub` (standard JWT claim) — Rejected because Better Auth uses `user_id`
- Extract from custom headers — Rejected because JWT is self-contained; no need for headers

**Implementation**: FastAPI dependency in `dependencies/auth.py` will verify JWT signature using `BETTER_AUTH_SECRET`, then extract `user_id` from payload. All route handlers receive `current_user` dict with `{"user_id": "..."}`.

### User Isolation at Database Layer

**Decision**: Filter all queries by user_id at the ORM level, not in application logic
**Rationale**: Database-level filtering is more secure and prevents accidental data leaks
**Alternatives Considered**:
- Application-level filtering only — Rejected because prone to logic errors; database filtering is defense-in-depth

**Implementation**: All `db.query(Task).filter(Task.user_id == current_user["user_id"])` patterns will be consistent across routes. Repository pattern deferred (YAGNI) unless multiple similar queries emerge.

### PostgreSQL Connection Strategy

**Decision**: Use asyncpg with SQLModel for async database operations
**Rationale**: FastAPI is async-first; blocking database calls negate performance gains. Neon PostgreSQL supports async pooling via asyncpg.
**Alternatives Considered**:
- Synchronous SQLAlchemy — Rejected due to blocking I/O in async context
- Connection pooling library (e.g., pgbouncer) — Deferred; Neon's serverless pooling sufficient for Phase II

**Implementation**: `db.py` will create async session factory using SQLModel's async engine with asyncpg driver. Middleware injects session into context.

---
