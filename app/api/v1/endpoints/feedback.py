from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4

from app.api.deps import get_db, get_current_user_dependency
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.crud.faq import faq as faq_crud
from app.crud.ticket import ticket as ticket_crud
from app.db.models.user import User

router = APIRouter()

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
        feedback: FeedbackCreate,
        current_user: User = Depends(get_current_user_dependency),
        db: Session = Depends(get_db)
):
    """
    Submit feedback, rating, or report.

    - **type**: Type of feedback
    - **rating**: Rating (1-5 stars, optional)
    - **comment**: Text feedback (optional)
    - **ticket_id**: Related ticket ID (optional)
    - **faq_id**: Related FAQ ID (optional)
    """

    # Validate related resources
    if feedback.ticket_id:
        ticket = ticket_crud.get(db, id=feedback.ticket_id)
        if not ticket or ticket.user_id != current_user.id:
            raise HTTPException(status_code=400, detail="Invalid ticket ID")

    if feedback.faq_id:
        faq = faq_crud.get(db, id=feedback.faq_id)
        if not faq:
            raise HTTPException(status_code=400, detail="Invalid FAQ ID")

        # Update FAQ helpfulness score if rating provided
        if feedback.rating:
            # Simple averaging - in production, use more sophisticated scoring
            new_score = (faq.helpfulness_score + feedback.rating * 20) / 2
            faq_crud.update_helpfulness_score(db, faq_id=faq.id, score=new_score)

    # In a real application, you'd save this to a feedback table
    # For now, we'll just acknowledge receipt

    feedback_id = str(uuid4())
    return FeedbackResponse(
        id=feedback_id,
        message="Thank you for your feedback! We appreciate your input."
    )
