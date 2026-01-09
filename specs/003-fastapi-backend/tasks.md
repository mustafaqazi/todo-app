# Implementation Tasks: Secure FastAPI Backend with JWT & PostgreSQL

**Feature**: 003-fastapi-backend
**Branch**: `003-fastapi-backend`
**Date**: 2026-01-08
**Status**: Ready for Implementation
**Scope**: Production-ready FastAPI backend with JWT auth, SQLModel ORM, Neon PostgreSQL, and strict user isolation

---

## Task Breakdown Strategy

This task list is organized by **User Story** (priority order from spec.md):
- **Phase 1**: Project Setup & Infrastructure
- **Phase 2**: JWT Authentication Middleware (Foundational)
- **Phase 3**: Database Models & Schemas (Foundational)
- **Phase 4**: User Story 1 - Create & View Tasks (P1, Critical)
- **Phase 5**: User Story 2 - Update & Complete Tasks (P1, Critical)
- **Phase 6**: User Story 3 - Delete Tasks (P1, Critical)
- **Phase 7**: User Story 4 - Multi-User Isolation (P1, Critical)
- **Phase 8**: User Story 5 - Filter Tasks by Status (P2, Enhancement)
- **Phase 9**: Documentation & Testing

---

## Phase 1: Project Setup & Infrastructure

- [ ] T001 Create backend project structure per plan.md in `/backend/`
- [ ] T002 [P] Initialize pyproject.toml with dependencies in `/backend/pyproject.toml`
- [ ] T003 [P] Create `.env` configuration file at `/backend/.env`
- [ ] T004 Implement FastAPI app initialization in `/backend/main.py`

## Phase 2: JWT Authentication Middleware (Foundational)

- [ ] T005 Implement JWT verification dependency in `/backend/dependencies/auth.py`
- [ ] T006 [P] Create test fixtures for JWT tokens in `/backend/tests/conftest.py`

## Phase 3: Database Models & Schemas (Foundational)

- [ ] T007 Implement Task model in `/backend/models.py`
- [ ] T008 [P] Implement Pydantic schemas in `/backend/schemas.py`
- [ ] T009 Implement async database connection in `/backend/db.py`

## Phase 4: User Story 1 - Create & View Tasks (P1)

- [ ] T010 [US1] Implement POST /api/tasks in `/backend/routes/tasks.py`
- [ ] T011 [US1] Implement GET /api/tasks in `/backend/routes/tasks.py`
- [ ] T012 [US1] Implement GET /api/tasks/{id} in `/backend/routes/tasks.py`
- [ ] T013 [P] [US1] Create integration tests in `/backend/tests/test_tasks.py`

## Phase 5: User Story 2 - Update & Complete Tasks (P1)

- [ ] T014 [US2] Implement PUT /api/tasks/{id} in `/backend/routes/tasks.py`
- [ ] T015 [US2] Implement PATCH /api/tasks/{id}/complete in `/backend/routes/tasks.py`
- [ ] T016 [P] [US2] Create integration tests in `/backend/tests/test_tasks.py`

## Phase 6: User Story 3 - Delete Tasks (P1)

- [ ] T017 [US3] Implement DELETE /api/tasks/{id} in `/backend/routes/tasks.py`
- [ ] T018 [P] [US3] Create integration tests in `/backend/tests/test_tasks.py`

## Phase 7: User Story 4 - Multi-User Isolation (P1)

- [ ] T019 [P] [US4] Create comprehensive isolation tests in `/backend/tests/test_isolation.py`
- [ ] T020 [US4] Validate acceptance criteria from User Story 4

## Phase 8: User Story 5 - Filter by Status (P2)

- [ ] T021 [US5] Enhance GET /api/tasks with status filtering in `/backend/routes/tasks.py`
- [ ] T022 [P] [US5] Create tests for status filtering in `/backend/tests/test_tasks.py`

## Phase 9: Documentation & Polish

- [ ] T023 Verify Swagger UI auto-documentation in `/backend/main.py`
- [ ] T024 [P] Implement comprehensive error handling in all route handlers
- [ ] T025 [P] Create `.env.example` template at `/backend/.env.example`
- [ ] T026 [P] Run complete integration test suite with coverage validation
- [ ] T027 Manual end-to-end testing via curl and Swagger UI
- [ ] T028 Verify production readiness against constitution and spec

---

## Detailed Task Specifications

### Phase 1: Project Setup

**T001**: Create backend project structure
- Create `/backend/main.py`, `/backend/db.py`, `/backend/models.py`, `/backend/schemas.py`
- Create `/backend/dependencies/auth.py`, `/backend/routes/tasks.py`
- Create `/backend/tests/`, `/backend/pyproject.toml`

**T002**: Initialize dependencies
- FastAPI, SQLModel, Pydantic, PyJWT, asyncpg, python-dotenv
- pytest, pytest-asyncio, httpx (dev)

**T003**: Create `.env` with BETTER_AUTH_SECRET and DATABASE_URL

**T004**: FastAPI app with CORS, request logging, route registration, Swagger UI, startup event for table creation

### Phase 2: JWT Authentication

**T005**: Implement `verify_jwt()` dependency
- Extract JWT from `Authorization: Bearer <token>` header
- Verify signature using BETTER_AUTH_SECRET
- Extract user_id claim
- Raise 401 if invalid, expired, or missing user_id
- Return `{"user_id": "..."}`

**T006**: Create pytest fixtures
- `test_secret`, `test_user_id`, `valid_jwt_token`, `expired_jwt_token`, `invalid_jwt_token`
- `test_database`, `client`

### Phase 3: Database

**T007**: SQLModel Task entity
- id (PK), user_id (indexed FK), title (1-200), description (nullable), completed (bool, default false)
- created_at, updated_at (datetime)
- Compound indexes: (user_id, created_at), (user_id, completed)

**T008**: Pydantic schemas
- TaskCreate (title, description)
- TaskUpdate (title, description)
- Task response (all fields)

**T009**: Async database connection
- Create async engine with asyncpg driver
- Async session factory
- `get_session()` dependency
- `create_db_and_tables()` startup function

### Phase 4-8: User Stories

Each story includes:
- Route implementation (endpoint logic)
- Database query with user_id filtering
- Proper error handling (401, 404, 422)
- Integration tests

### Phase 9: Documentation & Validation

- Swagger UI docs
- Error handling for all edge cases
- Environment configuration
- Full test suite with coverage
- Manual E2E testing
- Production readiness checklist

---

## Parallelization Opportunities

After Phase 3 complete:
- **T010-T013** (US1) can run parallel with **T014-T016** (US2) and **T017-T018** (US3)
- **T019-T020** (US4) can run once T017-T018 complete
- **T021-T022** (US5) can run once T011 complete
- **T023-T028** (Documentation) can run parallel with later phases

---

## Acceptance Criteria

Each task complete when:
1. Code implements spec exactly
2. All tests pass (if applicable)
3. Type hints present
4. No exceptions in happy path
5. User isolation verified
6. Database changes persist
7. API responses match OpenAPI contract

---

**Total Tasks**: 28
**Estimated Time**: 6-8 hours sequential, 3-4 hours with parallelization
**Ready for**: `/sp.implement` or manual execution

