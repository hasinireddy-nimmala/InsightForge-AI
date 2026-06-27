"""Basic health check test."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import():
    """Test that core modules can be imported."""
    from backend.config import settings
    assert settings.EMBEDDING_DIM == 384
    assert settings.LLM_MODEL == "gemini-2.5-flash"

def test_schemas():
    """Test that schemas can be instantiated."""
    from backend.models.schemas import HealthResponse, AnalysisRequest
    health = HealthResponse()
    assert health.status == "healthy"
    req = AnalysisRequest(input_text="test")
    assert req.customer_id == "default"
