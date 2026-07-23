"""A2.3 · Canonical→occurrence trace walkability (FACT · PROM-S3-audit-trail-immutable).

FENCE 1 (Owner E1 α · 2026-07-15 · load-bearing):
  Single code path. No `if modality == "occurrence"` branch. No `if source_type
  == "structured"` branch. One resolver, parameterized on locator keys.

Resolver signature: takes a NormalizedUnit; parses its ProvenanceRing.locator dict
via a shared locator-key extractor; returns the canonical-audio pointer. Works
identically for base audio units (t_start_ms, t_end_ms only) and for occurrence
units (t_start_ms, t_end_ms, canonical_id, station, timestamp_ms, batch_lineage).

The `canonical_id` key IS the canonical pointer for occurrence units. For base
audio units without a `canonical_id`, the resolver falls back to the source_ref
as the canonical pointer. This is NOT a branch on modality — it is a
parameterized-key lookup with a documented default fallback.

`PROM-S3-audit-trail-immutable`: audit-walk cell exercises this resolver on
real occurrence units end-to-end. See tests/test_a2_end_to_end_audit_walk.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from contracts.five_rings import NormalizedUnit


# Shared locator-key extractor. Not modality-branched.
# Base audio units carry {t_start_ms, t_end_ms}; occurrence units additively carry
# {canonical_id, station, timestamp_ms, batch_lineage}. Both flow through the
# same key lookup — the extractor doesn't know or care what "kind" of audio unit
# this is; it only knows the locator vocabulary.
CANONICAL_POINTER_KEYS = ("canonical_id",)  # if present, direct canonical pointer
FALLBACK_POINTER_KEYS = ("source_ref",)     # otherwise, ProvenanceRing.source_ref is the canonical


@dataclass(frozen=True)
class CanonicalPointer:
    """Resolved canonical-artifact pointer for a NormalizedUnit."""
    canonical_pointer: str
    t_start_ms: int
    t_end_ms: int
    lineage_chain: List[str]  # batch_lineage if present, else empty


def _extract_from_locator(locator: Dict[str, Any], key: str) -> Optional[Any]:
    """Shared locator-key extractor. Modality-agnostic."""
    return locator.get(key) if isinstance(locator, dict) else None


def resolve_canonical_pointer(unit: NormalizedUnit) -> CanonicalPointer:
    """Resolve a unit's canonical-artifact pointer via ONE code path (FENCE 1).

    Deterministic mapping:
    - canonical_pointer = locator["canonical_id"] IF present, ELSE source_ref
    - t_start_ms       = locator["t_start_ms"] (default 0)
    - t_end_ms         = locator["t_end_ms"]   (default 0)
    - lineage_chain    = locator["batch_lineage"] (default [])

    No branch on `modality`. No branch on `source_type`. No branch on
    presence-of-occurrence-keys — presence is a plain dict.get() with a
    documented default. Same call site for base audio and occurrence units.
    """
    locator = unit.provenance.locator or {}
    canonical_from_locator = _extract_from_locator(locator, "canonical_id")
    canonical_from_source = unit.provenance.source_ref
    # Deterministic OR-else pick — canonical_id takes precedence when present.
    canonical_pointer = canonical_from_locator or canonical_from_source
    t_start_ms = int(_extract_from_locator(locator, "t_start_ms") or 0)
    t_end_ms = int(_extract_from_locator(locator, "t_end_ms") or 0)
    lineage_raw = _extract_from_locator(locator, "batch_lineage") or []
    lineage_chain = list(lineage_raw) if isinstance(lineage_raw, (list, tuple)) else []
    return CanonicalPointer(
        canonical_pointer=str(canonical_pointer),
        t_start_ms=t_start_ms,
        t_end_ms=t_end_ms,
        lineage_chain=lineage_chain,
    )


def walk_canonical_lineage(units: List[NormalizedUnit]) -> List[CanonicalPointer]:
    """Batch-resolve canonical pointers for a list of units.

    Uses the same single code path for every unit — batch-level FENCE 1 attest.
    """
    return [resolve_canonical_pointer(u) for u in units]
