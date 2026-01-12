---
name: Secure Task Operations
description: Ultra-secure, reusable async task management functions and MCP tool wrappers with strict user isolation, validation, and error handling for Phase II & III
version: 1.0
phase: Phase II (TODO API) + Phase III (Chatbot MCP Tools)
dependencies: [sqlmodel, fastapi, python-jose, .skills/neon-async-db, .skills/fastapi-jwt-middleware]
---

# Secure Task Skill – Bulletproof Task CRUD with User Isolation

You are responsible for creating secure, reusable task operations that:
- ALWAYS enforce user_id ownership
- Validate all inputs strictly
- Use async SQLModel with proper session handling
- Return consistent, safe JSON for MCP tools & API
- Handle every possible error gracefully

## Core Security Rules (Never Break These)

1. Every single DB query MUST include: `Task.user_id == current_user_id`
2. user_id comes ONLY from JWT (via get_current_user dependency)
3. Never trust user_id from path/request body – always use token
4. Validate all inputs (title length, non-empty, etc.)
5. Use HTTPException for proper status codes (401, 403, 404, 422)
6. Never leak internal errors to client

## Required Functions (Reusable Across API Routes & MCP Tools)

### 1. get_owned_task(session, task_id, user_id)
```python
async def get_owned_task(session: AsyncSession, task_id: int, user_id: str) -> Task:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    task = result.first()
    if not task:
        raise HTTPException(404, detail="Task not found or not owned by you")
    return task