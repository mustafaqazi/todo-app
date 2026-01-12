"""Chat endpoint for AI-powered todo assistant.

This module provides the stateless POST /api/{user_id}/chat endpoint
that processes user messages through Cohere and executes MCP tools.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from dependencies import get_current_user
from schemas import ChatRequest, ChatResponse
from services.conversation import (
    get_or_create_conversation,
    get_last_n_messages,
    append_message,
)
from agents.cohere_todo_agent import CohereTodoAgent
from mcp.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])


# Tool executor mapping
TOOL_EXECUTORS = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}


@router.post("", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ChatResponse:
    """
    Chat endpoint for AI-powered todo assistant.

    This endpoint:
    1. Validates JWT and user_id match
    2. Fetches or creates a conversation
    3. Loads conversation history
    4. Calls Cohere API with message and tools
    5. Executes any tool calls returned by Cohere
    6. Stores messages in database
    7. Returns response and tool call results

    Args:
        user_id: User ID from path (must match JWT 'sub' claim).
        request: ChatRequest with optional conversation_id and message.
        current_user: Authenticated user from JWT.
        session: Database session for persistence.

    Returns:
        ChatResponse with conversation_id, assistant response, and optional tool_calls.

    Raises:
        HTTPException: 401 if JWT invalid, 400 if user_id doesn't match JWT, 503 if Cohere fails.
    """
    # Security: Validate user_id matches JWT
    jwt_user_id = current_user.get("user_id")
    if user_id != jwt_user_id:
        logger.warning(
            f"❌ User ID mismatch: path={user_id}, JWT={jwt_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in path does not match authenticated user",
        )

    try:
        # Get or create conversation
        conversation = await get_or_create_conversation(
            session, user_id, request.conversation_id
        )

        # Load last 20 messages for context
        message_history = await get_last_n_messages(
            session, conversation.id, user_id, n=20
        )

        # Convert message history to Cohere format
        cohere_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in message_history
        ]

        # Initialize Cohere agent
        agent = CohereTodoAgent()

        # Get user email from JWT
        user_email = current_user.get("email")

        # Call Cohere API
        cohere_response = await agent.process_message(
            message=request.message,
            conversation_history=cohere_messages,
            user_email=user_email,
        )

        # Store user message
        await append_message(
            session, conversation.id, user_id, "user", request.message
        )

        # Execute tool calls if present
        tool_call_results = []
        if cohere_response.get("tool_calls"):
            for tool_call in cohere_response["tool_calls"]:
                tool_name = tool_call.get("name")
                tool_params = tool_call.get("parameters", {})

                logger.info(
                    f"🔧 Executing tool: {tool_name} with params: {tool_params}"
                )

                try:
                    # Get tool executor
                    executor = TOOL_EXECUTORS.get(tool_name)
                    if not executor:
                        logger.warning(f"❌ Unknown tool: {tool_name}")
                        result = {"error": f"Unknown tool: {tool_name}"}
                    else:
                        # Execute tool
                        result = await executor(session, user_id, **tool_params)

                    tool_call_results.append(
                        {
                            "name": tool_name,
                            "parameters": tool_params,
                            "result": result,
                        }
                    )

                    logger.info(f"✅ Tool {tool_name} executed: {result}")

                except Exception as e:
                    logger.error(f"❌ Tool {tool_name} failed: {str(e)}")
                    tool_call_results.append(
                        {
                            "name": tool_name,
                            "parameters": tool_params,
                            "result": {"error": f"Tool failed: {str(e)}"},
                        }
                    )

        # Store assistant message with tool calls
        await append_message(
            session,
            conversation.id,
            user_id,
            "assistant",
            cohere_response.get("response", ""),
            tool_calls=tool_call_results if tool_call_results else None,
        )

        # Commit transaction
        await session.commit()

        logger.info(
            f"✅ Chat request processed for user {user_id}, "
            f"conversation {conversation.id}, {len(tool_call_results)} tools executed"
        )

        return ChatResponse(
            conversation_id=str(conversation.id),
            response=cohere_response.get("response", ""),
            tool_calls=tool_call_results if tool_call_results else None,
        )

    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {str(e)}")
        await session.rollback()

        # Return 503 for Cohere API errors
        if "Cohere" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service temporarily unavailable. Please try again.",
            )

        # Generic 500 for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request.",
        )
