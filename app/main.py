from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Customer Support System API",
    openapi_url="/openapi.json"
)

# Add CORS middleware for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://customer-ai007.netlify.app",  # Your specific Netlify URL
        # Add your Railway backend URL here after deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event - Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        from app.db.session import get_db
        from app.db.init_db import init_db
        
        db = next(get_db())
        try:
            init_db(db)
            print("✅ Database initialized successfully")
        finally:
            db.close()
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        # Don't crash the app, just log the error

@app.get("/")
async def root():
    return {
        "message": "ICS API up",
        "version": settings.VERSION,
        "environment": "production" if not settings.DEBUG else "development"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "cors_enabled": True,
        "port": os.environ.get("PORT", "8000")
    }

# Include API routes
try:
    from app.api.v1.api import api_router
    app.include_router(api_router, prefix="/api/v1")
    print("✅ API routes loaded successfully")
except Exception as e:
    print(f"❌ Error loading API routes: {e}")
    # Create a basic fallback route
    @app.get("/api/v1/test")
    async def test_route():
        return {"message": "Basic API working, but full routes failed to load"}

# For Railway deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )
