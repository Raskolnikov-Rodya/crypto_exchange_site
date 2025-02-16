from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create an Async Database Engine
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for Database Sessions
async def get_db():
    async with SessionLocal() as session:
        yield session
 
