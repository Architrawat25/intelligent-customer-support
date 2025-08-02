from sqlalchemy.orm import Session
from app.db.base import Base, engine

def init_db(db: Session) -> None:
    """Initialize database with default data."""

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Import CRUD modules locally to avoid circular imports
    from app.crud.user import user as user_crud
    from app.crud.faq import faq as faq_crud
    from app.schemas.user import UserCreate
    from app.schemas.faq import FAQCreate

    # Create default admin user
    admin_user = user_crud.get_by_email(db, email="admin@example.com")
    if not admin_user:
        admin_user_in = UserCreate(
            email="admin@example.com",
            password="admin123",
            full_name="System Administrator",
            is_admin=True
        )
        admin_user = user_crud.create(db, obj_in=admin_user_in)
        print(f"Created admin user: {admin_user.email}")

    # Create sample FAQs
    sample_faqs = [
        {
            "question": "How do I reset my password?",
            "answer": "You can reset your password by clicking the 'Forgot Password' link on the login page and following the instructions sent to your email.",
            "category": "account",
            "keywords": "password, reset, forgot, login, account"
        },
        {
            "question": "How do I contact customer support?",
            "answer": "You can contact customer support by creating a ticket through this system, emailing support@company.com, or calling 1-800-SUPPORT.",
            "category": "support",
            "keywords": "contact, support, help, ticket, email, phone"
        },
        {
            "question": "What are your business hours?",
            "answer": "Our business hours are Monday through Friday, 9 AM to 6 PM EST. Support tickets are monitored 24/7.",
            "category": "general",
            "keywords": "hours, time, business, support, availability"
        },
        {
            "question": "How do I cancel my subscription?",
            "answer": "To cancel your subscription, go to your account settings, select 'Billing', and click 'Cancel Subscription'. You can also contact support for assistance.",
            "category": "billing",
            "keywords": "cancel, subscription, billing, account, refund"
        }
    ]

    for faq_data in sample_faqs:
        existing = faq_crud.search(db, query=faq_data["question"], limit=1)
        if not existing:
            faq_in = FAQCreate(**faq_data)
            faq_crud.create(db, obj_in=faq_in)
            print(f"Created FAQ: {faq_data['question'][:50]}...")

if __name__ == "__main__":
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        init_db(db)
        print("Database initialized successfully!")
    finally:
        db.close()
