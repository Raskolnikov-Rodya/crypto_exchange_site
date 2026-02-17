from decimal import Decimal, ROUND_DOWN

DEFAULT_TRADING_FEE_RATE = Decimal("0.001")


def quantize_amount(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.000000000000000001"), rounding=ROUND_DOWN)


def calculate_trading_fee(amount: Decimal, fee_rate: Decimal = DEFAULT_TRADING_FEE_RATE) -> Decimal:
    if amount <= 0:
        return Decimal("0")
    return quantize_amount(amount * fee_rate)
