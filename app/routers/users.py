from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.models import User
from ..schemas.schemas import UserCreate, User as UserSchema
from ..services.user_service import UserService
from ..utils.validators import validate_limit, validate_skip

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user)

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    skip = validate_skip(skip)
    limit = validate_limit(limit)
    user_service = UserService(db)
    return user_service.get_users(skip, limit) 