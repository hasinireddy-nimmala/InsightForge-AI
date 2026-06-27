"""Memory service for recommendation learning and feedback loops."""
import aiosqlite
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class MemoryService:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def get_customer_memory(self, customer_id: str) -> list[dict]:
        """Retrieve past recommendations and outcomes for a customer."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute(
                    'SELECT * FROM memory WHERE customer_id = ? ORDER BY timestamp DESC LIMIT 50',
                    (customer_id,)
                )
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving memory: {e}")
            return []

    async def store_recommendation(self, customer_id: str, recommendation: str, approved: bool, outcome: str = "") -> None:
        """Store a recommendation decision in memory."""
        confidence_delta = 0.05 if approved else -0.03
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT INTO memory (customer_id, recommendation, approved, outcome, confidence_delta) VALUES (?, ?, ?, ?, ?)',
                    (customer_id, recommendation, int(approved), outcome, confidence_delta)
                )
                await db.commit()
                logger.info(f"Stored memory: {recommendation[:50]}... approved={approved}")
        except Exception as e:
            logger.error(f"Error storing memory: {e}")

    async def get_confidence_adjustment(self, customer_id: str, action_type: str) -> float:
        """Calculate confidence adjustment based on past approval history."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    'SELECT confidence_delta FROM memory WHERE customer_id = ? AND recommendation LIKE ?',
                    (customer_id, f'%{action_type}%')
                )
                rows = await cursor.fetchall()
                if rows:
                    return sum(r[0] for r in rows)
                return 0.0
        except Exception as e:
            logger.error(f"Error calculating confidence adjustment: {e}")
            return 0.0

    async def get_all_memory(self) -> list[dict]:
        """Get all memory entries."""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                cursor = await db.execute('SELECT * FROM memory ORDER BY timestamp DESC')
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving all memory: {e}")
            return []
