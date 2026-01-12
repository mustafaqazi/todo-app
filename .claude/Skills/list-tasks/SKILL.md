---
name: List Tasks
description: Lists user's tasks with filter.
---

# List Tasks Skill

Parameters: user_id (req), status (opt: all/pending/completed).

Output: Array of {"id": int, "title": str, "completed": bool, ...}

DB Operation: Select from tasks where user_id == ? and filter.