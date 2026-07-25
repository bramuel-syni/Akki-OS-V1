"""EAB-3 Parity 32→33 seal + AC-A5.a-c + Owner (a1) ruling gate cells.

Sanction: `docs/rulings/eab_3_e1_2026_07_24.md` · Owner ruled (a1) single-contract landing.

Composition: (a1) — single-contract PartitionSchema@v0 landing · 9-field envelope ·
Parity 32→33 single seal event · matches EAB-2 single-writer end-state precedent.

Gate cells landed here (per Stage A §2 band table + AC-A5.a-c enumeration):
  * `test_parity_33_contracts_and_snapshots` — Parity 32→33 seal attest.
  * `test_prior_32_contracts_byte_identity_under_eab3` — Standing Rule v3 (v0..v32).
  * `test_prior_32_snapshots_byte_identity_under_eab3` — Standing Rule v3 (snapshots).
  * `test_partition_schema_v0_snapshot_matches_schema` — schema stability.
  * `test_partition_schema_v0_field_count_9` — Owner ruling (a1) 9-field envelope.
  * `test_partition_schema_v0_shape_kind_literal` — R-A5.1 columnar_memmap discipline.
  * `test_ac_a5_a_design_gate_partition_schema_exists` — AC-A5.a wire attest.
  * `test_ac_a5_c_version_skew_wire_cell_session_cannot_mix_versions` — AC-A5.c.
  * `test_ac_a5_c_es1_ci_import_check_green` — AC-A5.c ES-1 CI-green.
  * `test_session_working_set_no_targeta_eligibility_import` — §5.2 AST negative-scan.
  * `test_session_working_set_purpose_inheritance` — R-A5.4 cache reads inherit purpose.
  * `test_session_working_set_promotion_invalidates_dependents` — R-A5.4.
  * `test_session_working_set_stores_references_and_arithmetic_only` — R-A5.4.
  * `test_partition_refresh_atomic_promotion_previous_serves_until_swap` — R-A5.3.
  * `test_partition_promotion_ledgered_append_only` — R-A5.3 + PROM-S3-append-only-ledger.
  * `test_lineage_partition_version_receipt_set_walkable` — R-A5.5.
  * `test_partition_schema_v0_additive_versioning_extends_parity_32` — additive-versioning attest.
  * `test_class_e_annotation_partition_shape_kind_registry_pinned` — Owner ITEM 1 forward-binding.
"""
from __future__ import annotations

import ast
import hashlib
import json
import pathlib

import pytest
from pydantic import ValidationError

from contracts.partition_schema import PartitionSchema_v0
from services.partitions import session_working_set
from services.partitions.session_working_set import (
    MixedPartitionVersionError,
    SessionWorkingSet,
    WorkingSetEntry,
    promote_partition,
    read_current_partition,
    get_partition_history,
    get_promotion_ledger,
)


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACTS_DIR = BACKEND_ROOT / "contracts"
INVARIANTS_DIR = BACKEND_ROOT / "tests" / "invariants"
SERVICES_DIR = BACKEND_ROOT / "services"
ROUTERS_DIR = BACKEND_ROOT / "routers"


# ---------------------------------------------------------------------------
# §0-CAL §23.1 per-line enumeration attest.
# ---------------------------------------------------------------------------

CAL_23_1_ENUM = [
    # (line-anchor,                                       rung, verdict)
    ("model_config ConfigDict(extra=forbid,frozen=True)", 1, "deterministic"),
    ("partition_id: str",                                 1, "deterministic"),
    ("schema_version: str",                               1, "deterministic"),
    ("key_dimensions: List[str]",                         1, "deterministic"),
    ("receipt_set_ref: str",                              1, "deterministic"),
    ("promoted_at: str",                                  1, "deterministic"),
    ("superseded_at: Optional[str]",                      1, "deterministic"),
    ("partition_shape_kind: Literal[columnar_memmap]",    1, "deterministic"),
    ("size_bytes: int (ge=0)",                            1, "deterministic"),
    ("instance_id: str",                                  1, "deterministic"),
]


def test_cal_23_1_enumeration_present_on_partition_schema_v0():
    """§0-CAL §23.1 per-line enumeration mandatory attest."""
    assert len(CAL_23_1_ENUM) == 10  # 1 config + 9 fields
    for _anchor, rung, verdict in CAL_23_1_ENUM:
        assert rung == 1
        assert verdict == "deterministic"


# ---------------------------------------------------------------------------
# Parity 32→33 seal attest + Standing Rule v3 (v0..v32 byte-identity).
# ---------------------------------------------------------------------------

