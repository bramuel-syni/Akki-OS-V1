"""SM-E1..E3 sample lifecycle (BCR §3.12 verbatim).

Sample = narrow-reach objective (SM-E1). Sample cost draws objective budget
and is shown doing so (SM-E2). Sample units tagged `sample_of={objective_ref}`
(SM-E3) — NOT counted as committed run units (SM-G5).

Stub-first per Owner P9-E7 verbatim: SM-G1 proves against stub worker at
9.3 close; 9.3 closes independently of 9.2 GPU.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from core import db

COLLECTION = "extraction_samples"


async def ensure_indexes() -> None:
    await db[COLLECTION].create_index("sample_ref", unique=True)
    await db[COLLECTION].create_index("idempotency_key", unique=True, sparse=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _sample_lifecycle_impl_run(objective_ref: str, sample_bound_hours: float,
                                     idempotency_key: Optional[str]) -> Dict[str, Any]:
    """Shared implementation: create-or-lookup sample record.

    Amortised base per Amendment I §1.3 (sample_lifecycle amortised via
    `_sample_lifecycle_impl`). Idempotent on idempotency_key when present.
    """
    if idempotency_key:
        existing = await db[COLLECTION].find_one({"idempotency_key": idempotency_key})
        if existing:
            return _project(existing)
    sample_ref = f"sample-{uuid.uuid4().hex[:12]}"
    doc = {
        "sample_ref": sample_ref,
        "objective_ref": objective_ref,
        "sample_bound_hours": float(sample_bound_hours),
        "idempotency_key": idempotency_key,
        "status": "pending",
        "created_at": _now_iso(),
        # SM-E3: tag sample units with sample_of=objective_ref (Owner-binding tag).
        "sample_of": objective_ref,
        # SM-E2: GPU budget draw shown on response.
        "gpu_budget_drawn_hours": float(sample_bound_hours),
        # Stub result: deterministic pending → complete transition can be
        # advanced by the stub worker at gate-proof time.
        "result": None,
    }
    await db[COLLECTION].insert_one(doc)
    return _project(doc)


def _project(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sample_ref": doc.get("sample_ref"),
        "objective_ref": doc.get("objective_ref"),
        "status": doc.get("status", "pending"),
        "sample_of": doc.get("sample_of"),
        "gpu_budget_drawn_hours": doc.get("gpu_budget_drawn_hours", 0.0),
        "result": doc.get("result"),
        "created_at": doc.get("created_at"),
    }


async def run_sample(objective_ref: str, sample_bound_hours: float,
                     idempotency_key: Optional[str] = None) -> Dict[str, Any]:
    return await _sample_lifecycle_impl_run(objective_ref, sample_bound_hours, idempotency_key)


async def get_sample(sample_ref: str) -> Optional[Dict[str, Any]]:
    doc = await db[COLLECTION].find_one({"sample_ref": sample_ref})
    return _project(doc) if doc else None


async def stub_complete_sample(sample_ref: str) -> Dict[str, Any]:
    """Advance sample to complete with deterministic stub result (SM-G1 stub proof).

    Result renders in the SampleResultCard: volume + class distribution + per-hour cost.
    """
    result = {
        "volume_found_units": 4180,
        "class_distribution": {"recorded_statement": 0.62, "established_fact": 0.21, "opinion": 0.17},
        "per_hour_cost_gpu_hours": 0.35,
    }
    await db[COLLECTION].update_one(
        {"sample_ref": sample_ref},
        {"$set": {"status": "complete", "result": result}},
    )
    doc = await db[COLLECTION].find_one({"sample_ref": sample_ref})
    return _project(doc)
