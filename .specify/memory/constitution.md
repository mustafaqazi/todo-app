# Phase II Todo Full-Stack Web Application Constitution

> **Purpose**: Establish non-negotiable principles and standards for Phase II development: transforming a Phase I console TODO app into a persistent, multi-user web application with proper authentication, data isolation, and spec-driven architecture.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code is generated from specifications, never written manually. Specifications are the source of truth. Every feature, API endpoint, database table, and UI component must have a dedicated spec file before implementation begins.

**Non-negotiable rules**:
- Every feature/API/database/UI change requires a spec in `/specs/`
- No code generation without approved specification
- Specs are written before any implementation (TDD applies to specs too)
- All work is traceable: specification → plan → tasks → implementation → tests
- Hackathon judges review spec history as proof of systematic development

### II. Strict User Isolation (Security-Critical)

Each user sees and modifies ONLY their own tasks. No data leakage, no cross-user access.

**Non-negotiable rules**:
- Every database query MUST filter by `user_id` from authenticated JWT token
- No endpoint may return or modify another user's data
- All API responses filtered before transmission
- Tests MUST include cross-user attack scenarios
- Violation is a critical security breach; must be caught and fixed immediately

### III. JWT-Based Stateless Authentication

Authentication via JWT tokens with shared `BETTER_AUTH_SECRET` environment variable. No session storage; verification at every request.

**Non-negotiable rules**:
- All API endpoints require `Authorization: Bearer <token>` header
- Backend extracts `user_id` from JWT and uses for all query filtering
- Frontend attaches JWT automatically via centralized API client (`/lib/api.ts`)
- 401 Unauthorized for missing/invalid/expired tokens
- Better Auth manages user table; backend does NOT manage users
- Shared secret identical on frontend and backend

### IV. Technology Stack Fidelity (No Deviations)

Stack is fixed and non-negotiable. Adding dependencies requires explicit constitutional amendment.

**Frontend**:
- Next.js 16+ (App Router only, no Pages Router)
- TypeScript (strict mode)
- Tailwind CSS + shadcn/ui
- Better Auth (for JWT support)

**Backend**:
- Python FastAPI (latest)
- SQLModel (ORM)
- Neon Serverless PostgreSQL

**Package Management**:
- Backend: UV
- Frontend: npm/pnpm

**No additional external dependencies for Phase II beyond the above.**

### V. Modular Architecture & Monorepo Structure

Single repository with organized subdirectories ensures scalability and clarity.

**Structure**:
- `/specs/` — All specifications (overview, architecture, features, api, database, ui)
- `/frontend/` — Next.js application with CLAUDE.md guidance
- `/backend/` — FastAPI application with CLAUDE.md guidance
- `/agents/` and `/skills/` — Reserved for Phase 3 (AI agents and skills)
- `/.specify/` — Spec-Kit Plus templates, scripts, and memory
- `/history/prompts/` — Prompt History Records (PHR)
- `/history/adr/` — Architecture Decision Records (ADR)

### VI. Testability & Quality Gates

All code must be testable and tested. Integration tests verify full flows including authentication and user isolation.

**Non-negotiable rules**:
- Backend: Unit tests for models and routes; integration tests for API contracts
- Frontend: Component tests; end-to-end tests for auth flows and task CRUD
- Cross-user security tests: Attempt to access another user's tasks; must fail with 401/403
- No code merge without passing tests
- Code coverage expectations: Backend routes ≥80%, frontend components ≥70%

### VII. API Design Standards

RESTful API with consistent contracts, clear error taxonomy, and JSON-only payloads.

**Non-negotiable rules**:
- Base path: `/api/tasks` (no `{user_id}` in URL; derived from JWT)
- Standard HTTP methods: GET (read), POST (create), PUT (update), PATCH (partial), DELETE (remove)
- All responses in JSON; no HTML
- Status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error
- Request/response schemas documented and validated
- Query parameters for filtering/sorting (e.g., `?status=pending&sort=created_at`)

