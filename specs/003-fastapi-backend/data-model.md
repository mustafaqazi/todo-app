# Data Model: Task Entity

**Feature**: Secure FastAPI Backend with JWT & PostgreSQL
**Date**: 2026-01-08
**Status**: Phase 1 Complete

---

## Entity Definition: Task

### Core Attributes

| Attribute | Type | Constraints | Notes |
|-----------|------|-------------|-------|
| `id` | int | Primary Key, auto-increment | Unique identifier for task |
| `user_id` | str (255) | NOT NULL, Indexed | Extracted from JWT user_id claim; links to Better Auth users |
| `title` | str (200) | NOT NULL, 1-200 chars | Task title; validation enforced in Pydantic schema |
| `description` | str (1000) | NULLABLE, optional | Additional context for task |
| `completed` | bool | NOT NULL, default=false | Completion status; toggled via PATCH endpoint |
| `created_at` | datetime | NOT NULL, UTC, immutable | Timestamp of task creation; set once, never updated |
| `updated_at` | datetime | NOT NULL, UTC, auto-update | Timestamp of last modification; updated on every change |

### Database Constraints

```sql
-- Table Definition
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(200) NOT NULL CHECK (length(title) > 0),
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES auth_users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_task_user_id ON tasks(user_id);
CREATE INDEX idx_task_user_created ON tasks(user_id, created_at);
CREATE INDEX idx_task_user_completed ON tasks(user_id, completed);
```

### Indexes & Query Optimization

| Index | Columns | Purpose | Query |
|-------|---------|---------|-------|
| Primary Key | `id` | Unique identification | `SELECT * FROM tasks WHERE id = ?` |
| user_id | `user_id` | Filter by owner | `SELECT * FROM tasks WHERE user_id = ?` |
| Compound (user_id, created_at) | `user_id`, `created_at` | List and sort by date | `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC` |
| Compound (user_id, completed) | `user_id`, `completed` | Filter by status | `SELECT * FROM tasks WHERE user_id = ? AND completed = ?` |

### Relationships

**Foreign Key**: `user_id` → `auth_users(id)` (Better Auth table)
- **Cardinality**: Many tasks per user (1:N)
- **Deletion**: CASCADE (delete tasks when user is deleted)
- **Reference**: Read-only; backend does not create/manage users

### Field Validation Rules

**title**:
- Required (NOT NULL in database)
- Length: 1-200 characters
- Enforced at: Database (CHECK constraint), Pydantic (Field with min_length, max_length)
- Example values: "Buy groceries", "Finish Q1 report"

**description**:
- Optional (NULL allowed)
- Max length: 1000 characters
- Enforced at: Pydantic (Field with max_length) if provided
- Example values: "milk, eggs, bread", null

**completed**:
- Boolean flag (true/false)
- Default: false (new tasks start as pending)
- Mutable: Can be toggled via PATCH /api/tasks/{id}/complete
- Query filter: ?status=pending (&completed=false), ?status=completed (&completed=true)

**user_id**:
- Extracted from JWT "user_id" claim
- Non-empty string (validated by JWT extraction)
- Immutable (set at creation, never modified)
- Links all tasks to owning user; enforces isolation

**created_at** / **updated_at**:
- ISO 8601 format (UTC timezone)
- created_at: Set once at insert, never changed
- updated_at: Auto-updated on every INSERT or UPDATE
- Used for sorting, audit trails

---

## Entity Lifecycle

### Create (POST /api/tasks)

**Trigger**: User submits new task
**Input**: { "title": "...", "description": "..." }
**Process**:
1. FastAPI dependency extracts JWT, gets `user_id`
2. Pydantic validates title (length 1-200), description (length <= 1000)
3. SQLModel creates Task instance with:
   - `user_id` = current_user["user_id"]
   - `title` = request.title
   - `description` = request.description (or None)
   - `completed` = false (default)
   - `created_at` = datetime.utcnow() (database sets CURRENT_TIMESTAMP)
   - `updated_at` = datetime.utcnow() (database sets CURRENT_TIMESTAMP)
4. INSERT into tasks table
5. Return 201 Created with full Task object

**Outcome**: New task record with auto-generated `id`

### Read (GET /api/tasks, GET /api/tasks/{id})

**Trigger**: User requests task list or specific task
**Query**: SELECT * FROM tasks WHERE user_id = ? [AND completed = ?] [ORDER BY created_at DESC]
**Constraints**:
- All queries include `WHERE user_id = current_user["user_id"]` (database-level isolation)
- Task {id} endpoints verify task belongs to user (return 404 if not owned)
- Status filter (?status=pending/completed) applied as WHERE clause

**Outcome**: Task(s) returned with all fields; no cross-user leakage

### Update (PUT /api/tasks/{id})

**Trigger**: User modifies existing task
**Input**: { "title": "...", "description": "..." }
**Process**:
1. Query task by id AND user_id (verify ownership, return 404 if not owned)
2. Validate new title (length 1-200) via Pydantic
3. UPDATE:
   - title = request.title
   - description = request.description (or None)
   - updated_at = CURRENT_TIMESTAMP (database auto-updates)
   - IMMUTABLE: id, user_id, created_at, completed (not changed)
