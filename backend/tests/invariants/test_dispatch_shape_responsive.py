"""Shape-responsive execution dispatch — Phase 2 gate tests.

Owner ruling dispatch (2026-07-03): 4 named gates + 5 positive-path
sub-tests + 1 v0-untouched regression (split into
`test_dispatch_v0_untouched.py`).

Named gates:
  1. `test_dispatch_unknown_freshness_forks_fresh_never_warm` — LOAD-BEARING
  2. `test_dispatch_uses_shared_feasibility_and_floor_feasibility` — LOAD-BEARING
  3. `test_dispatch_placeholder_never_leaks_into_governed_refusal` — LOAD-BEARING
  4. `test_dispatch_never_branches_on_depth_enum` — LOAD-BEARING

Positive-path sub-tests:
  * work_order dispatch → route_target = service_1_v0_via_adapter.
  * external_request warm-fork (populated Registry, feasible floor).
  * external_request fresh-fork (empty Registry).
  * output-form routing to placeholder for `knowledge_artifact`, `callable_skill`, `model`.

Every test drives `dispatch_module.dispatch()` directly OR the v2 route
via ASGITransport. Direct-import tests cover semantic correctness;
route tests cover wire-shape.
"""
from __future__ import annotations

import ast
import inspect
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from contracts.feasibility_result import Freshness
from contracts.five_rings import DefensibilityClass
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from contracts.objective_request_v2 import (
    Envelope,
    ObjectiveEntry,
    ObjectiveRequest_v2,
    Output,
    OutputConsumer,
    OutputForm,
    OutputGrain,
    Reach,
)
from contracts.objective_request import DefensibilityFloor
from core import db
from server import app
from services.service_1 import dispatch as dispatch_module


AUG_PATH = Path(__file__).parent / "feasibility_fixture_augmentation.json"
_AUG = json.loads(AUG_PATH.read_text())


async def _clear_registry() -> None:
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})


async def _seed_fresh_row(source_ref: str, region: str, klass: str,
                          days_ago: int = 0) -> None:
    """Populate one MtafitiRegistryRecord — mirrors the shape from
    contracts/mtafiti_registry.py."""
    logged = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    await db[MTAFITI_REGISTRY_COLLECTION].insert_one({
        "source_ref": source_ref,
        "region": region,
        "feed_id": region,
        "sensitivity": "standard",
        "defensibility_measure": {
            "source_standing": "accountable",
            "attachment": 0.0,
            "corroboration": 0.0,
            "recency_validity": 0.5,
            "contested": False,
        },
        "defensibility_runtime_mode": "declaration_baseline",
        "matrix_rule_ref": "qm.v0.rule.1",
        "defensibility_class": klass,
        "freshness_stamp": {
            "logged_date": logged,
            "structural_signature": None,
        },
    })


def _build_request(
    *,
    entry: ObjectiveEntry = ObjectiveEntry.EXTERNAL_REQUEST,
    scope_refs=None,
    exclusions=None,
    depth: str = "baseline",
    form: OutputForm = OutputForm.QUALIFIED_DATA,
    minimum_class: DefensibilityClass = DefensibilityClass.UTTERANCE,
) -> ObjectiveRequest_v2:
    """Minimal ObjectiveRequest_v2 for dispatch tests."""
    return ObjectiveRequest_v2(
        entry=entry,
        reach=Reach(
            scope_refs=scope_refs if scope_refs is not None else [],
            exclusions=exclusions if exclusions is not None else [],
            depth=depth,
        ),
        output=Output(
            form=form,
            consumer=OutputConsumer.PERSON,
            grain=OutputGrain.PER_CLAIM,
            standard=DefensibilityFloor(minimum_class=minimum_class),
        ),
        envelope=Envelope(
            lawful_basis="test_basis",
            done_condition="test_done",
            budget="test_budget",
            scope_ceiling="test_ceiling",
            commissioner="test_commissioner",
            committed_at="2026-07-03T12:00:00+00:00",
        ),
    )


