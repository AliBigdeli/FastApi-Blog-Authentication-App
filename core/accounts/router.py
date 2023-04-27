from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from accounts.auth import auth_handler 
from accounts.auth.auth_bearer import JWTBearer
from core.database import get_db
from sqlalchemy.orm import Session
from . import models
from . import schemas
import bcrypt

router = APIRouter(
    prefix="/accounts/api/v1/user",
    tags=["Account"]
)

# get_db = database.get_db


@router.post('/login/', response_model=schemas.ResponseUserLoginSchema, status_code=status.HTTP_200_OK)
def account_login(request: schemas.UserLoginSchema,db: Session = Depends(get_db)):

    user_obj = db.query(models.UserModel).filter(models.UserModel.email == request.email).first()

    if not user_obj:
        raise HTTPException(status_code=401, detail="Authentication failed")

    encoded_password = request.password.encode('utf-8')
    if not bcrypt.checkpw(encoded_password, user_obj.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    access_token = auth_handler.encode_access_jwt(user_obj.id)
    refresh_token = auth_handler.encode_refresh_jwt(user_obj.id)
    return JSONResponse({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user_obj.id,
        "email": request.email

    }, status_code=status.HTTP_200_OK)


@router.post('/refresh/', response_model=schemas.ResponseRefreshTokenSchema, status_code=status.HTTP_201_CREATED)
def account_refresh_token(request: schemas.RefreshTokenSchema,db: Session = Depends(get_db)):
    user_id = auth_handler.decode_refresh_jwt(request.refresh_token).get("user_id")
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
    
    user_obj = db.query(models.UserModel).filter(
        models.UserModel.email == request.email.lower()).first()
    if user_obj:
        raise HTTPException(status_code=409, detail="user already exists you cannot create another with the same email")
    
    encoded_password = request.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    
    user_obj = models.UserModel(email=request.email,
                                password=hashed_password.decode("utf-8"))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return JSONResponse({
        "detail": "user has been registered successfully, please go ahead on login"
    }, status_code=status.HTTP_201_CREATED)
