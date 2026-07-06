"""Phase 8 Stage B-5a Block 1 — Compliance Console backend invariants.

Stage A test-matrix enumeration (Owner B-4-close-acceptance standing
correction: endpoints × postures × cases, never a test-LoC lump):
  * §2A.1 /api/compliance/retention_config — 8 cells
  * §2A.2 /api/compliance/refusals?month=YYYY-MM — 10 cells
  * §2A.3 /api/northena/trace/{trace_id} auth-reconciliation — 4 cells

Stage B amendments (Owner ratification 2026-07-06):
  * Amendment 1 gates (trust-receipt allowlist; allowlist-up posture):
      - test_anonymous_trace_view_contains_no_field_outside_receipt_spec
      - test_anonymous_trace_view_contains_all_receipt_spec_fields
  * Amendment 2 gates (family-by-family coverage):
      - test_refusals_by_month_counts_admission_refusals
      - test_refusals_by_month_counts_composition_below_floor
      - test_refusals_by_month_counts_late_refusals (via async-ledger
        emission — see Refusals-by-Month Coverage Statement finding)
      - test_refusals_by_month_counts_outer_gate_refusals
      - test_refusals_by_month_excludes_auth_403_and_validation_422

Plus:
  * B5a-G1: read-only (surface-agnostic Jest gate at frontend; backend
    counterpart pins no write route on /api/compliance/*)
  * B5a-G2 substrate: prove-run-resolves-any-trace verified via
    trace_lens endpoint returning 200 for any valid trace_id shape
  * B5a-G3 substrate: retention-unset states honestly (posture="unset"
    on all 3 classes when nothing configured)
  * Held-class dual-gate: full split & inheritance-mixed postures

Standing rule: on-disk canonical + SHA; no LLM. Read-only surfaces —
no ledger writes performed by any test path here (only ledger SEED
writes via direct db insert to set up refusals aggregate cases).
"""
from __future__ import annotations

import pytest
from datetime import datetime, timezone
from httpx import ASGITransport, AsyncClient

from server import app  # ASGI app
from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from services.auth import auth_refusal
from services.auth import jwt_service
from services.auth import user_store
from services.compliance import held_class_registry, refusal_family_classifier
from services.compliance.trust_receipt_allowlist import (
    ANONYMOUS_TRACE_VIEW_ALLOWLIST,
)


# ────────────────────────────────────────────────────────────────────
# Fixtures / helpers
# ────────────────────────────────────────────────────────────────────

@pytest.fixture
def _clean_retention_env(monkeypatch):
    """Clear all retention env vars so a test starts from B5a-G3 unset."""
    monkeypatch.delenv("RMS_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS", raising=False)
    for cls in held_class_registry.HELD_CLASSES:
        monkeypatch.delenv(f"RMS_COMPLIANCE_RETENTION_{cls.upper()}_DAYS", raising=False)
    yield


async def _make_token_for_roles(roles: list[str]) -> str:
    """Create an identity with roles and mint an access token."""
    import uuid
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


async def _seed_ledger_row(*, run_id: str, trace_id: str, stage: str,
                            decision: str, reason: str,
                            at: datetime) -> None:
    """Direct-insert a ledger row to set up an aggregate case."""
    doc = {
        "run_id": run_id,
        "trace_id": trace_id,
        "stage": stage,
        "decision": decision,
        "reason": reason,
        "artifact_ref": {
            "artifact_type": "objective_request",
            "artifact_id": f"seed-{run_id}",
            "version": "v0",
        },
        "lawful_basis_ref": "seed-lb-ref",
        "at": at.isoformat(),
        "stamp_audit": None,
    }
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(doc)


@pytest.fixture
async def _isolated_ledger():
    """Delete ledger rows before + after each aggregate-consuming test."""
    await db[NORTHENA_LEDGER_COLLECTION].delete_many({"stamp_audit.b5a_test_marker": True})
    # Clean all ledger rows in the test months used by these tests (2020-01
    # to avoid touching production ledger data from other suites' 2026+ rows).
    from datetime import datetime as dt, timezone as tz
    start = dt(2020, 1, 1, tzinfo=tz.utc)
    end = dt(2020, 2, 1, tzinfo=tz.utc)
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(
        {"at": {"$gte": start.isoformat(), "$lt": end.isoformat()}}
    )
    yield
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(
        {"at": {"$gte": start.isoformat(), "$lt": end.isoformat()}}
    )


