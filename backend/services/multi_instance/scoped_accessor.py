"""Multi-instance scoped accessor — MC-E2 α constraint architecture.

Owner ruling 2026-07-14 (MC-E2 α): 'Constraint architecture — mandatory
instance_id field on every persistent row + Mongo accessor helper that
REFUSES to run a query without instance_id.'

Every read/write helper requires `instance_id` as positional first arg;
missing → InstanceScopeError raised at call time. Compound indexes
(instance_id, ...) are created on collection first-touch via
`ensure_instance_index()`.

Adversarial cross-instance cells (test_instance_isolation.py) verify
the constraint holds by attempting cross-scope reads and asserting
denial.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

from motor.motor_asyncio import AsyncIOMotorCollection


class InstanceScopeError(Exception):
    """Raised when a persistent accessor is called without instance_id."""


def _require(instance_id: Any) -> str:
    if not isinstance(instance_id, str) or not instance_id.strip():
        raise InstanceScopeError(
            f"instance_id required on every persistence accessor call; "
            f"got {instance_id!r}. MC-E2 α constraint architecture."
        )
    return instance_id


def _scope(instance_id: str, filter_: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Return filter_ + instance_id predicate."""
    q: Dict[str, Any] = dict(filter_ or {})
    q["instance_id"] = instance_id
    return q


async def sfind_one(
    collection: AsyncIOMotorCollection,
    instance_id: str,
    filter_: Optional[Mapping[str, Any]] = None,
    projection: Optional[Mapping[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Scoped find_one — refuses without instance_id."""
    iid = _require(instance_id)
    return await collection.find_one(_scope(iid, filter_), projection)


async def sfind(
    collection: AsyncIOMotorCollection,
    instance_id: str,
    filter_: Optional[Mapping[str, Any]] = None,
    projection: Optional[Mapping[str, Any]] = None,
    limit: int = 0,
) -> List[Dict[str, Any]]:
    """Scoped find (returns list) — refuses without instance_id."""
    iid = _require(instance_id)
    cursor = collection.find(_scope(iid, filter_), projection)
    if limit:
        cursor = cursor.limit(limit)
    return await cursor.to_list(length=limit or None)


async def sinsert_one(
    collection: AsyncIOMotorCollection,
    instance_id: str,
    doc: Dict[str, Any],
) -> Any:
    """Scoped insert_one — adds instance_id to doc if absent; refuses on empty scope."""
    iid = _require(instance_id)
    doc = dict(doc)
    doc["instance_id"] = iid
    return await collection.insert_one(doc)


async def scount_documents(
    collection: AsyncIOMotorCollection,
    instance_id: str,
    filter_: Optional[Mapping[str, Any]] = None,
) -> int:
    """Scoped count — refuses without instance_id."""
    iid = _require(instance_id)
    return await collection.count_documents(_scope(iid, filter_))


async def ensure_instance_index(
    collection: AsyncIOMotorCollection,
    additional_keys: Optional[List[str]] = None,
) -> None:
    """Ensure compound index (instance_id, additional_keys...) exists on the collection."""
    keys = [("instance_id", 1)]
    if additional_keys:
        keys.extend((k, 1) for k in additional_keys)
    await collection.create_index(keys, name="instance_id_compound")
