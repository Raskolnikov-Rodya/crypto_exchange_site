from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base


class Balance(Base):
    __tablename__ = "balances"
    __table_args__ = (UniqueConstraint("user_id", "coin", name="uq_balances_user_coin"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    coin = Column(String(10), nullable=False, index=True)
    amount = Column(Numeric(precision=36, scale=18), default=0, nullable=False)

    user = relationship("User", back_populates="balances")
