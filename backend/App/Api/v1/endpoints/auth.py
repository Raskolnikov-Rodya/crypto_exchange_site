from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import or_, select, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from App.core.security import create_access_token, decode_access_token, get_password_hash, validate_password_strength, verify_password
from App.database import get_db
from App.models.user import Role, User
from App.schemas.user import RegisterRequest, TokenResponse, UserOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

MIGRATION_HINT = "Database schema is out of date. Run: alembic upgrade head"


def _is_users_profile_column_error(exc: ProgrammingError) -> bool:
    message = str(getattr(exc, "orig", exc)).lower()
    return "column users.username does not exist" in message or "column users.phone does not exist" in message


async def _self_heal_user_profile_columns(db: AsyncSession) -> None:
    # Safety net for environments where migrations were skipped.
    await db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(50)"))
    await db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(25)"))
    await db.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users (username)"))
    await db.commit()


async def _safe_execute(db: AsyncSession, statement):
    try:
        return await db.execute(statement)
    except ProgrammingError as exc:
        if _is_users_profile_column_error(exc):
            try:
                await db.rollback()
                await _self_heal_user_profile_columns(db)
                return await db.execute(statement)
            except Exception as heal_exc:  # noqa: BLE001 - we convert to actionable API error
                raise HTTPException(status_code=503, detail=MIGRATION_HINT) from heal_exc
        raise


async def _safe_commit(db: AsyncSession) -> None:
    try:
        await db.commit()
    except ProgrammingError as exc:
        if _is_users_profile_column_error(exc):
            try:
                await db.rollback()
                await _self_heal_user_profile_columns(db)
                await db.commit()
                return
            except Exception as heal_exc:  # noqa: BLE001 - we convert to actionable API error
                raise HTTPException(status_code=503, detail=MIGRATION_HINT) from heal_exc
        raise


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    result = await _safe_execute(db, select(User).where(User.email == payload["sub"]))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> User:
    validate_password_strength(payload.password)

    clauses = [User.email == payload.email]
    if payload.username:
        clauses.append(User.username == payload.username)

    existing = await _safe_execute(db, select(User).where(or_(*clauses)))
    found = existing.scalar_one_or_none()
    if found:
        if found.email == payload.email:
            raise HTTPException(status_code=400, detail="Email already exists")
        raise HTTPException(status_code=400, detail="Username already exists")

    user = User(
        email=payload.email,
        username=payload.username,
        phone=payload.phone,
        hashed_password=get_password_hash(payload.password),
        role=Role.USER,
    )
    db.add(user)
    await _safe_commit(db)
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await _safe_execute(db, select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": user.role.value})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
