# Research: JWT Authentication & FastAPI Backend Design

**Scope**: FastAPI + SQLModel + PostgreSQL backend for Phase II Todo app
**Date**: 2026-01-08
**Status**: Phase 0 Complete (no unresolved unknowns)

---

## Summary

No critical unknowns identified. All technical decisions are pre-determined by project constitution and Phase I clarifications. This research document consolidates best practices and rationale for implementation.

---

## 1. JWT Validation in FastAPI

### Decision: PyJWT with FastAPI Dependency Injection

**Library**: PyJWT (industry standard, minimal dependencies)
**Pattern**: FastAPI dependency injection for `current_user` extraction
**Shared Secret**: `BETTER_AUTH_SECRET` environment variable (set on frontend and backend)

### Rationale

- PyJWT is lightweight and audited (no unnecessary dependencies)
- FastAPI's `Depends()` pattern is idiomatic and testable
- Stateless validation (no session DB lookups) aligns with constitution
- Single dependency injection point prevents logic duplication

### Implementation Pattern

```python
# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt
import os

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

async def verify_jwt(credentials: HTTPAuthCredentials = Depends(security)) -> dict:
    """
    Verify JWT signature and extract user_id claim.
    Raises 401 if token invalid, expired, or user_id missing.
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id")
        return {"user_id": user_id}
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Usage in route:
@router.get("/api/tasks")
async def list_tasks(current_user = Depends(verify_jwt)):
    # current_user = {"user_id": "user123"}
    ...
```

### Alternatives Considered

| Alternative | Pros | Cons | Verdict |
|-----------|------|------|---------|
| python-jose (JWT library) | More features | Heavier dependencies | Rejected |
| Manual JWT parsing | Minimal overhead | Prone to errors, security issues | Rejected |
| Bearer token header parsing | Simple | Requires custom logic | Accepted pattern, built into PyJWT + HTTPBearer |

---

## 2. Database Access Pattern: AsyncPG + SQLModel

### Decision: Async ORM with Neon PostgreSQL

**ORM**: SQLModel (SQLAlchemy 2.x abstraction, Pydantic integrated)
**Driver**: asyncpg (async PostgreSQL driver)
**Connection Pool**: Neon's serverless connection pooling

### Rationale

- SQLModel bridges ORM (models) and Pydantic (schemas), reducing boilerplate
- asyncpg is the de facto async PostgreSQL driver
- Neon's serverless pooling eliminates connection management complexity
- FastAPI is async-first; blocking database calls would negate performance gains

### Implementation Pattern

```python
# db.py
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# Convert postgres:// to postgresql+asyncpg://
async_url = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    async_url,
    echo=False,  # Set True for SQL debugging
    pool_pre_ping=True,  # Test connections before use
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Dependency injection:
# Depends(get_session) provides AsyncSession to route handlers
```

### Alternatives Considered

| Alternative | Pros | Cons | Verdict |
|-----------|------|------|---------|
| Synchronous SQLAlchemy | Simpler code | Blocking I/O in async context | Rejected |
| psycopg3 (sync driver) | Stable | Blocks entire event loop | Rejected |
| Raw asyncpg queries | Fastest | No ORM, manual SQL | Rejected (YAGNI) |

---

## 3. User Isolation Enforcement

### Decision: Database-Layer Filtering with Query Constraints

**Pattern**: Every `db.query(Task)` includes `.filter(Task.user_id == current_user["user_id"])`
**Scope**: All read, update, delete operations
**Principle**: Defense-in-depth; if application logic fails, database constraints prevent leaks

### Rationale

- Database-level filtering is more secure than application-only checks
- Prevents accidental data leaks if route handler logic contains bugs
- Aligns with constitution principle: "Every database query MUST filter by user_id"
- Query results are always pre-filtered; no need for post-fetch checks

### Implementation Pattern

```python
# routes/tasks.py
@router.get("/api/tasks")
async def list_tasks(
    current_user: dict = Depends(verify_jwt),
    session: AsyncSession = Depends(get_session),
    status: str = Query("all", regex="^(all|pending|completed)$")
):
    query = select(Task).where(Task.user_id == current_user["user_id"])

    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks
```

### Alternatives Considered

| Alternative | Pros | Cons | Verdict |
|-----------|------|------|---------|
| Application-only filtering | Flexible, easy to test | Prone to logic errors | Rejected |
| Repository pattern with filtering | Reduces code duplication | YAGNI for Phase II | Deferred |
| Row-level security (RLS) in PostgreSQL | Database enforces policy | Complex to set up, harder to debug | Deferred (Phase III?) |

---

## 4. Error Response Standards

### Decision: FastAPI HTTPException with Standardized Error Format

**Status Codes**:
- **401 Unauthorized**: Missing/invalid/expired JWT
- **403 Forbidden**: Valid JWT but insufficient permissions (reserved for future)
- **404 Not Found**: Task doesn't exist OR not owned by user (identical response to prevent information leakage)
- **422 Unprocessable Entity**: Validation error (title too long, etc.)

