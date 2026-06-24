from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.Modules.Auth.types import UserCreate, UserResponse, LoginPayload, TokenResponse
from src.Modules.Auth.controller import AuthController

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new admin or candidate user record.
    """
    return AuthController.register(payload, db)

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    """
    Authenticates user credentials and issues a JWT token.
    """
    return AuthController.login(payload, db)
