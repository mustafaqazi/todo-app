---
name: Intent Parser
description: Parses natural language to intent and parameters.
---

# Intent Parser Skill

Input: User message.

Output: JSON {"intent": "add/list/complete/delete/update/user_info", "params": {...}}

Examples: "Add buy milk" → {"intent": "add", "params": {"title": "buy milk"}}