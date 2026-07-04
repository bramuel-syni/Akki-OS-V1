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
from typing import Optional

import httpx
import pytest
from httpx import ASGITransport

from contracts.async_delivery_accepted import AsyncDeliveryAccepted_v0
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
    idempotency_key: Optional[str] = "idem-dispatch-test",
) -> ObjectiveRequest_v2:
    """Minimal ObjectiveRequest_v2 for dispatch tests.

    Phase 5 Stage B migration (2026-07-04): `idempotency_key` field
    added — required on external_request per v3 §7 bullet 6. Defaulted
    to a stable test string; tests that need to exercise the missing
    or mismatched-key paths override explicitly.
    """
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
        idempotency_key=(idempotency_key if entry == ObjectiveEntry.EXTERNAL_REQUEST else None),
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

    Phase 5 Stage B migration (2026-07-04): fresh-fork returns
    `AsyncDeliveryAccepted_v0` (§7 §7.1 acceptance 202) with a valid
    idempotency_key, rather than the pre-Stage-B `DispatchResult`
    placeholder. The fork-decision assertion is validated by the
    async-accepted result surface — the objective is enqueued via the
    async pathway (only reachable on FRESH per dispatch.dispatch
    control-flow — confirmed by grep-negative on the source).
    """
    await _clear_registry()
    req = _build_request(
        entry=ObjectiveEntry.EXTERNAL_REQUEST,
        scope_refs=[_AUG["uncensused_scope_ref"]],
        form=OutputForm.QUALIFIED_DATA,
        idempotency_key="idem-fresh-unknown-freshness",
    )
    result = await dispatch_module.dispatch(req)

    # Fresh-fork terminal shape at Phase 5 Stage B: AsyncDeliveryAccepted_v0.
    assert isinstance(result, AsyncDeliveryAccepted_v0), (
        f"Expected AsyncDeliveryAccepted_v0 on fresh-fork; "
        f"got {type(result).__name__}: {result!r}"
    )
    assert result.status == "accepted"
    assert result.objective_id.startswith("obj-")
    assert result.trace_id.startswith("trc-")


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
    outcome. The wire shape must be distinct from Service1Refusal@v0
    AND from AdmissionRefusal@v0 (Phase 3 landing).

    Service1Refusal@v0 canonical shape (contracts/service_1_refusal.py):
      { outcome: 'refused', reason, run_id, trace_id, asked,
        supported_class, what_would_raise_it }

    AdmissionRefusal@v0 canonical shape (contracts/admission_refusal.py,
    landed Phase 3, 2026-07-03):
      { outcome: 'refused', reason, trace_id, requested_output_form,
        off_menu_fact, what_you_can_do, computed_at }

    Phase-2 placeholder canonical shape (dispatch._make_placeholder):
      { outcome: 'not_yet_implemented', reason:
        'phase_2_scaffold_downstream_deferred', route, phase_debt,
        trace_id }

    Disjoint outcome discriminators; disjoint field-sets.

    Phase 3 migration (Condition 5): `form == "model"` is REMOVED from
    the placeholder-iteration list because it now emits an actual
    governed refusal (AdmissionRefusal@v0). The remaining cases still
    emit scaffold placeholders (their receivers stay Phase-4/5-debt).
    """
    await _clear_registry()

    # Iterate cases that STILL emit placeholders post-Phase-3 AND
    # post-Phase-5. Phase 5 Stage B migration (2026-07-04): the
    # external_request + un-censused reach case (fresh-fork) is
    # REMOVED from this iteration — fresh-fork now returns
    # `AsyncDeliveryAccepted_v0` (§7 202), not a `DispatchResult`
    # placeholder. The remaining cases (work_order, knowledge_artifact,
    # callable_skill) still emit placeholders for their respective
    # phase-4/5-debt receivers.
    cases = [
        _build_request(form=OutputForm.KNOWLEDGE_ARTIFACT),
        _build_request(form=OutputForm.CALLABLE_SKILL),
        _build_request(entry=ObjectiveEntry.WORK_ORDER, form=OutputForm.QUALIFIED_DATA),
    ]
    for req in cases:
        result = await dispatch_module.dispatch(req)
        # Every placeholder case returns a DispatchResult (NOT an
        # AdmissionRefusal — the union collapses to DispatchResult here).
        assert isinstance(result, dispatch_module.DispatchResult), (
            f"Case {req.output.form} expected DispatchResult; got {type(result).__name__}"
        )
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
        # AdmissionRefusal fields must ALSO not appear at top level of placeholder.
        for ar_field in ("off_menu_fact", "what_you_can_do", "requested_output_form"):
            assert ar_field not in pb, (
                f"Phase-2 placeholder MUST NOT carry AdmissionRefusal field "
                f"{ar_field!r} — Phase-2/Phase-3 rendering separation violated."
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
    """external_request + feasible floor + warm-fork qualified_data →
    §6.1 packaging returns `QualifiedDataPayload` @200.

    Post-Phase-4a (2026-07-03): warm-fork + qualified_data no longer
    emits a scaffold placeholder — it now returns the actual §6.1
    qualified-data payload via
    `services.service_1.qualified_data.package_qualified_data`.
    (Condition-5 migration analogous to Phase 3's MODEL → refusal migration.)

    To keep license-class filter passing, `feed_id=citizen_tv_news`
    maps to `editorial_use`; the default commissioner="test_commissioner"
    derives to `editorial_use` (config's `default_class`).
    """
    await _clear_registry()
    await _seed_fresh_row("s://a/r.raw", "warm_region_qd", "fact")
    await _seed_fresh_row("s://a/s.raw", "warm_region_qd", "utterance")
    await _seed_fresh_row("s://a/t.raw", "warm_region_qd", "utterance")

    req = _build_request(
        entry=ObjectiveEntry.EXTERNAL_REQUEST,
        scope_refs=["warm_region_qd"],
        form=OutputForm.QUALIFIED_DATA,
        minimum_class=DefensibilityClass.UTTERANCE,
    )
    # Override feed_id on all rows to citizen_tv_news (editorial_use).
    from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION as _C
    await db[_C].update_many({}, {"$set": {"feed_id": "citizen_tv_news"}})

    result = await dispatch_module.dispatch(req)

    # Post-Phase-4a: return is QualifiedDataPayload (not DispatchResult).
    from services.service_1.qualified_data import QualifiedDataPayload
    assert isinstance(result, QualifiedDataPayload), (
        f"warm+qualified_data MUST return QualifiedDataPayload post-Phase-4a; "
        f"got {type(result).__name__}"
    )
    assert result.unit_count == 3
    assert len(result.units) == 3
    for unit in result.units:
        assert "defensibility" in unit


@pytest.mark.asyncio
async def test_positive_external_request_fresh_fork_below_floor():
    """external_request + infeasible floor → fresh fork.

    Populated Registry with only NON_FACTUAL rows; floor=FACT.
    derive_floor_feasibility.feasible == False. Fork MUST be `fresh`.

    Phase 5 Stage B migration (2026-07-04): fresh-fork with a valid
    idempotency_key returns `AsyncDeliveryAccepted_v0` (§7 202),
    replacing the pre-Stage-B `DispatchResult` placeholder body.
    """
    await _clear_registry()
    await _seed_fresh_row("s://b/x.raw", "below_floor_region", "non_factual")
    await _seed_fresh_row("s://b/y.raw", "below_floor_region", "utterance")

    req = _build_request(
        entry=ObjectiveEntry.EXTERNAL_REQUEST,
        scope_refs=["below_floor_region"],
        form=OutputForm.QUALIFIED_DATA,
        minimum_class=DefensibilityClass.FACT,  # No FACT rows in Registry
        idempotency_key="idem-below-floor-fresh",
    )
    result = await dispatch_module.dispatch(req)
    # Fresh-fork terminal shape at Phase 5 Stage B.
    assert isinstance(result, AsyncDeliveryAccepted_v0), (
        f"Fresh-fork MUST return AsyncDeliveryAccepted_v0 at Stage B; "
        f"got {type(result).__name__}"
    )
    assert result.status == "accepted"
    assert result.objective_id.startswith("obj-")


@pytest.mark.asyncio
async def test_positive_output_form_model_routes_to_admission_refusal():
    """`output.form == 'model'` → AdmissionRefusal_v0 (Phase 3 landing).

    Post-Phase-3 (2026-07-03): the scaffold 501 placeholder that
    previously represented this route is REPLACED by an actual
    governed refusal envelope emission (AdmissionRefusal@v0, 17th
    frozen contract). Direct-dispatch test — the isinstance return is
    now `AdmissionRefusal_v0`, not `DispatchResult`.

    Historical name in this test file was `test_positive_output_form_model_routes_to_phase_3`;
    renamed post-Phase-3 to reflect the actual receiver landing.
    """
    from contracts.admission_refusal import AdmissionRefusal_v0
    req = _build_request(form=OutputForm.MODEL)
    result = await dispatch_module.dispatch(req)
    assert isinstance(result, AdmissionRefusal_v0), (
        f"form == 'model' MUST now return AdmissionRefusal_v0 (Phase 3); "
        f"got {type(result).__name__}"
    )
    assert result.outcome == "refused"
    assert result.reason == "form_not_offerable"
    assert result.requested_output_form == "model"


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
async def test_v2_dispatch_route_returns_202_async_delivery_accepted_on_fresh_fork():
    """POST /api/service_1/v2/dispatch returns 202 with AsyncDeliveryAccepted_v0.

    Phase 5 Stage B migration (2026-07-04): the pre-Stage-B 501 with
    DispatchResult placeholder for fresh-fork is REPLACED by an async
    admission accepting envelope at HTTP 202. Test renamed to reflect
    the ratified receiver landing.
    """
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
                "idempotency_key": "idem-v2-route-fresh-test",
            },
        )
    assert resp.status_code == 202, (
        f"Post-Stage-B fresh-fork MUST return HTTP 202 with AsyncDeliveryAccepted_v0; "
        f"got {resp.status_code}: {resp.text}"
    )
    body = resp.json()
    assert body["status"] == "accepted"
    assert body["objective_id"].startswith("obj-")
    assert body["trace_id"].startswith("trc-")
    # Contract validation of the response body.
    envelope = AsyncDeliveryAccepted_v0.model_validate(body)
    assert envelope.status == "accepted"


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
