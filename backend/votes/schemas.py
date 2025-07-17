from pydantic import BaseModel
from datetime import datetime

class VoteOut(BaseModel):
    id: int
    user_id: int
    feature_id: int
    created_at: datetime

    class Config:
        orm_mode = True 