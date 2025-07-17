from pydantic import BaseModel
from datetime import datetime

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