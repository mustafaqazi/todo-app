"""Cohere API client and todo assistant agent for Phase III.

This module provides Cohere integration for natural language task management.
Uses command-a-03-2025 model with tool calling for executing MCP tools.
"""

import os
import logging
from typing import Optional, Any

import cohere

logger = logging.getLogger(__name__)


class CohereTodoAgent:
    """Cohere-powered todo assistant with tool calling capabilities.

    Attributes:
        client: Cohere client instance (initialized with COHERE_API_KEY).
        model: Model name to use (command-a-03-2025).
        tools: List of tool definitions for Cohere tool calling.
    """

    MODEL = "command-a-03-2025"

    def __init__(self):
        """Initialize Cohere client with API key from environment."""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError(
                "COHERE_API_KEY environment variable is required. "
                "Set it in .env or pass as environment variable."
            )
        self.client = cohere.Client(api_key=api_key)
        logger.info("✅ Cohere client initialized with model: %s", self.MODEL)

    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Get MCP tool definitions for Cohere tool calling.

        Returns:
            List of tool definitions as dictionaries with name, description, and parameters.
            Tools: add_task, list_tasks, complete_task, delete_task, update_task.
        """
        return [
            {
                "name": "add_task",
                "description": "Add a new task for the user. Returns the task ID.",
                "parameter_definitions": {
                    "title": {
                        "description": "Task title (required, 1-200 characters)",
                        "type": "str",
                        "required": True
                    },
                    "description": {
                        "description": "Optional task description (0-2000 characters)",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "List all tasks for the user. Optionally filter by completion status.",
                "parameter_definitions": {
                    "status": {
                        "description": "Filter by status: 'all' (default), 'pending', or 'completed'",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as complete. Requires task ID or title.",
                "parameter_definitions": {
                    "task_id": {
                        "description": "Task ID (required if title not provided)",
                        "type": "int",
                        "required": False
                    },
                    "title": {
                        "description": "Task title (required if task_id not provided)",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task. Requires task ID or title.",
                "parameter_definitions": {
                    "task_id": {
                        "description": "Task ID (required if title not provided)",
                        "type": "int",
                        "required": False
                    },
                    "title": {
                        "description": "Task title (required if task_id not provided)",
                        "type": "str",
                        "required": False
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update a task's title or description. Requires task ID or current title.",
                "parameter_definitions": {
                    "task_id": {
                        "description": "Task ID (required if current_title not provided)",
                        "type": "int",
                        "required": False
                    },
                    "current_title": {
                        "description": "Current task title (required if task_id not provided)",
                        "type": "str",
                        "required": False
                    },
                    "new_title": {
                        "description": "New task title (optional)",
                        "type": "str",
                        "required": False
                    },
                    "new_description": {
                        "description": "New task description (optional)",
                        "type": "str",
                        "required": False
                    }
                }
            }
        ]

    def process_message(
        self,
        message: str,
        conversation_history: Optional[list[dict[str, str]]] = None,
        user_email: Optional[str] = None
    ) -> dict[str, Any]:
        """Process a user message with Cohere and return response.

        Note: This is a synchronous method because the Cohere SDK doesn't support async.
        FastAPI will handle this correctly as long as this method doesn't block the event loop.

        Args:
            message: User's message text.
            conversation_history: Optional list of previous messages (role, content).
            user_email: Optional user email for personalization.

        Returns:
            Dictionary with 'response' text and optional 'tool_calls' list.
        """
        system_prompt = (
            "You are a helpful TODO assistant. You help users manage their tasks using natural language. "
            "You have access to 5 tools: add_task, list_tasks, complete_task, delete_task, and update_task. "
            "Use these tools to execute user requests. Always confirm actions and provide friendly feedback. "
            f"{f'The user is logged in as {user_email}.' if user_email else ''}"
        )

        try:
            # Call Cohere API with tool definitions
            # Cohere SDK uses 'message' (singular) and 'chat_history' for conversation history
            # Note: 'system' parameter is not supported; system context is embedded in the user message

            # Use conversation history as-is (should already be formatted with 'message' key)
            chat_history = conversation_history or []

            # Prepend system prompt to the user's message
            user_message = f"{system_prompt}\n\nUser: {message}"

            response = self.client.chat(
                model=self.MODEL,
                message=user_message,
                chat_history=chat_history,
                tools=self.get_tool_definitions(),
                temperature=0.7,
            )

            # Extract response text and tool calls
            response_text = response.text
            tool_calls = []

            # Process tool calls if present
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_calls.append({
                        "name": tool_call.name,
                        "parameters": tool_call.parameters,
                        # Note: result will be populated by the endpoint after execution
                    })

            logger.info(
                "✅ Cohere response processed. Tool calls: %d",
                len(tool_calls)
            )

            return {
                "response": response_text,
                "tool_calls": tool_calls if tool_calls else None,
            }

        except Exception as e:
            # Handle any Cohere-related errors (API errors, timeouts, etc.)
            logger.error("❌ Cohere agent error: %s - %s", type(e).__name__, str(e))
            raise
