"""Business logic for task management.

This module contains pure functions for CRUD operations on tasks.
Task schema: {'id': int, 'title': str, 'description': str, 'complete': bool}

All functions validate inputs and raise ValueError for invalid operations.
No print statements here - all user feedback is handled in main.py.
"""


def get_task(tasks: list[dict], task_id: int) -> dict | None:
    """Find a task by ID.

    Args:
        tasks: List of task dictionaries
        task_id: ID of the task to find

    Returns:
        Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None


def add_task(tasks: list[dict], title: str, description: str = "") -> None:
    """Add a new task to the list.

    Args:
        tasks: List of task dictionaries to modify
        title: Task title (required, non-empty)
        description: Task description (optional)

    Raises:
        ValueError: If title is empty or whitespace-only
    """
    if not title or not title.strip():
        raise ValueError("Title cannot be empty.")

    title = title.strip()
    description = description.strip() if description else ""

    next_id = max((t['id'] for t in tasks), default=0) + 1

    task = {
        'id': next_id,
        'title': title,
        'description': description,
        'complete': False
    }
    tasks.append(task)
    print(f"Task {next_id} added.")


def list_tasks(tasks: list[dict]) -> str:
    """Return a formatted table of all tasks.

    Args:
        tasks: List of task dictionaries

    Returns:
        Formatted string with task table or empty message
    """
    if not tasks:
        return "No tasks yet. Add one with the 'add' command."

    header = f"{'ID':<5} | {'Title':<30} | {'Description':<40} | Status"
    separator = "=" * 85

    lines = [header, separator]

    for task in tasks:
        status = "[x]" if task['complete'] else "[ ]"
        title = task['title'][:30].ljust(30)
        description = task['description'][:40].ljust(40)
        line = f"{task['id']:<5} | {title} | {description} | {status}"
        lines.append(line)

    return "\n".join(lines)


def update_task(tasks: list[dict], task_id: int, title: str = "", description: str = "") -> None:
    """Update a task's title and/or description.

    Args:
        tasks: List of task dictionaries to modify
        task_id: ID of task to update
        title: New title (if provided, must be non-empty)
        description: New description (if provided)

    Raises:
        ValueError: If task not found or title is empty
    """
    task = get_task(tasks, task_id)
    if not task:
        raise ValueError(f"Task ID {task_id} not found.")

    if title:
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        task['title'] = title.strip()

    if description is not None:
        task['description'] = description.strip()

    print(f"Task {task_id} updated.")


def delete_task(tasks: list[dict], task_id: int) -> None:
    """Delete a task by ID.

    Args:
        tasks: List of task dictionaries to modify
        task_id: ID of task to delete

    Raises:
        ValueError: If task not found
    """
    task = get_task(tasks, task_id)
    if not task:
        raise ValueError(f"Task ID {task_id} not found.")

    tasks.remove(task)
    print(f"Task {task_id} deleted.")


def mark_complete(tasks: list[dict], task_id: int) -> None:
    """Mark a task as complete.

    Args:
        tasks: List of task dictionaries to modify
        task_id: ID of task to mark complete

    Raises:
        ValueError: If task not found
    """
    task = get_task(tasks, task_id)
    if not task:
        raise ValueError(f"Task ID {task_id} not found.")

    task['complete'] = True
    print(f"Task {task_id} marked complete.")


def mark_incomplete(tasks: list[dict], task_id: int) -> None:
    """Mark a task as incomplete.

    Args:
        tasks: List of task dictionaries to modify
        task_id: ID of task to mark incomplete

    Raises:
        ValueError: If task not found
    """
    task = get_task(tasks, task_id)
    if not task:
        raise ValueError(f"Task ID {task_id} not found.")

    task['complete'] = False
    print(f"Task {task_id} marked incomplete.")
