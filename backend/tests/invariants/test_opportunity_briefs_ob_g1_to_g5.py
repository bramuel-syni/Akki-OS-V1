"""Opportunity Briefs §3.15 gate roster — OB-G1..OB-G5 mandate + seam gates
+ auxiliary gates (2026-07-10).

Landed per Owner rulings OB-E1 α (byte-verbatim substring · whole-brief
reject · no semantic scoring · mirrors AF-E1 β + Owner Condition 1
precedent) + OB-E2 α × 3 seams (write-time attach + render reflection ·
route-level 404 with distinct `brief_id` namespace · grep-negative
import boundary) + OB-E3 α (Registry-computable aggregate = Registry-
exposed native · synthesis-time computation FORBIDDEN).

Rulings record: /app/docs/rulings/opportunity_briefs_ob_e1_to_e3.md
Stage A proposal: /app/docs/stage_a_proposals/opportunity_briefs.md
"""
from __future__ import annotations

import ast
import asyncio
import json
import re
from pathlib import Path
from unittest.mock import patch

import pytest

from services.opportunity_briefs import BRIEF_ID_PREFIX
from services.opportunity_briefs import (
    advisory_marker,
    brief_grounding,
    brief_registry,
    brief_selector,
    brief_telemetry,
    generator,
    shape_as_objective_prefill,
)
from services.synisense.shield import brief_synthesizer


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
OB_PKG_ROOT = BACKEND_ROOT / "services" / "opportunity_briefs"
SERVICE_1_ROOT = BACKEND_ROOT / "services" / "service_1"


# ─── OB-G1 · brief_numbers_are_registry_reads_verbatim ────────────────
def test_ob_g1_brief_numbers_are_registry_reads_verbatim():
    """OB-E1 α: every anchor value appears byte-verbatim in the
    referenced Registry read text; every numeric in brief_text has a
    corresponding anchor."""
    r = brief_grounding.verify_brief_grounding(
        brief_text="The measured slice contains 47 units at 12.5% share.",
        quantitative_anchors=[
            {"value": "47", "registry_read_ref": "reg-r1"},
            {"value": "12.5%", "registry_read_ref": "reg-r2"},
        ],
        registry_read_texts={
            "reg-r1": "count_of_units_in_slice(slice_a) = 47",
            "reg-r2": "share_in_estate(slice_a) = 12.5%",
        },
    )
    assert r.passed, f"OB-G1 rejected valid brief: {r.reject_detail}"

    # Value not in ref → REJECT
    r_bad = brief_grounding.verify_brief_grounding(
        brief_text="99 units.",
        quantitative_anchors=[{"value": "99", "registry_read_ref": "reg-r1"}],
        registry_read_texts={"reg-r1": "count = 47"},
    )
    assert not r_bad.passed
    assert "value_not_in_registry_read" in r_bad.reject_detail

    # Numeric in brief_text with no anchor → REJECT
    r_no_anchor = brief_grounding.verify_brief_grounding(
        brief_text="47 units and 12 anecdotes.",
        quantitative_anchors=[{"value": "47", "registry_read_ref": "reg-r1"}],
        registry_read_texts={"reg-r1": "47 units"},
    )
    assert not r_no_anchor.passed
    assert "numeric_not_anchored" in r_no_anchor.reject_detail


# ─── OB-G2 · advisory_marker_present_on_every_brief_render ────────────
def test_ob_g2_advisory_marker_present_on_every_brief_render():
    """OB-E2 Seam-1 α: write-time attach invariant · marker on every
    written brief · render surfaces read the marker from the sidecar."""
    reg = brief_registry.BriefRegistry()
    row = reg.write(
        scope="slice",
        contributing_slices=["dim:a"],
        brief_text="Placeholder body 47.",
        quantitative_anchors=[{"value": "47", "registry_read_ref": "r1"}],
        census_ref="census-v1",
    )
    assert advisory_marker.has_marker(row), (
        "OB-G2 · Seam-1 α write-time attach violated"
    )
    # Every row in the registry carries the marker
    for r in reg.all_rows():
        assert advisory_marker.has_marker(r), (
            f"OB-G2 · row {r['brief_id']} missing advisory marker"
        )


def test_ob_g2_seam1_no_strip_ast():
    """OB-E2 Seam-1 α sub-gate: §6.10 reflection walk — no code path
    strips or overwrites `ADVISORY_MARKER_KEY` in the OB package."""
    forbidden_patterns = (
        f"del", "pop(", "clear()",
    )
    key_literal = advisory_marker.ADVISORY_MARKER_KEY
    violations = []
    for py in OB_PKG_ROOT.rglob("*.py"):
        if "__pycache__" in str(py):
            continue
        text = py.read_text(encoding="utf-8")
        # If the file mentions the marker key, ensure it doesn't
        # combine it with a strip/delete op on the same line.
        for i, line in enumerate(text.splitlines(), 1):
            if key_literal in line and any(f in line for f in forbidden_patterns):
                violations.append(
                    f"{py.name}:{i}: {line.strip()!r} strips advisory marker"
                )
    assert not violations, (
        "OB-G2 Seam-1 no-strip violated:\n" + "\n".join(violations)
    )


