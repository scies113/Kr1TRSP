import time
import uuid
from itsdangerous import Signer, BadSignature
from config import SECRET_KEY

#//инициализация_подписчика
signer = Signer(SECRET_KEY, algorithm="HMACSHA256")

#//генерация_подписанного_токена
def generate_signed_token(user_id: str = None) -> str:
    if user_id is None:
        user_id = str(uuid.uuid4())
    timestamp = int(time.time())
    payload = f"{user_id}.{timestamp}"
    return signer.sign(payload).decode()

#//проверка_подписанного_токена
def verify_signed_token(token: str):
    try:
        #//проверка_подписи_и_извлечение_данных
        unsigned_payload = signer.unsign(token).decode()
        parts = unsigned_payload.split(".")
        if len(parts) != 2:
            return None, None
        
        user_id, timestamp_str = parts
        return user_id, int(timestamp_str)
    except (BadSignature, ValueError):
        return None, None

#//логика_продления_сессии
def check_session_extension(timestamp: int):
    current_time = int(time.time())
    delta = current_time - timestamp
    
    if delta >= 300:
        #//сессия_истекла
        return "expired", None
    elif delta >= 180:
        #//нужно_обновить_куку
        return "refresh", current_time
    else:
        #//сессия_валидна_обновление_не_требуется
        return "valid", None
