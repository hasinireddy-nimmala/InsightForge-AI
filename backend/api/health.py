"""Health check endpoint."""
from fastapi import APIRouter
from backend.models.schemas import HealthResponse
from backend.config import settings
import os

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    db_status = "connected" if os.path.exists(settings.DB_PATH) else "initializing"
    vs_status = "ready" if os.path.exists(settings.FAISS_INDEX_PATH) else "empty"
    llm_status = "configured" if settings.GOOGLE_API_KEY else "demo_mode"
    return HealthResponse(status="healthy", database=db_status, vector_store=vs_status, llm=llm_status)
