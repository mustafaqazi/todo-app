"""Application configuration and environment variables"""

import os
import warnings
from typing import Optional


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

    # CORS configuration
    ALLOWED_ORIGINS: list[str] = [
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
