"""G6 GATE CONDITION 2 — V2 refusal (LIVE) + cumulative-disclosure arm (SHAPE B — closed seam).

Product v2.1 §29.1: V2 gates the outer-gate file-out — "confirms rights past
extract-for-RMS, resolves the substrate/rights contract, verifies a sample
file-out cryptographically, and demonstrates the cumulative-disclosure guard
refusing a reconstruction attempt".

**Single-packet arm — LIVE**: every refusal reason produces a valid envelope,
no partial egress ever.

**Cumulative arm — SHAPE B, closed seam at v0**: arm is built, gate held
closed via `cumulative_arm_admitted() -> False`, declared in system_state.
Config-unlock: DPO/Owner-owned k, l, epsilon thresholds via env vars
(§32 pattern).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from contracts.cumulative_disclosure import CumulativeDisclosureLedger
from contracts.northena_ledger import LedgerArtifactRef
from contracts.v2_refusal import V2RefusalEnvelope
from services.v2_gate import cumulative
from services.v2_gate.refusal import build_refusal


ARTIFACT_REF = LedgerArtifactRef(
    artifact_type="portfolio_mandate",
    artifact_id="g6-test-artifact",
    version="v0",
)

REASON_CODES = [
    "lawful_basis_absent",
    "substrate_rights_expired",
    "sample_file_out_crypto_verify_failed",
    "cumulative_disclosure_risk",
]


# ---- Single-packet refusal (LIVE) ----------------------------------------
@pytest.mark.parametrize("reason_code", REASON_CODES)
def test_v2_refusal_valid_envelope_per_reason(reason_code):
    """Every refusal reason produces a well-formed V2RefusalEnvelope."""
    env = build_refusal(
        reason_code=reason_code,
        run_id="run-g6-1",
        trace_id="trace-g6-1",
        artifact_ref=ARTIFACT_REF,
        lawful_basis_ref="dpa-test",
        detail=f"test refusal for {reason_code}",
    )
    assert isinstance(env, V2RefusalEnvelope)
    assert env.reason_code == reason_code
    assert env.run_id == "run-g6-1"
    assert env.trace_id == "trace-g6-1"
    assert env.artifact_ref == ARTIFACT_REF


def test_v2_refusal_envelope_rejects_unknown_reason_code():
    """Unknown reason_code must be rejected by the Literal — no partial-egress
    escape hatch."""
    with pytest.raises(Exception):  # pydantic ValidationError
        V2RefusalEnvelope(
            reason_code="totally_made_up_reason",  # type: ignore[arg-type]
            refused_at="2026-07-02T00:00:00Z",
            run_id="r", trace_id="t", artifact_ref=ARTIFACT_REF,
        )


def test_v2_refusal_is_terminal_no_partial_egress():
    """Refusal envelope is the record; nothing else crosses.

    Structural invariant: the envelope's shape carries no 'partial_content'
    or 'egress_bytes' escape; refusal is a total decision.
    """
    env = build_refusal(
        reason_code="lawful_basis_absent",
        run_id="r", trace_id="t", artifact_ref=ARTIFACT_REF,
    )
    dumped = env.model_dump()
    for forbidden in ("partial_content", "partial_egress", "egress_bytes",
                      "content_stream", "partial_payload"):
        assert forbidden not in dumped, (
            f"V2RefusalEnvelope leaks partial-egress field {forbidden!r}"
        )


def test_v2_refusal_envelope_contract_frozen():
    snap = json.loads(
        (Path(__file__).parent / "v2_refusal_envelope.contract_snapshot.json"
         ).read_text(encoding="utf-8")
    )
    assert (
        json.dumps(V2RefusalEnvelope.model_json_schema(), indent=2, sort_keys=True)
        == json.dumps(snap, indent=2, sort_keys=True)
    ), "V2RefusalEnvelope schema drifted; re-bless snapshot in review."


# ---- Cumulative-disclosure arm — SHAPE B (closed seam at v0) ------------
def test_cumulative_arm_closed_by_default():
    """At G6 v0, no DPO/Owner thresholds → arm CLOSED.
    This is the acceptance bar for Shape B.
    """
    for k in ("RMS_G6_K_ANONYMITY_THRESHOLD",
              "RMS_G6_L_DIVERSITY_THRESHOLD",
              "RMS_G6_DP_EPSILON_BUDGET"):
        assert k not in os.environ or os.environ.get(k) is None, (
            f"config env {k} is set; test isolation broken"
        )
    assert cumulative.cumulative_arm_admitted() is False, (
        "cumulative arm admitted with no thresholds configured — "
        "closed-seam guarantee compromised"
    )


def test_cumulative_evaluate_short_circuits_when_closed():
    """When arm is closed, evaluate() must return None (no refusal
    generated), even for scenarios that WOULD refuse under a live arm.
    """
    prior = CumulativeDisclosureLedger(
        mint_window_id="mint-1",
        egress_fingerprints=["fp1", "fp2", "fp3"],
        k_threshold=2,  # would refuse if arm were live
        arm_admitted=False,
    )
    result = cumulative.evaluate(
        {"unit_id": "x"}, prior,
        run_id="r", trace_id="t", artifact_ref=ARTIFACT_REF,
    )
    assert result is None, (
        "closed-seam arm returned a refusal — arm should short-circuit "
        "when cumulative_arm_admitted() is False"
    )


def test_cumulative_arm_opens_when_all_thresholds_configured(monkeypatch):
    """Config unlock path: setting all three env vars opens the arm.
    This asserts the arm is BUILT, not just declared."""
    monkeypatch.setenv("RMS_G6_K_ANONYMITY_THRESHOLD", "5")
    monkeypatch.setenv("RMS_G6_L_DIVERSITY_THRESHOLD", "3")
    monkeypatch.setenv("RMS_G6_DP_EPSILON_BUDGET", "0.5")
    assert cumulative.cumulative_arm_admitted() is True


def test_cumulative_arm_stays_closed_if_only_some_thresholds_set(monkeypatch):
    """All-or-nothing: partial config keeps the arm closed."""
    monkeypatch.setenv("RMS_G6_K_ANONYMITY_THRESHOLD", "5")
    monkeypatch.setenv("RMS_G6_L_DIVERSITY_THRESHOLD", "3")
    # RMS_G6_DP_EPSILON_BUDGET NOT set
    assert cumulative.cumulative_arm_admitted() is False


def test_cumulative_evaluate_refuses_when_threshold_crossed(monkeypatch):
    """When arm is opened AND fingerprint count reaches k, evaluate()
    returns a V2RefusalEnvelope with reason_code='cumulative_disclosure_risk'.

    This proves the arm is BUILT, not merely present as scaffolding.
    """
    monkeypatch.setenv("RMS_G6_K_ANONYMITY_THRESHOLD", "3")
    monkeypatch.setenv("RMS_G6_L_DIVERSITY_THRESHOLD", "2")
    monkeypatch.setenv("RMS_G6_DP_EPSILON_BUDGET", "0.5")
    prior = CumulativeDisclosureLedger(
        mint_window_id="mint-1",
        egress_fingerprints=["fp1", "fp2"],  # 2 prior + 1 new = 3 = k
        k_threshold=3,
        arm_admitted=True,
    )
    result = cumulative.evaluate(
        {"unit_id": "x"}, prior,
        run_id="r", trace_id="t", artifact_ref=ARTIFACT_REF,
    )
    assert result is not None
    assert result.reason_code == "cumulative_disclosure_risk"


def test_cumulative_disclosure_ledger_contract_frozen():
    snap = json.loads(
        (Path(__file__).parent / "cumulative_disclosure_ledger.contract_snapshot.json"
         ).read_text(encoding="utf-8")
    )
    assert (
        json.dumps(CumulativeDisclosureLedger.model_json_schema(), indent=2, sort_keys=True)
        == json.dumps(snap, indent=2, sort_keys=True)
    ), "CumulativeDisclosureLedger schema drifted; re-bless snapshot in review."
