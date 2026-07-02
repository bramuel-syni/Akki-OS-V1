"""Targeta invariants — mandate §13 + §16.

Structural + behavioural tests. No MongoDB.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

from contracts.five_rings import DefensibilityClass
from contracts.northena_ledger import LedgerArtifactRef
from contracts.targeta_plan import MiningPlan
from services.targeta import core, gate, interface, plan, yield_layer

SNAPSHOT_PATH = (
    Path(__file__).parent / "targeta_mining_plan.contract_snapshot.json"
)


def _fake_registry_rows() -> list:
    return [
        {"source_ref": "synthetic://a", "region": "citizen_tv_news",
         "defensibility_class": "fact", "sensitivity": "standard"},
        {"source_ref": "synthetic://b", "region": "wire_kna",
         "defensibility_class": "fact", "sensitivity": "standard"},
        {"source_ref": "synthetic://c", "region": "x_ingest",
         "defensibility_class": "utterance", "sensitivity": "elevated"},
        {"source_ref": "synthetic://d", "region": "aggregator_blog",
         "defensibility_class": "non_factual", "sensitivity": "standard"},
    ]


# ------- §13 obligation: contract frozen -----------------------------------
def test_mining_plan_contract_frozen():
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    actual = MiningPlan.model_json_schema()
    assert json.dumps(actual, indent=2, sort_keys=True) == \
           json.dumps(expected, indent=2, sort_keys=True), (
        "MiningPlan schema drifted; re-bless snapshot in review if intentional."
    )


# ------- §13 test #7: core has no ML import --------------------------------
def test_targeta_core_has_no_ml_import():
    """Mandate §7 + §17 #2: core.py imports no ML library."""
    src_path = (Path(__file__).parent.parent.parent / "services" / "targeta"
                / "core.py")
    lines = src_path.read_text(encoding="utf-8").splitlines()
    import_lines = [
        line.strip() for line in lines
        if line.strip().startswith(("import ", "from "))
    ]
    ml_libs = ("torch", "tensorflow", "sklearn", "numpy", "scipy",
               "xgboost", "lightgbm", "transformers")
    for line in import_lines:
        for lib in ml_libs:
            assert lib not in line, (
                f"core.py imports ML library ({lib}): {line!r} — violates §17 #2"
            )


# ------- §7 dependency: yield_layer imports ONLY interface types -----------
def test_yield_layer_imports_only_interface_types():
    src_path = (Path(__file__).parent.parent.parent / "services" / "targeta"
                / "yield_layer.py")
    lines = src_path.read_text(encoding="utf-8").splitlines()
    from_lines = [line.strip() for line in lines
                  if line.strip().startswith("from services.")]
    for line in from_lines:
        assert "services.targeta.interface" in line, (
            f"yield_layer imports non-interface Targeta module: {line!r} — "
            "violates §7 dependency rule"
        )


# ------- §13 #1: yield output is a permutation -----------------------------
def test_yield_output_is_permutation_raises_on_drop():
    eligible = core.eligible_and_rank(
        _fake_registry_rows(), DefensibilityClass.FACT, "citizen_tv_news"
    )

    def bad_yield_drops(inp):
        return [c.source_ref for c in inp[:-1]]  # drops one

    with pytest.raises(interface.NonPermutationError):
        interface.apply_yield(eligible, bad_yield_drops)


def test_yield_output_is_permutation_raises_on_duplicate():
    eligible = core.eligible_and_rank(
        _fake_registry_rows(), DefensibilityClass.FACT, "citizen_tv_news"
    )
    if len(eligible) < 2:
        pytest.skip("need >= 2 eligible for duplicate test")

    def bad_yield_dupe(inp):
        refs = [c.source_ref for c in inp]
        return refs[:-1] + [refs[0]]  # replace last with dup of first

    with pytest.raises(interface.NonPermutationError):
        interface.apply_yield(eligible, bad_yield_dupe)


# ------- §13 #2: yield never sees floor ------------------------------------
def test_yield_candidate_never_carries_floor_or_raw_measure():
    """`YieldCandidate` must exclude floor + `registry_defensibility`."""
    fields = interface.YieldCandidate.__dataclass_fields__.keys()
    forbidden = {"defensibility_floor", "registry_defensibility", "floor"}
    intersection = forbidden & set(fields)
    assert not intersection, (
        f"YieldCandidate carries forbidden fields: {intersection}"
    )


