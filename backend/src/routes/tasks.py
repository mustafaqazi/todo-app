"""Task CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.future import select
from sqlmodel import Session
from typing import List, Dict
from datetime import datetime

from ..db import get_session
from ..dependencies.auth import get_current_user
from ..models import Task
from ..schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.post("", status_code=201, response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: Dict[str, str] = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Create a new task for the authenticated user."""
    db_task = Task(
        user_id=current_user["user_id"],
        title=task_data.title,
        description=task_data.description,
    )
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: str = Query("all", regex="^(all|pending|completed)$"),
    current_user: Dict[str, str] = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[TaskResponse]:
    """List all tasks for the authenticated user with optional status filtering."""
    query = select(Task).where(Task.user_id == current_user["user_id"])

    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.get("/{id}", response_model=TaskResponse)
async def get_task(
    id: int,
    current_user: Dict[str, str] = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Get a specific task by ID (returns 404 if not owned by user)."""
    query = select(Task).where(
        Task.id == id,
        Task.user_id == current_user["user_id"],
    )
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    id: int,
    task_data: TaskUpdate,
    current_user: Dict[str, str] = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Update a task (full update with validation)."""
    query = select(Task).where(
        Task.id == id,
        Task.user_id == current_user["user_id"],
    )
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validate title if provided
    if task_data.title is not None:
        if not task_data.title or len(task_data.title) > 200:
            raise HTTPException(status_code=422, detail="Title must be 1-200 characters")
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task


@router.patch("/{id}/complete", response_model=TaskResponse)
async def toggle_complete(
    id: int,
    current_user: Dict[str, str] = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Toggle the completion status of a task."""
    query = select(Task).where(
        Task.id == id,
        Task.user_id == current_user["user_id"],
    )
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task


@router.delete("/{id}", status_code=204)
async def delete_task(
    id: int,
    current_user: Dict[str, str] = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> None:
    """Delete a task."""
    query = select(Task).where(
        Task.id == id,
        Task.user_id == current_user["user_id"],
    )
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
