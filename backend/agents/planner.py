"""Planner Agent - orchestrates the analysis pipeline."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.llm_service import LLMService
from backend.services.memory_service import MemoryService
from backend.config import settings

logger = logging.getLogger(__name__)

llm = LLMService(api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_MODEL)
memory_service = MemoryService(db_path=settings.DB_PATH)

async def planner_agent(state: AgentState) -> dict:
    """Analyze input and create execution plan."""
    start = datetime.now(timezone.utc)
    logger.info("Planner Agent: Creating execution plan")
    
    try:
        # Get memory context
        memory = await memory_service.get_customer_memory(state.get('customer_id', 'default'))
        
        # Create plan
        plan_result = await llm.generate_json(
            f"Analyze this customer interaction and create an execution plan:\n\n{state.get('input_text', '')[:2000]}",
            system_prompt="You are a strategic planner. Create a JSON execution plan with key 'plan' containing a list of analysis steps."
        )
        
        plan = plan_result.get('plan', [
            'retrieve_context', 'analyze_business', 'detect_risks',
            'find_opportunities', 'recommend_actions', 'explain_reasoning'
        ])
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'plan': plan,
            'memory_context': memory,
            'agent_timeline': [{
                'agent_name': 'Planner Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f'Created plan with {len(plan)} steps'
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Planner error: {e}")
        return {
            'plan': ['retrieve_context', 'analyze_business', 'detect_risks', 'find_opportunities', 'recommend_actions', 'explain_reasoning'],
            'memory_context': [],
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Planner Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error: {str(e)[:100]}'
            }]
        }
