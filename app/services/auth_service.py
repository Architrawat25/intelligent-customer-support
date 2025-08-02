from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.exceptions import AuthenticationError, ValidationError
from app.crud.user import user as user_crud
from app.schemas.auth import UserRegister, UserLogin, Token, AuthResponse
from app.schemas.user import UserCreate

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserRegister) -> AuthResponse:
        """Register a new user."""
        # Check if user already exists
        existing_user = user_crud.get_by_email(self.db, email=user_data.email)
        if existing_user:
            raise ValidationError("Email already registered")

        # Create user
        user_create = UserCreate(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        user = user_crud.create(self.db, obj_in=user_create)

        # Generate token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )

        token = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        return AuthResponse(
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active
            },
            token=token
        )

    def authenticate_user(self, credentials: UserLogin) -> AuthResponse:
        """Authenticate user and return token."""
        user = user_crud.authenticate(
            self.db, email=credentials.email, password=credentials.password
        )
        if not user:
            raise AuthenticationError("Incorrect email or password")

        if not user_crud.is_active(user):
            raise AuthenticationError("Inactive user")

        # Generate token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )

        token = Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        return AuthResponse(
            user={
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_admin": user.is_admin
            },
            token=token
        )
