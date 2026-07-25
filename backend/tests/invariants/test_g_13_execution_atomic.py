"""G-13 execution atomic · pytest cells (surface-level + Class E pinned attest + ledger cells).

Owner ruling `docs/rulings/g_13_e1_e2_e3_2026_07_25.md` (2026-07-25 · FINAL · composition (b · a · a) + B-1/B-2/B-3).

Bindings B-1/B-2/B-3 discharge cells live at their dedicated test files:
  * B-1: `test_registry_context_block_golden_snapshot.py`
  * B-2: `test_mandate_spec_regeneration_diff.py`
  * B-3: `test_generated_gates_regeneration_diff.py` + `tests/rails/test_generated_gates_smoke.py`

This module lands the remaining execution-atomic attest cells.
"""
from __future__ import annotations

import hashlib
import pathlib
from typing import Any

import pytest

from contracts.mandate_spec_v0 import GateSpec, MandateSpec_v0
from services.sequencing_harness import (
    ENGINE_VERSION,
    REPETITION_COUNT,
    SIGNIFICANCE_ALPHA,
)
from services.sequencing_harness import emitter as sh_emitter
from services.sequencing_harness.enumerator import enumerate_candidate_orderings
from services.sequencing_harness.executor import RegisteredFunction, execute_registered_function
from services.sequencing_harness.measurement import (
    measure_deterministic,
    measure_statistical,
)
from services.sequencing_harness.optimizer import (
    FunctionCostRow,
    optimize_orderings,
    score_ordering,
)
from services.registry_context.injector import inject_context_into_prompt
from services.registry_context.prompt_builder import build_context_block
from services.registry_context.reader import known_function_ids, read_row
from services.registry_context.resolver import resolve_functions_in_scope


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent


# ---------------------------------------------------------------------------
# Owner ruling artifact byte-identity attest.
# ---------------------------------------------------------------------------

def test_owner_ruling_persisted_and_byte_identical():
    """Owner G-13 ruling persisted at docs/rulings/g_13_e1_e2_e3_2026_07_25.md · SHA byte-identical."""
    ruling_path = REPO_ROOT / "docs" / "rulings" / "g_13_e1_e2_e3_2026_07_25.md"
    assert ruling_path.exists(), f"Owner ruling missing: {ruling_path}"
    sha = hashlib.sha256(ruling_path.read_bytes()).hexdigest()
    EXPECTED = "6abdde0072affbe48758922330aa627ccd25767ac0674f44b1e89a51f49a64f7"
    assert sha == EXPECTED, (
        f"Owner ruling SHA drift · Standing Rule v3 breach.\n"
        f"  Expected: {EXPECTED}\n"
        f"  Actual  : {sha}"
    )


def test_predecessor_owner_rulings_byte_identical():
    """Standing Rule v3: prior Owner rulings remain byte-identical."""
    PRIOR_RULING_SHAS = {
        "docs/rulings/critic_pass_e1_2026_07_25.md":
            "42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a",
    }
    for rel_path, expected_sha in PRIOR_RULING_SHAS.items():
        path = REPO_ROOT / rel_path
        assert path.exists(), f"Prior ruling missing: {rel_path}"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == expected_sha, (
            f"Standing Rule v3 breach: {rel_path} SHA drift.\n"
            f"  Expected: {expected_sha}\n"
            f"  Actual  : {actual}"
        )


# ---------------------------------------------------------------------------
# Class E pinned-value attest (Owner ruling §5.5).
# ---------------------------------------------------------------------------

def test_class_e_repetition_count_pinned_at_ten():
    """Owner ruling §5.5 verbatim: 'Class E defaults N=10 [...] approved as pinned values on sequencing-harness-v0'."""
    assert REPETITION_COUNT == 10


def test_class_e_significance_alpha_pinned_at_five_percent():
    """Owner ruling §5.5 verbatim: 'Class E defaults [...] α=0.05 approved as pinned values on sequencing-harness-v0'."""
    assert SIGNIFICANCE_ALPHA == 0.05


