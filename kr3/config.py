import os
from pydantic_settings import BaseSettings
from pydantic import field_validator
from dotenv import load_dotenv

#загрузка переменных окружения
load_dotenv()

class Settings(BaseSettings):
    MODE: str
    SECRET_KEY: str
    DOCS_USER: str = "admin"
    DOCS_PASSWORD: str = "password123"
    
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator("MODE")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        #проверка режима работы
        if v not in ["DEV", "PROD"]:
            raise ValueError("MODE must be either 'DEV' or 'PROD'")
        return v

    class Config:
        env_file = ".env"

settings = Settings()
