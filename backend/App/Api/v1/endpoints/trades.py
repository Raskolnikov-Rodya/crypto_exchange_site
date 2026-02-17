from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.Api.v1.endpoints.auth import get_current_user
from App.database import get_db
from App.models.order import Order
from App.models.user import User

router = APIRouter()


class PlaceOrderRequest(BaseModel):
    side: str = Field(pattern="^(buy|sell)$")
    symbol: str
    price: Decimal
    amount: Decimal


@router.post("/")
async def place_order(payload: PlaceOrderRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.price <= 0 or payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Price and amount must be greater than zero")

    order = Order(
        user_id=user.id,
        side=payload.side,
        symbol=payload.symbol.upper(),
        price=payload.price,
        amount=payload.amount,
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return {"message": "Order created", "order_id": order.id}


@router.get("/")
async def get_trade_history(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc()))
    orders = result.scalars().all()
    return [
        {
            "id": order.id,
            "side": order.side,
            "symbol": order.symbol,
            "price": str(order.price),
            "amount": str(order.amount),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
        }
        for order in orders
    ]
