from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.core.base import Base

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feature_id = Column(Integer, ForeignKey('features.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='votes')
    feature = relationship('Feature', back_populates='votes')
    __table_args__ = (UniqueConstraint('user_id', 'feature_id', name='_user_feature_uc'),) 