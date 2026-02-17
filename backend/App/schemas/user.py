from datetime import datetime

from pydantic import BaseModel

from App.models.user import Role


class UserOut(BaseModel):
    id: int
    email: str
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
