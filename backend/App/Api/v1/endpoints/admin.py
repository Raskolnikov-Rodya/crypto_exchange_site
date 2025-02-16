from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.trade import Trade
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.security import is_admin

router = APIRouter()

@router.get("/transactions", dependencies=[Depends(is_admin)])
async def get_all_transactions(db: AsyncSession = Depends(get_db)):
    """Admin-only: Get all transactions"""
    result = await db.execute(select(Trade))
    return result.scalars().all()

@router.post("/block_user/{user_id}", dependencies=[Depends(is_admin)])
async def block_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Admin-only: Block a user from making transactions."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user:
        return {"error": "User not found"}

    user.is_active = False
    await db.commit()
    return {"message": "User blocked successfully"}
