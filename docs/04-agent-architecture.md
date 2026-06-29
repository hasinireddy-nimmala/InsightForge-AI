# 🤖 Agent Architecture Deep-Dive

Understanding InsightForge AI's 7-agent LangGraph pipeline.

---

## Pipeline Overview

```
Input Data
    ↓
┌─────────────────────────────────────────────────────────────────┐
│   1️⃣  Planner Agent                              │ ← Classifies & routes input
└─────────────────────────────────────────┬───────────────────────┘
             ↓
    ┌───────────────────────────────────────────────────────────────┐
    │   Parallel Processing (RAG available)                         │
    │                                                               │
    │  2️⃣  Sentiment Analyst  ←────────┬                           │
    │  3️⃣  Risk Assessor       ←────┬  │                           │
    │  4️⃣  Trend Detector      ←┬   │  │                           │
    │                            │   │  │                           │
    │                            └───┴──┴────────┬────┐             │
    │                                           │ 5️⃣ RAG  │             │
    │                                           └────┘             │
    └─────────────────────────────────────┬──────────────────────┘
                 ↓
    ┌──────────────────────────────────────────────┐
    │  6️⃣  Action Generator      │  ← Synthesizes insights
    └──────────────────────────────┬─────────────────┘
                 ↓
    ┌──────────────────────────────────────────────┐
    │  7️⃣  Auditor Agent        │  ← Quality assurance
    └──────────────────────────────┬─────────────────┘
                 ↓
            Output
```

---

## Agent Details

### 1️⃣ Planner Agent

**Responsibility**: Intake coordination and analysis planning

**Input**:
- Raw customer data (documents, CRM exports, tickets)
- Customer metadata (ID, industry, account value)

**Processing**:
1. Classifies input data type (meeting notes, CRM, tickets, etc.)
2. Identifies relevant analysis dimensions
3. Creates structured analysis plan
4. Routes data to specialist agents

**Output**:
```json
{
  "data_type": "meeting_notes",
  "analysis_plan": [
    "sentiment_analysis",
    "risk_assessment",
    "trend_detection"
  ],
  "customer_context": {...},
  "urgency_level": "high"
}
```

**Key Metrics**:
- Classification accuracy: >98%
- Planning time: <500ms

---

### 2️⃣ Sentiment Analyst

**Responsibility**: Emotional intelligence and tone analysis

**Input**:
- Classified customer data
- Historical sentiment trends (from RAG)

**Processing**:
1. Performs NLP sentiment analysis on text
2. Detects frustration signals, urgency markers
3. Identifies satisfaction indicators
4. Calculates sentiment scores (-1.0 to 1.0)
5. Tracks sentiment trends over time

**Output**:
```json
{
  "overall_sentiment": -0.45,
  "sentiment_trend": "declining",
  "key_signals": [
    {"signal": "frustrated_tone", "confidence": 0.92},
    {"signal": "urgency_markers", "confidence": 0.87}
  ],
  "recommendations": "Escalate to senior support"
}
```

**Sentiment Scale**:
- **+0.7 to +1.0**: Very positive
- **+0.4 to +0.7**: Positive
- **-0.3 to +0.4**: Neutral
- **-0.7 to -0.3**: Negative
- **-1.0 to -0.7**: Very negative

---

### 3️⃣ Risk Assessor

**Responsibility**: Churn prediction and revenue risk modeling

**Input**:
- Customer behavioral signals
- Historical risk patterns (from RAG)
- Usage and engagement metrics

**Processing**:
1. Calculates churn probability using behavioral signals
2. Quantifies revenue at risk (ARR impact)
3. Identifies risk accelerators and mitigators
4. Assigns risk severity (Critical/High/Medium/Low)
5. Estimates time to churn

**Output**:
```json
{
  "churn_probability": 0.78,
  "revenue_at_risk": "$450,000 ARR",
  "risk_level": "Critical",
  "risk_accelerators": [
    "declining_usage",
    "support_tickets_increasing",
    "nps_dropping"
  ],
  "time_to_churn_estimate": "30-60 days"
}
```

**Risk Levels**:
- **Critical**: >75% churn probability, immediate action required
- **High**: 50-75%, urgent attention needed
- **Medium**: 25-50%, monitor closely
- **Low**: <25%, routine management

---

### 4️⃣ Trend Detector

**Responsibility**: Pattern recognition and anomaly detection

**Input**:
- Time-series customer data
- Historical trends (from RAG)
- Behavioral metrics

**Processing**:
1. Analyzes engagement trends (improving/stable/declining)
2. Detects anomalies in usage, support, satisfaction
3. Calculates trend velocity and acceleration
4. Forecasts future trajectory
5. Identifies inflection points

**Output**:
```json
{
  "engagement_trend": "declining",
  "trend_velocity": "-15% per week",
  "trend_acceleration": "increasing",
  "anomalies": [
    {"metric": "login_frequency", "change": "-40%"},
    {"metric": "support_tickets", "change": "+250%"}
  ],
  "forecast_90_days": "continued decline"
}
```

---

### 5️⃣ RAG Retriever

**Responsibility**: Context enrichment via semantic search

**Input**:
- Query from any upstream agent
- Vector embeddings of customer history

