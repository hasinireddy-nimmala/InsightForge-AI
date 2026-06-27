"""Opportunity Discovery Agent - identifies upsell, cross-sell, expansion, and success opportunities."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.llm_service import LLMService
from backend.config import settings

logger = logging.getLogger(__name__)

llm = LLMService(api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_MODEL)

async def opportunity_discovery_agent(state: AgentState) -> dict:
    """Analyze context to find expansion and growth opportunities."""
    start = datetime.now(timezone.utc)
    logger.info("Opportunity Discovery Agent: Identifying customer growth opportunities")
    
    input_text = state.get('input_text', '')
    context_data = state.get('context', {})
    chunks = context_data.get('retrieved_chunks', [])
    context_str = "\n\n".join([f"Source: {c['source']} (Page {c['page']})\nContent: {c['text']}" for c in chunks])
    
    business_analysis = state.get('business_analysis', {})
    risks_data = state.get('risks', {})
    
    prompt = f"""
    Analyze the customer profile and engagement context below to discover account growth opportunities:
    
    ---
    CUSTOMER INTERACTION:
    {input_text}
    ---
    ENTERPRISE KNOWLEDGE CONTEXT:
    {context_str}
    ---
    BUSINESS & RISK PROFILE:
    Sentiment: {business_analysis.get('sentiment', 'neutral')}
    Customer Health Score: {business_analysis.get('customer_health_score', 50.0)}
    Detected Risks Level: {risks_data.get('risk_level', 'medium')}
    ---
    
    Identify potential growth and support opportunities, including:
    1. Upsell Opportunities (e.g. premium onboarding package, tier upgrade, dedicated training)
    2. Cross-sell Opportunities (e.g. adding analytics module, additional APIs, integrations)
    3. Expansion Opportunities (e.g. expanding to other teams, adding user seats)
    4. Customer Success Opportunities (e.g. scheduling training refreshes, assigning CSM)
    
    For each opportunity, specify:
    - Title
    - Description of the opportunity and how to position it
    - Impact level ("low", "medium", "high")
    - Confidence score (0.0 to 1.0)
    
    Format the response as a JSON object matching this schema:
    {{
        "opportunities": [
            {{
                "title": "Premium Onboarding Package",
                "description": "Offering dedicated support to fix adoption...",
                "impact": "high",
                "confidence": 0.85
            }}
        ]
    }}
    """
    
    system_prompt = "You are a customer success director and account growth strategist. Identify upsell, cross-sell, and retention opportunities. Respond ONLY with valid JSON."
    
    try:
        opps_res = await llm.generate_json(prompt, system_prompt)
        
        opps_list = []
        for o in opps_res.get('opportunities', []):
            opps_list.append({
                'title': o.get('title', ''),
                'description': o.get('description', ''),
                'impact': o.get('impact', 'medium'),
                'confidence': float(o.get('confidence', 0.5))
            })
            
        opps_package = {
            'opportunities': opps_list
        }
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'opportunities': opps_package,
            'agent_timeline': [{
                'agent_name': 'Opportunity Discovery Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f"Identified {len(opps_list)} expansion/growth opportunities"
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Opportunity discovery error: {e}")
        return {
            'opportunities': {'opportunities': []},
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Opportunity Discovery Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error: {str(e)[:100]}'
            }]
        }
