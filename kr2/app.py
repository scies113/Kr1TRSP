from fastapi import FastAPI, HTTPException, Response, Request, Header, Depends, Form
from typing import List, Optional
from datetime import datetime
import time

from models import UserCreate, CommonHeaders
from utils import generate_signed_token, verify_signed_token, check_session_extension, signer

app = FastAPI(title="FastAPI Server API & Auth System")

#//захардкоженные_данные_продуктов
sample_products = [
    {"product_id": 1, "name": "Laptop", "category": "Electronics", "price": 1200.0},
    {"product_id": 2, "name": "Smartphone", "category": "Electronics", "price": 800.0},
    {"product_id": 3, "name": "Coffee Maker", "category": "Appliances", "price": 150.0},
    {"product_id": 4, "name": "Desk Chair", "category": "Furniture", "price": 200.0},
    {"product_id": 5, "name": "Headphones", "category": "Electronics", "price": 100.0},
]

#//3.1_создание_пользователя
@app.post("/create_user")
async def create_user(user: UserCreate):
    return user

#//3.2_поиск_продуктов_(объявлен_ДО_/{product_id})
@app.get("/products/search")
async def search_products(keyword: str, category: Optional[str] = None, limit: int = 10):
    results = [
        p for p in sample_products 
        if keyword.lower() in p["name"].lower()
    ]
    if category:
        results = [p for p in results if p["category"].lower() == category.lower()]
    return results[:limit]

#//3.2_получение_продукта_по_id
@app.get("/product/{product_id}")
async def get_product(product_id: int):
    product = next((p for p in sample_products if p["product_id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

#//3.3/3.4/3.5_логин_и_установка_подписанной_куки
@app.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    #//хардкод_валидации
    if username == "user123" and password == "password123":
        token = generate_signed_token(user_id="user123")
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            max_age=300 #//5_минут_согласно_5.3
        )
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

#//3.3_базовая_проверка_куки
@app.get("/user")
async def get_user(request: Request):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_id, _ = verify_signed_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return {"username": user_id, "role": "admin"}

#//3.4/3.5_расширенная_проверка_с_динамическим_продлением
@app.get("/profile")
async def get_profile(request: Request, response: Response):
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_id, timestamp = verify_signed_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    status, new_timestamp = check_session_extension(timestamp)
    
    if status == "expired":
        raise HTTPException(status_code=401, detail="Session expired")
    
    if status == "refresh":
        #//генерация_нового_токена_с_обновленным_временем
        new_payload = f"{user_id}.{new_timestamp}"
        new_token = signer.sign(new_payload).decode()
        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            max_age=300
        )
    
    return {
        "user_id": user_id,
        "last_activity": datetime.fromtimestamp(timestamp).isoformat(),
        "status": "session active"
    }

#//3.6_извлечение_заголовков_напрямую
@app.get("/headers")
async def get_headers(request: Request):
    user_agent = request.headers.get("User-Agent")
    accept_language = request.headers.get("Accept-Language")
    
    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Missing required headers")
        
    return {"User-Agent": user_agent, "Accept-Language": accept_language}

#//3.7_использование_модели_заголовков
@app.get("/info")
async def get_info(response: Response, headers: CommonHeaders = Depends()):
    #//добавление_кастомного_заголовка
    response.headers["X-Server-Time"] = datetime.utcnow().isoformat()
    
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }
