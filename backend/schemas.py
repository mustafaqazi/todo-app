"""Request and response schemas using Pydantic"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


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
        user_id: Owner user ID.
        title: Task title.
        description: Task description.
        completed: Completion status.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    id: int = Field(..., description="Task ID")
    user_id: str = Field(..., description="Owner user ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    completed: bool = Field(..., description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user-123",
                "title": "Buy groceries",
                "description": "Milk, bread, eggs",
                "completed": False,
                "created_at": "2026-01-05T12:00:00",
                "updated_at": "2026-01-05T12:00:00"
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
