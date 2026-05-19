"""Кастомные исключения (Задание 10.1)."""


class CustomExceptionA(Exception):
    """Ресурс не найден (HTTP 404)."""

    def __init__(self, detail: str = "Запрашиваемый ресурс не найден"):
        self.detail = detail
        self.status_code = 404
        self.error_code = "RESOURCE_NOT_FOUND"


class CustomExceptionB(Exception):
    """Бизнес-правило нарушено (HTTP 403)."""

    def __init__(self, detail: str = "Доступ запрещён: условие не выполнено"):
        self.detail = detail
        self.status_code = 403
        self.error_code = "BUSINESS_RULE_VIOLATION"