# ---------------------------------------------------------------------------
# Gate 1 — LOAD-BEARING
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_dispatch_unknown_freshness_forks_fresh_never_warm():
    """v3 §5 honesty binds the fork decision.

    Warmth is an assertion of qualified availability. From an
    un-censused reach, the feasibility query returns UNKNOWN;
    asserting warm anyway would fabricate the exact thing Phase 1's
    honesty gate exists to prevent. Fork MUST be `fresh`.

    Uses the augmented un-censused scope_ref from
    `feasibility_fixture_augmentation.json` (Item 4 posture preserved
    — augmentation-file separation, not fixture mutation).
    """
    await _clear_registry()
    req = _build_request(
        entry=ObjectiveEntry.EXTERNAL_REQUEST,
        scope_refs=[_AUG["uncensused_scope_ref"]],
        form=OutputForm.QUALIFIED_DATA,
    )
    result = await dispatch_module.dispatch(req)

    # Feasibility must report UNKNOWN for the un-censused reach.
    assert result.feasibility_result is not None
    assert result.feasibility_result.freshness == Freshness.UNKNOWN, (
        f"expected UNKNOWN freshness on un-censused reach; "
        f"got {result.feasibility_result.freshness}"
    )
    # Fork MUST be fresh.
    assert result.fork_decision == "fresh", (
        f"UNKNOWN freshness MUST fork FRESH (never warm); "
        f"got fork_decision={result.fork_decision!r}"
    )
    # floor_feasibility is None under UNKNOWN (no distribution to derive from).
    assert result.floor_feasibility is None
    # route_target names the fresh admission fork.
    assert result.route_target == dispatch_module.ROUTE_ADMISSION_FRESH_FORK


# ---------------------------------------------------------------------------
# Gate 2 — LOAD-BEARING
# ---------------------------------------------------------------------------


def test_dispatch_uses_shared_feasibility_and_floor_feasibility():
    """Ruling 4: dispatch MUST import the shared feasibility + floor
    functions. Static import inspection + regression grep.

    Failure mode this prevents: a Phase 2+ file quietly reimplementing
    `compute_feasibility` or `derive_floor_feasibility` locally, even
    with equal outputs. That is a second-computation-path — the A2
    `supported_class` lesson exactly.
    """
    # Static-import inspection via AST — no execution needed.
    dispatch_source = Path(inspect.getfile(dispatch_module))
    tree = ast.parse(dispatch_source.read_text(encoding="utf-8"))

    imports_compute_feasibility = False
    imports_derive_floor = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = {alias.name for alias in node.names}
            if module == "services.mtafiti.feasibility" and "compute_feasibility" in names:
                imports_compute_feasibility = True
            if module == "services.mtafiti.floor_feasibility" and "derive_floor_feasibility" in names:
                imports_derive_floor = True

    assert imports_compute_feasibility, (
        "dispatch.py MUST import compute_feasibility from "
        "services.mtafiti.feasibility (Ruling 4 — single-consumer feasibility)"
    )
    assert imports_derive_floor, (
        "dispatch.py MUST import derive_floor_feasibility from "
        "services.mtafiti.floor_feasibility (Ruling 4 — shared derivation)"
    )

    # Regression grep — no local reimplementation of the two functions
    # anywhere in the Phase-2-touched surface.
    dispatch_text = dispatch_source.read_text(encoding="utf-8")
    # A reimplementation would define these names locally. The only
    # occurrences allowed are import references.
    for forbidden_pattern in (
        "def compute_feasibility",
        "def derive_floor_feasibility",
        "async def compute_feasibility",
    ):
        assert forbidden_pattern not in dispatch_text, (
            f"dispatch.py contains a local (re)definition of shared "
            f"function: {forbidden_pattern!r}. Ruling 4 requires import "
            f"from the canonical module."
        )


