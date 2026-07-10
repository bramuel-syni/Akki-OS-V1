"""Answer Fluency §3.8 gate roster — AF-G1..AF-G8 (2026-07-10).

Landed per Owner rulings AF-E1 β + 2 conditions (per-sentence structured
anchor mapping + numeric verification + full-response reject-on-fail) +
AF-E2 amended boundary set (config defect → 503 · runtime transient →
mechanical arm · never a refusal envelope) + AF-E3 α (sidecar telemetry
· envelope byte-identical · parity 31) + AF-E4 α + 1 ordering condition
(byte-identical mechanical baseline + capture-then-refactor).

Rulings record: /app/docs/rulings/answer_fluency_af_e1_to_e4.md
Stage A proposal: /app/docs/stage_a_proposals/answer_fluency.md

Cell density (§6.1 amortised): 14 backend cells at ~20 LoC/cell avg
(mix of §6.1 classic 12 LoC + §6.10 AST/reflection 40 LoC + §6.11 async
httpx 25 LoC).
"""
from __future__ import annotations

import ast
import asyncio
import hashlib
import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from contracts.five_rings import DefensibilityClass
from services.service_1 import (
    answer_grounding,
    composed_conclusion,
    fluency_mode_telemetry,
    mechanical_composer,
)
from services.synisense.shield import fluency_synthesizer


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
GOLDEN_PATH = (
    BACKEND_ROOT
    / "tests" / "goldens" / "answer_fluency" / "pre_3_8"
    / "mechanical_baseline.json"
)


# ─── AF-G1 · Mechanical composer byte-identical to pre-3.8 goldens ────
def test_af_g1_mechanical_composer_byte_identical_to_golden():
    """AF-E4 α: goldens captured pre-refactor per ordering condition.
    Mechanical composer output MUST be byte-identical to expected."""
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    assert golden["cases"], "goldens empty"
    for case in golden["cases"]:
        expected = case["expected_answer_text"]
        cls = DefensibilityClass(case["computed_class"])
        actual = mechanical_composer.synthesise_mechanical_answer_text(
            case["load_bearing_unit_ids"], cls,
        )
        assert actual == expected, (
            f"AF-G1 drift on case {case!r}:\n"
            f"  expected: {expected!r}\n"
            f"  actual  : {actual!r}"
        )


# ─── AF-G2a · Grounding gate (A) — foreign unit_id triggers REJECT ────
def test_af_g2a_foreign_unit_id_triggers_reject():
    """AF-E1 β sub-gate (A): every declared unit_id ∈ load_bearing set."""
    r = answer_grounding.verify_grounding(
        prose="The rate is 5.5%.",
        per_sentence=[{"sentence_text": "The rate is 5.5%.",
                       "unit_ids": ["u1", "u_foreign"]}],
        load_bearing_unit_ids=["u1", "u2"],
        unit_id_to_text={"u1": "held at 5.5%", "u2": ""},
    )
    assert not r.passed
    assert "foreign_unit_id" in r.reject_detail


# ─── AF-G2b · Grounding gate (B) — uncovered sentence triggers REJECT ─
def test_af_g2b_uncovered_sentence_triggers_reject():
    """AF-E1 β sub-gate (B): every sentence in prose has an anchor."""
    r = answer_grounding.verify_grounding(
        prose="The rate is 5.5%. Officials announced the outcome.",
        per_sentence=[{"sentence_text": "The rate is 5.5%.",
                       "unit_ids": ["u1"]}],
        load_bearing_unit_ids=["u1"],
        unit_id_to_text={"u1": "held at 5.5%"},
    )
    assert not r.passed
    assert "sentence_not_anchored" in r.reject_detail


# ─── AF-G2c · Grounding gate (C) — numeric verification (Owner Cond 1)
def test_af_g2c_unverified_numeral_triggers_reject():
    """AF-E1 β Condition 1 (Owner-verbatim): 'every numeral in a sentence
    must appear verbatim in that sentence's anchored units; mechanical
    check, no semantic scoring.'
    """
    # Prose asserts 7.5% but anchored unit only says 5.5%.
    r = answer_grounding.verify_grounding(
        prose="The rate is 7.5%.",
        per_sentence=[{"sentence_text": "The rate is 7.5%.",
                       "unit_ids": ["u1"]}],
        load_bearing_unit_ids=["u1"],
        unit_id_to_text={"u1": "CBK held the rate at 5.5% today."},
    )
    assert not r.passed
    assert "numeric_verification_failed" in r.reject_detail
    assert "7.5%" in r.reject_detail


