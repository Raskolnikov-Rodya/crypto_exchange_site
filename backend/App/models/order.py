from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    side = Column(String(10), nullable=False)
    symbol = Column(String(20), nullable=False, index=True)
    price = Column(Numeric(precision=36, scale=18), nullable=False)
    amount = Column(Numeric(precision=36, scale=18), nullable=False)
    status = Column(String(20), default="open", nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="orders")
