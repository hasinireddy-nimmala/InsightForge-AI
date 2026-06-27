"""Risk Detection Agent - identifies churn, revenue, escalation, renewal, and adoption risks."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.llm_service import LLMService
from backend.config import settings

logger = logging.getLogger(__name__)

llm = LLMService(api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_MODEL)

async def risk_detection_agent(state: AgentState) -> dict:
    """Analyze customer context, sentiment, and interaction history to detect risks."""
    start = datetime.now(timezone.utc)
    logger.info("Risk Detection Agent: Assessing relationship and revenue risks")
    
    input_text = state.get('input_text', '')
    context_data = state.get('context', {})
    chunks = context_data.get('retrieved_chunks', [])
    context_str = "\n\n".join([f"Source: {c['source']} (Page {c['page']})\nContent: {c['text']}" for c in chunks])
    
    business_analysis = state.get('business_analysis', {})
    
    prompt = f"""
    Analyze the following customer interaction details and business assessment:
    
    ---
    CUSTOMER INTERACTION:
    {input_text}
    ---
    ENTERPRISE KNOWLEDGE CONTEXT:
    {context_str}
    ---
    BUSINESS ASSESSMENT:
    Sentiment: {business_analysis.get('sentiment', 'neutral')}
    Pain Points: {", ".join(business_analysis.get('pain_points', []))}
    ---
    
    Identify specific risks in the following categories:
    1. Churn Risk (likelihood of customer canceling or not renewing)
    2. Revenue Risk (likelihood of loss of contract value or downsell)
    3. Escalation Risk (likelihood of support issue escalating or needing legal intervention)
    4. Renewal Risk (risks tied specifically to upcoming renewal dates/contract status)
    5. Product Adoption Risk (customer not using feature-set fully or training gaps)
    
    For each risk identified, provide:
    - Name (category name)
    - Description of the specific risk
    - Confidence score (0.0 to 1.0)
    - Specific evidence from the interaction or context (quotes, metrics)
    
    Also determine:
    - An aggregate risk_level ("low", "medium", "high", or "critical")
    - An aggregate risk_score from 0.0 (no risk) to 100.0 (extreme danger)
    
    Format the response as a JSON object matching this schema:
    {{
        "risk_level": "high",
        "risk_score": 75.0,
        "risks": [
            {{
                "name": "Churn Risk",
                "description": "Specific details...",
                "confidence": 0.85,
                "evidence": ["Evidence 1", "Evidence 2"]
            }}
        ]
    }}
    """
    
    system_prompt = "You are a senior Risk & Compliance Officer. Analyze accounts to detect churn, contract, escalation, and product adoption risks. Respond ONLY with valid JSON."
    
    try:
        risks_res = await llm.generate_json(prompt, system_prompt)
        
        # Clean risks structure
        risks_list = []
        for r in risks_res.get('risks', []):
            risks_list.append({
                'name': r.get('name', ''),
                'description': r.get('description', ''),
                'confidence': float(r.get('confidence', 0.5)),
                'evidence': list(r.get('evidence', []))
            })
            
        risks_package = {
            'risk_level': risks_res.get('risk_level', 'medium'),
            'risk_score': float(risks_res.get('risk_score', 50.0)),
            'risks': risks_list
        }
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'risks': risks_package,
            'agent_timeline': [{
                'agent_name': 'Risk Detection Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f"Detected {len(risks_list)} risk items. Level: {risks_package['risk_level']}, Score: {risks_package['risk_score']}"
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Risk detection error: {e}")
        return {
            'risks': {
                'risk_level': 'medium',
                'risk_score': 50.0,
                'risks': []
            },
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Risk Detection Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error: {str(e)[:100]}'
            }]
        }
