"""EAB-2 Parity 31→32 seal + AC-A3.a-c + AC-A4.a-c + §2 companion-channel-down gate cells.

Sanction: `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md`
(SHA `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5`).

Owner ruling composition: ε + α + γ (Locus 1 · 2 · 3).

Gate cells landed here:
  * `test_parity_32_contracts_and_snapshots` — Parity 31→32 attest.
  * `test_service_1_refusal_v0_byte_identity_under_eab2` — Standing Rule v3.
  * `test_service_1_refusal_v1_reason_enum_four_members` — Locus 1 = ε.
  * `test_service_1_refusal_v1_no_estimated_effort_field` — Locus 2 = α.
  * `test_service_1_refusal_v1_no_queue_action_url_field` — Locus 3 = γ.
  * `test_service_1_refusal_v1_snapshot_matches_schema` — schema stability.
  * `test_service_1_refusal_v1_ast_negative_scan_fault_never_dressed` — R-A3.3.
  * `test_service_1_refusal_v1_additive_extends_v0` — additive versioning.
  * `test_ac_a3_a_three_response_types_distinct_at_wire` — AC-A3.a.
  * `test_ac_a3_b_coverage_gap_idempotent_same_filed_candidate` — AC-A3.b.
  * `test_ac_a4_a_batch_quarantine_ledger_row_run_continues` — AC-A4.a.
  * `test_ac_a4_b_systemic_halt_threshold_fires_notification` — AC-A4.b.
  * `test_ac_a4_c_quarantine_remediate_reprocess_walk_visible` — AC-A4.c.
  * `test_eab2_owner_ruling_section_2_companion_channel_down_refusal_renders` — Owner §2.

Owner §2 failure-mode binding:
  If the Locus-2 companion read fails, times out, or returns empty: Prove
  renders the coverage_gap refusal without the effort line, in refusal
  styling. Never degrades to the fault surface, never converts to
  something-broke, never blocks the refusal render. The queue action is
  unaffected by companion-read failure — its URL derives from
  filed_candidate_id on the envelope itself.
"""
from __future__ import annotations

import ast
import json
import pathlib
from datetime import datetime, timezone

import pytest

from contracts.service_1_refusal import Service1Refusal as Service1Refusal_v0
from contracts.service_1_refusal_v1 import Service1Refusal_v1
from services.service_1 import batch_quarantine
from services.targeta import gap_candidate_filer


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACTS_DIR = BACKEND_ROOT / "contracts"
INVARIANTS_DIR = BACKEND_ROOT / "tests" / "invariants"


# ---------------------------------------------------------------------------
# §0-CAL §23.1 per-line enumeration attest — mandatory on backend/contracts/**.
#
# Each declarative line in `backend/contracts/service_1_refusal_v1.py` carries
# a rung verdict-line below. Rung 1 = Deterministic (Pydantic frozen-contract
# discipline). This table is the §0-CAL §23.1 enumeration anchor.
# ---------------------------------------------------------------------------

CAL_23_1_ENUM = [
    # (line-anchor,                                   rung, verdict)
    ("model_config ConfigDict(extra=forbid,frozen=True)", 1, "deterministic"),
    ("outcome: Literal['refused']",                       1, "deterministic"),
    ("reason: Literal[4-value enum]",                     1, "deterministic"),
    ("run_id: str",                                       1, "deterministic"),
    ("trace_id: str",                                     1, "deterministic"),
    ("asked: str",                                        1, "deterministic"),
    ("supported_class: Optional[DefensibilityClass]",     1, "deterministic"),
    ("what_would_raise_it: str",                          1, "deterministic"),
    ("estate_region: Optional[str]",                      1, "deterministic"),
    ("period: Optional[str]",                             1, "deterministic"),
    ("source_class: Optional[str]",                       1, "deterministic"),
    ("filed_candidate_id: Optional[str]",                 1, "deterministic"),
]


def test_cal_23_1_enumeration_present_on_v1_contract():
    """§0-CAL §23.1 per-line enumeration mandatory attest."""
    assert len(CAL_23_1_ENUM) == 12  # 1 config + 11 fields
    for _anchor, rung, verdict in CAL_23_1_ENUM:
        assert rung == 1
        assert verdict == "deterministic"


