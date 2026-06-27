"""FastAPI endpoints for recommendation human review and feedback."""
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
import logging
from typing import List

from backend.database import get_db
from backend.models.schemas import (
    RecommendationResponse, 
    RecommendationListResponse, 
    ApprovalRequest, 
    ModifyRequest
)
from backend.repositories import recommendation_repo, memory_repo, audit_repo
from backend.api.analysis import analysis_cache

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/recommendations/{analysis_id}", response_model=RecommendationListResponse)
async def get_analysis_recommendations(analysis_id: str, db: aiosqlite.Connection = Depends(get_db)):
    """Retrieve recommendations for a specific analysis run."""
    try:
        recs = await recommendation_repo.get_recommendations_by_analysis(db, analysis_id)
        resp_recs = []
        for r in recs:
            resp_recs.append(RecommendationResponse(
                id=r['id'],
                analysis_id=r['analysis_id'],
                action=r['action'],
                description=r['description'],
                priority=r['priority'],
                impact=r['impact'],
                confidence=r['confidence'],
                status=r['status'],
                created_at=r['created_at']
            ))
        return RecommendationListResponse(recommendations=resp_recs, total=len(resp_recs))
    except Exception as e:
        logger.error(f"Error retrieving recommendations for analysis {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/pending/all", response_model=RecommendationListResponse)
async def get_all_pending_recommendations(db: aiosqlite.Connection = Depends(get_db)):
    """Get all recommendations waiting for human-in-the-loop approval."""
    try:
        recs = await recommendation_repo.get_pending_recommendations(db)
        resp_recs = []
        for r in recs:
            resp_recs.append(RecommendationResponse(
                id=r['id'],
                analysis_id=r['analysis_id'],
                action=r['action'],
                description=r['description'],
                priority=r['priority'],
                impact=r['impact'],
                confidence=r['confidence'],
                status=r['status'],
                created_at=r['created_at']
            ))
        return RecommendationListResponse(recommendations=resp_recs, total=len(resp_recs))
    except Exception as e:
        logger.error(f"Error retrieving pending recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/{rec_id}/approve")
async def approve_recommendation(rec_id: int, req: ApprovalRequest, db: aiosqlite.Connection = Depends(get_db)):
    """Approve a recommendation, logging details and saving to decision memory."""
    try:
        rec = await recommendation_repo.get_recommendation(db, rec_id)
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found")
            
        # Update status
        await recommendation_repo.update_recommendation_status(db, rec_id, "approved")
        
        # Save feedback
        await memory_repo.save_feedback(
            db=db,
            recommendation_id=rec_id,
            decision="approved",
            modified_action="",
            reason=req.reason
        )
        
        # Get customer ID from cache or use fallback
        customer_id = "default"
        analysis_id = rec['analysis_id']
        if analysis_id in analysis_cache:
            customer_id = analysis_cache[analysis_id].customer_id
            
        # Store in recommendation learning memory
        await memory_repo.save_memory(
            db=db,
            customer_id=customer_id,
            recommendation=rec['action'],
            approved=True,
            outcome="Accepted",
            confidence_delta=0.05
        )
        
        # Log action in audit trails
        await audit_repo.log_action(
            db=db,
            action="recommendation_approved",
            entity_type="recommendation",
            entity_id=str(rec_id),
            details=f"Approved action: '{rec['action']}' for customer {customer_id}"
        )
        
        return {"status": "success", "message": f"Recommendation {rec_id} approved"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error approving recommendation {rec_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/{rec_id}/reject")
async def reject_recommendation(rec_id: int, req: ApprovalRequest, db: aiosqlite.Connection = Depends(get_db)):
    """Reject a recommendation, logging reasons and capturing decision memory."""
    try:
        rec = await recommendation_repo.get_recommendation(db, rec_id)
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found")
            
        # Update status
        await recommendation_repo.update_recommendation_status(db, rec_id, "rejected")
        
        # Save feedback
        await memory_repo.save_feedback(
            db=db,
            recommendation_id=rec_id,
            decision="rejected",
            modified_action="",
            reason=req.reason
        )
        
        # Get customer ID
        customer_id = "default"
        analysis_id = rec['analysis_id']
        if analysis_id in analysis_cache:
            customer_id = analysis_cache[analysis_id].customer_id
            
        # Store in learning memory
        await memory_repo.save_memory(
            db=db,
            customer_id=customer_id,
            recommendation=rec['action'],
            approved=False,
            outcome=f"Rejected: {req.reason}",
            confidence_delta=-0.03
        )
        
        # Log action
        await audit_repo.log_action(
            db=db,
            action="recommendation_rejected",
            entity_type="recommendation",
            entity_id=str(rec_id),
            details=f"Rejected action: '{rec['action']}' for customer {customer_id}. Reason: {req.reason}"
        )
        
        return {"status": "success", "message": f"Recommendation {rec_id} rejected"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rejecting recommendation {rec_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations/{rec_id}/modify")
async def modify_recommendation(rec_id: int, req: ModifyRequest, db: aiosqlite.Connection = Depends(get_db)):
    """Modify the recommendation text/details before approval."""
    try:
        rec = await recommendation_repo.get_recommendation(db, rec_id)
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found")
            
        # Update status and save modified action
        await db.execute(
            'UPDATE recommendations SET action = ?, status = ? WHERE id = ?',
            (req.modified_action, "approved", rec_id)
        )
        await db.commit()
        
        # Save feedback
        await memory_repo.save_feedback(
            db=db,
            recommendation_id=rec_id,
            decision="modified",
            modified_action=req.modified_action,
            reason=req.reason
        )
        
        # Get customer ID
        customer_id = "default"
        analysis_id = rec['analysis_id']
        if analysis_id in analysis_cache:
            customer_id = analysis_cache[analysis_id].customer_id
            
        # Store in memory (modified recommendations count as partially approved / learnings)
        await memory_repo.save_memory(
            db=db,
            customer_id=customer_id,
            recommendation=req.modified_action,
            approved=True,
            outcome="Modified and Accepted",
            confidence_delta=0.02
        )
        
        # Log action
        await audit_repo.log_action(
            db=db,
            action="recommendation_modified",
            entity_type="recommendation",
            entity_id=str(rec_id),
            details=f"Modified action from '{rec['action']}' to '{req.modified_action}' for customer {customer_id}"
        )
        
        return {"status": "success", "message": f"Recommendation {rec_id} modified and approved"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error modifying recommendation {rec_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
