"""Task CRUD API endpoints"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from db import get_session
from dependencies import get_current_user
from src.models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="List user's tasks",
    description="Retrieve all tasks for the authenticated user, optionally filtered by status.",
)
async def list_tasks(
    current_user: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    status_param: str = Query(
        "all",
        alias="status",
        regex="^(all|pending|completed)$",
        description="Filter tasks by status: all, pending, or completed"
    ),
) -> TaskListResponse:
    """
    List tasks for the authenticated user.

    Query Parameters:
    - status: Filter by status (all, pending, completed) - default: all

    Returns:
        TaskListResponse with list of TaskResponse objects

    Raises:
        HTTPException: 401 if not authenticated
    """
    user_id = current_user["user_id"]

    try:
        # Build query with user filter
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status_param == "pending":
            query = query.where(Task.completed == False)
        elif status_param == "completed":
            query = query.where(Task.completed == True)
        # If "all", no additional filter

        # Execute query and order by created_at DESC
        result = await session.execute(query.order_by(Task.created_at.desc()))
        tasks = result.scalars().all()

        return TaskListResponse(items=tasks)

    except Exception as e:
        logger.error(f"Failed to list tasks for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific task",
    description="Retrieve a single task by ID (must be owned by the authenticated user).",
)
async def get_task(
    task_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Get a specific task by ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        TaskResponse with the task details

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 404 if task not found or not owned by user
    """
    user_id = current_user["user_id"]

    try:
        # Query with user_id filter to ensure ownership
        query = select(Task).where(
            (Task.id == task_id) & (Task.user_id == user_id)
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task for the authenticated user.",
)
async def create_task(
    body: TaskCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Create a new task.

    Args:
        body: TaskCreate schema with title and optional description

    Returns:
        TaskResponse with the created task details (201 Created)

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 422 if validation fails
    """
    user_id = current_user["user_id"]

    try:
        # Create task with user_id from JWT
        task = Task(
            user_id=user_id,
            title=body.title,
            description=body.description,
            completed=False,
        )

        session.add(task)
        await session.flush()  # Flush to get the generated ID
        await session.commit()

        logger.info(f"Created task {task.id} for user {user_id}")
        return task

    except ValueError as e:
        logger.warning(f"Validation error creating task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to create task for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a task",
    description="Update a task (must be owned by the authenticated user).",
)
async def update_task(
    task_id: int,
    body: TaskUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Update a task.

    Args:
        task_id: The ID of the task to update
        body: TaskUpdate schema with optional title and description

    Returns:
        TaskResponse with the updated task details

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 404 if task not found or not owned by user
        HTTPException: 422 if validation fails
    """
    user_id = current_user["user_id"]

    try:
        # Query with user_id filter to ensure ownership
        query = select(Task).where(
            (Task.id == task_id) & (Task.user_id == user_id)
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update fields if provided
        if body.title is not None:
            task.title = body.title
        if body.description is not None:
            task.description = body.description

        # Update timestamp
        task.updated_at = datetime.utcnow()

        session.add(task)
        await session.commit()

        logger.info(f"Updated task {task_id} for user {user_id}")
        return task

    except HTTPException:
        raise
    except ValueError as e:
        await session.rollback()
        logger.warning(f"Validation error updating task {task_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to update task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Toggle task completion status",
    description="Toggle the completed flag of a task (must be owned by the authenticated user).",
)
async def toggle_task_complete(
    task_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """
    Toggle the completion status of a task.

    Args:
        task_id: The ID of the task to toggle

    Returns:
        TaskResponse with the updated task (completed status toggled)

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 404 if task not found or not owned by user
    """
    user_id = current_user["user_id"]

    try:
        # Query with user_id filter to ensure ownership
        query = select(Task).where(
            (Task.id == task_id) & (Task.user_id == user_id)
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Toggle completion status
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        await session.commit()

        logger.info(f"Toggled task {task_id} completion to {task.completed} for user {user_id}")
        return task

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to toggle task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task (must be owned by the authenticated user).",
)
async def delete_task(
    task_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a task.

    Args:
        task_id: The ID of the task to delete

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 401 if not authenticated
        HTTPException: 404 if task not found or not owned by user
    """
    user_id = current_user["user_id"]

    try:
        # Query with user_id filter to ensure ownership
        query = select(Task).where(
            (Task.id == task_id) & (Task.user_id == user_id)
        )
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        await session.delete(task)
        await session.commit()

        logger.info(f"Deleted task {task_id} for user {user_id}")

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        logger.error(f"Failed to delete task {task_id} for user {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )
