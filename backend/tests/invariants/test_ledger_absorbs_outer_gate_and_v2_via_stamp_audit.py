"""G6 Ledger absorption via stamp_audit — HAZARD-STOP (a) analog check.

Northena §14: "Stamp-audit → Ledger: Absorbs StampAudit by unit_id / trace_id.
CONFIRM against the stamp-audit side-channel." The side-channel IS the
extension point — outer-gate receipts + V2 refusal envelopes absorb into
stamp_audit as permissive Dict, without any mutation to
northena_ledger_row@v0's frozen shape.

**No new field on northena_ledger_row@v0.** No new stage/decision literal.
The row's frozen snapshot must remain byte-identical after G6.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from contracts.northena_ledger import LedgerArtifactRef
from services.northena import converge as northena_converge


ARTIFACT_REF = LedgerArtifactRef(
    artifact_type="portfolio_mandate",
    artifact_id="g6-absorb-test",
    version="v0",
)


@pytest.mark.asyncio
async def test_outer_gate_receipt_lands_in_stamp_audit():
    """Outer-gate receipt absorption produces a gate-stage row with the
    receipt payload inside stamp_audit; no new field on the row."""
    receipt_dict = {
        "transform_version": "hmac-sha256-v1",
        "key_fingerprint": "a" * 64,
        "mint_window_id": "mint-abs-1",
        "applied_transformations": ["pseudonymise:unit_id"],
        "input_identifier_categories": ["unit_id"],
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "run_id": "run-abs-1",
        "trace_id": "trace-abs-1",
        "artifact_ref": ARTIFACT_REF.model_dump(),
        "k_anonymity_bucket_size": None,
        "differential_privacy_epsilon": None,
    }
    row = await northena_converge.absorb_outer_gate_receipt(
        run_id="run-abs-1", trace_id="trace-abs-1",
        receipt_dict=receipt_dict,
        artifact_ref=ARTIFACT_REF, lawful_basis_ref="dpa-test",
    )
    assert row.stage == "gate"
    assert row.decision == "fresh"
    assert row.reason.startswith("outer_gate_transform_applied:")
    assert isinstance(row.stamp_audit, dict)
    assert row.stamp_audit.get("outer_gate_receipt") == receipt_dict


@pytest.mark.asyncio
async def test_v2_refusal_lands_in_stamp_audit():
    """V2 refusal absorption produces a gate-stage row with the refusal
    envelope inside stamp_audit; no new field on the row."""
    refusal_dict = {
        "reason_code": "lawful_basis_absent",
        "refused_at": datetime.now(timezone.utc).isoformat(),
        "run_id": "run-abs-2",
        "trace_id": "trace-abs-2",
        "artifact_ref": ARTIFACT_REF.model_dump(),
        "lawful_basis_ref": None,
        "substrate_contract_ref": None,
        "detail": "no lawful_basis attached to file-out request",
    }
    row = await northena_converge.absorb_v2_refusal(
        run_id="run-abs-2", trace_id="trace-abs-2",
        refusal_dict=refusal_dict,
        artifact_ref=ARTIFACT_REF, lawful_basis_ref="dpa-test",
    )
    assert row.stage == "gate"
    assert row.decision == "refused"
    assert row.reason == "v2_refused:lawful_basis_absent"
    assert isinstance(row.stamp_audit, dict)
    assert row.stamp_audit.get("v2_refusal") == refusal_dict


def test_northena_ledger_row_contract_snapshot_unchanged_at_g6():
    """The frozen `northena_ledger_row@v0` snapshot MUST be byte-identical
    after G6. If G6 accidentally added a field, this test fails.
    """
    from contracts.northena_ledger import LedgerRow
    snap = json.loads(
        (Path(__file__).parent / "northena_ledger_row.contract_snapshot.json"
         ).read_text(encoding="utf-8")
    )
    actual = LedgerRow.model_json_schema()
    assert json.dumps(actual, indent=2, sort_keys=True) == \
           json.dumps(snap, indent=2, sort_keys=True), (
        "HAZARD-STOP (a) TRIPPED: northena_ledger_row@v0 mutated at G6. "
        "Outer-gate receipts + V2 refusals MUST absorb via stamp_audit "
        "side-channel, not by extending the row's frozen shape."
    )


def test_no_new_stage_literal_at_g6():
    """The stage enum MUST remain {admit, gate, converge} at G6. No 'outer_gate'
    or 'v2_gate' stage may exist."""
    from contracts.northena_ledger import LedgerRow
    schema = LedgerRow.model_json_schema()
    stage_prop = schema["properties"]["stage"]
    allowed = set(stage_prop["enum"])
    assert allowed == {"admit", "gate", "converge"}, (
        f"HAZARD-STOP (a) TRIPPED: stage enum mutated at G6: {allowed}"
    )


def test_no_new_decision_literal_at_g6():
    """The decision enum MUST remain the 7 pre-G6 literals."""
    from contracts.northena_ledger import LedgerRow
    schema = LedgerRow.model_json_schema()
    decision_prop = schema["properties"]["decision"]
    allowed = set(decision_prop["enum"])
    expected = {
        "admitted", "refused",
        "warm", "fresh",
        "terminate_success", "terminate_budget", "continue",
    }
    assert allowed == expected, (
        f"HAZARD-STOP (a) TRIPPED: decision enum mutated at G6: {allowed}"
    )
