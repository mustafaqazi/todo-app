---
name: Delete Task
description: Deletes a task.
---

# Delete Task Skill

Parameters: user_id (req), task_id (req).

Output: {"task_id": int, "status": "deleted", "title": str}

DB Operation: Delete from tasks where id == ? and user_id == ?