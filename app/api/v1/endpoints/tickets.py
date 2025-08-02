from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user_dependency
from app.services.ticket_service import TicketService
from app.crud.ticket import ticket as ticket_crud
from app.schemas.ask import AskQuestion, AskResponse
from app.schemas.ticket import Ticket, TicketUpdate
from app.db.models.user import User
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.post("/ask", response_model=AskResponse, status_code=status.HTTP_201_CREATED)
async def ask_question(
        question: AskQuestion,
        current_user: User = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Submit a question and get an automated response or create a support ticket.

    - **subject**: Brief subject line for the question
    - **question**: Detailed question description
    - **category**: Question category (optional)
    - **priority**: Priority level (optional)
    """
    ticket_service = TicketService(db)
    return ticket_service.process_question(current_user.id, question)

@router.get("/", response_model=List[Ticket])
async def get_user_tickets(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        status: Optional[str] = Query(None),
        current_user: User = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Get current user's tickets with optional filtering.
    """
    if status:
        from app.db.models.ticket import TicketStatus
        if hasattr(TicketStatus, status.upper()):
            ticket_status = getattr(TicketStatus, status.upper())
            tickets = ticket_crud.get_by_status(db, status=ticket_status, skip=skip, limit=limit)
            # Filter by user
            tickets = [t for t in tickets if t.user_id == current_user.id]
        else:
            raise HTTPException(status_code=400, detail="Invalid status")
    else:
        tickets = ticket_crud.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)

    return tickets

@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket(
        ticket_id: str,
        current_user: User = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Get a specific ticket by ID.
    """
    ticket = ticket_crud.get(db, id=ticket_id)
    if not ticket:
        raise NotFoundError("Ticket not found")

    # Ensure user can only access their own tickets
    if ticket.user_id != current_user.id:
        raise PermissionError("Access denied")

    return ticket

@router.put("/{ticket_id}", response_model=Ticket)
async def update_ticket(
        ticket_id: str,
        ticket_update: TicketUpdate,
        current_user: User = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Update a ticket (limited fields for users).
    """
    ticket = ticket_crud.get(db, id=ticket_id)
    if not ticket:
        raise NotFoundError("Ticket not found")

    if ticket.user_id != current_user.id:
        raise PermissionError("Access denied")

    # Users can only update certain fields
    allowed_updates = {
        "subject": ticket_update.subject,
        "question": ticket_update.question
    }
    allowed_updates = {k: v for k, v in allowed_updates.items() if v is not None}

    updated_ticket = ticket_crud.update(db, db_obj=ticket, obj_in=allowed_updates)
    return updated_ticket
