# 🐛 Troubleshooting Guide

Common issues and solutions.

---

## Installation Issues

### Python Not Found

**Problem**: `python3.11: command not found`

**Solution**:
1. Install Python 3.11+ from [python.org](https://python.org)
2. Verify installation: `python3 --version`
3. Or use your system package manager:
   ```bash
   # macOS (Homebrew)
   brew install python@3.11
   
   # Ubuntu/Debian
   sudo apt install python3.11 python3.11-venv
   
   # Windows: Download from python.org and add to PATH
   ```

---

### Pip Install Failures

**Problem**: `ERROR: Could not find a version that satisfies the requirement...`

**Solution**:
```bash
# 1. Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# 2. Clear pip cache
pip cache purge

# 3. Install with verbose output to debug
pip install -vvv -r requirements.txt

# 4. If specific package fails, try installing it individually
pip install langraph==0.2.50 --no-cache-dir
```

---

### Virtual Environment Not Activating

**Problem**: Imports still fail after activating venv

**Solution**:
```bash
# Verify venv is activated (should show (venv) in prompt)
# Recreate venv if corrupted:
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Runtime Issues

### Port Already in Use

**Problem**: `Address already in use: ('127.0.0.1', 8000)`

**Solution**:
```bash
# Option 1: Find and kill process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process (replace PID with actual process id)
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Option 2: Use different port
uvicorn backend.main:app --port 8002
streamlit run frontend/app.py --server.port 8502
```

---

### API Key Error

**Problem**: `401 Unauthorized: Invalid API key`

**Solution**:
1. Verify `.env` file exists:
   ```bash
   cat .env | grep GOOGLE_API_KEY
   ```
2. Get free API key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
3. Update `.env`:
   ```bash
   GOOGLE_API_KEY=your_actual_key_here
   ```
4. Restart backend:
   ```bash
   # Kill old process, restart
   uvicorn backend.main:app --reload --port 8000
   ```

---

### CORS Errors

**Problem**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
Backend already has CORS configured. If issues persist:

1. Check backend logs for CORS errors
2. Verify frontend URL in `.env`:
   ```bash
   FRONTEND_URL=http://localhost:8501
   ```
3. Restart both services
4. Clear browser cache (Ctrl+Shift+Delete)

---

## API Issues

### Upload Returns 413 Payload Too Large

**Problem**: Cannot upload files larger than 25MB

**Solution**:
```python
# In backend/main.py, increase max upload size:
app = FastAPI()
app.add_middleware(
    GUnicornMiddleware,
    max_request_size=104857600  # 100MB
)
```

---

### Analysis Timeout

**Problem**: `Analysis failed: Timeout after 30 seconds`

**Solution**:
```bash
# 1. Check LLM provider status
curl https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY

# 2. Increase timeout in request:
curl -X POST http://localhost:8000/api/analyze \
  -d '{
    "input_text": "...",
    "timeout_seconds": 60
  }'

# 3. Check system resources
df -h  # Disk space
free -h  # RAM (Linux)
vm_stat  # RAM (macOS)
```

---

### Vector DB Issues

**Problem**: `Error: Cannot initialize FAISS index`

**Solution**:
```bash
# 1. Verify FAISS data directory exists
mkdir -p data/faiss

# 2. Delete corrupted index and reinitialize
rm -rf data/faiss/*

# 3. Upload a document to recreate index
curl -X POST http://localhost:8000/api/upload \
  -F "file=@data/demo/sample_meeting_notes.txt"

# 4. Check permissions
ls -la data/faiss/
chmod 755 data/faiss/
```

---

## Docker Issues

### Docker Build Fails

**Problem**: `ERROR: failed to solve with frontend dockerfile.v0`

**Solution**:
```bash
# 1. Clear Docker cache
docker system prune -a

# 2. Rebuild with no cache
docker build --no-cache -t insightforge-ai:latest .

# 3. Check available disk space
docker system df

# 4. If still failing, check Dockerfile syntax
docker build --progress=plain -t insightforge-ai:latest . 2>&1 | head -50
```

---

### Container Crashes on Start

**Problem**: `docker-compose up` exits immediately

**Solution**:
```bash
# 1. View logs
docker-compose logs -f

# 2. Check for missing .env
ls -la .env

# 3. Manually run container to see error
docker run -it --env-file .env insightforge-ai:latest

# 4. Verify GOOGLE_API_KEY is set
echo $GOOGLE_API_KEY
```

---

### Port Binding Failed

**Problem**: `bind: address already in use`

**Solution**:
```bash
# Kill process using port
lsof -i :8000  # Find process
kill -9 <PID>

# Or use different port in docker-compose.yml:
# ports:
#   - "8002:8000"  # Changed from 8000:8000

# Restart
docker-compose down
docker-compose up
```

---

## Performance Issues

### Slow Analysis (~30+ seconds)

**Solution**:
1. **Reduce RAG retrieval**: `include_rag_context=false`
2. **Use quick analysis**: `analysis_type=quick`
3. **Check system resources**:
   ```bash
   top  # Linux/macOS
   Task Manager  # Windows
   ```
4. **Monitor LLM API latency**:
   ```bash
   # Check Google Cloud logs
   gcloud logging read "resource.type=api" --limit 10
   ```

---

### High Memory Usage

**Problem**: RAM usage grows over time

**Solution**:
1. **Clear old analyses**:
   ```bash
   # Delete old database entries (be careful!)
   sqlite3 data/db/insightforge.db "DELETE FROM analyses WHERE created_at < datetime('now', '-30 days');"
   ```
2. **Restart services** periodically
3. **Monitor memory**:
   ```bash
   # Linux
   watch -n 1 'free -h'
   
   # macOS
   top -o MEM
   ```
4. **Increase Docker memory limit**:
   ```yaml
   # docker-compose.yml
   services:
     backend:
       mem_limit: 2g  # Was 1g
   ```

---

## Knowledge Base Issues

### Documents Not Searchable

**Problem**: Search returns no results

**Solution**:
1. **Verify documents were indexed**:
   ```bash
   curl http://localhost:8000/api/knowledge/stats
   ```
2. **Check vector index**:
   ```bash
   ls -lh data/faiss/
   ```
3. **Re-upload document**:
   ```bash
   rm -rf data/faiss/*
   curl -X POST http://localhost:8000/api/upload \
     -F "file=@document.txt"
   ```

---

## Database Issues

### SQLite "Database Locked"

**Problem**: `sqlite3.OperationalError: database is locked`

**Solution**:
```bash
# 1. Check if another process has lock
lsof data/db/insightforge.db

# 2. Remove lock file
rm data/db/insightforge.db-wal
rm data/db/insightforge.db-shm

# 3. Restart backend
uvicorn backend.main:app --reload --port 8000
```

---

## Getting Help

1. **Check logs**:
   ```bash
   # Backend logs
   tail -f logs/backend.log
   
   # Docker logs
   docker-compose logs -f backend
   ```

2. **Enable debug logging**:
   ```bash
   # In .env
   LOG_LEVEL=DEBUG
   ```

3. **Gather diagnostics**:
   ```bash
   python -V  # Python version
   pip list | grep -E "fastapi|streamlit|langgraph"
   docker --version
   docker-compose --version
   ```

4. **Open GitHub Issue** with:
   - Error message and stack trace
   - Your `.env` (without API keys)
   - Output from diagnostics above
   - Steps to reproduce

---

## Next Steps

- ❓ [FAQ](./19-faq.md)
- ⚙️ [Environment Configuration](./03-environment-config.md)
- 🚀 [Production Checklist](./11-production-checklist.md)