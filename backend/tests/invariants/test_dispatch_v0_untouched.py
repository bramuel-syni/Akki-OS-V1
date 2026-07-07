"""v0 untouched — Phase 2 regression proof.

Owner Gate 3 (Phase 2 dispatch): existing v0 route
(`POST /api/service_1/run`) + service (`services/service_1/service.py`)
+ v0 contract (`contracts/objective_request.py`) stay byte-identical
under a Phase 2 landing.

This regression checks:

  1. `contracts/objective_request.py` SHA-256 matches the pre-Phase-2
     value recorded at `PRE_PHASE_2_V0_CONTRACT_SHA`.
     Rationale: v0 objective request must remain unchanged.

  2. `services/service_1/service.py` SHA-256 matches the pre-Phase-2
     value recorded at `PRE_PHASE_2_V0_SERVICE_SHA`.
     Rationale: no modification to the composition orchestrator.

  3. v0 route (`POST /api/service_1/run`) with a fixed refusal-triggering
     input yields an identical Service1Refusal envelope pre- and
     post-Phase-2 — same status, same discriminator, same field set,
     same reason for the deterministic path.

The SHA constants are recorded at Phase 2 dispatch time (2026-07-03)
and stay LOAD-BEARING for regression. If a future phase legitimately
lifts v0 (with owner ruling), update the SHA constant IN THIS FILE and
document the ruling.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from server import app


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# --- Pre-Phase-2 recorded SHA-256s (2026-07-03) ---
# If either changes, Gate 3 is violated. Do NOT bump these constants
# to make a failing test pass — surface the mutation to owner first.
PRE_PHASE_2_V0_CONTRACT_SHA = (
    "2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1"
)
# Phase 8 Seam 3 Sub-stage 1 (2026-07-07): Owner Amendment F + R-1..R-6
# authorised additive wire-up of the un-ledgered refusal-terminal emission
# sites I1–I3 at service.py:127 / service.py:135 / service.py:188 via
# services/compliance/refusal_ledger.py::emit_refusal_ledger_row. See
# /app/docs/rulings/seam_3_stage_a_e1_to_e7.md §10 for the six rulings.
# The pre-2 baseline SHA below is retained in the module history via git;
# the constant is refreshed to reflect the Sub-stage 1 landing.
PRE_PHASE_2_V0_SERVICE_SHA = (
    "4a453e30a05f3d840ac7ff54d4a387db6f6f7252ad70358edcd1a9b5299c17f8"
)


def _sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v0_objective_request_contract_byte_identical():
    """contracts/objective_request.py SHA-256 unchanged."""
    p = BACKEND_ROOT / "contracts" / "objective_request.py"
    actual = _sha256_of(p)
    assert actual == PRE_PHASE_2_V0_CONTRACT_SHA, (
        f"Gate 3 violation — contracts/objective_request.py mutated.\n"
        f"  pre-Phase-2 SHA: {PRE_PHASE_2_V0_CONTRACT_SHA}\n"
        f"  post-Phase-2 SHA: {actual}\n"
        f"v0 objective contract must remain byte-identical under a "
        f"Phase 2 landing. Surface to owner for ruling."
    )


def test_v0_service_1_service_byte_identical():
    """services/service_1/service.py SHA-256 unchanged."""
    p = BACKEND_ROOT / "services" / "service_1" / "service.py"
    actual = _sha256_of(p)
    assert actual == PRE_PHASE_2_V0_SERVICE_SHA, (
        f"Gate 3 violation — services/service_1/service.py mutated.\n"
        f"  pre-Phase-2 SHA: {PRE_PHASE_2_V0_SERVICE_SHA}\n"
        f"  post-Phase-2 SHA: {actual}\n"
        f"Composition orchestrator must remain byte-identical under a "
        f"Phase 2 landing (owner scope declaration: 'no modification to "
        f"service_1/service.py beyond additive imports if necessary — "
        f"and if additive imports are necessary, HAZARD-STOP and surface')."
    )


@pytest.mark.asyncio
async def test_v0_run_route_still_returns_governed_refusal_envelope():
    """v0 route deterministically refuses with the same Service1Refusal
    envelope shape it did pre-Phase-2.

    Fixed input: empty units + valid other fields → composition below
    floor (targeta_core filters everything, service raises
    Service1Refusal with reason 'composition_below_floor'). Router
    returns 422 with outcome='refused' and the seven canonical fields.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/run",
            json={
                "artifact_id": "test_artifact",
                "artifact_version": "v1",
                "lawful_basis": "test_basis",
                "floor": "utterance",
                "scope_key": "portfolio",
                "objective_text": "regression probe",
                "units": [],
            },
        )
    assert resp.status_code == 422, f"expected 422 refusal; got {resp.status_code}"
    body = resp.json()
    # Canonical field-set of Service1Refusal@v0.
    expected_fields = {
        "outcome", "reason", "run_id", "trace_id",
        "asked", "supported_class", "what_would_raise_it",
    }
    assert set(body.keys()) == expected_fields, (
        f"v0 Service1Refusal envelope field-set drift.\n"
        f"  expected: {sorted(expected_fields)}\n"
        f"  actual:   {sorted(body.keys())}"
    )
    assert body["outcome"] == "refused"
    assert body["reason"] == "composition_below_floor"
    assert body["asked"] == "regression probe"
