from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    # user_id = Column(Integer, ForeignKey('users.id'))

    # creator = relationship("User", back_populates="blogs")

