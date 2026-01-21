# backend/app/database.py

import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from .models.user import Base  # Relative import from models/
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env file!")

# Async engine (shared across the app)
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,                  # Logs SQL — keep for now, disable in prod
    future=True,
    pool_pre_ping=True          # Helps with connection issues
)

# Async session factory (creates sessions on demand)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency for FastAPI: Provides a session per request
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency: Yields a DB session for the request, auto-closes after.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()