# Implementation Plan: Phase I - Todo In-Memory Python Console App

**Branch**: `1-todo-console-app` | **Date**: 2025-12-30 | **Spec**: `specs/1-todo-console-app/spec.md`
**Input**: User specification + architectural decisions framework from `/sp.plan` command input

**Note**: This plan document outlines the architecture, design decisions, data model, and implementation roadmap for the todo console application. All decisions are aligned with the project Constitution.

## Summary

Build a beginner-friendly, in-memory Python console TODO application (Phase I) with CRUD task management, auto-incrementing IDs, and a minimal CLI interface. The system will support adding, viewing, updating, deleting, and marking tasks complete/incomplete. All code is written in standard Python 3.13+ with no external dependencies, organized into two modules (CLI loop in `main.py`, business logic in `todo_manager.py`), and manually tested via console interaction. Design prioritizes simplicity, modularity, type safety, and validated input per the project Constitution.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only; UV for project management)
**Storage**: In-memory only (ephemeral session; no persistence to disk)
**Testing**: Manual interactive testing (no test framework required in Phase I)
**Target Platform**: Console/CLI (cross-platform via Python)
**Project Type**: Single console application
**Performance Goals**: Instant task operations (<100ms for any command), suitable for <1000 tasks in memory
**Constraints**: Standard library only, <500 lines of code across both modules, all inputs validated
**Scale/Scope**: Single-user, single-session, small task lists (educational/personal use)

## Constitution Check

*GATE: Must pass before proceeding with design. Re-checked after Phase 1 design.*

**Status**: PASS ✅ All principles satisfied.

| Principle | Requirement | Implementation | Status |
|-----------|------------|-----------------|--------|
| **I. Simplicity & Minimalism** | In-memory only, no external deps, simple data structures (dicts, no classes) | Single `tasks: list[dict]` variable, UV for project mgmt only, no frameworks | ✅ PASS |
| **II. Modularity** | Clear separation: `todo_manager.py` (logic) vs `main.py` (CLI), single responsibility per function | CRUD functions isolated in `todo_manager.py`, main loop + input handling in `main.py`, no cross-file duplication | ✅ PASS |
| **III. Type Safety & Clean Code** | Type hints on all functions, PEP 8 compliance, meaningful names, docstrings, comments for non-obvious logic | All functions typed as `def func(tasks: list[dict], ...) -> ReturnType:`, docstrings included, PEP 8 enforced | ✅ PASS |
| **IV. Input Validation** | All user inputs validated, required fields enforced, existing IDs checked, `ValueError` on invalid input | Title non-empty checks in `add_task`, ID existence validation in `update_task`/`delete_task`/`mark_*`, friendly error messages | ✅ PASS |
| **V. In-Memory Storage** | `list[dict]` schema with `id`, `title`, `description`, `complete`; auto-increment IDs starting from 1; no persistence | Task dict: `{'id': int, 'title': str, 'description': str, 'complete': bool}`, ID generation via `max([t['id'] for t in tasks]) + 1` | ✅ PASS |
| **VI. CLI & Minimal Parsing** | Simple string splitting via `input()`, case-insensitive commands, no argparse/external CLI libs, graceful exit on `exit` | Commands parsed via `input().lower().split()`, case handling in dispatcher, `exit`/`quit` triggers clean termination | ✅ PASS |
| **VII. Formatted Output** | Table-like output (ID \| Title \| Description \| Status), `[x]` complete / `[ ]` incomplete, human-readable feedback | `list_tasks()` returns formatted string with aligned columns, status notation matches spec, success/error messages explicit | ✅ PASS |

## Architectural Decisions

*Phase 0 output: Critical decisions identified for explicit documentation. All tradeoffs evaluated.*

### Decision 1: Command Input Parsing Method

**Decision**: Simple string splitting via `input().lower().split()` (no argparse)

**Rationale**:
- **Constitution Alignment**: Principle VI (Minimal CLI) mandates zero external dependencies and beginner-friendly parsing.
- **Tradeoff Analysis**:
  - ✅ **Chosen**: `input().lower().split()` + simple dispatcher: Zero dependencies, minimal code, intuitive for beginners, no learning curve for custom parsing.
  - ❌ **Sub-commands with fixed positions** (e.g., `mark complete 1`): Complex position logic, error-prone if user omits arguments, harder to extend.
  - ❌ **argparse library**: Violates Principle I (Simplicity, standard library only), adds external dependency, overkill for simple CLI.
