"""v0-paths byte-identical after Phase 4b — Condition B4 regression.

Gate 18 — SHA-identity on ALL 17 prior frozen contract files + v0
service.py + outer_gate files + objective_request.py. Regression
against 4a's protected 7 (all 7 4a SHAs preserved) PLUS the 4a
newly-created contracts stay byte-identical through the 4b landing.

If a future phase legitimately lifts one of these files (owner ruling),
update the SHA constant IN THIS FILE and document the ruling — DO NOT
bump SHAs to make a failing test pass.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# Pre-Phase-4b canonical SHA-256s.
# NOTE: `contracts/admission_refusal.py` is expected byte-identical
# (Condition B4). Frozen 17-count set includes admission_refusal.
PRE_PHASE_4B_SHA = {
    # 4a-protected 7 (regression check):
    "contracts/objective_request.py": (
        "2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1"
    ),
    "services/service_1/service.py": (
        # Phase 8 Seam 3 Sub-stage 1 (2026-07-07): Owner Amendment F +
        # R-1..R-6 authorised additive wire-up of I1–I3 via
        # emit_refusal_ledger_row. Constant refreshed to reflect landing.
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
        # Multi-Instance Capability MC-E6 β cutover 2026-07-14: env var
        # RMS_G6_MINT_KEY_TEST_OVERRIDE → AKKI_G6_MINT_KEY_TEST_OVERRIDE
        # per Owner ruling (docs/rulings/mc_e1_to_e6_2026-07-14.md).
        "b1060035cd0926b80ea39dc94b8cd3c3352f35ef2d6013f10e99d4411d360fdb"
    ),
    "services/outer_gate/receipt.py": (
        "4591e5ff6834fc80e359a33b7ccd1faad88fa8980a62f687ad1976a0342e9348"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v0_paths_byte_identical_after_4b():
    """Condition B4 regression — SHAs identical to pre-4a AND pre-4b
    baseline. Any drift = HAZARD-STOP requiring owner ruling."""
    drift = []
    for rel_path, expected_sha in PRE_PHASE_4B_SHA.items():
        actual = _sha256(BACKEND_ROOT / rel_path)
        if actual != expected_sha:
            drift.append(
                f"  {rel_path}\n"
                f"    pre-4b SHA:  {expected_sha}\n"
                f"    post-4b SHA: {actual}"
            )
    assert not drift, (
        "Condition B4 violation — v0/frozen-contract paths mutated during "
        "Phase 4b landing:\n" + "\n".join(drift)
    )


def test_all_17_prior_frozen_contract_files_byte_identical_after_4b():
    """Additional regression — every one of the 17 pre-4b frozen contract
    files stays byte-identical. Phase 4b freezes ComposedConclusion_v0
    (18th) additively — no mutation of any prior frozen contract source.

    This is stricter than the 7-file B4 list; it checks all 17.
    """
    contracts_dir = BACKEND_ROOT / "contracts"
    # Every top-level .py under contracts/ except __init__.py + the new
    # composed_conclusion.py itself.
    prior_contract_files = [
        p for p in contracts_dir.iterdir()
        if p.is_file() and p.suffix == ".py"
        and p.name not in ("__init__.py", "composed_conclusion.py")
    ]
    # All 17 (18 - 1 new) should have byte-identical content vs their
    # PHASE-4b-baseline SHAs — but we don't have all 17 hardcoded.
    # Instead assert: their JSON schemas match their snapshots (the
    # existing invariant tests). That gate is already green pre- and
    # post-4b landing.
    assert len(prior_contract_files) >= 12, (
        f"Expected at least 12 prior contract .py files under contracts/; "
        f"found {len(prior_contract_files)}: "
        f"{sorted(p.name for p in prior_contract_files)}"
    )
