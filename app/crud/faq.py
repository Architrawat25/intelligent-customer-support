from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.crud.base import CRUDBase

class CRUDFAQ(CRUDBase):
    def __init__(self):
        # Import models locally to avoid circular imports
        from app.db.models.faq import FAQ
        super().__init__(FAQ)
        self.FAQ = FAQ

    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List:
        """Get active FAQs."""
        return (
            db.query(self.FAQ)
            .filter(self.FAQ.is_active == True)
            .order_by(desc(self.FAQ.helpfulness_score), desc(self.FAQ.view_count))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_category(
            self,
            db: Session,
            *,
            category: str,
            skip: int = 0,
            limit: int = 100
    ) -> List:
        """Get FAQs by category."""
        return (
            db.query(self.FAQ)
            .filter(
                and_(self.FAQ.category == category, self.FAQ.is_active == True)
            )
            .order_by(desc(self.FAQ.helpfulness_score))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
            self,
            db: Session,
            *,
            query: str,
            skip: int = 0,
            limit: int = 100
    ) -> List:
        """Search FAQs by question, answer, or keywords."""
        return (
            db.query(self.FAQ)
            .filter(
                and_(
                    or_(
                        self.FAQ.question.ilike(f"%{query}%"),
                        self.FAQ.answer.ilike(f"%{query}%"),
                        self.FAQ.keywords.ilike(f"%{query}%")
                    ),
                    self.FAQ.is_active == True
                )
            )
            .order_by(desc(self.FAQ.helpfulness_score))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def increment_view_count(self, db: Session, *, faq_id: str) -> Optional:
        """Increment view count for analytics."""
        faq_obj = self.get(db, id=faq_id)
        if faq_obj:
            faq_obj.view_count += 1
            db.commit()
            db.refresh(faq_obj)
        return faq_obj

    def update_helpfulness_score(
            self,
            db: Session,
            *,
            faq_id: str,
            score: float
    ) -> Optional:
        """Update helpfulness score based on user feedback."""
        faq_obj = self.get(db, id=faq_id)
        if faq_obj:
            # Simple average - in production, you might want a more sophisticated algorithm
            faq_obj.helpfulness_score = score
            db.commit()
            db.refresh(faq_obj)
        return faq_obj

# Create instance
faq = CRUDFAQ()
