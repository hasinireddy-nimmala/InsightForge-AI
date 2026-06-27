"""FastAPI endpoints for recommendation memory center."""
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
import logging

from backend.database import get_db
from backend.models.schemas import (
    MemoryEntry, 
    MemoryListResponse, 
    MemoryTrendsResponse,
    MemoryTrend
)
from backend.repositories import memory_repo

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/memory", response_model=MemoryListResponse)
async def get_all_decision_memory(db: aiosqlite.Connection = Depends(get_db)):
    """Retrieve all recommendation memory entries."""
    try:
        entries = await memory_repo.get_all_memory(db)
        resp_entries = []
        for e in entries:
            resp_entries.append(MemoryEntry(
                id=e['id'],
                customer_id=e['customer_id'],
                recommendation=e['recommendation'],
                approved=bool(e['approved']),
                outcome=e['outcome'],
                confidence_delta=e['confidence_delta'],
                timestamp=e['timestamp']
            ))
        return MemoryListResponse(entries=resp_entries, total=len(resp_entries))
    except Exception as e:
        logger.error(f"Error retrieving memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/customer/{customer_id}", response_model=MemoryListResponse)
async def get_customer_decision_memory(customer_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Retrieve memory entries for a specific customer."""
    try:
        entries = await memory_repo.get_customer_memory(db, customer_id)
        resp_entries = []
        for e in entries:
            resp_entries.append(MemoryEntry(
                id=e['id'],
                customer_id=e['customer_id'],
                recommendation=e['recommendation'],
                approved=bool(e['approved']),
                outcome=e['outcome'],
                confidence_delta=e['confidence_delta'],
                timestamp=e['timestamp']
            ))
        return MemoryListResponse(entries=resp_entries, total=len(resp_entries))
    except Exception as e:
        logger.error(f"Error retrieving customer memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/trends", response_model=MemoryTrendsResponse)
async def get_decision_trends(db: aiosqlite.Connection = Depends(get_db)):
    """Calculate and return approval rates and trends over time."""
    try:
        trends_data = await memory_repo.get_memory_trends(db)
        
        trend_items = []
        for t in trends_data.get('trends', []):
            trend_items.append(MemoryTrend(
                period=t['period'],
                total_recommendations=t['total_recommendations'],
                approved=t['approved'],
                rejected=t['rejected'],
                approval_rate=t['approval_rate']
            ))
            
        return MemoryTrendsResponse(
            trends=trend_items,
            total_decisions=trends_data.get('total_decisions', 0),
            overall_approval_rate=trends_data.get('overall_approval_rate', 0.0)
        )
    except Exception as e:
        logger.error(f"Error retrieving memory trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))
