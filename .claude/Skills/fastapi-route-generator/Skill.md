---
name: FastAPI Route Generator
description: Automatically generates complete, secure FastAPI route files for CRUD operations with JWT auth and user filtering.
---

# FastAPI Route Generator Skill

You generate ready-to-paste FastAPI route code for any resource (e.g., tasks) following project standards.

## Input
- Resource name (e.g., "tasks")
- Operations needed: list, create, get, update, delete, custom (e.g., toggle complete)

## Output
Complete `/backend/routes/{resource}.py` file with:
- Proper imports
- Pydantic schemas
- JWT dependency (get_current_user)
- User_id filtering on all queries
- All endpoints with correct HTTP methods and status codes
- Validation and error handling
- Async session dependency

## Example
User: "Generate tasks routes with CRUD and toggle complete"
→ Full tasks.py with GET /tasks, POST /tasks, PATCH /tasks/{id}/complete etc.