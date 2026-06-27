"""Database initialization and connection management."""
import aiosqlite
import os
from backend.config import settings
import logging

logger = logging.getLogger(__name__)


async def init_db():
    """Initialize database and create all tables."""
    os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
    async with aiosqlite.connect(settings.DB_PATH) as db:
        await db.executescript('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_path TEXT NOT NULL,
                upload_time TEXT DEFAULT (datetime('now')),
                status TEXT DEFAULT 'processed',
                chunk_count INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                content TEXT NOT NULL,
                interaction_type TEXT DEFAULT 'general',
                timestamp TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (document_id) REFERENCES documents(id)
            );
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT DEFAULT '',
                health_score REAL DEFAULT 50.0,
                last_interaction TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id TEXT NOT NULL,
                action TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority TEXT DEFAULT 'medium',
                impact TEXT DEFAULT 'medium',
                confidence REAL DEFAULT 0.5,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS agent_outputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                output_json TEXT NOT NULL,
                execution_time_ms REAL DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                approved INTEGER DEFAULT 0,
                outcome TEXT DEFAULT '',
                confidence_delta REAL DEFAULT 0.0,
                timestamp TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id INTEGER,
                decision TEXT NOT NULL,
                modified_action TEXT DEFAULT '',
                reason TEXT DEFAULT '',
                decided_by TEXT DEFAULT 'user',
                timestamp TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (recommendation_id) REFERENCES recommendations(id)
            );
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                entity_type TEXT DEFAULT '',
                entity_id TEXT DEFAULT '',
                details TEXT DEFAULT '',
                timestamp TEXT DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS vector_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                chunk_index INTEGER DEFAULT 0,
                chunk_text TEXT NOT NULL,
                page_number INTEGER DEFAULT 0,
                start_char INTEGER DEFAULT 0,
                end_char INTEGER DEFAULT 0,
                FOREIGN KEY (document_id) REFERENCES documents(id)
            );
        ''')
        await db.commit()
    logger.info("Database initialized with all tables")


async def get_db():
    """Get async database connection."""
    db = await aiosqlite.connect(settings.DB_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()
