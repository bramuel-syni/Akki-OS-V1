"""Source connector base interface (Owner P9-E2 α, 2026-07-08).

Per Owner P9-E2 α verbatim: "Locator stays opaque free-form, owned per-adapter."
Each adapter owns its dialect inside `ProvenanceRing.locator` (existing frozen
`Dict[str, Any]` shape). No cross-adapter registry. Round-trip governance is
proven in each connector's happy-posture Pytest cell (write locator → re-read
via connector → same source region).

Two emission paths per BCR §3.1 V1-I4:
  * `emit_perception_jobs()` — for AUDIO/VIDEO material routed to GPU workers.
  * `emit_direct_intake_units()` — for TEXT material bypassing GPU entirely.
"""
from __future__ import annotations

from typing import Any, Dict, List


class SourceConnectorAdapter:
    """Base interface. Subclasses MUST implement one emission path."""

    name: str = "base"

    def emit_perception_jobs(self, source_ref: str) -> List[Dict[str, Any]]:
        """Return list of (partial) PerceptionJob_v0 dicts for AUDIO/VIDEO material."""
        raise NotImplementedError

    def emit_direct_intake_units(self, source_ref: str) -> List[Dict[str, Any]]:
        """Return list of TEXT NormalizedUnit dicts bypassing GPU."""
        raise NotImplementedError

    def read_source_region(self, locator: Dict[str, Any]) -> Dict[str, Any]:
        """Round-trip check (P9-E2 binding): re-read source region from locator.

        Returns a canonical `{source_ref, region_signature}` dict. Two writes
        with the same source region MUST yield the same `region_signature`.
        """
        raise NotImplementedError
