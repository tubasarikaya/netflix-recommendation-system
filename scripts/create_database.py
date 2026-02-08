from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, Movie, Preference
from app.utils.constants import GENRES, GENDERS, MIN_AGE, MAX_AGE, MIN_YEAR, MAX_YEAR, MIN_IMDB_RATING, MAX_IMDB_RATING, MIN_RATING, MAX_RATING
from faker import Faker
import random
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:your_password@localhost:5432/NetflixRecommendation")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
fake = Faker()

def generate_movies(count: int = 100):
    movies = []
    for _ in range(count):
        year = random.randint(MIN_YEAR, MAX_YEAR)
        rating = round(random.uniform(MIN_IMDB_RATING, MAX_IMDB_RATING), 1)
        genre = random.choice(GENRES)
        movie = Movie(
            name=fake.unique.catch_phrase(),
            genre=genre,
            year=year,
            imdb_rating=rating
        )
        movies.append(movie)
    return movies

def generate_users(count: int = 1000):
    users = []
    for _ in range(count):
        age = random.randint(MIN_AGE, MAX_AGE)
        gender = random.choice(GENDERS)
        user = User(
            name=fake.name(),
            email=fake.unique.email(),
            age=age,
            gender=gender
        )
        users.append(user)
    return users

def generate_preferences(user_count: int):
    preferences = []
    for user_id in range(1, user_count + 1):
        num_preferences = random.randint(3, 5)
        user_genres = random.sample(GENRES, num_preferences)
        for genre in user_genres:
            preference = Preference(
                user_id=user_id,
                genre=genre,
                rating=round(random.uniform(MIN_RATING, MAX_RATING), 1)
            )
            preferences.append(preference)
    return preferences

def assign_watched_movies(users, movies):
    for user in users:
        num_movies = random.randint(10, 20)
        watched_movies = random.sample(movies, num_movies)
        user.watched_movies.extend(watched_movies)

def main():
    try:
        print("Generating movies...")
        movies = generate_movies(100)
        for movie in movies:
            db.add(movie)
        db.commit()
        print(f"Added {len(movies)} movies")

        print("Generating users...")
        users = generate_users(1000)
        for user in users:
            db.add(user)
        db.commit()
        print(f"Added {len(users)} users")

        print("Generating preferences...")
        preferences = generate_preferences(1000)
        for preference in preferences:
            db.add(preference)
        db.commit()
        print(f"Added {len(preferences)} preferences")

        print("Assigning watched movies...")
        assign_watched_movies(users, movies)
        db.commit()
        print("Assigned watched movies to users")

        print("\nDatabase setup completed successfully!")
        print(f"Total users: {len(users)}")
        print(f"Total movies: {len(movies)}")
        print(f"Total preferences: {len(preferences)}")
        print("Average movies watched per user: 15")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
