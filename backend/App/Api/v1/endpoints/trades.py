from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.trade import Trade
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.core.logger import log_action
from app.api.v1.endpoints.monitor import notify_clients  # Import WebSocket notification

router = APIRouter()

@router.post("/")
async def place_trade(
    trade_type: str, 
    symbol: str, 
    amount: float, 
    price: float, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    """Handles trade execution (buy/sell orders)."""
    if trade_type.lower() not in ["buy", "sell"]:
        raise HTTPException(status_code=400, detail="Invalid trade type")

    new_trade = Trade(
        user_id=user.id, 
        trade_type=trade_type.lower(), 
        symbol=symbol.upper(), 
        amount=amount, 
        price=price
    )
    db.add(new_trade)
    await db.commit()

    log_action("Trade Executed", user.id, {"trade_id": new_trade.id, "symbol": symbol, "amount": amount, "price": price})

    # Notify WebSocket clients about the new trade
    await notify_clients({
        "type": "trade",
        "trade_id": new_trade.id,
        "user_id": user.id,
        "symbol": symbol,
        "amount": amount,
        "price": price
    })
    
    return {"message": "Trade placed successfully", "trade_id": new_trade.id}


@router.get("/")
async def get_trade_history(
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    """Fetches a user's trade history."""
    result = await db.execute(select(Trade).where(Trade.user_id == user.id))
    trades = result.scalars().all()
    return trades
