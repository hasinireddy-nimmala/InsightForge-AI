"""FAISS vector store with SQLite metadata persistence."""
import faiss
import numpy as np
import sqlite3
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class VectorStore:
    """Production-grade FAISS vector store with SQLite metadata."""

    def __init__(self, index_path: str, metadata_db_path: str, embedding_dim: int = 384):
        self.index_path = index_path
        self.metadata_db_path = metadata_db_path
        self.embedding_dim = embedding_dim
        self.index: Optional[faiss.IndexIDMap] = None
        self._next_id = 0
        self._init_storage()
        self.load_index()

    def _init_storage(self):
        """Initialize storage directories and metadata database."""
        os.makedirs(os.path.dirname(self.index_path) if os.path.dirname(self.index_path) else '.', exist_ok=True)
        os.makedirs(os.path.dirname(self.metadata_db_path) if os.path.dirname(self.metadata_db_path) else '.', exist_ok=True)
        conn = sqlite3.connect(self.metadata_db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS chunk_metadata (
                vector_id INTEGER PRIMARY KEY,
                document_id INTEGER,
                chunk_index INTEGER,
                chunk_text TEXT,
                page_number INTEGER DEFAULT 0,
                source_file TEXT DEFAULT '',
                start_char INTEGER DEFAULT 0,
                end_char INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        cursor = conn.execute('SELECT COALESCE(MAX(vector_id), -1) + 1 FROM chunk_metadata')
        self._next_id = cursor.fetchone()[0]
        conn.close()

    def load_index(self):
        """Load FAISS index from disk or create new one."""
        if os.path.exists(self.index_path):
            logger.info(f"Loading FAISS index from {self.index_path}")
            self.index = faiss.read_index(self.index_path)
            logger.info(f"FAISS index loaded with {self.index.ntotal} vectors")
        else:
            logger.info("Creating new FAISS index")
            base_index = faiss.IndexFlatIP(self.embedding_dim)
            self.index = faiss.IndexIDMap(base_index)

    def save_index(self):
        """Save FAISS index to disk."""
        if self.index is not None:
            os.makedirs(os.path.dirname(self.index_path) if os.path.dirname(self.index_path) else '.', exist_ok=True)
            faiss.write_index(self.index, self.index_path)
            logger.info(f"FAISS index saved with {self.index.ntotal} vectors")

    def add_documents(self, chunks: list[dict], embeddings: np.ndarray, document_id: int, source_file: str = "") -> int:
        """Add document chunks with embeddings to the index.

        Args:
            chunks: list of {text, page_number, chunk_index, start_char, end_char}
            embeddings: numpy array of shape (N, embedding_dim)
            document_id: ID of the source document
            source_file: filename of the source document

        Returns:
            Number of vectors added.
        """
        if len(chunks) == 0:
            return 0

        n = len(chunks)
        ids = np.array(range(self._next_id, self._next_id + n), dtype=np.int64)

        embeddings = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(embeddings)
        self.index.add_with_ids(embeddings, ids)

        conn = sqlite3.connect(self.metadata_db_path)
        for i, chunk in enumerate(chunks):
            conn.execute(
                'INSERT INTO chunk_metadata (vector_id, document_id, chunk_index, chunk_text, page_number, source_file, start_char, end_char) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (int(ids[i]), document_id, chunk.get('chunk_index', i), chunk.get('text', ''),
                 chunk.get('page_number', 0), source_file, chunk.get('start_char', 0), chunk.get('end_char', 0))
            )
        conn.commit()
        conn.close()

        self._next_id += n
        self.save_index()
        logger.info(f"Added {n} vectors for document {document_id}")
        return n

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> list[dict]:
        """Search for similar vectors.

        Returns:
            list of {vector_id, document_id, chunk_text, page_number, source_file, score}
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        query = query_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query)
        k = min(top_k, self.index.ntotal)
        scores, ids = self.index.search(query, k)

        results = []
        conn = sqlite3.connect(self.metadata_db_path)
        for score, vid in zip(scores[0], ids[0]):
            if vid == -1:
                continue
            cursor = conn.execute('SELECT * FROM chunk_metadata WHERE vector_id = ?', (int(vid),))
            row = cursor.fetchone()
            if row:
                results.append({
                    'vector_id': row[0], 'document_id': row[1], 'chunk_index': row[2],
                    'chunk_text': row[3], 'page_number': row[4], 'source_file': row[5],
                    'start_char': row[6], 'end_char': row[7], 'score': float(score)
                })
        conn.close()
        return results

    def delete_document(self, document_id: int):
        """Delete all vectors for a document."""
        conn = sqlite3.connect(self.metadata_db_path)
        cursor = conn.execute('SELECT vector_id FROM chunk_metadata WHERE document_id = ?', (document_id,))
        vector_ids = [row[0] for row in cursor.fetchall()]
        if vector_ids:
            id_array = np.array(vector_ids, dtype=np.int64)
            self.index.remove_ids(id_array)
            conn.execute('DELETE FROM chunk_metadata WHERE document_id = ?', (document_id,))
            conn.commit()
            self.save_index()
        conn.close()
        logger.info(f"Deleted {len(vector_ids)} vectors for document {document_id}")

    @property
    def total_vectors(self) -> int:
        return self.index.ntotal if self.index else 0
