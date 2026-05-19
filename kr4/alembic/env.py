"""Alembic environment configuration — асинхронный режим."""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.config import DATABASE_URL_ZOLOTOV
from app.database import Base_zolotov

# Импорт моделей, чтобы Alembic видел метаданные
from app import models  # noqa: F401

# this is the Alembic Config object
config = context.config

# Подставляем URL из .env
config.set_main_option("sqlalchemy.url", DATABASE_URL_ZOLOTOV)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base_zolotov.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode (async)."""
    connectable_zolotov = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable_zolotov.connect() as connection_zolotov:
        await connection_zolotov.run_sync(do_run_migrations)

    await connectable_zolotov.dispose()


def run_migrations_online() -> None:
    """Запуск async-миграций."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
