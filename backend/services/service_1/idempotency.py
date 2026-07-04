"""Idempotency canonicalisation + retry-detection — Phase 5 Stage B.

Canonicalisation rule (Stage A Return 5.2):
  1. Pydantic model_dump (schema-driven).
  2. Remove idempotency_key from hash input (the key IS the retry axis).
  3. sort_keys=True; separators=(",", ":"); UTF-8.

Registry-bump reason codes landed at v2:
  * idempotency_key_reused_with_different_body
  * idempotency_key_missing
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

from contracts.objective_request_v2 import ObjectiveEntry, ObjectiveRequest_v2


def canonical_request_hash(request: ObjectiveRequest_v2) -> str:
    """SHA-256 over the canonical serialisation of the request body,
    excluding idempotency_key. Deterministic across equal bodies."""
    body: Dict[str, Any] = request.model_dump(mode="python", exclude_none=False)
    body.pop("idempotency_key", None)
    canonical_json = json.dumps(
        body, sort_keys=True, separators=(",", ":"),
        default=str, ensure_ascii=False,
    )
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def requires_idempotency_key(request: ObjectiveRequest_v2) -> bool:
    """v3 §7 bullet 6: idempotency key REQUIRED on external_request."""
    return request.entry == ObjectiveEntry.EXTERNAL_REQUEST
