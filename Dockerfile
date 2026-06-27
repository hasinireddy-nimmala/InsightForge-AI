FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Data dirs
RUN mkdir -p data/db data/faiss data/uploads

EXPOSE 8000 8501

COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