def test_class_e_engine_version_pinned_sequencing_harness_v0():
    """Owner ruling verbatim: 'pinned values on sequencing-harness-v0'."""
    assert ENGINE_VERSION == "sequencing-harness-v0"


# ---------------------------------------------------------------------------
# Sequencing-harness rails (A.SH.1..A.SH.8).
# ---------------------------------------------------------------------------

def test_sequencing_harness_executor_runs_deterministic_gate():
    """A.SH.1: executor dispatches registered functions directly."""
    fn = RegisteredFunction(
        function_id="gate.X",
        rung="rung-1",
        callable_ref=lambda p: p.get("v", 0) * 2,
    )
    result = execute_registered_function(fn, {"v": 5})
    assert result == 10


def test_sequencing_harness_enumerator_respects_dependencies():
    """A.SH.2: enumerator only returns orderings satisfying dependency graph."""
    fns = ["a", "b", "c"]
    deps = {"b": {"a"}, "c": {"b"}}
    orderings = enumerate_candidate_orderings(fns, deps)
    assert orderings == [("a", "b", "c")]


def test_sequencing_harness_optimizer_prefers_deterministic_before_model():
    """A.SH.3: optimizer prefers rung-1 before rung-3."""
    rows = {
        "d1": FunctionCostRow("d1", "rung-1", 5.0, False),
        "m1": FunctionCostRow("m1", "rung-3", 50.0, False),
    }
    orderings = [("d1", "m1"), ("m1", "d1")]
    optimized = optimize_orderings(orderings, rows)
    assert optimized[0] == ("d1", "m1")


def test_sequencing_harness_measurement_deterministic_rung_1():
    """A.SH.5: rung-1/rung-2 exact measurement returns single-run verdict."""
    m = measure_deterministic(
        function_id="det.gate",
        rung="rung-1",
        fn=lambda p: p * 2,
        payload=3,
    )
    assert m.verdict == 6
    assert m.rung == "rung-1"
    assert m.wall_ms >= 0.0
    assert m.engine_version == "sequencing-harness-v0"


def test_sequencing_harness_measurement_statistical_rung_3_n_10():
    """A.SH.6: rung-3/rung-4 statistical measurement runs REPETITION_COUNT reps."""
    m = measure_statistical(
        function_id="stat.gate",
        rung="rung-3",
        fn=lambda p: p + 1,
        payload=0,
    )
    assert m.repetitions == 10  # matches Owner-ruled pinned N=10
    assert m.significance_alpha == 0.05  # matches Owner-ruled pinned α=0.05
    assert len(m.verdict_bag) == 10
    assert m.engine_version == "sequencing-harness-v0"


def test_sequencing_harness_ledger_append_only_immutable():
    """A.SH.7: measurement ledger rows are frozen dataclasses · append-only."""
    sh_emitter._reset_for_tests()
    row = sh_emitter.append_measurement(
        journey_id="j1",
        ordering=["a", "b"],
        total_wall_ms=1.0,
        per_function_wall_ms={"a": 0.5, "b": 0.5},
        ordering_score=(0, 0, 0.0),
        engine_version="sequencing-harness-v0",
    )
    assert row.row_id == 1
    with pytest.raises(Exception):
        row.row_id = 999  # frozen dataclass


def test_sequencing_harness_best_path_emitter_picks_best_score():
    """A.SH.8: measured-best-path emitter returns lowest-score row per journey."""
    sh_emitter._reset_for_tests()
    sh_emitter.append_measurement(
        "jY", ["a", "b"], 10.0, {"a": 5.0, "b": 5.0}, (0, 1, 0.0),
        "sequencing-harness-v0",
    )
    sh_emitter.append_measurement(
        "jY", ["b", "a"], 8.0, {"b": 3.0, "a": 5.0}, (0, 0, 0.0),
        "sequencing-harness-v0",
    )
    best = sh_emitter.emit_measured_best_path("jY")
    assert best is not None
    assert best.ordering == ("b", "a")


