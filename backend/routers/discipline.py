"""Discipline read surface — `GET /api/discipline/lift_manifest` (G5a).

GET-only. Serves the current lift_manifest.json + live-computed source-spec
SHA-256s + Rule 2 v2 accounting.

Zero writes. Freshness guaranteed by direct-file-read on every hit.
"""
from fastapi import APIRouter

from contracts.lift_manifest_response import LiftManifestEnvelope
from services.northena import trace_lens


router = APIRouter(prefix="/discipline", tags=["discipline"])


@router.get("/lift_manifest", response_model=LiftManifestEnvelope)
async def get_lift_manifest() -> LiftManifestEnvelope:
    """Serve the current lift manifest + spec fingerprints + Rule 2 v2
    accounting. Interface Spec §16 governance-legibility (all disciplines
    surface-legible)."""
    return trace_lens.read_lift_manifest_envelope()
