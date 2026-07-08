"""Perception job idempotency resolver (V1-I1).

Retried dispatch of the same idempotency_key returns the SAME job,
never a second. Persisted in Mongo as `perception_idempotency`:
document shape `{idempotency_key, job_id, created_at}` with a unique
index on `idempotency_key`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from core import db

COLLECTION = "perception_idempotency"


async def ensure_indexes() -> None:
    await db[COLLECTION].create_index("idempotency_key", unique=True)


async def lookup(idempotency_key: str) -> Optional[str]:
    """Return an existing job_id for this key, or None."""
    doc = await db[COLLECTION].find_one({"idempotency_key": idempotency_key})
    return doc.get("job_id") if doc else None


async def record(idempotency_key: str, job_id: str) -> None:
    """Persist the (key -> job_id) mapping. Idempotent on unique index."""
    await db[COLLECTION].update_one(
        {"idempotency_key": idempotency_key},
        {"$setOnInsert": {
            "idempotency_key": idempotency_key,
            "job_id": job_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }},
        upsert=True,
    )
