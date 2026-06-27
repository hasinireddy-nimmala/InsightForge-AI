"""Embedding service using sentence-transformers."""
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Singleton embedding service using sentence-transformers."""
    _instance = None
    _model = None
    _model_name = None

    def __new__(cls, model_name: str = "all-MiniLM-L6-v2"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._model_name = model_name
        return cls._instance

    def _load_model(self):
        if self._model is None:
            logger.info(f"Loading embedding model: {self._model_name}")
            self._model = SentenceTransformer(self._model_name)
            logger.info("Embedding model loaded successfully")

    def encode(self, texts: list[str]) -> np.ndarray:
        """Encode texts to embeddings. Returns (N, 384) numpy array."""
        self._load_model()
        embeddings = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.array(embeddings, dtype=np.float32)

    @property
    def dimension(self) -> int:
        return 384
