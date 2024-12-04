from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .user import User
from model_db.working_db import DataBase
from routes.models.crypto_hash import get_password_hash, pwd_context


db = DataBase()
auth_admin = APIRouter()

#ready
@auth_admin.post("/admin/register")
async def register(user: User):
    """
    Регистрация нового пользователя в системе.
    
    Эта функция выполняет несколько шагов для регистрации нового пользователя:
    1. Проверяет, не зарегистрирован ли уже пользователь с таким именем в базе данных.
    2. Хэширует пароль пользователя для безопасного хранения.
    3. Добавляет нового пользователя с именем пользователя и хэшированным паролем в базу данных.
    4. Возвращает сообщение об успешной регистрации или ошибке в случае проблем с добавлением пользователя.

    :param user: Объект пользователя, который содержит имя пользователя и пароль.
    :type user: User

    :raises HTTPException:
        - Если имя пользователя уже зарегистрировано, возвращается ошибка с кодом 400 и сообщением "Username already registered".
        - Если произошла ошибка при добавлении пользователя в базу данных, возвращается ошибка с кодом 500 и сообщением "Failed to register user due to server error".
    
    :return: Сообщение о результате регистрации с кодом 200, если регистрация успешна.
    :rtype: dict
    """
    # если нечего нету вернет nano 
    user_db = await db.read_database('data_admin', user.username,['user_name', 'password'])
    
    if user_db != None:
        raise HTTPException(status_code=400, detail="Username already registered") # name busy 
    # hash password 
    hashed_password = get_password_hash(user.password)
    success = await db.add_user_database_in_table('data_admin', user.username, hashed_password)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to register user due to server error")

    return {"msg": "User registered successfully"}
        


@auth_admin.post("/admin/login")
async def login(user: User):
    """
    Эндпоинт для входа пользователя в систему.
    
    Эта функция принимает данные пользователя (имя пользователя и пароль) и выполняет следующие шаги:
    1. Проверяет, существует ли пользователь с указанным именем в базе данных.
    2. Если пользователь найден, проверяет, совпадает ли введённый пароль с хешированным паролем, хранящимся в базе данных.
    3. В случае успешного совпадения пароля возвращает сообщение об успешном входе.
    4. Если пользователь не найден или пароль неверный, возвращает ошибку с соответствующим сообщением.

    :param user: Объект пользователя, содержащий имя пользователя и пароль.
    :type user: User

    :raises HTTPException: 
        - Если имя пользователя не найдено в базе данных, возвращается ошибка с кодом 400 и сообщением "Username not found".
        - Если введённый пароль неверен, возвращается ошибка с кодом 400 и сообщением "Incorrect password".
    
    :return: Сообщение об успешном входе в систему с кодом 200, если вход успешен.
    :rtype: dict
    """
    
    user_db = await db.read_database('data_admin', user.username,['user_name', 'password'])
    
    if user_db is None:
        raise HTTPException(status_code=400, detail="Username already registered") 
    if not pwd_context.verify(user.password, user_db[1]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"msg": "User logged in successfully"}