### VIII. Database Design & Normalization

Proper schema design with indexes, constraints, and relationships for performance and correctness.

**Non-negotiable rules**:
- `tasks` table: `id`, `user_id` (indexed, foreign key), `title`, `description`, `completed`, `created_at`, `updated_at`
- Foreign key constraints: `user_id` references Better Auth user table
- Indexes on: `user_id`, `created_at`, `completed` (compound indexes for common filters)
- Timestamps: `created_at` (immutable), `updated_at` (on insert and update)
- No NULL titles; default `completed=false`

### IX. Code Quality & Simplicity (YAGNI)

Keep solutions simple, focused, and maintainable. Avoid over-engineering.

**Non-negotiable rules**:
- Minimum viable diff: only code required for the feature
- No unrelated refactoring in the same commit
- No premature abstractions; DRY applies after 3+ uses
- Type safety: all functions have type hints
- Comments only for non-obvious logic
- Clear error messages; avoid cryptic codes

### X. Traceability & Documentation

All decisions, code, and tests are traceable for hackathon judging and future reference.

**Non-negotiable rules**:
- Prompt History Records (PHR) created for every significant user input
- Architecture Decision Records (ADR) for major decisions
- Code references in documentation (e.g., `backend/routes/tasks.py:42`)
- Commit messages reference spec/ADR/PHR when applicable
- Final submission includes complete `/history/` for audit trail

## Security & Authentication (Foundation)

### JWT Token Flow

1. **Frontend (Better Auth)**:
   - User signs up/logs in via Better Auth UI
   - Better Auth generates JWT token and stores in secure storage
   - Centralized API client (`/lib/api.ts`) automatically attaches token to all requests

2. **Backend (FastAPI)**:
   - Dependency injection extracts JWT from `Authorization: Bearer <token>` header
   - Shared secret (`BETTER_AUTH_SECRET`) verifies signature
   - Extract `user_id` and user claims; inject into route handlers
   - All database queries filtered by `user_id`

### Authentication Errors

- **401 Unauthorized**: Missing/invalid/expired token
- **403 Forbidden**: Valid token but insufficient permissions (should not occur for basic task CRUD)

### Data Isolation Enforcement

Every route handler receives `current_user` dependency containing verified `user_id`. Before returning any data, verify ownership:

```python
# Example: Get task (must belong to current user)
@router.get("/tasks/{id}")
async def get_task(id: int, current_user = Depends(verify_jwt)):
    task = db.query(Task).filter(Task.id == id, Task.user_id == current_user["user_id"]).first()
    if not task:
        raise HTTPException(404)  # Hides whether task exists or belongs to another user
    return task
```

### No Session Storage

All state is in JWT. No user sessions in database. Eliminates logout-but-still-valid token race conditions.

## API Specifications (Phase II Core)

### Task CRUD Endpoints

| Method | Path | Description | Auth | Filtering |
|--------|------|-------------|------|-----------|
| `GET` | `/api/tasks` | List all user's tasks | JWT | `?status=pending/completed&sort=created_at` |
| `POST` | `/api/tasks` | Create new task | JWT | N/A |
| `GET` | `/api/tasks/{id}` | Get specific task | JWT | Verifies ownership |
| `PUT` | `/api/tasks/{id}` | Update task (full) | JWT | Verifies ownership |
| `PATCH` | `/api/tasks/{id}/complete` | Toggle completion | JWT | Verifies ownership |
| `DELETE` | `/api/tasks/{id}` | Delete task | JWT | Verifies ownership |

### Request/Response Schemas

**Create Task** (`POST /api/tasks`):
```json
Request: { "title": "string (required)", "description": "string (optional)" }
Response (201): { "id": int, "user_id": string, "title": string, "description": string, "completed": false, "created_at": "ISO8601", "updated_at": "ISO8601" }
```

**List Tasks** (`GET /api/tasks`):
```json
Response (200): [{ task object }, ...]
```

**Update Task** (`PUT /api/tasks/{id}`):
```json
Request: { "title": "string", "description": "string" }
Response (200): { task object }
```

