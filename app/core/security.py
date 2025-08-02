from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def decode_access_token(token: str) -> Optional[str]:
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None

def get_current_user(db: Session, token: str):
    """Get current user from JWT token."""
    # Import locally to avoid circular imports
    from app.crud.user import user as user_crud
    from app.core.exceptions import AuthenticationError

    user_id = decode_access_token(token)
    if user_id is None:
        raise AuthenticationError()

    user = user_crud.get(db, id=user_id)
    if user is None:
        raise AuthenticationError()

    if not user_crud.is_active(user):
        raise AuthenticationError("Inactive user")

    return user

def get_current_active_admin(user) -> Any:
    """Ensure current user is an admin."""
    # Import locally to avoid circular imports
    from app.crud.user import user as user_crud
    from app.core.exceptions import PermissionError

    if not user_crud.is_admin(user):
        raise PermissionError("Not enough permissions")
    return user