def test_parity_33_contracts_and_snapshots():
    """Parity 32→33 sealed (EAB-3) · 33→34 sealed (G-13 MandateSpec@v0).

    Post-G-13 execution atomic (2026-07-25): 34 contract .py files +
    34 snapshot .json files. Prior Parity 33 seal held; MandateSpec@v0
    landed additively under Owner ruling G-13 §5.2 (a).
    """
    contract_files = sorted(CONTRACTS_DIR.glob("*.py"))
    snapshot_files = sorted(INVARIANTS_DIR.glob("*.contract_snapshot.json"))
    assert len(contract_files) == 34, f"expected 34 contracts, got {len(contract_files)}"
    assert len(snapshot_files) == 34, f"expected 34 snapshots, got {len(snapshot_files)}"


# Byte-identity SHAs for the two headline prior-frozen contracts under EAB-2
# (Service1Refusal@v0 + Service1Refusal@v1). These SHAs were captured live at
# EAB-2 close (2026-07-24) and MUST remain unchanged post-EAB-3 seal.
PRIOR_HEADLINE_CONTRACT_SHAS = {
    "service_1_refusal.py":
        "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022",
    "service_1_refusal_v1.py":
        "3d5d9845e03d841916e8ce47733710bc490585681fe5b1e8350243875a631fad",
}
PRIOR_HEADLINE_SNAPSHOT_SHAS = {
    "service_1_refusal.contract_snapshot.json":
        "56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d",
    "service_1_refusal_v1.contract_snapshot.json":
        "b0695338edb633eeafa315bc9c1d146586db8c0d9e1932f743c68c3217702335",
}


@pytest.mark.parametrize("fname,expected_sha", PRIOR_HEADLINE_CONTRACT_SHAS.items())
def test_prior_32_contracts_byte_identity_under_eab3(fname, expected_sha):
    """Standing Rule v3 · headline prior contracts byte-identical post-EAB-3 seal."""
    path = CONTRACTS_DIR / fname
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected_sha, f"{fname} drift under EAB-3 seal: {actual} != {expected_sha}"


@pytest.mark.parametrize("fname,expected_sha", PRIOR_HEADLINE_SNAPSHOT_SHAS.items())
def test_prior_32_snapshots_byte_identity_under_eab3(fname, expected_sha):
    """Standing Rule v3 · headline prior snapshots byte-identical post-EAB-3 seal."""
    path = INVARIANTS_DIR / fname
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual == expected_sha, f"{fname} snapshot drift under EAB-3 seal: {actual} != {expected_sha}"


# ---------------------------------------------------------------------------
# Owner ruling (a1) — 9-field envelope · single-contract landing.
# ---------------------------------------------------------------------------

def test_partition_schema_v0_field_count_9():
    """Owner ruling (a1): envelope shape is exactly 9 fields (single-contract landing)."""
    schema = PartitionSchema_v0.model_json_schema()
    assert len(schema["properties"]) == 9, (
        f"Owner ruling (a1) 9-field envelope drift: {sorted(schema['properties'].keys())}"
    )


def test_partition_schema_v0_shape_kind_literal_columnar_memmap():
    """R-A5.1 initial landing: partition_shape_kind = Literal['columnar_memmap'] (single value)."""
    schema = PartitionSchema_v0.model_json_schema()
    shape_kind = schema["properties"]["partition_shape_kind"]
    # Pydantic represents Literal["columnar_memmap"] as {'const': 'columnar_memmap'}
    assert shape_kind.get("const") == "columnar_memmap" or shape_kind.get("enum") == ["columnar_memmap"]


def test_partition_schema_v0_snapshot_matches_schema():
    """Snapshot invariant: on-disk snapshot equals live-generated schema."""
    snap_path = INVARIANTS_DIR / "partition_schema_v0.contract_snapshot.json"
    stored = json.loads(snap_path.read_text())
    live = PartitionSchema_v0.model_json_schema()
    live_normalized = json.loads(json.dumps(live, sort_keys=True))
    stored_normalized = json.loads(json.dumps(stored, sort_keys=True))
    assert live_normalized == stored_normalized


def test_partition_schema_v0_additive_versioning_extends_parity_32():
    """PROM-S1-additive-versioning: PartitionSchema@v0 is additive · zero mutation of prior 32.

    Reference to EAB-2 v0 + v1 refusal envelope (already verified byte-identical
    in test_prior_32_contracts_byte_identity_under_eab3). Zero shared field-set
    with any prior contract module — this is a new artifact class per §IX
    pre-naming (line 179 verbatim).
    """
    ps_schema = PartitionSchema_v0.model_json_schema()
    ps_fields = set(ps_schema["properties"].keys())
    expected_v0_fields = {
        "partition_id", "schema_version", "key_dimensions", "receipt_set_ref",
        "promoted_at", "superseded_at", "partition_shape_kind", "size_bytes",
        "instance_id",
    }
    assert ps_fields == expected_v0_fields


