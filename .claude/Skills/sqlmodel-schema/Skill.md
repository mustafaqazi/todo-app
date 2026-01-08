---
name: SQLModel Schema Creator
description: Generates SQLModel table models with proper fields, indexes, relationships, and user ownership.
---

# SQLModel Schema Creator Skill

You output complete models.py entries.

## Rules
- Always include user_id: str = Field(index=True)
- Proper Field constraints (min_length, max_length)
- Timestamps: created_at, updated_at
- completed: bool default False
- Indexes on user_id and frequently filtered fields

## Example
User: "Create Task model for TODO app"
→ Full Task class with all fields and docstrings