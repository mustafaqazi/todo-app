"""Application configuration and environment variables"""

import os
import warnings
from typing import Optional
from dotenv import load_dotenv

# Load .env file (skip in test mode)
if os.getenv("PYTEST_CURRENT_TEST") is None:
    load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./todo.db"
    )

    # JWT configuration
    BETTER_AUTH_SECRET: str = os.getenv(
        "BETTER_AUTH_SECRET",
        "default-secret-change-in-production"
    )
    JWT_ALGORITHM: str = "HS256"

    # CORS configuration - loaded from environment, falls back to development defaults
    ALLOWED_ORIGINS: list[str] = None  # Will be set in __post_init__ or __init__

    def __post_init__(self):
        """Parse CORS_ORIGINS from environment (comma-separated string)."""
        cors_env = os.getenv("CORS_ORIGINS", "")
        if cors_env:
            # Parse comma-separated origins and strip whitespace
            self.ALLOWED_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
        else:
            # Development defaults
            self.ALLOWED_ORIGINS = [
                "http://localhost:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3000",
            ]

    # API configuration
    API_PREFIX: str = "/api"
    TITLE: str = "TODO API"
    DESCRIPTION: str = "Secure FastAPI Backend with JWT & PostgreSQL"
    VERSION: str = "0.1.0"

    def __init__(self):
        """Validate recommended environment variables on init.

        Issues warnings if recommended environment variables are not properly set,
        but allows the application to start for development/testing purposes.
        """
        # Parse CORS_ORIGINS from environment
        self.__post_init__()

        # Warn about BETTER_AUTH_SECRET
        if not self.BETTER_AUTH_SECRET or self.BETTER_AUTH_SECRET == "default-secret-change-in-production":
            warnings.warn(
                "BETTER_AUTH_SECRET environment variable is not set or is using default. "
                "Set this to your actual Better Auth secret for production use. "
                "Export: BETTER_AUTH_SECRET=your-secret-key",
                UserWarning,
                stacklevel=2
            )

        # Warn about DATABASE_URL
        if self.DATABASE_URL == "postgresql+asyncpg://user:password@localhost/todo_db":
            warnings.warn(
                "DATABASE_URL environment variable is not set or is using default. "
                "Set this to your actual PostgreSQL connection string. "
                "Export: DATABASE_URL=postgresql+asyncpg://user:pass@host/db",
                UserWarning,
                stacklevel=2
            )


settings = Settings()
