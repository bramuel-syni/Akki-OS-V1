"""Fixture Refresh mini-phase gates — FR-G1..FR-G7 (2026-07-10).

Landed per Owner rulings FR-E1 α (fixture regenerate w/ neutralized content) +
FR-E2 α + 2 conditions (centralized single-source `license_classes.v1.json` +
distributed tables DELETED not shadowed + FR-G4 AST no-shadow-source gate) +
FR-E3 α (transform-golden snapshot re-blessed · historical closes preserved
byte-identical).

Gates:
  FR-G1 — `license_classes.v0.json` preserved byte-identical (append-only
          discipline; v0 stays; v1 is the new authoritative bless).
  FR-G2 — `license_classes.v1.json` present with expected feed_entries
          + valid_classes + commissioner_to_default_class + default_class
          + default_source_standing + default_bucket_category.
  FR-G3 — Loader reads highest-version file (v1 preferred);
          `is_valid_class` + `feed_id_to_license_class_map` +
          `get_source_standing_name` + `get_bucket_category` return
          values derived from v1.
  FR-G4 — AST/reflection gate (§6.10): no unaliased broadcaster feed_id
          string literal in NEW/MODIFIED service code introduced during
          Fixture Refresh. Grep-negative reflection over service modules
          (excluding archived rejected/ folder + tests/).
  FR-G5 — Adversarial fixture SHA attest — `fixture.json` regenerated
          with neutralized feed_ids (`feed_a..feed_h`); every unit's
          `provenance.context.feed_id` is in the neutralized alias set.
  FR-G6 — Test cascade parity: no residual broadcaster-name literals
          in the 10 identified test files (post-rename).
  FR-G7 — `outer_gate_transform.snapshot.json` re-bless attest:
          `canonical_input.feed_id` is neutralized; egress feed_id is
          a registered bucket_category.

Cell density: 7 backend cells (§6.1 classic amortised · ~12 LoC/cell).
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

import pytest


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend
SERVICES_ROOT = BACKEND_ROOT / "services"
CONFIG_DIR = SERVICES_ROOT / "service_1"


# Byte-identical v0 SHA-256 (recorded pre-Fixture-Refresh; must not drift
# per FR-E2 α cond 1). Sourced from prior on-disk state 2026-07-10.
LICENSE_CLASSES_V0_SHA = (
    "3351496c131578629dea34dddcc2a0cf6c5d5f98fe9a9719554ca9125526e841"
)


NEUTRALIZED_ALIASES = {
    "feed_a", "feed_b", "feed_c", "feed_d",
    "feed_e", "feed_f", "feed_g", "feed_h",
    "feed_i", "feed_j", "feed_k",
}


# Broadcaster feed_id literals that MUST NOT appear as string literals
# in NEW/MODIFIED service-tree code (FR-G4 no-shadow-source posture).
# Note: this set is defined ONLY inside this test's guarded scope; it
# does not count as a shadow source per FR-G4's own posture (tests are
# grep sinks, not runtime dispatch surfaces).
_BROADCASTER_LITERALS = (
    "citizen_tv_news", "citizen_archive", "citizen_drama",
    "wire_kna", "radio_jambo_callin", "aggregator_blog",
    "x_ingest", "ktn_news", "ntv_news", "print_edition",
)


# Test files updated during Fixture Refresh cascade — must be
# broadcaster-literal-free (FR-G6).
_CASCADE_TESTS = (
    "test_mtafiti_invariants.py",
    "test_dispatch_shape_responsive.py",
    "test_qualified_data_selection.py",
    "test_outer_gate_irreversibility.py",
    "test_qualified_data_outer_gate_ride.py",
    "test_phase_5_stage_b_async_delivery.py",
    "test_targeta_invariants.py",
    "test_trace_lens_cross_engine_correlation.py",
    "test_feasibility_honesty_under_absence.py",
    "test_composed_conclusion_dispatch.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---- FR-G1 ---------------------------------------------------------------
def test_fr_g1_license_classes_v0_byte_identical():
    """v0.json preserved byte-identical post-Fixture-Refresh (FR-E2 α
    condition 1 · append-only discipline).
    """
    v0 = CONFIG_DIR / "license_classes.v0.json"
    assert v0.exists(), "license_classes.v0.json missing"
    actual = _sha256(v0)
    assert actual == LICENSE_CLASSES_V0_SHA, (
        "FR-G1 violation — license_classes.v0.json drifted from "
        "recorded pre-Refresh SHA (append-only discipline broken).\n"
        f"  recorded SHA: {LICENSE_CLASSES_V0_SHA}\n"
        f"  actual  SHA: {actual}"
    )


# ---- FR-G2 ---------------------------------------------------------------
def test_fr_g2_license_classes_v1_present_with_expected_shape():
    """v1.json exists; carries centralized `feed_entries` + all required
    top-level fields.
    """
    v1 = CONFIG_DIR / "license_classes.v1.json"
    assert v1.exists(), "license_classes.v1.json missing (FR-E2 α)"
    cfg = json.loads(v1.read_text(encoding="utf-8"))
    for key in (
        "config_version", "valid_classes", "commissioner_to_default_class",
        "default_class", "default_source_standing",
        "default_bucket_category", "feed_entries",
    ):
        assert key in cfg, f"FR-G2: v1.json missing required field {key!r}"
    assert cfg["config_version"] == "v1"
    entries = cfg["feed_entries"]
    assert set(entries.keys()) == NEUTRALIZED_ALIASES, (
        f"FR-G2: feed_entries keys {sorted(entries)} != "
        f"expected neutralized aliases {sorted(NEUTRALIZED_ALIASES)}"
    )
    for feed_id, entry in entries.items():
        for col in ("license_class", "source_standing", "bucket_category"):
            assert col in entry, (
                f"FR-G2: entry {feed_id!r} missing column {col!r}"
            )


# ---- FR-G3 ---------------------------------------------------------------
def test_fr_g3_loader_reads_highest_version_v1():
    """Loader helper returns values derived from v1 (highest-version)."""
    from services.service_1 import license_class_selection as lc

    # is_valid_class reads valid_classes from v1
    assert lc.is_valid_class("editorial_use")
    assert lc.is_valid_class("syndication")
    assert lc.is_valid_class("training_data")
    assert not lc.is_valid_class("no_such_class")

    # feed_id_to_license_class_map is derived from v1 feed_entries
    m = lc.feed_id_to_license_class_map()
    assert set(m.keys()) == NEUTRALIZED_ALIASES
    assert m["feed_a"] == "editorial_use"
    assert m["feed_d"] == "training_data"
    assert m["feed_i"] == "syndication"

    # source_standing + bucket_category are derived from v1 feed_entries
    assert lc.get_source_standing_name("feed_a") == "accountable_tier1"
    assert lc.get_source_standing_name("feed_d") == "licensed_wire"
    assert lc.get_source_standing_name("nonexistent") == "unknown"
    assert lc.get_bucket_category("feed_a") == "broadcast_news"
    assert lc.get_bucket_category("feed_d") == "broadcast_wire"
    assert lc.get_bucket_category("nonexistent") == "unknown_broadcast_category"


# ---- FR-G4 ---------------------------------------------------------------
def test_fr_g4_no_shadow_source_broadcaster_literals_in_service_code():
    """AST/reflection §6.10 gate — no broadcaster feed_id string literal
    appears as a top-level constant OR argument literal in NEW code under
    services/ (excludes archived `rejected/` and `__pycache__`).

    A literal is considered a violation if it appears as either:
      (a) a string constant assigned to a module-level name; or
      (b) a string constant appearing inside a dict/list/tuple literal
          at module scope (shadow-source dict pattern).

    Test files, contracts/, routers/ NOT scanned (tests are grep-sinks;
    contracts frozen; router-layer strings are business-domain terms
    that don't shadow the registry).
    """
    violations = []
    for py in SERVICES_ROOT.rglob("*.py"):
        rel = py.relative_to(BACKEND_ROOT)
        if "__pycache__" in str(py) or "rejected" in str(py):
            continue
        text = py.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError:  # pragma: no cover — service tree parses
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value in _BROADCASTER_LITERALS:
                    line_no = getattr(node, "lineno", "?")
                    violations.append(
                        f"{rel}:{line_no}: broadcaster literal "
                        f"{node.value!r} appears in service code "
                        f"(FR-G4 no-shadow-source violation)"
                    )
    assert not violations, (
        "FR-G4 violation — broadcaster feed_id literals appear as string "
        "constants in services/ Python files. Distributed shadow tables "
        "were DELETED at Fixture Refresh per Owner FR-E2 α condition 2; "
        "feed_id → attribute lookup MUST route through the centralized "
        "v1 registry.\n" + "\n".join(violations)
    )


# ---- FR-G5 ---------------------------------------------------------------
def test_fr_g5_adversarial_fixture_uses_neutralized_feed_ids():
    """Every unit in the regenerated adversarial fixture carries a
    neutralized `feed_id` in its provenance.context envelope.
    """
    fx = (
        BACKEND_ROOT
        / "services" / "data_source" / "synthetic_assets"
        / "rms_adversarial_v1" / "fixture.json"
    )
    corpus = json.loads(fx.read_text(encoding="utf-8"))
    assert corpus.get("_manifest", {}).get("synthetic") is True
    for unit in corpus["units"]:
        ctx = json.loads(unit["provenance"]["context"])
        fid = ctx["feed_id"]
        assert fid in NEUTRALIZED_ALIASES, (
            f"FR-G5: fixture unit {unit['unit_id']} carries "
            f"non-neutralized feed_id {fid!r}"
        )


# ---- FR-G6 ---------------------------------------------------------------
def test_fr_g6_test_cascade_carries_no_residual_broadcaster_literals():
    """None of the 10 cascade test files retain broadcaster string
    literals post-rename (mechanical sed).
    """
    tests_dir = Path(__file__).resolve().parent
    violations = []
    pattern = re.compile(
        r'["\'](' + "|".join(re.escape(s) for s in _BROADCASTER_LITERALS) + r')["\']'
    )
    for fname in _CASCADE_TESTS:
        p = tests_dir / fname
        assert p.exists(), f"cascade test file {fname!r} missing"
        text = p.read_text(encoding="utf-8")
        for m in pattern.finditer(text):
            line_no = text[:m.start()].count("\n") + 1
            violations.append(
                f"{fname}:{line_no}: residual broadcaster literal "
                f"{m.group(1)!r}"
            )
    assert not violations, (
        "FR-G6 violation — broadcaster literals persist in cascade "
        "test files post-Fixture-Refresh rename.\n" + "\n".join(violations)
    )


# ---- FR-G7 ---------------------------------------------------------------
def test_fr_g7_outer_gate_transform_snapshot_reblessed_neutralized():
    """`outer_gate_transform.snapshot.json` `canonical_input.feed_id`
    is a neutralized alias; egress `feed_id` is a registered
    bucket_category (drawn from the centralized v1 registry).
    """
    snap_path = (
        BACKEND_ROOT
        / "tests" / "invariants" / "outer_gate_transform.snapshot.json"
    )
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    canonical_feed = snap["canonical_input"]["feed_id"]
    assert canonical_feed in NEUTRALIZED_ALIASES, (
        f"FR-G7: canonical_input.feed_id {canonical_feed!r} "
        f"is not a neutralized alias"
    )
    egress_feed = snap["egress_artifact"]["feed_id"]
    # Egress must be a bucket_category (not the raw feed_id).
    assert egress_feed != canonical_feed
    # Confirm the egress bucket is a registered value in v1.
    from services.service_1 import license_class_selection as lc
    known_buckets = {
        entry["bucket_category"]
        for entry in lc._feed_entries().values()  # noqa: SLF001
    }
    known_buckets.add("unknown_broadcast_category")  # default
    assert egress_feed in known_buckets, (
        f"FR-G7: egress feed_id bucket {egress_feed!r} not in "
        f"registered set {sorted(known_buckets)}"
    )
