from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from fastapi import HTTPException

#//модель_создания_пользователя
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = Field(None, description="Возраст должен быть больше 0")
    is_subscribed: Optional[bool] = False

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Возраст должен быть больше 0")
        return v

#//модель_общих_заголовков
class CommonHeaders(BaseModel):
    user_agent: str = Field(..., alias="User-Agent")
    accept_language: str = Field(..., alias="Accept-Language")

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, v):
        #//базовая_проверка_формата_заголовка
        if not v or ("," not in v and ";" not in v and "-" not in v):
            raise HTTPException(status_code=400, detail="Invalid Accept-Language format")
        return v
