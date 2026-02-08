from typing import Optional

def validate_age(age: int) -> bool:
    return 18 <= age <= 120

def validate_rating(rating: float) -> bool:
    return 1.0 <= rating <= 5.0

def validate_year(year: int) -> bool:
    return 1900 <= year <= 2030

def validate_imdb_rating(rating: float) -> bool:
    return 0.0 <= rating <= 10.0

def validate_email(email: str) -> bool:
    return "@" in email and "." in email

def validate_limit(limit: int, max_limit: int = 100) -> int:
    if limit <= 0:
        return 10
    return min(limit, max_limit)

def validate_skip(skip: int) -> int:
    return max(0, skip)
