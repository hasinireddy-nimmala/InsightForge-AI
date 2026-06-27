"""LangGraph agent state definition."""
from typing import TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    """Shared state for the LangGraph agent pipeline."""
    input_text: str
    customer_id: str
    document_ids: list[int]
    plan: list[str]
    context: dict
    business_analysis: dict
    risks: dict
    opportunities: dict
    actions: dict
    explanations: dict
    memory_context: list
    agent_timeline: Annotated[list, add]
    error: str
    status: str
