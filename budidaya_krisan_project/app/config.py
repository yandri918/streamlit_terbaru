from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    APP_NAME: str = "Budidaya Krisan Pro"
    APP_ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./krisan.db"
    CORS_ORIGINS: str = "*"
    API_V1_PREFIX: str = "/api/v1"
    WEBHOOK_URL: Optional[str] = None
    WEBHOOK_ENABLED: bool = False
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    CLERK_SECRET_KEY: Optional[str] = None

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
