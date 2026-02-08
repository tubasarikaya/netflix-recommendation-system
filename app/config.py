import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:your_password@localhost:5432/NetflixRecommendation"
    )
    API_TITLE: str = "Netflix Recommendation System"
    API_DESCRIPTION: str = "Movie/Series recommendation system based on user viewing preferences"
    API_VERSION: str = "1.0.0"
    KMEANS_CLUSTERS: int = 5
    KMEANS_RANDOM_STATE: int = 42

settings = Settings()