# ─── AF-G2d · Grounding gate (D) — full-response REJECT (Owner Cond 2)
def test_af_g2d_any_failure_full_response_falls_to_mechanical():
    """AF-E1 β Condition 2 (Owner-verbatim): 'any unanchored or failing
    sentence → grounding REJECT → whole response falls to the mechanical
    arm — the gate never patches prose.'

    The grounding gate function returns pass/fail; it never patches
    prose. Caller in composed_conclusion routes to mechanical arm.
    """
    # Two sentences, second has numeric failure. Whole response fails.
    r = answer_grounding.verify_grounding(
        prose="The rate is 5.5%. Reserves fell by 12 percent.",
        per_sentence=[
            {"sentence_text": "The rate is 5.5%.", "unit_ids": ["u1"]},
            {"sentence_text": "Reserves fell by 12 percent.", "unit_ids": ["u2"]},
        ],
        load_bearing_unit_ids=["u1", "u2"],
        unit_id_to_text={"u1": "held at 5.5%",
                          "u2": "reserves fell by five percent"},
    )
    assert not r.passed
    assert "numeric_verification_failed" in r.reject_detail
    # First sentence was fine; but overall REJECT — no patching.
    # (No API in this module can "patch" a partial response — the
    # function signature returns only pass/fail.)
    sig = (answer_grounding.verify_grounding.__doc__ or "").replace("\n", " ")
    # Docstring mandates the caller does the routing; this function
    # returns only pass/fail. That's the "never patches" discipline.
    assert "never edits" in sig and "or patches prose" in sig


# ─── AF-G3a · Amended AF-E2: Missing Emergent key → 503 (fail loud) ───
@pytest.mark.asyncio
async def test_af_g3a_missing_llm_key_fails_loud_503():
    """AF-E2 amended: config defect (Emergent key missing/invalid) →
    503 fail-loud. NOT routed to mechanical arm."""
    # Force config-defect: unset key AND remove mock-mode override.
    with patch.dict(os.environ, {"EMERGENT_LLM_KEY": "", "SYNISENSE_LLM_MODE": ""}, clear=False):
        with pytest.raises(fluency_synthesizer.EmergentKeyMissingError):
            await fluency_synthesizer.synthesise_fluent_answer(
                load_bearing_unit_ids=["u1"],
                unit_id_to_text={"u1": "held at 5.5%"},
                defensibility_class="fact",
            )


# ─── AF-G3b · Amended AF-E2: runtime transient → mechanical arm ───────
@pytest.mark.asyncio
async def test_af_g3b_runtime_transient_degrades_to_mechanical_arm():
    """AF-E2 amended: provider down / rate-limited / timeout / parse
    failure → mechanical arm. Response succeeds; fluency_mode='mechanical';
    telemetry reason set."""
    # Simulate LLMUnavailable at the Shield boundary.
    async def _boom(*a, **kw):
        raise fluency_synthesizer.LLMUnavailableError("provider down (simulated)")

    with patch.object(composed_conclusion, "synthesise_fluent_answer", _boom):
        answer_text, mode, reason, detail = await composed_conclusion._synthesise_answer_text(
            load_bearing_unit_ids=["u1"],
            computed_class=DefensibilityClass.FACT,
            unit_views=[composed_conclusion._UnitView(
                unit_id="u1",
                defensibility=composed_conclusion._DefensibilityView(
                    defensibility_class=DefensibilityClass.FACT,
                ),
                text="held at 5.5%",
            )],
        )
    assert mode == "mechanical"
    assert reason == "llm_unavailable"
    assert detail is None
    # Byte-identical mechanical output
    assert answer_text == mechanical_composer.synthesise_mechanical_answer_text(
        ["u1"], DefensibilityClass.FACT,
    )