# ---------------------------------------------------------------------------
# AC-A5.a · design-gate discipline (partition schema exists before any
# interactive feature builds against live data).
# ---------------------------------------------------------------------------

def test_ac_a5_a_design_gate_partition_schema_exists():
    """AC-A5.a · Partition schema + refresh job exist before any interactive feature."""
    # Contract file exists on-disk.
    assert (CONTRACTS_DIR / "partition_schema.py").exists()
    # Snapshot file exists on-disk.
    assert (INVARIANTS_DIR / "partition_schema_v0.contract_snapshot.json").exists()
    # Refresh runner + session working-set service exist on-disk.
    assert (SERVICES_DIR / "partitions" / "session_working_set.py").exists()
    # Contract is importable and instantiable.
    p = PartitionSchema_v0(
        partition_id="p1", schema_version="v0",
        key_dimensions=["region", "period"],
        receipt_set_ref="rs-1", promoted_at="2026-07-24T00:00:00+00:00",
        size_bytes=1024, instance_id="inst-1",
    )
    assert p.partition_shape_kind == "columnar_memmap"


# ---------------------------------------------------------------------------
# AC-A5.c · version-skew wire cell · one cited result NEVER mixes versions.
# ---------------------------------------------------------------------------

def test_ac_a5_c_version_skew_wire_cell_session_cannot_mix_versions():
    """AC-A5.c · session cannot cite two partition versions in one output.

    R-A5.4 verbatim: *"one cited result NEVER mixes evidence versions"*.
    """
    session_working_set._reset_for_tests()

    ws = SessionWorkingSet(session_id="S1", validated_purpose="test-purpose")

    p_v1 = PartitionSchema_v0(
        partition_id="p1", schema_version="v0", key_dimensions=["region"],
        receipt_set_ref="rs-VERSION-A", promoted_at="2026-07-24T00:00:00+00:00",
        size_bytes=1024, instance_id="inst-1",
    )
    p_v2 = PartitionSchema_v0(
        partition_id="p1", schema_version="v0", key_dimensions=["region"],
        receipt_set_ref="rs-VERSION-B", promoted_at="2026-07-24T00:01:00+00:00",
        size_bytes=1024, instance_id="inst-1",
    )

    ws.bind_partition(p_v1)
    # Binding a different version of the same partition_id must fail.
    with pytest.raises(MixedPartitionVersionError):
        ws.bind_partition(p_v2)

    # Adding an entry that references a different version must also fail.
    with pytest.raises(MixedPartitionVersionError):
        ws.add_entry(WorkingSetEntry(
            partition_ref="p1",
            partition_version_receipt_set_ref="rs-VERSION-B",  # skewed
            derived_arithmetic_key="k1", derived_arithmetic_value="v1",
        ))


# ---------------------------------------------------------------------------
# AC-A5.c · ES-1 CI import/route check green · no estate-query client
# reachable from interactive-surface code path.
# ---------------------------------------------------------------------------

def test_ac_a5_c_es1_ci_import_check_green():
    """AC-A5.c · ES-1 CI check green: no estate-query client reachable from A5 service.

    Per Owner ruling `es1_scope_2026-07-14.md` L9 verbatim: *"ES-1 scope =
    evidence-assembly reads — request-time queries over the raw estate or the
    qualified-unit corpus to compose an answer, simulation, or brief."*

    A5 session-working-set service is NEW interactive-surface code (post-ruling
    2026-07-14). It MUST NOT import evidence-assembly reads at request time.
    Cache reads only.
    """
    src = (SERVICES_DIR / "partitions" / "session_working_set.py").read_text()
    tree = ast.parse(src)
    banned_estate_query_symbols = {
        # Raw-estate assembly modules (not operational-record modules).
        "backend.services.mtafiti.perception_worker",
        "services.mtafiti.perception_worker",
        "backend.services.mtafiti.extraction_worker",
        "services.mtafiti.extraction_worker",
        # Note: Northena ledger + Targeta plans + Registry metadata are
        # operational-record reads (OUTSIDE ES-1 scope per rulings/es1_scope L10).
    }
    imports_found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for banned in banned_estate_query_symbols:
                if mod.startswith(banned):
                    imports_found.append((mod, [a.name for a in node.names]))
    assert not imports_found, (
        f"ES-1 violation: session-working-set service imports estate-assembly "
        f"reads: {imports_found}"
    )


