from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from app.models.user import User
from app.db.session import get_user_db
from app.api.v1.endpoints.auth import get_jwt_strategy

router = APIRouter()

fastapi_users = FastAPIUsers(
    get_user_db,
    [get_jwt_strategy()],
    User,
)

@router.get("/all", dependencies=[Depends(is_admin)])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """Admin-only: Get all users."""
    result = await db.execute(select(User))
    return result.scalars().all()
    
# User Profile Endpoints
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["Users"])
