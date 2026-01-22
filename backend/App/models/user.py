# backend/app/models/user.py

from .base import Base
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
# At top
from datetime import datetime
from zoneinfo import ZoneInfo
import pytz  # or from zoneinfo import ZoneInfo in Python 3.9+


#Base = declarative_base()  # All models inherit from this

class Role(str, PyEnum):
    USER = "user"
    ADMIN = "admin"
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default="user", nullable=False)
    #is_active = Column(Boolean, default=True, nullable=False)
    # Fixed: timezone-aware UTC default
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC), nullable=False)
    
    balances = relationship("Balance", back_populates="user")
    # In user.py, add (optional):
    transactions = relationship("Transaction", back_populates="user")
    
    def __repr__(self):
         return f"<user(email='{self.email}', role='{self.role}')>"