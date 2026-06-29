# ⚡ Quick Start Guide

Get InsightForge AI running in 5 minutes.

## Prerequisites

- **Python 3.11+** (or Docker)
- **Google Gemini API Key** (free tier available at [aistudio.google.com/apikey](https://aistudio.google.com/apikey))
- **Git**

---

## Local Setup (3 minutes)

```bash
# 1. Clone and enter directory
git clone https://github.com/saikiranthouti/InsightForge-AI.git
cd InsightForge-AI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 5. Start services (two terminals)
# Terminal 1:
uvicorn backend.main:app --reload --port 8000

# Terminal 2:
streamlit run frontend/app.py --server.port 8501
```

### Access the Application

| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:8501 |
| **API Docs** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/api/health |

---

## Docker Setup (2 minutes)

```bash
# 1. Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 2. Start all services
docker-compose up --build
```

> Dashboard and API will be available after ~30 seconds

---

## Demo Mode (No API Key Needed)

1. Open http://localhost:8501
2. Navigate to **📄 Upload & Ingest**
3. Upload sample files from `data/demo/`:
   - `sample_meeting_notes.txt`
   - `sample_crm_export.csv`
   - `sample_support_tickets.txt`
4. Run **Analyze** to see the pipeline in action

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Run `pip install -r requirements.txt` |
| Port 8000/8501 in use | Change port: `--port 8002` |
| API key error | Check `.env` file and GOOGLE_API_KEY value |
| Docker build fails | Run `docker system prune -a` then retry |

→ For more help, see [Troubleshooting Guide](./18-troubleshooting.md)

---

## Next Steps

✅ Application running? Great!

- 📖 [Read the main README](../README.md)
- 🤖 [Understand the agent architecture](./04-agent-architecture.md)
- 📡 [Explore the API](./07-api-reference.md)
- 🚀 [Deploy to production](./11-production-checklist.md)