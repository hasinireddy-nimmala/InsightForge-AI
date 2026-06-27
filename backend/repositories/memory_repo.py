"""Repository for memory and feedback CRUD operations."""
import aiosqlite
import logging

logger = logging.getLogger(__name__)


async def save_memory(
    db: aiosqlite.Connection,
    customer_id: str,
    recommendation: str,
    approved: bool,
    outcome: str = "",
    confidence_delta: float = 0.0
) -> int:
    """Save a memory entry and return its ID."""
    cursor = await db.execute(
        'INSERT INTO memory (customer_id, recommendation, approved, outcome, confidence_delta) VALUES (?, ?, ?, ?, ?)',
        (customer_id, recommendation, int(approved), outcome, confidence_delta)
    )
    await db.commit()
    mem_id = cursor.lastrowid
    logger.info(f"Saved memory: {recommendation[:50]}... (id={mem_id})")
    return mem_id


async def get_customer_memory(db: aiosqlite.Connection, customer_id: str) -> list[dict]:
    """Get all memory entries for a customer."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM memory WHERE customer_id = ? ORDER BY timestamp DESC',
        (customer_id,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def get_all_memory(db: aiosqlite.Connection) -> list[dict]:
    """Get all memory entries."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('SELECT * FROM memory ORDER BY timestamp DESC')
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def save_feedback(
    db: aiosqlite.Connection,
    recommendation_id: int,
    decision: str,
    modified_action: str = "",
    reason: str = ""
) -> int:
    """Save a feedback entry and return its ID."""
    cursor = await db.execute(
        'INSERT INTO feedback (recommendation_id, decision, modified_action, reason) VALUES (?, ?, ?, ?)',
        (recommendation_id, decision, modified_action, reason)
    )
    await db.commit()
    fb_id = cursor.lastrowid
    logger.info(f"Saved feedback for recommendation id={recommendation_id}: decision={decision}")
    return fb_id


async def get_feedback_by_recommendation(db: aiosqlite.Connection, recommendation_id: int) -> list[dict]:
    """Get all feedback for a given recommendation."""
    db.row_factory = aiosqlite.Row
    cursor = await db.execute(
        'SELECT * FROM feedback WHERE recommendation_id = ? ORDER BY timestamp DESC',
        (recommendation_id,)
    )
    rows = await cursor.fetchall()
    return [dict(row) for row in rows]


async def get_memory_trends(db: aiosqlite.Connection) -> dict:
    """Compute approval rates grouped by month.
    
    Returns:
        dict with 'trends' (list of monthly stats), 'total_decisions', and 'overall_approval_rate'.
    """
    db.row_factory = aiosqlite.Row
    cursor = await db.execute('''
        SELECT 
            strftime('%Y-%m', timestamp) as period,
            COUNT(*) as total_recommendations,
            SUM(CASE WHEN approved = 1 THEN 1 ELSE 0 END) as approved,
            SUM(CASE WHEN approved = 0 THEN 1 ELSE 0 END) as rejected
        FROM memory
        GROUP BY strftime('%Y-%m', timestamp)
        ORDER BY period DESC
    ''')
    rows = await cursor.fetchall()

    trends = []
    total_decisions = 0
    total_approved = 0

    for row in rows:
        row_dict = dict(row)
        total = row_dict['total_recommendations']
        approved = row_dict['approved']
        rejected = row_dict['rejected']
        approval_rate = (approved / total * 100.0) if total > 0 else 0.0

        trends.append({
            'period': row_dict['period'],
            'total_recommendations': total,
            'approved': approved,
            'rejected': rejected,
            'approval_rate': round(approval_rate, 1)
        })

        total_decisions += total
        total_approved += approved

    overall_approval_rate = (total_approved / total_decisions * 100.0) if total_decisions > 0 else 0.0

    return {
        'trends': trends,
        'total_decisions': total_decisions,
        'overall_approval_rate': round(overall_approval_rate, 1)
    }
