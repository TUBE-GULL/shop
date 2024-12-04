from fastapi import APIRouter

admin = APIRouter()

@admin.get('/admin')
def page_admin():
    return {"message": "Admin route"}
