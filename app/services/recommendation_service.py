from sklearn.cluster import KMeans
import numpy as np
from sqlalchemy.orm import Session
from ..models.models import User, Movie, Preference
from ..schemas.schemas import RecommendationResponse
from ..config import settings
from typing import List

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.kmeans = KMeans(
            n_clusters=settings.KMEANS_CLUSTERS, 
            random_state=settings.KMEANS_RANDOM_STATE
        )
        self.user_vectors = None
        self.user_clusters = None

    def _create_user_vectors(self):
        users = self.db.query(User).all()
        genres = self._get_all_genres()
        
        user_vectors = []
        for user in users:
            vector = np.zeros(len(genres))
            preferences = self.db.query(Preference).filter(Preference.user_id == user.id).all()
            
            for pref in preferences:
                if pref.genre in genres:
                    idx = genres.index(pref.genre)
                    vector[idx] = pref.rating
            
            user_vectors.append(vector)
        
        self.user_vectors = np.array(user_vectors)
        return self.user_vectors

    def _get_all_genres(self) -> List[str]:
        movies = self.db.query(Movie).all()
        genres = set()
        for movie in movies:
            genres.add(movie.genre)
        return list(genres)

    def train_model(self):
        if self.user_vectors is None:
            self._create_user_vectors()
        
        self.kmeans.fit(self.user_vectors)
        self.user_clusters = self.kmeans.labels_
        return self.user_clusters

    def get_recommendations(self, user_id: int, limit: int = 10) -> List[RecommendationResponse]:
        if self.user_clusters is None:
            self.train_model()
        
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        user_idx = user.id - 1
        if user_idx >= len(self.user_clusters):
            return []
        
        user_cluster = self.user_clusters[user_idx]
        
        cluster_users = [
            u.id for u, c in zip(self.db.query(User).all(), self.user_clusters) 
            if c == user_cluster
        ]
        
        watched_movie_ids = {movie.id for movie in user.watched_movies}
        recommended_movies = []
        seen_movie_ids = set()
        
        for cluster_user_id in cluster_users:
            if cluster_user_id == user_id:
                continue
            
            cluster_user = self.db.query(User).filter(User.id == cluster_user_id).first()
            if not cluster_user:
                continue
            
            for movie in cluster_user.watched_movies:
                if movie.id not in watched_movie_ids and movie.id not in seen_movie_ids:
                    recommended_movies.append(movie)
                    seen_movie_ids.add(movie.id)
        
        recommended_movies.sort(key=lambda x: x.imdb_rating, reverse=True)
        
        recommendations = []
        for movie in recommended_movies[:limit]:
            recommendations.append(RecommendationResponse(
                movie_id=movie.id,
                movie_name=movie.name,
                genre=movie.genre,
                year=movie.year,
                imdb_rating=movie.imdb_rating,
                similarity_score=movie.imdb_rating
            ))
        
        return recommendations 