# ─── OB-G3 · brief_excluded_from_trace_resolution ─────────────────────
@pytest.mark.asyncio
async def test_ob_g3_brief_excluded_from_trace_resolution():
    """OB-E2 Seam-2 α: /api/trace/{brief_id} returns 404 for the
    `brief_` namespace."""
    from httpx import AsyncClient, ASGITransport
    from server import app

    fresh_brief_id = brief_registry.new_brief_id()
    assert fresh_brief_id.startswith(BRIEF_ID_PREFIX)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get(f"/api/solva/trace/{fresh_brief_id}")
    assert resp.status_code == 404, (
        f"OB-G3 · Seam-2 α violated · trace resolution accepted brief_id "
        f"{fresh_brief_id!r}: status={resp.status_code}"
    )
    # non-brief trace_id still resolves (200 with empty list per get_trace).
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp2 = await ac.get("/api/solva/trace/some-normal-trace-id")
    assert resp2.status_code == 200


def test_ob_g3_seam2_namespace_distinct():
    """OB-E2 Seam-2 α sub-gate: `brief_` prefix is distinct from all
    known id namespaces (`unit_id`/`trace_id`/`run_id`/`cc-unit-`)."""
    fresh = brief_registry.new_brief_id()
    for other_ns in ("cc-unit-", "run-", "trace-", "unit-"):
        assert not fresh.startswith(other_ns), (
            f"OB-G3 · brief_id namespace {BRIEF_ID_PREFIX!r} collides with {other_ns!r}"
        )
    assert fresh.startswith(BRIEF_ID_PREFIX)


# ─── OB-G4 · shape_as_objective_prefills_reach_only ───────────────────
def test_ob_g4_shape_as_objective_prefills_reach_only():
    """OB-R4: pre-fill payload ONLY carries `reach`; no other wizard
    mandatory field is pre-filled from the brief."""
    brief = {
        "brief_id": brief_registry.new_brief_id(),
        "scope": "combined",
        "contributing_slices": ["dim:a", "dim:b"],
        "brief_text": "Placeholder.",
    }
    payload = shape_as_objective_prefill.build_prefill(brief)
    assert set(payload.keys()) == {"reach"}, (
        f"OB-G4 violated — pre-fill payload keys {sorted(payload.keys())} "
        f"exceed {{'reach'}}"
    )
    # Mandatory wizard fields must be absent
    for forbidden in ("commissioner", "objective", "class", "defensibility"):
        assert forbidden not in payload
    # Reach carries brief's contributing_slices + brief_id
    assert payload["reach"]["contributing_slices"] == ["dim:a", "dim:b"]
    assert payload["reach"]["brief_id"] == brief["brief_id"]


# ─── OB-G5 · combined_brief_numbers_trace_to_each_contributing_slice ──
def test_ob_g5_combined_brief_numbers_trace_to_each_contributing_slice():
    """OB-E3 α (per OB-R6 grounding clause): a Combined brief's anchors
    trace to Registry reads of the NAMED contributing_slices; blended
    figures permitted iff Registry read exposes the aggregate natively."""
    # A well-formed combined brief: 2 slices, 2 anchors, one per slice.
    r = brief_grounding.verify_brief_grounding(
        brief_text="Slice-a contributes 47 units and slice-b contributes 22.",
        quantitative_anchors=[
            {"value": "47", "registry_read_ref": "reg-slice-a-count"},
            {"value": "22", "registry_read_ref": "reg-slice-b-count"},
        ],
        registry_read_texts={
            "reg-slice-a-count": "count_of_units_in_slice(slice_a) = 47",
            "reg-slice-b-count": "count_of_units_in_slice(slice_b) = 22",
        },
    )
    assert r.passed, r.reject_detail

    # A blended-figure that's Registry-computable native (aggregate exposed by Registry)
    r_agg = brief_grounding.verify_brief_grounding(
        brief_text="Combined slice-a and slice-b contain 69 units.",
        quantitative_anchors=[
            {"value": "69", "registry_read_ref": "reg-combined-a-b-count"},
        ],
        registry_read_texts={
            "reg-combined-a-b-count": "count_of_units_in_combined(slice_a,slice_b) = 69",
        },
    )
    assert r_agg.passed, r_agg.reject_detail


