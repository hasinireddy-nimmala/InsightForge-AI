"""Pydantic schemas for InsightForge AI API."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentUploadResponse(BaseModel):
    doc_id: int
    filename: str
    file_type: str
    chunk_count: int
    status: str = "processed"


class DocumentInfo(BaseModel):
    id: int
    filename: str
    file_type: str
    upload_time: str
    status: str
    chunk_count: int


class DocumentListResponse(BaseModel):
    documents: list[DocumentInfo]
    total: int


class AnalysisRequest(BaseModel):
    input_text: str = ""
    customer_id: str = "default"
    document_ids: list[int] = []


class AgentTimelineEntry(BaseModel):
    agent_name: str
    status: str
    start_time: str
    end_time: str
    execution_time_ms: float
    output_summary: str = ""


class RiskItem(BaseModel):
    name: str
    description: str = ""
    confidence: float = 0.5
    evidence: list[str] = []


class RiskAssessment(BaseModel):
    risk_level: str = "medium"
    risk_score: float = 50.0
    risks: list[RiskItem] = []


class OpportunityItem(BaseModel):
    title: str
    description: str = ""
    impact: str = "medium"
    confidence: float = 0.5


class OpportunityAssessment(BaseModel):
    opportunities: list[OpportunityItem] = []


class ActionItem(BaseModel):
    action: str
    description: str = ""
    priority: str = "medium"
    impact: str = "medium"
    confidence: float = 0.5
    reasoning: str = ""
    evidence: list[str] = []
    source_documents: list[str] = []


class BusinessAnalysis(BaseModel):
    summary: str = ""
    sentiment: str = "neutral"
    business_goal: str = ""
    customer_health_score: float = 50.0
    stakeholders: list[str] = []
    pain_points: list[str] = []


class ExplanationItem(BaseModel):
    recommendation: str
    reason: str = ""
    evidence: list[str] = []
    source_documents: list[str] = []
    confidence: float = 0.5


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    customer_id: str = "default"
    plan: list[str] = []
    business_analysis: Optional[BusinessAnalysis] = None
    risks: Optional[RiskAssessment] = None
    opportunities: Optional[OpportunityAssessment] = None
    actions: list[ActionItem] = []
    explanations: list[ExplanationItem] = []
    agent_timeline: list[AgentTimelineEntry] = []


class AnalysisTimelineResponse(BaseModel):
    analysis_id: str
    timeline: list[AgentTimelineEntry] = []


class RecommendationResponse(BaseModel):
    id: int
    analysis_id: str
    action: str
    description: str
    priority: str
    impact: str
    confidence: float
    status: str
    created_at: str


class RecommendationListResponse(BaseModel):
    recommendations: list[RecommendationResponse]
    total: int


class ApprovalRequest(BaseModel):
    reason: str = ""


class ModifyRequest(BaseModel):
    modified_action: str
    reason: str = ""


class MemoryEntry(BaseModel):
    id: int
    customer_id: str
    recommendation: str
    approved: bool
    outcome: str
    confidence_delta: float
    timestamp: str


class MemoryListResponse(BaseModel):
    entries: list[MemoryEntry]
    total: int


class MemoryTrend(BaseModel):
    period: str
    total_recommendations: int
    approved: int
    rejected: int
    approval_rate: float


class MemoryTrendsResponse(BaseModel):
    trends: list[MemoryTrend]
    total_decisions: int
    overall_approval_rate: float


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"
    vector_store: str = "ready"
    llm: str = "configured"
