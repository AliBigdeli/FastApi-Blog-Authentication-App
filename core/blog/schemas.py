from pydantic import BaseModel
from typing import List, Optional

class PostSchema(BaseModel):
    title : str
    content : str
    
class PostUpdateSchema(BaseModel):
    title : Optional[str]= None
    content : Optional[str]= None
    user : int