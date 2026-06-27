"""Repository for document and interaction CRUD operations."""
import aiosqlite
import logging

logger = logging.getLogger(__name__)


async def save_document(db: aiosqlite.Connection, filename: str, file_type: str, file_path: str, chunk_count: int) -> int:
    """Save a new document record and return its ID."""
    cursor = await db.execute(
        'INSERT INTO documents (filename, file_type, file_path, chunk_count) VALUES (?, ?, ?, ?)',
        (filename, file_type, file_path, chunk_count)
    )
    await db.commit()
    doc_id = cursor.lastrowid
    logger.info(f"Saved document: {filename} (id={doc_id}, chunks={chunk_count})")
    return doc_id


async def get_document(db: aiosqlite.Connection, doc_id: int) -> dict | None:
    """Get a document by ID. Returns dict or None."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))
    row = await cursor.fetchone()
    if row:
        return dict(row)
    return None


async def list_documents(db: aiosqlite.Connection) -> list[dict]:
    """List all documents."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('SELECT * FROM documents ORDER BY upload_time DESC')
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def delete_document(db: aiosqlite.Connection, doc_id: int) -> None:
    """Delete a document and its related interactions."""
    await db.execute('DELETE FROM interactions WHERE document_id = ?', (doc_id,))
    await db.execute('DELETE FROM vector_metadata WHERE document_id = ?', (doc_id,))
    await db.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
    await db.commit()
    logger.info(f"Deleted document id={doc_id}")


async def save_interaction(db: aiosqlite.Connection, document_id: int, content: str, interaction_type: str = "general") -> int:
    """Save a new interaction record and return its ID."""
    cursor = await db.execute(
        'INSERT INTO interactions (document_id, content, interaction_type) VALUES (?, ?, ?)',
        (document_id, content, interaction_type)
    )
    await db.commit()
    return cursor.lastrowid


async def get_interactions_by_document(db: aiosqlite.Connection, document_id: int) -> list[dict]:
    """Get all interactions for a given document."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM interactions WHERE document_id = ? ORDER BY timestamp DESC',
        (document_id,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def update_document_status(db: aiosqlite.Connection, doc_id: int, status: str, chunk_count: int) -> None:
    """Update document processing status and chunk count."""
    await db.execute(
        'UPDATE documents SET status = ?, chunk_count = ? WHERE id = ?',
        (status, chunk_count, doc_id)
    )
    await db.commit()
    logger.info(f"Updated document id={doc_id}: status={status}, chunks={chunk_count}")
