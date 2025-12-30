"""CLI entry point for the Todo Console Application.

This module contains the main command loop, input handling, and user interface.
All business logic is delegated to todo_manager.py functions.
"""

from src import todo_manager


def _parse_task_id(task_id_str: str) -> int | None:
    """Parse and validate a task ID from string input.

    Args:
        task_id_str: String representation of task ID

    Returns:
        Parsed integer ID if valid, None otherwise
    """
    try:
        task_id = int(task_id_str)
        if task_id <= 0:
            print("Invalid task ID. Please provide a positive integer.")
            return None
        return task_id
    except ValueError:
        print("Invalid task ID. Please provide a positive integer.")
        return None


def _handle_add(tasks: list[dict]) -> None:
    """Handle the 'add' command - create a new task."""
    title = input("Enter task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    description = input("Enter task description (optional): ").strip()

    try:
        todo_manager.add_task(tasks, title, description)
    except ValueError as e:
        print(f"Error: {e}")


def _handle_list(tasks: list[dict]) -> None:
    """Handle the 'list' command - display all tasks."""
    output = todo_manager.list_tasks(tasks)
    print(output)


def _handle_mark(tasks: list[dict], command_parts: list[str]) -> None:
    """Handle the 'mark' command - toggle task completion status."""
    if len(command_parts) < 2:
        print("Please provide a task ID to mark.")
        return

    task_id = _parse_task_id(command_parts[1])
    if task_id is None:
        return

    try:
        task = todo_manager.get_task(tasks, task_id)
        if not task:
            print(f"Task ID {task_id} not found.")
            return

        if task['complete']:
            todo_manager.mark_incomplete(tasks, task_id)
        else:
            todo_manager.mark_complete(tasks, task_id)
    except ValueError as e:
        print(f"Error: {e}")


def _handle_update(tasks: list[dict], command_parts: list[str]) -> None:
    """Handle the 'update' command - modify task title/description."""
    if len(command_parts) < 2:
        print("Please provide a task ID to update.")
        return

    task_id = _parse_task_id(command_parts[1])
    if task_id is None:
        return

    if not todo_manager.get_task(tasks, task_id):
        print(f"Task ID {task_id} not found.")
        return

    title = input("Enter new title (press Enter to keep current): ").strip()
    description = input("Enter new description (press Enter to keep current): ").strip()

    if not title and not description:
        print("No changes made.")
        return

    try:
        todo_manager.update_task(tasks, task_id, title, description)
    except ValueError as e:
        print(f"Error: {e}")


def _handle_delete(tasks: list[dict], command_parts: list[str]) -> None:
    """Handle the 'delete' command - remove a task."""
    if len(command_parts) < 2:
        print("Please provide a task ID to delete.")
        return

    task_id = _parse_task_id(command_parts[1])
    if task_id is None:
        return

    try:
        todo_manager.delete_task(tasks, task_id)
    except ValueError as e:
        print(f"Error: {e}")


def main() -> None:
    """Main entry point - command loop for the todo application."""
    print("Welcome to TODO! Type 'help' for available commands.")

    tasks: list[dict] = []

    while True:
        try:
            user_input = input("Enter command (add/list/update/delete/mark/exit): ").strip()

            if not user_input:
                continue

            command_parts = user_input.lower().split()
            command = command_parts[0] if command_parts else None

            if command == "exit" or command == "quit":
                print("Goodbye!")
                break
            elif command == "help":
                print("Available commands:")
                print("  add        - Add a new task")
                print("  list       - View all tasks")
                print("  mark ID    - Mark task complete/incomplete")
                print("  update ID  - Update task title/description")
                print("  delete ID  - Delete a task")
                print("  exit       - Exit the application")
            elif command == "add":
                _handle_add(tasks)
            elif command == "list":
                _handle_list(tasks)
            elif command == "mark":
                _handle_mark(tasks, command_parts)
            elif command == "update":
                _handle_update(tasks, command_parts)
            elif command == "delete":
                _handle_delete(tasks, command_parts)
            else:
                print("Unknown command. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
