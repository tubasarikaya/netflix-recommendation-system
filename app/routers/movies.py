from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import Movie
from ..schemas.schemas import MovieCreate, Movie as MovieSchema, WatchCreate
from ..services.movie_service import MovieService
from ..services.watch_service import WatchService

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

@router.post("/", response_model=MovieSchema)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    return movie_service.create_movie(movie)

@router.get("/", response_model=List[MovieSchema])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    return movie_service.get_movies(skip, limit)

@router.get("/{movie_id}", response_model=MovieSchema)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    movie = movie_service.get_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.post("/watch/save")
def save_watching(watch: WatchCreate, db: Session = Depends(get_db)):
    watch_service = WatchService(db)
    result = watch_service.save_watch(watch)
    
    if not result:
        raise HTTPException(status_code=404, detail="User or movie not found")
    
    return result 