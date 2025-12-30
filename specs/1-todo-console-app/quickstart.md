# Quick Start: Phase I TODO Application

**Feature**: Phase I - Todo In-Memory Python Console App
**Date**: 2025-12-30
**Audience**: Developers and end-users getting started with the application

---

## Installation & Setup

### Prerequisites

- **Python 3.13+** installed on your system
- **UV** package manager installed ([install UV](https://docs.astral.sh/uv/))

### Project Setup

1. **Clone or navigate to the repository**:
   ```bash
   cd /path/to/todo-app
   ```

2. **Verify Python version**:
   ```bash
   python --version
   # Output: Python 3.13.x (or higher)
   ```

3. **Verify UV is installed**:
   ```bash
   uv --version
   # Output: uv 0.x.x
   ```

4. **(Optional) Create a virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Installation Complete ✅

No external dependencies to install—the application uses only Python's standard library. The project is ready to run.

---

## Running the Application

### Method 1: Using UV (Recommended)

```bash
uv run src/main.py
```

This command:
- Resolves the Python environment
- Runs `src/main.py` directly
- Starts the TODO application

### Method 2: Using Python Module Syntax

```bash
python -m src.main
```

This command:
- Imports and executes the `src.main` module
- Requires the current directory to be the repository root

### Method 3: Direct Python Execution

```bash
python src/main.py
```

This command:
- Executes the file directly
- Works if Python is in your PATH

**Expected Output**:
```
Welcome to TODO!
Enter command (add/list/update/delete/mark/exit):
```

---

## Quick Walkthrough

### Start the Application

```bash
uv run src/main.py
```

### 1. Add Your First Task

```
Enter command (add/list/update/delete/mark/exit): add
Title: Buy groceries
Description: Milk, bread, eggs
Task 1 added.
```

### 2. Add Another Task

```
Enter command (add/list/update/delete/mark/exit): add
Title: Write project report
Description: Q4 summary and findings
Task 2 added.
```

### 3. View All Tasks

```
Enter command (add/list/update/delete/mark/exit): list

ID | Title | Description | Status
=====================================
1  | Buy groceries | Milk, bread, eggs | [ ]
2  | Write project report | Q4 summary and findings | [ ]
```

### 4. Mark a Task Complete

```
Enter command (add/list/update/delete/mark/exit): mark 1
Task 1 marked complete.
```

### 5. View Updated List

```
Enter command (add/list/update/delete/mark/exit): list

ID | Title | Description | Status
=====================================
1  | Buy groceries | Milk, bread, eggs | [x]
2  | Write project report | Q4 summary and findings | [ ]
```

### 6. Update a Task

```
Enter command (add/list/update/delete/mark/exit): update 2
New title: Write project report and present
New description: Q4 summary, findings, and presentation
Task 2 updated.
```

### 7. Delete a Task

```
Enter command (add/list/update/delete/mark/exit): delete 1
Task 1 deleted.
```

### 8. View Final List

```
Enter command (add/list/update/delete/mark/exit): list

ID | Title | Description | Status
=====================================
2  | Write project report and present | Q4 summary, findings, and presentation | [ ]
```

### 9. Exit Gracefully

```
Enter command (add/list/update/delete/mark/exit): exit
Goodbye!
```

---

## Command Reference

### Quick Command Summary

| Command | Syntax | Description |
|---------|--------|-------------|
| **add** | `add` | Create a new task (prompts for title and description) |
| **list** | `list` | Display all tasks in a formatted table |
| **update** | `update <id>` | Edit an existing task's title/description |
| **delete** | `delete <id>` | Remove a task from the list |
| **mark** | `mark <id>` | Toggle task completion status (incomplete → complete or vice versa) |
| **exit** | `exit` or `quit` | Exit the application gracefully |
| **help** | `help` | (Optional) Display available commands |

### Detailed Command Examples

#### 1. Add a Task

```
Command: add
Input prompt: Title: <enter task title>
Input prompt: Description: <enter task description (optional)>
Output: Task <id> added.
```

**Example**:
```
add
Title: Exercise
Description: 30-minute run
Task 3 added.
```

#### 2. List All Tasks

```
Command: list
Output: Formatted table with columns: ID | Title | Description | Status
```

**Example Output**:
```
ID | Title | Description | Status
=====================================
1  | Study Python | Read chapter 3 | [ ]
2  | Exercise | 30-minute run | [x]
3  | Grocery shopping | Milk, eggs | [ ]
```

**If list is empty**:
```
No tasks yet. Add one with the 'add' command.
```

#### 3. Update a Task

```
Command: update <id>
Input prompt: New title: <enter updated title (or leave blank to skip)>
Input prompt: New description: <enter updated description (or leave blank to skip)>
Output: Task <id> updated.
```

**Example**:
```
update 2
New title: Extended exercise
New description: 45-minute run + stretching
Task 2 updated.
```

#### 4. Delete a Task

```
Command: delete <id>
Output: Task <id> deleted.
```

**Example**:
```
delete 1
Task 1 deleted.
```

#### 5. Mark Task Complete/Incomplete

```
Command: mark <id>
Output: Task <id> marked complete. (if was incomplete)
   OR: Task <id> marked incomplete. (if was complete)
```

**Example**:
```
mark 2
Task 2 marked complete.

mark 2
Task 2 marked incomplete.
```

#### 6. Exit Application

```
Command: exit (or quit)
Output: Goodbye!
Program terminates.
```

**Example**:
```
exit
Goodbye!
```

---

## Input Validation & Error Messages

### Common Errors & Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `"Title cannot be empty."` | User submitted blank/whitespace title on `add` | Enter a non-empty title |
| `"Task ID <id> not found."` | Tried to update/delete/mark non-existent task | Verify task ID with `list` command |
| `"Invalid task ID. Please provide a positive integer."` | Task ID argument is not a valid integer | Use numeric task IDs only (e.g., `mark 1` not `mark one`) |
| `"Please provide a task ID to [action]."` | Command issued without required task ID | Include task ID (e.g., `delete 2`) |
| `"Unknown command. Type 'add', 'list', 'update', 'delete', 'mark', or 'exit'."` | Unrecognized command entered | Check command spelling and list available commands |
| `"No tasks to [action]. Add one with the 'add' command."` | Tried to update/delete/mark on empty list | Create tasks first with `add` command |

### Input Tips

- **Commands are case-insensitive**: `ADD`, `Add`, `add` all work
- **Whitespace is trimmed**: Leading/trailing spaces are removed automatically
- **Task IDs are numeric**: Use integers only (1, 2, 3, etc.)
- **Titles cannot be empty**: At least one non-whitespace character required
- **Descriptions are optional**: Can be empty (just press Enter)
- **Long text is accepted**: Descriptions and titles can be 500+ characters

---

## Application Scope & Limitations

### What This Application Does ✅

- Store tasks in memory during a single session
- Add, view, update, delete, and mark tasks complete
- Display tasks in a formatted table
- Validate user input and provide friendly error messages
- Gracefully exit when requested

### What This Application Does NOT Do ❌

- **Persist data**: Tasks are lost when you exit (no save/load feature)
- **Multi-user support**: Single interactive user per session
- **Advanced features**: No filtering, sorting, search, priorities, due dates, or categories
- **Undo/Redo**: Deleted tasks cannot be recovered
- **Concurrent access**: Not designed for simultaneous users

### Phase I Scope

This is **Phase I** (MVP) of the TODO application. It provides the core CRUD functionality for learning and foundational use. Future phases may add persistence, additional features, and UI enhancements.

---

## Troubleshooting

### Issue: `python: command not found` or `python version < 3.13`

**Solution**:
- Install Python 3.13+ from [python.org](https://www.python.org/downloads/)
- Verify installation: `python --version`

### Issue: `uv: command not found`

**Solution**:
- Install UV: Follow instructions at [astral.sh/uv](https://docs.astral.sh/uv/)
- Verify installation: `uv --version`

### Issue: `ModuleNotFoundError: No module named 'src'`

**Solution**:
- Ensure you're running from the repository root directory: `cd /path/to/todo-app`
- Run with UV: `uv run src/main.py`

### Issue: Commands not recognized or strange output

**Solution**:
- Ensure you're in the command loop (after running the app)
- Check command spelling: `add`, `list`, `update`, `delete`, `mark`, `exit`
- Press Enter after typing a command

---

## Next Steps

1. **Run the app** and complete the Quick Walkthrough above
2. **Experiment with all commands** (add, list, update, delete, mark, exit)
3. **Test edge cases** (invalid IDs, empty titles, rapid commands)
4. **Review the code** in `src/main.py` and `src/todo_manager.py` to understand the implementation
5. **Read the specification** at `specs/1-todo-console-app/spec.md` for detailed requirements
6. **Read the architecture plan** at `specs/1-todo-console-app/plan.md` for design decisions

---

## Support

For questions or issues:
1. Check the **Troubleshooting** section above
2. Review the **Command Reference** for command syntax
3. Read the **Feature Specification** at `specs/1-todo-console-app/spec.md`
4. Check the **Implementation Plan** at `specs/1-todo-console-app/plan.md`

Enjoy using the TODO application!