- **Implementation**: Main loop uses dispatcher dict mapping command strings to handler functions; multi-word commands (e.g., `mark complete`) handled by checking command parts.
- **Risk**: None significant; simplicity outweighs validation benefits for Phase I educational scope.

### Decision 2: Task Storage Format

**Decision**: `list[dict]` with schema `{'id': int, 'title': str, 'description': str, 'complete': bool}`

**Rationale**:
- **Constitution Alignment**: Principle I (Simplicity) and Principle V (In-Memory Storage) mandate list of dicts, no classes.
- **Tradeoff Analysis**:
  - ✅ **Chosen**: `list[dict]`: No class definitions, minimal code, easy to inspect/debug in REPL, aligns with constitution "no classes unless functionally required."
  - ❌ **dataclass**: Slightly more type-safe but requires Python 3.10+ feature imports, adds cognitive overhead for learners.
  - ❌ **Custom Task class**: Violates Principle I (simplicity), adds encapsulation overhead, contradicts constitution guidance.
- **Implementation**: All `todo_manager.py` functions operate on `tasks: list[dict]`, mutation via list methods (`append`, `pop`, direct field assignment).
- **Risk**: None; dicts are native Python and familiar to all skill levels.

### Decision 3: ID Generation & Management

**Decision**: Resilient ID generation via `max(t['id'] for t in tasks) + 1` on each add (no separate counter)

**Rationale**:
- **Constitution Alignment**: Principle V (In-Memory Storage) specifies auto-increment IDs; no mention of persistence for counter.
- **Tradeoff Analysis**:
  - ✅ **Chosen**: `max(...) + 1` on each add: Resilient after deletions (IDs never reused), no extra state variable to synchronize, simple logic.
  - ❌ **Separate next_id counter**: Requires careful synchronization if tasks are deleted out-of-order, extra state management, higher complexity.
  - **Edge Case**: Empty list handled by `max(...) or 0` to return 0, then + 1 yields ID=1.
- **Implementation**: `add_task()` computes next ID before appending; handles empty list safely.
- **Risk**: Negligible; O(n) scan on each add is acceptable for Phase I scope (<1000 tasks).

### Decision 4: Error Handling Pattern

**Decision**: Manager functions raise `ValueError` (Pythonic exceptions caught in main loop)

**Rationale**:
- **Constitution Alignment**: Principle IV (Input Validation) and III (Type Safety) favor exception-based validation in pure functions.
- **Tradeoff Analysis**:
  - ✅ **Chosen**: Manager functions raise `ValueError` for validation failures; main loop catches and displays error message: Pythonic idiom, clean separation (validation in business logic), user-friendly error display in UI layer.
  - ❌ **Return success/error tuples**: More explicit control flow but verbose, non-Pythonic, pushes validation burden to caller, harder to trace errors.
- **Implementation**: `add_task()` raises `ValueError("Title cannot be empty.")` if title is whitespace-only; main loop catches and prints message, re-prompts user.
- **Risk**: None; exception-based error handling is Python best practice.

### Decision 5: Output Formatting for List Command

**Decision**: Manual formatted string with aligned columns (no external columnar libraries)

**Rationale**:
- **Constitution Alignment**: Principle I (standard library only) and VII (Formatted Output) require manual formatting.
- **Tradeoff Analysis**:
  - ✅ **Chosen**: Manual f-strings with padding (`f"{id:<5} | {title:<30} | {description:<40} | {status}"`): Full control, zero dependencies, aligns with constitution, readable output.
  - ❌ **Simple columnar print()**: Minimal alignment, poor UX, harder to scan large lists.
  - ❌ **External libraries** (tabulate, rich, etc.): Violates Principle I (standard library only).
- **Implementation**: `list_tasks()` returns formatted string with header + separator + rows, each row aligned to fixed column widths.
- **Risk**: Minor; very long titles/descriptions may overflow columns, but spec accepts wrapping as acceptable.

---

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-console-app/
├── plan.md              # This file (architecture, decisions, roadmap)
├── research.md          # Phase 0 output (decision rationales, best practices)
├── data-model.md        # Phase 1 output (entity schema, relationships, validation)
├── quickstart.md        # Phase 1 output (setup instructions, usage examples)
├── contracts/           # Phase 1 output (CLI command contracts)
│   ├── commands.md      # Command signatures, arguments, return values
│   └── task-schema.md   # Task entity structure and fields
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code Structure

