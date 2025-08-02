from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Customer Support System API",
    openapi_url="/openapi.json"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    # Import locally to avoid circular imports at startup
    from app.db.session import get_db
    from app.db.init_db import init_db

    db = next(get_db())
    try:
        init_db(db)
    finally:
        db.close()

@app.get("/")
async def root():
    return {
        "message": "ICS API up",
        "version": settings.VERSION
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