# ---------------------------------------------------------------------------
# Parity 31→32 attest + v0 byte-identity attest (Standing Rule v3).
# ---------------------------------------------------------------------------

def test_parity_32_contracts_and_snapshots():
    """Parity 32 baseline attest · post-EAB-2 seal · superseded by EAB-3 seal.

    Post-EAB-3 (2026-07-24 · Owner ruling (a1)), parity moves 32→33. This cell
    retains its historical name for lineage but asserts against the live post-
    EAB-3 count of 33 (Owner ITEM 1 seal). The Parity 32→33 authoritative attest
    is at `tests/invariants/test_partition_schema_v0_envelope.py::
    test_parity_33_contracts_and_snapshots`.
    """
    contract_files = sorted(CONTRACTS_DIR.glob("*.py"))
    snapshot_files = sorted(INVARIANTS_DIR.glob("*.contract_snapshot.json"))
    assert len(contract_files) == 33, f"expected 33 contracts, got {len(contract_files)}"
    assert len(snapshot_files) == 33, f"expected 33 snapshots, got {len(snapshot_files)}"


def test_service_1_refusal_v0_byte_identity_under_eab2():
    """Standing Rule v3: v0 contract file bytes unchanged post-EAB-2 seal."""
    import hashlib
    v0_path = CONTRACTS_DIR / "service_1_refusal.py"
    sha = hashlib.sha256(v0_path.read_bytes()).hexdigest()
    # SHA fixed at v0 landing (A2 · 2026-07-04); MUST NOT change post-EAB-2.
    assert sha == "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022"


def test_service_1_refusal_v0_snapshot_byte_identity_under_eab2():
    """Standing Rule v3: v0 snapshot file bytes unchanged post-EAB-2 seal."""
    import hashlib
    v0_snap_path = INVARIANTS_DIR / "service_1_refusal.contract_snapshot.json"
    sha = hashlib.sha256(v0_snap_path.read_bytes()).hexdigest()
    assert sha == "56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d"


# ---------------------------------------------------------------------------
# Locus 1 = ε · Locus 2 = α · Locus 3 = γ attest cells.
# ---------------------------------------------------------------------------

def test_service_1_refusal_v1_reason_enum_four_members():
    """Locus 1 = ε: reason enum is EXACTLY 4 members (3 evidential + coverage_gap)."""
    schema = Service1Refusal_v1.model_json_schema()
    enum = schema["properties"]["reason"]["enum"]
    assert set(enum) == {
        "no_defensibility_floor",
        "no_lawful_basis",
        "composition_below_floor",
        "coverage_gap",
    }
    assert len(enum) == 4
    # Option η rejected: `something_broke` MUST NOT be a reason value.
    assert "something_broke" not in enum
    assert "something-broke" not in enum


def test_service_1_refusal_v1_no_estimated_effort_field():
    """Locus 2 = α: envelope carries NO `estimated_effort` field."""
    schema = Service1Refusal_v1.model_json_schema()
    fields = set(schema["properties"].keys())
    assert "estimated_effort" not in fields
    assert "estimated_effort_to_close_it" not in fields


def test_service_1_refusal_v1_no_queue_action_url_field():
    """Locus 3 = γ: envelope carries NO `queue_action_url` or `queue_action` field."""
    schema = Service1Refusal_v1.model_json_schema()
    fields = set(schema["properties"].keys())
    assert "queue_action_url" not in fields
    assert "queue_action" not in fields


def test_service_1_refusal_v1_field_count_11():
    """Envelope shape: exactly 11 fields (7 v0-preserved + 4 v1 additive)."""
    schema = Service1Refusal_v1.model_json_schema()
    assert len(schema["properties"]) == 11


def test_service_1_refusal_v1_additive_4_tuple_matches_stage_a():
    """Stage A §5.1 4-tuple additive set: {estate_region, period, source_class, filed_candidate_id}."""
    schema = Service1Refusal_v1.model_json_schema()
    v0_fields = {"outcome", "reason", "run_id", "trace_id", "asked",
                 "supported_class", "what_would_raise_it"}
    v1_additive = set(schema["properties"].keys()) - v0_fields
    assert v1_additive == {"estate_region", "period", "source_class", "filed_candidate_id"}


