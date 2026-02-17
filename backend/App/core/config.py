from typing import List

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Crypto Exchange"
    PROJECT_VERSION: str = "1.0.0"
    ENV: str = "development"

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    JWT_SECRET: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    AUTH_LOGIN_RATE_LIMIT: int = 20
    AUTH_REGISTER_RATE_LIMIT: int = 10
    AUTH_RATE_LIMIT_WINDOW_SECONDS: int = 60

    SUPPORTED_CURRENCIES: List[str] = ["BTC", "ETH", "USDT", "LTC", "BCH"]
    PRICE_UPDATE_INTERVAL: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @model_validator(mode="after")
    def validate_secrets(self):
        if self.ENV.lower() == "production" and (self.JWT_SECRET == "your-secret-key" or len(self.JWT_SECRET) < 32):
            raise ValueError("JWT_SECRET must be set to a strong value in production (min 32 chars).")
        return self


settings = Settings()
