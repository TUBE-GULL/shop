from fastapi import APIRouter

shop = APIRouter()

@shop.get('/shop')
def get_shop():
    return {"message": "welcom with shop !"}