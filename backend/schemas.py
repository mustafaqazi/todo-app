"""Request and response schemas using Pydantic"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Attributes:
        title: Task title, required, 1-200 characters.
        description: Optional task description.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, bread, eggs"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating a task.

    Attributes:
        title: Updated task title, optional (1-200 if provided).
        description: Updated task description, optional.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Updated task description"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook",
                "description": "Milk, bread, eggs, and prepare dinner"
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response.

    Attributes:
        id: Task ID.
        userId: Owner user ID.
        title: Task title.
        description: Task description.
        status: Task status (pending or completed).
        createdAt: Creation timestamp.
        updatedAt: Last update timestamp.
    """

    id: int = Field(..., description="Task ID")
    userId: str = Field(..., alias="user_id", description="Owner user ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: str = Field(..., description="Task status (pending or completed)")
    createdAt: datetime = Field(..., alias="created_at", description="Creation timestamp")
    updatedAt: datetime = Field(..., alias="updated_at", description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "userId": "1",
                "title": "Buy groceries",
                "description": "Milk, bread, eggs",
                "status": "pending",
                "createdAt": "2026-01-05T12:00:00",
                "updatedAt": "2026-01-05T12:00:00"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for task list response.

    Attributes:
        items: List of tasks.
    """

    items: list[TaskResponse] = Field(..., description="List of tasks")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "user_id": "user-123",
                        "title": "Buy groceries",
                        "description": "Milk, bread, eggs",
                        "completed": False,
                        "created_at": "2026-01-05T12:00:00",
                        "updated_at": "2026-01-05T12:00:00"
                    }
                ]
            }
        }


class UserSignup(BaseModel):
    """Schema for user signup (registration).

    Attributes:
        email: User's email address.
        password: User's password (will be hashed).
    """

    email: str = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User's password (minimum 8 characters)"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login.

    Attributes:
        email: User's email address.
        password: User's password.
    """

    email: str = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        description="User's password"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!"
            }
        }


class AuthResponse(BaseModel):
    """Schema for authentication response (signup/login).

    Attributes:
        access_token: JWT token for API requests.
        token_type: Token type (usually "bearer").
        user_id: User ID (same as JWT sub claim).
    """

    access_token: str = Field(
        ...,
        description="JWT access token"
    )
    token_type: str = Field(
        ...,
        description="Token type (usually 'bearer')"
    )
    user_id: str = Field(
        ...,
        description="User ID (same as JWT 'sub' claim)"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "1"
            }
        }


class VerifyResponse(BaseModel):
    """Schema for token verification response.

    Attributes:
        valid: Whether the token is valid.
        user_id: User ID if valid, None otherwise.
    """

    valid: bool = Field(
        ...,
        description="Whether the token is valid"
    )
    user_id: Optional[str] = Field(
        None,
        description="User ID (from JWT 'sub' claim) if valid, None otherwise"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "valid": True,
                "user_id": "1"
            }
        }
