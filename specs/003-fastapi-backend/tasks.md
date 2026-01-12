# Implementation Tasks: Secure FastAPI Backend with JWT & PostgreSQL

**Feature**: Secure FastAPI Backend with JWT & PostgreSQL
**Branch**: `003-fastapi-backend`
**Status**: Ready for Implementation
**Last Updated**: 2026-01-08

---

## Overview

Complete implementation of FastAPI authentication system with JWT token generation and task management with strict user isolation. Tasks organized by user story for parallel execution and independent testing.

**Architecture**: Custom FastAPI auth endpoints (signup/login/verify) + JWT token generation + existing JWT verification + task CRUD with user isolation.

---

## Phase 1: Setup & Project Initialization

- [x] T001 Verify project structure matches implementation plan (`backend/`, `frontend/`, `specs/`)

- [x] T002 [P] Verify BETTER_AUTH_SECRET is configured in `backend/.env`

- [x] T003 [P] Verify DATABASE_URL is configured in `backend/.env` pointing to Neon PostgreSQL

- [x] T004 [P] Verify Python version >= 3.9 and FastAPI 0.100+ installed in `backend/`

---

## Phase 2: Foundational Authentication Infrastructure

- [x] T005 [P] Replace `pyjwt==2.8.0` with `python-jose[cryptography]==3.3.0` in `backend/requirements.txt` line 11

- [x] T006 [P] Add `passlib[bcrypt]==1.7.4` to `backend/requirements.txt` after line 12

- [x] T007 [P] Run `cd backend && uv pip install python-jose[cryptography] passlib[bcrypt]` to verify install

- [x] T008 [P] Verify `config.py` exports `settings.BETTER_AUTH_SECRET` for use in auth modules

- [x] T009 Add `User` SQLModel to `backend/src/models.py` with fields: id, email (unique, indexed), hashed_password, created_at

- [x] T010 Create `UserSignup`, `UserLogin`, `AuthResponse`, `VerifyResponse` schemas in `backend/src/schemas.py`

- [x] T011 [P] Create password hashing module at `backend/src/utils/password.py` with hash_password() and verify_password()

- [x] T012 [P] Create JWT token generation module at `backend/src/utils/jwt.py` with create_access_token()

- [x] T013 Verify database schema auto-creation by running backend startup and checking Neon database for `user` table

---

## Phase 3: User Story 1 — Create and View Tasks (Priority: P1)

**Story Goal**: Authenticated users can create tasks and view only their own tasks.

**Independent Test**: Signup → Receive token → Create task → List tasks (see own only) → Other user cannot access.

- [x] T014 [P] [US1] Create authentication router at `backend/src/routes/auth.py` with POST /auth/signup endpoint

- [x] T015 [P] [US1] Add POST /auth/login endpoint to `backend/src/routes/auth.py`

- [x] T016 [P] [US1] Add GET /auth/verify endpoint to `backend/src/routes/auth.py`

- [x] T017 [US1] Register auth router in `backend/src/main.py` (import and app.include_router)

- [x] T018 [US1] Create auth endpoint tests at `backend/tests/test_auth.py` (test_signup_success, test_login, test_verify_token, etc.)

- [x] T019 [US1] Run auth tests: `cd backend && pytest tests/test_auth.py -v` (all 7+ tests pass)

- [x] T020 [US1] Verify existing task routes use JWT auth in `backend/src/routes/tasks.py` (no modifications needed)

- [x] T021 [US1] Create integration test test_full_auth_flow() in `backend/tests/test_auth.py` (signup → create task → list)

- [x] T022 [US1] Run integration test: `cd backend && pytest tests/test_auth.py::test_full_auth_flow -v` (passes)

---

## Phase 4: User Story 2 — Update & Complete Tasks (Priority: P1)

**Story Goal**: Users can update and toggle completion status of their tasks. Only owner can modify.

**Independent Test**: Create task → PUT to update → PATCH to toggle complete → Other user gets 404.

- [x] T023 [US2] Verify PUT /api/tasks/{id} implementation in `backend/src/routes/tasks.py` (no modifications needed)

- [x] T024 [P] [US2] Verify PATCH /api/tasks/{id}/complete implementation in `backend/src/routes/tasks.py`

- [x] T025 [US2] Add tests to `backend/tests/test_tasks.py`: test_update_task_success, test_toggle_complete_success, test_update_not_owner, test_toggle_not_owner

- [x] T026 [US2] Run update/complete tests: `cd backend && pytest tests/test_tasks.py::test_update_task_success tests/test_tasks.py::test_toggle_complete_success -v`

---

## Phase 5: User Story 3 — Delete Tasks (Priority: P1)

**Story Goal**: Users can delete their own tasks. Only owner can delete.

**Independent Test**: Create task → DELETE → Verify 404 on GET → Other user cannot delete.

- [x] T027 [US3] Verify DELETE /api/tasks/{id} implementation in `backend/src/routes/tasks.py` (no modifications needed)

- [x] T028 [US3] Add tests to `backend/tests/test_tasks.py`: test_delete_task_success, test_delete_not_owner, test_delete_verify_gone

- [x] T029 [US3] Run delete tests: `cd backend && pytest tests/test_tasks.py::test_delete_task_success tests/test_tasks.py::test_delete_not_owner -v`

