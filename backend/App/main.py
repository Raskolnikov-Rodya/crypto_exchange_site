from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import auth, users, trades, wallet
from app.api.v1.endpoints import prices
from app.middleware.rate_limiter import limiter
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.middleware.error_handler import http_error_handler, generic_exception_handler
from app.api.v1.endpoints import blockchain


app.state.limiter = limiter
app.add_exception_handler(429, limiter._fastapi_handler)
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(trades.router, prefix="/api/v1/trades", tags=["Trades"])
app.include_router(wallet.router, prefix="/api/v1/wallet", tags=["Wallet"])
app.include_router(prices.router, prefix="/api/v1/prices", tags=["Crypto Prices"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "mycryptoexchange.com"])
app.include_router(blockchain.router, prefix="/api/v1/blockchain", tags=["Blockchain"])

