from sqlalchemy.orm import Session
from datetime import datetime
from ..models.models import User, Movie
from ..schemas.schemas import WatchCreate

class WatchService:
    def __init__(self, db: Session):
        self.db = db
    
    def save_watch(self, watch: WatchCreate) -> dict:
        user = self.db.query(User).filter(User.id == watch.user_id).first()
        if not user:
            return None
        
        movie = self.db.query(Movie).filter(Movie.id == watch.movie_id).first()
        if not movie:
            return None
        
        if movie not in user.watched_movies:
            user.watched_movies.append(movie)
            self.db.commit()
        
        return {
            "user_id": user.id,
            "movie_id": movie.id,
            "watch_date": datetime.utcnow(),
            "watch_duration": watch.watch_duration
        }
    
    def get_user_watched_movies(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user.watched_movies if user else []
    
    def has_watched(self, user_id: int, movie_id: int) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        return any(movie.id == movie_id for movie in user.watched_movies)
