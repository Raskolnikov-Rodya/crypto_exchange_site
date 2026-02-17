from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PlaceOrderRequest(BaseModel):
    side: str = Field(pattern="^(buy|sell)$")
    symbol: str
    price: Decimal
    amount: Decimal


class OrderOut(BaseModel):
    id: int
    user_id: int
    side: str
    symbol: str
    price: Decimal
    amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
