"""Comprehensive tests for authentication endpoints."""

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
class TestSignup:
    """Tests for user signup endpoint."""

    async def test_signup_success(self, client: AsyncClient) -> None:
        """Test successful user signup."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    async def test_signup_duplicate_email(self, client: AsyncClient) -> None:
        """Test signup with duplicate email returns 409 Conflict."""
        email = "duplicate@example.com"
        password = "SecurePass123!"

        # First signup should succeed
        response1 = await client.post(
            "/api/auth/signup",
            json={"email": email, "password": password}
        )
        assert response1.status_code == status.HTTP_201_CREATED

        # Second signup with same email should fail
        response2 = await client.post(
            "/api/auth/signup",
            json={"email": email, "password": password}
        )
        assert response2.status_code == status.HTTP_409_CONFLICT
        assert "already registered" in response2.json()["detail"].lower()

    async def test_signup_weak_password_too_short(self, client: AsyncClient) -> None:
        """Test signup with password < 8 chars returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "user@example.com",
                "password": "Short1!"  # Only 7 chars
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_weak_password_no_uppercase(self, client: AsyncClient) -> None:
        """Test signup with no uppercase letter returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "user@example.com",
                "password": "nouppercase123"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_weak_password_no_lowercase(self, client: AsyncClient) -> None:
        """Test signup with no lowercase letter returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "user@example.com",
                "password": "NOLOWERCASE123"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_weak_password_no_digit(self, client: AsyncClient) -> None:
        """Test signup with no digit returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "user@example.com",
                "password": "NoDigitPassword"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_invalid_email(self, client: AsyncClient) -> None:
        """Test signup with invalid email format returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={
                "email": "not-an-email",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_missing_email(self, client: AsyncClient) -> None:
        """Test signup without email returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={"password": "SecurePass123!"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_signup_missing_password(self, client: AsyncClient) -> None:
        """Test signup without password returns 422."""
        response = await client.post(
            "/api/auth/signup",
            json={"email": "user@example.com"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestLogin:
    """Tests for user login endpoint."""

    async def test_login_success(self, mock_user_1: object, client: AsyncClient) -> None:
        """Test successful login."""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test1@example.com",
                "password": "TestPass123!"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user_id" in data

    async def test_login_wrong_password(self, mock_user_1: object, client: AsyncClient) -> None:
        """Test login with wrong password returns 401."""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "test1@example.com",
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in response.json()["detail"].lower()

    async def test_login_nonexistent_email(self, client: AsyncClient) -> None:
        """Test login with non-existent email returns 401."""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid" in response.json()["detail"].lower()

    async def test_login_invalid_email_format(self, client: AsyncClient) -> None:
        """Test login with invalid email format returns 422."""
        response = await client.post(
            "/api/auth/login",
            json={
                "email": "not-an-email",
                "password": "SecurePass123!"
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_login_missing_email(self, client: AsyncClient) -> None:
        """Test login without email returns 422."""
        response = await client.post(
            "/api/auth/login",
            json={"password": "SecurePass123!"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_login_missing_password(self, client: AsyncClient) -> None:
        """Test login without password returns 422."""
        response = await client.post(
            "/api/auth/login",
            json={"email": "user@example.com"}
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestVerify:
    """Tests for token verification endpoint."""

    async def test_verify_valid_token(self, valid_jwt_token: str, client: AsyncClient) -> None:
        """Test verifying a valid token."""
        response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is True
        assert data["user_id"] == "1"

    async def test_verify_invalid_token(self, invalid_jwt_token: str, client: AsyncClient) -> None:
        """Test verifying an invalid token."""
        response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {invalid_jwt_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False
        assert data["user_id"] is None

    async def test_verify_expired_token(self, expired_jwt_token: str, client: AsyncClient) -> None:
        """Test verifying an expired token."""
        response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {expired_jwt_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False
        assert data["user_id"] is None

    async def test_verify_missing_header(self, client: AsyncClient) -> None:
        """Test verify without Authorization header."""
        response = await client.get("/api/auth/verify")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False
        assert data["user_id"] is None

    async def test_verify_malformed_header(self, client: AsyncClient) -> None:
        """Test verify with malformed Authorization header."""
        response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": "InvalidFormat token"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False

    async def test_verify_wrong_secret(self, jwt_token_wrong_secret: str, client: AsyncClient) -> None:
        """Test verifying token signed with different secret."""
        response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {jwt_token_wrong_secret}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False
        assert data["user_id"] is None

    async def test_verify_missing_sub_claim(self, jwt_token_missing_user_id: str, client: AsyncClient) -> None:
        """Test verifying token without 'sub' claim."""
        response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {jwt_token_missing_user_id}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["valid"] is False
        assert data["user_id"] is None


@pytest.mark.asyncio
class TestAuthFlow:
    """Integration tests for complete authentication flow."""

    async def test_full_signup_and_login_flow(self, client: AsyncClient) -> None:
        """Test complete signup and login workflow."""
        email = "integration@example.com"
        password = "IntegrationPass123!"

        # Signup
        signup_response = await client.post(
            "/api/auth/signup",
            json={"email": email, "password": password}
        )
        assert signup_response.status_code == status.HTTP_201_CREATED
        signup_data = signup_response.json()
        signup_token = signup_data["access_token"]
        signup_user_id = signup_data["user_id"]

        # Verify signup token
        verify_response = await client.get(
            "/api/auth/verify",
            headers={"Authorization": f"Bearer {signup_token}"}
        )
        assert verify_response.status_code == status.HTTP_200_OK
        verify_data = verify_response.json()
        assert verify_data["valid"] is True
        assert verify_data["user_id"] == signup_user_id

        # Login
        login_response = await client.post(
            "/api/auth/login",
            json={"email": email, "password": password}
        )
        assert login_response.status_code == status.HTTP_200_OK
        login_data = login_response.json()
        assert login_data["user_id"] == signup_user_id

    async def test_signup_then_create_task_flow(self, client: AsyncClient) -> None:
        """Test signup, then use token to create a task."""
        # Signup
        signup_response = await client.post(
            "/api/auth/signup",
            json={
                "email": "taskuser@example.com",
                "password": "TaskPass123!"
            }
        )
        assert signup_response.status_code == status.HTTP_201_CREATED
        token = signup_response.json()["access_token"]

        # Create task with token
        task_response = await client.post(
            "/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Test Task", "description": "Created after signup"}
        )
        assert task_response.status_code == status.HTTP_201_CREATED
        task_data = task_response.json()
        assert task_data["title"] == "Test Task"
        assert task_data["completed"] is False
