# Python TODO Application Constitution

<!-- Specification Constitution for a basic in-memory TODO console app in Python 3.13+ -->

## Core Principles

### I. Simplicity and Minimalism

Every implementation decision prioritizes simplicity: in-memory storage only (no database),
standard library exclusively (no external dependencies except UV for project management),
and straightforward data structures (task list of dictionaries). Code must avoid unnecessary
abstractions—dictionaries suffice; no classes unless functionally required. This principle
ensures the codebase remains beginner-friendly and maintainable.

**Rationale**: Reduces cognitive load, minimizes security surface, and aligns with educational
goals. Complex abstractions introduce maintenance burden without proportional benefit.

### II. Modular Code Organization

Code is organized into two distinct modules: `todo_manager.py` handles core task logic
(CRUD operations, validation), and `main.py` provides the CLI interface and command loop.
Each module has a single responsibility; functions are small and testable in isolation.
No cross-file duplication; common operations are factored into dedicated functions.

**Rationale**: Separation of concerns enables independent testing, easier debugging, and
clear responsibility boundaries. Teams can work on different modules without interference.

### III. Type Safety and Clean Code

All functions include type hints (e.g., `def add_task(tasks: list[dict], title: str) -> None`).
Code follows PEP 8: 4-space indentation, 79-character line limit, snake_case naming.
Variables and functions use meaningful names—no abbreviations (use `task_id`, not `tid`).
Docstrings required for all functions; comments only for non-obvious logic.
Error handling raises `ValueError` for invalid inputs with user-friendly messages.

**Rationale**: Type hints enable static analysis and catch bugs early. PEP 8 compliance
ensures consistency across the Python ecosystem. Meaningful names and docstrings reduce
onboarding time and support long-term maintainability.

### IV. Validated User Input and Error Handling

All user inputs are validated at entry points: required fields checked (non-empty title),
existing IDs verified before update/delete operations, and command format validated.
Invalid input raises `ValueError` with descriptive messages printed to the user.
Edge cases (empty task list, invalid IDs, duplicate operations) are handled explicitly.

**Rationale**: Input validation prevents data corruption and provides defensive guarantees
to downstream code. User-friendly error messages reduce support burden and improve UX.

### V. In-Memory Task Storage

Tasks are stored as a Python list of dictionaries with fixed schema:
`{'id': int, 'title': str, 'description': str, 'complete': bool}`.
IDs auto-increment starting from 1. No persistence layer (sessions are ephemeral).
This design is sufficient for console-based learning applications and allows
straightforward testing without test infrastructure.

**Rationale**: In-memory storage eliminates external dependencies, database complexity,
and operational overhead. Suitable for educational use and small-scale console apps.
Auto-increment IDs ensure uniqueness without manual management.

### VI. CLI and Minimal Command Parsing

The CLI loop accepts commands via `input()` or `sys.argv`: `add`, `list`, `update`,
`delete`, `mark`, `exit`. No argparse or external CLI libraries—simple string splitting
suffices. Commands are case-insensitive; unclear commands prompt for clarification.
On `exit`, print a goodbye message and terminate gracefully.

**Rationale**: Minimal parsing keeps the code beginner-friendly and dependency-free.
Simple string-based commands are intuitive for console users. Graceful exit improves UX.

### VII. Formatted Output and Readability

Tasks are displayed in a formatted table-like string (e.g., `ID | Title | Description | Status`).
Status uses `[x]` for complete, `[ ]` for incomplete. Column alignment and spacing ensure
easy scanning. Each command produces clear, human-readable feedback (success messages,
error explanations, confirmation prompts).

**Rationale**: Well-formatted output reduces errors during manual testing and provides
professional UX. Consistent status notation (`[x]` vs `[ ]`) is intuitive and aligns with
common TODO list conventions.

## Implementation Standards

### Function Signature Convention

All functions in `todo_manager.py` follow this pattern:
- First parameter: `tasks: list[dict]` (mutable task list)
- Subsequent parameters: domain-specific inputs (title, id, etc.)
- Return type: `None` (side-effect based) or appropriate value (query-based)
- Docstring: one-line summary, optional parameter/return description if non-obvious

### Validation Pattern

For each user input operation:
1. Check required fields are non-empty (title required for add)
2. Validate ID exists (for update, delete, mark)
3. Verify no duplicate IDs on new task creation
4. Raise `ValueError` with user-friendly message if validation fails

### Testing Approach

Code is manually testable in the console without external test frameworks:
- `add` creates task and prints success
- `list` displays all tasks with proper formatting
- `update` modifies an existing task
- `delete` removes a task and confirms
- `mark` toggles task completion status
- `exit` terminates cleanly

Developers verify functionality by running the app and executing each command.

## Code Structure

### Directory Layout

```
todo-app/
├── .specify/
│   ├── memory/
│   │   └── constitution.md           # This file
│   └── templates/
├── src/
│   ├── main.py                       # CLI entry point, command loop
│   └── todo_manager.py               # Core task logic (CRUD, validation)
├── CLAUDE.md                         # Agent-specific guidance
├── README.md                         # User documentation
└── pyproject.toml                    # UV project config (Python 3.13+)
```

### Module Responsibilities

**`src/todo_manager.py`**:
- `add_task(tasks, title, description) -> None`: Create new task
- `list_tasks(tasks) -> str`: Format tasks for display
- `update_task(tasks, task_id, title, description) -> None`: Modify task
- `delete_task(tasks, task_id) -> None`: Remove task
- `mark_complete(tasks, task_id) -> None`: Toggle completion
- `mark_incomplete(tasks, task_id) -> None`: Toggle incompletion
- `get_task(tasks, task_id) -> dict`: Retrieve task by ID (internal helper)

**`src/main.py`**:
- `if __name__ == "__main__": main()` entry point
- `main()`: Command loop accepting user input
- Parse commands and delegate to `todo_manager` functions
- Handle and display results/errors

## Governance

### Amendment Procedure

This constitution is binding for all code contributions. Changes to this document require:
1. Explicit justification (why the change improves the project)
2. Impact assessment (which code/templates are affected)
3. Update dependent templates if principles or constraints change
4. Version bump following semantic versioning

### Principle Compliance Review

All code PRs must verify alignment with these seven principles:
- Simplicity (no external deps, in-memory only)
- Modularity (clear separation of concerns)
- Type safety and clean code (type hints, PEP 8, meaningful names)
- Input validation (no invalid states possible)
- Storage design (list of dicts, auto-increment IDs)
- CLI implementation (minimal parsing, graceful commands)
- Output formatting (human-readable, consistent status notation)

### Development Workflow

Use this constitution as the lens for all design and implementation discussions.
If a proposal violates a principle, surface it explicitly: "This violates Principle II
(Modularity)" or "This adds external dependency, violating Principle I (Simplicity)."

Treat principles as hard constraints, not guidelines. Exceptions require documented
justification in a commit message or ADR.

## Version and History

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-29

### Rationale for v1.0.0

Initial constitution for the Python TODO application project. Establishes seven core
principles focused on simplicity, modularity, type safety, validation, in-memory storage,
minimal CLI, and formatted output. Principles are derived from the project brief and
reflect best practices for beginner-friendly console applications.
