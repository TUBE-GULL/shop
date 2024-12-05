from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from fastapi import Form

from model_db.working_db import DataBase
from routes.models.crypto_hash import get_password_hash, pwd_context

authorization = APIRouter()
db = DataBase()
auth = APIRouter()


def get_current_user(request: Request):
    return request.cookies.get("user")


@auth.get('/authorization')
def page_auth():
    file_path = Path(__file__).parent.parent.parent / "client/authorization/login.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


@auth.get('/authorization/r')
def page_auth():
    file_path = Path(__file__).parent.parent.parent / "client/authorization/register.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


#ready
@auth.post("/authorization/register")
async def register(username: str = Form(...), password: str = Form(...)):

    # если нечего нету вернет nano 
    user_db = await db.read_database('data_users', username,['user_name', 'password'])
    
    if user_db != None:
        raise HTTPException(status_code=400, detail="Username already registered") # name busy 
    # hash password 
    hashed_password = get_password_hash(password)
    success = await db.add_user_database_in_table('data_users', username, hashed_password)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to register user due to server error")

    return RedirectResponse(url='/authorization', status_code=303)
        


@auth.post("/authorization/login")
async def login(username: str = Form(...), password: str = Form(...)):
    
    user_db = await db.read_database('data_users', username,['user_name', 'password'])
    
    if user_db is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        # response = RedirectResponse(url='/authorization', status_code=303) 
    if not pwd_context.verify(password, user_db[1]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # response = RedirectResponse(url='/cabinet_admin', status_code=303)
    response = RedirectResponse(url='/shop', status_code=303)
    response.set_cookie(key="user", value=user_db[0])  # Сохр имя пользователя в cookie
    return response
