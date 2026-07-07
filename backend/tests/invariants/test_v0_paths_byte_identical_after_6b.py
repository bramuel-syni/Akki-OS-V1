"""Byte-identity regression — 20 prior frozen contract source files
MUST remain byte-identical after Phase 6 Stage B landing.

Owner Rule (Phase 5 Stage B redelivery, 2026-07-04): the byte-identity
regression at Phase N Stage B guards contracts 1..N-1 (net-new at N are
NOT included here — mechanical parity invariant guards them).

At Phase 6 Stage B: the 20 PRIOR frozen contract files are contracts
1..20 (all landed pre-6b). Contracts 21 (`quote_envelope.py`) + 22
(`async_delivery_accepted_v1.py`) are net-new at 6b; NOT included here.

Any drift in the 20 prior files is a HAZARD-STOP under
Standing Owner Disposition `frozen-field-changes-as-new-versions`:
  [Owner ruling, Phase 5 Stage A close, 2026-07-04] "the outcome of Opt 4
  via the doctrinal path: northena_ledger_row@v1 as a new frozen
  contract version. In-place widening of the Literal (Opt 4 as written)
  is mutation — the Phase 0 loose-as-frozen ruling already settled that
  changes to frozen fields land as new versions, never in-place."

Also pins `services/service_1/composed_conclusion.py:316-321` per
Verdict A protection ratification (2026-07-04, Owner ruling); a redundant
Q4.c regression guard from 5b that stays LOAD-BEARING at 6b.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest


CONTRACTS_DIR = Path(__file__).resolve().parent.parent.parent / "contracts"


# 20 PRIOR frozen contract source SHAs captured at Phase 6 Stage B open
# (2026-07-04). Contracts 21 + 22 (net-new) are NOT included.
PRIOR_20_SHAS = {
    "admission_refusal.py":           "e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f",
    "async_delivery_accepted.py":     "fc495b76db99ab57901a1eccad490bdbed74368d9a2ffc081c42f619d38d7dde",
    "composed_conclusion.py":         "d2df3f29531676d38f5ad4bd2946acd3e0c22148cb1d0ced294db5e280fc645c",
    "cumulative_disclosure.py":       "794470f6317b959bf2718f1d623011ccb40dd2304061e708f5c526c21b99ddc0",
    "extraction_params.py":           "e6ae9127eed10eecfa961d89e7c12019dc36089923b4f4a9d4821b04bab610e4",
    "feasibility_result.py":          "a64a6faf2afe9bb6674399a097f90906ecce4675217fe2ad33dc0efea683a9f5",
    "five_rings.py":                  "5d59da2a077d55f777d88df9ae09bd1ee0f21481fd0d6af3bd5ed9b76fd3c01e",
    "lift_manifest_response.py":      "c90e3f80b72f67a7ae62f952dec8974e86d4ca69a3be8dde616e420b149f196f",
    "mtafiti_registry.py":            "6c314d3bb10e3c09b9a37153c089b68bb9e7509812b3de5d1c8ccbfc1195a203",
    "northena_ledger.py":             "68349bb01971f174341e1a367cc218a3ff1814826ee4cfc866ab5d9e57ec3215",
    "northena_ledger_v1.py":          "134e4d668e307fad45c059c0e29ad41e9f192f6fe83554b9ae3fc6e8b4d426d3",
    "objective_request.py":           "2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1",
    "objective_request_v2.py":        "e20956c5c3751180e9b69fed08a8738c0cdeed3d86aaa0db604f3ef932f2e994",
    "outer_gate_receipt.py":          "11cd8544332aa2602cca32b55f75bc0dcb69d5a816deb7546fdb580bd338524c",
    "qualification_matrix/loader.py": "eef3135e4fc2dcfac8c430e5f13f11d7ac40d5cb627ec75a33ef9264eaf0ab83",
    "service_1_refusal.py":           "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022",
    "signal_ring.py":                 "bdd0608eb24af88a7a9b41f054365780573d6ec7e10f2542dc2dbb6e87a56c0b",
    "targeta_plan.py":                "013979c39dee561cf598dd30868b18faf70fc912094f906dc74ec0ec5272fe4f",
    "trace_lens.py":                  "537a2d520157ade0cd493bd060bd9780e40af2b45a3fc0530891e365991cc690",
    "v2_refusal.py":                  "0e6f3288e83dec558d83fdffedbb79fbae6af78b5d239512248e38f75eeddaaf",
}


def test_prior_20_contracts_count_at_20():
    """Sanity: the protected-set enumeration is exactly 20 at Phase 6 Stage B."""
    assert len(PRIOR_20_SHAS) == 20, (
        f"Protected-set MUST enumerate exactly 20 prior frozen contract "
        f"files at Phase 6 Stage B; got {len(PRIOR_20_SHAS)}. HAZARD-STOP — reconcile."
    )


@pytest.mark.parametrize("rel_path,expected_sha", sorted(PRIOR_20_SHAS.items()))
def test_prior_contract_file_byte_identical_after_6b(rel_path: str, expected_sha: str):
    """Each of the 20 prior frozen contract sources MUST hash to the
    exact SHA-256 captured at Phase 6 Stage B open.

    Standing Owner Disposition `frozen-field-changes-as-new-versions`:
    the prior file MUST be preserved and any change lands as a NEW
    contract version (e.g. `<name>_v1.py`).
    """
    p = CONTRACTS_DIR / rel_path
    assert p.exists(), f"Frozen contract source missing: {p}"
    actual_sha = hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual_sha == expected_sha, (
        f"HAZARD-STOP — file {rel_path!r} SHA drifted post-Phase-6-Stage-B.\n"
        f"  Expected: {expected_sha}\n"
        f"  Actual  : {actual_sha}\n"
        f"Standing Owner Disposition `frozen-field-changes-as-new-versions` "
        f"requires the prior file be preserved and any change land as a NEW "
        f"contract version (e.g. `<name>_v1.py`)."
    )


def test_composed_conclusion_synthesis_lines_untouched_at_6b():
    """Verdict A protection regression — `services/service_1/composed_conclusion.py:316-321`
    UNTOUCHED at Phase 6 Stage B. Same SHA slice as 5b's Q4.c gate."""
    backend_root = Path(__file__).resolve().parent.parent.parent
    p = backend_root / "services" / "service_1" / "composed_conclusion.py"
    lines = p.read_text().splitlines(keepends=True)
    assert len(lines) >= 321, (
        f"services/service_1/composed_conclusion.py truncated below 321 lines: {len(lines)}"
    )
    # Sub-stage 1 (2026-07-07): synthesis-lines slice shifted [315:321]→[329:335]
    # after I4 wire-up; slice content SHA d2e72653 byte-identical.
    slice_bytes = "".join(lines[329:335]).encode("utf-8")
    slice_sha = hashlib.sha256(slice_bytes).hexdigest()
    EXPECTED = "d2e72653f84c4772796a6fb71b61fb70345f057cfd3451d60bbfb15bc2d58159"
    assert slice_sha == EXPECTED, (
        f"HAZARD-STOP — services/service_1/composed_conclusion.py:316-321 "
        f"synthesis lines drifted post-Phase-6-Stage-B.\n"
        f"  Expected: {EXPECTED}\n"
        f"  Actual  : {slice_sha}\n"
        f"Owner Q4.c ratification (5b) + Verdict A regression at 6b: untouched."
    )