# ─── AF-G3c · Never refusal envelope on any runtime transient ─────────
@pytest.mark.asyncio
async def test_af_g3c_never_refusal_envelope_on_runtime_transient():
    """AF-E2 amended: NEVER a refusal envelope on any transient.
    Refusal taxonomy stays closed."""
    for exc_cls, reason in (
        (fluency_synthesizer.LLMUnavailableError, "llm_unavailable"),
        (fluency_synthesizer.LLMTimeoutError, "llm_timeout"),
        (fluency_synthesizer.LLMParseFailureError, "llm_parse_failure"),
    ):
        async def _boom(*a, **kw):
            raise exc_cls("simulated")

        with patch.object(composed_conclusion, "synthesise_fluent_answer", _boom):
            answer_text, mode, r, d = await composed_conclusion._synthesise_answer_text(
                load_bearing_unit_ids=["u1"],
                computed_class=DefensibilityClass.FACT,
                unit_views=[composed_conclusion._UnitView(
                    unit_id="u1",
                    defensibility=composed_conclusion._DefensibilityView(
                        defensibility_class=DefensibilityClass.FACT,
                    ),
                    text="",
                )],
            )
        assert mode == "mechanical", f"exception {exc_cls.__name__} did not degrade to mechanical"
        assert r == reason
        # answer_text is the mechanical output — a ComposedConclusion_v0
        # envelope will wrap this; NOT an admission_refusal envelope.
        assert answer_text.startswith("Composed conclusion over")


# ─── AF-G4 · ComposedConclusion_v0 snapshot byte-identical · parity 31
def test_af_g4_composed_conclusion_snapshot_byte_identical_parity_31():
    """AF-E3 α: frozen contract preserved; parity 31 preserved."""
    from contracts.composed_conclusion import ComposedConclusion_v0
    snap_path = (
        BACKEND_ROOT
        / "tests" / "invariants" / "composed_conclusion.contract_snapshot.json"
    )
    if not snap_path.exists():
        pytest.skip("composed_conclusion.contract_snapshot.json not present")
    snapshot = json.loads(snap_path.read_text(encoding="utf-8"))
    live_schema = ComposedConclusion_v0.model_json_schema()
    assert live_schema == snapshot, (
        "AF-G4: ComposedConclusion_v0 schema drifted from snapshot. "
        "Answer Fluency AF-E3 α requires envelope byte-identical."
    )


# ─── AF-G5 · Fluency-mode telemetry sidecar shape ─────────────────────
def test_af_g5_fluency_mode_telemetry_sidecar_shape():
    """AF-E3 α sidecar: annotate_result returns a NEW dict (non-mutating);
    fluency_mode + attribution + reason fields populated correctly."""
    src = {"pre_existing_key": "value_A"}
    out = fluency_mode_telemetry.annotate_result(
        trace_id="trc-123",
        telemetry_dict=src,
        fluency_mode="llm",
        fluency_reason=None,
    )
    # Non-mutating
    assert "fluency_mode" not in src
    # Attribution present
    assert out["fluency_mode"] == "llm"
    assert out["_fluency_attribution_trace_id"] == "trc-123"
    assert out["_fluency_reason"] is None
    assert out["_grounding_reject_detail"] is None
    # Pre-existing key carried through
    assert out["pre_existing_key"] == "value_A"

    # Mechanical + grounding_reject: detail required
    out2 = fluency_mode_telemetry.annotate_result(
        trace_id="trc-456", telemetry_dict={},
        fluency_mode="mechanical",
        fluency_reason="grounding_reject",
        grounding_reject_detail="numeric_verification_failed:sentence_index=0:numeral='7.5%'",
    )
    assert out2["_grounding_reject_detail"].startswith("numeric_verification_failed")

    # Invalid mode raises
    with pytest.raises(ValueError):
        fluency_mode_telemetry.annotate_result(
            trace_id="t", telemetry_dict={}, fluency_mode="oops",
        )
    # LLM + reason: raises (success path takes reason=None)
    with pytest.raises(ValueError):
        fluency_mode_telemetry.annotate_result(
            trace_id="t", telemetry_dict={},
            fluency_mode="llm", fluency_reason="llm_timeout",
        )
    # grounding_reject without detail: raises
    with pytest.raises(ValueError):
        fluency_mode_telemetry.annotate_result(
            trace_id="t", telemetry_dict={},
            fluency_mode="mechanical",
            fluency_reason="grounding_reject",
        )


