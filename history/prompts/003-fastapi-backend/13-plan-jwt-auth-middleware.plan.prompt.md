---
id: 13
title: Plan JWT auth middleware and backend architecture
stage: plan
date: 2026-01-08
surface: agent
model: claude-haiku-4-5
feature: 003-fastapi-backend
branch: 003-fastapi-backend
user: user
command: sp.plan
labels: ["fastapi", "jwt", "auth", "architecture", "data-model", "api-design"]
links:
  spec: E:\GH-Q4\todo-app-Phase2\specs\003-fastapi-backend\spec.md
  ticket: null
  adr: null
  pr: null
files:
  - E:\GH-Q4\todo-app-Phase2\specs\003-fastapi-backend\plan.md
  - E:\GH-Q4\todo-app-Phase2\specs\003-fastapi-backend\research.md
  - E:\GH-Q4\todo-app-Phase2\specs\003-fastapi-backend\data-model.md
  - E:\GH-Q4\todo-app-Phase2\specs\003-fastapi-backend\quickstart.md
  - E:\GH-Q4\todo-app-Phase2\specs\003-fastapi-backend\contracts\openapi.json
tests:
  - All acceptance criteria from spec.md testable via integration tests
  - Swagger API documentation auto-generated from FastAPI
---

## Prompt

run `/sp.plan` to design auth middleware

## Response snapshot

### Plan Execution (Phase 0 + Phase 1 Complete)

**Phase 0 (Research)**: No unknowns identified. All technical context pre-determined by constitution.
- JWT library: PyJWT (HS256)
- ORM: SQLModel with asyncpg
- Database: Neon PostgreSQL (async)
- Testing: pytest with async support
- User isolation: Database-level query filtering
- Error handling: FastAPI HTTPException with standardized response format
- Concurrency: asyncio native with connection pooling

**Phase 1 (Design)** delivered:

1. **plan.md**: Comprehensive implementation plan including:
   - Technical Context (Python 3.11+, FastAPI, SQLModel, asyncpg, pytest)
   - Constitution Check (PASS WITH CONDITIONS on user isolation, testability, database design)
   - Project Structure (backend/ with routes, models, schemas, dependencies, tests)
   - Phase 0 Research (no unknowns, best practices consolidated)
   - Phase 1 Design (data model, API contracts, quickstart)
   - Decision Log (JWT claim strategy, user isolation, connection pooling)

2. **research.md**: Best practices for:
   - JWT validation with FastAPI dependency injection
   - AsyncPG + SQLModel async setup
   - Database-layer user isolation filtering
   - Standardized error responses (401, 403, 404, 422)
   - Concurrent request handling
   - Integration test patterns for auth-protected endpoints

3. **data-model.md**: Complete Task entity specification:
   - Fields: id, user_id, title, description, completed, created_at, updated_at
   - Constraints: title NOT NULL (1-200), user_id indexed
   - Relationships: Foreign key to Better Auth users
   - Lifecycle: Create, Read, Update, Toggle, Delete with user_id filtering
   - Indexes: (user_id), (user_id, created_at), (user_id, completed)
   - Validation: Pydantic schemas (TaskCreate, TaskUpdate, Task response)
   - Immutability: created_at, user_id never modified post-creation

4. **quickstart.md**: Operational guide:
   - Setup (Python 3.11+, PostgreSQL, UV, .env configuration)
   - Database initialization (table creation, indexes)
   - Running development server (uvicorn main:app --reload --port 8000)
   - Testing endpoints via cURL with Bearer tokens
   - Troubleshooting (401, 404, 422, connection errors)
   - Frontend integration (CORS, JWT attachment, full flow testing)
   - Security checklist

5. **contracts/openapi.json**: OpenAPI 3.0 specification:
   - 6 endpoints fully specified (GET /tasks, POST /tasks, GET /tasks/{id}, PUT /tasks/{id}, PATCH /tasks/{id}/complete, DELETE /tasks/{id})
   - Request/response schemas with examples
   - Error responses with status codes and descriptions
   - Security scheme: BearerAuth (JWT)
   - Auto-generates Swagger UI and ReDoc documentation

### Architecture Decisions Finalized

1. **JWT Claim Extraction**: Extract `user_id` from JWT (custom claim, not `sub`)
2. **User Isolation**: Database-level filtering (WHERE user_id = current_user["user_id"])
3. **Database Concurrency**: AsyncPG + Neon serverless pooling for 50+ concurrent users
4. **Error Handling**: Standardized 401/404/422 responses, identical 404 for non-existent and non-owned tasks
5. **Code Structure**: dependencies/auth.py (JWT verification), routes/tasks.py (CRUD), models.py (SQLModel Task)

### Acceptance Criteria Status

✅ All acceptance criteria from spec.md are testable:
- [x] Backend runs: uvicorn main:app --reload --port 8000
- [x] Swagger lists all 6 endpoints (auto-generated)
- [x] User A sees own tasks; User B cannot (database query filtering enforced)
- [x] All CRUD return correct codes (401, 404, 422 specified in contracts)
- [x] Data matches /lib/api.ts (OpenAPI contract validated)
- [x] Database filters by user_id (architecture decision finalized)
- [x] Invalid JWT→401, bad title→422, wrong user→404 (error handling specified)

## Outcome

- ✅ Impact: Architecture designed and documented for JWT validation middleware, user isolation, and API contracts. Plan provides unambiguous direction for code implementation. Constitution Check PASSED WITH CONDITIONS (user_id injection, query filtering, test coverage verified during implementation).
- 🧪 Tests: Phase 0/1 outputs are testable; pytest integration tests will validate auth flows, user isolation, CRUD operations, concurrent requests, and error responses.
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.json created in specs/003-fastapi-backend/
- 🔁 Next prompts: `/sp.tasks` to generate actionable, dependency-ordered implementation tasks
- 🧠 Reflection: Planning phase complete with high fidelity (no unknowns remaining). All architectural decisions documented with rationale and alternatives. Ready for code generation by `/sp.implement` or manual task breakdown via `/sp.tasks`.

## Evaluation notes (flywheel)

- Failure modes observed: None; specification and clarification from earlier session provided sufficient context for complete architecture design
- Graders run and results (PASS/FAIL): Constitution Check PASS WITH CONDITIONS; all design decisions align with constitutionality; no violations identified
- Prompt variant (if applicable): N/A
- Next experiment: Code generation phase — implement based on plan.md; integration tests will validate JWT extraction, user_id filtering, and concurrent request handling against spec acceptance criteria

