from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.database import get_db
from App.dependencies import require_admin
from App.models.user import Role, User

router = APIRouter()


class UserPublic(BaseModel):
    id: int
    email: str
    role: Role

    class Config:
        from_attributes = True


@router.get("/", response_model=list[UserPublic])
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)) -> list[User]:
    result = await db.execute(select(User).order_by(User.id.asc()))
    return list(result.scalars().all())
