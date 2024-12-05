from fastapi import APIRouter, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path

shop = APIRouter()

# Проверка текущего пользователя
def get_current_user(request: Request):
    return request.cookies.get("user")

# Главная страница магазина (доступна всем)
@shop.get('/shop')
def page_shop(request: Request, current_user: str = Depends(get_current_user)):
    is_logged_in = current_user is not None  # Проверяем, авторизован ли пользователь
    file_path = Path(__file__).parent.parent.parent / "client/shop/index.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    if is_logged_in:
        # Дополняем страницу информацией для авторизованных пользователей
        html_content = html_content.replace("{{user_status}}", f"Logged in as: {current_user}")
    else:
        html_content = html_content.replace("{{user_status}}", "Not logged in")
    
    return HTMLResponse(content=html_content)

# Добавление товара в корзину (доступно всем, но для незарегистрированных данные временные)
@shop.post('/shop/add_to_cart')
async def add_to_cart(item_id: int, request: Request, current_user: str = Depends(get_current_user)):
    if current_user:
        # Логика для зарегистрированного пользователя (например, сохранить в БД)
        return {"message": f"Item {item_id} added to {current_user}'s cart"}
    else:
        # Логика для незарегистрированного пользователя (например, сохранить в cookies)
        cart = request.cookies.get("cart", "")
        updated_cart = f"{cart},{item_id}" if cart else str(item_id)
        response = HTMLResponse(content="Item added to cart")
        response.set_cookie(key="cart", value=updated_cart)
        return response

# Страница личного кабинета (доступ только авторизованным)
@shop.get('/shop/account')
def account_page(request: Request, current_user: str = Depends(get_current_user)):
    if not current_user:
        # Если пользователь не авторизован, перенаправляем на страницу входа
        return RedirectResponse(url="/login")
    
    # Если пользователь авторизован, отображаем личный кабинет
    file_path = Path(__file__).parent.parent.parent / "client/shop/account.html"
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    html_content = html_content.replace("{{username}}", current_user)
    return HTMLResponse(content=html_content)


