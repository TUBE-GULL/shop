from fastapi import APIRouter, UploadFile, File,HTTPException
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from model_db.working_db import DataBase

card = APIRouter()
db = DataBase()

static_path = Path(__file__).parent.parent.parent / "images"
card.mount("/static", StaticFiles(directory=static_path), name="static") 

 
@card.post('/admin/add_product')
async def add_product(name: str, group: str, price: int, unit: str, quantity: int, image: UploadFile = File(...)):
    print(image.filename)
    
    image_path = Path('images') / image.filename
    image_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Записываем изображение в файл в бинарном формате
        with open(image_path, 'wb') as f: 
            f.write(await image.read())
        
        await db.add_card(str(image_path), name, group, price, unit, quantity)
        # print(f"Product added successfully: {image_path}")
        return {"message": "Product added successfully", "image_path": str(image_path)}
    except Exception as e:
        # Логируем ошибку и возвращаем сообщение об ошибке
        # print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to add product due to server error")
    
    
    
    
    
@card.delete('/admin/delete_product')
async def delete_product():
    print('delete')
    