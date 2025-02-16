from passlib.context import CryptContext
from fastapi import Depends, HTTPException
import re
from cryptography.fernet import Fernet
import os
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Generate and store encryption key securely (one-time setup)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())

cipher = Fernet(ENCRYPTION_KEY.encode())





def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def is_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return user
 
def validate_password_strength(password: str):
    """Enforces strong password rules"""
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Password must contain at least one number")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Creates a JWT token with expiration"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def decode_access_token(token: str):
    """Decodes and validates a JWT token"""
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

def encrypt_private_key(private_key: str) -> str:
    """Encrypts a private key before storing it."""
    return cipher.encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted_key: str) -> str:
    """Decrypts a private key before using it."""
    return cipher.decrypt(encrypted_key.encode()).decode()