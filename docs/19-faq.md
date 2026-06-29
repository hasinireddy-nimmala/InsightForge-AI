# ❓ Frequently Asked Questions

## General

### What is InsightForge AI?

InsightForge AI is an **agentic intelligence platform** that transforms raw customer signals (meeting notes, CRM data, support tickets) into audited, actionable business recommendations using a 7-agent LangGraph pipeline powered by Google's Gemini 2.5 Flash.

### Who should use InsightForge AI?

- **Customer Success Teams** — Identify at-risk accounts and plan interventions
- **Account Executives** — Prioritize time and resources on high-opportunity accounts
- **Customer Support** — Understand sentiment trends and escalation patterns
- **Product Teams** — Surface feature requests and pain points
- **Finance/Revenue Ops** — Quantify revenue at risk and forecast churn

### What's the cost?

InsightForge AI is **open source** (MIT license). You only pay for:
- Google Gemini API (free tier available, pay-as-you-go after)
- Server hosting (if deploying to cloud)
- Embedding costs (minimal, ~$0.01 per 1M tokens)

### Can I use this without API keys?

Yes! Demo mode includes sample data so you can explore without credentials. For production use, you'll need a Google Gemini API key (free tier available).

---

## Getting Started

### How long does setup take?

**Local Setup**: 5 minutes  
**Docker Setup**: 2 minutes

See [Quick Start Guide](./01-quick-start.md).

### What are the system requirements?

**Minimum**:
- Python 3.11+ (or Docker)
- 4GB RAM
- 2GB disk space

**Recommended** (Production):
- Ubuntu 22.04 LTS
- Python 3.11.x
- 16GB RAM
- 20GB SSD
- 4+ CPU cores

### Can I run this on Windows?

Yes, via:
1. **WSL 2** (Windows Subsystem for Linux 2)
2. **Docker Desktop**
3. **Native Python** (with Windows bash alternatives)

See [Installation Guide](./02-installation.md).

---

## Architecture & Design

### Why 7 agents?

Each agent has a specific responsibility:
1. **Planner** — Routing and analysis planning
2. **Sentiment Analyst** — Emotional tone and frustration signals
3. **Risk Assessor** — Churn probability and revenue impact
4. **Trend Detector** — Pattern recognition and forecasting
5. **RAG Retriever** — Context enrichment from history
6. **Action Generator** — Strategic recommendations
7. **Auditor** — Quality assurance and consistency

Specialization improves accuracy and allows parallel processing.

### How does RAG work?

RAG (Retrieval-Augmented Generation) enriches analysis by:
1. Converting queries to embeddings (Sentence-Transformers)
2. Searching FAISS vector store for similar documents
3. Passing relevant context to agents
4. Improving recommendations with historical context

### Can I add custom agents?

Yes! See [Development Guide](./14-development-setup.md) for extending the pipeline.

---

## Performance & Scalability

### How fast is analysis?

**End-to-end**: 8-10 seconds for comprehensive analysis

Breakdown:
- Planner: 300-400ms
- Sentiment: 1.5-2s
- Risk: 1.8-2s
- Trend: 0.8-1s
- RAG: 0.5-0.8s
- Actions: 1.5-2s
- Audit: 0.8-1s

### How many documents can the knowledge base hold?

With default FAISS configuration: **100,000+ documents**

For larger scale:
- Use hierarchical clustering (IVF with subquantizers)
- Implement document sharding by customer
- Consider managed vector DB (Pinecone, Weaviate)

See [Scaling Guide](./13-scaling-guide.md).

### Can it handle concurrent requests?

Yes! The async FastAPI backend supports hundreds of concurrent requests. For production, use:
- Gunicorn with multiple workers
- Load balancing (nginx, HAProxy)
- Task queueing (Celery, RQ)

---

## Data & Privacy

### Where is data stored?

- **Analysis results**: SQLite (local `data/db/`)
- **Vector embeddings**: FAISS (local `data/faiss/`)
- **Uploaded documents**: Disk (local `data/uploads/`)
- **LLM inference**: Sent to Google Gemini API

### Is data encrypted?

**Currently**: No encryption at rest or in transit

**For production**, implement:
- TLS/SSL for API communication
- Encryption at rest (AES-256)
- Encrypted database backups

