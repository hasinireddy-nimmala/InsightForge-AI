"""FastAPI endpoints for running multi-agent AI analysis."""
from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any

from backend.database import get_db
from backend.config import settings
from backend.models.schemas import (
    AnalysisRequest, 
    AnalysisResponse, 
    BusinessAnalysis, 
    RiskAssessment, 
    RiskItem,
    OpportunityAssessment, 
    OpportunityItem, 
    ActionItem, 
    ExplanationItem, 
    AgentTimelineEntry,
    AnalysisTimelineResponse
)
from backend.agents.workflow import run_analysis
from backend.repositories import recommendation_repo, audit_repo

logger = logging.getLogger(__name__)
router = APIRouter()

# Global cache for active session analysis
analysis_cache: Dict[str, Any] = {}

@router.post("/analysis/run", response_model=AnalysisResponse)
async def trigger_analysis(req: AnalysisRequest, db: aiosqlite.Connection = Depends(get_db)):
    """Run the multi-agent decision intelligence pipeline on customer context."""
    input_text = req.input_text.strip()
    
    # If no input text is provided, gather all text from database documents to build interaction context
    if not input_text:
        try:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT chunk_text FROM vector_metadata LIMIT 20")
            rows = await cursor.fetchall()
            input_text = "\n\n".join([row['chunk_text'] for row in rows])
            
            if not input_text:
                input_text = "Acme Corporation onboarding review. Usage metrics are down, and support tickets have increased."
                logger.info("No vectors found. Using default fallback interaction text.")
        except Exception as e:
            logger.error(f"Error gathering context from database: {e}")
            input_text = "Acme Corporation onboarding review. Usage metrics are down, and support tickets have increased."
            
    try:
        # Run LangGraph pipeline
        result = await run_analysis(
            input_text=input_text,
            customer_id=req.customer_id,
            document_ids=req.document_ids
        )
        
        analysis_id = result["analysis_id"]
        
        # Save individual agent outputs to the database
        # Planner
        plan = result.get("plan", [])
        await recommendation_repo.save_agent_output(
            db=db,
            analysis_id=analysis_id,
            agent_name="Planner Agent",
            output_json=json.dumps({"plan": plan}),
            execution_time_ms=0.0
        )
        
        # Business Analysis
        ba_data = result.get("business_analysis", {})
        await recommendation_repo.save_agent_output(
            db=db,
            analysis_id=analysis_id,
            agent_name="Business Analysis Agent",
            output_json=json.dumps(ba_data),
            execution_time_ms=0.0
        )
        
        # Risks
        risks_data = result.get("risks", {})
        await recommendation_repo.save_agent_output(
            db=db,
            analysis_id=analysis_id,
            agent_name="Risk Detection Agent",
            output_json=json.dumps(risks_data),
            execution_time_ms=0.0
        )
        
        # Opportunities
        opps_data = result.get("opportunities", {})
        await recommendation_repo.save_agent_output(
            db=db,
            analysis_id=analysis_id,
            agent_name="Opportunity Discovery Agent",
            output_json=json.dumps(opps_data),
            execution_time_ms=0.0
        )
        
        # Next Best Actions & Explanations
        actions_data = result.get("actions", {})
        actions_list = actions_data.get("actions", [])
        
        explanations_data = result.get("explanations", {})
        explanations_list = explanations_data.get("explanations", [])
        
        # Save recommendations to database
        for action in actions_list:
            await recommendation_repo.save_recommendation(
                db=db,
                analysis_id=analysis_id,
                action=action.get("action", ""),
                description=action.get("description", ""),
                priority=action.get("priority", "medium"),
                impact=action.get("impact", "medium"),
                confidence=action.get("confidence", 0.5)
            )
            
        # Log analysis run in audit log
        await audit_repo.log_action(
            db=db,
            action="analysis_run",
            entity_type="analysis",
            entity_id=analysis_id,
            details=f"Ran multi-agent pipeline for customer {req.customer_id}. Actions generated: {len(actions_list)}"
        )
        
        # Format timeline entries
        timeline_entries = []
        for t in result.get("agent_timeline", []):
            timeline_entries.append(AgentTimelineEntry(
                agent_name=t.get("agent_name", ""),
                status=t.get("status", "completed"),
                start_time=t.get("start_time", ""),
                end_time=t.get("end_time", ""),
                execution_time_ms=t.get("execution_time_ms", 0.0),
                output_summary=t.get("output_summary", "")
            ))
            
        # Format Pydantic response models
        ba_model = None
        if ba_data:
            ba_model = BusinessAnalysis(
                summary=ba_data.get("summary", ""),
                sentiment=ba_data.get("sentiment", "neutral"),
                business_goal=ba_data.get("business_goal", ""),
                customer_health_score=ba_data.get("customer_health_score", 50.0),
                stakeholders=ba_data.get("stakeholders", []),
                pain_points=ba_data.get("pain_points", [])
            )
            
        risks_model = None
        if risks_data:
            risk_items = [RiskItem(
                name=r.get("name", ""),
                description=r.get("description", ""),
                confidence=r.get("confidence", 0.5),
                evidence=r.get("evidence", [])
            ) for r in risks_data.get("risks", [])]
            risks_model = RiskAssessment(
                risk_level=risks_data.get("risk_level", "medium"),
                risk_score=risks_data.get("risk_score", 50.0),
                risks=risk_items
            )
            
        opps_model = None
        if opps_data:
            opp_items = [OpportunityItem(
                title=o.get("title", ""),
                description=o.get("description", ""),
                impact=o.get("impact", "medium"),
                confidence=o.get("confidence", 0.5)
            ) for o in opps_data.get("opportunities", [])]
            opps_model = OpportunityAssessment(opportunities=opp_items)
            
        action_models = [ActionItem(
            action=a.get("action", ""),
            description=a.get("description", ""),
            priority=a.get("priority", "medium"),
            impact=a.get("impact", "medium"),
            confidence=a.get("confidence", 0.5),
            reasoning=a.get("reasoning", ""),
            evidence=a.get("evidence", []),
            source_documents=a.get("source_documents", [])
        ) for a in actions_list]
        
        explanation_models = [ExplanationItem(
            recommendation=e.get("recommendation", ""),
            reason=e.get("reason", ""),
            evidence=e.get("evidence", []),
            source_documents=e.get("source_documents", []),
            confidence=e.get("confidence", 0.5)
        ) for e in explanations_list]
        
        response = AnalysisResponse(
            analysis_id=analysis_id,
            status=result["status"],
            customer_id=result["customer_id"],
            plan=plan,
            business_analysis=ba_model,
            risks=risks_model,
            opportunities=opps_model,
            actions=action_models,
            explanations=explanation_models,
            agent_timeline=timeline_entries
        )
        
        # Save to memory cache
        analysis_cache[analysis_id] = response
        
        return response
        
    except Exception as e:
        logger.error(f"Error executing analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis_results(analysis_id: str):
    """Retrieve full analysis results by ID."""
    if analysis_id in analysis_cache:
        return analysis_cache[analysis_id]
        
    raise HTTPException(status_code=404, detail="Analysis results not found or expired")

@router.get("/analysis/{analysis_id}/timeline", response_model=AnalysisTimelineResponse)
async def get_analysis_timeline(analysis_id: str):
    """Retrieve timeline execution metrics for a specific analysis run."""
    if analysis_id in analysis_cache:
        res = analysis_cache[analysis_id]
        return AnalysisTimelineResponse(
            analysis_id=analysis_id,
            timeline=res.agent_timeline
        )
        
    raise HTTPException(status_code=404, detail="Analysis results not found or expired")