4. Return 200 OK with updated Task object

**Outcome**: Task modified, updated_at reflects change; owned and auditable

### Toggle (PATCH /api/tasks/{id}/complete)

**Trigger**: User marks task complete/incomplete
**Input**: (empty body)
**Process**:
1. Query task by id AND user_id (verify ownership, return 404 if not owned)
2. UPDATE:
   - completed = NOT completed (toggle)
   - updated_at = CURRENT_TIMESTAMP (database auto-updates)
3. Return 200 OK with Task object showing new completed status

**Outcome**: Task completion toggled; timestamp updated

### Delete (DELETE /api/tasks/{id})

**Trigger**: User removes task
**Input**: (none)
**Process**:
1. Query task by id AND user_id (verify ownership, return 404 if not owned)
2. DELETE FROM tasks WHERE id = ? AND user_id = ?
3. Return 204 No Content (empty body)

**Outcome**: Task record removed; no soft delete, full removal

---

## Validation Summary

### At Pydantic Layer (FastAPI)

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(None, max_length=1000, description="Optional details")

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

class Task(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # Support SQLModel instances
```

### At Database Layer (SQL)

- `title`: NOT NULL, CHECK (length > 0), max 200 chars
- `description`: NULLABLE, max 1000 chars (if stored as VARCHAR)
- `user_id`: NOT NULL, indexed, foreign key
- `completed`: NOT NULL, default FALSE
- `id`: PRIMARY KEY, auto-increment

---

## Data Integrity Guarantees

### User Isolation (Constitutional)

**Guarantee**: No user can read, modify, or delete another user's tasks
**Enforcement**:
1. JWT extraction ensures correct user_id
2. Database query filtering: WHERE user_id = current_user_id
3. 404 response hides task existence from unauthorized users
4. Tests verify cross-user access returns 404

### Immutability (Audit Trail)

**Guarantee**: created_at and user_id never change after creation
**Enforcement**:
1. Database: No UPDATE clause includes these columns
2. Application: Schema/model does not allow modification
3. Audit friendly: Task creation date always available

### Timestamp Accuracy

**Guarantee**: Timestamps are UTC and timezone-aware
**Enforcement**:
1. Database: TIMESTAMP type with DEFAULT CURRENT_TIMESTAMP (UTC)
2. ORM: Pydantic returns datetime objects with UTC timezone
3. API: Responses in ISO 8601 format (2026-01-08T10:30:00Z)

### Referential Integrity

**Guarantee**: Every task.user_id references a valid Better Auth user
**Enforcement**:
1. Database: FOREIGN KEY constraint (REFERENCES auth_users)
2. Application: user_id extracted from valid JWT (verified signature)
3. Cascade: Deleting a Better Auth user cascades to delete their tasks

---

## Scalability Considerations

### Query Performance

- **Typical query**: ~5-50ms for indexed (user_id, created_at) scan
- **Bottleneck**: PostgreSQL full table scans if user_id not indexed
- **Mitigation**: Index on user_id, compound indexes for filtering + sorting
- **Concurrent load**: 50+ users × ~10 tasks each = 500 rows; indexes ensure O(log n) scans

### Storage Estimates

- **Per task**: ~250 bytes (id, user_id, title, description, metadata)
- **100 users × 50 tasks**: 1.25 MB
- **1000 users × 100 tasks**: 25 MB
- **Storage is not a Phase II concern** (Neon supports multi-GB databases)

### Connection Pool

- **Async connections**: Neon's serverless pooling handles 50+ concurrent requests
- **No connection exhaustion**: asyncpg + Neon's pooling prevents leaks
- **Timeout**: Queries > 30s trigger timeout (adjust if needed for bulk operations)

---

## Migration Path (Future)

### From Phase I (In-Memory)

1. **Dump Phase I data** (if any): Extract task JSON, map to new schema
2. **Create PostgreSQL schema**: Run migration scripts
3. **Load Phase I data**: Insert into new tables with user_id = "phase1-user"
4. **Verify**: Test queries filter correctly

### To Phase III (Advanced Features)

- Row-Level Security (RLS) policies in PostgreSQL
- Soft deletes (add deleted_at column)
- Task sharing (new table: task_shares linking users to tasks)
- Tags/categories (new table: task_tags)

---

## Implementation Checklist

- [ ] SQLModel Task class created with all fields and indexes
- [ ] Pydantic TaskCreate and TaskUpdate schemas with validation
- [ ] Pydantic Task response schema with from_attributes=True
- [ ] Migration script creates tasks table with constraints
- [ ] Foreign key constraint references Better Auth user table
- [ ] Compound indexes on (user_id, created_at) and (user_id, completed)
- [ ] All routes filter queries by user_id
- [ ] created_at and user_id are immutable (not in PUT/PATCH endpoints)
- [ ] Tests verify cross-user queries return 404
- [ ] Database timestamps tested for UTC correctness

---

**Next**: Quickstart guide and OpenAPI contracts (Phase 1 completion). Then proceed to `/sp.tasks` for implementation planning.
