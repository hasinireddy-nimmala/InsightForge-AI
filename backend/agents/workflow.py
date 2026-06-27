"""LangGraph workflow orchestration for InsightForge AI."""
from langgraph.graph import StateGraph, START, END
from backend.agents.state import AgentState
from backend.agents.planner import planner_agent
from backend.agents.context_retrieval import context_retrieval_agent
from backend.agents.business_analysis import business_analysis_agent
from backend.agents.risk_detection import risk_detection_agent
from backend.agents.opportunity_discovery import opportunity_discovery_agent
from backend.agents.next_best_action import next_best_action_agent
from backend.agents.explanation import explanation_agent
import uuid
import logging

logger = logging.getLogger(__name__)

def create_workflow():
    """Create and compile the LangGraph multi-agent workflow."""
    workflow = StateGraph(AgentState)
    
    # Add all agent nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("context_retrieval", context_retrieval_agent)
    workflow.add_node("business_analysis", business_analysis_agent)
    workflow.add_node("risk_detection", risk_detection_agent)
    workflow.add_node("opportunity_discovery", opportunity_discovery_agent)
    workflow.add_node("next_best_action", next_best_action_agent)
    workflow.add_node("explanation", explanation_agent)
    
    # Define edges (sequential pipeline)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "context_retrieval")
    workflow.add_edge("context_retrieval", "business_analysis")
    workflow.add_edge("business_analysis", "risk_detection")
    workflow.add_edge("risk_detection", "opportunity_discovery")
    workflow.add_edge("opportunity_discovery", "next_best_action")
    workflow.add_edge("next_best_action", "explanation")
    workflow.add_edge("explanation", END)
    
    return workflow.compile()

async def run_analysis(input_text: str, customer_id: str = "default", document_ids: list[int] = None) -> dict:
    """Run the full multi-agent analysis pipeline."""
    logger.info(f"Starting analysis for customer: {customer_id}")
    app = create_workflow()
    analysis_id = str(uuid.uuid4())[:8]
    
    initial_state = {
        "input_text": input_text,
        "customer_id": customer_id,
        "document_ids": document_ids or [],
        "plan": [],
        "context": {},
        "business_analysis": {},
        "risks": {},
        "opportunities": {},
        "actions": {},
        "explanations": {},
        "memory_context": [],
        "agent_timeline": [],
        "error": "",
        "status": "running"
    }
    
    try:
        result = await app.ainvoke(initial_state)
        result["status"] = "completed"
        result["analysis_id"] = analysis_id
        logger.info(f"Analysis {analysis_id} completed successfully")
    except Exception as e:
        logger.error(f"Workflow error: {e}")
        result = {**initial_state, "status": "error", "error": str(e), "analysis_id": analysis_id}
    
    return result
