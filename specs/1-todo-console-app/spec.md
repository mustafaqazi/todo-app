# Feature Specification: Phase I - Todo In-Memory Python Console App

**Feature Branch**: `1-todo-console-app`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Phase I: Todo In-Memory Python Console App"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Task (Priority: P1)

A user starts the TODO application and wants to create a new task to track work they need to complete. They provide a task title and optional description, and the system assigns a unique ID and displays confirmation.

**Why this priority**: Adding tasks is the foundational capability. Without the ability to create tasks, the application has no value. This is the critical MVP feature.

**Independent Test**: Can be fully tested by launching the app, executing the "add" command with a title and description, and verifying the task appears in the task list with a unique ID. Delivers the core capability to create work items.

**Acceptance Scenarios**:

1. **Given** the app is running and the task list is empty, **When** user enters `add`, **Then** the app prompts for title and description, creates the task with auto-incremented ID starting at 1, and displays success confirmation with the new task ID.
2. **Given** existing tasks in the list, **When** user adds a new task with title and description, **Then** the new task is assigned the next sequential ID and marked as incomplete `[ ]`.
3. **Given** user attempts to add a task without a title, **When** the user submits an empty or whitespace-only title, **Then** the app displays an error "Title cannot be empty" and re-prompts for input without creating the task.
4. **Given** the app is running, **When** user adds a task with title only (no description), **Then** the task is created successfully with empty description field.

---

### User Story 2 - View All Tasks (Priority: P1)

A user wants to see all their tasks in a formatted, easy-to-scan list with completion status visible at a glance.

**Why this priority**: Viewing is equally critical as adding. Users need to see what they've created. This P1 feature works independently—users can add tasks, then view them.

**Independent Test**: Can be fully tested by adding several tasks with different states, executing the "list" command, and verifying all tasks display with correct IDs, titles, descriptions, and status indicators. Demonstrates the core viewing capability.

**Acceptance Scenarios**:

1. **Given** the app contains 3 tasks (one complete, two incomplete), **When** user enters `list`, **Then** the app displays a formatted table with columns: ID | Title | Description | Status, where status shows `[x]` for complete and `[ ]` for incomplete.
2. **Given** the task list is empty, **When** user enters `list`, **Then** the app displays "No tasks yet. Add one with the 'add' command." message.
3. **Given** a task has a long title or description, **When** the user views the list, **Then** the app displays the text without truncation (wrapping is acceptable) and maintains readable column alignment.
4. **Given** multiple tasks exist, **When** user executes `list`, **Then** all tasks are displayed in order by ID (oldest first).

---

### User Story 3 - Mark Task Complete/Incomplete (Priority: P1)

A user wants to toggle the completion status of a task to track progress as they complete work.

**Why this priority**: Marking completion is core functionality and works independently of other features. Users can add tasks, mark them complete, and view the results.

**Independent Test**: Can be fully tested by creating tasks, marking one complete with `mark`, viewing the list to confirm status changed, and toggling it back incomplete with `mark`. Demonstrates task state management.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists and is marked incomplete `[ ]`, **When** user executes `mark 1`, **Then** the app marks the task complete `[x]` and displays "Task 1 marked complete."
2. **Given** a task with ID 2 is marked complete `[x]`, **When** user executes `mark 2` again, **Then** the app toggles the task to incomplete `[ ]` and displays "Task 2 marked incomplete."
3. **Given** user attempts to mark a non-existent task (e.g., `mark 99`), **When** the ID does not exist in the task list, **Then** the app displays "Task ID 99 not found." and does not modify any task.
4. **Given** user enters `mark` without an ID, **When** no task ID is provided, **Then** the app displays "Please provide a task ID to mark." and re-prompts.

---

### User Story 4 - Update Task Details (Priority: P2)

A user wants to edit the title and/or description of an existing task to correct mistakes or add more detail.

**Why this priority**: Update capability is valuable but not strictly required for an MVP. However, once adding and viewing work, users naturally want to fix mistakes. This feature is independently testable—add a task, update it, and verify the change.

**Independent Test**: Can be fully tested by creating a task, executing the "update" command with a new title and description, and verifying the changes appear in the task list. Demonstrates task editing capability.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists with title "Buy milk", **When** user executes `update 1 "Buy milk and bread" "From the grocery store"`, **Then** the task title and description are updated and the app displays "Task 1 updated."
2. **Given** user attempts to update a non-existent task (ID 99), **When** the ID does not exist, **Then** the app displays "Task ID 99 not found." and does not create a new task.
3. **Given** a task exists, **When** user updates only the title (leaving description unchanged), **Then** the title is updated and description remains as-is.
4. **Given** user attempts to update a task with an empty title, **When** the new title is empty or whitespace-only, **Then** the app displays "Title cannot be empty." and does not modify the task.

---

### User Story 5 - Delete Task (Priority: P2)

A user wants to remove a task from the list when it's no longer needed or was added by mistake.

**Why this priority**: Delete is useful but less critical than add/view/mark. Still independently testable—add a task, delete it, and verify removal.

**Independent Test**: Can be fully tested by creating a task, executing the "delete" command with the task ID, and verifying the task no longer appears in the list. Demonstrates task removal capability.

**Acceptance Scenarios**:

1. **Given** a task with ID 2 exists, **When** user executes `delete 2`, **Then** the task is removed from the list and the app displays "Task 2 deleted."
2. **Given** 3 tasks exist (IDs 1, 2, 3), **When** user deletes task 2, **Then** the app removes it and IDs 1 and 3 remain (IDs are not re-numbered; they remain as originally assigned).
3. **Given** user attempts to delete a non-existent task (ID 50), **When** the ID does not exist, **Then** the app displays "Task ID 50 not found." and does not remove any task.
4. **Given** user enters `delete` without an ID, **When** no task ID is provided, **Then** the app displays "Please provide a task ID to delete." and re-prompts.

