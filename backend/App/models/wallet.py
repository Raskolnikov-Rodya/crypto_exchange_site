from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(String, nullable=False)  # e.g., "BTC", "ETH"
    balance = Column(Float, default=0.0)
    address = Column(String, unique=True, nullable=False)
    encrypted_private_key = Column(String, nullable=False)  # Encrypted private key


    user = relationship("User", back_populates="wallets")
 