---

## Phase 6: User Story 4 — Multi-User Isolation (Priority: P1)

**Story Goal**: Verify complete data isolation. User A never sees User B's tasks via any operation.

**Independent Test**: Two users signup → Create tasks → Each sees only own → Cross-user GET/PUT/DELETE returns 404.

- [x] T030 [US4] Add multi-user isolation tests to `backend/tests/test_tasks.py`: test_user_isolation_list, test_cross_user_get_returns_404, test_cross_user_put_returns_404, test_cross_user_delete_returns_404

- [x] T031 [US4] Run isolation tests: `cd backend && pytest tests/test_tasks.py::test_user_isolation_list tests/test_tasks.py::test_cross_user_get_returns_404 tests/test_tasks.py::test_cross_user_put_returns_404 tests/test_tasks.py::test_cross_user_delete_returns_404 -v`

---

## Phase 7: User Story 5 — Filter Tasks by Status (Priority: P2)

**Story Goal**: Users can filter tasks by completion status.

**Independent Test**: Create 3 tasks (2 pending, 1 completed) → ?status=pending returns 2 → ?status=completed returns 1 → ?status=all returns 3.

- [x] T032 [US5] Verify GET /api/tasks status filtering in `backend/src/routes/tasks.py:35` (check if implemented)

- [x] T033 [P] [US5] If incomplete, implement status filter logic: add ?status parameter, validate (pending/completed/all), apply filter, return 400 for invalid

- [x] T034 [US5] Add filtering tests to `backend/tests/test_tasks.py`: test_filter_pending, test_filter_completed, test_filter_all, test_filter_default, test_filter_invalid

- [x] T035 [US5] Run filtering tests: `cd backend && pytest tests/test_tasks.py::test_filter_pending tests/test_tasks.py::test_filter_completed tests/test_tasks.py::test_filter_invalid -v`

---

## Phase 8: Polish & Verification

- [x] T036 Run complete test suite: `cd backend && pytest tests/ -v --tb=short` (all tests pass, coverage >= 80%)

- [x] T037 [P] Verify backend starts cleanly: `cd backend && python -m uvicorn src.main:app --reload` (no errors, /docs available)

- [x] T038 [P] Verify Neon database schema: Connect to console, confirm tables (user, task) with correct columns and indexes

- [x] T039 [P] Test signup: `curl -X POST http://localhost:8000/auth/signup -d '{"email":"test1@example.com","password":"SecurePass123!"}'` (201 with token)

- [x] T040 [P] Test login: `curl -X POST http://localhost:8000/auth/login -d '{"email":"test1@example.com","password":"SecurePass123!"}'` (200 with token)

- [x] T041 [P] Test create task with token: `curl -X POST http://localhost:8000/api/tasks -H "Authorization: Bearer <TOKEN>" -d '{"title":"Test"}'` (201)

- [x] T042 [P] Test cross-user isolation: User 2 tries `curl -X GET http://localhost:8000/api/tasks/{user1_task_id} -H "Authorization: Bearer <USER2_TOKEN>"` (404)

- [x] T043 Test frontend signup: Navigate to http://localhost:3000/login, click Sign Up, enter email/password, verify redirect to /tasks and token in localStorage

- [x] T044 Test frontend login: On login page, enter credentials, verify redirect to /tasks and token stored

- [x] T045 Test frontend task creation: Create task, verify appears in list, persists on refresh

- [x] T046 Test frontend task update: Edit task, verify title updates and persists

- [x] T047 Test frontend task completion: Toggle completion checkbox, verify visual update and persistence

- [x] T048 Test frontend logout & re-login: Logout/clear localStorage, verify redirect to /login, re-login and verify tasks visible

- [x] T049 [P] Update `backend/.env.example` with placeholders for BETTER_AUTH_SECRET, DATABASE_URL, CORS_ORIGINS

- [x] T050 [P] Verify `.env` is in `.gitignore` and no hardcoded credentials in code

- [x] T051 [P] Create IMPLEMENTATION_COMPLETE.md listing: Features (signup, login, task CRUD, isolation), Tests (11 auth + 20+ task), Tables (user, task)

---

## Task Summary

| Phase | Name | Count |
|-------|------|-------|
| 1 | Setup | 4 |
| 2 | Foundational Auth | 9 |
| 3 | US1: Create & View | 9 |
| 4 | US2: Update & Complete | 4 |
| 5 | US3: Delete | 3 |
| 6 | US4: Multi-User Isolation | 2 |
| 7 | US5: Status Filtering | 4 |
| 8 | Polish & Verification | 16 |
| **TOTAL** | | **51 tasks** |

## Parallelization

**Can run in parallel**:
- Phase 1: All 4 tasks (setup)
- Phase 2: Tasks T005-T012 (dependencies, models, schemas, utilities)
- Phase 3: Tasks T014-T016 and T018-T022 (routes and tests, after models)
- Phase 8: All verification tasks (independent)

**MVP Scope**: Complete Phase 1, 2, and 3 (~25 tasks) for minimum viable product with signup/login and task isolation.

**Estimated Time**: 1-2 hours with parallel execution

---

**Ready for implementation** | Generated: 2026-01-08 | Next: Begin Phase 1 or Phase 2 with parallel task execution

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

