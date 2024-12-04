from fastapi import APIRouter

auth = APIRouter()

@auth.get('/authorization')
def page_auth():
    return {"message": "Login route"}