---

### User Story 6 - Exit Application Gracefully (Priority: P1)

A user wants to cleanly exit the application and see a goodbye message.

**Why this priority**: Graceful exit is part of the core CLI experience. Works independently—start app, execute commands, exit cleanly.

**Independent Test**: Can be fully tested by launching the app and executing the "exit" command, verifying the goodbye message displays and the app terminates cleanly.

**Acceptance Scenarios**:

1. **Given** the app is running with tasks in the list, **When** user executes `exit`, **Then** the app displays a goodbye message (e.g., "Goodbye!") and terminates cleanly without errors.
2. **Given** the app has been running for multiple commands, **When** user executes `exit`, **Then** the command loop ends and the program terminates (no tasks are persisted; sessions are ephemeral).

---

### Edge Cases

- What happens when user enters an unrecognized command (e.g., `foobar`)? The app displays "Unknown command. Type 'add', 'list', 'update', 'delete', 'mark', or 'exit'." and re-prompts.
- How does the system handle invalid input for a task ID (e.g., `mark abc` or `delete -5`)? The app displays "Invalid task ID. Please provide a positive integer." and re-prompts.
- What happens if the task list is empty and user tries to mark, update, or delete? The app displays "No tasks to [action]. Add one with the 'add' command." and re-prompts.
- How does the app handle very long titles or descriptions (e.g., 500+ characters)? The app accepts and stores the full text; display wrapping occurs naturally in the formatted table.
- What if a user rapidly executes multiple commands in sequence? The app processes each command in order, maintaining task state accurately across all operations.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new task with a required title and optional description via the `add` command.
- **FR-002**: System MUST auto-increment task IDs starting from 1 and assign a unique ID to each new task.
- **FR-003**: System MUST display all tasks in a formatted table-like view (ID | Title | Description | Status) via the `list` command.
- **FR-004**: System MUST display incomplete tasks with status `[ ]` and complete tasks with status `[x]` in the list view.
- **FR-005**: System MUST allow users to mark a task complete or incomplete (toggle) via the `mark <task_id>` command.
- **FR-006**: System MUST allow users to update a task's title and/or description via the `update <task_id> <new_title> [new_description]` command.
- **FR-007**: System MUST allow users to delete a task by ID via the `delete <task_id>` command, with remaining tasks retaining their original IDs.
- **FR-008**: System MUST validate all user inputs: required title fields cannot be empty, task IDs must be positive integers and must exist in the task list.
- **FR-009**: System MUST display user-friendly error messages for all validation failures (e.g., "Task ID not found", "Title cannot be empty").
- **FR-010**: System MUST support a command loop accepting commands via `input()` (interactive prompt) that continues until the user executes the `exit` command.
- **FR-011**: System MUST accept commands case-insensitively (e.g., `ADD`, `add`, `Add` all work).
- **FR-012**: System MUST display a goodbye message and terminate cleanly when the user executes the `exit` command.
- **FR-013**: System MUST store all tasks in memory as a Python list of dictionaries with schema `{'id': int, 'title': str, 'description': str, 'complete': bool}`.
- **FR-014**: System MUST handle an empty task list gracefully and display "No tasks yet. Add one with the 'add' command." when users attempt to view an empty list.
- **FR-015**: System MUST be executable via `python -m src.main` or `uv run src/main.py` after project setup with UV.

### Key Entities

- **Task**: Represents a single work item. Attributes: `id` (unique integer, auto-increment), `title` (non-empty string, required), `description` (string, optional/empty allowed), `complete` (boolean, defaults to False on creation). No relationships to other entities in Phase I.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 core features (add, list, mark, update, delete) are fully functional and independently testable via console commands without errors.
- **SC-002**: Application code follows PEP 8 standard with type hints on all functions, 79-character line limit, and snake_case naming conventions.
- **SC-003**: Code is organized into exactly two modules (`src/main.py` for CLI loop, `src/todo_manager.py` for task logic) with no duplication and each function having a single responsibility.
- **SC-004**: Application handles all identified edge cases (empty list, invalid ID, invalid input, unrecognized commands) with user-friendly error messages.
- **SC-005**: Users can complete a full workflow (add 3 tasks, mark one complete, update one, delete one, view list) in under 2 minutes with clear, intuitive prompts.
- **SC-006**: Project repository structure matches specification: `constitution.md`, `README.md`, `CLAUDE.md` in root; `/src` with code; `specs/1-todo-console-app/` with all design artifacts.
- **SC-007**: Application runs successfully on Python 3.13+ using UV for project management with zero external dependencies beyond the Python standard library.
- **SC-008**: Total source code (both modules combined) is between 300-500 lines of code, demonstrating simplicity and readability.

## Assumptions

- **Session Ephemeral**: Tasks exist only in memory during a single application session. Closing and re-opening the app starts with an empty task list (no persistence to disk).
- **Single User**: The application is designed for a single interactive user in a console session; no multi-user or concurrent access scenarios.
- **Manual Testing**: The specification focuses on manual console-based testing by developers; no automated test framework is required or expected in Phase I.
- **Command Parsing**: Commands are parsed from user input via `input().split()` or similar simple string operations; no external argument parsing library (like argparse) is used.
- **Input Format**: Titles and descriptions are single-line text. Multi-line input is not supported (users can include spaces in titles/descriptions if quoted or input via a single command line).
- **Non-Destructive by Default**: Confirmation prompts for destructive operations (delete) are not required; user confirmation is implicit in explicit command entry.
- **Exit Behavior**: The `exit` command terminates the program immediately without prompting to save (since there is no persistence).
