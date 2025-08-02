from app.ai.semantic_search_service import get_search_service

class TicketService:
    def __init__(self, db: Session):
        self.db = db
        self.search_service = get_search_service()

    async def process_question(self, user_id: str, question_data: AskQuestion) -> AskResponse:
        """Process user question with AI enhancement"""

        try:
            # Try AI-powered processing first
            if self.search_service.is_available():
                ai_result = self.search_service.get_best_answer(
                    question_data.question,
                    confidence_threshold=0.7
                )

                confidence = ai_result['confidence']
                answer = ai_result['answer']
                source = ai_result['source']

                # Create ticket based on AI result
                ticket = self._create_ticket(
                    user_id=user_id,
                    question_data=question_data,
                    answer=answer,
                    confidence=confidence
                )

                return AskResponse(
                    ticket_id=ticket.id,
                    answer=answer,
                    confidence_score=confidence,
                    source='ai_enhanced',
                    created_at=datetime.now(timezone.utc).isoformat(),
                    metadata={
                        'ai_source': source,
                        'needs_human_support': ai_result.get('needs_human_support', False),
                        'category': ai_result.get('category'),
                        'faq_id': ai_result.get('faq_id')
                    }
                )
            else:
                # Fallback to basic processing
                return self._fallback_process_question(user_id, question_data)

        except Exception as e:
            logger.error(f"Error in AI processing: {e}")
            return self._fallback_process_question(user_id, question_data)

    def _create_ticket(self, user_id: str, question_data: AskQuestion, answer: str, confidence: float):
        """Create ticket with AI-generated response"""
        from app.db.models.ticket import TicketPriority, TicketStatus

        # Determine status and priority based on confidence
        if confidence >= 0.8:
            status = TicketStatus.RESOLVED
            priority = TicketPriority.LOW
        elif confidence >= 0.5:
            status = TicketStatus.OPEN
            priority = TicketPriority.MEDIUM
        else:
            status = TicketStatus.OPEN
            priority = TicketPriority.HIGH

        ticket_data = TicketCreate(
            user_id=user_id,
            subject=question_data.subject,
            question=question_data.question,
            answer=answer,
            status=status,
            priority=priority,
            confidence_score=confidence
        )

        ticket = ticket_crud.create(self.db, obj_in=ticket_data)

        if status == TicketStatus.RESOLVED:
            ticket_crud.mark_resolved(self.db, ticket_id=ticket.id)

        return ticket
