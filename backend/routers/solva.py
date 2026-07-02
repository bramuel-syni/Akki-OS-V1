"""Solva API surface — enforcement + trace read.

Source: `docs/mandates/RMS_Solva_Specification.md` §7 module layout —
`routers/solva.py # enforcement + trace read surfaces`.

Read-side: `GET /api/solva/trace/{trace_id}` returns the SolvaTrace-shaped
`stamp_audit` blob from the Northena Ledger for the given trace_id.
Write-side is via the pipeline (`services.solva_depth.pipeline.run_solva`)
which absorbs its output into the Ledger via
`services.northena.converge.absorb_solva_trace` (converge.py owns the
stage="converge" writes per N-INV-6).
"""
from typing import Any, Dict, List

from fastapi import APIRouter

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db

router = APIRouter(prefix="/solva", tags=["solva"])


@router.get("/status")
async def status() -> Dict[str, Any]:
    return {
        "gate": "G3",
        "reasoning_stages": ["frame", "candidate", "tension", "probability", "reflection"],
        "note": "Solva reshape at G3. Assertion boundary is the guard.",
    }


@router.get("/trace/{trace_id}")
async def get_trace(trace_id: str) -> List[Dict[str, Any]]:
    """Return SolvaTrace-shaped `stamp_audit` blobs for this trace_id.

    Solva writes to the Ledger's `stamp_audit` field (spec §13). This
    endpoint reads the field back, oldest first. Empty list if the
    trace_id is unknown (honest empty answer, HTTP 200 []).
    """
    cursor = db[NORTHENA_LEDGER_COLLECTION].find(
        {"trace_id": trace_id, "stage": "converge"}, {"_id": 0}
    ).sort("at", 1)
    out: List[Dict[str, Any]] = []
    async for row in cursor:
        sa = row.get("stamp_audit")
        if isinstance(sa, dict):
            out.append(sa)
    return out
