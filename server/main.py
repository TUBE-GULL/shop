from fastapi import FastAPI
from routes.root import root  
from model_db.working_db import DataBase
 
app = FastAPI()
app.include_router(root)


#
db = DataBase()
db._ensure_db_directory()
@app.on_event("startup")
async def startup():
    await db.create_table_user()
    await db.create_table_admin()
    await db.create_table_card()