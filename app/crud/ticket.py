from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timezone

from app.crud.base import CRUDBase
from app.db.models.ticket import Ticket, TicketStatus, TicketPriority
from app.schemas.ticket import TicketCreate, TicketUpdate

class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    def get_by_user(
            self,
            db: Session,
            *,
            user_id: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[Ticket]:
        return (
            db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .order_by(desc(Ticket.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
            self,
            db: Session,
            *,
            status: TicketStatus,
            skip: int = 0,
            limit: int = 100
    ) -> List[Ticket]:
        return (
            db.query(Ticket)
            .filter(Ticket.status == status)
            .order_by(desc(Ticket.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
            self,
            db: Session,
            *,
            query: str,
            user_id: Optional[str] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Ticket]:
        base_query = db.query(Ticket).filter(
            or_(
                Ticket.subject.ilike(f"%{query}%"),
                Ticket.question.ilike(f"%{query}%"),
                Ticket.answer.ilike(f"%{query}%")
            )
        )

        if user_id:
            base_query = base_query.filter(Ticket.user_id == user_id)

        return (
            base_query
            .order_by(desc(Ticket.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def mark_resolved(self, db: Session, *, ticket_id: str) -> Optional[Ticket]:
        ticket_obj = self.get(db, id=ticket_id)
        if ticket_obj:
            ticket_obj.status = TicketStatus.RESOLVED
            ticket_obj.resolved_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(ticket_obj)
        return ticket_obj

ticket = CRUDTicket(Ticket)
