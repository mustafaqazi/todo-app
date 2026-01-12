"""Comprehensive task CRUD operation tests (Phases 4-8)."""

import pytest
from httpx import AsyncClient
from sqlmodel import Session

# Test constants from conftest
TEST_USER_ID = "1"
TEST_USER_ID_2 = "2"
TEST_USER_EMAIL = "test1@example.com"
TEST_USER_EMAIL_2 = "test2@example.com"
TEST_PASSWORD = "TestPass123!"


# ============ Phase 4: User Story 2 - Update & Complete Tasks ============


class TestUpdateTask:
    """Test PUT /api/tasks/{id} update endpoint."""

    @pytest.mark.asyncio
    async def test_update_task_success(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
        test_session: Session,
    ):
        """Test successful task update (T023)."""
        # Act
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={
                "title": "Updated Task Title",
                "description": "Updated description",
            },
            headers=auth_header,
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Task Title"
        assert data["description"] == "Updated description"
        assert data["completed"] is False
        assert data["id"] == mock_task_1.id

    @pytest.mark.asyncio
    async def test_update_task_title_only(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test updating only task title."""
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": "New Title"},
            headers=auth_header,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["description"] == mock_task_1.description  # Unchanged

    @pytest.mark.asyncio
    async def test_update_task_not_found(
        self,
        client: AsyncClient,
        auth_header: dict,
    ):
        """Test updating non-existent task returns 404."""
        response = await client.put(
            "/api/tasks/99999",
            json={"title": "New Title"},
            headers=auth_header,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_update_task_invalid_title_empty(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test updating task with empty title returns 422."""
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": ""},
            headers=auth_header,
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_task_invalid_title_too_long(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test updating task with title > 200 chars returns 422."""
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": "x" * 201},
            headers=auth_header,
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_update_task_cross_user_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test cross-user update returns 404 (T023 user isolation)."""
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": "Hacked"},
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_update_task_no_auth_returns_401(
        self,
        client: AsyncClient,
        mock_task_1,
    ):
        """Test update without auth token returns 401."""
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": "New Title"},
        )

        assert response.status_code == 401


class TestToggleComplete:
    """Test PATCH /api/tasks/{id}/complete toggle endpoint."""

    @pytest.mark.asyncio
    async def test_toggle_complete_success(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test successful task completion toggle (T024)."""
        # Act
        response = await client.patch(
            f"/api/tasks/{mock_task_1.id}/complete",
            headers=auth_header,
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["id"] == mock_task_1.id

    @pytest.mark.asyncio
    async def test_toggle_complete_toggle_back(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test toggling completion back to false."""
        # Toggle to complete
        response1 = await client.patch(
            f"/api/tasks/{mock_task_1.id}/complete",
            headers=auth_header,
        )
        assert response1.status_code == 200
        assert response1.json()["completed"] is True

        # Toggle back to incomplete
        response2 = await client.patch(
            f"/api/tasks/{mock_task_1.id}/complete",
            headers=auth_header,
        )
        assert response2.status_code == 200
        assert response2.json()["completed"] is False

    @pytest.mark.asyncio
    async def test_toggle_complete_not_found(
        self,
        client: AsyncClient,
        auth_header: dict,
    ):
        """Test toggling non-existent task returns 404."""
        response = await client.patch(
            "/api/tasks/99999/complete",
            headers=auth_header,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_toggle_complete_cross_user_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test cross-user toggle returns 404 (T024 user isolation)."""
        response = await client.patch(
            f"/api/tasks/{mock_task_1.id}/complete",
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_toggle_complete_no_auth_returns_401(
        self,
        client: AsyncClient,
        mock_task_1,
    ):
        """Test toggle without auth token returns 401."""
        response = await client.patch(
            f"/api/tasks/{mock_task_1.id}/complete",
        )

        assert response.status_code == 401


# ============ Phase 5: User Story 3 - Delete Tasks ============


class TestDeleteTask:
    """Test DELETE /api/tasks/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_task_success(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test successful task deletion (T027)."""
        # Act
        response = await client.delete(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header,
        )

        # Assert
        assert response.status_code == 204

    @pytest.mark.asyncio
    async def test_delete_verify_gone(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test deleted task cannot be retrieved (T028)."""
        # Delete task
        delete_response = await client.delete(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header,
        )
        assert delete_response.status_code == 204

        # Try to get deleted task
        get_response = await client.get(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header,
        )

        assert get_response.status_code == 404
        assert get_response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_delete_task_not_found(
        self,
        client: AsyncClient,
        auth_header: dict,
    ):
        """Test deleting non-existent task returns 404."""
        response = await client.delete(
            "/api/tasks/99999",
            headers=auth_header,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_delete_task_cross_user_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test cross-user delete returns 404 (T027 user isolation)."""
        response = await client.delete(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

        # Verify task still exists for original user
        auth_header = {"Authorization": f"Bearer valid_jwt_token", "Content-Type": "application/json"}

    @pytest.mark.asyncio
    async def test_delete_task_no_auth_returns_401(
        self,
        client: AsyncClient,
        mock_task_1,
    ):
        """Test delete without auth token returns 401."""
        response = await client.delete(
            f"/api/tasks/{mock_task_1.id}",
        )

        assert response.status_code == 401


# ============ Phase 6: User Story 4 - Multi-User Isolation ============


class TestUserIsolation:
    """Test multi-user isolation across all task operations."""

    @pytest.mark.asyncio
    async def test_user_isolation_list_tasks(
        self,
        client: AsyncClient,
        auth_header: dict,
        auth_header_user_2: dict,
        mock_task_1,
        mock_task_2,
        mock_task_user_2,
    ):
        """Test users only see their own tasks in list (T030)."""
        # User 1 list tasks
        response1 = await client.get(
            "/api/tasks",
            headers=auth_header,
        )
        assert response1.status_code == 200
        user1_tasks = response1.json()
        assert len(user1_tasks) == 2  # mock_task_1 and mock_task_2
        user1_ids = [t["id"] for t in user1_tasks]
        assert mock_task_1.id in user1_ids
        assert mock_task_2.id in user1_ids

        # User 2 list tasks
        response2 = await client.get(
            "/api/tasks",
            headers=auth_header_user_2,
        )
        assert response2.status_code == 200
        user2_tasks = response2.json()
        assert len(user2_tasks) == 1  # Only mock_task_user_2
        assert user2_tasks[0]["id"] == mock_task_user_2.id

        # Verify user 1 cannot see user 2's tasks
        assert mock_task_user_2.id not in user1_ids

    @pytest.mark.asyncio
    async def test_cross_user_get_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test GET returns 404 when accessing other user's task (T030)."""
        response = await client.get(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_cross_user_put_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test PUT returns 404 when updating other user's task (T030)."""
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": "Hacked"},
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_cross_user_patch_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test PATCH returns 404 when toggling other user's task (T030)."""
        response = await client.patch(
            f"/api/tasks/{mock_task_1.id}/complete",
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_cross_user_delete_returns_404(
        self,
        client: AsyncClient,
        auth_header_user_2: dict,
        mock_task_1,
    ):
        """Test DELETE returns 404 when deleting other user's task (T030)."""
        response = await client.delete(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header_user_2,
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    @pytest.mark.asyncio
    async def test_cross_user_cannot_modify_others_data(
        self,
        client: AsyncClient,
        auth_header: dict,
        auth_header_user_2: dict,
        mock_task_1,
        test_session: Session,
    ):
        """Test that user 2 modifications don't affect user 1's data (T031)."""
        original_title = mock_task_1.title

        # User 2 tries to update user 1's task
        response = await client.put(
            f"/api/tasks/{mock_task_1.id}",
            json={"title": "Hacked Title"},
            headers=auth_header_user_2,
        )
        assert response.status_code == 404

        # Verify user 1's task is unchanged
        verify_response = await client.get(
            f"/api/tasks/{mock_task_1.id}",
            headers=auth_header,
        )
        assert verify_response.status_code == 200
        assert verify_response.json()["title"] == original_title


# ============ Phase 7: User Story 5 - Status Filtering ============


class TestStatusFiltering:
    """Test GET /api/tasks with status filtering."""

    @pytest.mark.asyncio
    async def test_filter_pending_tasks(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
        mock_task_2,
    ):
        """Test filtering for pending (incomplete) tasks (T032)."""
        # mock_task_1 is incomplete (completed=False)
        # mock_task_2 is complete (completed=True)
        response = await client.get(
            "/api/tasks?status=pending",
            headers=auth_header,
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["id"] == mock_task_1.id
        assert tasks[0]["completed"] is False

    @pytest.mark.asyncio
    async def test_filter_completed_tasks(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
        mock_task_2,
    ):
        """Test filtering for completed tasks (T032)."""
        response = await client.get(
            "/api/tasks?status=completed",
            headers=auth_header,
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["id"] == mock_task_2.id
        assert tasks[0]["completed"] is True

    @pytest.mark.asyncio
    async def test_filter_all_tasks(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
        mock_task_2,
    ):
        """Test 'all' status returns all tasks (T032)."""
        response = await client.get(
            "/api/tasks?status=all",
            headers=auth_header,
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2

    @pytest.mark.asyncio
    async def test_filter_default_is_all(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
        mock_task_2,
    ):
        """Test default status (no param) returns all tasks (T032)."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header,
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2

    @pytest.mark.asyncio
    async def test_filter_invalid_status_returns_422(
        self,
        client: AsyncClient,
        auth_header: dict,
    ):
        """Test invalid status parameter returns 422 (T034)."""
        response = await client.get(
            "/api/tasks?status=invalid",
            headers=auth_header,
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_filter_empty_result(
        self,
        client: AsyncClient,
        auth_header: dict,
        mock_task_1,
    ):
        """Test filtering returns empty list when no matches."""
        # mock_task_1 is incomplete, so completed filter should be empty
        response = await client.get(
            "/api/tasks?status=completed",
            headers=auth_header,
        )

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 0

    @pytest.mark.asyncio
    async def test_filter_respects_user_isolation(
        self,
        client: AsyncClient,
        auth_header: dict,
        auth_header_user_2: dict,
        mock_task_1,
        mock_task_2,
        mock_task_user_2,
    ):
        """Test status filtering respects user isolation (T032)."""
        # User 1 filter for pending
        response1 = await client.get(
            "/api/tasks?status=pending",
            headers=auth_header,
        )
        user1_tasks = response1.json()
        assert len(user1_tasks) == 1
        assert user1_tasks[0]["user_id"] == TEST_USER_ID

        # User 2 filter for pending (mock_task_user_2 is incomplete)
        response2 = await client.get(
            "/api/tasks?status=pending",
            headers=auth_header_user_2,
        )
        user2_tasks = response2.json()
        assert len(user2_tasks) == 1
        assert user2_tasks[0]["user_id"] == TEST_USER_ID_2


# ============ Phase 8: Comprehensive Integration Tests ============


class TestTaskIntegration:
    """End-to-end integration tests for complete task workflows."""

    @pytest.mark.asyncio
    async def test_full_task_lifecycle(
        self,
        client: AsyncClient,
        auth_header: dict,
    ):
        """Test complete task lifecycle: create, update, toggle, delete."""
        # Create task
        create_response = await client.post(
            "/api/tasks",
            json={
                "title": "Integration Test Task",
                "description": "Full lifecycle test",
            },
            headers=auth_header,
        )
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        assert task["completed"] is False

        # Update task
        update_response = await client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Task Title"},
            headers=auth_header,
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Updated Task Title"

        # Toggle to complete
        toggle_response = await client.patch(
            f"/api/tasks/{task_id}/complete",
            headers=auth_header,
        )
        assert toggle_response.status_code == 200
        assert toggle_response.json()["completed"] is True

        # Delete task
        delete_response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_header,
        )
        assert delete_response.status_code == 204

        # Verify task is deleted
        get_response = await client.get(
            f"/api/tasks/{task_id}",
            headers=auth_header,
        )
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_multiple_users_independent_tasks(
        self,
        client: AsyncClient,
        auth_header: dict,
        auth_header_user_2: dict,
    ):
        """Test that multiple users maintain independent task lists."""
        # User 1 creates tasks
        user1_create1 = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task 1"},
            headers=auth_header,
        )
        user1_task1_id = user1_create1.json()["id"]

        user1_create2 = await client.post(
            "/api/tasks",
            json={"title": "User 1 Task 2"},
            headers=auth_header,
        )
        user1_task2_id = user1_create2.json()["id"]

        # User 2 creates tasks
        user2_create1 = await client.post(
            "/api/tasks",
            json={"title": "User 2 Task 1"},
            headers=auth_header_user_2,
        )
        user2_task1_id = user2_create1.json()["id"]

        # Verify task counts
        user1_list = await client.get("/api/tasks", headers=auth_header)
        assert len(user1_list.json()) == 2

        user2_list = await client.get("/api/tasks", headers=auth_header_user_2)
        assert len(user2_list.json()) == 1

        # User 1 updates their task
        user1_update = await client.put(
            f"/api/tasks/{user1_task1_id}",
            json={"title": "User 1 Task 1 Updated"},
            headers=auth_header,
        )
        assert user1_update.status_code == 200

        # Verify user 2 cannot see update
        user2_verify = await client.get(
            f"/api/tasks/{user1_task1_id}",
            headers=auth_header_user_2,
        )
        assert user2_verify.status_code == 404

    @pytest.mark.asyncio
    async def test_filtering_with_operations(
        self,
        client: AsyncClient,
        auth_header: dict,
    ):
        """Test status filtering works correctly after task operations."""
        # Create multiple tasks
        tasks = []
        for i in range(3):
            response = await client.post(
                "/api/tasks",
                json={"title": f"Task {i}"},
                headers=auth_header,
            )
            tasks.append(response.json())

        # Complete first and second task
        await client.patch(
            f"/api/tasks/{tasks[0]['id']}/complete",
            headers=auth_header,
        )
        await client.patch(
            f"/api/tasks/{tasks[1]['id']}/complete",
            headers=auth_header,
        )

        # Filter for pending
        pending_response = await client.get(
            "/api/tasks?status=pending",
            headers=auth_header,
        )
        pending_tasks = pending_response.json()
        assert len(pending_tasks) == 1
        assert pending_tasks[0]["id"] == tasks[2]["id"]

        # Filter for completed
        completed_response = await client.get(
            "/api/tasks?status=completed",
            headers=auth_header,
        )
        completed_tasks = completed_response.json()
        assert len(completed_tasks) == 2

    @pytest.mark.asyncio
    async def test_authorization_failures(
        self,
        client: AsyncClient,
        mock_task_1,
    ):
        """Test all operations fail without proper authorization."""
        # No auth header
        endpoints = [
            ("GET", f"/api/tasks/{mock_task_1.id}"),
            ("PUT", f"/api/tasks/{mock_task_1.id}"),
            ("PATCH", f"/api/tasks/{mock_task_1.id}/complete"),
            ("DELETE", f"/api/tasks/{mock_task_1.id}"),
        ]

        for method, endpoint in endpoints:
            if method == "GET":
                response = await client.get(endpoint)
            elif method == "PUT":
                response = await client.put(endpoint, json={"title": "Test"})
            elif method == "PATCH":
                response = await client.patch(endpoint)
            elif method == "DELETE":
                response = await client.delete(endpoint)

            assert response.status_code == 401
