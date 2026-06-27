"""Business Analysis Agent - analyzes goals, sentiment, health, stakeholders, pain points."""
import logging
from datetime import datetime, timezone
from backend.agents.state import AgentState
from backend.services.llm_service import LLMService
from backend.config import settings

logger = logging.getLogger(__name__)

llm = LLMService(api_key=settings.GOOGLE_API_KEY, model_name=settings.LLM_MODEL)

async def business_analysis_agent(state: AgentState) -> dict:
    """Analyze customer interaction and retrieved context for business details."""
    start = datetime.now(timezone.utc)
    logger.info("Business Analysis Agent: Evaluating business context")
    
    # Compile prompt content
    input_text = state.get('input_text', '')
    context_data = state.get('context', {})
    chunks = context_data.get('retrieved_chunks', [])
    context_str = "\n\n".join([f"Source: {c['source']} (Page {c['page']})\nContent: {c['text']}" for c in chunks])
    
    prompt = f"""
    Analyze the following customer interaction and retrieved enterprise knowledge:
    
    ---
    CUSTOMER INTERACTION:
    {input_text}
    ---
    RETIRIEVED ENTERPRISE KNOWLEDGE:
    {context_str}
    ---
    
    Provide a comprehensive business analysis. Your analysis MUST include:
    1. A detailed executive summary of the customer's current status and relationship health.
    2. Sentiment analysis (e.g., negative, positive, neutral).
    3. The primary business goal the customer wants to achieve or the team wants to achieve with this customer.
    4. A customer health score from 0.0 (critical danger of churn) to 100.0 (extremely satisfied and growing).
    5. A list of key stakeholders mentioned.
    6. A list of customer pain points.
    
    Format the response as a JSON object matching this schema:
    {{
        "summary": "Detailed executive summary...",
        "sentiment": "negative/positive/neutral",
        "business_goal": "Primary business goal...",
        "customer_health_score": 75.0,
        "stakeholders": ["Name/Role", ...],
        "pain_points": ["Pain point 1", ...]
    }}
    """
    
    system_prompt = "You are an expert Enterprise Business Analyst. Analyze interactions to understand customer sentiment, health, goals, and key stakeholders. Respond ONLY with valid JSON."
    
    try:
        analysis = await llm.generate_json(prompt, system_prompt)
        
        # Ensure default structure if missing keys
        analysis_cleaned = {
            'summary': analysis.get('summary', ''),
            'sentiment': analysis.get('sentiment', 'neutral'),
            'business_goal': analysis.get('business_goal', ''),
            'customer_health_score': float(analysis.get('customer_health_score', 50.0)),
            'stakeholders': list(analysis.get('stakeholders', [])),
            'pain_points': list(analysis.get('pain_points', []))
        }
        
        end = datetime.now(timezone.utc)
        duration = (end - start).total_seconds() * 1000
        
        return {
            'business_analysis': analysis_cleaned,
            'agent_timeline': [{
                'agent_name': 'Business Analysis Agent',
                'status': 'completed',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': duration,
                'output_summary': f"Determined sentiment: {analysis_cleaned['sentiment']}, health score: {analysis_cleaned['customer_health_score']}"
            }]
        }
    except Exception as e:
        end = datetime.now(timezone.utc)
        logger.error(f"Business analysis error: {e}")
        return {
            'business_analysis': {
                'summary': 'Error performing business analysis.',
                'sentiment': 'neutral',
                'business_goal': '',
                'customer_health_score': 50.0,
                'stakeholders': [],
                'pain_points': []
            },
            'error': str(e),
            'agent_timeline': [{
                'agent_name': 'Business Analysis Agent',
                'status': 'error',
                'start_time': start.isoformat(),
                'end_time': end.isoformat(),
                'execution_time_ms': (end - start).total_seconds() * 1000,
                'output_summary': f'Error: {str(e)[:100]}'
            }]
        }