**Toggle Completion** (`PATCH /api/tasks/{id}/complete`):
```json
Response (200): { task object with updated completed status }
```

## Frontend Standards (Next.js 16+ App Router)

### Architecture

- **Server Components** (default): Fetch data server-side; render HTML
- **Client Components** (`use client`): Only for interactive elements (forms, real-time updates)
- **Centralized API Client** (`/lib/api.ts`): All HTTP requests go through single client; JWT attached automatically
- **Layout & Pages**: Organize by feature (e.g., `/app/tasks/page.tsx`, `/app/tasks/[id]/page.tsx`)
- **Components**: Reusable shadcn/ui components; minimal custom CSS

### Required Features

1. **Auth Guard**: Redirect unauthenticated users to login (Better Auth handles UI)
2. **Task List Page** (`/app/tasks`): Display all user tasks with completion status
3. **Add Task Form**: Create new task (title, optional description)
4. **Edit Task Modal/Form**: Update existing task
5. **Delete Confirmation**: Confirm before deletion
6. **Mark Complete**: Toggle completion status (button or checkbox)

### Responsive Design

- Mobile-first: Tailwind responsive classes
- Desktop: Full layout with sidebar/navigation
- Dark mode ready: shadcn/ui theme support

## Backend Standards (FastAPI + SQLModel)

### Project Structure

```
backend/
├── main.py                 # FastAPI app, CORS, middleware, routes
├── db.py                   # Database connection, session management
├── models.py               # SQLModel tables (Task, User if needed)
├── schemas.py              # Pydantic schemas for request/response validation
├── dependencies/
│   └── auth.py             # JWT verification, current_user injection
├── routes/
│   └── tasks.py            # Task CRUD endpoints
├── pyproject.toml          # UV dependencies
└── .env.example            # Environment variable template
```

### Async Patterns

- All route handlers are `async def`
- Database operations use SQLModel async sessions
- No blocking I/O; use appropriate async libraries

### Error Handling

- Custom `HTTPException` with clear messages
- Proper status codes (400, 401, 403, 404, 500)
- Stack traces logged; generic messages returned to client

## Testing Standards

### Backend Tests

- **Unit**: Model creation, schema validation, utility functions
- **Integration**: Full request/response cycle, authentication, authorization
- **Security**: Cross-user access attempts must fail with 401/403

### Frontend Tests

- **Component**: Render, user interaction, async data loading
- **Integration**: Full auth flow, task CRUD workflow
- **E2E**: Login → Create task → Edit → Mark complete → Delete

### Coverage & CI/CD

- Backend: 80%+ coverage for routes and models
- Frontend: 70%+ coverage for critical paths
- CI/CD pipeline runs tests on every PR; must pass before merge

## Development Workflow

### Specification Phase

1. Write spec for feature/API/database/UI change
2. User approves spec
3. Plan phase begins

### Planning Phase

1. Architect solution given spec
2. Identify tasks and dependencies
3. Document decisions (ADRs for significant ones)
4. User approves plan

### Implementation Phase

1. Execute tasks in dependency order
2. Generate code from plan using specialized agents
3. Tests written alongside code
4. All changes reference spec/plan/task
5. Commit with traceability information

### Testing Phase

1. All tests pass locally
2. Code review verifies compliance with constitution
3. Cross-user security tests executed
4. Integration tests verify full flows

### Deployment Readiness

- All specs in `/specs/`
- All decisions in `/history/adr/`
- All prompts in `/history/prompts/`
- All tests passing
- Code coverage ≥ thresholds
- Commit history clean and traceable

## Governance

### Constitution Authority

This constitution supersedes all other guidance. When conflicts arise, this document is authoritative. Every pull request must verify compliance before merge.

### Amendment Process

1. **Identification**: Current principle/section identified as inadequate
2. **Proposal**: Detailed amendment with rationale and impact on existing code
3. **Approval**: User consent required
4. **Migration**: Changes to dependent code/specs documented
5. **Version Bump**: Semantic versioning applied
6. **Documentation**: Changelog updated; team notified

