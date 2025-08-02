from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_optional_current_user
from app.crud.faq import faq as faq_crud
from app.schemas.faq import FAQ, FAQCreate, FAQUpdate
from app.db.models.user import User

router = APIRouter()

@router.get("/", response_model=List[FAQ])
async def get_faqs(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        category: Optional[str] = Query(None),
        search: Optional[str] = Query(None),
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get FAQs with optional filtering. Public endpoint.

    - **category**: Filter by category
    - **search**: Search in questions, answers, and keywords
    """
    if search:
        faqs = faq_crud.search(db, query=search, skip=skip, limit=limit)
    elif category:
        faqs = faq_crud.get_by_category(db, category=category, skip=skip, limit=limit)
    else:
        faqs = faq_crud.get_active(db, skip=skip, limit=limit)

    # Increment view counts if user is authenticated
    if current_user:
        for faq in faqs:
            faq_crud.increment_view_count(db, faq_id=faq.id)

    return faqs

@router.get("/{faq_id}", response_model=FAQ)
async def get_faq(
        faq_id: str,
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Get a specific FAQ by ID.
    """
    faq = faq_crud.get(db, id=faq_id)
    if not faq or not faq.is_active:
        raise HTTPException(status_code=404, detail="FAQ not found")

    # Increment view count if user is authenticated
    if current_user:
        faq_crud.increment_view_count(db, faq_id=faq.id)

    return faq
