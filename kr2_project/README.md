# FastAPI Контрольная работа №2

Приложение "СЕРВЕРНЫЕ API И СИСТЕМА АУТЕНТИФИКАЦИИ" для дисциплины "Технологии разработки серверных приложений".

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск

Из директории `kr2_project` выполните:
```bash
uvicorn app:app --reload
```

## Примеры запросов (curl)

### 1. Создание пользователя
```bash
curl -X POST "http://127.0.0.1:8000/create_user" \
     -H "Content-Type: application/json" \
     -d "{\"name\": \"Ivan\", \"email\": \"ivan@example.com\", \"age\": 25, \"is_subscribed\": true}"
```

### 2. Поиск продуктов
```bash
curl "http://127.0.0.1:8000/products/search?keyword=lap&limit=5"
```

### 3. Получение продукта по ID
```bash
curl "http://127.0.0.1:8000/product/1"
```

### 4. Авторизация (Login)
```bash
# Сохранение куки в файл cookies.txt
curl -c cookies.txt -X POST "http://127.0.0.1:8000/login" \
     -d "username=user123&password=password123"
```

### 5. Проверка профиля (с куками)
```bash
# Использование сохраненных кук
curl -b cookies.txt "http://127.0.0.1:8000/profile"
```

### 6. Заголовки (Headers)
```bash
curl "http://127.0.0.1:8000/info" \
     -H "User-Agent: Mozilla/5.0" \
     -H "Accept-Language: ru-RU,ru;q=0.9"
```

## Особенности реализации
- **Pydantic v2**: Использование `field_validator`.
- **Itsdangerous**: Подпись cookie (HMACSHA256).
- **Stateless Auth**: Хранение состояния в токене.
- **Динамические сессии**: Продление за 2 минуты до истечения.
