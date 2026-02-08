from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, movies, recommendations
from .database import engine
from .models import models
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(movies.router)
app.include_router(recommendations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Netflix Recommendation System API!"} 