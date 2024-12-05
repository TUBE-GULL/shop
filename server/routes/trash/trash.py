from fastapi import APIRouter, HTTPException
from model_db.working_db import DataBase
from .Trash import Trash

trash = APIRouter()
db = DataBase()

 
@trash.post('/trash/add_product')
async def add_product(trash: Trash):
    print(trash)
    
@trash.delete('/trash/delete_product')
async def delete_product(trash: Trash):
    print(trash)
    