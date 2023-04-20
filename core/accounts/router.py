from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
# from core import database
from accounts.schemas import UserLoginSchema
from accounts.auth.auth_handler import sign_jwt
from accounts.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/accounts/api/v1/user",
    tags=["Account"]
)

# get_db = database.get_db


@router.post('/login/')
def account_login(request: UserLoginSchema):

    access_token = sign_jwt(request.email)
    refresh_token = sign_jwt(request.email)
    return JSONResponse({
        "access_token": access_token,
        "refresh_token":refresh_token,
        "user_id":1,
        "email":request.email
            
    }, status_code=status.HTTP_200_OK)


@router.post('/refresh/', dependencies=[Depends(JWTBearer())])
def account_refresh_token(refresh_token):
    return {"access_token": "adasdasdasdasd"}


@router.post('/register/')
def account_register(username, password):
    return {"username": username, "password": password}
