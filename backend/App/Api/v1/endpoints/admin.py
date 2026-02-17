from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.database import get_db
from App.dependencies import require_admin
from App.models.balance import Balance
from App.models.queue import WithdrawalQueue
from App.models.transaction import Transaction
from App.models.user import User
from App.schemas.queue import WithdrawalCompleteIn, WithdrawalQueueOut, WithdrawalReviewIn

router = APIRouter()


class CreditRequest(BaseModel):
    user_id: int
    coin: str
    amount: Decimal


@router.get("/transactions")
async def get_all_transactions(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    result = await db.execute(select(Transaction).order_by(Transaction.created_at.desc()))
    txs = result.scalars().all()
    return [
        {
            "id": tx.id,
            "user_id": tx.user_id,
            "coin": tx.coin,
            "amount": str(tx.amount),
            "type": tx.type,
            "status": tx.status,
        }
        for tx in txs
    ]
    return [{"id": tx.id, "user_id": tx.user_id, "coin": tx.coin, "amount": str(tx.amount), "type": tx.type, "status": tx.status} for tx in txs]


@router.post("/credit")
async def manual_credit(payload: CreditRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    result = await db.execute(select(Balance).where(Balance.user_id == payload.user_id, Balance.coin == payload.coin.upper()))
    balance = result.scalar_one_or_none()
    if balance is None:
        balance = Balance(user_id=payload.user_id, coin=payload.coin.upper(), amount=Decimal("0"))
        balance = Balance(user_id=payload.user_id, coin=payload.coin.upper(), amount=0)
        db.add(balance)

    balance.amount = balance.amount + payload.amount
    tx = Transaction(user_id=payload.user_id, coin=payload.coin.upper(), amount=payload.amount, type="deposit", status="approved")
    db.add(tx)

    await db.commit()
    return {"message": "Balance credited"}


@router.get("/withdrawals", response_model=list[WithdrawalQueueOut])
async def list_withdrawal_queue(db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    result = await db.execute(select(WithdrawalQueue).order_by(WithdrawalQueue.created_at.asc()))
    return list(result.scalars().all())


@router.post("/withdrawals/{withdrawal_id}/approve", response_model=WithdrawalQueueOut)
async def approve_withdrawal(
    withdrawal_id: int,
    payload: WithdrawalReviewIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    item = await db.get(WithdrawalQueue, withdrawal_id)
    if not item:
        raise HTTPException(status_code=404, detail="Withdrawal request not found")
    if item.status != "pending":
        raise HTTPException(status_code=409, detail="Only pending requests can be approved")

    item.status = "approved"
    item.note = payload.note
    item.reviewed_at = datetime.now(timezone.utc)

    tx_result = await db.execute(
        select(Transaction)
        .where(
            Transaction.user_id == item.user_id,
            Transaction.coin == item.coin,
            Transaction.amount == item.amount,
            Transaction.type == "withdrawal",
            Transaction.status == "pending",
        )
        .order_by(Transaction.created_at.desc())
    )
    tx = tx_result.scalars().first()
    if tx:
        tx.status = "approved"

    await db.commit()
    await db.refresh(item)
    return item


@router.post("/withdrawals/{withdrawal_id}/reject", response_model=WithdrawalQueueOut)
async def reject_withdrawal(
    withdrawal_id: int,
    payload: WithdrawalReviewIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    item = await db.get(WithdrawalQueue, withdrawal_id)
    if not item:
        raise HTTPException(status_code=404, detail="Withdrawal request not found")
    if item.status != "pending":
        raise HTTPException(status_code=409, detail="Only pending requests can be rejected")

    item.status = "rejected"
    item.note = payload.note
    item.reviewed_at = datetime.now(timezone.utc)

    balance_result = await db.execute(select(Balance).where(Balance.user_id == item.user_id, Balance.coin == item.coin))
    balance = balance_result.scalar_one_or_none()
    if balance is None:
        balance = Balance(user_id=item.user_id, coin=item.coin, amount=Decimal("0"))
        db.add(balance)
    balance.amount = balance.amount + item.amount

    tx_result = await db.execute(
        select(Transaction)
        .where(
            Transaction.user_id == item.user_id,
            Transaction.coin == item.coin,
            Transaction.amount == item.amount,
            Transaction.type == "withdrawal",
            Transaction.status == "pending",
        )
        .order_by(Transaction.created_at.desc())
    )
    tx = tx_result.scalars().first()
    if tx:
        tx.status = "rejected"

    await db.commit()
    await db.refresh(item)
    return item


@router.post("/withdrawals/{withdrawal_id}/complete", response_model=WithdrawalQueueOut)
async def complete_withdrawal(
    withdrawal_id: int,
    payload: WithdrawalCompleteIn,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    item = await db.get(WithdrawalQueue, withdrawal_id)
    if not item:
        raise HTTPException(status_code=404, detail="Withdrawal request not found")
    if item.status != "approved":
        raise HTTPException(status_code=409, detail="Only approved requests can be completed")

    item.status = "completed"
    item.tx_hash = payload.tx_hash
    item.completed_at = datetime.now(timezone.utc)

    tx_result = await db.execute(
        select(Transaction)
        .where(
            Transaction.user_id == item.user_id,
            Transaction.coin == item.coin,
            Transaction.amount == item.amount,
            Transaction.type == "withdrawal",
            Transaction.status == "approved",
        )
        .order_by(Transaction.created_at.desc())
    )
    tx = tx_result.scalars().first()
    if tx:
        tx.status = "completed"

    await db.commit()
    await db.refresh(item)
    return item
    await db.commit()
    return {"message": "Balance credited"}