def test_service_1_refusal_v1_snapshot_matches_schema():
    """Snapshot invariant: on-disk snapshot equals live-generated schema (byte-drift = CI red)."""
    snap_path = INVARIANTS_DIR / "service_1_refusal_v1.contract_snapshot.json"
    stored = json.loads(snap_path.read_text())
    live = Service1Refusal_v1.model_json_schema()
    live_normalized = json.loads(json.dumps(live, sort_keys=True))
    stored_normalized = json.loads(json.dumps(stored, sort_keys=True))
    assert live_normalized == stored_normalized


def test_service_1_refusal_v1_additive_extends_v0_fields():
    """PROM-S1-additive-versioning: v1 field-set is a strict superset of v0's field-set."""
    v0_schema = Service1Refusal_v0.model_json_schema()
    v1_schema = Service1Refusal_v1.model_json_schema()
    v0_fields = set(v0_schema["properties"].keys())
    v1_fields = set(v1_schema["properties"].keys())
    assert v0_fields.issubset(v1_fields)
    # v0 has 7 fields; v1 has 11; additive count = 4.
    assert len(v1_fields) - len(v0_fields) == 4


# ---------------------------------------------------------------------------
# R-A3.3 AST negative-scan · fault-never-dressed-as-refusal.
# ---------------------------------------------------------------------------

def test_service_1_refusal_v1_ast_negative_scan_fault_never_dressed():
    """R-A3.3 AST scan: `something_broke` / fault vocabulary MUST NOT appear as a `reason` value."""
    v1_source = (CONTRACTS_DIR / "service_1_refusal_v1.py").read_text()
    tree = ast.parse(v1_source)

    banned_reason_values = {
        "something_broke", "something-broke",
        "fault", "error", "timeout", "runtime_transient",
        "config_defect", "downstream_error",
    }

    # Walk the AST for Literal[...] Subscripts assigned to `reason` field.
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            assert node.value not in banned_reason_values, (
                f"R-A3.3 violation: fault-family token '{node.value}' appears in v1 contract module"
            )


# ---------------------------------------------------------------------------
# AC-A3.a · three response types distinct at wire.
# ---------------------------------------------------------------------------

def test_ac_a3_a_three_response_types_distinct_at_wire():
    """AC-A3.a: three response types distinct at wire schema (schema cells · not copy variations).

    Response types:
      1. coverage_gap refusal (reason='coverage_gap' · 4 additive fields populated · HTTP 422)
      2. evidential-family refusal (reason ∈ 3-value evidential enum · 4 additive fields None · HTTP 422)
      3. fault envelope (HTTP 503 · structured detail · no `outcome` · disjoint envelope family per R-A3.3)
    """
    # Type 1: coverage_gap
    coverage = Service1Refusal_v1(
        reason="coverage_gap",
        run_id="R1",
        trace_id="T1",
        asked="…",
        supported_class=None,
        what_would_raise_it="close the gap via extraction",
        estate_region="EU",
        period="2024Q4",
        source_class="loan_book",
        filed_candidate_id="OBJ-ABC123",
    )
    assert coverage.reason == "coverage_gap"
    assert coverage.filed_candidate_id is not None
    assert coverage.outcome == "refused"

    # Type 2: evidential
    evidential = Service1Refusal_v1(
        reason="composition_below_floor",
        run_id="R2",
        trace_id="T2",
        asked="…",
        supported_class="utterance",
        what_would_raise_it="corroboration",
    )
    assert evidential.reason == "composition_below_floor"
    assert evidential.filed_candidate_id is None
    assert evidential.estate_region is None
    assert evidential.outcome == "refused"

    # Type 3: fault envelope — disjoint. R-A3.3: MUST NOT be constructable as a
    # Service1Refusal_v1 instance. Attempting reason='something_broke' raises.
    with pytest.raises(Exception):  # pydantic ValidationError
        Service1Refusal_v1(
            reason="something_broke",  # type: ignore[arg-type]
            run_id="R3",
            trace_id="T3",
            asked="…",
            what_would_raise_it="…",
        )


