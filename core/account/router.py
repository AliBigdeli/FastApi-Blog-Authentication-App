from fastapi import APIRouter
# from core import database

router = APIRouter(
    prefix="/account/api/v1/user",
    tags=["Account"]
)

# get_db = database.get_db

@router.post('/login/')
def account_login(username,password):
    return {"access_token":"adasdasdasdasd","refresh_token":"asdasdasdasd","type":"Bearer"}

@router.post('/refresh/')
def account_refresh_token(refresh_token):
    return {"access_token":"adasdasdasdasd"}

@router.post('/register/')
def account_register(username,password):
    return {"username": username, "password": password}