from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
COIN_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "LTC": "litecoin",
    "BCH": "bitcoin-cash",
    "USDT": "tether",
    "SOL": "solana",
    "XRP": "ripple",
    "ADA": "cardano",
}


@router.get("/")
async def get_crypto_prices():
    ids = ",".join(COIN_MAP.values())
    params = {"ids": ids, "vs_currencies": "usd"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(COINGECKO_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch prices from upstream API")

    payload = response.json()
    return {symbol: payload.get(coin_id, {}).get("usd") for symbol, coin_id in COIN_MAP.items()}
