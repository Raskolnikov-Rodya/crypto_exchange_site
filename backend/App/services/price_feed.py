import ccxt.async_support as ccxt
from typing import Dict
from app.core.config import settings

class PriceFeedService:
    def __init__(self):
        self.exchange = ccxt.binance({
            'enableRateLimit': True,
        })

    async def get_current_prices(self) -> Dict[str, float]:
        prices = {}
        try:
            for currency in settings.SUPPORTED_CURRENCIES:
                if currency != "USDT":  # Base currency
                    symbol = f"{currency}/USDT"
                    ticker = await self.exchange.fetch_ticker(symbol)
                    prices[currency] = ticker['last']
        except Exception as e:
            # Log the error (logging can be added later)
            print(f"Error fetching prices: {e}")
        return prices
 
