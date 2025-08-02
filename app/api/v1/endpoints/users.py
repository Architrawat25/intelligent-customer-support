from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_dependency
from app.crud.user import user as user_crud
from app.schemas.user import User, UserUpdate
from app.db.models.user import User as UserModel

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_profile(
        current_user: UserModel = Depends(get_current_user_dependency)
):
    """
    Get current user's profile.
    """
    return current_user

@router.put("/me", response_model=User)
async def update_current_user(
        user_update: UserUpdate,
        current_user: UserModel = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Update current user's profile.
    """
    updated_user = user_crud.update(db, db_obj=current_user, obj_in=user_update)
    return updated_user

@router.get("/me/tickets")
async def get_current_user_tickets(
        skip: int = 0,
        limit: int = 100,
        current_user: UserModel = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Get current user's tickets.
    """
    from app.crud.ticket import ticket as ticket_crud
    tickets = ticket_crud.get_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return tickets
