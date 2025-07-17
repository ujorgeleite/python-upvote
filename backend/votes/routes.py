from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.votes import schemas as vote_schemas, models as vote_models
from backend.features.models import Feature
from backend.users.models import User
from backend.core.deps import get_db
from backend.auth.deps import get_current_user

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("/upvote/{feature_id}", response_model=vote_schemas.VoteOut)
def upvote_feature(feature_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    feature = db.query(Feature).filter(Feature.id == feature_id).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    if db.query(vote_models.Vote).filter(vote_models.Vote.user_id == current_user.id, vote_models.Vote.feature_id == feature_id).first():
        raise HTTPException(status_code=400, detail="Already voted for this feature")
    vote = vote_models.Vote(user_id=current_user.id, feature_id=feature_id)
    db.add(vote)
    db.commit()
    db.refresh(vote)
    return vote 