from fastapi import APIRouter, HTTPException
import httpx
from app.core.config import settings

router = APIRouter()

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

@router.get("/")
async def get_crypto_prices():
    """Fetch real-time cryptocurrency prices from CoinGecko."""
    params = {
        "ids": ",".join(settings.SUPPORTED_CURRENCIES),
        "vs_currencies": "usd"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(COINGECKO_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch prices")

    return response.json()
