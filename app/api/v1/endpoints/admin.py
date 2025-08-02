from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_admin_user
from app.crud.user import user as user_crud
from app.crud.ticket import ticket as ticket_crud
from app.crud.faq import faq as faq_crud
from app.schemas.user import User
from app.schemas.ticket import Ticket, TicketUpdate
from app.schemas.faq import FAQ, FAQCreate, FAQUpdate
from app.db.models.user import User as UserModel
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/users", response_model=List[User])
async def get_all_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Get all users (admin only).
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users

@router.get("/tickets", response_model=List[Ticket])
async def get_all_tickets(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        status: Optional[str] = Query(None),
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Get all tickets with optional status filtering (admin only).
    """
    if status:
        from app.db.models.ticket import TicketStatus
        if hasattr(TicketStatus, status.upper()):
            ticket_status = getattr(TicketStatus, status.upper())
            tickets = ticket_crud.get_by_status(db, status=ticket_status, skip=skip, limit=limit)
        else:
            raise HTTPException(status_code=400, detail="Invalid status")
    else:
        tickets = ticket_crud.get_multi(db, skip=skip, limit=limit)

    return tickets

@router.put("/tickets/{ticket_id}", response_model=Ticket)
async def admin_update_ticket(
        ticket_id: str,
        ticket_update: TicketUpdate,
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Update any ticket (admin only).
    """
    ticket = ticket_crud.get(db, id=ticket_id)
    if not ticket:
        raise NotFoundError("Ticket not found")

    updated_ticket = ticket_crud.update(db, db_obj=ticket, obj_in=ticket_update)
    return updated_ticket

@router.post("/faqs", response_model=FAQ, status_code=status.HTTP_201_CREATED)
async def admin_create_faq(
        faq_data: FAQCreate,
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Create a new FAQ (admin only).
    """
    faq = faq_crud.create(db, obj_in=faq_data)
    return faq

@router.put("/faqs/{faq_id}", response_model=FAQ)
async def admin_update_faq(
        faq_id: str,
        faq_update: FAQUpdate,
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Update FAQ (admin only).
    """
    faq = faq_crud.get(db, id=faq_id)
    if not faq:
        raise NotFoundError("FAQ not found")

    updated_faq = faq_crud.update(db, db_obj=faq, obj_in=faq_update)
    return updated_faq

@router.delete("/faqs/{faq_id}")
async def admin_delete_faq(
        faq_id: str,
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Delete FAQ (admin only).
    """
    faq = faq_crud.get(db, id=faq_id)
    if not faq:
        raise NotFoundError("FAQ not found")

    faq_crud.remove(db, id=faq_id)
    return {"message": "FAQ deleted successfully"}

@router.get("/analytics")
async def get_analytics(
        current_admin: UserModel = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
):
    """
    Get system analytics (admin only).
    """
    stats = {
        "total_users": user_crud.count(db),
        "total_tickets": ticket_crud.count(db),
        "total_faqs": faq_crud.count(db),
        "ticket_stats": ticket_crud.count_by_status(db),
        "active_users": len([u for u in user_crud.get_multi(db, limit=1000) if u.is_active])
    }
    return stats
