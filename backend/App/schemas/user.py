from datetime import datetime

from pydantic import BaseModel

from App.models.user import Role


class UserOut(BaseModel):
    id: int
    email: str
    username: str | None = None
    phone: str | None = None
    role: Role
    created_at: datetime

    class Config:
        from_attributes = True


class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str | None = None
    phone: str | None = None


class UserUpdateRequest(BaseModel):
    email: str | None = None
    username: str | None = None
    phone: str | None = None


class PasswordUpdateRequest(BaseModel):
    current_password: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
