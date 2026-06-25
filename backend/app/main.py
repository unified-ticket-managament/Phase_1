# main.py

from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Ticket Management Backend Running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }