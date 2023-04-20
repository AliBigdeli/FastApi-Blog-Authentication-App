from pydantic import BaseModel,EmailStr
from typing import List, Optional

class UserSchema(BaseModel):
    username: str 
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "alibigdeli",
                "email": "bigdeli.ali3@gmail.com",
                "password": "yourpassword"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr 
    password: str 

    class Config:
        schema_extra = {
            "example": {
                "email": "bigdeli.ali3@gmail.com",
                "password": "yourpassword"
            }
        }