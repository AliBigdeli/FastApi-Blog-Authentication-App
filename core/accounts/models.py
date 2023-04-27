import datetime
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from core.database import Base
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True,index=True)
    password = Column(String)
    created_date = Column(DateTime,default=datetime.datetime.utcnow())
    updated_date = Column(DateTime)
    
    posts = relationship("PostModel",back_populates='users')
    
    def json(self):
        return jsonable_encoder(self)
    
    

    