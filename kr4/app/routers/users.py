"""Эндпоинты для Задания 11.1 & 11.2 — CRUD пользователей (in-memory)."""

import threading
from fastapi import APIRouter
from fastapi.responses import Response

from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users (11.1 / 11.2)"])

# -------- in-memory хранилище (суффикс _zolotov) --------
db_zolotov: dict[int, dict] = {}
_id_counter_lock_zolotov = threading.Lock()
_next_id_zolotov: int = 1


def _generate_id_zolotov() -> int:
    """Потокобезопасная генерация уникального ID."""
    global _next_id_zolotov
    with _id_counter_lock_zolotov:
        current = _next_id_zolotov
        _next_id_zolotov += 1
    return current


# ---------- эндпоинты ----------

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user_zolotov(user: UserCreate):
    """Создание пользователя (сохранение в in-memory словарь)."""
    user_id_zolotov = _generate_id_zolotov()
    user_data_zolotov = user.model_dump()
    user_data_zolotov.pop("password", None)  # не храним пароль
    user_data_zolotov["id"] = user_id_zolotov
    db_zolotov[user_id_zolotov] = user_data_zolotov
    return user_data_zolotov


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_zolotov(user_id: int):
    """Получение пользователя по ID."""
    user_zolotov = db_zolotov.get(user_id)
    if user_zolotov is None:
        from app.exceptions import CustomExceptionA
        raise CustomExceptionA(detail=f"Пользователь с id={user_id} не найден")
    return user_zolotov


@router.delete("/{user_id}", status_code=204)
async def delete_user_zolotov(user_id: int):
    """Удаление пользователя по ID."""
    if user_id not in db_zolotov:
        from app.exceptions import CustomExceptionA
        raise CustomExceptionA(detail=f"Пользователь с id={user_id} не найден")
    del db_zolotov[user_id]
    return Response(status_code=204)
