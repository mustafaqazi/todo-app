"""Integration tests for task API endpoints"""

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_session
from backend.main import app


@pytest.mark.asyncio
class TestTaskCreate:
    """Tests for task creation endpoint."""

    async def test_create_task_success(self, auth_header, test_session):
        """Test successful task creation."""
        # Override get_session dependency
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={
                    "title": "Test task",
                    "description": "Test description"
                },
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Test task"
        assert data["description"] == "Test description"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    async def test_create_task_without_auth(self, test_session):
        """Test task creation without authentication fails."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={"title": "Test task"}
            )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_create_task_invalid_title_empty(self, auth_header, test_session):
        """Test task creation with empty title fails."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={"title": ""},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_task_title_too_long(self, auth_header, test_session):
        """Test task creation with title > 200 chars fails."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={"title": "x" * 201},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_create_task_null_description_accepted(self, auth_header, test_session):
        """Test that null description is accepted."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/tasks",
                json={"title": "Test task", "description": None},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["description"] is None


@pytest.mark.asyncio
class TestTaskList:
    """Tests for task listing endpoint."""

    async def test_list_tasks_empty(self, auth_header, test_session):
        """Test listing tasks when none exist."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/tasks",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []

    async def test_list_tasks_with_status_all(self, auth_header, mock_task_1, mock_task_2, test_session):
        """Test listing all tasks."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/tasks?status=all",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 2

    async def test_list_tasks_filter_pending(self, auth_header, mock_task_1, mock_task_2, test_session):
        """Test filtering tasks by pending status."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/tasks?status=pending",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["completed"] is False

    async def test_list_tasks_filter_completed(self, auth_header, mock_task_1, mock_task_2, test_session):
        """Test filtering tasks by completed status."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/tasks?status=completed",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["completed"] is True

    async def test_list_tasks_user_isolation(
        self, auth_header, auth_header_user_2,
        mock_task_1, mock_task_user_2, test_session
    ):
        """Test that users only see their own tasks."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            # User 1 should see 1 task
            response = await client.get(
                "/api/tasks",
                headers=auth_header,
            )
            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()["items"]) == 1

            # User 2 should see 1 task (different one)
            response = await client.get(
                "/api/tasks",
                headers=auth_header_user_2,
            )
            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()["items"]) == 1

    async def test_list_tasks_without_auth(self, test_session):
        """Test listing tasks without authentication fails."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/tasks")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
class TestTaskGet:
    """Tests for getting a single task."""

    async def test_get_task_success(self, auth_header, mock_task_1, test_session):
        """Test getting a task successfully."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                f"/api/tasks/{mock_task_1.id}",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == mock_task_1.id
        assert data["title"] == "Buy groceries"

    async def test_get_task_not_found(self, auth_header, test_session):
        """Test getting non-existent task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/tasks/999",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_task_wrong_user(
        self, auth_header, auth_header_user_2,
        mock_task_user_2, test_session
    ):
        """Test getting another user's task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            # User 1 tries to get User 2's task
            response = await client.get(
                f"/api/tasks/{mock_task_user_2.id}",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_get_task_without_auth(self, mock_task_1, test_session):
        """Test getting task without authentication fails."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(f"/api/tasks/{mock_task_1.id}")

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
class TestTaskUpdate:
    """Tests for updating tasks."""

    async def test_update_task_title_success(self, auth_header, mock_task_1, test_session):
        """Test updating task title successfully."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(
                f"/api/tasks/{mock_task_1.id}",
                json={"title": "Updated title"},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated title"

    async def test_update_task_description(self, auth_header, mock_task_1, test_session):
        """Test updating task description."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(
                f"/api/tasks/{mock_task_1.id}",
                json={"description": "New description"},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["description"] == "New description"

    async def test_update_task_empty_title_fails(self, auth_header, mock_task_1, test_session):
        """Test updating with empty title fails."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(
                f"/api/tasks/{mock_task_1.id}",
                json={"title": ""},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_update_task_not_found(self, auth_header, test_session):
        """Test updating non-existent task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(
                "/api/tasks/999",
                json={"title": "Updated"},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_task_wrong_user(
        self, auth_header, mock_task_user_2, test_session
    ):
        """Test updating another user's task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.put(
                f"/api/tasks/{mock_task_user_2.id}",
                json={"title": "Hacked"},
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestTaskToggleComplete:
    """Tests for toggling task completion status."""

    async def test_toggle_complete_pending_to_done(self, auth_header, mock_task_1, test_session):
        """Test toggling pending task to completed."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.patch(
                f"/api/tasks/{mock_task_1.id}/complete",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["completed"] is True

    async def test_toggle_complete_done_to_pending(self, auth_header, mock_task_2, test_session):
        """Test toggling completed task to pending."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.patch(
                f"/api/tasks/{mock_task_2.id}/complete",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["completed"] is False

    async def test_toggle_complete_not_found(self, auth_header, test_session):
        """Test toggling non-existent task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.patch(
                "/api/tasks/999/complete",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_toggle_complete_wrong_user(
        self, auth_header, mock_task_user_2, test_session
    ):
        """Test toggling another user's task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.patch(
                f"/api/tasks/{mock_task_user_2.id}/complete",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestTaskDelete:
    """Tests for deleting tasks."""

    async def test_delete_task_success(self, auth_header, mock_task_1, test_session):
        """Test deleting a task successfully."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(
                f"/api/tasks/{mock_task_1.id}",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_delete_task_not_found(self, auth_header, test_session):
        """Test deleting non-existent task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(
                "/api/tasks/999",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_delete_task_wrong_user(
        self, auth_header, mock_task_user_2, test_session
    ):
        """Test deleting another user's task returns 404."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(
                f"/api/tasks/{mock_task_user_2.id}",
                headers=auth_header,
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
class TestHealthCheck:
    """Tests for health check endpoint."""

    async def test_health_check(self, test_session):
        """Test health check endpoint."""
        async def override_get_session():
            yield test_session

        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "ok"
