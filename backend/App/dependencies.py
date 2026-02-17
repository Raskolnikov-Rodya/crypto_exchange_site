from fastapi import Depends, HTTPException

from App.Api.v1.endpoints.auth import get_current_user
from App.models.user import Role, User


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
