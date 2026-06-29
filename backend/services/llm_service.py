"""LLM service for Gemini 2.5 Flash with demo fallback."""
import json
import logging
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self, api_key: str = "", model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self._model = None
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self._model = genai.GenerativeModel(model_name)
                logger.info(f"LLM configured: {model_name}")
            except Exception as e:
                logger.warning(f"Failed to configure LLM: {e}")

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key) and self._model is not None

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.is_configured:
            return self._demo_response(prompt)
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = await asyncio.to_thread(self._model.generate_content, full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return self._demo_response(prompt)

    async def generate_json(self, prompt: str, system_prompt: str = "") -> dict:
        if not self.is_configured:
            return self._demo_json_response(prompt)

        json_prompt = (
            f"{system_prompt}\n\n"
            f"Respond ONLY with valid JSON. No markdown.\n\n"
            f"{prompt}"
        )

        for attempt in range(3):
            try:
                response = await asyncio.to_thread(
                    self._model.generate_content,
                    json_prompt
                )

                text = response.text.strip()

                if text.startswith("```"):
                    text = text.split("\n", 1)[1]
                    text = text.rsplit("```", 1)[0]

                return json.loads(text)

            except Exception as e:
                error = str(e)

                if "429" in error:
                    wait_time = (attempt + 1) * 10

                    logger.warning(
                        f"Gemini rate limit reached. Waiting {wait_time} seconds..."
                    )

                    await asyncio.sleep(wait_time)
                    continue

                logger.error(f"LLM JSON error: {e}")
                break

        logger.warning("Using demo response after retries failed.")
        return self._demo_json_response(prompt)

    def _demo_response(self, prompt: str) -> str:
        return "Customer is experiencing significant onboarding challenges with declining platform adoption. Urgent executive intervention needed before 45-day renewal deadline."

    def _demo_json_response(self, prompt: str) -> dict:
        p = prompt.lower()
        if 'plan' in p:
            return {"plan": ["retrieve_context", "analyze_business", "detect_risks", "find_opportunities", "recommend_actions", "explain_reasoning"]}
        elif 'risk' in p:
            return {"risk_level": "high", "risk_score": 78.0, "risks": [
                {"name": "Churn Risk", "description": "Customer showing dissatisfaction with declining usage and increasing support tickets", "confidence": 0.87, "evidence": ["Usage declined 35% over last quarter", "3 escalated support tickets in 2 weeks"]},
                {"name": "Renewal Risk", "description": "Contract renewal approaching with unresolved issues", "confidence": 0.82, "evidence": ["Renewal due in 45 days", "Customer expressed frustration in last meeting"]},
                {"name": "Escalation Risk", "description": "Support ticket volume increasing with higher severity", "confidence": 0.75, "evidence": ["Support tickets increased 60%", "Average resolution time growing"]},
                {"name": "Product Adoption Risk", "description": "Low feature adoption indicating poor onboarding", "confidence": 0.80, "evidence": ["Only 30% feature adoption rate", "Training completion below 50%"]}
            ]}
        elif 'opportunit' in p:
            return {"opportunities": [
                {"title": "Premium Onboarding Package", "description": "Dedicated onboarding support could resolve adoption issues and demonstrate commitment", "impact": "high", "confidence": 0.85},
                {"title": "Executive Business Review", "description": "Strategic alignment session to address concerns and showcase platform value", "impact": "high", "confidence": 0.80},
                {"title": "Customer Success Manager Assignment", "description": "Dedicated CSM to drive adoption and provide proactive support", "impact": "medium", "confidence": 0.78},
                {"title": "Custom Integration Support", "description": "Tailored integration assistance to resolve technical pain points", "impact": "medium", "confidence": 0.72}
            ]}
        elif 'action' in p or 'recommend' in p:
            return {"actions": [
                {"action": "Schedule Executive Business Review", "description": "Arrange urgent executive meeting to address concerns and align on success metrics", "priority": "critical", "impact": "high", "confidence": 0.92, "reasoning": "Customer VP expressed dissatisfaction; executive engagement shows commitment", "evidence": ["VP mentioned dissatisfaction in last 3 meetings", "Usage dropped 35%"], "source_documents": ["meeting_notes.txt"]},
                {"action": "Assign Dedicated Customer Success Manager", "description": "Immediately assign senior CSM for personalized guidance and weekly check-ins", "priority": "high", "impact": "high", "confidence": 0.88, "reasoning": "Reactive support model failing; proactive CSM needed", "evidence": ["Support tickets up 60%", "No proactive outreach in 45 days"], "source_documents": ["support_tickets.txt"]},
                {"action": "Launch Retention Campaign", "description": "Initiate targeted retention with custom training and onboarding refresh", "priority": "high", "impact": "medium", "confidence": 0.85, "reasoning": "Renewal in 45 days requires immediate value demonstration", "evidence": ["Feature adoption at only 30%", "Training completion below 50%"], "source_documents": ["crm_export.csv"]},
                {"action": "Offer Complimentary Premium Onboarding", "description": "Provide premium onboarding package to resolve adoption issues before renewal", "priority": "medium", "impact": "high", "confidence": 0.80, "reasoning": "Root cause of dissatisfaction is poor initial onboarding experience", "evidence": ["Customer cited onboarding as primary frustration"], "source_documents": ["meeting_notes.txt"]},
                {"action": "Escalate Open Support Tickets", "description": "Prioritize all open tickets with dedicated engineering support", "priority": "high", "impact": "medium", "confidence": 0.90, "reasoning": "Unresolved tickets eroding trust and satisfaction", "evidence": ["4 open tickets older than 7 days", "2 critical severity tickets"], "source_documents": ["support_tickets.txt"]}
            ]}
        elif 'explain' in p or 'evidence' in p:
            return {"explanations": [
                {"recommendation": "Schedule Executive Business Review", "reason": "Customer VP expressed dissatisfaction in last 3 meetings with declining engagement. An executive review demonstrates organizational commitment and provides opportunity to realign on success metrics.", "evidence": ["VP mentioned considering alternatives", "Usage declined 35% QoQ", "No executive engagement in 60 days"], "source_documents": ["meeting_notes.txt - Section 3", "crm_export.csv"], "confidence": 0.92},
                {"recommendation": "Assign Dedicated Customer Success Manager", "reason": "Current reactive support model is failing to address growing customer needs. A dedicated CSM can anticipate issues and drive proactive adoption.", "evidence": ["Support tickets increased 60%", "No proactive outreach in 45 days", "Customer requested single point of contact"], "source_documents": ["support_tickets.txt", "meeting_notes.txt"], "confidence": 0.88},
                {"recommendation": "Launch Retention Campaign", "reason": "With renewal approaching in 45 days and declining usage, targeted intervention needed to demonstrate ongoing platform value.", "evidence": ["Renewal in 45 days", "Feature adoption at 30%", "Negative sentiment trend"], "source_documents": ["crm_export.csv", "meeting_notes.txt"], "confidence": 0.85},
                {"recommendation": "Offer Complimentary Premium Onboarding", "reason": "Root cause analysis shows poor onboarding as the primary driver of dissatisfaction. Addressing this directly shows responsiveness.", "evidence": ["Customer cited onboarding as #1 frustration", "Training completion below 50%"], "source_documents": ["meeting_notes.txt"], "confidence": 0.80},
                {"recommendation": "Escalate Open Support Tickets", "reason": "Unresolved technical issues are compounding customer frustration and blocking adoption. Rapid resolution will build trust.", "evidence": ["4 tickets open >7 days", "2 critical severity unresolved", "Customer threatened escalation"], "source_documents": ["support_tickets.txt"], "confidence": 0.90}
            ]}
        elif 'business' in p or 'summar' in p or 'analy' in p:
            return {"summary": "Customer Acme Corporation is experiencing significant onboarding challenges leading to declining platform adoption. With renewal approaching in 45 days, there is an urgent need for executive intervention and dedicated success management. Support ticket volume has increased 60% while usage metrics show a 35% decline, indicating growing dissatisfaction. The VP of Operations has expressed frustration about lack of executive engagement and is reportedly considering alternatives.", "sentiment": "negative", "business_goal": "Reduce churn risk and drive platform adoption before renewal deadline", "customer_health_score": 32.0, "stakeholders": ["Sarah Chen - VP of Operations", "Michael Rodriguez - IT Director", "End Users (Engineering Team)"], "pain_points": ["Poor onboarding experience", "Increasing support ticket volume", "Declining platform usage", "Lack of dedicated support contact", "Integration delays", "Insufficient training"]}
        return {"result": "Demo mode - configure GOOGLE_API_KEY for live AI"}
