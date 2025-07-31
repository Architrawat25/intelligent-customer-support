from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.crud.base import CRUDBase
from app.db.models.faq import FAQ
from app.schemas.faq import FAQCreate, FAQUpdate

class CRUDFAQ(CRUDBase[FAQ, FAQCreate, FAQUpdate]):
    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[FAQ]:
        return (
            db.query(FAQ)
            .filter(FAQ.is_active == True)
            .order_by(desc(FAQ.helpfulness_score), desc(FAQ.view_count))
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
    ) -> List[FAQ]:
        return (
            db.query(FAQ)
            .filter(
                and_(FAQ.category == category, FAQ.is_active == True)
            )
            .order_by(desc(FAQ.helpfulness_score))
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
    ) -> List[FAQ]:
        return (
            db.query(FAQ)
            .filter(
                and_(
                    or_(
                        FAQ.question.ilike(f"%{query}%"),
                        FAQ.answer.ilike(f"%{query}%"),
                        FAQ.keywords.ilike(f"%{query}%")
                    ),
                    FAQ.is_active == True
                )
            )
            .order_by(desc(FAQ.helpfulness_score))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def increment_view_count(self, db: Session, *, faq_id: str) -> Optional[FAQ]:
        faq_obj = self.get(db, id=faq_id)
        if faq_obj:
            faq_obj.view_count += 1
            db.commit()
            db.refresh(faq_obj)
        return faq_obj

faq = CRUDFAQ(FAQ)
