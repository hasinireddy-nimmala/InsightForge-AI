"""Repository for recommendation and agent output CRUD operations."""
import aiosqlite
import logging

logger = logging.getLogger(__name__)


async def save_recommendation(
    db: aiosqlite.Connection,
    analysis_id: str,
    action: str,
    description: str,
    priority: str,
    impact: str,
    confidence: float
) -> int:
    """Save a new recommendation and return its ID."""
    cursor = await db.execute(
        'INSERT INTO recommendations (analysis_id, action, description, priority, impact, confidence) VALUES (?, ?, ?, ?, ?, ?)',
        (analysis_id, action, description, priority, impact, confidence)
    )
    await db.commit()
    rec_id = cursor.lastrowid
    logger.info(f"Saved recommendation: {action[:50]}... (id={rec_id})")
    return rec_id


async def get_recommendations_by_analysis(db: aiosqlite.Connection, analysis_id: str) -> list[dict]:
    """Get all recommendations for a given analysis."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM recommendations WHERE analysis_id = ? ORDER BY created_at DESC',
        (analysis_id,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def update_recommendation_status(db: aiosqlite.Connection, rec_id: int, status: str) -> None:
    """Update the status of a recommendation."""
    await db.execute(
        'UPDATE recommendations SET status = ? WHERE id = ?',
        (status, rec_id)
    )
    await db.commit()
    logger.info(f"Updated recommendation id={rec_id}: status={status}")


async def get_recommendation(db: aiosqlite.Connection, rec_id: int) -> dict | None:
    """Get a single recommendation by ID."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('SELECT * FROM recommendations WHERE id = ?', (rec_id,))
    row = await cursor.fetchone()
    if row:
        return dict(row)
    return None


async def save_agent_output(
    db: aiosqlite.Connection,
    analysis_id: str,
    agent_name: str,
    output_json: str,
    execution_time_ms: float
) -> int:
    """Save an agent output record and return its ID."""
    cursor = await db.execute(
        'INSERT INTO agent_outputs (analysis_id, agent_name, output_json, execution_time_ms) VALUES (?, ?, ?, ?)',
        (analysis_id, agent_name, output_json, execution_time_ms)
    )
    await db.commit()
    return cursor.lastrowid


async def get_agent_outputs(db: aiosqlite.Connection, analysis_id: str) -> list[dict]:
    """Get all agent outputs for a given analysis."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM agent_outputs WHERE analysis_id = ? ORDER BY created_at ASC',
        (analysis_id,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def get_pending_recommendations(db: aiosqlite.Connection) -> list[dict]:
    """Get all recommendations with pending status."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        "SELECT * FROM recommendations WHERE status = 'pending' ORDER BY created_at DESC"
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]
