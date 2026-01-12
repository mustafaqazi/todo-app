"""Database models using SQLModel"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, Index
from sqlmodel import Field, SQLModel, Relationship


class Task(SQLModel, table=True, extend_existing=True):
    """Task model representing a TODO item in the database.

    Attributes:
        id: Primary key, auto-generated integer.
        user_id: Owner of the task (from JWT 'user_id' claim, custom Better Auth claim).
        title: Task title, required, 1-200 characters.
        description: Optional task description, max 2000 characters.
        completed: Boolean flag for completion status, defaults to false.
        created_at: Timestamp when task was created (UTC, immutable).
        updated_at: Timestamp when task was last updated (UTC, auto-updated).

    Indexes:
        - user_id: Fast filtering of user's tasks.
        - (user_id, created_at): Optimized for listing and sorting by date.
        - (user_id, completed): Optimized for status filtering.
    """

    __tablename__ = "task"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier"
    )
    user_id: str = Field(
        sa_column=Column(String(255), nullable=False, index=True),
        description="Owner user ID from JWT user_id claim"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)",
        sa_column=Column(String(200), nullable=False)
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description (max 2000 characters)",
        sa_column=Column(String(2000), nullable=True)
    )
    completed: bool = Field(
        default=False,
        description="Task completion status",
        sa_column=Column(Boolean, nullable=False, default=False)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of task creation (UTC, immutable)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last update (UTC, auto-updated)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )

    class Config:
        """SQLModel configuration."""
        arbitrary_types_allowed = True


class User(SQLModel, table=True, extend_existing=True):
    """User model for authentication.

    Attributes:
        id: Primary key, auto-generated integer.
        email: User's email address, unique and indexed.
        hashed_password: Bcrypt-hashed password.
        created_at: Timestamp when user was created (UTC).
        updated_at: Timestamp when user record was last updated (UTC).
    """

    __tablename__ = "user"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique user identifier"
    )
    email: str = Field(
        sa_column=Column(String(255), nullable=False, unique=True, index=True),
        description="User's email address (unique)"
    )
    hashed_password: str = Field(
        sa_column=Column(String(255), nullable=False),
        description="Bcrypt-hashed password"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of user creation (UTC)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last update (UTC)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )

    class Config:
        """SQLModel configuration."""
        arbitrary_types_allowed = True


class Conversation(SQLModel, table=True, extend_existing=True):
    """Conversation model for storing chat sessions.

    Attributes:
        id: Primary key, UUID (unique per conversation).
        user_id: Owner of the conversation (from JWT user_id claim).
        created_at: Timestamp when conversation was created (UTC).
        updated_at: Timestamp when conversation was last updated (UTC).

    Relationships:
        messages: List of Message objects in this conversation.

    Indexes:
        - user_id: Fast filtering of user's conversations.
        - (user_id, created_at DESC): Optimized for listing conversations by recency.
    """

    __tablename__ = "conversation"

    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique conversation identifier (UUID)"
    )
    user_id: str = Field(
        sa_column=Column(String(255), nullable=False, index=True),
        description="Owner user ID from JWT user_id claim"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of conversation creation (UTC)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last update (UTC, auto-updated)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    messages: Optional[list["Message"]] = Relationship(back_populates="conversation")

    class Config:
        """SQLModel configuration."""
        arbitrary_types_allowed = True


class Message(SQLModel, table=True, extend_existing=True):
    """Message model for storing chat messages and tool calls.

    Attributes:
        id: Primary key, UUID (unique per message).
        conversation_id: Foreign key to Conversation.
        user_id: Owner of the message (from JWT user_id claim, indexed for security).
        role: Message role ('user' or 'assistant').
        content: Message text content.
        tool_calls: Optional JSON data with tool call information.
        created_at: Timestamp when message was created (UTC).

    Relationships:
        conversation: Parent Conversation object.

    Indexes:
        - (conversation_id, user_id): Fast filtering by conversation and user.
        - user_id: Security index for cross-user access checks.
        - created_at DESC: Optimized for chronological ordering.
    """

    __tablename__ = "message"

    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique message identifier (UUID)"
    )
    conversation_id: UUID = Field(
        sa_column=Column(String, ForeignKey("conversation.id", ondelete="CASCADE"), nullable=False, index=True),
        description="Parent conversation ID"
    )
    user_id: str = Field(
        sa_column=Column(String(255), nullable=False, index=True),
        description="Owner user ID from JWT user_id claim (for security filtering)"
    )
    role: str = Field(
        sa_column=Column(String(50), nullable=False),
        description="Message role: 'user' or 'assistant'"
    )
    content: str = Field(
        sa_column=Column(Text, nullable=False),
        description="Message text content"
    )
    tool_calls: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
        description="Optional JSON object with tool call information"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of message creation (UTC)",
        sa_column=Column(DateTime, nullable=False, default=datetime.utcnow)
    )
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    class Config:
        """SQLModel configuration."""
        arbitrary_types_allowed = True