**Response Format**:
```json
{
  "detail": "Human-readable error message"
}
```

For 422 errors (Pydantic validation):
```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": ["body", "title"],
      "msg": "String should have at most 200 characters",
      "input": "..."
    }
  ]
}
```

### Rationale

- Consistent with FastAPI default error format
- Clear messages help debugging without leaking sensitive info
- 404 for both "not found" and "not owned" prevents user enumeration

### Implementation Pattern

```python
from fastapi import HTTPException, status

# Invalid JWT
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# Task not found or not owned (identical response)
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

# Validation error (handled automatically by Pydantic)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
```

---

## 5. Concurrent Request Handling

### Decision: FastAPI's Native Async Concurrency

**Mechanism**: asyncio event loop with asyncpg connection pooling
**Concurrency Level**: Supports 50+ concurrent users (spec requirement)
**Bottleneck**: Database connection pool, not application code

### Rationale

- FastAPI handles concurrency via asyncio; each request runs concurrently if I/O-bound
- asyncpg connection pooling prevents connection exhaustion
- Neon's serverless connection pooling handles burst traffic

### Implementation Guarantees

- All route handlers are `async def`
- All database operations use `await`
- No blocking operations (no time.sleep, CPU-bound loops, file I/O)
- Connection pooling: Neon + asyncpg handle 50+ concurrent connections

### Alternatives Considered

| Alternative | Pros | Cons | Verdict |
|-----------|------|------|---------|
| Thread pool executors | Familiar to sync devs | Overhead for I/O-bound workloads | Rejected |
| Gunicorn + workers | Good for scaling | Overkill for async framework | Deferred (Phase III?) |
| uvicorn with multiple workers | Horizontal scaling | Adds complexity, external state | Deferred |

---

## 6. Integration Testing for Auth-Protected Endpoints

### Decision: pytest + httpx with Test Client

**Framework**: pytest with async support (`pytest-asyncio`)
**HTTP Client**: httpx (async test client for FastAPI)
**Test Tokens**: Generate valid JWTs using same `BETTER_AUTH_SECRET` (test fixture)

### Rationale

- pytest is Python standard for testing
- httpx has native async support for FastAPI
- Test tokens allow full endpoint testing without real Better Auth service
- Integration tests can simulate concurrent requests and cross-user scenarios

### Implementation Pattern

```python
# tests/conftest.py
import jwt
import pytest
from datetime import datetime, timedelta

@pytest.fixture
def test_secret():
    return "test-secret-key"

@pytest.fixture
def test_user_id():
    return "test-user-123"

@pytest.fixture
def valid_jwt_token(test_secret, test_user_id):
    payload = {
        "user_id": test_user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, test_secret, algorithm="HS256")

# tests/test_tasks.py
@pytest.mark.asyncio
async def test_list_tasks_unauthorized(client):
    response = await client.get("/api/tasks")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_tasks_authorized(client, valid_jwt_token):
    response = await client.get("/api/tasks", headers={"Authorization": f"Bearer {valid_jwt_token}"})
    assert response.status_code == 200
```

---

## Decision Summary Table

| Aspect | Chosen | Rationale | Trade-offs |
|--------|--------|-----------|-----------|
| JWT Library | PyJWT | Standard, minimal deps | Less feature-rich than python-jose |
| Database ORM | SQLModel | Pydantic integration, async | Learning curve for SQLAlchemy 2.x |
| Async Driver | asyncpg | De facto standard, fastest | PostgreSQL-specific |
| User Isolation | Database-level filtering | Secure, defense-in-depth | Requires discipline in all queries |
| Error Format | FastAPI HTTPException | Idiomatic, consistent | Slightly verbose for some cases |
| Concurrency | asyncio native | Zero overhead for async code | All code must be async-aware |
| Testing | pytest + httpx | Familiar, async-capable | Setup overhead for fixtures |

---

## Implementation Checklist

- [ ] PyJWT installed in backend pyproject.toml
- [ ] HTTPBearer security scheme implemented in dependencies/auth.py
- [ ] SQLModel async engine and session factory configured in db.py
- [ ] Task model with proper indexes and constraints defined in models.py
- [ ] Pydantic TaskCreate/TaskUpdate schemas in schemas.py
- [ ] All routes use Depends(verify_jwt) and Depends(get_session)
- [ ] All Task queries include .where(Task.user_id == current_user["user_id"])
- [ ] Error handling returns 401, 404, 422 with standardized messages
- [ ] All route handlers are async def
- [ ] All database operations use await
- [ ] Integration tests cover auth flows, user isolation, concurrent requests
- [ ] Swagger/OpenAPI documentation auto-generated by FastAPI

---

**Next**: Phase 1 Design (data-model.md, contracts/, quickstart.md) complete. Proceed to `/sp.tasks` for implementation task generation.
