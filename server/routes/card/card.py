from fastapi import APIRouter, HTTPException
from model_db.working_db import DataBase
from .Card import Card

card = APIRouter()
db = DataBase()

 

@card.post('/admin/add_product')
async def add_product(card: Card):
    print(card)
    
@card.delete('/admin/delete_product')
async def delete_product(card: Card):
    print(card)
    