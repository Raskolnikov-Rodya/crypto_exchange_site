from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy
from app.core.config import settings
from app.models.user import User  # Your User model
from app.db.session import get_user_db  # User database dependency

router = APIRouter()

# JWT Authentication Strategy
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)

# FastAPI Users Instance
fastapi_users = FastAPIUsers(
    get_user_db,
    [get_jwt_strategy()],
    User,
)

# Authentication Endpoints
router.include_router(
    fastapi_users.get_auth_router(get_jwt_strategy()), prefix="/auth/jwt", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_users_router(), prefix="/users", tags=["Users"]
)
