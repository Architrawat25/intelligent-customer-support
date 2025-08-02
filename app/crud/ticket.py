from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timezone

from app.crud.base import CRUDBase

class CRUDTicket(CRUDBase):
    def __init__(self):
        # Import models locally to avoid circular imports
        from app.db.models.ticket import Ticket, TicketStatus, TicketPriority
        super().__init__(Ticket)
        self.Ticket = Ticket
        self.TicketStatus = TicketStatus
        self.TicketPriority = TicketPriority

    def get_by_user(
            self,
            db: Session,
            *,
            user_id: str,
            skip: int = 0,
            limit: int = 100
    ) -> List:
        """Get tickets for a specific user."""
        return (
            db.query(self.Ticket)
            .filter(self.Ticket.user_id == user_id)
            .order_by(desc(self.Ticket.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
            self,
            db: Session,
            *,
            status,
            skip: int = 0,
            limit: int = 100
    ) -> List:
        """Get tickets by status."""
        return (
            db.query(self.Ticket)
            .filter(self.Ticket.status == status)
            .order_by(desc(self.Ticket.created_at))
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
    ) -> List:
        """Search tickets by subject or question content."""
        base_query = db.query(self.Ticket).filter(
            or_(
                self.Ticket.subject.ilike(f"%{query}%"),
                self.Ticket.question.ilike(f"%{query}%"),
                self.Ticket.answer.ilike(f"%{query}%")
            )
        )

        if user_id:
            base_query = base_query.filter(self.Ticket.user_id == user_id)

        return (
            base_query
            .order_by(desc(self.Ticket.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def mark_resolved(self, db: Session, *, ticket_id: str) -> Optional:
        """Mark ticket as resolved."""
        ticket_obj = self.get(db, id=ticket_id)
        if ticket_obj:
            ticket_obj.status = self.TicketStatus.RESOLVED
            ticket_obj.resolved_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(ticket_obj)
        return ticket_obj

    def count_by_status(self, db: Session) -> dict:
        """Get count of tickets by status."""
        from sqlalchemy import func

        result = (
            db.query(self.Ticket.status, func.count(self.Ticket.id))
            .group_by(self.Ticket.status)
            .all()
        )

        return {status.value: count for status, count in result}

# Create instance
ticket = CRUDTicket()
