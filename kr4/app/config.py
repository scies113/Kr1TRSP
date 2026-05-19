"""Конфигурация приложения — загрузка переменных окружения."""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL_ZOLOTOV: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/kr4_db",
)
