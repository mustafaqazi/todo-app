"""Database connection and session management"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlmodel import SQLModel

from config import settings


def create_engine():
    """Create async engine based on database type."""

    # SQLite (development)
    if settings.DATABASE_URL.startswith("sqlite"):
        return create_async_engine(
            settings.DATABASE_URL,
            echo=True,
            future=True,
        )

    # PostgreSQL (production / Neon / Render)
    return create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        future=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        connect_args={
            "timeout": 10,
            "command_timeout": 10,
            "ssl": "require",
        },
    )


engine = create_engine()

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to inject database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_tables() -> None:
    """Create all SQLModel tables on application startup."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db() -> None:
    """Close database connection pool on application shutdown."""
    await engine.dispose()
