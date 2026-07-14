"""v0-paths byte-identical after Phase 4a — Condition B4.

Gate 10 — SHA-identity on the FIVE files enumerated by the Phase 4a
dispatch:
  * `contracts/objective_request.py`   (v0 objective contract)
  * `services/service_1/service.py`    (v0 composition orchestrator)
  * `contracts/service_1_refusal.py`   (14th frozen contract, A2)
  * `contracts/admission_refusal.py`   (17th frozen contract, Phase 3)
  * `services/outer_gate/transform.py` (Condition B3)
  * `services/outer_gate/mint.py`      (Condition B3)
  * `services/outer_gate/receipt.py`   (Condition B3)

Pre-Phase-4a SHA-256s were captured at Phase 4a dispatch time
(2026-07-03). If a future phase legitimately lifts one of these files
(owner ruling), update the SHA constant IN THIS FILE and document the
ruling — DO NOT bump SHAs to make a failing test pass.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# Pre-Phase-4a canonical SHA-256s.
PRE_PHASE_4A_SHA = {
    "contracts/objective_request.py": (
        "2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1"
    ),
    "services/service_1/service.py": (
        # Phase 8 Seam 3 Sub-stage 1 (2026-07-07): Owner Amendment F +
        # R-1..R-6 authorised additive wire-up of I1–I3 refusal-terminal
        # emission sites via emit_refusal_ledger_row. See rulings §10.
        "4a453e30a05f3d840ac7ff54d4a387db6f6f7252ad70358edcd1a9b5299c17f8"
    ),
    "contracts/service_1_refusal.py": (
        "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022"
    ),
    "contracts/admission_refusal.py": (
        "e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f"
    ),
    "services/outer_gate/transform.py": (
        # Fixture Refresh 2026-07-10 · FR-E2 α re-bless: distributed
        # `_FEED_ID_BUCKET` DELETED (not shadowed); feed_id generalisation
        # now reads from centralized `license_classes.v1.json`. Owner
        # ruling authorises the SHA update per FR-E2 α condition 2.
        # See /app/docs/close_reports/fixture_refresh.md §Rebless-Log.
        "bb8ec05d1e24fefe42c437e73c66a803c1ab3b712bdd983ffe5a44181c95228b"
    ),
    "services/outer_gate/mint.py": (
        # Multi-Instance Capability MC-E6 β cutover (2026-07-14): env
        # var `RMS_G6_MINT_KEY_TEST_OVERRIDE` renamed to
        # `AKKI_G6_MINT_KEY_TEST_OVERRIDE` per Owner ruling
        # (docs/rulings/mc_e1_to_e6_2026-07-14.md). Hard cutover
        # authorized on evidence: no non-fixture external integrators
        # exist (STEP 1 guard result: AUTHORIZED). SHA update per
        # precedent set at Owner Amendment F (line 32-37 above) and
        # FR-E2 α re-bless (line 45-49 above).
        "b1060035cd0926b80ea39dc94b8cd3c3352f35ef2d6013f10e99d4411d360fdb"
    ),
    "services/outer_gate/receipt.py": (
        "4591e5ff6834fc80e359a33b7ccd1faad88fa8980a62f687ad1976a0342e9348"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v0_paths_byte_identical_after_4a():
    """Condition B4 — the seven files above stay byte-identical during
    Phase 4a landing. Any drift is a HAZARD-STOP requiring owner
    ruling before proceeding."""
    drift = []
    for rel_path, expected_sha in PRE_PHASE_4A_SHA.items():
        actual = _sha256(BACKEND_ROOT / rel_path)
        if actual != expected_sha:
            drift.append(
                f"  {rel_path}\n"
                f"    pre-4a SHA:  {expected_sha}\n"
                f"    post-4a SHA: {actual}"
            )
    assert not drift, (
        "Condition B4 violation — v0/frozen-contract paths mutated during "
        "Phase 4a landing:\n" + "\n".join(drift)
    )
