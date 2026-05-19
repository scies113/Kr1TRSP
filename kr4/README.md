# Контрольная работа №4

**Автор: Максим Денисович Золотов, группа ЭФБО-12-24**

---

## Описание

Проект объединяет четыре задания в рамках контрольной работы:

| Задание | Тема |
|---------|------|
| **9.1** | Миграции БД через Alembic (модель `Product`) |
| **10.1** | Пользовательская обработка ошибок (кастомные исключения) |
| **10.2** | Валидация данных запроса (Pydantic-модель `User`) |
| **11.1 & 11.2** | Асинхронные модульные тесты (pytest-asyncio, httpx, Faker) |

**Стек**: FastAPI, SQLAlchemy (async PostgreSQL), Alembic, Pydantic, Pytest.

---

## Структура проекта

```
kr4/
├── alembic/                          # Конфигурация Alembic
│   ├── env.py                        # Async-окружение миграций
│   ├── script.py.mako                # Шаблон миграций
│   └── versions/
│       ├── 0001_create_products_table.py   # Миграция 1: создание таблицы + seed-данные
│       └── 0002_add_description_to_products.py  # Миграция 2: поле description
├── app/
│   ├── __init__.py
│   ├── config.py                     # Загрузка .env
│   ├── database.py                   # Async-движок и сессия SQLAlchemy
│   ├── exceptions.py                 # Кастомные исключения (10.1)
│   ├── main.py                       # Точка входа FastAPI
│   ├── models.py                     # SQLAlchemy-модели (Product)
│   ├── schemas.py                    # Pydantic-схемы
│   └── routers/
│       ├── __init__.py
│       ├── errors.py                 # Эндпоинты с исключениями (10.1)
│       ├── validation.py             # Эндпоинт валидации (10.2)
│       └── users.py                  # CRUD пользователей in-memory (11.1/11.2)
├── tests/
│   ├── __init__.py
│   └── test_users.py                 # Асинхронные тесты (11.1/11.2)
├── .env.example                      # Пример переменных окружения
├── .gitignore
├── alembic.ini                       # Конфигурация Alembic
├── pytest.ini                        # Конфигурация Pytest
├── requirements.txt                  # Зависимости Python
└── README.md
```

---

## Установка и запуск

### 1. Создание виртуального окружения и установка зависимостей

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и укажите свои параметры подключения к PostgreSQL:

```bash
cp .env.example .env
```

Пример `.env`:
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/kr4_db
```

### 3. Запуск миграций (Задание 9.1)

```bash
# Применить все миграции:
alembic upgrade head

# Откатить последнюю миграцию:
alembic downgrade -1
```

### 4. Запуск приложения

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

Документация Swagger UI: http://127.0.0.1:8000/docs

---

## Проверка основной функциональности

### Задание 10.1 — Кастомные исключения

```bash
# CustomExceptionA (404):
curl http://127.0.0.1:8000/errors/not-found/-1

# CustomExceptionB (403):
curl http://127.0.0.1:8000/errors/forbidden/15
```

### Задание 10.2 — Валидация данных

```bash
# Валидный запрос:
curl -X POST http://127.0.0.1:8000/validation/user \
  -H "Content-Type: application/json" \
  -d '{"username":"ivan","age":25,"email":"ivan@example.com","password":"SecurePass1"}'

# Невалидный запрос (age < 18):
curl -X POST http://127.0.0.1:8000/validation/user \
  -H "Content-Type: application/json" \
  -d '{"username":"ivan","age":15,"email":"bad-email","password":"short"}'
```

### Задание 11.1/11.2 — CRUD пользователей (in-memory)

```bash
# Создание:
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test_user","age":25,"email":"test@mail.com","password":"Password123"}'

# Получение по ID:
curl http://127.0.0.1:8000/users/1

# Удаление:
curl -X DELETE http://127.0.0.1:8000/users/1
```

---

## Запуск тестов

```bash
pytest -v
```

Тесты используют `httpx.AsyncClient` с `ASGITransport` (без запуска Uvicorn) и `Faker` для генерации данных. Состояние in-memory хранилища полностью изолируется между тестами.