def test_sequencing_harness_registry_cost_backfill_aggregate():
    """A.SH.8: Registry cost back-fill map aggregates per-function mean wall_ms."""
    sh_emitter._reset_for_tests()
    sh_emitter.append_measurement(
        "j1", ["a"], 4.0, {"a": 4.0}, (0, 0, 0.0), "sequencing-harness-v0",
    )
    sh_emitter.append_measurement(
        "j2", ["a"], 6.0, {"a": 6.0}, (0, 0, 0.0), "sequencing-harness-v0",
    )
    backfill = sh_emitter.registry_cost_backfill_map()
    assert backfill["a"] == 5.0


# ---------------------------------------------------------------------------
# Worker context-harnessing (B.WCH.1..B.WCH.5).
# ---------------------------------------------------------------------------

def test_wch_resolver_returns_declared_list_deterministic():
    """B.WCH.1: resolver preserves declared order deterministic-ly."""
    ids = ["PROM-S1-frozen-wire-contract", "PROM-S3-append-only-ledger"]
    assert resolve_functions_in_scope(ids) == ids


def test_wch_reader_returns_triplet_for_known_id():
    """B.WCH.2: reader returns mandate + promise + service_trace triplet."""
    row = read_row("PROM-S1-frozen-wire-contract")
    assert len(row.mandate) > 0
    assert len(row.promise) > 0
    assert len(row.service_trace) > 0


def test_wch_injector_prepends_context_block():
    """B.WCH.3: injector prepends block above operating-prompt body."""
    body = "Do the thing."
    composed = inject_context_into_prompt(body, ["PROM-S1-frozen-wire-contract"])
    assert composed.endswith(body)
    assert "Registry context" in composed
    # Block above body (block appears BEFORE body in string).
    assert composed.index("Registry context") < composed.index(body)


def test_wch_three_role_attest_all_fields_present():
    """B.WCH.4: mandate + promise + service_trace present for every in-scope function."""
    for fn_id in known_function_ids():
        row = read_row(fn_id)
        assert row.mandate  # non-empty
        assert row.promise  # non-empty
        assert len(row.service_trace) >= 1  # at least one trace ref


# ---------------------------------------------------------------------------
# Far-endpoint round-trip attest (fold C.FE.4).
# ---------------------------------------------------------------------------

def test_c_fe_4_round_trip_mandate_to_spec_to_gate():
    """C.FE.4: every generated gate traces back to its source mandate line-anchor."""
    from services.far_endpoint.gate_generator import GENERATED_GATES_DIR
    from services.far_endpoint.mandate_reader import list_mandate_paths, parse_mandate
    from services.far_endpoint.mandate_spec_emitter import emit_mandate_spec

    for mandate_path in list_mandate_paths():
        parsed = parse_mandate(mandate_path)
        spec = emit_mandate_spec(parsed)
        module_path = GENERATED_GATES_DIR / f"{spec.spec_id}.py"
        assert module_path.exists()
        text = module_path.read_text()
        # Every generated gate function docstring cites its source anchor.
        for gate in spec.gates:
            assert gate.source_line_anchor in text, (
                f"Round-trip attest failed: gate {gate.gate_id} does not "
                f"cite source anchor {gate.source_line_anchor} in {module_path.name}"
            )


# ---------------------------------------------------------------------------
# Held D7 fence attest · sequencing-harness fresh-authoring discipline.
# ---------------------------------------------------------------------------

