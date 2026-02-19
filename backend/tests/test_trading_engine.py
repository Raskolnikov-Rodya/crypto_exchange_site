from decimal import Decimal

from App.services.fee_handler import calculate_trading_fee
from App.services.trading_engine import SimpleOrder, match_orders, settle_trade


def test_fee_handler_uses_default_rate():
    fee = calculate_trading_fee(Decimal("10"))
    assert fee == Decimal("0.010000000000000000")


def test_price_time_matching_priority():
    buys = [
        SimpleOrder(id=1, user_id=100, side="buy", price=Decimal("100"), amount=Decimal("1"), created_at_ts=2.0),
        SimpleOrder(id=2, user_id=101, side="buy", price=Decimal("101"), amount=Decimal("1"), created_at_ts=1.0),
    ]
    sells = [
        SimpleOrder(id=3, user_id=200, side="sell", price=Decimal("100"), amount=Decimal("0.4"), created_at_ts=1.0),
        SimpleOrder(id=4, user_id=201, side="sell", price=Decimal("100"), amount=Decimal("1.0"), created_at_ts=2.0),
    ]

    matches = match_orders(buys, sells)

    assert len(matches) == 3
    assert matches[0].buy_order_id == 2
    assert matches[0].sell_order_id == 3
    assert matches[0].amount == Decimal("0.4")
    assert matches[1].buy_order_id == 2
    assert matches[1].sell_order_id == 4
    assert matches[1].amount == Decimal("0.6")
    assert matches[2].buy_order_id == 1
    assert matches[2].sell_order_id == 4
    assert matches[2].amount == Decimal("0.4")


def test_settlement_applies_fees_to_received_amount():
    result = settle_trade(price=Decimal("100"), amount=Decimal("1"))

    assert result.buyer_base_delta == Decimal("0.999000000000000000")
    assert result.buyer_quote_delta == Decimal("-100")
    assert result.seller_base_delta == Decimal("-1")
    assert result.seller_quote_delta == Decimal("99.900000000000000000")
