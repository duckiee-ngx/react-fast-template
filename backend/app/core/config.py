from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    APP_URL: str = "http://localhost:8000"

    CORS_ALLOW_ORIGINS: list[str] = Field(default_factory=list)

    POSTGRES_USER: str = Field(min_length=1)
    POSTGRES_PASSWORD: str = Field(min_length=1)
    POSTGRES_SERVER: str = Field(min_length=1)
    POSTGRES_PORT: str = Field(min_length=1)
    POSTGRES_DB: str = Field(min_length=1)
    SQL_ECHO: bool = False

    @property
    def POSTGRES_URL(self) -> str:
        user = quote_plus(self.POSTGRES_USER)
        password = quote_plus(self.POSTGRES_PASSWORD)
        return (
            f"postgresql+asyncpg://{user}:{password}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    REDIS_HOST: str = Field(min_length=1)
    REDIS_PORT: str = Field(min_length=1)

    def REDIS_URL(self, db: int) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"

    JWT_SECRET: str = Field(min_length=1)
    JWT_ALGORITHM: Literal["HS256", "HS384", "HS512"]
    JWT_EXPIRE_MINUTES: int = Field(gt=0)
    JWT_REFRESH_EXPIRE_DAYS: int = Field(gt=0)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )


app_settings = AppSettings()  # type: ignore[call-arg]  # loaded from env
