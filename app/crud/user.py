from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError

from app.crud.base import CRUDBase
from app.core.security import get_password_hash, verify_password

class CRUDUser(CRUDBase):
    def __init__(self):
        # Import User model locally to avoid circular imports
        from app.db.models.user import User
        super().__init__(User)
        self.User = User

    def get_by_email(self, db: Session, *, email: str) -> Optional:
        return db.query(self.User).filter(self.User.email == email).first()

    def create(self, db: Session, *, obj_in) -> Any:
        """Create new user with hashed password."""
        obj_in_data = jsonable_encoder(obj_in)
        # Remove password and add hashed_password
        password = obj_in_data.pop("password", None)
        if password:
            obj_in_data["hashed_password"] = get_password_hash(password)

        db_obj = self.User(**obj_in_data)
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise

    def update(
            self, db: Session, *, db_obj, obj_in: Union[Dict[str, Any], Any]
    ) -> Any:
        """Update user, hashing password if provided."""
        if hasattr(obj_in, 'dict'):
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = obj_in

        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional:
        """Authenticate user with email and password."""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user) -> bool:
        """Check if user is active."""
        return user.is_active

    def is_admin(self, user) -> bool:
        """Check if user is admin."""
        return user.is_admin

# Create instance
user = CRUDUser()
