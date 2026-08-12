from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import app_settings

engine = create_async_engine(app_settings.POSTGRES_URL, echo=app_settings.SQL_ECHO)


async def close_db() -> None:
    await engine.dispose()


AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
