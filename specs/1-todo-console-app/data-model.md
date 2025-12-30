# Data Model: Phase I TODO Application

**Feature**: Phase I - Todo In-Memory Python Console App
**Date**: 2025-12-30
**Source**: Feature specification + architectural design

---

## Core Entity: Task

### Schema

```python
{
    'id': int,              # Unique auto-incremented identifier (starting from 1)
    'title': str,           # Required, non-empty, single-line text
    'description': str,     # Optional, single-line text (can be empty string)
    'complete': bool        # Task completion status (default: False on creation)
}
```

### Field Descriptions

| Field | Type | Constraints | Semantics |
|-------|------|-------------|-----------|
| `id` | `int` | Auto-increment, unique, ≥ 1, immutable after creation | Globally unique task identifier within session. Assigned on creation; never reused even after deletion. |
| `title` | `str` | Required, non-empty (no whitespace-only), single-line | User-provided name/description of the task. Must be provided on creation; cannot be empty. |
| `description` | `str` | Optional (can be empty string `""`), single-line | User-provided supplementary details. May be empty; users can add later via `update`. |
| `complete` | `bool` | `True` or `False` | Completion state. Defaults to `False` on creation. Toggled via `mark complete` / `mark incomplete` commands. |

### Validation Rules

1. **ID Assignment**:
   - On creation: `next_id = max([t['id'] for t in tasks]) + 1 if tasks else 1`
   - IDs are never reused; deletion does not cause renumbering
   - IDs are immutable after assignment

2. **Title Validation**:
   - Required field; cannot be `None`
   - Cannot be empty string `""`
   - Cannot be whitespace-only (e.g., `"   "`)
   - If validation fails: raise `ValueError("Title cannot be empty.")`

3. **Description Validation**:
   - Optional field; can be empty string `""`
   - No minimum or maximum length enforced (accepts any valid Python string)
   - Long strings (500+ chars) are accepted; display wrapping is acceptable

4. **Completion State**:
   - Defaults to `False` on creation
   - Only valid values: `True` (complete) or `False` (incomplete)
   - Toggled by `mark complete` and `mark incomplete` commands

### Relationship Graph

*Phase I contains a single entity; no relationships to other entities.*

```
┌─────────────┐
│    Task     │
│             │
│  id         │
│  title      │
│  description│
│  complete   │
└─────────────┘
```

No foreign keys, no composite keys, no multi-valued attributes.

---

## In-Memory Storage

### Data Structure

All tasks are stored in a single Python `list[dict]`:

```python
tasks: list[dict] = []  # Initially empty
```

### Example State

After three commands (`add`, `add`, `mark 1`):

```python
tasks = [
    {'id': 1, 'title': 'Buy milk', 'description': 'From the grocery store', 'complete': True},
    {'id': 2, 'title': 'Write report', 'description': 'Q4 summary', 'complete': False},
]
```

### Mutation Patterns

All modifications follow these patterns:

1. **Add task**:
   ```python
   new_task = {'id': next_id, 'title': title, 'description': description, 'complete': False}
   tasks.append(new_task)
   ```

2. **Update task**:
   ```python
   task = next(t for t in tasks if t['id'] == task_id)  # or use get_task() helper
   task['title'] = new_title      # if provided
   task['description'] = new_description  # if provided
   ```

3. **Delete task**:
   ```python
   task = next(t for t in tasks if t['id'] == task_id)
   tasks.remove(task)  # or: tasks.pop(tasks.index(task))
   ```

4. **Mark complete**:
   ```python
   task['complete'] = True
   ```

5. **Mark incomplete**:
   ```python
   task['complete'] = False
   ```

6. **Query (list)**:
   ```python
   for task in tasks:  # Iterate in order (oldest first)
       print(format_task(task))
   ```

### Session Lifecycle

- **Initialization**: `tasks = []` (empty list)
- **Runtime**: Tasks added/modified/deleted in memory
- **Exit**: All tasks discarded; no persistence to disk
- **Re-run**: Fresh session starts with empty list

---

## Type Annotations

All functions in `todo_manager.py` use these type signatures:

```python
def add_task(tasks: list[dict], title: str, description: str) -> None:
    """Add a new task with auto-incremented ID."""
    ...

def list_tasks(tasks: list[dict]) -> str:
    """Return formatted table of all tasks."""
    ...

def get_task(tasks: list[dict], task_id: int) -> dict | None:
    """Retrieve task by ID; return None if not found."""
    ...

def update_task(tasks: list[dict], task_id: int, title: str, description: str) -> None:
    """Update task title and/or description."""
    ...

def delete_task(tasks: list[dict], task_id: int) -> None:
    """Remove task by ID."""
    ...

def mark_complete(tasks: list[dict], task_id: int) -> None:
    """Mark task as complete."""
    ...

def mark_incomplete(tasks: list[dict], task_id: int) -> None:
    """Mark task as incomplete."""
    ...
```

All functions accept `tasks` as the first parameter (mutable list) and modify in-place or return computed values.

---

## State Transitions

### Task Lifecycle

```
[Creation]
   |
   v
Incomplete [ ] ------> Complete [x]
   ^                        |
   |                        v
   +------- Toggle --------+

[Deletion]
   |
   v
Removed (not persisted)
```

**Transitions**:
- **New → Incomplete**: Default state on `add_task()`
- **Incomplete ↔ Complete**: Toggled via `mark_complete()` / `mark_incomplete()`
- **Any → Deleted**: Via `delete_task()` (immediate removal, no recovery)
- **Update**: Title/description can change at any state via `update_task()`

---

## Constraints & Edge Cases

### Uniqueness Constraints

| Field | Constraint | Enforcement |
|-------|-----------|------------|
| `id` | Unique across all tasks | ID auto-increment logic ensures uniqueness; no manual ID assignment |
| `title` | Non-unique (multiple tasks can have same title) | No constraint |
| `description` | Non-unique | No constraint |

### Size & Performance

- **Task list size**: Phase I designed for <1000 tasks; no pagination/optimization
- **ID assignment**: O(n) scan per add (acceptable for scope)
- **Query operations**: O(n) to find task by ID (linear search acceptable for Phase I)
- **Memory**: All tasks in memory; no external storage

### Empty/Null Handling

| Scenario | Handling |
|----------|----------|
| Empty task list | `list_tasks()` returns "No tasks yet" message |
| Task with empty description | Valid state; displayed as blank in table |
| ID lookup on non-existent task | Raise `ValueError` (caught in main loop) |
| Empty title on add | Raise `ValueError` (validation in add_task) |

---

## Display Format

### List View

```
ID | Title | Description | Status
=====================================
1  | Buy milk | From the grocery store | [x]
2  | Write report | Q4 summary | [ ]
```

- Status notation: `[x]` = complete, `[ ]` = incomplete
- Columns are separated by ` | ` (pipe with spaces)
- Fields are left-aligned with padding for readability
- Long text wraps naturally within terminal width

---

## Evolution & Future Phases

*Phase I is foundational; future phases may extend this model.*

**Potential Phase II extensions** (out of scope for Phase I):
- Persistence (save/load from file)
- Due dates or priority levels
- Task categories/tags
- Task relationships (sub-tasks, dependencies)
- Filtering/sorting options
- Search functionality

**Backward compatibility**: Phase II will maintain the core task schema (id, title, description, complete) and extend with new optional fields.