See [Production Checklist](./11-production-checklist.md#security).

### Can I run this on-premise?

Yes! Fully self-contained except for Gemini API calls. To minimize cloud calls:
- Use open-source LLM (Llama 2, Mistral)
- Replace with local embedding models
- See [Development Guide](./14-development-setup.md#using-local-llms).

### GDPR/Data Residency?

Google Gemini may store queries temporarily. For compliance:
- Use Gemini's "not stored" feature if available
- Implement data masking before sending to API
- Use on-premise LLMs for sensitive data
- Consult legal/security teams

---

## Troubleshooting

### Why is analysis slow?

1. **API latency** — Google Gemini experiencing delays
2. **RAG retrieval** — Disable with `include_rag_context=false`
3. **System resources** — Monitor CPU/RAM with `top`
4. **Network** — Check internet connection speed

### Why are analysis results inconsistent?

LLM outputs include randomness. To improve consistency:
- Lower temperature: `temperature=0.1` (more deterministic)
- Increase in auditor agent review
- Use more detailed analysis plans

### Document not showing in search results?

1. Verify it was uploaded: `GET /api/knowledge/stats`
2. Check FAISS index: `ls -lh data/faiss/index.faiss`
3. Try different search query (more semantic relevance)
4. Re-upload document: `POST /api/upload`

→ See [Troubleshooting Guide](./18-troubleshooting.md) for more solutions.

---

## Integration & API

### How do I integrate with my CRM?

1. **Export data** from CRM (CSV or API)
2. **Transform to text** format
3. **Upload via** `/api/upload` endpoint
4. **Get results** from `/api/analyze`
5. **Sync back** recommendations to CRM

See [Integration Guide](./08-integration-guide.md).

### Can I call this from Python?

Yes! Use the Python SDK:

```python
from insightforge import InsightForgeClient

client = InsightForgeClient(base_url="http://localhost:8000")
results = client.analyze(
    input_text="Customer feedback...",
    customer_id="acme-corp"
)
print(results.actions)
```

See [SDK Guide](./09-sdk-guide.md).

### What APIs does it expose?

- `/api/upload` — Document ingestion
- `/api/analyze` — Run analysis pipeline
- `/api/analysis/{id}` — Retrieve results
- `/api/history` — List past analyses
- `/api/knowledge/search` — Semantic search
- `/api/knowledge/stats` — Knowledge base stats

Full reference: [API Documentation](./07-api-reference.md).

---

## Deployment

### How do I deploy to production?

1. **Review** [Production Checklist](./11-production-checklist.md)
2. **Security** — Add auth, CORS, rate limiting
3. **Monitoring** — Set up logging, alerting
4. **Infrastructure** — Docker, Kubernetes, or serverless
5. **Testing** — Run full test suite

### What cloud platforms are supported?

**Tested & Recommended**:
- ☁️ **AWS** — EC2, ECS, Lambda
- ☁️ **Google Cloud** — Cloud Run, Compute Engine
- ☁️ **Azure** — App Service, Container Instances
- ☁️ **DigitalOcean** — App Platform, Droplets
- 🐳 **Any Docker-compatible** platform

### How do I handle secrets/API keys?

**Development**: `.env` file  
**Production**: Use platform secrets:
- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault
- HashiCorp Vault

---

## Contributing & Development

### How can I contribute?

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/my-feature`
3. **Implement** your changes with tests
4. **Submit** pull request with description

See [Contributing Guide](./15-contributing.md).

### Can I add a custom LLM?

Yes! Replace Gemini in `backend/agents/`:

```python
# Current: Uses Google Gemini
from google.generativeai import GenerativeModel

# Custom: Use any LLM with LangChain
from langchain.llms import OpenAI, Ollama
llm = OpenAI(model="gpt-4")  # or Ollama locally
```

See [Development Guide](./14-development-setup.md).

### How do I write tests?

```python
# tests/test_agents.py
def test_sentiment_analyst():
    from backend.agents.sentiment import sentiment_analyzer
    result = sentiment_analyzer({"input_text": "I love this!"})
    assert result["sentiment"] > 0.8
```

Run: `pytest tests/ -v`

See [Testing Guide](./16-testing.md).

---

## License & Legal

### What license is this?

**MIT License** — Free to use, modify, distribute.

See [LICENSE](../LICENSE) file.

### Can I use this commercially?

Yes! MIT license permits commercial use with attribution.

### Do I need to open-source my modifications?

No, MIT allows proprietary modifications.

---

## More Questions?

💬 **No answer?** Check:
1. [Troubleshooting Guide](./18-troubleshooting.md)
2. [GitHub Issues](https://github.com/saikiranthouti/InsightForge-AI/issues)
3. Open a new issue with your question

---

*Last updated: 2026-06-29*