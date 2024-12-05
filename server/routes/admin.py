from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from pathlib import Path
from typing import Optional

from model_db.working_db import DataBase
from routes.models.crypto_hash import get_password_hash, pwd_context

db = DataBase()

# Создаем объект для маршрутов администратора
admin = APIRouter()

def get_current_user(request: Request):
    """Функция для получения текущего пользователя из cookie"""
    return request.cookies.get("user")

@admin.get('/admin', response_class=HTMLResponse, description="Страница входа для администраторов")
async def page_admin():
    """
    Отображает страницу входа для администраторов.
    
    Возвращает HTML-страницу с формой для входа администратора.
    """
    file_path = Path(__file__).parent.parent.parent / "client/admin/login.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@admin.get('/admin/r', response_class=HTMLResponse, description="Страница регистрации для администраторов")
async def page_admin_register():
    """
    Отображает страницу регистрации для администраторов.

    Возвращает HTML-страницу с формой для регистрации нового администратора.
    """
    file_path = Path(__file__).parent.parent.parent / "client/admin/register.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@admin.post("/admin/register", status_code=status.HTTP_201_CREATED, description="Регистрация нового пользователя")
async def register(
    username: str = Form(..., description="Имя пользователя"),
    password: str = Form(..., description="Пароль пользователя"),
    current_user: Optional[str] = Depends(get_current_user)
):
    """
    Регистрация нового администратора в системе.

    Если пользователь уже существует, будет возвращена ошибка 400.
    Пароль хешируется перед сохранением в базе данных.
    """
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized. Please log in.")

    user_db = await db.read_database('data_admin', username, ['user_name', 'password', 'role'])
    
    if user_db is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already taken")
    
    hashed_password = get_password_hash(password)
    success = await db.add_user_database_in_table('data_admin', username, hashed_password)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user due to server error")
    
    return RedirectResponse(url='/admin', status_code=status.HTTP_303_SEE_OTHER)

@admin.post("/admin/login", description="Авторизация пользователя в системе")
async def login(
    username: str = Form(..., description="Имя пользователя для входа"),
    password: str = Form(..., description="Пароль пользователя для входа")
):
    """
    Логин администратора в систему.

    Если введенные данные неверны, возвращается ошибка 401 или 400.
    Успешная авторизация перенаправляет на личный кабинет с установкой cookie для пользователя.
    """
    user_db = await db.read_database('data_admin', username, ['user_name', 'password'])
    
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not pwd_context.verify(password, user_db[1]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    response = RedirectResponse(url='/cabinet_admin', status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="user", value=user_db[0])  # Устанавливаем cookie для текущего пользователя
    return response

@admin.get('/cabinet_admin', description="Личный кабинет администратора")
async def page_admin_cabinet(request: Request, current_user: str = Depends(get_current_user)):
    """
    Личный кабинет администратора, доступен только для авторизованных пользователей.
    
    Если пользователь не авторизован, происходит перенаправление на страницу входа.
    """
    if current_user is None:
        return RedirectResponse(url='/admin')
    
    file_path = Path(__file__).parent.parent.parent / "client/admin/admin.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)
