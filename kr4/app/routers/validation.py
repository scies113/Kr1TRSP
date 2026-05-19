"""Эндпоинт для Задания 10.2 — валидация данных пользователя."""

from fastapi import APIRouter

from app.schemas import UserCreate

router = APIRouter(prefix="/validation", tags=["Validation (10.2)"])


@router.post("/user")
async def create_validated_user_zolotov(user: UserCreate):
    """Принимает JSON с данными пользователя и валидирует через Pydantic."""
    return {
        "message": "Пользователь успешно валидирован",
        "user": user.model_dump(),
    }
