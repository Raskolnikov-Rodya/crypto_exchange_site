from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Crypto Exchange"
    PROJECT_VERSION: str = "1.0.0"

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    JWT_SECRET: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SUPPORTED_CURRENCIES: List[str] = ["BTC", "ETH", "USDT", "LTC", "BCH"]
    PRICE_UPDATE_INTERVAL: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
