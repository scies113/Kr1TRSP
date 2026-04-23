import secrets
import sqlite3
from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import settings
from .models import (
    User, UserInDB, UserBase, UserLogin, Token, TokenData, 
    UserWithRole, Todo, TodoCreate, TodoUpdate, UserResponse
)
from .utils import hash_password, verify_password, create_access_token, verify_token
from .database import get_db_connection

#---инициализация---
limiter = Limiter(key_func=get_remote_address)
app_params = {}

#отключение документации в режиме PROD
if settings.MODE == "PROD":
    app_params.update({
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None
    })

app = FastAPI(**app_params)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

security_basic = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_jwt")

#---база пользователей в памяти для задач 6.2, 6.5, 7.1---
fake_users_db = {}

#---зависимости---

#6.1 зависимость простой базовой аутентификации
def get_basic_user(credentials: Annotated[HTTPBasicCredentials, Depends(security_basic)]):
    correct_username = secrets.compare_digest(credentials.username, "user123")
    correct_password = secrets.compare_digest(credentials.password, "password123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

#6.2 зависимость продвинутой базовой аутентификации
def auth_user(credentials: Annotated[HTTPBasicCredentials, Depends(security_basic)]):
    user_data = fake_users_db.get(credentials.username)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not verify_password(credentials.password, user_data.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user_data

#6.3 зависимость для защиты документации
def docs_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security_basic)]):
    correct_username = secrets.compare_digest(credentials.username, settings.DOCS_USER)
    correct_password = secrets.compare_digest(credentials.password, settings.DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

#6.4 & 7.1 зависимости для JWT и RBAC
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    user = fake_users_db.get(username)
    if user is None:
         raise HTTPException(status_code=401, detail="User not found")
    return user

#проверка ролей
def require_role(allowed_roles: List[str]):
    def role_checker(current_user: Annotated[UserInDB, Depends(get_current_user)]):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

#---кастомные маршруты документации для задачи 6.3 (режим DEV)---
if settings.MODE == "DEV":
    @app.get("/docs", include_in_schema=False)
    async def get_documentation(username: str = Depends(docs_auth)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

    @app.get("/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint(username: str = Depends(docs_auth)):
        return get_openapi(title="FastAPI", version="1.0.0", routes=app.routes)

#---эндпоинты---

#6.1 базовая аутентификация
@app.get("/login_basic_simple")
async def login_basic_simple(username: str = Depends(get_basic_user)):
    return {"message": "You got my secret, welcome"}

#6.2 регистрация и логин с использованием PassLib
@app.post("/register_basic")
async def register_basic(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = hash_password(user.password)
    fake_users_db[user.username] = UserInDB(username=user.username, hashed_password=hashed)
    return {"message": "User registered successfully"}

@app.get("/login_basic_advanced")
async def login_basic_advanced(user: UserInDB = Depends(auth_user)):
    return {"message": f"Welcome, {user.username}!"}

#6.4 & 6.5 JWT аутентификация и ограничение частоты запросов
@app.post("/register")
@limiter.limit("1/minute")
async def register(request: Request, user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    hashed = hash_password(user.password)
    #роль по умолчанию для задачи 7.1
    fake_users_db[user.username] = UserInDB(username=user.username, hashed_password=hashed, role="user")
    return {"message": "New user created"}, status.HTTP_201_CREATED

@app.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, user_data: UserLogin):
    user = fake_users_db.get(user_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization failed")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected_resource")
async def protected_resource(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return {"message": "Access granted", "user": current_user.username}

#7.1 управление доступом на основе ролей (RBAC)
@app.get("/rbac/protected", dependencies=[Depends(require_role(["admin", "user"]))])
async def rbac_protected():
    return {"message": "Access granted to protected resource"}

@app.post("/admin/create", dependencies=[Depends(require_role(["admin"]))])
async def admin_create():
    return {"message": "Resource created by admin"}

@app.put("/user/update", dependencies=[Depends(require_role(["user", "admin"]))])
async def user_update():
    return {"message": "Resource updated"}

@app.get("/guest/read", dependencies=[Depends(require_role(["admin", "user", "guest"]))])
async def guest_read():
    return {"message": "Public data accessed"}

#8.1 регистрация в SQLite (чистый SQL)
@app.post("/db/register", response_model=UserResponse)
async def db_register(user: UserLogin):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, user.password) #хранение пароля в открытом виде согласно 8.1
            )
            user_id = cursor.lastrowid
            conn.commit()
            return {"id": user_id, "username": user.username}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")

#8.2 CRUD операции для задач в SQLite
@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, description, completed) VALUES (?, ?, 0)",
            (todo.title, todo.description)
        )
        todo_id = cursor.lastrowid
        conn.commit()
        return {**todo.model_dump(), "id": todo_id, "completed": False}

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return dict(row)

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        #получение текущих данных
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        current_data = dict(row)
        title = todo_update.title if todo_update.title is not None else current_data['title']
        description = todo_update.description if todo_update.description is not None else current_data['description']
        completed = int(todo_update.completed) if todo_update.completed is not None else current_data['completed']
        
        cursor.execute(
            "UPDATE todos SET title=?, description=?, completed=? WHERE id=?",
            (title, description, completed, todo_id)
        )
        conn.commit()
        return {"id": todo_id, "title": title, "description": description, "completed": bool(completed)}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        return {"message": "Todo deleted successfully"}

@app.get("/todos", response_model=List[Todo])
async def read_todos():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
