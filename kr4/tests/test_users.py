"""Асинхронные модульные тесты (Задания 11.1 & 11.2).

Используются: pytest-asyncio, httpx.AsyncClient, Faker.
Хранилище (in-memory dict) полностью очищается до и после каждого теста.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker

from app.main import app
from app.routers import users

fake_zolotov = Faker("ru_RU")


# -------- Фикстура: изоляция состояния in-memory хранилища --------

@pytest.fixture(autouse=True)
def _isolate_db_zolotov():
    """Полностью очищает in-memory словарь до и после каждого теста."""
    users.db_zolotov.clear()
    users._next_id_zolotov = 1
    yield
    users.db_zolotov.clear()
    users._next_id_zolotov = 1


# -------- Фикстура: httpx async client --------

@pytest.fixture
async def client_zolotov():
    """Асинхронный HTTP-клиент, работающий напрямую через ASGI (без Uvicorn)."""
    transport_zolotov = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport_zolotov,
        base_url="http://testserver",
    ) as ac_zolotov:
        yield ac_zolotov


# -------- Вспомогательная функция: генерация данных --------

def _make_user_payload_zolotov() -> dict:
    """Генерирует реалистичные данные пользователя через Faker."""
    return {
        "username": fake_zolotov.user_name(),
        "age": fake_zolotov.random_int(min=19, max=80),
        "email": fake_zolotov.email(),
        "password": fake_zolotov.password(length=12),
        "phone": fake_zolotov.phone_number(),
    }


# ===================== ТЕСТЫ =====================


@pytest.mark.asyncio
async def test_create_user_201_zolotov(client_zolotov: AsyncClient):
    """Создание пользователя — ожидаем 201."""
    payload_zolotov = _make_user_payload_zolotov()
    response_zolotov = await client_zolotov.post("/users/", json=payload_zolotov)

    assert response_zolotov.status_code == 201
    data_zolotov = response_zolotov.json()
    assert data_zolotov["username"] == payload_zolotov["username"]
    assert data_zolotov["email"] == payload_zolotov["email"]
    assert "id" in data_zolotov


@pytest.mark.asyncio
async def test_get_existing_user_200_zolotov(client_zolotov: AsyncClient):
    """Получение существующего пользователя — ожидаем 200."""
    payload_zolotov = _make_user_payload_zolotov()
    create_resp_zolotov = await client_zolotov.post("/users/", json=payload_zolotov)
    user_id_zolotov = create_resp_zolotov.json()["id"]

    response_zolotov = await client_zolotov.get(f"/users/{user_id_zolotov}")

    assert response_zolotov.status_code == 200
    assert response_zolotov.json()["username"] == payload_zolotov["username"]


@pytest.mark.asyncio
async def test_get_nonexistent_user_404_zolotov(client_zolotov: AsyncClient):
    """Получение несуществующего пользователя — ожидаем 404."""
    response_zolotov = await client_zolotov.get("/users/9999")

    assert response_zolotov.status_code == 404
    assert "detail" in response_zolotov.json()


@pytest.mark.asyncio
async def test_delete_existing_user_204_zolotov(client_zolotov: AsyncClient):
    """Удаление существующего пользователя — ожидаем 204."""
    payload_zolotov = _make_user_payload_zolotov()
    create_resp_zolotov = await client_zolotov.post("/users/", json=payload_zolotov)
    user_id_zolotov = create_resp_zolotov.json()["id"]

    response_zolotov = await client_zolotov.delete(f"/users/{user_id_zolotov}")

    assert response_zolotov.status_code == 204


@pytest.mark.asyncio
async def test_delete_nonexistent_user_404_zolotov(client_zolotov: AsyncClient):
    """Повторное удаление (несуществующего) пользователя — ожидаем 404."""
    # Создаём и удаляем
    payload_zolotov = _make_user_payload_zolotov()
    create_resp_zolotov = await client_zolotov.post("/users/", json=payload_zolotov)
    user_id_zolotov = create_resp_zolotov.json()["id"]
    await client_zolotov.delete(f"/users/{user_id_zolotov}")

    # Повторное удаление
    response_zolotov = await client_zolotov.delete(f"/users/{user_id_zolotov}")

    assert response_zolotov.status_code == 404
    assert "detail" in response_zolotov.json()
