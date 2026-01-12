---
name: Update Task
description: Updates task details.
---

# Update Task Skill

Parameters: user_id (req), task_id (req), title (opt), description (opt).

Output: {"task_id": int, "status": "updated", "title": str}

DB Operation: Update where id == ? and user_id == ?