"""Next Best Action Agent - generates concrete, prioritized recommendations adjusted by memory."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.llm_service import LLMService
from backend.services.memory_service import MemoryService
from backend.config import settings

logger = logging.getLogger(__name__)

llm = LLMService(api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_MODEL)
memory_service = MemoryService(db_path=settings.DB_PATH)

async def next_best_action_agent(state: AgentState) -> dict:
    """Generate and prioritize Next Best Actions based on customer analysis and historical memory."""
    start = datetime.now(timezone.utc)
    logger.info("Next Best Action Agent: Formulating recommended actions")
    
    input_text = state.get('input_text', '')
    context_data = state.get('context', {})
    chunks = context_data.get('retrieved_chunks', [])
    context_str = "\n\n".join([f"Source: {c['source']} (Page {c['page']})\nContent: {c['text']}" for c in chunks])
    
    business_analysis = state.get('business_analysis', {})
    risks_data = state.get('risks', {})
    opps_data = state.get('opportunities', {})
    
    memory_context = state.get('memory_context', [])
    memory_str = "\n".join([
        f"- Recommendation: '{m.get('recommendation')}' was {'Approved' if m.get('approved') else 'Rejected'}. Outcome: '{m.get('outcome')}'"
        for m in memory_context
    ])
    
    prompt = f"""
    Based on the following comprehensive analysis and historical recommendations memory, generate the Next Best Actions for this customer:
    
    ---
    CUSTOMER INTERACTION:
    {input_text}
    ---
    ENTERPRISE KNOWLEDGE CONTEXT:
    {context_str}
    ---
    ANALYSIS PROFILE:
    Sentiment: {business_analysis.get('sentiment', 'neutral')}
    Customer Health Score: {business_analysis.get('customer_health_score', 50.0)}
    Pain Points: {", ".join(business_analysis.get('pain_points', []))}
    Risks Level: {risks_data.get('risk_level', 'medium')}
    Risks Score: {risks_data.get('risk_score', 50.0)}
    Growth Opportunities: {", ".join([o.get('title', '') for o in opps_data.get('opportunities', [])])}
    ---
    HISTORICAL RECOMMENDATIONS MEMORY (Human approvals and outcomes):
    {memory_str if memory_str else "No historical records."}
    ---
    
    Generate 3 to 5 concrete, actionable Next Best Actions.
    For each action, specify:
    1. Action (title / summary of recommendation)
    2. Description (detailed execution plan)
    3. Priority ("critical", "high", "medium", "low")
    4. Impact ("high", "medium", "low")
    5. Confidence score (0.0 to 1.0)
    6. Reasoning (specific explanation of why this action is selected)
    7. Evidence (exact quotes or details supporting the need for this action)
    8. Source documents (list of filenames or sources containing the evidence)
    
    IMPORTANT: Review the HISTORICAL RECOMMENDATIONS MEMORY.
    - If a similar recommendation was previously approved and had a positive outcome, INCREASE its confidence score.
    - If a similar recommendation was previously rejected, either avoid recommending it or DECREASE its confidence score and explain how it has been modified to address past issues.
    
    Format the response as a JSON object matching this schema:
    {{
        "actions": [
            {{
                "action": "Schedule Executive Business Review",
                "description": "Arrange a meeting with key executives...",
                "priority": "critical",
                "impact": "high",
                "confidence": 0.95,
                "reasoning": "Past review was highly successful. VP of Ops requested engagement.",
                "evidence": ["VP expressed frustration about lack of executive engagement"],
                "source_documents": ["meeting_notes.txt"]
            }}
        ]
    }}
    """
    
    system_prompt = "You are a customer success and account director. Generate high-impact, prioritized, memory-adjusted recommendations. Respond ONLY with valid JSON."
    
    try:
        actions_res = await llm.generate_json(prompt, system_prompt)
        
        actions_list = []
        for a in actions_res.get('actions', []):
            # Apply memory confidence adjustments programmatically as secondary check
            action_title = a.get('action', '')
            conf = float(a.get('confidence', 0.5))
            
            # Simple similarity adjustment based on memory
            for m in memory_context:
                rec_title = m.get('recommendation', '')
                if action_title.lower() in rec_title.lower() or rec_title.lower() in action_title.lower():
                    delta = float(m.get('confidence_delta', 0.0))
                    conf = min(1.0, max(0.0, conf + delta))
                    logger.info(f"Memory matched '{rec_title}'. Adjusted confidence of '{action_title}' by {delta} to {conf}")
            
            actions_list.append({
                'action': action_title,
                'description': a.get('description', ''),
                'priority': a.get('priority', 'medium'),
                'impact': a.get('impact', 'medium'),
                'confidence': round(conf, 2),
                'reasoning': a.get('reasoning', ''),
                'evidence': list(a.get('evidence', [])),
                'source_documents': list(a.get('source_documents', []))
            })
            
        actions_package = {
            'actions': actions_list
        }
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'actions': actions_package,
            'agent_timeline': [{
                'agent_name': 'Next Best Action Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f"Generated {len(actions_list)} next best actions"
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Next best action error: {e}")
        return {
            'actions': {'actions': []},
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Next Best Action Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error: {str(e)[:100]}'
            }]
        }
