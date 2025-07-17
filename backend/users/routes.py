from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from backend.users import schemas as user_schemas, models as user_models
from backend.auth import auth_utils
from backend.core.deps import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=user_schemas.UserOut)
def register(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(user_models.User).filter((user_models.User.username == user.username) | (user_models.User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = auth_utils.get_password_hash(user.password)
    db_user = user_models.User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=user_schemas.UserOut)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user 