from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trade_type = Column(String, nullable=False)  # "buy" or "sell"
    symbol = Column(String, nullable=False)  # e.g., "BTC/USDT"
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    status = Column(String, default="pending")  # "pending", "completed", "fraud"

    user = relationship("User", back_populates="trades")
 
