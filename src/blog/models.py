from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base
# from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    def json(self):
        return jsonable_encoder(self)

