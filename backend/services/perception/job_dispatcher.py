"""Job dispatcher — Mongo-persisted perception job queue (V1-B1, V1-B2).

State machine per BCR §3.1:
  queued -> claimed (on worker claim)
  claimed -> running (on first result post)
  running -> complete | failed_resumable | failed_terminal

Collection: `perception_jobs`. Document shape mirrors PerceptionJob_v0
+ state fields (state, claimed_by, claimed_at, last_checkpoint_offset,
last_completed_unit_ids, purge_attestation, telemetry, status).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from core import db
from contracts.perception_job_v0 import PerceptionJob_v0
from services.perception import idempotency

COLLECTION = "perception_jobs"


async def ensure_indexes() -> None:
    await db[COLLECTION].create_index("job_id", unique=True)
    await db[COLLECTION].create_index("state")
    await idempotency.ensure_indexes()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


async def enqueue_job(
    objective_ref: str,
    trace_lineage: str,
    reextraction_handles: List[str],
    modality: str,
    extraction_params_ref: str,
    idempotency_key: str,
) -> PerceptionJob_v0:
    """Mint (or return existing) PerceptionJob_v0 keyed on idempotency_key.

    V1-I1: retried dispatch of same idempotency_key returns same job.
    """
    existing_job_id = await idempotency.lookup(idempotency_key)
    if existing_job_id:
        doc = await db[COLLECTION].find_one({"job_id": existing_job_id})
        if doc:
            return _doc_to_job(doc)
    job_id = f"pj-{uuid.uuid4().hex[:12]}"
    job = PerceptionJob_v0(
        job_id=job_id,
        objective_ref=objective_ref,
        trace_lineage=trace_lineage,
        reextraction_handles=reextraction_handles,
        modality=modality,
        extraction_params_ref=extraction_params_ref,
        idempotency_key=idempotency_key,
        issued_at=_now_iso(),
    )
    doc = job.model_dump()
    doc["state"] = "queued"
    doc["claimed_by"] = None
    doc["claimed_at"] = None
    doc["last_checkpoint_offset_s"] = 0
    doc["last_completed_unit_ids"] = []
    doc["telemetry"] = None
    doc["purge_attestation"] = None
    doc["result_status"] = None
    await db[COLLECTION].insert_one(doc)
    await idempotency.record(idempotency_key, job_id)
    return job


def _doc_to_job(doc: Dict[str, Any]) -> PerceptionJob_v0:
    return PerceptionJob_v0(
        job_id=doc["job_id"],
        objective_ref=doc["objective_ref"],
        trace_lineage=doc["trace_lineage"],
        reextraction_handles=doc["reextraction_handles"],
        modality=doc["modality"],
        extraction_params_ref=doc["extraction_params_ref"],
        idempotency_key=doc["idempotency_key"],
        issued_at=doc["issued_at"],
    )


async def claim_next(worker_id: str) -> Optional[PerceptionJob_v0]:
    """Atomically transition a queued job to claimed. Returns None if no work."""
    doc = await db[COLLECTION].find_one_and_update(
        {"state": "queued"},
        {"$set": {
            "state": "claimed",
            "claimed_by": worker_id,
            "claimed_at": _now_iso(),
        }},
        return_document=True,
    )
    return _doc_to_job(doc) if doc else None


async def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    return await db[COLLECTION].find_one({"job_id": job_id})


async def apply_result(job_id: str, result_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Merge a PerceptionResult into the job document (V1-B2 checkpoint semantics).

    Idempotent on (job_id, checkpoint.last_completed_offset_s + status):
    posting the same checkpoint twice is a no-op.
    """
    doc = await db[COLLECTION].find_one({"job_id": job_id})
    if doc is None:
        return {"result": "not_found"}
    checkpoint = result_dict.get("checkpoint", {})
    incoming_offset = checkpoint.get("last_completed_offset_s", 0)
    incoming_ids = checkpoint.get("completed_unit_ids", []) or []
    stored_offset = doc.get("last_checkpoint_offset_s", 0)
    stored_ids = doc.get("last_completed_unit_ids", []) or []
    # Idempotency: same offset + same ids + same status → no-op.
    if (incoming_offset == stored_offset
            and incoming_ids == stored_ids
            and doc.get("result_status") == result_dict.get("status")):
        return {"result": "idempotent_replay", "job_id": job_id}
    # Advance checkpoint (unit-level; V1-B2 no duplicate rows).
    new_ids = list(dict.fromkeys(stored_ids + incoming_ids))
    new_state = "complete" if result_dict.get("status") == "complete" else "running"
    await db[COLLECTION].update_one(
        {"job_id": job_id},
        {"$set": {
            "state": new_state,
            "last_checkpoint_offset_s": max(stored_offset, incoming_offset),
            "last_completed_unit_ids": new_ids,
            "telemetry": result_dict.get("telemetry"),
            "purge_attestation": result_dict.get("purge_attestation"),
            "result_status": result_dict.get("status"),
        }},
    )
    return {"result": "applied", "job_id": job_id}