# ---------------------------------------------------------------------------
# Gate 3 (rendering separation) — LOAD-BEARING
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_dispatch_placeholder_never_leaks_into_governed_refusal():
    """Phase-2 placeholder is engineering scaffolding, NOT a product
    outcome. The wire shape must be distinct from Service1Refusal@v0.

    Service1Refusal@v0 canonical shape (contracts/service_1_refusal.py):
      { outcome: 'refused', reason, run_id, trace_id, asked,
        supported_class, what_would_raise_it }

    Phase-2 placeholder canonical shape (dispatch._make_placeholder):
      { outcome: 'not_yet_implemented', reason:
        'phase_2_scaffold_downstream_deferred', route, phase_debt,
        trace_id }

    Two disjoint discriminators (`outcome`), two disjoint field-sets.
    """
    await _clear_registry()

    # Drive dispatch across every entry × output.form combination that
    # can produce a placeholder — MODEL, KNOWLEDGE_ARTIFACT,
    # CALLABLE_SKILL, and QUALIFIED_DATA (with UNKNOWN freshness).
    cases = [
        _build_request(form=OutputForm.MODEL),
        _build_request(form=OutputForm.KNOWLEDGE_ARTIFACT),
        _build_request(form=OutputForm.CALLABLE_SKILL),
        _build_request(entry=ObjectiveEntry.WORK_ORDER, form=OutputForm.QUALIFIED_DATA),
        _build_request(
            entry=ObjectiveEntry.EXTERNAL_REQUEST,
            scope_refs=[_AUG["uncensused_scope_ref"]],
            form=OutputForm.QUALIFIED_DATA,
        ),
    ]
    for req in cases:
        result = await dispatch_module.dispatch(req)
        assert result.placeholder_body is not None
        pb = result.placeholder_body
        assert pb["outcome"] == "not_yet_implemented", (
            f"placeholder outcome MUST be 'not_yet_implemented'; got {pb['outcome']!r}"
        )
        assert pb["reason"] == "phase_2_scaffold_downstream_deferred"
        # Field set — matches spec.
        assert set(pb.keys()) == {"outcome", "reason", "route", "phase_debt", "trace_id"}
        # Explicitly assert none of the Service1Refusal field names are present.
        for refusal_field in ("asked", "supported_class", "what_would_raise_it", "run_id"):
            assert refusal_field not in pb, (
                f"Phase-2 placeholder MUST NOT carry Service1Refusal field "
                f"{refusal_field!r} — rendering separation violated."
            )
        assert pb["outcome"] != "refused", "Phase-2 placeholder outcome MUST NOT be 'refused'"


# ---------------------------------------------------------------------------
# Gate 4 — LOAD-BEARING
# ---------------------------------------------------------------------------


def test_dispatch_never_branches_on_depth_enum():
    """`Reach.depth` is `str` per Phase 0 loose-as-frozen ruling.

    Grep-negative: no pattern in Phase-2 files of the form
    `if depth ==`, `match depth`, or `Depth.` (against nonexistent
    enum members). Grep-negative == pass.

    If dispatch scaffold ever needs enumerated depth values to branch,
    HAZARD-STOP — freezing guessed enums is fabrication (Phase 0 ruling).
    """
    import io
    import tokenize

    dispatch_path = Path(inspect.getfile(dispatch_module))
    text = dispatch_path.read_text(encoding="utf-8")

    # Reconstruct only the executable-code portion of the file — strip
    # string literals (including docstrings) and comments. This prevents
    # false positives from docstrings that DOCUMENT the banned patterns.
    stripped_tokens = []
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type in (tokenize.STRING, tokenize.COMMENT):
            continue
        if tok.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                        tokenize.DEDENT, tokenize.ENCODING, tokenize.ENDMARKER):
            stripped_tokens.append(tok.string)
            continue
        stripped_tokens.append(tok.string + " ")
    code_only = "".join(stripped_tokens)

    violations = []
    for line_no, raw_line in enumerate(code_only.splitlines(), start=1):
        # Pattern 1: `if depth ==` (or `elif depth ==`)
        if "if depth ==" in raw_line or "elif depth ==" in raw_line:
            violations.append(
                f"{dispatch_path.name}:code-line-{line_no}: 'if/elif depth ==' — "
                f"Gate 4 violation: {raw_line.strip()!r}"
            )
        # Pattern 2: `match depth` (Python 3.10+ match-case)
        if raw_line.strip().startswith("match depth"):
            violations.append(
                f"{dispatch_path.name}:code-line-{line_no}: 'match depth' — "
                f"Gate 4 violation: {raw_line.strip()!r}"
            )
        # Pattern 3: `Depth.` — reference to a nonexistent Depth enum
        if "Depth." in raw_line:
            violations.append(
                f"{dispatch_path.name}:code-line-{line_no}: 'Depth.' — "
                f"Gate 4 violation (no such enum): {raw_line.strip()!r}"
            )

    assert not violations, (
        "Gate 4 violation — dispatch.py branches on depth value:\n" + "\n".join(violations)
    )


