# CLI Command Contracts

**Feature**: Phase I - Todo In-Memory Python Console App
**Date**: 2025-12-30
**Purpose**: Formal specification of command syntax, arguments, return values, and error cases

---

## Command Dispatcher Interface

All commands are dispatched from the main REPL loop via simple string parsing:

```python
command = input("Enter command: ").lower().split()
dispatcher = {
    'add': handle_add,
    'list': handle_list,
    'update': handle_update,
    'delete': handle_delete,
    'mark': handle_mark,
    'exit': handle_exit,
    'quit': handle_exit,
    'help': handle_help,
}
```

---

## Command Specifications

### 1. ADD: Create a New Task

**Contract**:
```
COMMAND: add
SYNTAX:  add
ARGS:    (none from CLI; prompted interactively)
RETURN:  String message "Task <id> added." (printed to stdout)
RAISES:  ValueError("Title cannot be empty.") if title validation fails
```

**Behavior**:

1. **Prompt for input**:
   - Prompt: `"Title: "` → Await user input
   - Validate: Title non-empty (strip whitespace); raise `ValueError` if empty
   - Prompt: `"Description: "` → Await user input (can be empty)

2. **Create task**:
   - Compute next ID: `max([t['id'] for t in tasks]) + 1 if tasks else 1`
   - Create dict: `{'id': next_id, 'title': title, 'description': description, 'complete': False}`
   - Append to `tasks` list

3. **Confirm**:
   - Print: `"Task {next_id} added."` (where `next_id` is the assigned ID)

**Error Cases**:
- Empty title (whitespace-only): `ValueError("Title cannot be empty.")`
- Handled in main loop: Catch exception, print error, re-prompt

**Idempotency**: Not idempotent; each invocation creates a new task with incremented ID.

**Example**:
```
> add
Title: Buy milk
Description: From the grocery store
Task 1 added.

> add
Title: Finish report
Description:
Task 2 added.
```

---

### 2. LIST: View All Tasks

**Contract**:
```
COMMAND: list
SYNTAX:  list
ARGS:    (none)
RETURN:  String containing formatted table of all tasks
         Empty list message: "No tasks yet. Add one with the 'add' command."
RAISES:  (none; always succeeds)
```

**Behavior**:

1. **Check empty list**:
   - If `len(tasks) == 0`, return: `"No tasks yet. Add one with the 'add' command."`

2. **Format output**:
   - Header row: `"ID | Title | Description | Status"`
   - Separator: `"=" * 80` or similar
   - For each task (in order, oldest first):
     - Format: `f"{task['id']:<5} | {task['title']:<30} | {task['description']:<40} | {status}"`
     - Status: `"[x]"` if `task['complete'] == True`, else `"[ ]"`

3. **Return**:
   - Print formatted string to stdout

**Error Cases**:
- None; always succeeds (empty list shows helpful message)

**Idempotency**: Idempotent; no state changes.

**Example**:
```
> list

ID | Title | Description | Status
=====================================
1  | Buy milk | From the grocery store | [x]
2  | Finish report |  | [ ]

> list
No tasks yet. Add one with the 'add' command.
```

---

### 3. UPDATE: Modify Task Title/Description

**Contract**:
```
COMMAND: update
SYNTAX:  update <task_id>
ARGS:    task_id (integer, positional argument)
RETURN:  String message "Task {task_id} updated." (printed to stdout)
RAISES:  ValueError("Task ID {task_id} not found.") if task_id does not exist
         ValueError("Invalid task ID. Please provide a positive integer.") if task_id not integer
```

**Behavior**:

1. **Validate arguments**:
   - Ensure task_id provided (if not, prompt: `"Please provide a task ID to update."`)
   - Ensure task_id is integer (parse from string); raise `ValueError` if not

2. **Find task**:
   - Search for task with `id == task_id`; raise `ValueError` if not found

