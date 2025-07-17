from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class FeatureCreate(BaseModel):
    title: str
    description: str

class FeatureOut(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    created_at: datetime
    votes: int

    class Config:
        orm_mode = True

class VoteOut(BaseModel):
    id: int
    user_id: int
    feature_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 