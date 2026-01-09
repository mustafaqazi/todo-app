"""Database connection and session management."""

import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# Load environment variables from .env file
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

# Create async engine with connection pooling
# Clean up the DATABASE_URL to remove psycopg-specific parameters and use asyncpg format
db_url = DATABASE_URL.replace('?sslmode=require&channel_binding=require', '').replace('?sslmode=require', '') if DATABASE_URL else ""

engine = create_async_engine(
    db_url or DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connection health
    connect_args={"ssl": True} if "neon" in (DATABASE_URL or "").lower() else {},
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    future=True,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session for route handlers."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
