# 📡 REST API Reference

Complete documentation of InsightForge AI REST API endpoints.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production, implement:
- API key validation
- JWT tokens
- OAuth 2.0

See [Production Checklist](./11-production-checklist.md#security).

---

## Health & Status

### GET /api/health

Check API health and system status.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-06-29T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "vector_store": "connected",
    "llm_provider": "connected"
  }
}
```

---

## Document Upload

### POST /api/upload

Upload and ingest customer documents.

**Request**:
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.txt" \
  -F "customer_id=acme-corp" \
  -F "document_type=meeting_notes"
```

**Parameters**:
- `file` (required): Document file (TXT, CSV, PDF, DOCX)
- `customer_id` (required): Unique customer identifier
- `document_type` (optional): Type of document
  - `meeting_notes`
  - `crm_export`
  - `support_tickets`
  - `auto_detect` (default)

**Response** (200 OK):
```json
{
  "file_id": "doc_abc123",
  "filename": "document.txt",
  "customer_id": "acme-corp",
  "size_bytes": 2048,
  "chunks_created": 5,
  "ingestion_time_ms": 1250,
  "status": "indexed",
  "message": "Document successfully ingested and vectorized"
}
```

**Error Responses**:
```json
{
  "error": "Unsupported file format",
  "supported_formats": ["txt", "csv", "pdf", "docx"]
}
```

---

## Analysis Pipeline

### POST /api/analyze

Run the 7-agent analysis pipeline.

**Request**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Customer expressed concerns about feature deprecation",
    "customer_id": "acme-corp",
    "analysis_type": "comprehensive",
    "include_rag_context": true
  }'
```

**Parameters**:
- `input_text` (required): Customer data or query
- `customer_id` (required): Customer identifier
- `analysis_type` (optional): Type of analysis
  - `comprehensive`: Full 7-agent pipeline (default)
  - `quick`: Planner + Action Generator only
  - `sentiment_only`: Sentiment analysis only
  - `risk_only`: Risk assessment only
- `include_rag_context` (optional): Include RAG retrieval (default: true)
- `timeout_seconds` (optional): Pipeline timeout (default: 30)

**Response** (200 OK):
```json
{
  "analysis_id": "ana_xyz789",
  "customer_id": "acme-corp",
  "status": "completed",
  "execution_time_ms": 8432,
  "pipeline": {
    "planner": {
      "data_type": "meeting_notes",
      "analysis_plan": ["sentiment_analysis", "risk_assessment"],
      "execution_time_ms": 380
    },
    "sentiment": {
      "overall_sentiment": -0.65,
      "trend": "declining",
      "key_signals": [{"signal": "frustrated_tone", "confidence": 0.92}],
      "execution_time_ms": 1850
    },
    "risk": {
      "churn_probability": 0.72,
      "revenue_at_risk": "$300,000",
      "risk_level": "High",
      "execution_time_ms": 1950
    },
    "trend": {
      "engagement_trend": "declining",
      "trend_velocity": "-12% per week",
      "forecast_90_days": "continued decline",
      "execution_time_ms": 920
    },
    "actions": {
      "recommendations": [
        {
          "priority": 1,
          "action": "Schedule executive business review",
          "confidence": 0.95
        }
      ],
      "execution_time_ms": 1840
    },
    "audit": {
      "overall_confidence": 0.92,
      "quality_grade": "A",
      "consistency_check": "passed",
      "execution_time_ms": 680
    }
  },
  "rag_context": [
    {
      "source": "meeting_notes_2024_03.txt",
      "snippet": "Customer mentioned similar concerns 3 months ago...",
      "similarity": 0.89
    }
  ]
}
```

**Error Responses**:
```json
{
  "error": "Analysis failed",
  "reason": "LLM provider unavailable",
  "retry_after_seconds": 30
}
```

### GET /api/analysis/{id}

Retrieve analysis results by ID.

**Response** (200 OK):
```json
{
  "analysis_id": "ana_xyz789",
  "customer_id": "acme-corp",
  "created_at": "2026-06-29T10:30:00Z",
  "status": "completed",
  "pipeline": {...},
  "rag_context": [...]
}
```

### GET /api/history

List all past analyses.

**Query Parameters**:
- `customer_id` (optional): Filter by customer
- `limit` (optional): Max results (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response** (200 OK):
```json
{
  "total": 127,
  "limit": 50,
  "offset": 0,
  "analyses": [
    {
      "analysis_id": "ana_xyz789",
      "customer_id": "acme-corp",
      "created_at": "2026-06-29T10:30:00Z",
      "status": "completed",
      "execution_time_ms": 8432
    }
  ]
}
```

---

## Knowledge Base

### POST /api/knowledge/search

Semantic search across ingested documents.

**Request**:
```bash
curl -X POST http://localhost:8000/api/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main complaints from Acme?",
    "customer_id": "acme-corp",
    "top_k": 5
  }'
```

**Parameters**:
- `query` (required): Natural language search query
- `customer_id` (optional): Filter by customer
- `top_k` (optional): Number of results (default: 5)
- `similarity_threshold` (optional): Min similarity (0-1, default: 0.5)

**Response** (200 OK):
```json
{
  "query": "What are the main complaints from Acme?",
  "results": [
    {
      "rank": 1,
      "source": "meeting_notes_2024_06.txt",
      "snippet": "Customer reported three main issues: feature X doesn't work as advertised, performance degradation in reports module, and insufficient API documentation.",
      "similarity_score": 0.94,
      "document_id": "doc_abc123",
      "ingestion_date": "2026-06-15T08:00:00Z"
    }
  ]
}
```

### GET /api/knowledge/stats

Get knowledge base statistics.

**Response** (200 OK):
```json
{
  "total_documents": 42,
  "total_chunks": 1250,
  "total_customers": 8,
  "vector_index_size_mb": 45.3,
  "embedding_model": "all-MiniLM-L6-v2",
  "last_indexed": "2026-06-29T10:15:00Z",
  "customers": [
    {"customer_id": "acme-corp", "documents": 12, "chunks": 340}
  ]
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|----------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (resource doesn't exist) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (LLM provider down) |

### Error Response Format

```json
{
  "error": "Descriptive error message",
  "error_code": "INVALID_FILE_FORMAT",
  "details": {
    "received_format": "xyz",
    "supported_formats": ["txt", "csv", "pdf", "docx"]
  },
  "request_id": "req_12345",
  "timestamp": "2026-06-29T10:30:00Z"
}
```

---

## Rate Limiting

Currently no rate limiting. For production:
- Implement per-IP rate limiting
- Add API key tier-based limits
- Queue long-running analyses

---

## OpenAPI Documentation

Full interactive API documentation available at:

```
http://localhost:8000/docs
```

---

## Next Steps

- 🔗 [Integration Guide](./08-integration-guide.md)
- 🐍 [Python SDK Guide](./09-sdk-guide.md)
- 💡 [Example Usage](#example-usage)

---

## Example Usage

### Complete Workflow

```bash
#!/bin/bash

# 1. Upload document
RESPONSE=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@customer_notes.txt" \
  -F "customer_id=acme-corp")
echo "Uploaded: $RESPONSE"

# 2. Run analysis
RESPONSE=$(curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Customer feedback from recent call",
    "customer_id": "acme-corp",
    "analysis_type": "comprehensive"
  }')
echo "Analysis: $RESPONSE"

# 3. Search knowledge base
curl -s -X POST http://localhost:8000/api/knowledge/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main issues?",
    "customer_id": "acme-corp"
  }'
```