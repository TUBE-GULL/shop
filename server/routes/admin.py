from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends
from pathlib import Path
from fastapi import Form

from model_db.working_db import DataBase
from routes.models.crypto_hash import get_password_hash, pwd_context


db = DataBase()
# templates = Jinja2Templates(directory="client/admin")

admin = APIRouter()

def get_current_user(request: Request):
    return request.cookies.get("user")


@admin.get('/admin')
def page_admin():
    file_path = Path(__file__).parent.parent.parent / "client/admin/login.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)



@admin.get('/admin/r')
def page_admin():
    file_path = Path(__file__).parent.parent.parent / "client/admin/register.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)



#ready
@admin.post("/admin/register")
async def register(
    username: str = Form(...), 
    password: str = Form(...), 
    current_user: str = Depends(get_current_user)
):

    if current_user is None:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")

    
    # если нечего нету вернет nano usernameuser.username,['user_name', 'password'])
    user_db = await db.read_database('data_admin', username,['user_name', 'password', 'role'])

    print(user_db)
    
    if user_db != None:
        raise HTTPException(status_code=400, detail="Unauthorized. Please log in.") # name busy 
        
    # hash password 
    hashed_password = get_password_hash(password)
    success = await db.add_user_database_in_table('data_admin', username, hashed_password)
    
    if not success:
          raise HTTPException(status_code=500, detail="Failed to register user due to server error")

      # Устанавливаем RedirectResponse со статусом 303
    return RedirectResponse(url='/admin', status_code=303)



@admin.post("/admin/login")
async def login(username: str = Form(...), password: str = Form(...)):
    print(f"Username: {username}, Password: {password}")
       
    user_db = await db.read_database('data_admin', username,['user_name', 'password'])
    
    if user_db is None:
        raise HTTPException(status_code=401, detail="Invalid credentials") 
    if not pwd_context.verify(password, user_db[1]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    response = RedirectResponse(url='/cabinet_admin', status_code=303)
    response.set_cookie(key="user", value=user_db[0])  # Сохр имя пользователя в cookie
    return response



@admin.get('/cabinet_admin')
def page_admin(request: Request, current_user: str = Depends(get_current_user)):
    if current_user is None:
        return RedirectResponse(url='/admin')
    
    
    file_path = Path(__file__).parent.parent.parent / "client/admin/admin.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)