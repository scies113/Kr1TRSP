# Проект FastAPI: Комплексная безопасность и работа с БД

Контрольная работа №3 по дисциплине "Технологии разработки серверных приложений".

## Установка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Создайте файл `.env` на основе `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Укажите нужный режим `MODE` (DEV или PROD) и секретный ключ `SECRET_KEY`.

## Запуск

```bash
uvicorn kr3.main:app --reload
```

## Тестирование эндпоинтов

### 6.1 Базовая аутентификация (Простая)
```bash
curl -u user123:password123 http://127.0.0.1:8000/login_basic_simple
```

### 6.2 Продвинутая базовая аутентификация
```bash
#регистрация
curl -X POST http://127.0.0.1:8000/register_basic -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}'
#логин
curl -u testuser:testpassword http://127.0.0.1:8000/login_basic_advanced
```

### 6.3 Документация
- Если `MODE=DEV`, доступ к `http://127.0.0.1:8000/docs` осуществляется с использованием `DOCS_USER` и `DOCS_PASSWORD` из `.env`.
- Если `MODE=PROD`, документация отключена (404).

### 6.4 & 6.5 JWT-аутентификация и Rate Limiting
```bash
#регистрация (макс. 1 запрос в минуту)
curl -X POST http://127.0.0.1:8000/register -H "Content-Type: application/json" -d '{"username": "jwtuser", "password": "jwtpassword"}'
#логин (макс. 5 запросов в минуту)
curl -X POST http://127.0.0.1:8000/login -H "Content-Type: application/json" -d '{"username": "jwtuser", "password": "jwtpassword"}'
#получите токен из ответа и используйте его:
curl http://127.0.0.1:8000/protected_resource -H "Authorization: Bearer <ВАШ_ТОКЕН>"
```

### 7.1 RBAC (Управление доступом на основе ролей)
Зарегистрируйте пользователя. По умолчанию новым пользователям назначается роль "user". Для тестирования других ролей можно вручную изменить значение в `fake_users_db` в коде.

### 8.1 SQLite (Чистый SQL)
```bash
curl -X POST http://127.0.0.1:8000/db/register -H "Content-Type: application/json" -d '{"username": "dbuser", "password": "dbpassword"}'
```

### 8.2 SQLite CRUD (Задачи/Todos)
```bash
#создание
curl -X POST http://127.0.0.1:8000/todos -H "Content-Type: application/json" -d '{"title": "Задача 1", "description": "Сделать КР3"}'
#чтение всех
curl http://127.0.0.1:8000/todos
#обновление
curl -X PUT http://127.0.0.1:8000/todos/1 -H "Content-Type: application/json" -d '{"completed": true}'
#удаление
curl -X DELETE http://127.0.0.1:8000/todos/1
```
