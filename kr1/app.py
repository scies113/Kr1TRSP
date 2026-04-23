from fastapi import FastAPI
from fastapi.responses import FileResponse
from models import User, UserWithAge, Feedback

app = FastAPI()

feedbacks = []


#1.1
@app.get("/")
def read_root():
    """
    Корневой маршрут.
    Возвращает приветственное сообщение в формате JSON.
    """
    return {"message": "Авторелоад действительно работает"}


#1.2
@app.get("/html")
def read_html():
    """
    Возвращает HTML-страницу из файла index.html.
    """
    return FileResponse("index.html")


#1.3
@app.get("/calculate")
def calculate_get(num1: float, num2: float):
    """
    GET-версия для проверки в браузере.
    """
    result = num1 + num2
    return {"result": result}


@app.post("/calculate")
def calculate_post(num1: float, num2: float):
    """
    POST-версия как требуется в задании.
    """
    result = num1 + num2
    return {"result": result}

#1.4
current_user = User(name="Иван Иванов", id=1)

@app.get("/users")
def get_user():
    """
    Возвращает данные о пользователе в формате JSON.
    """
    return current_user.model_dump()


#1.5
@app.post("/user")
def create_user(user: UserWithAge):
    """
    Принимает данные пользователя (имя и возраст).
    Возвращает те же данные с дополнительным полем is_adult.
    """
    is_adult = user.age >= 18
    
    response = {
        "name": user.name,
        "age": user.age,
        "is_adult": is_adult
    }
    
    return response


#2.1 и 2.2
@app.post("/feedback")
def create_feedback(feedback: Feedback):
    """
    Принимает отзыв от пользователя.
    Валидирует данные (длина полей, запрещенные слова).
    Сохраняет отзыв в список.
    Возвращает подтверждение.
    """
    feedbacks.append(feedback.model_dump())
    
    return {"message": f"Спасибо, {feedback.name}! Ваш отзыв сохранён."}


@app.get("/feedbacks")
def get_all_feedbacks():
    """
    Возвращает список всех сохраненных отзывов.
    """
    return {"feedbacks": feedbacks}