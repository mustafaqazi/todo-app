"""SQLModel database models."""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, JSON, ForeignKey, Index, Uuid


class User(SQLModel, table=True):
    """User model for authentication."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)  # User's email for login
    hashed_password: str  # Bcrypt hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Task(SQLModel, table=True):
    """Task model for todo application."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column_kwargs={"index": True})  # From JWT sub claim
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Conversation(SQLModel, table=True):
    """Conversation model for storing chat sessions.

    Attributes:
        id: Primary key, UUID (unique per conversation).
        user_id: Owner of the conversation (from JWT user_id claim).
        created_at: Timestamp when conversation was created (UTC).
        updated_at: Timestamp when conversation was last updated (UTC).

    Relationships:
        messages: List of Message objects in this conversation.
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


class Message(SQLModel, table=True):
    """Message model for storing chat messages and tool calls.

    Attributes:
        id: Primary key, UUID (unique per message).
        conversation_id: Foreign key to Conversation (UUID).
        user_id: Owner of the message (from JWT user_id claim, indexed for security).
        role: Message role ('user' or 'assistant').
        content: Message text content.
        tool_calls: Optional JSON data with tool call information.
        created_at: Timestamp when message was created (UTC).

    Relationships:
        conversation: Parent Conversation object.
    """

    __tablename__ = "message"

    id: Optional[UUID] = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique message identifier (UUID)"
    )
    conversation_id: UUID = Field(
        index=True,
        description="Parent conversation ID (foreign key to conversation.id)"
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
