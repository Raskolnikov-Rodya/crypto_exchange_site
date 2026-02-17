from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.Api.v1.endpoints.auth import get_current_user
from App.database import get_db
from App.models.order import Order
from App.models.user import User
from App.schemas.order import OrderOut, PlaceOrderRequest

router = APIRouter()


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


@router.get("/", response_model=list[OrderOut])
async def get_trade_history(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(select(Order).where(Order.user_id == user.id).order_by(Order.created_at.desc()))
    return list(result.scalars().all())
