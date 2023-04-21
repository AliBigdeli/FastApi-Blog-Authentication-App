from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder

class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer,ForeignKey('users.id'))
    title = Column(String)
    content = Column(String)
    
    users = relationship("UserModel",back_populates='posts')

    def json(self):
        return jsonable_encoder(self)