### Version Numbering

- **MAJOR**: Backward-incompatible principle changes or removals
- **MINOR**: New principles or significant expansions
- **PATCH**: Clarifications, wording, non-semantic refinements

### Compliance Review

- All specs verified against constitution before approval
- All code generation validated against stack/architecture rules
- Security principles (user isolation, auth) verified on every implementation
- Code reviews check: traceability, compliance, tests, simplicity

### Runtime Guidance

Detailed development guidance in `CLAUDE.md` files at each level:
- Root: `/CLAUDE.md` (constitutional context)
- Frontend: `/frontend/CLAUDE.md` (Next.js patterns)
- Backend: `/backend/CLAUDE.md` (FastAPI patterns)

These files evolve with constitution but never contradict it.

### Hackathon Submission Checklist

Before final submission:

- [ ] All features functional and tested
- [ ] User isolation verified: attempts to access other users' tasks fail
- [ ] Authentication: all endpoints require valid JWT
- [ ] Specs complete: `/specs/` organized and comprehensive
- [ ] Architecture decisions documented: `/history/adr/`
- [ ] Prompt history complete: `/history/prompts/` with all major interactions
- [ ] Code references correct: all citations match actual line numbers
- [ ] Tests passing: backend ≥80%, frontend ≥70% coverage
- [ ] Monorepo clean: no stray files, proper structure
- [ ] Documentation: README updated for Phase II; setup instructions clear
- [ ] Commit history traceable: messages reference specs/decisions

## Sync Impact Report

<!-- Generated: 2026-01-03 -->

### Version Change
- **Old**: [CONSTITUTION_VERSION] (template, unversioned)
- **New**: 1.0.0 (Phase II kickoff)

### Modified Principles
- New constitution established; no renames (first version)

### Added Sections
- Security & Authentication (JWT token flow, data isolation)
- API Specifications (REST endpoints, request/response schemas)
- Frontend Standards (Next.js App Router patterns)
- Backend Standards (FastAPI structure, async patterns)
- Testing Standards (unit, integration, E2E, coverage)
- Development Workflow (spec → plan → implement → test)
- Governance (amendment process, versioning, compliance, hackathon checklist)

### Removed Sections
- None (first complete constitution)

### Templates Requiring Updates

| Template | Status | Notes |
|----------|--------|-------|
| `/specs/features/spec-template.md` | ⚠ Pending | Create feature spec template aligned with Section V |
| `/specs/api/api-template.md` | ⚠ Pending | Create API spec template aligned with Section "API Specifications" |
| `/specs/database/db-template.md` | ⚠ Pending | Create database spec template aligned with Section "Database Design" |
| `/specs/ui/ui-template.md` | ⚠ Pending | Create UI spec template aligned with Section "Frontend Standards" |
| `.specify/templates/plan-template.md` | ⚠ Pending | Verify alignment with "Development Workflow" |
| `.specify/templates/tasks-template.md` | ⚠ Pending | Verify alignment with "Implementation Phase" |
| `CLAUDE.md` (root) | ⚠ Pending | Sync with constitution; remove outdated phase-specific guidance |
| `/frontend/CLAUDE.md` | ⚠ Pending | Create; align with "Frontend Standards" |
| `/backend/CLAUDE.md` | ⚠ Pending | Create; align with "Backend Standards" |

### Follow-Up TODOs

- [ ] Create spec templates for all domains (features, api, database, ui)
- [ ] Create frontend and backend CLAUDE.md guidance files
- [ ] Set up CI/CD pipeline with test coverage gates
- [ ] Initialize `.env.example` with required variables (BETTER_AUTH_SECRET, DATABASE_URL, etc.)
- [ ] Create first set of specs for Phase II features (auth, task CRUD, database schema)

---

**Version**: 1.0.0 | **Ratified**: 2026-01-03 | **Last Amended**: 2026-01-03
