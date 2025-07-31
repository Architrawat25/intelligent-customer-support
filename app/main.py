# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.db.session import get_db
from app.db.init_db import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/openapi.json"
)

@app.on_event("startup")
def on_startup() -> None:
    db = next(get_db())
    init_db(db)

@app.get("/")
async def root():
    return {"message": "ICS API up", "version": settings.VERSION}
