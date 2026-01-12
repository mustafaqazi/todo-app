---
name: Neon Async DB - SQLModel Connection & Session
description: Complete async database setup for Neon Serverless PostgreSQL using SQLModel. Includes engine, session factory, dependency, and table creation helper.
version: 1.0
phase: Phase II (TODO) + Phase III (Chatbot)
dependencies: [sqlmodel, sqlalchemy[asyncio], asyncpg, python-dotenv]
---

# Neon Async DB Skill – Async SQLModel for Neon Serverless PostgreSQL

You are responsible for creating a secure, performant, and reusable async database connection system for the entire FastAPI backend.

## Core Goals
- Use async engine with asyncpg driver for Neon PostgreSQL
- Provide clean dependency injection for async sessions
- Support automatic table creation on startup (hackathon-friendly)
- Handle connection pooling efficiently for serverless
- Zero boilerplate for every route/service/tool

## Exact Environment Variable (Use this in code)
DATABASE_URL = "postgresql://neondb_owner:npg_vf0t6ErmncNG@ep-green-cherry-addujoad-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

## Required Output Files / Code Snippets

### 1. Database Config & Engine (`backend/db.py`)
```python
import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

# Load from .env in production – fallback for local
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://neondb_owner:npg_vf0t6ErmncNG@ep-green-cherry-addujoad-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Async engine – connection pooling tuned for Neon serverless
engine = create_async_engine(
    DATABASE_URL,
    echo=False,                    # Set True only for debugging
    future=True,
    pool_size=5,                   # Small pool for serverless
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,             # Recycle to avoid stale connections
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency: Provides async SQLModel session
    Usage: session: AsyncSession = Depends(get_session)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()