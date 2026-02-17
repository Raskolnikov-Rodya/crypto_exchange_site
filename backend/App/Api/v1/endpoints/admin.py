from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.database import get_db
from App.dependencies import require_admin
from App.models.balance import Balance
from App.models.transaction import Transaction
from App.models.user import User

router = APIRouter()


class CreditRequest(BaseModel):
    user_id: int
    coin: str
    amount: Decimal


@router.get("/transactions")
async def get_all_transactions(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    result = await db.execute(select(Transaction).order_by(Transaction.created_at.desc()))
    txs = result.scalars().all()
    return [{"id": tx.id, "user_id": tx.user_id, "coin": tx.coin, "amount": str(tx.amount), "type": tx.type, "status": tx.status} for tx in txs]


@router.post("/credit")
async def manual_credit(payload: CreditRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    result = await db.execute(select(Balance).where(Balance.user_id == payload.user_id, Balance.coin == payload.coin.upper()))
    balance = result.scalar_one_or_none()
    if balance is None:
        balance = Balance(user_id=payload.user_id, coin=payload.coin.upper(), amount=0)
        db.add(balance)

    balance.amount = balance.amount + payload.amount
    tx = Transaction(user_id=payload.user_id, coin=payload.coin.upper(), amount=payload.amount, type="deposit", status="approved")
    db.add(tx)

    await db.commit()
    return {"message": "Balance credited"}
