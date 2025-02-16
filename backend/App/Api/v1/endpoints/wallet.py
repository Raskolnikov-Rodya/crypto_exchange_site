from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.wallet import Wallet
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/")
async def get_wallet_balances(
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id))
    wallets = result.scalars().all()
    return wallets

@router.post("/deposit")
async def deposit_funds(
    currency: str, 
    amount: float, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero")

    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id, Wallet.currency == currency.upper()))
    wallet = result.scalars().first()

    if wallet:
        wallet.balance += amount
    else:
        wallet = Wallet(user_id=user.id, currency=currency.upper(), balance=amount)
        db.add(wallet)

    await db.commit()
    return {"message": "Deposit successful", "new_balance": wallet.balance}
 
@router.post("/withdraw")
async def withdraw_funds(
    currency: str, 
    amount: float, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be greater than zero")

    # Get user's wallet balance
    result = await db.execute(select(Wallet).where(Wallet.user_id == user.id, Wallet.currency == currency.upper()))
    wallet = result.scalars().first()

    if not wallet or wallet.balance < amount:
        log_action("Failed Withdrawal", user.id, {"currency": currency, "amount": amount})
        raise HTTPException(status_code=400, detail="Insufficient funds")

    wallet.balance -= amount
    await db.commit()

    log_action("Withdrawal Processed", user.id, {"currency": currency, "amount": amount})
    
    return {"message": "Withdrawal successful", "remaining_balance": wallet.balance}