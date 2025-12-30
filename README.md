# Todo Console Application - Phase I

A beginner-friendly, in-memory Python console TODO application with simple CRUD task management.

## Features

- ✅ **Add Tasks**: Create new tasks with title and description
- ✅ **View Tasks**: Display all tasks in a formatted table with completion status
- ✅ **Mark Complete**: Toggle task completion status
- ✅ **Update Tasks**: Edit task title and description
- ✅ **Delete Tasks**: Remove tasks from the list
- ✅ **Graceful Exit**: Clean application termination

## Installation

### Requirements

- Python 3.13 or higher
- UV (Python package manager)

### Setup

1. **Install UV** (if not already installed):
   ```bash
   pip install uv
   ```

2. **Install project dependencies** (none required for Phase I):
   ```bash
   uv venv
   ```

3. **Verify installation**:
   ```bash
   uv run src/main.py
   ```

## Usage

### Starting the Application

**Important**: Always run these commands from the **repository root**, not from the `src/` directory.

```bash
uv run src/main.py
```

Or directly with Python:

```bash
python -m src.main
```

**Example**:
```bash
cd /path/to/todo-app          # Navigate to repo root
uv run src/main.py            # Correct ✅
# NOT: cd src && uv run main.py  (this will fail) ❌
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add a new task | `add` → prompted for title/description |
| `list` | View all tasks | `list` |
| `mark <ID>` | Toggle task complete/incomplete | `mark 1` |
| `update <ID>` | Edit task title/description | `update 1` |
| `delete <ID>` | Remove a task | `delete 2` |
| `help` | Show available commands | `help` |
| `exit` | Exit application | `exit` |

### Example Workflow

```
Welcome to TODO! Type 'help' for available commands.
Enter command (add/list/update/delete/mark/exit): add
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task 1 added.

Enter command (add/list/update/delete/mark/exit): add
Enter task title: Finish project
Enter task description (optional):
Task 2 added.

Enter command (add/list/update/delete/mark/exit): list
ID    | Title                          | Description                              | Status
============================================================================
1     | Buy groceries                  | Milk, eggs, bread                        | [ ]
2     | Finish project                 |                                          | [ ]

Enter command (add/list/update/delete/mark/exit): mark 1
Task 1 marked complete.

Enter command (add/list/update/delete/mark/exit): list
ID    | Title                          | Description                              | Status
============================================================================
1     | Buy groceries                  | Milk, eggs, bread                        | [x]
2     | Finish project                 |                                          | [ ]

Enter command (add/list/update/delete/mark/exit): exit
Goodbye!
```

## Project Structure

```
todo-app/
├── src/
│   ├── __init__.py          # Package marker
│   ├── main.py              # CLI entry point and command loop
│   └── todo_manager.py      # Pure functions for task management
├── pyproject.toml           # UV project configuration
├── README.md                # This file
└── .gitignore              # Git ignore patterns
```

## Technical Details

### Architecture

- **No External Dependencies**: Uses only Python standard library (3.13+)
- **In-Memory Storage**: Tasks exist only during the application session
- **Simple CLI**: String-based command parsing, no external CLI libraries
- **Modular Design**: Clear separation between UI (main.py) and logic (todo_manager.py)

### Data Model

Each task is a dictionary with the following structure:

```python
{
    'id': int,              # Unique auto-incrementing identifier
    'title': str,           # Task title (required, non-empty)
    'description': str,     # Task description (optional)
    'complete': bool        # Completion status (default: False)
}
```

### Code Quality

- ✅ Type hints on all functions
- ✅ PEP 8 compliant (79-character line limit)
- ✅ Comprehensive docstrings
- ✅ Single responsibility principle
- ✅ Input validation with user-friendly error messages
- ✅ ~400 lines of clean, readable code

## Limitations & Scope

### Phase I Scope

This is an **educational, minimal implementation** with the following characteristics:

- **No Persistence**: Tasks are stored in memory only and lost when the application closes
- **Single User**: Designed for a single interactive user
- **No Network**: Runs locally in a console terminal
- **Manual Testing**: No automated test framework (console-based testing)
- **Limited Scale**: Suitable for <1000 tasks in a single session

### Out of Scope for Phase I

- Persistent file storage (database or file)
- Multi-user or concurrent access
- Network/API integration
- Automated testing framework
- GUI or web interface
- Advanced search/filtering

## Future Enhancements (Phase II+)

Potential improvements for future phases:

- File-based persistence (JSON, CSV)
- Task filtering and search
- Task priorities and due dates
- Categories/tags for tasks
- Undo/redo functionality
- Multi-session persistence
- Web API or GUI interface

## Development

### Running the Application

```bash
uv run src/main.py
```

### Code Structure

**main.py**: CLI loop, command parsing, user interaction
**todo_manager.py**: Pure task management functions (no print statements)

### Testing

Manual console testing per Phase I specification:

1. Launch the application
2. Execute each command manually
3. Verify output and state changes
4. Test edge cases (invalid IDs, empty fields, etc.)

### Maintenance

All code follows the **Project Constitution**:
- Simplicity & minimalism first
- Type safety with type hints
- Input validation at system boundaries
- Clear error messages
- Single responsibility per function

## Code Statistics

- **Total Lines**: ~400 (both modules combined)
- **Modules**: 2 (main.py, todo_manager.py)
- **Functions**: 8 (add, list, update, delete, mark_complete, mark_incomplete, get_task, main)
- **External Dependencies**: 0 (standard library only)

## License

Generated with Claude Code - Anthropic's official CLI for software engineering
