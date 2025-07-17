from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

from backend.core.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    features = relationship('Feature', back_populates='author')
    votes = relationship('Vote', back_populates='user') 