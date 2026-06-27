"""FastAPI application for InsightForge AI backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import sys

# Ensure root dir is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import init_db
from backend.config import settings
from backend.api.health import router as health_router
from backend.api.documents import router as documents_router
from backend.api.analysis import router as analysis_router
from backend.api.recommendations import router as recommendations_router
from backend.api.memory import router as memory_router

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("InsightForge AI Backend starting...")
    # Create data directories
    for d in ['data/db', 'data/faiss', 'data/uploads']:
        os.makedirs(d, exist_ok=True)
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("InsightForge AI Backend shutting down")

app = FastAPI(
    title="InsightForge AI",
    description="Agentic Next Best Action Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount endpoints
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(documents_router, prefix="/api", tags=["Documents"])
app.include_router(analysis_router, prefix="/api", tags=["Analysis"])
app.include_router(recommendations_router, prefix="/api", tags=["Recommendations"])
app.include_router(memory_router, prefix="/api", tags=["Memory"])
