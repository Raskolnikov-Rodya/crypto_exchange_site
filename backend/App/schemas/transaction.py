from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionOut(BaseModel):
    id: int
    user_id: int
    coin: str
    amount: Decimal
    type: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
