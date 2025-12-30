---
id: 001
title: Python TODO Constitution
stage: constitution
date: 2025-12-29
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "governance", "python", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

You are an expert Python developer building a command-line TODO application using spec-driven development. Adhere strictly to the following constitution for all code generation and validation:

Project Overview and Goals:
Build a basic in-memory TODO console app in Python 3.13+.
Features: Add task (title, description), View tasks with status ([ ] incomplete, [x] complete), Update task details, Delete task by ID, Mark task complete/incomplete.
No external dependencies beyond standard library. Use UV for project management.
Store tasks in memory as a list of dictionaries: {'id': int, 'title': str, 'description': str, 'complete': bool}.
Run in a loop accepting commands: add, list, update, delete, mark, exit.

Coding Standards (Clean Code Principles):
Follow PEP 8: 4-space indentation, 79-char line limit, snake_case for variables/functions.
Use type hints for all functions (e.g., def add_task(tasks: list[dict], title: str, description: str) -> None).
Modular code: Separate concerns – one file for task logic (todo_manager.py), one for main loop (main.py).
Meaningful names: No abbreviations (e.g., use task_id, not tid).
Error handling: Raise ValueError for invalid inputs, print user-friendly messages.
No duplication: Refactor common code into functions.
Comments: Only where logic is non-obvious; docstrings for all functions.

Project Structure:
Root: constitution.txt, README.md, CLAUDE.md.
/src: main.py (entry point), todo_manager.py (core logic).
/specs-history: Store all spec files as Markdown.
Use if name == "main" in main.py.

Implementation Guidelines:
Command parsing: Use sys.argv or simple input().split() – no argparse to keep minimal.
ID Management: Auto-increment starting from 1.
Viewing: Print tasks in a formatted table-like string (e.g., ID | Title | Description | Status).
Status: Use '[x]' for complete, '[ ]' for incomplete.
Input Validation: Check for existing IDs, required fields.
Exit Gracefully: On 'exit' command, print goodbye and break loop.

Spec-Driven Rules:
Generate code only from provided specs.
Validate against this constitution: If code violates, suggest fixes.
Ensure completeness: Cover all edge cases from specs (e.g., empty list, invalid ID).
Testability: Code should be easy to test manually in console.

General Principles:
Prioritize readability over cleverness.
Keep it simple: No classes unless needed (dictionaries suffice).
Assume user is beginner-friendly: Clear prompts and errors.
No internet/network code; pure console.

When generating or validating code, reference this constitution explicitly in your reasoning.

## Response snapshot

Created comprehensive Python TODO Application Constitution (v1.0.0) with 7 core principles:

1. **Simplicity and Minimalism**: In-memory, no external deps, straightforward data structures
2. **Modular Code Organization**: `todo_manager.py` for logic, `main.py` for CLI interface
3. **Type Safety and Clean Code**: PEP 8, type hints, meaningful names, docstrings
4. **Validated User Input**: Required field checks, ID validation, user-friendly errors
5. **In-Memory Task Storage**: List of dicts with auto-increment IDs, no persistence
6. **CLI and Minimal Command Parsing**: Simple string-based commands, graceful exit
7. **Formatted Output and Readability**: Table-like display, [x]/[ ] status notation

Constitution includes Implementation Standards section with function signature conventions, validation patterns, and testing approach. Code Structure section defines directory layout and module responsibilities with specific function signatures for each module.

Governance section establishes amendment procedure, compliance review gates (all 7 principles), and development workflow treating principles as hard constraints.

Version 1.0.0 ratified and last amended 2025-12-29.

## Outcome

- ✅ Impact: Establishes binding governance for all code contributions; provides clear compliance gates for spec/plan/tasks phases
- 🧪 Tests: Manual console testing approach documented; no external test frameworks required
- 📁 Files: `.specify/memory/constitution.md` created and populated
- 🔁 Next prompts: Run `/sp.specify` to create feature specification, or `/sp.plan` to design implementation
- 🧠 Reflection: Constitution successfully captures project requirements from user input into concrete, testable principles. All seven principles are declarative, measurable, and tied to rationale. Principles are hard constraints with explicit compliance gates for code reviews.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - all placeholders filled, no unexplained brackets, version coherent, dates ISO format
- Prompt variant (if applicable): none
- Next experiment: Proceed with `/sp.specify` to capture user stories and requirements for the feature
