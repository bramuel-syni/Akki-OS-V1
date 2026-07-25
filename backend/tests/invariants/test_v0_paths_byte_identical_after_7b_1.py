"""Byte-identity regression — 22 prior frozen contract source files
MUST remain byte-identical after Phase 7 Stage B-1 landing.

Owner Standing Disposition `frozen-field-changes-as-new-versions`
[Owner ruling, Phase 5 Stage A close, 2026-07-04] "the outcome of Opt 4
via the doctrinal path: northena_ledger_row@v1 as a new frozen contract
version. In-place widening of the Literal (Opt 4 as written) is
mutation — the Phase 0 loose-as-frozen ruling already settled that
changes to frozen fields land as new versions, never in-place."

At Phase 7 Stage B-1 the 22 PRIOR frozen contract files are contracts
1..22 (all landed at ≤ Phase 6 Stage B). Contracts 23..26 (the four
wizard contracts: `wizard_commit_state.py` + `operator_turn.py` +
`agent_assumption.py` + `committed_value.py`) are net-new at B-1 and
are NOT included in this table (they're guarded by the mechanical
parity invariant + per-contract frozen-schema gates).

Also pins `services/service_1/composed_conclusion.py:316-321` per
Verdict A regression from 4b/5b/6b — the answer_text synthesis
lines stay untouched at B-1 (see the dedicated gate below).
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest


CONTRACTS_DIR = Path(__file__).resolve().parent.parent.parent / "contracts"


# 22 PRIOR frozen contract source SHAs captured at Phase 7 Stage B-1
# open (2026-07-04). Contracts 23..26 (the four wizard net-new) are
# NOT included.
PRIOR_22_SHAS = {
    "admission_refusal.py":           "e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f",
    "async_delivery_accepted.py":     "fc495b76db99ab57901a1eccad490bdbed74368d9a2ffc081c42f619d38d7dde",
    "async_delivery_accepted_v1.py":  "fb5c274f99ed66a4604169325f35ae642cfe0152b625a6a0661ad253cefdfe92",
    "composed_conclusion.py":         "d2df3f29531676d38f5ad4bd2946acd3e0c22148cb1d0ced294db5e280fc645c",
    "cumulative_disclosure.py":       "794470f6317b959bf2718f1d623011ccb40dd2304061e708f5c526c21b99ddc0",
    "extraction_params.py":           "e6ae9127eed10eecfa961d89e7c12019dc36089923b4f4a9d4821b04bab610e4",
    "feasibility_result.py":          "e979e5155820a2c2da9a71e4a97359c76c24effd4390ffb86245111b2807c58f",
    "five_rings.py":                  "5d59da2a077d55f777d88df9ae09bd1ee0f21481fd0d6af3bd5ed9b76fd3c01e",
    "lift_manifest_response.py":      "c90e3f80b72f67a7ae62f952dec8974e86d4ca69a3be8dde616e420b149f196f",
    "mtafiti_registry.py":            "6c314d3bb10e3c09b9a37153c089b68bb9e7509812b3de5d1c8ccbfc1195a203",
    "northena_ledger.py":             "68349bb01971f174341e1a367cc218a3ff1814826ee4cfc866ab5d9e57ec3215",
    "northena_ledger_v1.py":          "134e4d668e307fad45c059c0e29ad41e9f192f6fe83554b9ae3fc6e8b4d426d3",
    "objective_request.py":           "2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1",
    "objective_request_v2.py":        "e20956c5c3751180e9b69fed08a8738c0cdeed3d86aaa0db604f3ef932f2e994",
    "outer_gate_receipt.py":          "11cd8544332aa2602cca32b55f75bc0dcb69d5a816deb7546fdb580bd338524c",
    "qualification_matrix/loader.py": "eef3135e4fc2dcfac8c430e5f13f11d7ac40d5cb627ec75a33ef9264eaf0ab83",
    "quote_envelope.py":              "4189c5df2414e9f93a4d9d5bd9b0dcd0277f9e479c1705acea46d4eb0f2e15fe",
    "service_1_refusal.py":           "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022",
    "signal_ring.py":                 "bdd0608eb24af88a7a9b41f054365780573d6ec7e10f2542dc2dbb6e87a56c0b",
    "targeta_plan.py":                "4dfb8177d60900d558ba49c76bb3bde03c87b0d0de11fcf72552b2fe5c8f2179",
    "trace_lens.py":                  "537a2d520157ade0cd493bd060bd9780e40af2b45a3fc0530891e365991cc690",
    "v2_refusal.py":                  "0e6f3288e83dec558d83fdffedbb79fbae6af78b5d239512248e38f75eeddaaf",
}


def test_prior_22_contracts_count_at_22():
    """Sanity: the protected-set enumeration is exactly 22 at Phase 7 Stage B-1."""
    assert len(PRIOR_22_SHAS) == 22, (
        f"Protected-set MUST enumerate exactly 22 prior frozen contract "
        f"files at Phase 7 Stage B-1; got {len(PRIOR_22_SHAS)}. "
        f"HAZARD-STOP — reconcile."
    )


@pytest.mark.parametrize("rel_path,expected_sha", sorted(PRIOR_22_SHAS.items()))
def test_prior_contract_file_byte_identical_after_7b_1(rel_path: str, expected_sha: str):
    """Each of the 22 prior frozen contract sources MUST hash to the
    exact SHA-256 captured at Phase 7 Stage B-1 open.

    Standing Owner Disposition `frozen-field-changes-as-new-versions`:
    the prior file MUST be preserved and any change lands as a NEW
    contract version (e.g. `<name>_v1.py`).
    """
    p = CONTRACTS_DIR / rel_path
    assert p.exists(), f"Frozen contract source missing: {p}"
    actual_sha = hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual_sha == expected_sha, (
        f"HAZARD-STOP — file {rel_path!r} SHA drifted post-Phase-7-Stage-B-1.\n"
        f"  Expected: {expected_sha}\n"
        f"  Actual  : {actual_sha}\n"
        f"Standing Owner Disposition `frozen-field-changes-as-new-versions` "
        f"requires the prior file be preserved and any change land as a NEW "
        f"contract version (e.g. `<name>_v1.py`)."
    )


def test_composed_conclusion_synthesis_lines_untouched_at_7b_1():
    """AF-E4 α re-bless — mechanical composer extracted byte-identically
    to `services/service_1/mechanical_composer.py` at Answer Fluency
    close (Owner 2026-07-10). Gate repointed at the extracted composer
    for backward-compat continuity; byte-identical slice · SHA re-blessed.
    """
    backend_root = Path(__file__).resolve().parent.parent.parent
    p = backend_root / "services" / "service_1" / "mechanical_composer.py"
    lines = p.read_text().splitlines(keepends=True)
    assert len(lines) >= 40, (
        f"services/service_1/mechanical_composer.py truncated below 40 lines: {len(lines)}"
    )
    slice_bytes = "".join(lines[35:40]).encode("utf-8")
    slice_sha = hashlib.sha256(slice_bytes).hexdigest()
    EXPECTED = "7475be407cf35e1d87f2d6712a262d58fe26aac00897a4475f0cb88180565f4d"
    assert slice_sha == EXPECTED, (
        f"HAZARD-STOP — mechanical_composer.py:36-41 synthesis lines "
        f"drifted post-Answer-Fluency.\n"
        f"  Expected: {EXPECTED}\n"
        f"  Actual  : {slice_sha}\n"
        f"AF-E4 α: golden diff against pre_3_8/mechanical_baseline.json "
        f"is the primary attest (AF-G1)."
    )


def test_grain_compatibility_untouched_at_7b_1():
    """Ruling 4 shared-derivation regression — grain_compatibility.py stays
    byte-identical at 7b-1 (no new inputs, no re-implementation)."""
    backend_root = Path(__file__).resolve().parent.parent.parent
    p = backend_root / "services" / "service_1" / "grain_compatibility.py"
    actual_sha = hashlib.sha256(p.read_bytes()).hexdigest()
    EXPECTED = "183a18b47de481c4566e6dcacaa9b33c62e485bb4be33de0ca31b32f42cccfcc"
    assert actual_sha == EXPECTED, (
        f"HAZARD-STOP — grain_compatibility.py SHA drifted post-7b-1.\n"
        f"  Expected: {EXPECTED}\n"
        f"  Actual  : {actual_sha}\n"
        f"Ruling 4 shared-derivation: this module is one derivation seam; "
        f"drift means either behavioural change (needs owner bless) or "
        f"accidental refactor (revert)."
    )


def test_derive_license_class_from_commissioner_untouched_at_7b_1():
    """Owner E1 Option C wrap invariant — the FALLBACK ARM body slice
    (function `derive_license_class_from_commissioner`) MUST remain
    byte-identical. The Option C wrap is ADDITIVE (adds a new
    `derive_license_class` function above/below); it does not touch the
    fallback arm's body.
    """
    backend_root = Path(__file__).resolve().parent.parent.parent
    p = backend_root / "services" / "service_1" / "license_class_selection.py"
    lines = p.read_text().splitlines(keepends=True)
    start = None
    for i, ln in enumerate(lines):
        if "def derive_license_class_from_commissioner" in ln:
            start = i
            break
    assert start is not None, (
        "derive_license_class_from_commissioner not found in "
        "license_class_selection.py — fallback arm missing?"
    )
    end = len(lines)
    for j in range(start + 1, len(lines)):
        # Fallback body ends at the next top-level def/class OR at EOF.
        if lines[j].startswith("def ") or lines[j].startswith("class "):
            end = j
            break
    slice_bytes = "".join(lines[start:end]).encode("utf-8")
    slice_sha = hashlib.sha256(slice_bytes).hexdigest()
    EXPECTED = "ca3b2007f0cee58da3de0562eea3e92492761cda95a8297e632b5346b8d0e41e"
    assert slice_sha == EXPECTED, (
        f"HAZARD-STOP — derive_license_class_from_commissioner body slice "
        f"drifted post-Phase-7-Stage-B-1.\n"
        f"  Expected: {EXPECTED}\n"
        f"  Actual  : {slice_sha}\n"
        f"Owner E1 Option C wrap is ADDITIVE only; the fallback arm body "
        f"MUST remain byte-identical."
    )