3. **Prompt for updates**:
   - Prompt: `"New title (or blank to skip): "` → If provided, validate non-empty; update task
   - Prompt: `"New description (or blank to skip): "` → If provided, update task (can be empty)

4. **Confirm**:
   - Print: `"Task {task_id} updated."`

**Error Cases**:
- Task ID not provided: `"Please provide a task ID to update."`
- Task ID not integer: `ValueError("Invalid task ID. Please provide a positive integer.")`
- Task ID not found: `ValueError("Task ID {task_id} not found.")`
- New title empty (if provided): `ValueError("Title cannot be empty.")`

**Idempotency**: Idempotent if same input; if re-run, overwrites with same values.

**Example**:
```
> update 1
New title (or blank to skip): Buy milk and bread
New description (or blank to skip): From the grocery store
Task 1 updated.

> update 1
New title (or blank to skip):
New description (or blank to skip): From the market
Task 1 updated.
```

---

### 4. DELETE: Remove a Task

**Contract**:
```
COMMAND: delete
SYNTAX:  delete <task_id>
ARGS:    task_id (integer, positional argument)
RETURN:  String message "Task {task_id} deleted." (printed to stdout)
RAISES:  ValueError("Task ID {task_id} not found.") if task_id does not exist
         ValueError("Invalid task ID. Please provide a positive integer.") if task_id not integer
```

**Behavior**:

1. **Validate arguments**:
   - Ensure task_id provided (if not, prompt: `"Please provide a task ID to delete."`)
   - Ensure task_id is integer; raise `ValueError` if not

2. **Find and remove task**:
   - Search for task with `id == task_id`; raise `ValueError` if not found
   - Remove task from `tasks` list: `tasks.remove(task)` or `tasks.pop(index)`

3. **Confirm**:
   - Print: `"Task {task_id} deleted."`

**Error Cases**:
- Task ID not provided: `"Please provide a task ID to delete."`
- Task ID not integer: `ValueError("Invalid task ID. Please provide a positive integer.")`
- Task ID not found: `ValueError("Task ID {task_id} not found.")`

**Idempotency**: Not idempotent; second invocation fails (task already deleted).

**Example**:
```
> delete 1
Task 1 deleted.

> delete 1
ValueError("Task ID 1 not found.")
```

---

### 5. MARK: Toggle Task Completion Status

**Contract**:
```
COMMAND: mark
SYNTAX:  mark <task_id>
ARGS:    task_id (integer, positional argument)
RETURN:  String message "Task {task_id} marked complete." or "Task {task_id} marked incomplete." (printed to stdout)
RAISES:  ValueError("Task ID {task_id} not found.") if task_id does not exist
         ValueError("Invalid task ID. Please provide a positive integer.") if task_id not integer
```

**Behavior**:

1. **Validate arguments**:
   - Ensure task_id provided (if not, prompt: `"Please provide a task ID to mark."`)
   - Ensure task_id is integer; raise `ValueError` if not

2. **Find task and toggle**:
   - Search for task with `id == task_id`; raise `ValueError` if not found
   - Toggle: `task['complete'] = not task['complete']`

3. **Confirm**:
   - If now complete: Print `"Task {task_id} marked complete."`
   - If now incomplete: Print `"Task {task_id} marked incomplete."`

**Error Cases**:
- Task ID not provided: `"Please provide a task ID to mark."`
- Task ID not integer: `ValueError("Invalid task ID. Please provide a positive integer.")`
- Task ID not found: `ValueError("Task ID {task_id} not found.")`

**Idempotency**: Idempotent (toggle is reversible); re-run toggles back.

**Example**:
```
> mark 1
Task 1 marked complete.

> mark 1
Task 1 marked incomplete.

> mark 1
Task 1 marked complete.
```

---

### 6. EXIT: Terminate Application

**Contract**:
```
COMMAND: exit or quit
SYNTAX:  exit (or quit)
ARGS:    (none)
RETURN:  Print message "Goodbye!" and terminate program
RAISES:  (none)
```

