from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.repositories import UserRepository
from src.models import User
from src.Modules.Auth.types import UserCreate
from src.core.security import hash_password, verify_password, create_access_token
from typing import Dict, Any

class AuthService:
    """
    Implements authentication business logic workflows, keeping routers thin.
    """
    
    @staticmethod
    def register_user(db: Session, payload: UserCreate) -> User:
        """
        Registers a new user after verifying that the email is unique.
        Hashes the password prior to repository insertion.
        """
        existing_user = UserRepository.get_by_email(db, payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email address already registered."
            )
        
        hashed = hash_password(payload.password)
        db_user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hashed,
            role=payload.role
        )
        return UserRepository.create(db, db_user)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticates a user, verifies credentials, and issues a JWT token.
        """
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Build token payload (access token has sub = user_id and custom claim role)
        token_data = {
            "sub": str(user.id),
            "role": user.role.value
        }
        token = create_access_token(data=token_data)
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role.value,
            "name": user.name,
            "email": user.email
        }
