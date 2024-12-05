from fastapi import APIRouter
from routes.auth import auth  
from routes.admin import admin 
from routes.shop import shop  
from routes.card.card import card
from routes.trash.trash import trash

root = APIRouter()
root.include_router(auth)
root.include_router(admin)
root.include_router(shop)
root.include_router(card)
root.include_router(trash)