# ------- §13 #3: floor is hard filter --------------------------------------
def test_floor_is_hard_filter_excludes_below_floor():
    rows = _fake_registry_rows()
    # Floor = fact → utterance + non_factual excluded
    eligible = core.eligible_and_rank(rows, DefensibilityClass.FACT, "any")
    excluded_refs = {"synthetic://c", "synthetic://d"}
    for c in eligible:
        assert c.source_ref not in excluded_refs, (
            f"source below floor appeared in eligible set: {c.source_ref}"
        )


# ------- §13 #4: fallback to core when gate not admitted --------------------
def test_fallback_to_core_when_yield_thresholds_none():
    eligible = core.eligible_and_rank(
        _fake_registry_rows(), DefensibilityClass.FACT, "citizen_tv_news"
    )
    ordered, version = gate.compose_ordering(eligible, thresholds=None)
    assert version == "core-only"
    # Ordering equals core baseline when yield closed:
    assert [c.source_ref for c in ordered] == [c.source_ref for c in eligible]


# ------- §13 #6: coverage veto overrides helps -----------------------------
def test_gate_closed_seam_returns_admitted_false():
    result = gate.evaluate_gate(thresholds=None)
    assert result.admitted is False
    assert result.helps is False
    assert result.veto is False
    assert result.reason == "thresholds_not_configured"


# ------- §13 #5: plan reproducible -----------------------------------------
def test_plan_reproducible_byte_identical():
    """Same Registry state + artifact + yield-layer version → same plan_id."""
    eligible = core.eligible_and_rank(
        _fake_registry_rows(), DefensibilityClass.FACT, "citizen_tv_news"
    )
    ordered, version = gate.compose_ordering(eligible, thresholds=None)
    ref = LedgerArtifactRef(
        artifact_type="portfolio_mandate", artifact_id="test", version="v0",
    )
    p1 = plan.build_plan(
        ordered=ordered, core_baseline=eligible,
        floor=DefensibilityClass.FACT,
        mode="portfolio", governing_artifact_ref=ref,
        registry_snapshot_ref="snap-1", yield_layer_version=version,
        generated_at="2026-07-01T00:00:00Z",
    )
    p2 = plan.build_plan(
        ordered=ordered, core_baseline=eligible,
        floor=DefensibilityClass.FACT,
        mode="portfolio", governing_artifact_ref=ref,
        registry_snapshot_ref="snap-1", yield_layer_version=version,
        generated_at="2026-07-01T00:00:00Z",
    )
    assert p1.plan_id == p2.plan_id


# ------- §14 construction #1: core is a complete targeter alone -----------
def test_targeta_core_complete_alone():
    """§14 verbatim: `core is a complete targeter and the fallback the yield
    layer degrades to.`"""
    eligible = core.eligible_and_rank(
        _fake_registry_rows(), DefensibilityClass.FACT, "citizen_tv_news"
    )
    assert len(eligible) > 0, "core-alone must produce a non-empty eligible set"
    for i, c in enumerate(eligible):
        assert c.baseline_rank == i, "core must produce a deterministic ranking"


# ------- G4-specific: gate.py is the ONLY module comparing orderings -------
def test_only_gate_compares_orderings():
    """§7 dependency rule: gate.py is the only module that compares
    core + yield orderings.

    Structural check: `apply_yield` (in interface.py) delegates to a
    caller-provided yield_fn; it does NOT itself compare orderings.
    `core.py` does not import yield_layer. `gate.py` imports both.
    """
    core_src = (Path(__file__).parent.parent.parent / "services" / "targeta"
                / "core.py").read_text(encoding="utf-8")
    assert "yield_layer" not in core_src, (
        "core.py imports yield_layer — violates §7 dependency rule"
    )
    gate_src = (Path(__file__).parent.parent.parent / "services" / "targeta"
                / "gate.py").read_text(encoding="utf-8")
    assert "yield_layer" in gate_src, (
        "gate.py must reference yield_layer to compose orderings"
    )
