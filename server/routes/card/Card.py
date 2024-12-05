from pydantic import BaseModel

class Card(BaseModel):
    name: str
    price: float # 
    unit: str # тип под счета 
    quantity: int 
    url_image: str # адрес img