#!/bin/bash
echo "Starting InsightForge AI..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
sleep 3
streamlit run frontend/app.py --server.port 8501 --server.headless true --server.address 0.0.0.0
