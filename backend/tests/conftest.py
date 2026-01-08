"""Pytest configuration and fixtures for testing."""

import pytest
import jwt
from datetime import datetime, timedelta
from typing import AsyncGenerator, Dict, Any

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Import app and dependencies
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import app
from src.db import get_session
from src.config import settings
from src.models import Task, User

# ============ Test Configuration ============

# Use in-memory SQLite for all tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Set test JWT secret before creating fixtures
TEST_SECRET = "test-secret-key-for-jwt"
settings.BETTER_AUTH_SECRET = TEST_SECRET

# Test user identifiers
TEST_USER_ID = "1"  # Database ID as string
TEST_USER_ID_2 = "2"
TEST_USER_EMAIL = "test1@example.com"
TEST_USER_EMAIL_2 = "test2@example.com"
TEST_PASSWORD = "TestPass123!"

# Ensure metadata is set to allow extend_existing
SQLModel.metadata.extend_existing = True


# ============ Session & Secret Fixtures ============


@pytest.fixture(scope="session")
def test_secret() -> str:
    """Return test JWT secret."""
    return TEST_SECRET


@pytest.fixture(scope="session")
def test_user_id() -> str:
    """Return test user ID."""
    return TEST_USER_ID


@pytest.fixture(scope="session")
def test_user_id_2() -> str:
    """Return second test user ID."""
    return TEST_USER_ID_2


# ============ JWT Token Fixtures ============


@pytest.fixture
def valid_jwt_token(test_user_id: str, test_secret: str) -> str:
    """Generate a valid JWT token with 'sub' claim (standard JWT)."""
    payload = {
        "sub": test_user_id,  # Standard JWT claim for subject (user ID)
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, test_secret, algorithm="HS256")


@pytest.fixture
def valid_jwt_token_user_2(test_user_id_2: str, test_secret: str) -> str:
    """Generate a valid JWT token for second user."""
    payload = {
        "sub": test_user_id_2,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, test_secret, algorithm="HS256")


@pytest.fixture
def expired_jwt_token(test_user_id: str, test_secret: str) -> str:
    """Generate an expired JWT token."""
    payload = {
        "sub": test_user_id,
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    return jwt.encode(payload, test_secret, algorithm="HS256")


@pytest.fixture
def invalid_jwt_token() -> str:
    """Return an invalid JWT token."""
    return "invalid.token.here"


@pytest.fixture
def jwt_token_missing_user_id(test_secret: str) -> str:
    """Generate JWT token without 'sub' claim."""
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, test_secret, algorithm="HS256")


@pytest.fixture
def jwt_token_wrong_secret(test_user_id: str) -> str:
    """Generate JWT token signed with wrong secret."""
    payload = {
        "sub": test_user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, "wrong-secret", algorithm="HS256")


# ============ Database Fixtures ============


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh test database session per test."""
    # Create in-memory SQLite engine
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    # Create fresh tables for this test
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session factory
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create and yield session
    async with async_session() as session:
        yield session

    # Cleanup: drop tables and dispose engine
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def test_session(test_db: AsyncSession) -> AsyncSession:
    """Alias for test_db fixture."""
    return test_db


# ============ Client Fixtures ============


@pytest.fixture
async def client(test_db: AsyncSession, test_secret: str) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with mocked database and JWT secret."""

    # Override get_session to use test database
    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    # Save original secret and override for testing
    original_secret = settings.BETTER_AUTH_SECRET
    settings.BETTER_AUTH_SECRET = test_secret

    try:
        app.dependency_overrides[get_session] = override_get_session

        async with AsyncClient(app=app, base_url="http://test") as test_client:
            yield test_client
    finally:
        # Restore original settings
        app.dependency_overrides.clear()
        settings.BETTER_AUTH_SECRET = original_secret


# ============ Authorization Headers ============


@pytest.fixture
async def auth_header(valid_jwt_token: str) -> Dict[str, str]:
    """Authenticated request headers for user 1."""
    return {
        "Authorization": f"Bearer {valid_jwt_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
async def authenticated_headers(valid_jwt_token: str) -> Dict[str, str]:
    """Alias for auth_header fixture."""
    return {
        "Authorization": f"Bearer {valid_jwt_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
async def auth_header_user_2(valid_jwt_token_user_2: str) -> Dict[str, str]:
    """Authenticated request headers for user 2."""
    return {
        "Authorization": f"Bearer {valid_jwt_token_user_2}",
        "Content-Type": "application/json",
    }


@pytest.fixture
async def authenticated_headers_user_2(valid_jwt_token_user_2: str) -> Dict[str, str]:
    """Return authenticated request headers for second user."""
    return {
        "Authorization": f"Bearer {valid_jwt_token_user_2}",
        "Content-Type": "application/json",
    }


# ============ Mock Objects ============


@pytest.fixture
async def mock_task_1(test_session: AsyncSession) -> Task:
    """Create a mock task for user 1."""
    task = Task(
        user_id=TEST_USER_ID,
        title="Test Task 1",
        description="First test task",
        completed=False,
    )
    test_session.add(task)
    await test_session.flush()
    return task


@pytest.fixture
async def mock_task_2(test_session: AsyncSession) -> Task:
    """Create a second mock task for user 1."""
    task = Task(
        user_id=TEST_USER_ID,
        title="Test Task 2",
        description="Second test task",
        completed=True,
    )
    test_session.add(task)
    await test_session.flush()
    return task


@pytest.fixture
async def mock_task_user_2(test_session: AsyncSession) -> Task:
    """Create a mock task for user 2."""
    task = Task(
        user_id=TEST_USER_ID_2,
        title="Test Task User 2",
        description="Task belonging to user 2",
        completed=False,
    )
    test_session.add(task)
    await test_session.flush()
    return task


@pytest.fixture
async def mock_user_1(test_session: AsyncSession) -> User:
    """Create a mock user."""
    from src.utils.password import hash_password

    user = User(
        email=TEST_USER_EMAIL,
        hashed_password=hash_password(TEST_PASSWORD),
    )
    test_session.add(user)
    await test_session.flush()
    return user


@pytest.fixture
async def mock_user_2(test_session: AsyncSession) -> User:
    """Create a second mock user."""
    from src.utils.password import hash_password

    user = User(
        email=TEST_USER_EMAIL_2,
        hashed_password=hash_password(TEST_PASSWORD),
    )
    test_session.add(user)
    await test_session.flush()
    return user
