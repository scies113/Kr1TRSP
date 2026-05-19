"""Эндпоинты для Задания 10.1 — демонстрация кастомных исключений."""

from fastapi import APIRouter

from app.exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/errors", tags=["Exceptions (10.1)"])


@router.get("/not-found/{item_id}")
async def get_item_zolotov(item_id: int):
    """Вызывает CustomExceptionA, если item_id < 0 (ресурс не найден)."""
    if item_id < 0:
        raise CustomExceptionA(detail=f"Элемент с id={item_id} не найден")
    return {"item_id": item_id, "status": "ok"}


@router.get("/forbidden/{age}")
async def check_age_zolotov(age: int):
    """Вызывает CustomExceptionB, если возраст < 18 (бизнес-правило)."""
    if age < 18:
        raise CustomExceptionB(
            detail=f"Доступ запрещён: возраст {age} меньше 18"
        )
    return {"age": age, "access": "granted"}
