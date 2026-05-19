"""Pydantic-схемы для валидации и ответов."""

from typing import Any, Optional
from pydantic import BaseModel, EmailStr, conint, constr, Field


# ---------- Задание 10.1 — схема ответа об ошибке ----------
class ErrorResponse(BaseModel):
    """Стандартный формат ответа при ошибке."""
    detail: str
    error_code: str


# ---------- Задание 10.2 — валидация User ----------
class UserCreate(BaseModel):
    """Модель валидации входящего JSON пользователя."""
    username: str
    age: int = Field(..., gt=18)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class UserResponse(BaseModel):
    """Ответ при успешном создании / получении пользователя."""
    id: int
    username: str
    age: int
    email: str
    phone: Optional[str] = "Unknown"


# ---------- Задание 10.2 — кастомный ответ ValidationError ----------
class ValidationErrorDetail(BaseModel):
    field: str
    message: str


class CustomValidationErrorResponse(BaseModel):
    error: str = "Validation Error"
    details: list[ValidationErrorDetail]