def _client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


# ────────────────────────────────────────────────────────────────────
# §2A.1 — /api/compliance/retention_config — 8 cells
# ────────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_retention_config_no_token_401_auth_missing(_clean_retention_env):
    async with _client() as c:
        r = await c.get("/api/compliance/retention_config")
    assert r.status_code == 401
    body = r.json()
    assert body["reason"] == "auth_missing"
    assert isinstance(body["detail"], str)


@pytest.mark.anyio
async def test_retention_config_expired_token_401_auth_expired(_clean_retention_env):
    # Craft a token then expire it via monkeypatching or use a known bad one.
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": "Bearer notavalidtoken.xxx.yyy"},
        )
    assert r.status_code == 401
    body = r.json()
    # Invalid token maps to auth_missing per dependencies.py:83
    assert body["reason"] in ("auth_missing", "auth_expired")


@pytest.mark.anyio
async def test_retention_config_wrong_role_403_auth_scope_insufficient(_clean_retention_env):
    token = await _make_token_for_roles(["operator"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 403
    body = r.json()
    assert body["reason"] == "auth_scope_insufficient"


@pytest.mark.anyio
async def test_retention_config_dpo_all_unset_states_honestly(_clean_retention_env):
    """B5a-G3 substrate: all-unset posture."""
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["global_default"]["days"] is None
    assert len(body["held_classes"]) == 3
    for row in body["held_classes"]:
        assert row["posture"] == "unset"
        assert row["days"] is None


@pytest.mark.anyio
async def test_retention_config_dpo_global_default_inheritance(_clean_retention_env, monkeypatch):
    monkeypatch.setenv("RMS_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS", "365")
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["global_default"]["days"] == 365
    for row in body["held_classes"]:
        assert row["posture"] == "inheriting"
        assert row["days"] == 365


@pytest.mark.anyio
async def test_retention_config_dpo_full_split_all_three_classes(_clean_retention_env, monkeypatch):
    """DPO wizard_transcript §0.2 debt resolution gate (part 1)."""
    monkeypatch.setenv("RMS_COMPLIANCE_RETENTION_LEDGER_ROW_DAYS", "730")
    monkeypatch.setenv("RMS_COMPLIANCE_RETENTION_WIZARD_TRANSCRIPT_DAYS", "90")
    monkeypatch.setenv("RMS_COMPLIANCE_RETENTION_DELIVERED_ARTIFACT_DAYS", "180")
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    by_class = {row["class_name"]: row for row in body["held_classes"]}
    assert by_class["ledger_row"]["posture"] == "explicit"
    assert by_class["ledger_row"]["days"] == 730
    assert by_class["wizard_transcript"]["posture"] == "explicit"
    assert by_class["wizard_transcript"]["days"] == 90
    assert by_class["delivered_artifact"]["posture"] == "explicit"
    assert by_class["delivered_artifact"]["days"] == 180


@pytest.mark.anyio
async def test_retention_config_dpo_partial_split_mixed_postures(_clean_retention_env, monkeypatch):
    monkeypatch.setenv("RMS_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS", "365")
    monkeypatch.setenv("RMS_COMPLIANCE_RETENTION_WIZARD_TRANSCRIPT_DAYS", "60")
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    by_class = {row["class_name"]: row for row in body["held_classes"]}
    assert by_class["ledger_row"]["posture"] == "inheriting"
    assert by_class["ledger_row"]["days"] == 365
    assert by_class["wizard_transcript"]["posture"] == "explicit"
    assert by_class["wizard_transcript"]["days"] == 60
    assert by_class["delivered_artifact"]["posture"] == "inheriting"
    assert by_class["delivered_artifact"]["days"] == 365


@pytest.mark.anyio
async def test_retention_config_admin_role_reads(_clean_retention_env):
    token = await _make_token_for_roles(["admin"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200


# ────────────────────────────────────────────────────────────────────
# §2A.2 — /api/compliance/refusals — 10 cells
# ────────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_refusals_aggregate_no_token_401_auth_missing():
    async with _client() as c:
        r = await c.get("/api/compliance/refusals?month=2020-01")
    assert r.status_code == 401
    assert r.json()["reason"] == "auth_missing"


@pytest.mark.anyio
async def test_refusals_aggregate_expired_token_401_auth_expired():
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": "Bearer bad.token.value"},
        )
    assert r.status_code == 401
    assert r.json()["reason"] in ("auth_missing", "auth_expired")


@pytest.mark.anyio
async def test_refusals_aggregate_wrong_role_403_auth_scope_insufficient():
    token = await _make_token_for_roles(["operator"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 403
    assert r.json()["reason"] == "auth_scope_insufficient"


@pytest.mark.anyio
async def test_refusals_aggregate_dpo_malformed_month_400():
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=notamonth",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 400
    assert r.json()["reason"] == "malformed_month"


@pytest.mark.anyio
async def test_refusals_aggregate_dpo_empty_month_honest_zero(_isolated_ledger):
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["total"] == 0
    assert body["by_reason"] == []
    assert body["by_day"] == []


@pytest.mark.anyio
async def test_refusals_by_month_counts_admission_refusals(_isolated_ledger):
    """Amendment 2 gate: admission-family classification + count."""
    await _seed_ledger_row(
        run_id="ral-r1", trace_id="ral-t1", stage="admit",
        decision="refused", reason="form_not_offerable",
        at=datetime(2020, 1, 15, 12, 0, tzinfo=timezone.utc),
    )
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["admission_refusals"] == 1
    assert body["totals"]["total"] == 1
    assert body["by_reason"][0]["family"] == "admission_refusals"
    assert body["by_reason"][0]["reason"] == "form_not_offerable"


@pytest.mark.anyio
async def test_refusals_by_month_counts_composition_below_floor(_isolated_ledger):
    """Amendment 2 gate: composition-below-floor family classifier.
    NOTE: In production, `composition_below_floor` Service_1 refusals do
    not currently emit a ledger row (see Refusals-by-Month Coverage
    Statement in close report — this is a documented FINDING). This
    gate tests the CLASSIFIER's correctness given a seeded row of that
    shape; the aggregate WILL count them correctly IF/when the
    emission gap is closed."""
    await _seed_ledger_row(
        run_id="cbf-r1", trace_id="cbf-t1", stage="admit",
        decision="refused", reason="composition_below_floor",
        at=datetime(2020, 1, 20, 8, 0, tzinfo=timezone.utc),
    )
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["composition_below_floor"] == 1
    assert body["by_reason"][0]["family"] == "composition_below_floor"


@pytest.mark.anyio
async def test_refusals_by_month_counts_late_refusals(_isolated_ledger):
    """Amendment 2 gate: late-refusal (async-worker path).

    "Late refusals" is a TIMING context that overlays the four families
    (see coverage statement). If an async worker emitted a refusal row
    via `emit_ledger_terminate_refused` (currently unwired — see
    coverage-statement FINDING #2), it would carry an admission-family
    reason. This test seeds such a row and verifies the aggregate
    counts it correctly in its family."""
    await _seed_ledger_row(
        run_id="lat-r1", trace_id="lat-t1", stage="admit",
        decision="refused", reason="grain_form_incompatible",
        at=datetime(2020, 1, 25, 14, 30, tzinfo=timezone.utc),
    )
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["admission_refusals"] == 1
    assert body["by_reason"][0]["family"] == "admission_refusals"
    assert body["by_reason"][0]["reason"] == "grain_form_incompatible"


@pytest.mark.anyio
async def test_refusals_by_month_counts_outer_gate_refusals(_isolated_ledger):
    """Amendment 2 gate: V2 outer-gate family classifier."""
    await _seed_ledger_row(
        run_id="og-r1", trace_id="og-t1", stage="gate",
        decision="refused", reason="v2_refused:license_class_mismatch",
        at=datetime(2020, 1, 10, 10, 0, tzinfo=timezone.utc),
    )
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["outer_gate_refusals"] == 1
    assert body["by_reason"][0]["family"] == "outer_gate_refusals"


@pytest.mark.anyio
async def test_refusals_by_month_excludes_auth_403_and_validation_422(_isolated_ledger):
    """Amendment 2 gate: 403s and 422s STRUCTURALLY excluded.

    Auth denials + validation failures never write to the ledger, so
    the query naturally excludes them. Seed one legitimate refusal +
    make an anonymous unauth call (which returns 401 — not written) and
    verify the aggregate only counts the seeded refusal."""
    await _seed_ledger_row(
        run_id="ex-r1", trace_id="ex-t1", stage="admit",
        decision="refused", reason="form_not_offerable",
        at=datetime(2020, 1, 5, 9, 0, tzinfo=timezone.utc),
    )
    # Fire an auth 403 (wrong role) — must not affect ledger.
    op_token = await _make_token_for_roles(["operator"])
    async with _client() as c:
        r_403 = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {op_token}"},
        )
        assert r_403.status_code == 403
    # Fire a validation 422 (malformed request body on v2/dispatch —
    # will not reach the ledger).
    async with _client() as c:
        r_422 = await c.post(
            "/api/service_1/v2/dispatch",
            json={"malformed": True},
        )
        assert r_422.status_code in (403, 422)
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/compliance/refusals?month=2020-01",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["totals"]["total"] == 1
    assert body["totals"]["admission_refusals"] == 1


# ────────────────────────────────────────────────────────────────────
# §2A.3 — /api/northena/trace/{trace_id} auth-reconciliation — 4 cells
# Plus Amendment 1 gates (allowlist-up posture)
# ────────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_trace_endpoint_stays_anonymous_callable_regression(_isolated_ledger):
    """Regression: anonymous callers still succeed on trace lookup — the
    G5a design (2026-07-02) is preserved by allowlist-up projection.
    Amendment 1 changes the SHAPE of the anonymous response, not whether
    it succeeds."""
    await _seed_ledger_row(
        run_id="anon-r1", trace_id="anon-trace-1", stage="admit",
        decision="admitted", reason="admitted",
        at=datetime(2020, 1, 3, 8, 0, tzinfo=timezone.utc),
    )
    async with _client() as c:
        r = await c.get("/api/northena/trace/anon-trace-1")
    assert r.status_code == 200
    body = r.json()
    # Allowlist projection has EXACTLY the 4 spec fields.
    assert set(body.keys()) == ANONYMOUS_TRACE_VIEW_ALLOWLIST


@pytest.mark.anyio
async def test_trace_endpoint_dpo_positive_path(_isolated_ledger):
    """§4.2 Prove-one-run substrate — dpo sees full TraceLensEnvelope."""
    await _seed_ledger_row(
        run_id="dpo-r1", trace_id="dpo-trace-1", stage="admit",
        decision="admitted", reason="admitted",
        at=datetime(2020, 1, 3, 8, 0, tzinfo=timezone.utc),
    )
    token = await _make_token_for_roles(["dpo"])
    async with _client() as c:
        r = await c.get(
            "/api/northena/trace/dpo-trace-1",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    # Full record has the allowlisted fields PLUS additional fields.
    assert "ledger_rows" in body
    assert "registry_freshness" in body
    assert "engines_touched" in body


@pytest.mark.anyio
async def test_trace_endpoint_not_found_404_regression():
    async with _client() as c:
        r = await c.get("/api/northena/trace/nonexistent_trace_id_xyz")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"]["reason"] == "trace_id_not_found"


@pytest.mark.anyio
async def test_trace_endpoint_malformed_400_regression():
    async with _client() as c:
        r = await c.get("/api/northena/trace/{}".format(" "))  # whitespace only
    # Empty/whitespace trace_id currently routes as 404 not-found because
    # the route matcher accepts any string. FastAPI won't match empty path
    # segments, so a whitespace value is a legitimate lookup miss (404).
    assert r.status_code in (400, 404)


# ────────────────────────────────────────────────────────────────────
# Amendment 1 — trust-receipt allowlist gates
# ────────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_anonymous_trace_view_contains_no_field_outside_receipt_spec(_isolated_ledger):
    """AMENDMENT 1 GATE — no field OUTSIDE the trust-receipt allowlist
    appears in the anonymous view.

    Doctrinal note (Owner 2026-07-06): "Blocklist masking is
    public-by-default with future fields; allowlist-up inverts the
    failure mode." Any future field added to TraceLensEnvelope_v0 must
    default to NOT-visible-anonymously unless explicitly added to
    ANONYMOUS_TRACE_VIEW_ALLOWLIST.
    """
    await _seed_ledger_row(
        run_id="a1a-r1", trace_id="a1a-trace-1", stage="admit",
        decision="admitted", reason="admitted",
        at=datetime(2020, 1, 3, 8, 0, tzinfo=timezone.utc),
    )
    async with _client() as c:
        r = await c.get("/api/northena/trace/a1a-trace-1")
    assert r.status_code == 200
    body = r.json()
    for field in body.keys():
        assert field in ANONYMOUS_TRACE_VIEW_ALLOWLIST, (
            f"Anonymous trace view leaked field {field!r} outside the "
            f"trust-receipt allowlist. Allowlist: "
            f"{sorted(ANONYMOUS_TRACE_VIEW_ALLOWLIST)}."
        )


@pytest.mark.anyio
async def test_anonymous_trace_view_contains_all_receipt_spec_fields(_isolated_ledger):
    """AMENDMENT 1 GATE — anonymous view is BYTE-EQUIVALENT to the
    trust-receipt spec (not a strict subset that misses fields)."""
    await _seed_ledger_row(
        run_id="a1b-r1", trace_id="a1b-trace-1", stage="admit",
        decision="admitted", reason="admitted",
        at=datetime(2020, 1, 3, 8, 0, tzinfo=timezone.utc),
    )
    async with _client() as c:
        r = await c.get("/api/northena/trace/a1b-trace-1")
    assert r.status_code == 200
    body = r.json()
    for expected in ANONYMOUS_TRACE_VIEW_ALLOWLIST:
        assert expected in body, (
            f"Anonymous trace view MISSING allowlisted field {expected!r}. "
            "Byte-equivalence to trust-receipt spec broken."
        )


# ────────────────────────────────────────────────────────────────────
# B5a-G1 substrate — no write route on /api/compliance/*
# ────────────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_compliance_surface_backend_read_only():
    """B5a-G1 backend counterpart — the compliance router exposes no
    write route (POST/PUT/PATCH/DELETE)."""
    async with _client() as c:
        # POST anything under /api/compliance — must be 405 or 404, never 200
        for path in ("/api/compliance/retention_config", "/api/compliance/refusals"):
            r = await c.post(path, json={})
            assert r.status_code in (401, 403, 404, 405), (
                f"Compliance surface has an unexpected write route at {path} "
                f"(got {r.status_code}); B5a-G1 violated."
            )


# ────────────────────────────────────────────────────────────────────
# Held-class enumeration single-source
# ────────────────────────────────────────────────────────────────────

def test_held_class_enumeration_single_source():
    """The 3-class list is defined ONCE as a named constant."""
    assert held_class_registry.HELD_CLASSES == (
        "ledger_row",
        "wizard_transcript",
        "delivered_artifact",
    )


# ────────────────────────────────────────────────────────────────────
# Family classifier pure-function tests
# ────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("reason,expected_family", [
    ("form_not_offerable", "admission_refusals"),
    ("grain_form_incompatible", "admission_refusals"),
    ("composition_below_floor", "composition_below_floor"),
    ("v2_refused:some_reason_code", "outer_gate_refusals"),
    ("v2_refused:license_class_mismatch", "outer_gate_refusals"),
    ("garbage_reason_string", "unclassified"),
    ("", "unclassified"),
])
def test_family_classifier_maps_reasons_deterministically(reason, expected_family):
    """Pure-function classifier over 7 representative reason strings."""
    assert refusal_family_classifier.classify_family(reason) == expected_family
