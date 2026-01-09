"""Database models using SQLModel"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlmodel import Field, SQLModel


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