# ─── OB-G-Seam-3 · governed_response_import_boundary ──────────────────
def test_ob_g_seam3_governed_response_import_boundary():
    """OB-E2 Seam-3 α: no service_1/** file imports from
    opportunity_briefs/**. AST attest — §6.10 reflection gate."""
    violations = []
    for py in SERVICE_1_ROOT.rglob("*.py"):
        if "__pycache__" in str(py):
            continue
        text = py.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = []
                if isinstance(node, ast.ImportFrom):
                    names.append(node.module or "")
                for alias in node.names:
                    names.append(alias.name or "")
                for n in names:
                    if "opportunity_briefs" in n:
                        violations.append(
                            f"{py.relative_to(BACKEND_ROOT)}:{node.lineno}: "
                            f"import of {n!r} violates OB-E2 Seam-3 boundary"
                        )
    assert not violations, (
        "OB-E2 Seam-3 α violated — service_1 imports opportunity_briefs:\n"
        + "\n".join(violations)
    )


# ─── OB-G-DB · brief_prompt_template_data_blind_no_residues ───────────
def test_ob_g_db_brief_prompt_template_data_blind_no_residues():
    """§8 data-blind posture — prompt template contains no
    broadcaster/regional/dialectal/genre residues."""
    prompt_path = (
        BACKEND_ROOT / "services" / "synisense" / "shield" / "brief_prompt.v0.txt"
    )
    text = prompt_path.read_text(encoding="utf-8").lower()
    forbidden = (
        "citizen_tv_news", "wire_kna", "ktn_news", "ntv_news",
        "print_edition", "radio_jambo", "citizen_archive",
        "citizen_drama", "aggregator_blog", "x_ingest",
        "kenya", "nairobi", "swahili", "sheng", "safisasa",
        "tahidi", "kayole", "thika",
    )
    hits = [f for f in forbidden if f in text]
    assert not hits, (
        f"OB-G-DB violation — brief prompt template contains "
        f"data-blind residues: {hits}"
    )


# ─── OB-G-Parity · parity_31_preserved_at_ob_landing ──────────────────
def test_ob_g_parity_31_preserved_at_ob_landing():
    """OB lands via new-registry-table + sidecar telemetry pattern;
    NO frozen contract touched. Parity stays at 31."""
    snap_dir = BACKEND_ROOT / "tests" / "invariants"
    snapshots = list(snap_dir.glob("*.contract_snapshot.json"))
    # Parity 31 pre-established by AF-G4 baseline; OB touches no snapshots
    # so this count is stable. The exact count check lives at V1-G7;
    # here we assert no new contract snapshots were added by OB.
    assert len(snapshots) >= 1, "no contract snapshots on disk"
    # Verify OpportunityBrief_v0 has NOT been added as a frozen contract
    from pathlib import Path
    contracts_dir = BACKEND_ROOT / "contracts"
    ob_contract = contracts_dir / "opportunity_brief.py"
    ob_snapshot = snap_dir / "opportunity_brief.contract_snapshot.json"
    assert not ob_contract.exists(), (
        "OB-G-Parity violated — contracts/opportunity_brief.py exists; "
        "OB-E2 Seam-1 β was not selected · sidecar posture broken"
    )
    assert not ob_snapshot.exists(), (
        "OB-G-Parity violated — opportunity_brief.contract_snapshot.json "
        "exists; parity 31 broken"
    )


# ─── OB-G-Refresh · stale_marking_on_census_change ────────────────────
def test_ob_g_refresh_stale_marking_on_census_change():
    """OB-R5: regeneration on census change · stale briefs marked · retained."""
    reg = brief_registry.BriefRegistry()
    r1 = reg.write(
        scope="slice",
        contributing_slices=["dim:a"],
        brief_text="47.",
        quantitative_anchors=[{"value": "47", "registry_read_ref": "r"}],
        census_ref="census-v1",
    )
    assert not r1["stale"]

    marked = reg.refresh_on_census_change("census-v2")
    assert marked == 1
    # Retained
    assert reg.read(r1["brief_id"]) is not None
    assert reg.read(r1["brief_id"])["stale"] is True


# ─── OB-G-Grounding-Fail · grounding_fail_prevents_brief_write ────────
@pytest.mark.asyncio
async def test_ob_g_grounding_fail_prevents_brief_write():
    """OB-E1 α whole-brief REJECT: grounding failure → brief NOT
    written to registry; telemetry status='grounding_reject'."""
    async def _bad_synth(**kwargs):
        # LLM returns brief_text with unanchored numeral
        return {
            "brief_text": "This slice contains 999 units.",
            "quantitative_anchors": [
                {"value": "47", "registry_read_ref": "r1"},  # value not in brief_text
            ],
        }

    with patch.object(brief_synthesizer, "synthesise_brief", _bad_synth):
        row, telem = await generator.generate_one_brief(
            scope="slice",
            contributing_slices=["dim:a"],
            registry_read_texts={"r1": "count = 47"},
            census_ref="census-v1",
        )
    assert row is None, "OB-E1 α violated — grounding-reject brief was written"
    assert telem["_generation_status"] == "grounding_reject"
    assert telem["_grounding_reject_detail"] is not None
    assert "numeric_not_anchored" in telem["_grounding_reject_detail"]


