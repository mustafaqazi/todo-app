"""MCP tools for task management with strict user isolation.

Each tool filters by user_id to ensure zero data leakage across users.
Tools are stateless and safe for concurrent use.
"""

import logging
from typing import Optional, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from src.models import Task

logger = logging.getLogger(__name__)


async def add_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> dict[str, Any]:
    """Add a new task for the user.

    Args:
        session: AsyncSession for database operations.
        user_id: Owner user ID (from JWT user_id claim).
        title: Task title (required, 1-200 chars).
        description: Optional task description (max 2000 chars).

    Returns:
        Dictionary with task_id and confirmation message.

    Security:
        - Only creates tasks owned by the authenticated user_id.
        - Returns 400 Bad Request for invalid input.
    """
    try:
        # Validate input
        if not title or not title.strip():
            return {"error": "Task title cannot be empty"}
        if len(title) > 200:
            return {"error": "Task title must be 200 characters or less"}
        if description and len(description) > 2000:
            return {"error": "Description must be 2000 characters or less"}

        # Create task
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )
        session.add(task)
        await session.flush()

        logger.info(f"✅ Added task '{title}' (ID: {task.id}) for user {user_id}")
        return {
            "id": task.id,
            "title": task.title,
            "message": f"Task '{task.title}' added successfully! ID: {task.id}"
        }
    except Exception as e:
        logger.error(f"❌ Error adding task: {str(e)}")
        return {"error": f"Failed to add task: {str(e)}"}


async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status: str = "all"
) -> dict[str, Any]:
    """List tasks for the user with optional status filtering.

    Args:
        session: AsyncSession for database operations.
        user_id: Owner user ID (from JWT user_id claim).
        status: Filter by status: 'all' (default), 'pending', or 'completed'.

    Returns:
        Dictionary with task list and count.

    Security:
        - Only returns tasks owned by the authenticated user_id.
        - Prevents cross-user data leakage via user_id filter.
    """
    try:
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter if specified
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        elif status != "all":
            return {"error": f"Invalid status '{status}'. Use 'all', 'pending', or 'completed'."}

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Format response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]

        logger.info(
            f"✅ Listed {len(task_list)} {status} tasks for user {user_id}"
        )

        if not tasks:
            return {
                "count": 0,
                "tasks": [],
                "message": f"No {status} tasks found."
            }

        return {
            "count": len(task_list),
            "tasks": task_list,
            "message": f"Found {len(task_list)} {status} task(s)."
        }
    except Exception as e:
        logger.error(f"❌ Error listing tasks: {str(e)}")
        return {"error": f"Failed to list tasks: {str(e)}"}


async def complete_task(
    session: AsyncSession,
    user_id: str,
    task_id: Optional[int] = None,
    title: Optional[str] = None
) -> dict[str, Any]:
    """Mark a task as complete.

    Args:
        session: AsyncSession for database operations.
        user_id: Owner user ID (from JWT user_id claim).
        task_id: Task ID (required if title not provided).
        title: Task title (required if task_id not provided).

    Returns:
        Dictionary with confirmation message.

    Security:
        - Requires both task_id/title AND user_id match.
        - Prevents completing tasks owned by other users.
    """
    try:
        # Find task
        if task_id:
            stmt = select(Task).where(
                and_(Task.id == task_id, Task.user_id == user_id)
            )
        elif title:
            stmt = select(Task).where(
                and_(Task.title.ilike(f"%{title}%"), Task.user_id == user_id)
            )
        else:
            return {"error": "Either task_id or title must be provided"}

        result = await session.execute(stmt)
        task = result.scalars().first()

        if not task:
            return {"error": f"Task not found or not owned by you"}

        # Mark complete
        task.completed = True
        task.updated_at = datetime.utcnow()
        await session.flush()

        logger.info(f"✅ Completed task '{task.title}' (ID: {task.id}) for user {user_id}")
        return {
            "id": task.id,
            "title": task.title,
            "message": f"Task '{task.title}' marked as complete! ✓"
        }
    except Exception as e:
        logger.error(f"❌ Error completing task: {str(e)}")
        return {"error": f"Failed to complete task: {str(e)}"}


async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: Optional[int] = None,
    title: Optional[str] = None
) -> dict[str, Any]:
    """Delete a task.

    Args:
        session: AsyncSession for database operations.
        user_id: Owner user ID (from JWT user_id claim).
        task_id: Task ID (required if title not provided).
        title: Task title (required if task_id not provided).

    Returns:
        Dictionary with confirmation message.

    Security:
        - Requires both task_id/title AND user_id match.
        - Prevents deleting tasks owned by other users.
    """
    try:
        # Find task
        if task_id:
            stmt = select(Task).where(
                and_(Task.id == task_id, Task.user_id == user_id)
            )
        elif title:
            stmt = select(Task).where(
                and_(Task.title.ilike(f"%{title}%"), Task.user_id == user_id)
            )
        else:
            return {"error": "Either task_id or title must be provided"}

        result = await session.execute(stmt)
        task = result.scalars().first()

        if not task:
            return {"error": f"Task not found or not owned by you"}

        # Delete task
        await session.delete(task)
        await session.flush()

        logger.info(f"✅ Deleted task '{task.title}' (ID: {task.id}) for user {user_id}")
        return {
            "id": task.id,
            "title": task.title,
            "message": f"Task '{task.title}' deleted. It's gone! 🗑️"
        }
    except Exception as e:
        logger.error(f"❌ Error deleting task: {str(e)}")
        return {"error": f"Failed to delete task: {str(e)}"}


async def update_task(
    session: AsyncSession,
    user_id: str,
    task_id: Optional[int] = None,
    current_title: Optional[str] = None,
    new_title: Optional[str] = None,
    new_description: Optional[str] = None
) -> dict[str, Any]:
    """Update a task's title or description.

    Args:
        session: AsyncSession for database operations.
        user_id: Owner user ID (from JWT user_id claim).
        task_id: Task ID (required if current_title not provided).
        current_title: Current task title (required if task_id not provided).
        new_title: New task title (optional).
        new_description: New task description (optional).

    Returns:
        Dictionary with updated task info.

    Security:
        - Requires both task_id/current_title AND user_id match.
        - Prevents updating tasks owned by other users.
    """
    try:
        # Validate at least one field to update
        if not new_title and new_description is None:
            return {"error": "Either new_title or new_description must be provided"}

        # Find task
        if task_id:
            stmt = select(Task).where(
                and_(Task.id == task_id, Task.user_id == user_id)
            )
        elif current_title:
            stmt = select(Task).where(
                and_(Task.title.ilike(f"%{current_title}%"), Task.user_id == user_id)
            )
        else:
            return {"error": "Either task_id or current_title must be provided"}

        result = await session.execute(stmt)
        task = result.scalars().first()

        if not task:
            return {"error": f"Task not found or not owned by you"}

        # Update fields
        if new_title:
            if len(new_title) > 200:
                return {"error": "New title must be 200 characters or less"}
            task.title = new_title.strip()

        if new_description is not None:
            if len(new_description) > 2000:
                return {"error": "Description must be 2000 characters or less"}
            task.description = new_description.strip() if new_description else None

        task.updated_at = datetime.utcnow()
        await session.flush()

        logger.info(f"✅ Updated task (ID: {task.id}) for user {user_id}")
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "message": f"Task updated successfully!"
        }
    except Exception as e:
        logger.error(f"❌ Error updating task: {str(e)}")
        return {"error": f"Failed to update task: {str(e)}"}