# ---------------------------------------------------------------------------
# Positive-path sub-tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_positive_work_order_dispatch_routes_to_service_1_v0():
    """work_order entry → route_target = service_1_v0_via_adapter.

    No feasibility computation (wizard grounds per-turn). Placeholder
    points at Phase 4 receiver (transform variants).
    """
    req = _build_request(
        entry=ObjectiveEntry.WORK_ORDER,
        form=OutputForm.QUALIFIED_DATA,
    )
    result = await dispatch_module.dispatch(req)
    assert result.route_target == dispatch_module.ROUTE_SERVICE_1_V0_VIA_ADAPTER
    assert result.fork_decision is None
    assert result.feasibility_result is None
    assert result.floor_feasibility is None
    assert result.placeholder_body is not None
    assert result.placeholder_body["phase_debt"] == dispatch_module.DEBT_PHASE_4


@pytest.mark.asyncio
async def test_positive_external_request_warm_fork_populated_registry():
    """external_request + feasible floor → warm fork.

    Populated Registry with UTTERANCE+FACT rows; floor=UTTERANCE.
    derive_floor_feasibility.feasible == True; qualifying_volume >= 1;
    freshness == FRESH. Fork MUST be `warm`.
    """
    await _clear_registry()
    await _seed_fresh_row("s://a/r.raw", "warm_region", "fact")
    await _seed_fresh_row("s://a/s.raw", "warm_region", "utterance")
    await _seed_fresh_row("s://a/t.raw", "warm_region", "utterance")

    req = _build_request(
        entry=ObjectiveEntry.EXTERNAL_REQUEST,
        scope_refs=["warm_region"],
        form=OutputForm.QUALIFIED_DATA,
        minimum_class=DefensibilityClass.UTTERANCE,
    )
    result = await dispatch_module.dispatch(req)
    assert result.feasibility_result is not None
    assert result.feasibility_result.freshness == Freshness.FRESH
    assert result.floor_feasibility is not None
    assert result.floor_feasibility["feasible"] is True
    assert result.fork_decision == "warm", (
        f"populated feasible reach MUST fork WARM; got {result.fork_decision!r}"
    )
    assert result.route_target == dispatch_module.ROUTE_ADMISSION_WARM_FORK
    assert result.placeholder_body["phase_debt"] == dispatch_module.DEBT_PHASE_4


