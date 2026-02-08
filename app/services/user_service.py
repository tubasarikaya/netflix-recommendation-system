from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.models import User, Preference
from ..schemas.schemas import UserCreate, User as UserSchema, Preference as PreferenceSchema

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def create_user(self, user: UserCreate) -> User:
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_user_preferences(self, user_id: int) -> List[Preference]:
        return self.db.query(Preference).filter(Preference.user_id == user_id).all()
    
    def get_user_watched_movies(self, user_id: int) -> Optional[User]:
        user = self.get_user(user_id)
        return user if user else None
    
    def user_exists(self, user_id: int) -> bool:
        return self.db.query(User).filter(User.id == user_id).first() is not None
