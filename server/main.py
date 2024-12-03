# импортируем FastAPI
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List


app = FastAPI()

class admin():



# class Product(product):
#     name :str 
#     group : str 
#     price : float 
#     unit : str 
#     quantity : float 
    
#     shopping_list : List[Product] = []
    
#     @app.post('/products')
#     def add_product(product:Product)
#         """Добавить товар в список покупок"""
        
#         shopping_list.append(product)
#         return{"message": "Товар добавлен", "item": item}