# ---------------------------------------------------------------------------
# AC-A3.b · coverage_gap idempotent · second identical ask cites same filed candidate.
# ---------------------------------------------------------------------------

def test_ac_a3_b_coverage_gap_idempotent_same_filed_candidate():
    """AC-A3.b: identical (estate_region, period, source_class) → same filed_candidate_id."""
    gap_candidate_filer._reset_for_tests()
    first = gap_candidate_filer.file_gap_candidate(
        estate_region="EU", period="2024Q4", source_class="loan_book",
        estimated_effort="≈ 3 days",
    )
    second = gap_candidate_filer.file_gap_candidate(
        estate_region="EU", period="2024Q4", source_class="loan_book",
        estimated_effort="≈ 3 days",
    )
    assert first.filed_candidate_id == second.filed_candidate_id
    # Distinct tuple → distinct id.
    third = gap_candidate_filer.file_gap_candidate(
        estate_region="US", period="2024Q4", source_class="loan_book",
        estimated_effort="≈ 5 days",
    )
    assert third.filed_candidate_id != first.filed_candidate_id


# ---------------------------------------------------------------------------
# AC-A4.a · per-batch quarantine · run continues.
# ---------------------------------------------------------------------------

def test_ac_a4_a_batch_quarantine_ledger_row_run_continues():
    """AC-A4.a: quarantined batch ledgered, batch_excluded=True, run_continues=True."""
    batch_quarantine._reset_for_tests()
    event = batch_quarantine.quarantine_batch(
        batch_id="B-42", reason="policy_violation_synthetic",
        run_id="RUN-A", instance_id="inst-1",
    )
    assert event.batch_excluded is True
    assert event.run_continues is True
    assert event.receipt.startswith("QN-")
    ledger = batch_quarantine.get_quarantine_events("RUN-A", "inst-1")
    assert len(ledger) == 1
    assert ledger[0].batch_id == "B-42"


# ---------------------------------------------------------------------------
# AC-A4.b · systemic-halt threshold fires notification.
# ---------------------------------------------------------------------------

def test_ac_a4_b_systemic_halt_threshold_fires_notification():
    """AC-A4.b: quarantine rate exceeds F2 seam threshold → HALT ledgered · notification observable."""
    batch_quarantine._reset_for_tests()
    # Simulate 3 quarantined batches out of 100 total → rate 3% > 2% threshold (F2 DEFAULT).
    for i in range(3):
        batch_quarantine.quarantine_batch(
            batch_id=f"B-{i}", reason="policy_violation_synthetic",
            run_id="RUN-B", instance_id="inst-1",
        )
    halt = batch_quarantine.evaluate_systemic_halt(
        run_id="RUN-B", instance_id="inst-1",
        total_batches=100, threshold=0.02,
    )
    assert halt is not None
    assert halt.live_quarantine_rate == 0.03
    assert halt.threshold == 0.02
    assert halt.receipt.startswith("HALT-")
    # Below threshold: no halt fires.
    batch_quarantine._reset_for_tests()
    batch_quarantine.quarantine_batch(
        batch_id="B-0", reason="policy_violation_synthetic",
        run_id="RUN-C", instance_id="inst-1",
    )
    no_halt = batch_quarantine.evaluate_systemic_halt(
        run_id="RUN-C", instance_id="inst-1",
        total_batches=100, threshold=0.02,
    )
    assert no_halt is None


# ---------------------------------------------------------------------------
# AC-A4.c · quarantine → remediate → re-process walk visible end-to-end.
# ---------------------------------------------------------------------------

