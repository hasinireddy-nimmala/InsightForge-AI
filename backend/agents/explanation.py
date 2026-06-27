"""Explanation Agent - provides explainable evidence and justifications for recommendations."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.llm_service import LLMService
from backend.config import settings

logger = logging.getLogger(__name__)

llm = LLMService(api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_MODEL)

async def explanation_agent(state: AgentState) -> dict:
    """Generate detailed, auditable explanations for each recommended action."""
    start = datetime.now(timezone.utc)
    logger.info("Explanation Agent: Creating explainability reports")
    
    actions_data = state.get('actions', {})
    actions_list = actions_data.get('actions', [])
    
    if not actions_list:
        end = datetime.now(timezone.utc)
        return {
            'explanations': {'explanations': []},
            'agent_timeline': [{
                'agent_name': 'Explanation Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': 'No actions to explain'
            }]
        }
        
    prompt = f"""
    You are an Explainable AI agent. Review the following recommended actions generated for a customer:
    
    ---
    RECOMMENDED ACTIONS:
    {actions_list}
    ---
    
    For each action recommended, expand and produce a formal explainability record that includes:
    1. Recommendation (matching the action title)
    2. Reason (a comprehensive business-justified explanation of why this action is recommended)
    3. Evidence (a list of concrete points, quotes, or metrics proving the need)
    4. Source documents (list of filenames or data points where the evidence resides)
    5. Confidence (0.0 to 1.0 confidence score justifying the action, explaining if memory adjusted it)
    
    Format the response as a JSON object matching this schema:
    {{
        "explanations": [
            {{
                "recommendation": "Schedule Executive Business Review",
                "reason": "VP of Operations expressed frustration...",
                "evidence": ["VP mentioned considering alternatives"],
                "source_documents": ["meeting_notes.txt"],
                "confidence": 0.95
            }}
        ]
    }}
    """
    
    system_prompt = "You are a specialized Explainable AI (XAI) engine. Ensure all AI decisions are transparent, audit-ready, and backed by verifiable source facts. Respond ONLY with valid JSON."
    
    try:
        exp_res = await llm.generate_json(prompt, system_prompt)
        
        explanations_list = []
        for e in exp_res.get('explanations', []):
            explanations_list.append({
                'recommendation': e.get('recommendation', ''),
                'reason': e.get('reason', ''),
                'evidence': list(e.get('evidence', [])),
                'source_documents': list(e.get('source_documents', [])),
                'confidence': float(e.get('confidence', 0.5))
            })
            
        explanations_package = {
            'explanations': explanations_list
        }
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'explanations': explanations_package,
            'agent_timeline': [{
                'agent_name': 'Explanation Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f"Generated explanations for {len(explanations_list)} recommendations"
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Explanation error: {e}")
        
        # Build raw fallback from actions
        explanations_list = []
        for a in actions_list:
            explanations_list.append({
                'recommendation': a.get('action', ''),
                'reason': a.get('reasoning', 'Action recommended to address customer profile risks.'),
                'evidence': a.get('evidence', []),
                'source_documents': a.get('source_documents', []),
                'confidence': a.get('confidence', 0.5)
            })
            
        return {
            'explanations': {'explanations': explanations_list},
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Explanation Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error occurred; generated fallback explanations from actions.'
            }]
        }
