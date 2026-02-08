# Movie Recommendation System

## Contributors
Tuba SARIKAYA & Gül ERTEN -- GYK1

## Overview
This is a movie recommendation system built with FastAPI and PostgreSQL. The system suggests movies to users based on their viewing history and preferences using KMeans clustering.

## Features
- User registration and management
- Movie database
- Track user preferences and watch history
- Get personalized movie recommendations
- RESTful API with interactive documentation

## Tech Stack
- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **ML Library:** scikit-learn (KMeans)
- **Data Tools:** Pandas, NumPy
- **Python:** 3.8+

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd netflix_recommendation_system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create PostgreSQL database:
```sql
CREATE DATABASE "NetflixRecommendation";
```

4. Configure database:
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/NetflixRecommendation
```

5. Load sample data:
```bash
python scripts/create_database.py
```
Creates 1000 users, 100 movies, and assigns preferences and watch history to each user.

## Running the App

Start the server:
```bash
uvicorn app.main:app --reload --port 8001
```

Open the API docs:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## API Endpoints

### User Management
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user details
- `POST /users/create` - Create new user

### Movie Management
- `GET /movies/` - List all movies
- `GET /movies/{movie_id}` - Get movie details
- `POST /movies/` - Create new movie
- `POST /movies/watch/save` - Record movie watch event

### Recommendations
- `GET /recommendations/{user_id}` - Get personalized movie recommendations

## Database Schema

### Users
- ID, Name, Email
- Age, Gender
- Watched movies (many-to-many)
- Genre preferences

### Movies
- ID, Name, Genre
- Year, IMDB Rating

### Preferences
- User ID, Genre, Rating

## How It Works
The recommendation system uses KMeans clustering to group users with similar preferences. When you request recommendations for a user, the system:
1. Finds users in the same cluster
2. Gets movies they watched
3. Filters out movies you already saw
4. Returns top-rated unwatched movies