def test_held_d7_file_not_referenced_in_sequencing_harness_service():
    """STEP-2 Surfaces ruling verbatim (Surface 2 (a)): sequencing-harness authored fresh · zero content lifted from held D7 file.

    Test discipline: scan sequencing-harness service code for any RUNTIME
    read of the held D7 file (open/read_text/Path-of-marker). Mentions
    of the marker string inside module docstrings for discipline-attest
    are permitted (this is a fresh-authoring assertion, not a content lift).
    """
    sh_dir = BACKEND_ROOT / "services" / "sequencing_harness"
    held_d7_marker = "sequencing_harness_stage_a"
    for py_file in sh_dir.glob("*.py"):
        src = py_file.read_text()
        # Fail on any construct that would READ the held file at runtime.
        if held_d7_marker in src:
            # Docstring-only mention is permitted; test for structural usage.
            for line in src.split("\n"):
                stripped = line.strip()
                if held_d7_marker not in stripped:
                    continue
                # Runtime-read patterns: assignment/open/Path/read_text.
                dangerous_patterns = (
                    "open(", "Path(", "read_text(", ".read_bytes(",
                    "import ", "from ",
                )
                for pat in dangerous_patterns:
                    assert pat not in stripped, (
                        f"D-7 breach: {py_file.name} contains runtime read "
                        f"of held D7 file (pattern '{pat}' with marker "
                        f"'{held_d7_marker}'): {stripped[:120]}"
                    )


# ---------------------------------------------------------------------------
# MandateSpec@v0 landing attest.
# ---------------------------------------------------------------------------

def test_mandate_spec_v0_contract_landed():
    """§5.2 (a) landing: MandateSpec@v0 frozen contract exists at expected path."""
    spec_path = BACKEND_ROOT / "contracts" / "mandate_spec_v0.py"
    assert spec_path.exists()
    snap_path = BACKEND_ROOT / "tests" / "invariants" / "mandate_spec_v0.contract_snapshot.json"
    assert snap_path.exists()


def test_mandate_spec_v0_pydantic_construction():
    """MandateSpec@v0 constructs from valid fields."""
    spec = MandateSpec_v0(
        spec_id="test",
        source_mandate_path="docs/mandates/test.md",
        source_mandate_sha_256="0" * 64,
        mandate_title="Test",
        gates=[
            GateSpec(
                gate_id="test_gate_0",
                gate_kind="rail",
                condition_expr="payload must exist",
                refusal_reason="test refusal",
                source_line_anchor="docs/mandates/test.md#L1",
            ),
        ],
        generated_at="anchor",
    )
    assert spec.spec_id == "test"
    assert len(spec.gates) == 1


def test_mandate_spec_v0_snapshot_matches_schema():
    """MandateSpec@v0 snapshot byte-identical to model_json_schema() output."""
    import json
    snap_path = BACKEND_ROOT / "tests" / "invariants" / "mandate_spec_v0.contract_snapshot.json"
    on_disk = snap_path.read_text()
    fresh = json.dumps(MandateSpec_v0.model_json_schema(), indent=2, sort_keys=True)
    assert on_disk == fresh, (
        f"MandateSpec@v0 snapshot drift: on-disk snapshot does not match "
        f"model_json_schema() output. Regenerate with:\n"
        f"  python -c 'import json; from contracts.mandate_spec_v0 import MandateSpec_v0; "
        f"open(\"{snap_path}\", \"w\").write(json.dumps(MandateSpec_v0.model_json_schema(), indent=2, sort_keys=True))'"
    )


# ---------------------------------------------------------------------------
# Instance Replication Playbook document-class landing attest.
# ---------------------------------------------------------------------------

def test_instance_replication_playbook_landed():
    """§B.7 landing: playbook document exists at canonical path."""
    playbook_path = REPO_ROOT / "docs" / "mandates" / "instance_replication_playbook_v1.md"
    assert playbook_path.exists(), f"Playbook missing: {playbook_path}"
    text = playbook_path.read_text()
    # Playbook cites Registry Doctrine §8.1 line 159 verbatim (document-class discipline).
    assert "§8.1" in text or "8.1" in text
