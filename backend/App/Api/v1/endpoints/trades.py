from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from App.Api.v1.endpoints.auth import get_current_user
from App.database import get_db
from App.dependencies import require_admin
from App.models.balance import Balance
from App.models.order import Order
from App.models.transaction import Transaction
from App.models.user import User
from App.schemas.order import OrderOut, PlaceOrderRequest
from App.services.trading_engine import SimpleOrder, match_orders, settle_trade

router = APIRouter()


def split_symbol(symbol: str) -> tuple[str, str]:
    clean = symbol.replace("/", "").upper()
    if clean.endswith("USDT") and len(clean) > 4:
        return clean[:-4], "USDT"
    raise HTTPException(status_code=400, detail="Only */USDT symbols are supported")


async def get_or_create_balance(db: AsyncSession, user_id: int, coin: str) -> Balance:
    result = await db.execute(select(Balance).where(Balance.user_id == user_id, Balance.coin == coin))
    bal = result.scalar_one_or_none()
    if bal is None:
        bal = Balance(user_id=user_id, coin=coin, amount=Decimal("0"))
        db.add(bal)
    return bal


@router.post("/")
async def place_order(payload: PlaceOrderRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.price <= 0 or payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Price and amount must be greater than zero")

    symbol = payload.symbol.replace("/", "").upper()
    order = Order(
        user_id=user.id,
        side=payload.side,
        symbol=symbol,
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


@router.get("/orderbook/{symbol}")
async def get_orderbook(symbol: str, db: AsyncSession = Depends(get_db)):
    clean = symbol.replace("/", "").upper()
    buys = await db.execute(
        select(Order).where(Order.symbol == clean, Order.side == "buy", Order.status == "open").order_by(Order.price.desc(), Order.created_at.asc())
    )
    sells = await db.execute(
        select(Order).where(Order.symbol == clean, Order.side == "sell", Order.status == "open").order_by(Order.price.asc(), Order.created_at.asc())
    )

    return {
        "symbol": clean,
        "bids": [{"id": o.id, "price": str(o.price), "amount": str(o.amount)} for o in buys.scalars().all()],
        "asks": [{"id": o.id, "price": str(o.price), "amount": str(o.amount)} for o in sells.scalars().all()],
    }


@router.post("/match/{symbol}")
async def run_matching(symbol: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    base_coin, quote_coin = split_symbol(symbol)
    clean = f"{base_coin}{quote_coin}"

    buy_result = await db.execute(
        select(Order).where(Order.symbol == clean, Order.side == "buy", Order.status == "open").order_by(Order.price.desc(), Order.created_at.asc())
    )
    sell_result = await db.execute(
        select(Order).where(Order.symbol == clean, Order.side == "sell", Order.status == "open").order_by(Order.price.asc(), Order.created_at.asc())
    )
    buy_orders = list(buy_result.scalars().all())
    sell_orders = list(sell_result.scalars().all())

    buy_simple = [
        SimpleOrder(id=o.id, user_id=o.user_id, side=o.side, price=Decimal(o.price), amount=Decimal(o.amount), created_at_ts=o.created_at.timestamp())
        for o in buy_orders
    ]
    sell_simple = [
        SimpleOrder(id=o.id, user_id=o.user_id, side=o.side, price=Decimal(o.price), amount=Decimal(o.amount), created_at_ts=o.created_at.timestamp())
        for o in sell_orders
    ]

    matches = match_orders(buy_simple, sell_simple)
    if not matches:
        return {"symbol": clean, "matches": 0, "detail": "No crossable orders"}

    by_id = {o.id: o for o in [*buy_orders, *sell_orders]}
    executed = 0

    for m in matches:
        buy_order = by_id[m.buy_order_id]
        sell_order = by_id[m.sell_order_id]

        buyer_quote = await get_or_create_balance(db, buy_order.user_id, quote_coin)
        buyer_base = await get_or_create_balance(db, buy_order.user_id, base_coin)
        seller_base = await get_or_create_balance(db, sell_order.user_id, base_coin)
        seller_quote = await get_or_create_balance(db, sell_order.user_id, quote_coin)

        settlement = settle_trade(price=m.price, amount=m.amount)

        # Skip invalid executions if balances are insufficient at settlement time.
        required_quote = -settlement.buyer_quote_delta
        required_base = -settlement.seller_base_delta
        if buyer_quote.amount < required_quote or seller_base.amount < required_base:
            continue

        buyer_quote.amount += settlement.buyer_quote_delta
        buyer_base.amount += settlement.buyer_base_delta
        seller_base.amount += settlement.seller_base_delta
        seller_quote.amount += settlement.seller_quote_delta

        buy_order.amount = Decimal(buy_order.amount) - m.amount
        sell_order.amount = Decimal(sell_order.amount) - m.amount
        buy_order.status = "filled" if buy_order.amount == 0 else "open"
        sell_order.status = "filled" if sell_order.amount == 0 else "open"

        now = datetime.now(timezone.utc)
        db.add(
            Transaction(
                user_id=buy_order.user_id,
                coin=base_coin,
                amount=settlement.buyer_base_delta,
                type="trade_buy",
                status="completed",
                created_at=now,
            )
        )
        db.add(
            Transaction(
                user_id=sell_order.user_id,
                coin=quote_coin,
                amount=settlement.seller_quote_delta,
                type="trade_sell",
                status="completed",
                created_at=now,
            )
        )
        executed += 1

    await db.commit()
    return {"symbol": clean, "matches": executed}
