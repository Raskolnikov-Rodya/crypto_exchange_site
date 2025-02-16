import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import engine, SessionLocal
from app.models.user import User
from sqlalchemy.future import select
from app.core.security import get_password_hash

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)

    async with SessionLocal() as session:
        await seed_admin_user(session)

async def seed_admin_user(session: AsyncSession):
    """Create an admin user if none exists."""
    result = await session.execute(select(User).where(User.is_admin == True))
    admin_user = result.scalars().first()

    if not admin_user:
        new_admin = User(
            email="admin@crypto.com",
            hashed_password=get_password_hash("admin123"),  # Securely hash password
            is_admin=True
        )
        session.add(new_admin)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db())
 