# ─── OB-G-E3-No-Synth-Compute · §6.10 grep-negative on aggregate ops ──
def test_ob_g_e3_no_synthesis_compute_ast():
    """OB-E3 α: synthesis-time computation FORBIDDEN. §6.10 AST attest
    that neither `generator.py` nor `brief_synthesizer.py` invokes
    sum/avg/min/max/count-style aggregate operators.
    """
    targets = [
        OB_PKG_ROOT / "generator.py",
        OB_PKG_ROOT / "brief_proposer.py" if (OB_PKG_ROOT / "brief_proposer.py").exists() else None,
        BACKEND_ROOT / "services" / "synisense" / "shield" / "brief_synthesizer.py",
    ]
    forbidden_calls = {"sum", "avg", "average", "mean", "min", "max", "count", "statistics"}
    violations = []
    for path in targets:
        if path is None or not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            # Detect direct builtin call: sum(x), min(x), max(x)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in forbidden_calls:
                    violations.append(
                        f"{path.name}:{node.lineno}: forbidden aggregate "
                        f"call {node.func.id}(...) at synthesis time (OB-E3 α)"
                    )
    assert not violations, (
        "OB-E3 α violated — synthesis-time aggregate computation:\n"
        + "\n".join(violations)
    )


# ─── OB-G-Selector · three-scope enumeration ──────────────────────────
def test_ob_g_selector_three_scope_enumeration():
    """Selector produces candidates at all three scopes (slice, combined, estate)."""
    candidates = brief_selector.enumerate_candidates(
        {"dim_x": ["s1", "s2"], "dim_y": ["s3"]},
    )
    scopes = {c.scope for c in candidates}
    assert scopes == {"slice", "combined", "estate"}, (
        f"OB-G-Selector missing scopes; got {scopes}"
    )
    # Slice count = 3 (2 + 1)
    slice_count = sum(1 for c in candidates if c.scope == "slice")
    assert slice_count == 3
    # Estate count = 1
    estate_count = sum(1 for c in candidates if c.scope == "estate")
    assert estate_count == 1


# ─── OB-G-Telemetry · sidecar shape validity ──────────────────────────
def test_ob_g_telemetry_sidecar_shape():
    """Sidecar telemetry — mirrors AF-E3 α precedent."""
    telem = brief_telemetry.annotate_brief_result(
        brief_id="brief_abc",
        scope="slice",
        telemetry_dict={"pre": "keep"},
        regeneration_reason="initial",
        generation_status="success",
        stale_flag=False,
        advisory_marker_attached=True,
    )
    assert telem["brief_id"] == "brief_abc"
    assert telem["scope"] == "slice"
    assert telem["_generation_status"] == "success"
    assert telem["_advisory_marker_attached"] is True
    assert telem["pre"] == "keep"

    # grounding_reject requires detail
    with pytest.raises(ValueError):
        brief_telemetry.annotate_brief_result(
            brief_id="brief_abc",
            scope="slice",
            telemetry_dict={},
            regeneration_reason="initial",
            generation_status="grounding_reject",
            stale_flag=False,
            advisory_marker_attached=False,
        )
    # invalid reason raises
    with pytest.raises(ValueError):
        brief_telemetry.annotate_brief_result(
            brief_id="brief_abc",
            scope="slice",
            telemetry_dict={},
            regeneration_reason="oops",
            generation_status="success",
            stale_flag=False,
            advisory_marker_attached=True,
        )


# ─── OB-G-Runtime-Transient · never a refusal envelope ────────────────
@pytest.mark.asyncio
async def test_ob_g_runtime_transient_never_refusal_envelope():
    """AF-E2-precedent-shaped: runtime transients (LLM unavailable /
    timeout / parse failure) surface as telemetry statuses; brief NOT
    written; NEVER a refusal envelope."""
    async def _boom_unavailable(**kwargs):
        raise brief_synthesizer.LLMUnavailableError("provider down")

    with patch.object(brief_synthesizer, "synthesise_brief", _boom_unavailable):
        row, telem = await generator.generate_one_brief(
            scope="slice",
            contributing_slices=["dim:a"],
            registry_read_texts={"r": "text"},
            census_ref="census-v1",
        )
    assert row is None
    assert telem["_generation_status"] == "llm_unavailable"
    # No refusal envelope shape (would be `AdmissionRefusal_v0`)
    assert "refusal" not in telem
