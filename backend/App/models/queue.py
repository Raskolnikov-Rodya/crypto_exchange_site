from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String

from .base import Base


class WithdrawalQueue(Base):
    __tablename__ = "withdrawal_queue"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    coin = Column(String(10), nullable=False)
    amount = Column(Numeric(precision=36, scale=18), nullable=False)
    destination_address = Column(String(255), nullable=False)
    status = Column(String(30), default="pending", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
