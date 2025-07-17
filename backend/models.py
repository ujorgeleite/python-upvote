from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    features = relationship('Feature', back_populates='author')
    votes = relationship('Vote', back_populates='user')

class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author = relationship('User', back_populates='features')
    votes = relationship('Vote', back_populates='feature')

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='votes')
    feature = relationship('Feature', back_populates='votes')
    __table_args__ = (UniqueConstraint('user_id', 'feature_id', name='_user_feature_uc'),) 