"""Advisory marker attach + render-time invariant — OB-E2 Seam-1 α.

Owner ruling OB-E2 α (2026-07-10 · verbatim): *"Write-time attach +
render reflection walk (Seam-1)."*

Every OpportunityBriefRow carries the advisory marker attached at
Registry write time. Frontend render component reads the marker from
the sidecar payload; render-time reflection walk in the OB-G2 sub-cell
verifies no frontend render code path can strip or hide the marker.

Two protection layers:
  1. Write-time attach — enforced here.
  2. Render-time reflection walk — enforced in
     `test_ob_g2_seam1_no_strip_ast`.

Seam-1 β (contract-embed marker in frozen `OpportunityBrief_v0` field)
was NOT selected per Owner ruling; parity 31 preserved. Deferred as
future-additive path if a client-facing disclosure need emerges.
"""
from __future__ import annotations

from typing import Any, Dict


ADVISORY_MARKER_STRING = (
    "Advisory: opportunity brief — not a governed response."
)
ADVISORY_MARKER_KEY = "_advisory_marker"


def attach(brief: Dict[str, Any]) -> Dict[str, Any]:
    """Attach the advisory marker to a brief payload (non-mutating).

    Returns a NEW dict with `_advisory_marker` populated. The brief
    row's Registry write-path calls this at write time; the frontend
    render surface reads the marker from the sidecar.
    """
    out = dict(brief)
    out[ADVISORY_MARKER_KEY] = ADVISORY_MARKER_STRING
    return out


def has_marker(brief: Dict[str, Any]) -> bool:
    """Return True iff the brief carries the advisory marker."""
    return brief.get(ADVISORY_MARKER_KEY) == ADVISORY_MARKER_STRING
