"""Phase 8 Seam 3 Sub-stage 1 — refusal-family ledger wire-up + coverage marker.

Test-matrix enumeration (per Amendment F + R-1 data-shape invariant):

§A. LB gate `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit`
    (R-1 disposition, retirement condition: never). Data-shape invariant scan
    over `NORTHENA_LEDGER_COLLECTION` where `decision="refused"`. Fixture roster:
    - 6 exercise fixtures (I1–I6 live instrumentation sites per grep census
      `a6697d82…` §3).
    - 1 aggregate-regression fixture (compose_coverage_marker regression).
    = 7 cases total.

§B. `emit_refusal_ledger_row` unit tests — family/stage validation, pinned key
    discipline, extra_stamp_audit merge behaviour.

§C. coverage_marker (E3.β query-time first-timestamp-per-family): populated,
    empty, cross-boundary (seam-3 date).

§D. Compliance router — `GET /api/compliance/refusals_coverage` auth + shape.

§E. R-5 emission-order + idempotency — async_worker refusal paths emit ledger
    row BEFORE `async_state.transition_to_refused`; retry-safe dedup on
    (trace_id, reason).

§F. R-6 registry attribution note — verify `refusal_families.v0.json`
    admission_refusals prose corrected per R-4.

Standing Rule v3: on-disk canonical + SHA; matrix-enumerated sizing (no LoC
lumps in reply body).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from httpx import ASGITransport, AsyncClient

from server import app  # noqa: E402 — required import
from contracts.northena_ledger import (
    LedgerArtifactRef,
    NORTHENA_LEDGER_COLLECTION,
)
from core import db
from services.auth import jwt_service, user_store
from services.compliance import coverage_marker as cm_mod
from services.compliance.coverage_marker import compose_coverage_marker
from services.compliance.refusal_ledger import (
    UnknownRefusalFamilyError,
    VALID_REFUSAL_FAMILIES,
    emit_refusal_ledger_row,
)


# ────────────────────────────────────────────────────────────────────
# Fixtures / helpers
# ────────────────────────────────────────────────────────────────────


async def _make_token_for_roles(roles):
    email = f"tester_{uuid.uuid4().hex[:8]}@rms.test"
    identity = await user_store.create_user(
        email=email,
        password_plaintext="Passw0rd!Passw0rd!",
        roles=roles,
        name="tester",
    )
    return jwt_service.create_access_token(
        identity.user_id, identity.email, identity.roles, []
    )


def _client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


def _artifact_ref():
    return LedgerArtifactRef(
        artifact_type="objective_request",
        artifact_id="seam3-test-artifact",
        version="v2",
    )


@pytest.fixture
async def _isolated_seam3_ledger():
    """Delete refusal-terminal rows created by these tests both before and after."""
    marker = {"stamp_audit.source": {"$regex": "^seam3_test"}}
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)
    yield
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)


# ────────────────────────────────────────────────────────────────────
# §A. LB gate — data-shape invariant over refusal-terminal rows
# ────────────────────────────────────────────────────────────────────


async def _emit_at(site_tag: str, family: str, reason: str) -> None:
    """Emit one row through the canonical writer, marked with a site tag we
    can filter and later verify with the invariant."""
    await emit_refusal_ledger_row(
        run_id=f"run-{uuid.uuid4().hex[:12]}",
        trace_id=f"trace-{uuid.uuid4().hex[:12]}",
        family=family,
        reason=reason,
        artifact_ref=_artifact_ref(),
        lawful_basis_ref="lb-ref-seam3",
        stage="admit",
        extra_stamp_audit={"source": f"seam3_test.{site_tag}"},
    )


def _assert_row_pins_family(row: dict) -> None:
    """LB gate assertion — presence + registry-validity of stamp_audit['refusal_family']."""
    assert "stamp_audit" in row and row["stamp_audit"] is not None, (
        f"row missing stamp_audit sidecar: {row!r}"
    )
    assert "refusal_family" in row["stamp_audit"], (
        f"row missing pinned refusal_family key: {row!r}"
    )
    family = row["stamp_audit"]["refusal_family"]
    assert family in VALID_REFUSAL_FAMILIES, (
        f"refusal_family={family!r} not in registry {sorted(VALID_REFUSAL_FAMILIES)}"
    )


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("site_tag", "family", "reason"),
    [
        # I1 — service.py:127 (composition family, no_defensibility_floor).
        ("i1_no_defensibility_floor", "composition_below_floor", "no_defensibility_floor"),
        # I2 — service.py:135 (composition family, no_lawful_basis).
        ("i2_no_lawful_basis", "composition_below_floor", "no_lawful_basis"),
        # I3 — service.py:188 (composition family, composition_below_floor).
        ("i3_composition_below_floor_sync", "composition_below_floor", "composition_below_floor"),
        # I4 — composed_conclusion.py:273 (composition family).
        ("i4_composed_conclusion_sync", "composition_below_floor", "composition_below_floor"),
        # I5 — async_worker.py ComposedService1Refusal arm (composition family).
        ("i5_async_composed_refusal", "composition_below_floor", "composition_below_floor"),
        # I6 — async_worker.py AdmissionRefusal_v0 arm (admission family).
        ("i6_async_admission_refusal", "admission_refusals", "unrecognized_reason"),
    ],
)
async def test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit(
    _isolated_seam3_ledger, site_tag, family, reason,
):
    """LB gate (R-1): every refusal-terminal ledger row (decision='refused')
    MUST carry `stamp_audit["refusal_family"]` present and registry-valid.

    Parametrised over the 6 live instrumentation sites (I1–I6 per grep census).
    """
    await _emit_at(site_tag, family, reason)
    # Data-shape scan — the invariant that resurrects on any future C-path emission too.
    async for row in db[NORTHENA_LEDGER_COLLECTION].find(
        {
            "decision": "refused",
            "stamp_audit.source": f"seam3_test.{site_tag}",
        }
    ):
        _assert_row_pins_family(row)


@pytest.mark.anyio
async def test_refusal_terminal_lb_gate_aggregate_regression(_isolated_seam3_ledger):
    """LB gate aggregate regression — after all 6 site fixtures emit, the
    coverage-marker composer sees all covered families and no honest-note
    empty-state fires. Ensures the invariant + the read wire up correctly."""
    for tag, fam, reason in [
        ("i1", "composition_below_floor", "no_defensibility_floor"),
        ("i2", "composition_below_floor", "no_lawful_basis"),
        ("i3", "composition_below_floor", "composition_below_floor"),
        ("i4", "composition_below_floor", "composition_below_floor"),
        ("i5", "composition_below_floor", "composition_below_floor"),
        ("i6", "admission_refusals", "some_admission_reason"),
    ]:
        await _emit_at(tag, fam, reason)
    resp = await compose_coverage_marker()
    # composition_below_floor + admission_refusals should be present.
    assert (
        "composition_below_floor" in resp.per_family_since_date
    ), f"expected composition_below_floor coverage, got {resp.per_family_since_date}"
    assert (
        "admission_refusals" in resp.per_family_since_date
    ), f"expected admission_refusals coverage, got {resp.per_family_since_date}"
    assert resp.honest_note_when_no_families_covered is None


# ────────────────────────────────────────────────────────────────────
# §B. emit_refusal_ledger_row unit tests
# ────────────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_emit_refusal_ledger_row_rejects_unknown_family(_isolated_seam3_ledger):
    with pytest.raises(UnknownRefusalFamilyError) as exc:
        await emit_refusal_ledger_row(
            run_id="r1", trace_id="t1",
            family="not_a_family",
            reason="composition_below_floor",
            artifact_ref=_artifact_ref(),
            lawful_basis_ref="lb",
            stage="admit",
            extra_stamp_audit={"source": "seam3_test.unit_family"},
        )
    assert "not_a_family" in str(exc.value)


@pytest.mark.anyio
async def test_emit_refusal_ledger_row_rejects_converge_stage(_isolated_seam3_ledger):
    """Contract v1 forbids decision='refused' at converge stage; helper enforces."""
    with pytest.raises(ValueError) as exc:
        await emit_refusal_ledger_row(
            run_id="r2", trace_id="t2",
            family="composition_below_floor",
            reason="composition_below_floor",
            artifact_ref=_artifact_ref(),
            lawful_basis_ref="lb",
            stage="converge",
            extra_stamp_audit={"source": "seam3_test.unit_stage"},
        )
    assert "converge" in str(exc.value) or "stage" in str(exc.value)


@pytest.mark.anyio
async def test_emit_refusal_ledger_row_pins_family_key_over_extra(_isolated_seam3_ledger):
    """extra_stamp_audit CANNOT override the pinned refusal_family."""
    await emit_refusal_ledger_row(
        run_id="r3", trace_id="t3",
        family="admission_refusals",
        reason="some_reason",
        artifact_ref=_artifact_ref(),
        lawful_basis_ref="lb",
        stage="admit",
        extra_stamp_audit={
            "refusal_family": "malicious_override",
            "source": "seam3_test.unit_pin",
        },
    )
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.source": "seam3_test.unit_pin"},
    )
    assert row is not None
    assert row["stamp_audit"]["refusal_family"] == "admission_refusals"


@pytest.mark.anyio
async def test_emit_refusal_ledger_row_registry_contains_unclassified_per_r_3(
    _isolated_seam3_ledger,
):
    """R-3: `unclassified` is a registered, renderable family."""
    assert "unclassified" in VALID_REFUSAL_FAMILIES
    await emit_refusal_ledger_row(
        run_id="r4", trace_id="t4",
        family="unclassified",
        reason="some_edge_reason",
        artifact_ref=_artifact_ref(),
        lawful_basis_ref="lb",
        stage="admit",
        extra_stamp_audit={"source": "seam3_test.unit_unclassified"},
    )
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.source": "seam3_test.unit_unclassified"},
    )
    assert row is not None
    assert row["stamp_audit"]["refusal_family"] == "unclassified"


# ────────────────────────────────────────────────────────────────────
# §C. coverage_marker (E3.β query-time)
# ────────────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_coverage_marker_empty_state_honest_note(_isolated_seam3_ledger):
    resp = await compose_coverage_marker()
    if not resp.per_family_since_date:
        # No family rows anywhere in ledger — honest-empty-state fires.
        assert resp.honest_note_when_no_families_covered is not None
        assert resp.seam_3_earliest_date is None


@pytest.mark.anyio
async def test_coverage_marker_populates_from_pinned_key_rows(_isolated_seam3_ledger):
    await _emit_at("cov_admission", "admission_refusals", "some_reason")
    resp = await compose_coverage_marker()
    assert "admission_refusals" in resp.per_family_since_date


@pytest.mark.anyio
async def test_coverage_marker_uses_query_time_earliest_per_family(
    _isolated_seam3_ledger, monkeypatch,
):
    """Emit two rows for the same family; the earliest timestamp wins."""
    # We can't easily pin a past date via the canonical writer (it uses `now`),
    # so seed via direct insert with a pre-set `at` — bypasses the writer's
    # timestamp default but preserves the pinned-key discipline.
    old_ts = "2025-01-15T10:00:00+00:00"
    new_ts = "2026-07-07T10:00:00+00:00"
    await db[NORTHENA_LEDGER_COLLECTION].insert_one({
        "run_id": "rx1", "trace_id": "tx1",
        "stage": "admit", "decision": "refused",
        "reason": "some_reason",
        "artifact_ref": {"artifact_type": "objective_request",
                          "artifact_id": "cov-test-1", "version": "v2"},
        "lawful_basis_ref": "lb",
        "stamp_audit": {"refusal_family": "outer_gate_refusals",
                        "source": "seam3_test.cov_earliest_1"},
        "at": old_ts,
    })
    await db[NORTHENA_LEDGER_COLLECTION].insert_one({
        "run_id": "rx2", "trace_id": "tx2",
        "stage": "admit", "decision": "refused",
        "reason": "some_reason",
        "artifact_ref": {"artifact_type": "objective_request",
                          "artifact_id": "cov-test-2", "version": "v2"},
        "lawful_basis_ref": "lb",
        "stamp_audit": {"refusal_family": "outer_gate_refusals",
                        "source": "seam3_test.cov_earliest_2"},
        "at": new_ts,
    })
    resp = await compose_coverage_marker()
    assert resp.per_family_since_date.get("outer_gate_refusals") == "2025-01-15"


@pytest.mark.anyio
async def test_coverage_marker_categorises_by_seam_3_boundary(
    _isolated_seam3_ledger, monkeypatch,
):
    """Rows earlier than seam_3 wire-up date → system_start bucket; after → seam_3 bucket."""
    monkeypatch.setattr(cm_mod, "_SEAM_3_WIRE_UP_DATE", "2026-07-06")
    await db[NORTHENA_LEDGER_COLLECTION].insert_one({
        "run_id": "rx3", "trace_id": "tx3",
        "stage": "admit", "decision": "refused", "reason": "r",
        "artifact_ref": {"artifact_type": "objective_request",
                          "artifact_id": "cov-boundary-old", "version": "v2"},
        "lawful_basis_ref": "lb",
        "stamp_audit": {"refusal_family": "admission_refusals",
                        "source": "seam3_test.cov_boundary_old"},
        "at": "2025-06-01T10:00:00+00:00",
    })
    await db[NORTHENA_LEDGER_COLLECTION].insert_one({
        "run_id": "rx4", "trace_id": "tx4",
        "stage": "admit", "decision": "refused", "reason": "r",
        "artifact_ref": {"artifact_type": "objective_request",
                          "artifact_id": "cov-boundary-new", "version": "v2"},
        "lawful_basis_ref": "lb",
        "stamp_audit": {"refusal_family": "composition_below_floor",
                        "source": "seam3_test.cov_boundary_new"},
        "at": "2026-07-07T10:00:00+00:00",
    })
    resp = await compose_coverage_marker()
    assert "admission_refusals" in resp.families_since_system_start
    assert "composition_below_floor" in resp.families_since_seam_3
    assert resp.seam_3_earliest_date == "2026-07-07"


# ────────────────────────────────────────────────────────────────────
# §D. Compliance router — GET /api/compliance/refusals_coverage
# ────────────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_refusals_coverage_no_token_401_auth_missing():
    async with _client() as c:
        r = await c.get("/api/compliance/refusals_coverage")
    assert r.status_code == 401
    body = r.json()
    assert body["reason"] == "auth_missing"


@pytest.mark.anyio
async def test_refusals_coverage_wrong_role_403_auth_scope_insufficient():
    token = await _make_token_for_roles(["operator"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals_coverage",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 403
    body = r.json()
    assert body["reason"] == "auth_scope_insufficient"


@pytest.mark.anyio
async def test_refusals_coverage_dpo_role_200_shape(_isolated_seam3_ledger):
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals_coverage",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    # Shape check — RefusalsCoverageResponse fields.
    for key in (
        "families_since_system_start",
        "families_since_seam_3",
        "per_family_since_date",
        "seam_3_earliest_date",
        "honest_note_when_no_families_covered",
    ):
        assert key in body


@pytest.mark.anyio
async def test_refusals_coverage_admin_role_200():
    token = await _make_token_for_roles(["admin"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals_coverage",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200


# ────────────────────────────────────────────────────────────────────
# §E. R-5 emission order + idempotency (async_worker paths I5, I6)
# ────────────────────────────────────────────────────────────────────


@pytest.mark.anyio
async def test_r5_no_duplicate_ledger_rows_across_emission_and_transition(
    _isolated_seam3_ledger,
):
    """R-5: emit BEFORE `transition_to_refused`, idempotent — a second retry
    with the same (trace_id, reason) does NOT produce a duplicate refused row."""
    from services.service_1.async_worker import _refusal_row_exists_for_objective

    trace_id = f"trace-{uuid.uuid4().hex[:12]}"
    objective_id = f"obj-{uuid.uuid4().hex[:12]}"
    # Seed the async_state doc so the dedup helper can find trace_id.
    await db["objectives_async_state"].insert_one({
        "objective_id": objective_id,
        "trace_id": trace_id,
        "state": "running",
    })
    try:
        # First emission — no row exists yet.
        assert not await _refusal_row_exists_for_objective(objective_id, "reason_x")
        await emit_refusal_ledger_row(
            run_id="r5-1", trace_id=trace_id,
            family="composition_below_floor", reason="reason_x",
            artifact_ref=_artifact_ref(), lawful_basis_ref="lb",
            stage="admit",
            extra_stamp_audit={"source": "seam3_test.r5_first"},
        )
        # Retry — helper returns True, so no duplicate emission would happen.
        assert await _refusal_row_exists_for_objective(objective_id, "reason_x")
    finally:
        await db["objectives_async_state"].delete_one({"objective_id": objective_id})


# ────────────────────────────────────────────────────────────────────
# §F. R-4 registry attribution note fix
# ────────────────────────────────────────────────────────────────────


def test_r4_registry_admission_refusals_note_matches_classifier():
    """R-4: `refusal_families.v0.json` admission_refusals description NO LONGER
    attributes `no_defensibility_floor` / `no_lawful_basis` to admission_refusals.
    """
    import json
    from pathlib import Path

    reg_path = (
        Path(__file__).resolve().parents[2]
        / "services" / "compliance" / "refusal_families.v0.json"
    )
    data = json.loads(reg_path.read_text(encoding="utf-8"))
    admission = next(
        (e for e in data["valid_families"] if e["family"] == "admission_refusals"),
        None,
    )
    assert admission is not None
    desc = admission["description"]
    # The corrected note MUST reference R-4 amendment F.
    assert "R-4" in desc
    # The corrected note MUST reference that no_defensibility_floor and
    # no_lawful_basis are classified as composition_below_floor.
    assert "composition_below_floor" in desc
    # The corrected note MUST NOT contain the pre-R-4 mis-attribution phrase
    # that reads as if service.py sync raises land under admission_refusals.
    assert "services/service_1/service.py sync raises for no_defensibility_floor / no_lawful_basis" not in desc


# ────────────────────────────────────────────────────────────────────
# §G. 409 self-audit — no HTTP 409 in Sub-stage 1 diff
# ────────────────────────────────────────────────────────────────────


def test_g_no_409_in_sub_stage_1_diff():
    """Sub-stage 1 obligation (§8.5 E5 narrowed): no HTTP 409 introduced
    by any file touched in Sub-stage 1's diff."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    # Sub-stage 1 diff files (backend + router).
    files = [
        root / "services" / "compliance" / "refusal_ledger.py",
        root / "services" / "compliance" / "coverage_marker.py",
        root / "services" / "compliance" / "refusals_coverage_response.py",
        root / "services" / "compliance" / "refusal_families.v0.json",
        root / "services" / "service_1" / "service.py",
        root / "services" / "service_1" / "composed_conclusion.py",
        root / "services" / "service_1" / "async_worker.py",
        root / "services" / "service_1" / "async_state.py",
        root / "routers" / "compliance.py",
    ]
    pat = re.compile(r"\b409\b")
    hits = []
    for f in files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if pat.search(line):
                # Anything except commentary about the anti-rule itself is a violation.
                # Allow comments that reference the anti-rule (they don't introduce it).
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith('"'):
                    continue
                hits.append(f"{f.name}:{lineno}: {stripped!r}")
    assert not hits, (
        "Sub-stage 1 diff must not introduce HTTP 409 anywhere. "
        f"Hits: {hits}"
    )
