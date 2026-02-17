import os

from fastapi import Depends, FastAPI, Request
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from App.Api.v1.endpoints import admin, auth, blockchain, monitor, prices, trades, users, wallet
from App.core.config import settings
from App.database import get_db
from App.middleware.rate_limiter import AuthRateLimiter, LimitWindow
from App.database import get_db

app = FastAPI(
    title="Crypto Exchange API",
    description="Simplified centralized crypto exchange (pet project)",
    version="0.1.0",
)

limiter = AuthRateLimiter(
    login_window=LimitWindow(settings.AUTH_LOGIN_RATE_LIMIT, settings.AUTH_RATE_LIMIT_WINDOW_SECONDS),
    register_window=LimitWindow(settings.AUTH_REGISTER_RATE_LIMIT, settings.AUTH_RATE_LIMIT_WINDOW_SECONDS),
)


@app.middleware("http")
async def auth_sensitive_rate_limit(request: Request, call_next):
    path = request.url.path
    client_ip = request.client.host if request.client else "unknown"

    if path == "/api/v1/auth/login":
        limiter.check(client_ip, "login")
    elif path == "/api/v1/auth/register":
        limiter.check(client_ip, "register")

    return await call_next(request)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["wallet"])
app.include_router(trades.router, prefix="/api/v1/trades", tags=["trades"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(prices.router, prefix="/api/v1/prices", tags=["prices"])
app.include_router(monitor.router, prefix="/api/v1/monitor", tags=["monitor"])
app.include_router(blockchain.router, prefix="/api/v1/blockchain", tags=["blockchain"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to the Crypto Exchange API"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": os.getenv("ENV", "development"),
        "database_url": "configured" if os.getenv("DATABASE_URL") else "missing",
    }


@app.get("/test-db")
async def test_db_connection(db: AsyncSession = Depends(get_db)) -> dict[str, str | int]:
    result = await db.execute(text("SELECT 1"))
    return {
        "status": "success",
        "db_response": result.scalar_one(),
    }
