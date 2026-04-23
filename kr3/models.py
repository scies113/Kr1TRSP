from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal

#---модели пользователей---
class UserBase(BaseModel):
    username: str

class User(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    role: str = "user"

class UserWithRole(UserBase):
    role: Literal["admin", "user", "guest"]

class UserLogin(BaseModel):
    username: str
    password: str

#---модели токенов---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

#---модели задач---
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = ""

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    completed: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    username: str