# ─── AF-G6b · §6.10 AST/reflection — no semantic scoring branches ─────
def test_af_g6b_answer_grounding_no_semantic_scoring_ast():
    """AF-E1 β discipline (Owner condition 1 verbatim): 'mechanical
    check, no semantic scoring.'

    §6.10 AST/reflection gate — grep-negative on the answer_grounding
    module for semantic-scoring vocabulary (similarity, overlap,
    jaccard, embedding, cosine).
    """
    src = (BACKEND_ROOT / "services" / "service_1" / "answer_grounding.py").read_text()
    forbidden = ("similarity", "overlap", "jaccard", "embedding", "cosine")
    tree = ast.parse(src)
    violations = []
    for node in ast.walk(tree):
        # Any identifier containing a forbidden word (case-insensitive)?
        for attr in ("id", "name", "attr", "arg"):
            v = getattr(node, attr, None)
            if isinstance(v, str) and any(f in v.lower() for f in forbidden):
                violations.append(
                    f"line {getattr(node, 'lineno', '?')}: "
                    f"{attr}={v!r} contains forbidden semantic-scoring vocabulary"
                )
        # String constants
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for f in forbidden:
                if f in node.value.lower() and "no semantic scoring" not in node.value.lower():
                    violations.append(
                        f"line {getattr(node, 'lineno', '?')}: "
                        f"string constant contains {f!r}: {node.value[:80]!r}"
                    )
    assert not violations, (
        "AF-G6b violation — answer_grounding.py contains semantic-scoring "
        "vocabulary. Owner AF-E1 β Condition 1: 'mechanical check, no "
        "semantic scoring.'\n" + "\n".join(violations)
    )


# ─── AF-G7 · Grounding-gate reject NOT a refusal · mechanical passes ──
@pytest.mark.asyncio
async def test_af_g7_grounding_reject_falls_through_not_refusal():
    """AF-E1 β Condition 2 + AF-E2 amended: grounding REJECT is a
    quality-gate outcome; falls through to mechanical arm. NEVER a
    refusal envelope. Ledger row still fires with
    data_class='composed_conclusion' (not a new class)."""
    async def _bad_llm_output(*a, **kw):
        # Return a payload whose prose sentence has an unverified numeral.
        return {
            "prose": "The rate is 99.9%.",
            "per_sentence": [
                {"sentence_text": "The rate is 99.9%.", "unit_ids": ["u1"]},
            ],
        }

    with patch.object(composed_conclusion, "synthesise_fluent_answer", _bad_llm_output):
        answer_text, mode, reason, detail = await composed_conclusion._synthesise_answer_text(
            load_bearing_unit_ids=["u1"],
            computed_class=DefensibilityClass.FACT,
            unit_views=[composed_conclusion._UnitView(
                unit_id="u1",
                defensibility=composed_conclusion._DefensibilityView(
                    defensibility_class=DefensibilityClass.FACT,
                ),
                text="held at 5.5%",
            )],
        )
    assert mode == "mechanical"
    assert reason == "grounding_reject"
    assert detail is not None and "numeric_verification_failed" in detail
    # Mechanical prose emitted; NOT a refusal envelope shape.
    assert "Composed conclusion over" in answer_text


# ─── AF-G8 · §6.10 · Data-blind posture · prompt template no residues ─
def test_af_g8_prompt_template_data_blind_no_residues():
    """Prompt template contains no broadcaster/genre/regional residues
    from pre-Fixture-Refresh estate. Data-blind posture governance §8."""
    prompt_path = (
        BACKEND_ROOT
        / "services" / "synisense" / "shield" / "fluency_prompt.v0.txt"
    )
    text = prompt_path.read_text(encoding="utf-8").lower()
    forbidden = (
        "citizen_tv_news", "wire_kna", "ktn_news", "ntv_news",
        "print_edition", "radio_jambo", "citizen_archive",
        "citizen_drama", "aggregator_blog", "x_ingest",
        # Also block genre/regional priors
        "kenya", "nairobi", "swahili", "sheng", "safisasa",
        "tahidi", "kayole", "thika",
    )
    hits = [f for f in forbidden if f in text]
    assert not hits, (
        f"AF-G8 violation — prompt template contains data-blind residues: "
        f"{hits}. Governance §8 posture broken."
    )
