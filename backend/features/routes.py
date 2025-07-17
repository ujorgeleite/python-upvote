from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.features import schemas as feature_schemas, models as feature_models
from backend.votes import models as vote_models
from backend.core.deps import get_db
from backend.users.models import User
from sqlalchemy import func
from backend.auth.deps import get_current_user

router = APIRouter(prefix="/features", tags=["features"])

@router.post("/", response_model=feature_schemas.FeatureOut)
def create_feature(feature: feature_schemas.FeatureCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_feature = feature_models.Feature(title=feature.title, description=feature.description, user_id=current_user.id)
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return feature_schemas.FeatureOut(
        id=db_feature.id,
        title=db_feature.title,
        description=db_feature.description,
        user_id=db_feature.user_id,
        created_at=db_feature.created_at,
        votes=0
    )

@router.get("/", response_model=List[feature_schemas.FeatureOut])
def list_features(db: Session = Depends(get_db)):
    features = db.query(feature_models.Feature).all()
    vote_counts = dict(db.query(vote_models.Vote.feature_id, func.count(vote_models.Vote.id)).group_by(vote_models.Vote.feature_id).all())
    return [
        feature_schemas.FeatureOut(
            id=f.id,
            title=f.title,
            description=f.description,
            user_id=f.user_id,
            created_at=f.created_at,
            votes=vote_counts.get(f.id, 0)
        ) for f in features
    ] 