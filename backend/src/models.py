"""SQLModel database models."""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


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
