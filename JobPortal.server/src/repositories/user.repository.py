from sqlalchemy.orm import Session
from uuid import UUID
from src.models import User
from typing import Optional

class UserRepository:
    """
    Handles all raw database interactions for the User model.
Decouples raw SQL/ORM query mechanisms from business services.
    """
    
    @staticmethod
    def get_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """
        Retrieves a user by their UUID primary key.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """
        Retrieves a user by their unique email address.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user: User) -> User:
        """
        Saves a new user instance to the database.
        """
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
