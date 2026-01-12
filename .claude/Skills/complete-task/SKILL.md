---
name: Complete Task
description: Toggles task complete.
---

# Complete Task Skill

Parameters: user_id (req), task_id (req).

Output: {"task_id": int, "status": "completed", "title": str}

DB Operation: Update completed = NOT completed where id == ? and user_id == ?