"""Repository for audit log CRUD operations."""
import aiosqlite
import logging

logger = logging.getLogger(__name__)


async def log_action(
    db: aiosqlite.Connection,
    action: str,
    entity_type: str = "",
    entity_id: str = "",
    details: str = ""
) -> None:
    """Log an audit action."""
    await db.execute(
        'INSERT INTO audit_logs (action, entity_type, entity_id, details) VALUES (?, ?, ?, ?)',
        (action, entity_type, entity_id, details)
    )
    await db.commit()
    logger.debug(f"Audit log: action={action}, entity={entity_type}/{entity_id}")


async def get_audit_logs(db: aiosqlite.Connection, limit: int = 100) -> list[dict]:
    """Get the most recent audit log entries."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT ?',
        (limit,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def get_audit_logs_by_entity(db: aiosqlite.Connection, entity_type: str, entity_id: str) -> list[dict]:
    """Get all audit log entries for a specific entity."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM audit_logs WHERE entity_type = ? AND entity_id = ? ORDER BY timestamp DESC',
        (entity_type, entity_id)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]
