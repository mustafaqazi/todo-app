---
name: MCP Server Setup
description: Complete setup and configuration of the Official MCP Server for exposing task management tools in the Todo AI Chatbot project
version: 1.0
phase: Phase III - AI Chatbot
dependencies: [fastapi, sqlmodel, openai-agents-sdk, official-mcp-sdk]
---

# MCP Server Setup Skill

You are responsible for creating and configuring a fully functional MCP (Model Context Protocol) Server that exposes the required task management tools for the AI agent in the Todo AI Chatbot.

## Objective
Create a stateless MCP server that:
- Runs inside or alongside the FastAPI application
- Exposes exactly the 5 required tools: add_task, list_tasks, complete_task, delete_task, update_task
- Enforces user isolation using user_id from JWT
- Uses existing Neon PostgreSQL database (SQLModel)
- Returns structured JSON responses as specified in the project document

## Required MCP Tools to Expose

1. add_task
   - Parameters: user_id (string, required), title (string, required), description (string, optional)
   - Returns: {"task_id": int, "status": "created", "title": str}

2. list_tasks
   - Parameters: user_id (string, required), status (string, optional: "all"|"pending"|"completed")
   - Returns: array of task objects [{"id": int, "title": str, "description": str|null, "completed": bool, ...}]

3. complete_task
   - Parameters: user_id (string, required), task_id (integer, required)
   - Returns: {"task_id": int, "status": "completed", "title": str}

4. delete_task
   - Parameters: user_id (string, required), task_id (integer, required)
   - Returns: {"task_id": int, "status": "deleted", "title": str}

5. update_task
   - Parameters: user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional)
   - Returns: {"task_id": int, "status": "updated", "title": str}

## Technical Requirements

1. MCP Server Location
   - Preferred: Integrated inside FastAPI as a separate router/mount
   - Alternative: Separate FastAPI instance (but single app recommended for hackathon)

2. Authentication & Security
   - Every tool call MUST receive user_id from the JWT token (via dependency)
   - Validate user_id matches the authenticated user
   - All DB operations MUST include WHERE user_id = :user_id

3. Database Integration
   - Use existing SQLModel Task table
   - Use async session via dependency (get_session)
   - Update updated_at on modify operations

4. Response Format
   - Always return valid JSON matching the exact structure in the project document
   - Use HTTP status codes: 200 for success, 400 for validation, 401 for auth, 404 for not found

5. Error Handling
   - Return friendly error messages in JSON
   - Examples:
     - {"error": "Task not found", "code": "not_found"}
     - {"error": "Title is required", "code": "validation_error"}

## Recommended File Structure Additions
