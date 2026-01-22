from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user import User

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    coin = Column(String(10), nullable=False)
    amount = Column(Numeric(precision=36, scale=18), nullable=False)
    type = Column(String, nullable=False)  # "deposit", "withdrawal", "trade_buy", "trade_sell"
    status = Column(String, default="pending", nullable=False)  # "pending", "approved", "rejected", "completed"
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("UTC")), nullable=False)

    user = relationship("User")

# In user.py, add (optional):
transactions = relationship("Transaction", back_populates="user")