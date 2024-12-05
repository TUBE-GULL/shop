from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from model_db.working_db import DataBase
from routes.models.crypto_hash import get_password_hash, pwd_context

# Инициализация базы данных и роутеров
db = DataBase()
auth = APIRouter()

# Вспомогательная функция для получения текущего пользователя из cookie
def get_current_user(request: Request):
    return request.cookies.get("user")


@auth.get('/authorization', summary="Показать страницу авторизации", response_class=HTMLResponse)
async def page_auth():
    """
    Отображает страницу авторизации.

    Возвращает:
        HTMLResponse: HTML-контент страницы авторизации.
    """
    file_path = Path(__file__).parent.parent.parent / "client/authorization/login.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@auth.get('/authorization/r', summary="Показать страницу регистрации", response_class=HTMLResponse)
async def page_auth():
    """
    Отображает страницу регистрации для пользователей.

    Возвращает:
        HTMLResponse: HTML-контент страницы регистрации.
    """
    file_path = Path(__file__).parent.parent.parent / "client/authorization/register.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@auth.post("/authorization/register", summary="Регистрация нового пользователя", status_code=201)
async def register(username: str = Form(...), password: str = Form(...)):
    """
    Регистрирует нового пользователя в системе. Проверяет, что имя пользователя еще не занято.
    
    Аргументы:
        username (str): Имя пользователя, которое нужно зарегистрировать.
        password (str): Пароль для нового пользователя.
    
    Возвращает:
        RedirectResponse: Редирект на страницу авторизации после успешной регистрации.
    
    Исключения:
        HTTPException: Если имя пользователя уже занято или произошла ошибка на сервере.
    """
    # Проверка, существует ли уже пользователь с таким именем
    user_db = await db.read_database('data_users', username, ['user_name', 'password'])
    if user_db is not None:
        raise HTTPException(status_code=400, detail="Имя пользователя уже зарегистрировано")
    
    # Хеширование пароля и добавление пользователя в базу данных
    hashed_password = get_password_hash(password)
    success = await db.add_user_database_in_table('data_users', username, hashed_password)
    if not success:
        raise HTTPException(status_code=500, detail="Не удалось зарегистрировать пользователя из-за ошибки на сервере")

    return RedirectResponse(url='/authorization', status_code=303)


@auth.post("/authorization/login", summary="Авторизация пользователя")
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Авторизует пользователя, проверяя его имя пользователя и пароль.
    
    Аргументы:
        username (str): Имя пользователя для авторизации.
        password (str): Пароль пользователя.
    
    Возвращает:
        RedirectResponse: Редирект на страницу магазина после успешной авторизации.
    
    Исключения:
        HTTPException: Если учетные данные неверные.
    """
    # Проверка существования пользователя и правильности пароля
    user_db = await db.read_database('data_users', username, ['user_name', 'password'])
    if user_db is None or not pwd_context.verify(password, user_db[1]):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    
    # Успешная авторизация, установка cookie и редирект на страницу магазина
    response = RedirectResponse(url='/shop', status_code=303)
    response.set_cookie(key="user", value=user_db[0])  # Сохраняем имя пользователя в cookie
    return response