**Processing**:
1. Converts query to embedding using Sentence-Transformers
2. Searches FAISS vector store for similar documents
3. Retrieves top-K relevant documents with context
4. Ranks results by relevance
5. Augments agent context with historical information

**Output**:
```json
{
  "retrieved_documents": [
    {
      "source": "meeting_notes_2024_03.txt",
      "snippet": "Customer expressed concerns about feature X...",
      "similarity_score": 0.89,
      "date": "2024-03-15"
    }
  ],
  "context_summary": "Historical issues indicate ongoing frustration with feature X"
}
```

**Vector Store Details**:
- **Embedding Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Similarity Metric**: Cosine similarity
- **Index Type**: IVF (Inverted File)

---

### 6️⃣ Action Generator

**Responsibility**: Strategic recommendation synthesis

**Input**:
- Outputs from all upstream agents
- Action templates and best practices

**Processing**:
1. Synthesizes insights from Sentiment, Risk, Trend agents
2. Generates prioritized Next Best Actions (NBAs)
3. Calculates confidence scores for each action
4. Estimates business impact
5. Suggests implementation timeline and owner
6. References supporting evidence from agent outputs

**Output**:
```json
{
  "actions": [
    {
      "priority": 1,
      "action": "Schedule executive business review",
      "confidence": 0.95,
      "business_impact": "Addresses escalating concerns, may prevent churn",
      "timeline": "Within 48 hours",
      "owner": "Account Executive",
      "evidence": ["High sentiment decline", "Critical risk level", "Usage trending down"]
    },
    {
      "priority": 2,
      "action": "Assign technical support specialist",
      "confidence": 0.88,
      "business_impact": "Reduces support burden, improves satisfaction",
      "timeline": "Today",
      "owner": "Support Manager",
      "evidence": ["350% increase in support tickets"]
    }
  ]
}
```

---

### 7️⃣ Auditor Agent

**Responsibility**: Quality assurance and consistency validation

**Input**:
- Complete analysis from all upstream agents
- Original input data

**Processing**:
1. Verifies logical consistency across agent outputs
2. Checks recommendations are supported by evidence
3. Detects contradictions between agents
4. Validates sentiment/risk/trend alignment
5. Assigns confidence grade to overall output
6. Flags any anomalies for review

**Output**:
```json
{
  "overall_confidence": 0.92,
  "consistency_check": "passed",
  "evidence_alignment": [
    {"agent": "sentiment", "aligned": true, "score": 0.95},
    {"agent": "risk", "aligned": true, "score": 0.90},
    {"agent": "trend", "aligned": true, "score": 0.88}
  ],
  "flagged_issues": [],
  "quality_grade": "A",
  "audit_notes": "Analysis is well-supported and internally consistent"
}
```

**Quality Grades**:
- **A**: Excellent (>90% confidence, no issues)
- **B**: Good (80-90% confidence, minor concerns)
- **C**: Fair (70-80% confidence, some contradictions)
- **D**: Poor (<70% confidence, significant issues)

---

## Data Flow

```
1. INPUT INGESTION
   ├─ Document parsing (TXT, CSV, PDF, DOCX)
   ├─ Text extraction & cleaning
   └─ Chunking into embeddings

2. VECTOR STORE INDEXING
   ├─ Sentence-Transformer embeddings
   ├─ FAISS index creation
   └─ Metadata storage (SQLite)

3. AGENT PIPELINE EXECUTION
   ├─ Planner routes and plans
   ├─ Parallel processing (Sentiment, Risk, Trend)
   ├─ RAG enrichment (available on demand)
   ├─ Action synthesis
   └─ Quality auditing

4. OUTPUT GENERATION
   ├─ JSON structured results
   ├─ Confidence scores & evidence
   ├─ Full execution trace
   └─ Database persistence
```

---

## State Management

LangGraph manages shared state across all agents:

```python
class AnalysisState(TypedDict):
    input_data: str
    customer_id: str
    data_type: str
    
    # Planner outputs
    analysis_plan: List[str]
    
    # Agent outputs
    sentiment_result: dict
    risk_result: dict
    trend_result: dict
    actions: List[dict]
    
    # RAG context
    rag_context: List[str]
    
    # Audit results
    audit_result: dict
    execution_trace: List[dict]
```

---

## Error Handling & Resilience

### Fault Tolerance
- **Agent Timeout**: 30-second timeout per agent
- **Fallback Strategy**: If agent fails, use cached results
- **Graceful Degradation**: Skip RAG if vector DB unavailable
- **Retry Logic**: 3 attempts with exponential backoff

### Logging
- All agent inputs/outputs logged
- Full execution traces retained
- Error tracking and alerting
- Performance metrics collected

---

## Performance Characteristics

| Metric | Target | Actual |
|--------|--------|--------|
| End-to-end analysis | <10s | 8-9s |
| Planner | <500ms | 300-400ms |
| Sentiment | <2s | 1.5-2s |
| Risk assessment | <2s | 1.8-2s |
| Trend detection | <1s | 0.8-1s |
| RAG retrieval | <1s | 0.5-0.8s |
| Action generation | <2s | 1.5-2s |
| Audit | <1s | 0.8-1s |

---

## Next Steps

- 📡 [REST API Reference](./07-api-reference.md)
- 🧪 [Testing Guide](./16-testing.md)
- 🚀 [Deployment Guide](./11-production-checklist.md)