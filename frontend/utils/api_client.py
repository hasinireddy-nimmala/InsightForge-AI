"""API client for InsightForge AI backend."""
import requests
import logging

logger = logging.getLogger(__name__)
BACKEND_URL = "http://localhost:8000"


class APIClient:
    """HTTP client for InsightForge AI FastAPI backend."""

    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url
        self.timeout = 120

    def health_check(self) -> dict:
        """Check backend health status."""
        try:
            r = requests.get(f"{self.base_url}/api/health", timeout=5)
            return r.json()
        except Exception:
            return {"status": "offline"}

    def upload_documents(self, files) -> list:
        """Upload documents to the backend."""
        try:
            file_list = [
                ("files", (f.name, f.getvalue(), f.type or "application/octet-stream"))
                for f in files
            ]
            r = requests.post(
                f"{self.base_url}/api/documents/upload",
                files=file_list,
                timeout=60,
            )
            return r.json()
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return []

    def list_documents(self) -> dict:
        """List all indexed documents."""
        try:
            r = requests.get(f"{self.base_url}/api/documents", timeout=10)
            return r.json()
        except Exception:
            return {"documents": [], "total": 0}

    def delete_document(self, doc_id: int) -> bool:
        """Delete a document by ID."""
        try:
            r = requests.delete(
                f"{self.base_url}/api/documents/{doc_id}", timeout=10
            )
            return r.status_code == 200
        except Exception:
            return False

    def run_analysis(
        self,
        input_text: str,
        customer_id: str = "default",
        document_ids: list = None,
    ) -> dict:
        """Run AI analysis pipeline."""
        try:
            r = requests.post(
                f"{self.base_url}/api/analysis/run",
                json={
                    "input_text": input_text,
                    "customer_id": customer_id,
                    "document_ids": document_ids or [],
                },
                timeout=self.timeout,
            )
            return r.json()
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {}

    def get_analysis(self, analysis_id: str) -> dict:
        """Retrieve analysis results."""
        try:
            r = requests.get(
                f"{self.base_url}/api/analysis/{analysis_id}", timeout=10
            )
            return r.json()
        except Exception:
            return {}

    def get_timeline(self, analysis_id: str) -> dict:
        """Retrieve agent execution timeline."""
        try:
            r = requests.get(
                f"{self.base_url}/api/analysis/{analysis_id}/timeline", timeout=10
            )
            return r.json()
        except Exception:
            return {"timeline": []}

    def get_recommendations(self, analysis_id: str) -> dict:
        """Get recommendations for an analysis."""
        try:
            r = requests.get(
                f"{self.base_url}/api/recommendations/{analysis_id}", timeout=10
            )
            return r.json()
        except Exception:
            return {"recommendations": [], "total": 0}

    def get_pending_recommendations(self) -> dict:
        """Get all pending recommendations."""
        try:
            r = requests.get(
                f"{self.base_url}/api/recommendations/pending/all", timeout=10
            )
            return r.json()
        except Exception:
            return {"recommendations": [], "total": 0}

    def approve_recommendation(self, rec_id: int, reason: str = "") -> dict:
        """Approve a recommendation."""
        try:
            r = requests.post(
                f"{self.base_url}/api/recommendations/{rec_id}/approve",
                json={"reason": reason},
                timeout=10,
            )
            return r.json()
        except Exception:
            return {}

    def reject_recommendation(self, rec_id: int, reason: str = "") -> dict:
        """Reject a recommendation."""
        try:
            r = requests.post(
                f"{self.base_url}/api/recommendations/{rec_id}/reject",
                json={"reason": reason},
                timeout=10,
            )
            return r.json()
        except Exception:
            return {}

    def modify_recommendation(
        self, rec_id: int, modified_action: str, reason: str = ""
    ) -> dict:
        """Modify a recommendation."""
        try:
            r = requests.post(
                f"{self.base_url}/api/recommendations/{rec_id}/modify",
                json={"modified_action": modified_action, "reason": reason},
                timeout=10,
            )
            return r.json()
        except Exception:
            return {}

    def get_memory(self) -> dict:
        """Get all memory entries."""
        try:
            r = requests.get(f"{self.base_url}/api/memory", timeout=10)
            return r.json()
        except Exception:
            return {"entries": [], "total": 0}

    def get_customer_memory(self, customer_id: str) -> dict:
        """Get memory entries for a specific customer."""
        try:
            r = requests.get(
                f"{self.base_url}/api/memory/customer/{customer_id}", timeout=10
            )
            return r.json()
        except Exception:
            return {"entries": [], "total": 0}

    def get_memory_trends(self) -> dict:
        """Get memory and decision trends."""
        try:
            r = requests.get(f"{self.base_url}/api/memory/trends", timeout=10)
            return r.json()
        except Exception:
            return {
                "trends": [],
                "total_decisions": 0,
                "overall_approval_rate": 0.0,
            }