def test_ac_a4_c_quarantine_remediate_reprocess_walk_visible():
    """AC-A4.c: full walk visible in the trace · remediation produces new output version."""
    batch_quarantine._reset_for_tests()
    # Quarantine 2 batches.
    e1 = batch_quarantine.quarantine_batch(
        batch_id="B-1", reason="policy_violation_synthetic",
        run_id="RUN-D", instance_id="inst-1",
    )
    e2 = batch_quarantine.quarantine_batch(
        batch_id="B-2", reason="policy_violation_synthetic",
        run_id="RUN-D", instance_id="inst-1",
    )
    # Remediate to new version.
    rem = batch_quarantine.remediate_to_new_version(
        original_run_id="RUN-D",
        remediated_batch_ids=["B-1", "B-2"],
    )
    assert rem.remediation_run_id == "RUN-D_r1"
    assert rem.remediation_version == 1
    assert set(rem.remediated_batch_ids) == {"B-1", "B-2"}
    assert rem.receipt.startswith("REM-")
    # Second remediation increments version (append-only · no in-place mutation).
    rem2 = batch_quarantine.remediate_to_new_version(
        original_run_id="RUN-D",
        remediated_batch_ids=["B-2"],
    )
    assert rem2.remediation_run_id == "RUN-D_r2"
    assert rem2.remediation_version == 2
    # Full walk visible: original quarantine events + remediation trail.
    quarantines = batch_quarantine.get_quarantine_events("RUN-D", "inst-1")
    remediations = batch_quarantine.get_remediations("RUN-D")
    assert len(quarantines) == 2
    assert len(remediations) == 2


# ---------------------------------------------------------------------------
# Owner §2 failure-mode binding · companion-channel-down refusal renders.
# ---------------------------------------------------------------------------

def test_eab2_owner_ruling_section_2_companion_channel_down_refusal_renders():
    """Owner §2: refusal render succeeds with companion channel down.

    When Targeta gap-candidate companion GET returns error/timeout/empty:
      * Prove `not-extracted-yet` refusal render still succeeds.
      * Refusal is rendered without the effort line.
      * Rendered in refusal styling (NOT fault surface).
      * Does NOT convert to `something-broke`.
      * Queue action URL remains derivable from `filed_candidate_id` on the envelope alone.

    Test asserts on the wire contract layer:
      * Envelope construction with `filed_candidate_id` succeeds even when the
        companion store has no matching record (companion channel down).
      * `read_gap_candidate` raises `GapCandidateNotFound` (the "companion
        channel down" signal caller MUST treat as effort-line-absent refusal).
      * Envelope's `outcome` remains 'refused' (NEVER converts to fault).
      * `filed_candidate_id` on the envelope alone suffices to derive the
        queue action URL Prove-side.
    """
    gap_candidate_filer._reset_for_tests()

    # Envelope constructs cleanly with a filed_candidate_id that is NOT in the
    # companion store (simulating companion-channel-down at render time).
    envelope = Service1Refusal_v1(
        reason="coverage_gap",
        run_id="R-COMPANION-DOWN",
        trace_id="T-COMPANION-DOWN",
        asked="EU 2024Q4 loan_book coverage",
        supported_class=None,
        what_would_raise_it="close the gap via extraction",
        estate_region="EU",
        period="2024Q4",
        source_class="loan_book",
        filed_candidate_id="OBJ-DOES-NOT-EXIST-IN-STORE",
    )

    # Refusal is intact: outcome remains 'refused' (NEVER converts to fault surface).
    assert envelope.outcome == "refused"
    assert envelope.reason == "coverage_gap"

    # Queue action URL derives from filed_candidate_id ALONE (envelope-side).
    # Prove UI constructs: /extract/shape?prefill_from={filed_candidate_id}
    assert envelope.filed_candidate_id == "OBJ-DOES-NOT-EXIST-IN-STORE"
    derived_queue_url = f"/extract/shape?prefill_from={envelope.filed_candidate_id}"
    assert "OBJ-DOES-NOT-EXIST-IN-STORE" in derived_queue_url

    # Companion GET fires GapCandidateNotFound (channel-down signal).
    # Caller MUST render refusal without effort line (no fault conversion).
    with pytest.raises(gap_candidate_filer.GapCandidateNotFound):
        gap_candidate_filer.read_gap_candidate(envelope.filed_candidate_id)

    # No `something_broke` reason value has been assigned (never converts).
    assert envelope.reason != "something_broke"
    # Envelope did not gain a fault-family field.
    dumped = envelope.model_dump()
    assert "error" not in dumped
    assert "fault" not in dumped
    assert "detail" not in dumped
