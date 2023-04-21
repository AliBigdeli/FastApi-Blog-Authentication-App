from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from accounts.auth import auth_handler 
from accounts.auth.auth_bearer import JWTBearer
from core.database import get_db
from sqlalchemy.orm import Session
from . import models
from . import schemas


router = APIRouter(
    prefix="/accounts/api/v1/user",
    tags=["Account"]
)

# get_db = database.get_db


@router.post('/login/', response_model=schemas.ResponseUserLoginSchema, status_code=status.HTTP_200_OK)
def account_login(request: schemas.UserLoginSchema,db: Session = Depends(get_db)):
    user_obj = db.query(models.UserModel).filter(models.UserModel.email == request.email).first()
    if not user_obj:
        raise HTTPException(status_code=403, detail="Authentication failed")
    elif user_obj.password != request.password:
        raise HTTPException(status_code=403, detail="Authentication failed")
    
    access_token = auth_handler.encode_access_jwt(user_obj.id)
    refresh_token = auth_handler.encode_refresh_jwt(user_obj.id)
    return JSONResponse({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": 1,
        "email": request.email

    }, status_code=status.HTTP_201_CREATED)


@router.post('/refresh/', response_model=schemas.ResponseRefreshTokenSchema, status_code=status.HTTP_201_CREATED)
def account_refresh_token(request: schemas.RefreshTokenSchema,db: Session = Depends(get_db)):
    user_id = auth_handler.decode_refresh_jwt(request.refresh_token).get("user_id")
    print("user_id",user_id)
    access_token = auth_handler.encode_access_jwt(user_id)
    refresh_token = auth_handler.encode_refresh_jwt(user_id)
    return JSONResponse({
        "access_token": access_token,
        "refresh_token": refresh_token,

    }, status_code=status.HTTP_201_CREATED)


@router.post('/register/', response_model=schemas.ResponseUserRegistrationSchema, status_code=status.HTTP_201_CREATED)
def account_register(request: schemas.UserRegistrationSchema,db: Session = Depends(get_db)):
    if request.password != request.password1:
        raise HTTPException(status_code=400, detail="passwords doest match")
    
    user_obj = models.UserModel(email=request.email,
                                password=request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return JSONResponse({
        "detail": "user has been registered successfully, please go ahead on login"
    }, status_code=status.HTTP_201_CREATED)
