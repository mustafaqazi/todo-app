"""Conversation service for managing chat history and persistence.

This module provides database operations for storing and retrieving conversations
and messages with strict user isolation.
"""

import logging
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_
from sqlmodel import Session

# Import from src.models to ensure unified model registry (Phase II + Phase III)
from src.models import Conversation, Message

logger = logging.getLogger(__name__)


async def get_or_create_conversation(
    session: AsyncSession,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Conversation:
    """Get existing conversation or create new one.

    Args:
        session: AsyncSession for database operations.
        user_id: Owner user ID (from JWT user_id claim).
        conversation_id: Optional UUID of existing conversation; if provided, fetches it.

    Returns:
        Conversation object (existing or newly created).

    Raises:
        ValueError: If conversation_id is provided but not found or owned by different user.
    """
    logger.debug(f"📌 get_or_create_conversation called: user_id={user_id}, conversation_id={conversation_id}")

    if conversation_id:
        try:
            logger.debug(f"🔍 Attempting to fetch conversation {conversation_id} for user {user_id}")
            # Fetch existing conversation with strict user_id check
            stmt = select(Conversation).where(
                and_(
                    Conversation.id == UUID(conversation_id),
                    Conversation.user_id == user_id
                )
            )
            result = await session.execute(stmt)
            conversation = result.scalars().first()
            logger.debug(f"📊 Query result: {'Found' if conversation else 'Not found'}")

            if conversation:
                logger.info(f"✅ Loaded existing conversation: {conversation_id}")
                return conversation
            else:
                logger.warning(
                    f"⚠️ Conversation {conversation_id} not found for user {user_id}. Creating new conversation."
                )
        except Exception as e:
            logger.warning(f"⚠️ Error loading conversation {conversation_id}: {e}. Creating new conversation.")

    # Create new conversation
    logger.debug(f"🆕 Creating new conversation for user {user_id}")
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    logger.debug(f"💾 Added conversation to session, flushing to get ID...")
    await session.flush()  # Ensure ID is generated
    logger.info(f"✅ Created new conversation: {conversation.id} for user {user_id}")
    logger.debug(f"🎯 Conversation object: id={conversation.id}, user_id={conversation.user_id}, created_at={conversation.created_at}")
    return conversation


async def get_last_n_messages(
    session: AsyncSession,
    conversation_id: UUID,
    user_id: str,
    n: int = 20
) -> list[Message]:
    """Fetch last N messages from conversation with user isolation.

    Args:
        session: AsyncSession for database operations.
        conversation_id: UUID of conversation.
        user_id: Owner user ID (for security filtering).
        n: Number of messages to fetch (default 20).

    Returns:
        List of Message objects sorted by creation time (oldest first).

    Note:
        Filters by both conversation_id AND user_id for security.
        Even if an attacker knows conversation_id, they cannot access
        messages from conversations owned by other users.
    """
    # Query with double-check: conversation_id AND user_id
    stmt = select(Message).where(
        and_(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        )
    ).order_by(Message.created_at).limit(n)

    result = await session.execute(stmt)
    messages = result.scalars().all()
    logger.info(f"✅ Fetched {len(messages)} messages from conversation {conversation_id}")
    return messages


async def append_message(
    session: AsyncSession,
    conversation_id: UUID,
    user_id: str,
    role: str,
    content: str,
    tool_calls: Optional[dict] = None
) -> Message:
    """Append a new message to conversation.

    Args:
        session: AsyncSession for database operations.
        conversation_id: UUID of conversation.
        user_id: Owner user ID.
        role: Message role ('user' or 'assistant').
        content: Message text content.
        tool_calls: Optional JSON dict with tool call information.

    Returns:
        Created Message object.

    Raises:
        ValueError: If role is not 'user' or 'assistant'.
    """
    logger.debug(f"📝 append_message called: conversation_id={conversation_id}, user_id={user_id}, role={role}, content_len={len(content)}")

    if role not in ("user", "assistant"):
        raise ValueError(f"Invalid role '{role}'. Must be 'user' or 'assistant'.")

    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    logger.debug(f"📌 Message object created: id={message.id}, role={role}")
    session.add(message)
    await session.flush()
    logger.debug(f"✅ Message flushed: id={message.id}")
    logger.info(
        f"✅ Appended {role} message to conversation {conversation_id}: {len(content)} chars"
    )
    return message