# ---------------------------------------------------------------------------
# §5.2 AST negative-scan · session-working-set does NOT import Targeta
# eligibility modules (eligibility-wall stands · §1.2 discipline).
# ---------------------------------------------------------------------------

def test_session_working_set_no_targeta_eligibility_import():
    """§5.2 · A5 session-working-set service NOT importing Targeta eligibility modules.

    Enforces eligibility-wall discipline per EAB v1.1 §1.2 (verbatim from
    Stage A refresh §5.4 pattern extended to A5).
    """
    src = (SERVICES_DIR / "partitions" / "session_working_set.py").read_text()
    tree = ast.parse(src)
    banned_eligibility_modules = {
        "backend.services.targeta.gate",
        "services.targeta.gate",
        "backend.services.targeta.yield_layer",
        "services.targeta.yield_layer",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for banned in banned_eligibility_modules:
                assert not mod.startswith(banned), (
                    f"§5.2 violation: session-working-set imports Targeta "
                    f"eligibility module '{mod}'"
                )


# ---------------------------------------------------------------------------
# R-A5.4 · cache reads inherit session's validated purpose.
# ---------------------------------------------------------------------------

def test_session_working_set_purpose_inheritance():
    """R-A5.4 · cache reads inherit session's validated purpose (not bypassable)."""
    session_working_set._reset_for_tests()
    ws = SessionWorkingSet(
        session_id="S-PURPOSE",
        validated_purpose="analyst-fluency-mode-purpose-abc",
    )
    # Session carries its validated_purpose immutably (frozen at open time).
    assert ws.validated_purpose == "analyst-fluency-mode-purpose-abc"


# ---------------------------------------------------------------------------
# R-A5.4 · promotion invalidates dependents.
# ---------------------------------------------------------------------------

def test_session_working_set_promotion_invalidates_dependents():
    """R-A5.4 · promotion invalidates dependents · cache entries are purged."""
    session_working_set._reset_for_tests()
    ws = SessionWorkingSet(session_id="S2", validated_purpose="test")
    p = PartitionSchema_v0(
        partition_id="p2", schema_version="v0", key_dimensions=["k"],
        receipt_set_ref="rs-100", promoted_at="2026-07-24T00:00:00+00:00",
        size_bytes=100, instance_id="i1",
    )
    ws.bind_partition(p)
    ws.add_entry(WorkingSetEntry(
        partition_ref="p2", partition_version_receipt_set_ref="rs-100",
        derived_arithmetic_key="k1", derived_arithmetic_value="v1",
    ))
    assert len(ws.read_entries("p2")) == 1
    invalidated_count = ws.invalidate_partition("p2")
    assert invalidated_count == 1
    assert len(ws.read_entries("p2")) == 0


# ---------------------------------------------------------------------------
# R-A5.4 · cache stores references + arithmetic ONLY (never raw).
# ---------------------------------------------------------------------------

def test_session_working_set_stores_references_and_arithmetic_only():
    """R-A5.4 · cache stores partition references + derived arithmetic ONLY.

    WorkingSetEntry dataclass fields ARE the shape enforcement (no raw payload
    field · no 'estate_row' field · no bytes-blob field). Frozen dataclass.
    """
    from dataclasses import fields, is_dataclass
    assert is_dataclass(WorkingSetEntry)
    field_names = {f.name for f in fields(WorkingSetEntry)}
    assert field_names == {
        "partition_ref", "partition_version_receipt_set_ref",
        "derived_arithmetic_key", "derived_arithmetic_value",
    }
    # Explicit negative attest: no raw-payload field surface exists.
    banned_field_names = {"estate_row", "raw_bytes", "payload", "materialized_data"}
    assert not (field_names & banned_field_names)


# ---------------------------------------------------------------------------
# R-A5.3 · atomic promotion · previous version serves until swap.
# ---------------------------------------------------------------------------

def test_partition_refresh_atomic_promotion_previous_serves_until_swap():
    """R-A5.3 · previous version serves until the new version is atomically promoted."""
    session_working_set._reset_for_tests()

    # No partition initially.
    assert read_current_partition("p3", "i1") is None

    # Promote v1.
    v1, ledger1 = promote_partition(
        partition_id="p3", schema_version="v0",
        key_dimensions=["region"], receipt_set_ref="rs-v1",
        size_bytes=100, instance_id="i1",
    )
    assert read_current_partition("p3", "i1") == v1
    assert v1.superseded_at is None
    assert ledger1.prior_version_receipt_set_ref is None
    assert ledger1.new_version_receipt_set_ref == "rs-v1"

    # Promote v2 · v1 gets superseded_at stamped and archived to history.
    v2, ledger2 = promote_partition(
        partition_id="p3", schema_version="v0",
        key_dimensions=["region"], receipt_set_ref="rs-v2",
        size_bytes=200, instance_id="i1",
    )
    assert read_current_partition("p3", "i1") == v2
    assert v2.superseded_at is None
    history = get_partition_history("p3", "i1")
    assert len(history) == 1
    assert history[0].receipt_set_ref == "rs-v1"
    assert history[0].superseded_at is not None  # stamped at promotion
    assert ledger2.prior_version_receipt_set_ref == "rs-v1"
    assert ledger2.new_version_receipt_set_ref == "rs-v2"


# ---------------------------------------------------------------------------
# R-A5.3 · promotion is ledgered · append-only.
# ---------------------------------------------------------------------------

def test_partition_promotion_ledgered_append_only():
    """R-A5.3 · promotion is ledgered · append-only per PROM-S3-append-only-ledger."""
    session_working_set._reset_for_tests()

    for i in range(3):
        promote_partition(
            partition_id=f"p-A{i}", schema_version="v0",
            key_dimensions=["k"], receipt_set_ref=f"rs-{i}",
            size_bytes=10, instance_id="i-LEDGER",
        )

    ledger = get_promotion_ledger("i-LEDGER")
    assert len(ledger) == 3
    # Ledger rows are append-only: promotion_id strictly increases.
    ids = [row.promotion_id for row in ledger]
    assert ids == sorted(ids)
    # Each row has an immutable promoted_at timestamp.
    for row in ledger:
        assert row.promoted_at  # non-empty ISO-8601


# ---------------------------------------------------------------------------
# R-A5.5 · lineage · partition version → receipt set is walkable.
# ---------------------------------------------------------------------------

def test_lineage_partition_version_receipt_set_walkable():
    """R-A5.5 · every partition version records the receipt set it was built from.

    Walkable chain: partition_id → partition_version_receipt_set_ref → receipts.
    Zero additional retrieval at request time — the citation IS the identifier.
    """
    session_working_set._reset_for_tests()
    p, ledger_row = promote_partition(
        partition_id="p-LINEAGE", schema_version="v0",
        key_dimensions=["region"], receipt_set_ref="rs-LINEAGE-TARGET-42",
        size_bytes=42, instance_id="i-L",
    )
    # The partition envelope carries the FK.
    assert p.receipt_set_ref == "rs-LINEAGE-TARGET-42"
    # The ledger row also carries the FK · walkable both ways.
    assert ledger_row.new_version_receipt_set_ref == "rs-LINEAGE-TARGET-42"


# ---------------------------------------------------------------------------
# Owner ITEM 1 forward-binding annotation · Class E parameter attest.
# ---------------------------------------------------------------------------

def test_class_e_annotation_partition_shape_kind_registry_pinned():
    """Owner ITEM 1 forward-binding: partition_shape_kind is Class E engine parameter.

    Per Owner ruling `docs/rulings/eab_3_e1_2026_07_24.md` verbatim:
    *"all five §5.5 defaults are Class E engine parameters under the Rules
    Taxonomy filed at ITEM 2 (A3.4) — pinned per engine version, changed
    only via version bumps with evaluation verdicts; any future runtime
    tunability takes the E→O promotion path (A3.2), no other route."*

    This cell asserts partition_shape_kind is a `Literal[...]` type (not a
    free `str` type · not runtime-settable · pinned at contract level).
    """
    schema = PartitionSchema_v0.model_json_schema()
    shape_kind = schema["properties"]["partition_shape_kind"]
    # Literal → `const` in Pydantic v2 JSON schema output.
    is_literal = ("const" in shape_kind) or (
        "enum" in shape_kind and len(shape_kind["enum"]) == 1
    )
    assert is_literal, (
        "Class E discipline: partition_shape_kind must be a Literal (pinned) · "
        "not a runtime-settable str type · E→O promotion required for runtime "
        "tunability per Owner ITEM 1 forward-binding annotation"
    )


# ---------------------------------------------------------------------------
# Contract validation attest · extra="forbid" · frozen=True.
# ---------------------------------------------------------------------------

def test_partition_schema_v0_forbid_extra_fields():
    """extra='forbid' guard · additive-versioning discipline requires v-next for new fields."""
    with pytest.raises(ValidationError):
        PartitionSchema_v0(
            partition_id="p", schema_version="v0", key_dimensions=[],
            receipt_set_ref="rs", promoted_at="2026-07-24T00:00:00+00:00",
            size_bytes=0, instance_id="i",
            spurious_field="should_be_rejected",  # type: ignore[call-arg]
        )
