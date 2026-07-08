"""Purge attestation (V1-D1). Raw AV lives transiently worker-side; purged on job close."""
from __future__ import annotations

from datetime import datetime, timezone

from contracts.perception_result_v0 import PurgeAttestation


def attest_purge() -> PurgeAttestation:
    """Build a purge attestation stamped with UTC now."""
    return PurgeAttestation(purged=True, purged_at=datetime.now(timezone.utc).isoformat())
