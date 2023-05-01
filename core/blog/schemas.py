from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
class PostSchema(BaseModel):
    title : str
    content : str
    is_published: bool
    
class PostUpdateSchema(BaseModel):
    title : Optional[str]= None
    content : Optional[str]= None
    is_published: Optional[str]= None
    

class PostResponse(BaseModel):
    id: Optional[int]
    title: str
    user: int
    content: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True
        

class AuthorPostResponse(BaseModel):
    id: Optional[int]
    title: str
    user: int
    content: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    is_published: bool

    class Config:
        orm_mode = True