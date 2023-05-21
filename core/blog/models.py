from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from core.database import Base
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_published = Column(Boolean, default=False)

    users = relationship("UserModel", back_populates="posts")
