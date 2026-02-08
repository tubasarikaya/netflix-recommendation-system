from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.models import Movie
from ..schemas.schemas import MovieCreate, Movie as MovieSchema

class MovieService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.db.query(Movie).filter(Movie.id == movie_id).first()
    
    def get_movies(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        return self.db.query(Movie).offset(skip).limit(limit).all()
    
    def create_movie(self, movie: MovieCreate) -> Movie:
        db_movie = Movie(**movie.dict())
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie
    
    def get_movies_by_genre(self, genre: str) -> List[Movie]:
        return self.db.query(Movie).filter(Movie.genre == genre).all()
    
    def movie_exists(self, movie_id: int) -> bool:
        return self.db.query(Movie).filter(Movie.id == movie_id).first() is not None
    
    def get_all_genres(self) -> List[str]:
        movies = self.db.query(Movie).all()
        genres = set()
        for movie in movies:
            genres.add(movie.genre)
        return list(genres)
