# app/db/init_db.py
from sqlalchemy.orm import Session
from app.db.base import Base, engine
from app.schemas.user import UserCreate
from app.schemas.faq  import FAQCreate
from app.crud.user import user as user_crud
from app.crud.faq  import faq as faq_crud

def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)

    # bootstrap admin
    if not user_crud.get_by_email(db, email="admin@example.com"):
        admin = UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="System Admin",
            is_admin=True
        )
        user_crud.create(db=db, obj_in=admin)

    # seed FAQs
    seed = [
        {"question": "Reset password?", "answer": "Click *Forgot password*…", "category": "account"},
        {"question": "Business hours?", "answer": "Mon–Fri 09:00–18:00 EST", "category": "general"},
    ]
    for row in seed:
        if not faq_crud.search(db, query=row["question"], limit=1):
            faq_crud.create(db=db, obj_in=FAQCreate(**row))