@pytest.mark.asyncio
async def test_positive_external_request_fresh_fork_below_floor():
    """external_request + infeasible floor → fresh fork.

    Populated Registry with only NON_FACTUAL rows; floor=FACT.
    derive_floor_feasibility.feasible == False. Fork MUST be `fresh`.
    """
    await _clear_registry()
    await _seed_fresh_row("s://b/x.raw", "below_floor_region", "non_factual")
    await _seed_fresh_row("s://b/y.raw", "below_floor_region", "utterance")

    req = _build_request(
        entry=ObjectiveEntry.EXTERNAL_REQUEST,
        scope_refs=["below_floor_region"],
        form=OutputForm.QUALIFIED_DATA,
        minimum_class=DefensibilityClass.FACT,  # No FACT rows in Registry
    )
    result = await dispatch_module.dispatch(req)
    assert result.feasibility_result is not None
    assert result.feasibility_result.freshness == Freshness.FRESH
    assert result.floor_feasibility is not None
    assert result.floor_feasibility["feasible"] is False
    assert result.fork_decision == "fresh"
    assert result.route_target == dispatch_module.ROUTE_ADMISSION_FRESH_FORK
    assert result.placeholder_body["phase_debt"] == dispatch_module.DEBT_PHASE_5


@pytest.mark.asyncio
async def test_positive_output_form_model_routes_to_phase_3():
    """output.form == 'model' → Phase 3 refusal envelope debt.

    Distinct from Service1Refusal — the model-refusal envelope is a
    NEW frozen contract (§6.5) that Phase 3 will land. Phase 2 emits
    the routing placeholder pointing at that debt.
    """
    req = _build_request(form=OutputForm.MODEL)
    result = await dispatch_module.dispatch(req)
    assert result.route_target == dispatch_module.ROUTE_PHASE_3_MODEL_REFUSAL
    assert result.placeholder_body["phase_debt"] == dispatch_module.DEBT_PHASE_3
    # No feasibility computed for model form — output-form refusal bypasses fork.
    assert result.feasibility_result is None
    assert result.fork_decision is None


@pytest.mark.asyncio
async def test_positive_output_form_knowledge_artifact_routes_to_phase_4():
    req = _build_request(form=OutputForm.KNOWLEDGE_ARTIFACT)
    result = await dispatch_module.dispatch(req)
    assert result.route_target == dispatch_module.ROUTE_PHASE_4_KNOWLEDGE_ARTIFACT
    assert result.placeholder_body["phase_debt"] == dispatch_module.DEBT_PHASE_4


@pytest.mark.asyncio
async def test_positive_output_form_callable_skill_routes_to_phase_4():
    req = _build_request(form=OutputForm.CALLABLE_SKILL)
    result = await dispatch_module.dispatch(req)
    assert result.route_target == dispatch_module.ROUTE_PHASE_4_CALLABLE_SKILL
    assert result.placeholder_body["phase_debt"] == dispatch_module.DEBT_PHASE_4


# ---------------------------------------------------------------------------
# Route-level wire shape
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_v2_dispatch_route_returns_501_with_placeholder():
    """POST /api/service_1/v2/dispatch returns 501 with dispatch envelope."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json={
                "entry": "external_request",
                "reach": {"scope_refs": ["nowhere_at_all"], "exclusions": [], "depth": "baseline"},
                "output": {
                    "form": "qualified_data",
                    "consumer": "person",
                    "grain": "per_claim",
                    "standard": {"minimum_class": "utterance"},
                },
                "envelope": {
                    "lawful_basis": "test",
                    "done_condition": "test",
                    "budget": "test",
                    "scope_ceiling": "test",
                    "commissioner": "test",
                    "committed_at": "2026-07-03T12:00:00+00:00",
                },
            },
        )
    assert resp.status_code == 501
    body = resp.json()
    assert body["route_target"] == dispatch_module.ROUTE_ADMISSION_FRESH_FORK
    assert body["fork_decision"] == "fresh"
    assert body["placeholder_body"]["outcome"] == "not_yet_implemented"


@pytest.mark.asyncio
async def test_v2_dispatch_route_rejects_malformed_body():
    """Missing required v2 field → Pydantic 422 (FastAPI default validation)."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json={"entry": "external_request"},  # missing everything else
        )
    assert resp.status_code == 422
