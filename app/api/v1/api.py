from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, tickets, faqs, feedback, admin
from app.core.config import settings

api_router = APIRouter()

# Authentication routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# User routes
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

# Ticket routes
api_router.include_router(
    tickets.router,
    prefix="/tickets",
    tags=["tickets"]
)

# FAQ routes
api_router.include_router(
    faqs.router,
    prefix="/faqs",
    tags=["faqs"]
)

# Feedback routes
api_router.include_router(
    feedback.router,
    prefix="/feedback",
    tags=["feedback"]
)

# Admin routes
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[]  # Admin auth handled in individual endpoints
)
