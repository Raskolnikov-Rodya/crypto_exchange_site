from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Crypto Exchange"
    PROJECT_VERSION: str = "1.0.0"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Crypto API Settings
    SUPPORTED_CURRENCIES: List[str] = ["BTC", "ETH", "USDT", "LTC"]
    PRICE_UPDATE_INTERVAL: int = 30  # seconds

    class Config:
        env_file = ".env"

settings = Settings()
 
