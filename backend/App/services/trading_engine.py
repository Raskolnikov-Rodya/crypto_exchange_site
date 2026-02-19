from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from App.services.fee_handler import calculate_trading_fee


@dataclass
class SimpleOrder:
    id: int
    user_id: int
    side: str
    price: Decimal
    amount: Decimal
    created_at_ts: float


@dataclass
class MatchExecution:
    buy_order_id: int
    sell_order_id: int
    price: Decimal
    amount: Decimal


@dataclass
class SettlementResult:
    buyer_base_delta: Decimal
    buyer_quote_delta: Decimal
    seller_base_delta: Decimal
    seller_quote_delta: Decimal
    buyer_fee: Decimal
    seller_fee: Decimal


def price_time_sort_buy(orders: Iterable[SimpleOrder]) -> list[SimpleOrder]:
    return sorted(orders, key=lambda o: (-o.price, o.created_at_ts, o.id))


def price_time_sort_sell(orders: Iterable[SimpleOrder]) -> list[SimpleOrder]:
    return sorted(orders, key=lambda o: (o.price, o.created_at_ts, o.id))


def match_orders(buys: list[SimpleOrder], sells: list[SimpleOrder]) -> list[MatchExecution]:
    buy_book = price_time_sort_buy([o for o in buys if o.amount > 0])
    sell_book = price_time_sort_sell([o for o in sells if o.amount > 0])

    matches: list[MatchExecution] = []
    i = j = 0
    while i < len(buy_book) and j < len(sell_book):
        b = buy_book[i]
        s = sell_book[j]

        if b.price < s.price:
            break

        fill_amount = min(b.amount, s.amount)
        matches.append(MatchExecution(buy_order_id=b.id, sell_order_id=s.id, price=s.price, amount=fill_amount))

        b.amount -= fill_amount
        s.amount -= fill_amount

        if b.amount == 0:
            i += 1
        if s.amount == 0:
            j += 1

    return matches


def settle_trade(price: Decimal, amount: Decimal, fee_rate: Decimal = Decimal("0.001")) -> SettlementResult:
    gross_quote = price * amount

    buyer_fee = calculate_trading_fee(amount, fee_rate)
    seller_fee = calculate_trading_fee(gross_quote, fee_rate)

    return SettlementResult(
        buyer_base_delta=amount - buyer_fee,
        buyer_quote_delta=-gross_quote,
        seller_base_delta=-amount,
        seller_quote_delta=gross_quote - seller_fee,
        buyer_fee=buyer_fee,
        seller_fee=seller_fee,
    )