**Behavior**:

1. **Print farewell**:
   - Print: `"Goodbye!"`

2. **Terminate**:
   - Exit the command loop and terminate the program

**Error Cases**:
- None; always succeeds

**Idempotency**: Not idempotent; once executed, program terminates.

**Example**:
```
> exit
Goodbye!
(program exits)
```

---

### 7. HELP: Display Available Commands (Optional)

**Contract**:
```
COMMAND: help
SYNTAX:  help
ARGS:    (none)
RETURN:  String message listing available commands
RAISES:  (none)
```

**Behavior**:

1. **Display help**:
   - Print list of commands with brief descriptions:
   ```
   Available commands:
   - add: Create a new task
   - list: View all tasks
   - update <id>: Edit a task
   - delete <id>: Remove a task
   - mark <id>: Toggle task completion status
   - exit (or quit): Exit the application
   - help: Display this message
   ```

**Error Cases**:
- None; always succeeds

**Idempotency**: Idempotent; no state changes.

---

## Error Handling Patterns

### Exception Propagation

All manager functions (`add_task`, `list_tasks`, `update_task`, `delete_task`, `mark_complete`, `mark_incomplete`) raise `ValueError` for validation failures.

The main command loop catches these exceptions and handles them:

```python
try:
    handler(tasks, *args)
except ValueError as e:
    print(f"Error: {str(e)}")
    continue  # Re-prompt for next command
```

### User-Friendly Error Messages

All error messages are human-readable and suggest corrective action:

| Error | Message Format |
|-------|-----------------|
| Empty title | `"Title cannot be empty."` |
| Invalid task ID (format) | `"Invalid task ID. Please provide a positive integer."` |
| Task ID not found | `"Task ID {task_id} not found."` |
| Missing required argument | `"Please provide a task ID to [action]."` |
| Unknown command | `"Unknown command. Type 'add', 'list', 'update', 'delete', 'mark', or 'exit'."` |

---

## Input Validation Rules

| Input | Rule | Example |
|-------|------|---------|
| Command | Case-insensitive; stripped of leading/trailing whitespace | `"ADD"`, `"  add  "` → `"add"` |
| Task ID | Positive integer; parsed from string argument | `"1"` → `1`; `"abc"` → `ValueError` |
| Title | Non-empty after stripping whitespace | `"   "` → `ValueError`; `"Task"` → OK |
| Description | Any string (can be empty) | `""` → OK; `"long text"` → OK |

---

## Command Loop Control Flow

```
┌─────────────────────┐
│  REPL Loop Start    │
└──────────┬──────────┘
           │
           v
   ┌───────────────────┐
   │ Prompt for input  │
   │ Parse command     │
   └────┬──────────────┘
        │
        v
   ┌────────────────┐
   │ Dispatch to    │
   │ handler        │
   └────┬───────────┘
        │
        v
   ┌─────────────────────────┐
   │ Handler executes;       │
   │ may raise ValueError    │
   └────┬────────────────────┘
        │
   ┌────v────────────────┐
   │ Catch ValueError?   │
   └────┬───────┬────────┘
        │ Yes   │ No
        │       v
        │    ┌──────────────┐
        │    │ Print result │
        │    └──────┬───────┘
        │           │
        v           v
   ┌─────────────────────────┐
   │ Exit command?           │
   │ (exit/quit)             │
   └────┬───────────┬────────┘
        │ Yes       │ No
        │           v
        │       (Loop continues)
        │
        v
   ┌──────────────┐
   │ Print "Done" │
   │ Exit program │
   └──────────────┘
```

---

## Integration Notes

- All commands integrate with a single `tasks: list[dict]` variable passed by reference
- Commands are stateless (no session state beyond task list)
- Error handling is localized to main loop; functions raise exceptions
- Output is printed to stdout; errors printed with `"Error: "` prefix
