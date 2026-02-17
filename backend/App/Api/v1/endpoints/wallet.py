from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.Api.v1.endpoints.auth import get_current_user
from App.database import get_db
from App.models.balance import Balance
from App.models.queue import WithdrawalQueue
from App.models.transaction import Transaction
from App.models.user import User
from pydantic import BaseModel

from App.schemas.queue import WithdrawalQueueOut, WithdrawalRequestIn
from App.models.transaction import Transaction
from App.models.user import User

router = APIRouter()


class AmountRequest(BaseModel):
    coin: str
    amount: Decimal


@router.get("/balances")
async def get_wallet_balances(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Balance).where(Balance.user_id == user.id).order_by(Balance.coin.asc()))
    balances = result.scalars().all()
    return [{"coin": b.coin, "amount": str(b.amount)} for b in balances]


class DepositRequest(BaseModel):
    coin: str
    amount: Decimal


@router.post("/deposit")
async def deposit_funds(payload: DepositRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):

@router.post("/deposit")
async def deposit_funds(payload: AmountRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero")

    result = await db.execute(select(Balance).where(Balance.user_id == user.id, Balance.coin == payload.coin.upper()))
    balance = result.scalar_one_or_none()

    if balance is None:
        balance = Balance(user_id=user.id, coin=payload.coin.upper(), amount=Decimal("0"))
        balance = Balance(user_id=user.id, coin=payload.coin.upper(), amount=0)
        db.add(balance)

    balance.amount = balance.amount + payload.amount
    db.add(Transaction(user_id=user.id, coin=payload.coin.upper(), amount=payload.amount, type="deposit", status="completed"))
    await db.commit()

    return {"message": "Deposit recorded", "coin": payload.coin.upper(), "new_balance": str(balance.amount)}


@router.post("/withdraw/request", response_model=WithdrawalQueueOut)
async def request_withdrawal(
    payload: WithdrawalRequestIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
@router.post("/withdraw")
async def withdraw_funds(payload: AmountRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be greater than zero")

    result = await db.execute(select(Balance).where(Balance.user_id == user.id, Balance.coin == payload.coin.upper()))
    balance = result.scalar_one_or_none()

    if balance is None or balance.amount < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    balance.amount = balance.amount - payload.amount

    queue_item = WithdrawalQueue(
        user_id=user.id,
        coin=payload.coin.upper(),
        amount=payload.amount,
        destination_address=payload.destination_address,
        status="pending",
    )
    db.add(queue_item)
    db.add(Transaction(user_id=user.id, coin=payload.coin.upper(), amount=payload.amount, type="withdrawal", status="pending"))

    db.add(Transaction(user_id=user.id, coin=payload.coin.upper(), amount=payload.amount, type="withdrawal", status="pending"))
    await db.commit()
    await db.refresh(queue_item)
    return queue_item


@router.get("/withdraw/requests", response_model=list[WithdrawalQueueOut])
async def list_my_withdrawal_requests(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(
        select(WithdrawalQueue).where(WithdrawalQueue.user_id == user.id).order_by(WithdrawalQueue.created_at.desc())
    )
    return list(result.scalars().all())
    return {"message": "Withdrawal queued", "coin": payload.coin.upper(), "remaining_balance": str(balance.amount)}
