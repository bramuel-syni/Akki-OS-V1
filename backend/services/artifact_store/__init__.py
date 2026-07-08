"""Artifact Store service package — BCR §3.2 V3 last mile.

Landing per Owner rulings AS-E1..AS-E4 (2026-07-08) under the 3-tier
governance model (`docs/governance/tiered_ruling_model.md`).

Three-op adapter seam (AS-I1) with dev-tier local filesystem backing.
Provider swaps as config when [OWNER: object-store choice] fact arrives;
call sites (`adapter.put_once` / `adapter.get` / `adapter.head`) never change.
"""
from .adapter import (
    ArtifactStoreAdapter,
    PutOnceResult,
    HeadResult,
    ArtifactKeyExistsError,
    build_key,
)
from .atomic_write import atomic_put_with_receipt, reconcile_incomplete_write
from .orphan_scan import scan_orphans

__all__ = [
    "ArtifactStoreAdapter",
    "PutOnceResult",
    "HeadResult",
    "ArtifactKeyExistsError",
    "build_key",
    "atomic_put_with_receipt",
    "reconcile_incomplete_write",
    "scan_orphans",
]
