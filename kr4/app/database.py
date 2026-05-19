"""Асинхронное подключение к PostgreSQL через SQLAlchemy."""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL_ZOLOTOV

# -------- движок и фабрика сессий (суффикс _zolotov) --------
engine_zolotov = create_async_engine(DATABASE_URL_ZOLOTOV, echo=True)

session_factory_zolotov = async_sessionmaker(
    bind=engine_zolotov,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base_zolotov(DeclarativeBase):
    """Базовый класс для всех моделей."""
    pass


async def get_session_zolotov() -> AsyncSession:  # type: ignore[misc]
    """Dependency — асинхронная сессия БД."""
    async with session_factory_zolotov() as session_zolotov:
        yield session_zolotov
