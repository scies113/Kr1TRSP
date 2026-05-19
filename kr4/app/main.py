"""Главный модуль FastAPI-приложения.

Объединяет задания 9.1, 10.1, 10.2, 11.1 и 11.2 в одном проекте.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.schemas import ErrorResponse, CustomValidationErrorResponse, ValidationErrorDetail
from app.routers import errors, validation, users

app = FastAPI(
    title="КР-4 — Золотов Максим Денисович (ЭФБО-12-24)",
    description="Контрольная работа №4: FastAPI + Alembic + Pydantic + Pytest",
    version="1.0.0",
)

# -------- Подключение роутеров --------
app.include_router(errors.router)
app.include_router(validation.router)
app.include_router(users.router)


# -------- Задание 10.1 — обработчики кастомных исключений --------

@app.exception_handler(CustomExceptionA)
async def handle_custom_exception_a(request: Request, exc: CustomExceptionA):
    """Обработчик CustomExceptionA (404 — ресурс не найден)."""
    body = ErrorResponse(detail=exc.detail, error_code=exc.error_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=body.model_dump(),
    )


@app.exception_handler(CustomExceptionB)
async def handle_custom_exception_b(request: Request, exc: CustomExceptionB):
    """Обработчик CustomExceptionB (403 — бизнес-правило)."""
    body = ErrorResponse(detail=exc.detail, error_code=exc.error_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=body.model_dump(),
    )


# -------- Задание 10.2 — кастомный перехватчик RequestValidationError --------

@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    """Информативный ответ при ошибках валидации вместо стандартного FastAPI."""
    details = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err.get("loc", []))
        details.append(
            ValidationErrorDetail(field=field, message=err.get("msg", ""))
        )
    body = CustomValidationErrorResponse(details=details)
    return JSONResponse(status_code=422, content=body.model_dump())


# -------- Корневой эндпоинт --------

@app.get("/", tags=["Root"])
async def root():
    return {
        "project": "КР-4",
        "author": "Золотов Максим Денисович",
        "group": "ЭФБО-12-24",
    }
