from fastapi import APIRouter


from routes.auth import auth  
from routes.authorization.authorization import authorization 


from routes.admin import admin 
from routes.authorization.auth_admin import auth_admin 


from routes.shop import shop  
 

 

root = APIRouter()

# get (html)
root.include_router(auth)
# post
root.include_router(authorization)

# get (html)
root.include_router(admin)
# post
root.include_router(auth_admin)

# get (html)
root.include_router(shop)

