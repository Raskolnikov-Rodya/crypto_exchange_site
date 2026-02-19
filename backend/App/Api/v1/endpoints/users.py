from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.Api.v1.endpoints.auth import get_current_user
from App.core.security import get_password_hash, validate_password_strength, verify_password
from App.database import get_db
from App.dependencies import require_admin
from App.models.user import User
from App.schemas.user import PasswordUpdateRequest, UserOut, UserUpdateRequest

router = APIRouter()


@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)) -> list[User]:
    result = await db.execute(select(User).order_by(User.id.asc()))
    return list(result.scalars().all())


@router.get("/me", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/me", response_model=UserOut)
async def update_profile(
    payload: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    if payload.email is not None and payload.email != current_user.email:
        exists = await db.execute(select(User).where(User.email == payload.email, User.id != current_user.id))
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists")
        current_user.email = payload.email

    if payload.username is not None and payload.username != current_user.username:
        exists = await db.execute(select(User).where(User.username == payload.username, User.id != current_user.id))
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")
        current_user.username = payload.username

    if payload.phone is not None:
        current_user.phone = payload.phone

    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.post("/me/password")
async def update_password(
    payload: PasswordUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    validate_password_strength(payload.new_password)
    current_user.hashed_password = get_password_hash(payload.new_password)
    await db.commit()
    return {"message": "Password updated"}
