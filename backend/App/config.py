from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Crypto Exchange"
    PROJECT_VERSION: str = "1.0.0"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    DATABASE_URL: str
    JWT_SECRET: str
    ALGORITHM: str = "HS256"

    # Crypto-specific settings
    SUPPORTED_CURRENCIES: List[str] = ["BTC", "ETH", "USDT", "LTC"]
    PRICE_UPDATE_INTERVAL: int = 30  # seconds

    class Config:
        env_file = ".env"

# Instantiate settings
settings = Settings()
 
