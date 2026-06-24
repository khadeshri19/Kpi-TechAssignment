from sqlalchemy.orm import Session
from src.Modules.Auth.types import UserCreate, LoginPayload
from src.Modules.Auth.service import AuthService

class AuthController:
    @staticmethod
    def register(payload: UserCreate, db: Session):
        return AuthService.register_user(db, payload)

    @staticmethod
    def login(payload: LoginPayload, db: Session):
        return AuthService.authenticate_user(db, payload.email, payload.password)
