from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin, AuthResponse

router = APIRouter()

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
        user_data: UserRegister,
        db: Session = Depends(get_db)
):
    """
    Register a new user.

    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    - **full_name**: User's full name
    """
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)

@router.post("/login", response_model=AuthResponse)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    Login user and receive access token.

    - **username**: User's email address
    - **password**: User's password
    """
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    auth_service = AuthService(db)
    return auth_service.authenticate_user(credentials)

@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
        current_user: dict = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Refresh user access token.
    """
    auth_service = AuthService(db)
    credentials = UserLogin(email=current_user.email, password="") # Won't be used
    # In a real app, you'd use a refresh token here
    return auth_service.authenticate_user(credentials)