```text
todo-app/
├── src/
│   ├── main.py          # CLI entry point, command loop, input handling
│   └── todo_manager.py  # Pure functions: add_task, list_tasks, update_task, delete_task, mark_complete, mark_incomplete, get_task
├── pyproject.toml       # UV project config (Python 3.13+, no dependencies)
├── CLAUDE.md            # Agent-specific workflow guidance
├── README.md            # User documentation (setup, run, usage)
└── .specify/
    └── memory/
        └── constitution.md  # Project principles (this defines all constraints above)
```

**Structure Decision**: Single console application (Option 1 - Simple Project) selected.
- Rationale: Phase I is a beginner-friendly educational app, no tests, no web/mobile layers. Single `src/` with two modules is sufficient and aligns with simplicity principle.
- No `tests/` directory (manual console testing per constitution).
- No external `contracts/` API servers; contracts document CLI command signatures and task schema only.

## Complexity Tracking

**Status**: PASS ✅ No Constitution violations. All complexity decisions justified.

All architectural decisions (input parsing, task storage, ID generation, error handling, output formatting) align with the seven constitutional principles. No tradeoff sacrifices core principles; all chosen approaches are simplicity-first.

---

## Implementation Roadmap

*Feature-by-feature implementation phases, dependency-ordered for testing and integration.*

### Phase 0: Setup & Project Initialization
**Deliverable**: Project structure, dependencies, skeleton code ready for implementation

- Initialize UV project with Python 3.13+ (`pyproject.toml` with no external dependencies)
- Create `/src/` directory structure with empty `main.py` and `todo_manager.py` stubs
- Create `CLAUDE.md` with agent workflow guidance
- Verify project builds/runs via `uv run src/main.py` (basic REPL prompt working)
- **Acceptance**: Project scaffold complete; `python -m src.main` exits cleanly on `exit` command

### Phase 1: Foundation & Data Model
**Deliverable**: Task data model, basic command dispatcher, function stubs in `todo_manager.py`

- Define task schema in `todo_manager.py` docstring and constants (if any)
- Implement `get_task(tasks, task_id) -> dict | None` helper (internal, used by other functions)
- Implement command dispatcher in `main()`: Parse commands from `input()`, route to handlers
- Create function stubs for all CRUD operations (raise `NotImplementedError` for now):
  - `add_task(tasks, title, description) -> None`
  - `list_tasks(tasks) -> str`
  - `update_task(tasks, task_id, title, description) -> None`
  - `delete_task(tasks, task_id) -> None`
  - `mark_complete(tasks, task_id) -> None`
  - `mark_incomplete(tasks, task_id) -> None`
- **Acceptance**: Command dispatcher recognizes all commands (add, list, update, delete, mark, exit); stubs exist with correct type hints

### Phase 2: Core Visibility Features
**Deliverable**: Users can add tasks and view the full list (foundation for testing all other features)

- Fully implement `add_task(tasks, title, description) -> None`:
  - Prompt user for title if not provided as argument
  - Validate title non-empty; raise `ValueError("Title cannot be empty.")` if whitespace-only
  - Compute next ID via `max([t['id'] for t in tasks]) + 1 if tasks else 1`
  - Append task dict to list: `{'id': next_id, 'title': title, 'description': description, 'complete': False}`
  - Print success message: `f"Task {next_id} added."`
- Fully implement `list_tasks(tasks) -> str`:
  - Return header row: `"ID | Title | Description | Status"` (with column separators)
  - If empty, return `"No tasks yet. Add one with the 'add' command."`
  - For each task, format row: `f"{task['id']:<5} | {task['title']:<30} | {task['description']:<40} | {status}"` where status is `[x]` if complete else `[ ]`
  - Include separator line for readability (optional but recommended for UX)
- Update `main()` to print `list_tasks()` output after calling handler
- **Acceptance**: Can add multiple tasks with auto-incremented IDs; list displays all tasks with correct status; empty list shows helpful message

### Phase 3: Task Modification Layer
**Deliverable**: Users can update, delete, and mark tasks complete/incomplete

- Fully implement `update_task(tasks, task_id, title, description) -> None`:
  - Find task by ID; raise `ValueError(f"Task ID {task_id} not found.")` if not found
  - If title provided, validate non-empty; update task dict
  - If description provided, update task dict
  - Print success message: `f"Task {task_id} updated."`
- Fully implement `delete_task(tasks, task_id) -> None`:
  - Find task by ID; raise `ValueError(f"Task ID {task_id} not found.")` if not found
  - Remove from list via `tasks.remove(task)` or direct index deletion
  - Print success message: `f"Task {task_id} deleted."`
