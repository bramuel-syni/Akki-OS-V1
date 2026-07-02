"""Northena API surface — status + ledger read-side queries.

Read-side queries live here (router owns the API shape); the write path
(`record`, `absorb_stamp_audit`) lives in `services/northena/ledger.py`.

Contract-surface discipline (mandate §7.2 + G0 pattern): the `LedgerRow`
Pydantic model is declared as `response_model` on the by_run route so
`northena_ledger_row@v0` lands in `components.schemas` of the OpenAPI
document — same discipline as `NormalizedUnit`, `ObjectiveRequest`,
`FiveRings`, etc. External consumers (audit lens, DPO tooling, G5
operator console) can discover the nine-field row shape via OpenAPI.
"""
from typing import List

from fastapi import APIRouter

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION, LedgerRow
from contracts.trace_lens import TraceLensEnvelope
from core import db
from fastapi import HTTPException
from services.northena import ledger, trace_lens as trace_lens_svc

router = APIRouter(prefix="/northena", tags=["northena"])


async def _open_runs() -> List[str]:
    """Runs with no `converge` terminate row yet (N-INV-6 / §7)."""
    admits, terminated = set(), set()
    async for r in db[NORTHENA_LEDGER_COLLECTION].find(
        {"stage": "admit", "decision": "admitted"}, {"run_id": 1, "_id": 0}
    ):
        admits.add(r["run_id"])
    async for r in db[NORTHENA_LEDGER_COLLECTION].find(
        {"stage": "converge", "decision": {"$in": ["terminate_success", "terminate_budget"]}},
        {"run_id": 1, "_id": 0},
    ):
        terminated.add(r["run_id"])
    return sorted(admits - terminated)


@router.get("/status")
async def status() -> dict:
    return {
        "gate": "G2a",
        "retention_mode": ledger.retention_mode(),
        "retention_window_days": ledger.retention_window_days(),
        "open_runs_count": len(await _open_runs()),
        "note": "G2b (V1 productionisation + real material) still parked.",
    }


@router.get("/ledger/open_runs", response_model=List[str])
async def open_runs() -> List[str]:
    """Bare list of open-run UUIDs. Tester dispatch: list-shaped, not object-wrapped."""
    return await _open_runs()


@router.get("/ledger/by_run/{run_id}", response_model=List[LedgerRow])
async def by_run(run_id: str) -> List[LedgerRow]:
    """All ledger rows for a run, oldest first. Empty query is an honest
    empty answer (HTTP 200 []) — the endpoint exists, the collection just
    has no rows for that run. 404 would mean 'endpoint doesn't exist'."""
    cursor = db[NORTHENA_LEDGER_COLLECTION].find({"run_id": run_id}, {"_id": 0}).sort("at", 1)
    rows = [LedgerRow(**r) async for r in cursor]
    return rows


@router.get("/trace/{trace_id}", response_model=TraceLensEnvelope)
async def trace_lens(trace_id: str) -> TraceLensEnvelope:
    """Cross-engine trace-lens read surface (G5a).

    Realises Interface Spec §16 invariant #9: one record, seen at two
    scopes. Resolves every engine artifact under `trace_id`.

    READ-ONLY. Zero writes to any persistent store. GET-only (FastAPI
    method enforcement + `test_trace_lens_readonly.py` invariant).
    Errors: 404 (unknown trace_id), 400 (malformed).
    """
    try:
        return await trace_lens_svc.resolve_trace(trace_id)
    except trace_lens_svc.TraceLensInputError as e:
        raise HTTPException(status_code=400, detail={
            "reason": "malformed_trace_id", "message": str(e),
        })
    except trace_lens_svc.TraceLensNotFound as e:
        raise HTTPException(status_code=404, detail={
            "reason": "trace_id_not_found",
            "message": str(e),
            "trace_id": trace_id,
        })
