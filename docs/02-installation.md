# 📥 Installation Guide

Detailed installation instructions for all platforms.

## System Requirements

### Minimum
- **OS**: macOS 10.14+, Ubuntu 18.04+, Windows 10+
- **Python**: 3.11 or higher
- **RAM**: 4GB (8GB recommended)
- **Disk**: 2GB free space

### Recommended (Production)
- **OS**: Ubuntu 22.04 LTS
- **Python**: 3.11.x
- **RAM**: 16GB
- **Disk**: 20GB SSD
- **CPU**: 4+ cores

---

## Option 1: Local Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/saikiranthouti/InsightForge-AI.git
cd InsightForge-AI
```

### Step 2: Create Virtual Environment

**macOS/Linux:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install requirements
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import streamlit; import fastapi; import langgraph; print('✅ All dependencies installed')"
```

---

## Option 2: Docker Installation

### Prerequisites
- Docker 20.10+
- Docker Compose 1.29+

### Installation

```bash
# Verify Docker installation
docker --version
docker-compose --version

# Build image
docker build -t insightforge-ai:latest .

# Run container
docker run -p 8000:8000 -p 8501:8501 --env-file .env insightforge-ai:latest
```

### Using Docker Compose

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Option 3: Development Installation

For contributing or modifying the codebase:

```bash
# Follow Option 1 steps, then:

# Install dev dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest tests/ -v
```

---

## Post-Installation Setup

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env`:
```bash
GOOGLE_API_KEY=your_api_key_here
LOG_LEVEL=INFO
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gemini-2.5-flash
```

### 3. Initialize Database

```bash
# Backend creates SQLite DB automatically on first run
# Verify:
ls -la data/db/
```

### 4. Create FAISS Index

```bash
# FAISS index is created on first document upload
# Or initialize empty:
mkdir -p data/faiss
```

---

## Verification

### Health Check

```bash
# With backend running:
curl http://localhost:8000/api/health

# Expected response:
# {"status": "healthy", "timestamp": "..."}
```

### Test Upload

```bash
# Test document ingestion
curl -X POST http://localhost:8000/api/upload \
  -F "file=@data/demo/sample_meeting_notes.txt"
```

---

## Troubleshooting Installation

| Issue | Solution |
|-------|----------|
| `python3.11: command not found` | Install Python 3.11 from python.org |
| `pip install` fails | Try `pip install --upgrade pip` first |
| Permission denied on venv/bin/activate | Run `chmod +x venv/bin/activate` |
| ModuleNotFoundError after pip install | Verify venv is activated |
| Docker build fails | Clear cache: `docker system prune -a` |

→ See [Troubleshooting Guide](./18-troubleshooting.md) for more help.

---

## Next Steps

✅ Installation complete?

- 🚀 [Quick Start Guide](./01-quick-start.md)
- ⚙️ [Environment Configuration](./03-environment-config.md)
- 📖 [Read Full README](../README.md)