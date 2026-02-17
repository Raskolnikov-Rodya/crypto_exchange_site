from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class WithdrawalRequestIn(BaseModel):
    coin: str
    amount: Decimal
    destination_address: str


class WithdrawalReviewIn(BaseModel):
    note: Optional[str] = None


class WithdrawalCompleteIn(BaseModel):
    tx_hash: Optional[str] = None


class WithdrawalQueueOut(BaseModel):
    id: int
    user_id: int
    coin: str
    amount: Decimal
    destination_address: str
    status: str
    note: Optional[str] = None
    tx_hash: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
