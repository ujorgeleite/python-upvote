from fastapi import FastAPI
from backend.core.database import engine
from backend.core.base import Base
from backend.users.routes import router as users_router
from backend.features.routes import router as features_router
from backend.votes.routes import router as votes_router
from backend.auth.routes import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(features_router)
app.include_router(votes_router)
app.include_router(auth_router) 