- Fully implement `mark_complete(tasks, task_id) -> None`:
  - Find task by ID; raise `ValueError(f"Task ID {task_id} not found.")` if not found
  - Set `task['complete'] = True`
  - Print success message: `f"Task {task_id} marked complete."`
- Fully implement `mark_incomplete(tasks, task_id) -> None`:
  - Find task by ID; raise `ValueError(f"Task ID {task_id} not found.")` if not found
  - Set `task['complete'] = False`
  - Print success message: `f"Task {task_id} marked incomplete."`
- **Acceptance**: Can update/delete/mark existing tasks; invalid IDs raise appropriate errors; state persists across commands

### Phase 4: Input Validation & Error Handling Refinement
**Deliverable**: Robust error handling, user-friendly prompts, edge case coverage

- Add input validation in `main()`:
  - Parse task IDs from command args; validate integer format; raise `ValueError` if non-integer
  - Prompt user interactively if required arguments missing (e.g., prompt for title on `add` if not provided)
  - Catch `ValueError` from manager functions; print error message; re-prompt for next command
- Handle edge cases:
  - Empty command input (blank line) → display prompt again
  - Invalid command (e.g., `foobar`) → display "Unknown command" message + list available commands
  - Missing task ID arguments (e.g., `update` without ID) → display "Please provide a task ID"
- **Acceptance**: All edge cases from spec handled gracefully; error messages friendly and actionable

### Phase 5: Output Formatting & UX Polish
**Deliverable**: Professional table formatting, clear prompts, graceful exit

- Enhance `list_tasks()` formatting:
  - Add separator line (e.g., `"=" * 80`) between header and rows for clarity
  - Dynamically calculate column widths if needed, or use fixed widths with truncation/wrapping
  - Ensure alignment is consistent across all tasks
- Enhance prompts in `main()`:
  - Welcome message on startup
  - Clear command prompt (e.g., `"Enter command (add/list/update/delete/mark/exit): "`)
  - Confirmation messages on success (e.g., task created, marked complete, deleted)
- Implement graceful exit:
  - On `exit` or `quit`, print "Goodbye!" and terminate cleanly
  - Ensure no errors on exit; verify program terminates
- **Acceptance**: Output is professional and easy to scan; prompts are clear; exit is clean

### Phase 6: Documentation & Finalization
**Deliverable**: User-facing documentation, code review, clean commit history

- Write `README.md`:
  - Installation instructions (UV setup)
  - Running instructions (`uv run src/main.py` or `python -m src.main`)
  - Usage examples (quick walkthrough of each command)
  - Scope/limitations (Phase I, no persistence, single-user)
- Update `CLAUDE.md`:
  - Spec-driven workflow explanation
  - Module responsibilities recap
  - Testing approach (manual console testing)
- Verify code meets Constitution:
  - Type hints on all functions ✅
  - PEP 8 compliance ✅
  - Docstrings on all functions ✅
  - No external dependencies ✅
  - <500 lines total ✅
- Ensure clean commit history with meaningful messages
- **Acceptance**: README/CLAUDE.md complete; code passes constitution review; ready for user delivery

---

## Testing Strategy

*Manual interactive testing per Constitution (no automated test framework required in Phase I).*

### Command-Level Verification (Each Feature Phase)

After implementing each feature, verify:
1. **Command execution**: Does the command run without errors?
2. **State updates**: Does the task list reflect the command's effects?
3. **Output messages**: Are success/error messages clear and accurate?
4. **Idempotency** (where applicable): Can the command run multiple times safely?

### Full Workflow Validation

After Phase 3 (all CRUD features), run complete workflow:
```
add        # Create task 1 (title + description)
list       # Verify task 1 appears with [ ]
add        # Create task 2
mark 1     # Toggle task 1 to [x]
list       # Verify task 1 is [x], task 2 is [ ]
update 2   # Modify task 2 title/description
list       # Verify task 2 changes
delete 1   # Remove task 1
list       # Verify task 1 gone; task 2 still present
exit       # Goodbye message + clean exit
```

### Edge Case Verification

Test each edge case from spec:
- Empty task list → `list` shows "No tasks yet"
- Invalid ID (e.g., `mark 999`) → "Task ID 999 not found"
- Non-integer ID (e.g., `delete abc`) → "Invalid task ID"
- Empty title on add → "Title cannot be empty"
- Unrecognized command → "Unknown command"
- Rapid command sequence → All commands execute in order; state correct

### User Experience Checks

- Prompts are clear and self-explanatory
- Error messages guide user to correct action
- Confirmation messages confirm what was done
- Exit is immediate and graceful
- Command loop continues until explicit `exit`
