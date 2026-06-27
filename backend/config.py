"""Application configuration for InsightForge AI."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    BACKEND_URL: str = "http://localhost:8000"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_DIM: int = 384
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5
    DB_PATH: str = "data/db/insightforge.db"
    FAISS_INDEX_PATH: str = "data/faiss/index.faiss"
    FAISS_METADATA_DB: str = "data/faiss/metadata.sqlite"
    UPLOAD_DIR: str = "data/uploads"
    DATA_DIR: str = "data"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
