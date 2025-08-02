from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user, get_current_active_admin, oauth2_scheme
from app.db.session import get_db
from app.db.models.user import User

def get_current_user_dependency(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    """Dependency to get current authenticated user."""
    return get_current_user(db=db, token=token)

def get_current_admin_user(
        current_user: User = Depends(get_current_user_dependency)
) -> User:
    """Dependency to get current admin user."""
    return get_current_active_admin(current_user)

def get_optional_current_user(
        db: Session = Depends(get_db),
        token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """Dependency to optionally get current user (for public endpoints)."""
    if token is None:
        return None
    try:
        return get_current_user(db=db, token=token)
    except HTTPException:
        return None
