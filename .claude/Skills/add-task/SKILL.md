---
name: Add Task
description: Creates a new task via MCP.
---

# Add Task Skill

Parameters: user_id (req), title (req), description (opt).

Output: {"task_id": int, "status": "created", "title": str}

DB Operation: Insert into tasks with user_id.