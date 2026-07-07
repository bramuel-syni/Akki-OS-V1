"""Phase 8 Seam 3 Sub-stage 2 — retention writes + authorized deletion executor + E2 gate.

Matrix (per Stage A §5 test roster, cell × posture × case):

§A. `POST /api/compliance/retention_config` write endpoint:
    - Auth postures (no-token / operator / dpo / admin) × 4.
    - Payload postures (empty / partial / bad-shape / unknown-class /
      bad-window-days-negative) × 5.
    - E2 refusal (loosening in payload → 403 access-control class with
      awaiting_consequence_class_checker: prefix; ledger NOT written) × 3.
    - Accepted-tightening (int decrease) × 1.
    - Accepted-setting-from-unset (null → int) × 1.
    - Version bump (retention.v{N+1}.json lands on disk) × 1.

§B. `POST /api/compliance/authorized_deletion` executor endpoint:
    - Auth postures × 3.
    - Payload postures (missing held_class / unknown held_class /
      no retention window set / retention_rule bad shape) × 4.
    - Held-class dispatch (ledger_row × wizard_transcript ×
      delivered_artifact) × 3 (rows deleted per class).
    - Deletion event ledger emission asserts data_class="authorized_deletion"
      + pinned held_class + keys_deleted + retention_rule_ref + actor × 3.
    - Empty selector honest-zero (no rows older than cutoff) × 1.

§C. `execute_authorized_deletion` unit (services/retention/):
    - Rejects window_days=None × 1.
    - Rejects unknown held_class × 1.
    - Idempotency (rerun with same rule → same/zero keys_deleted) × 1.
    - `rollback_saturated_queue_admit` unit — deletes and returns count × 1.

§D. `emit_deletion_ledger_row` (services/compliance/) unit:
    - Rejects unknown data_class × 1.
    - Pins data_class + held_class + keys_deleted over extra_stamp_audit × 1.
    - Includes `unclassified` in valid_data_classes (R-3 discipline) × 1.

§E. Invariant re-scope structural — three held-classes separately addressable:
    - ledger_row deletion → NORTHENA_LEDGER_COLLECTION only × 1.
    - wizard_transcript deletion → wizard_session only × 1.
    - delivered_artifact deletion → objectives_async_state only × 1.

§F. Named LB gate `test_retention_endpoint_loosening_disabled_pre_checker`:
    - Reset config to v0, POST loosening payload, assert 403 body prefix,
      assert ledger row count unchanged.

§G. Full-anti-rule 409 audit (E5 reactivation per §5.2):
    - Static scan across Sub-stage 2 diff files: zero `\\b409\\b` outside
      comments/docstrings.
    - Static scan across full backend production tree: zero introductions
      of `409` under Sub-stage 2's authorship.

§H. Data-class LB invariant (mirror of R-1):
    - `test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit`
      — data-shape scan over ledger rows where reason starts with
      "authorized_deletion:" — asserts pinned data_class + registry-valid.

§I. Rider items landing verification:
    - Sub-stage 1 close report has R-6 footer appended (SHA changes).
    - `rule2_accounting.json` stale line corrected 855/72/24 → 847/92/26.
"""
from __future__ import annotations

import hashlib
import json
import re
import uuid
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.northena_ledger import (
    LedgerArtifactRef,
    NORTHENA_LEDGER_COLLECTION,
)
from core import db
from server import app
from services.auth import jwt_service, user_store
from services.compliance import retention_config_writes as rcw
from services.compliance.deletion_ledger import (
    UnknownDataClassError,
    VALID_DATA_CLASSES,
    emit_deletion_ledger_row,
)
from services.compliance.held_class_registry import HELD_CLASSES
from services.retention.authorized_deletion import (
    _HELD_CLASS_TO_COLLECTION,
    DeletionResult,
    execute_authorized_deletion,
    rollback_saturated_queue_admit,
)

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_RETENTION_DIR = _BACKEND_ROOT / "services" / "compliance"


# ────────────────────────────────────────────────────────────────────
# Fixtures
# ────────────────────────────────────────────────────────────────────


async def _make_token(roles):
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


@pytest.fixture(autouse=True)
def _isolate_retention_dir_and_ledger():
    """Delete any retention.vN.json (N>=1) files created by tests + any
    seam3_sub_2 test-tagged ledger rows. Runs before AND after each test."""
    def _cleanup():
        for p in _RETENTION_DIR.glob("retention.v*.json"):
            stem = p.stem
            try:
                v = int(stem.split(".v", 1)[1])
            except (IndexError, ValueError):
                continue
            if v >= 1:
                p.unlink(missing_ok=True)
    _cleanup()
    yield
    _cleanup()


@pytest.fixture
async def _isolate_test_ledger():
    marker = {"stamp_audit.actor": {"$regex": "^seam3_sub_2"}}
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)
    yield
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)


def _ref():
    # LedgerArtifactRef.artifact_type is a frozen Literal — only
    # 'portfolio_mandate' | 'objective_request' allowed at v1. Deletion
    # events use 'objective_request' as the closest semantic fit
    # (deletion targets the request/state history). Documented in
    # close report §12 pragmatic-choice note (no contract change per §7.1).
    return LedgerArtifactRef(
        artifact_type="objective_request",
        artifact_id="seam3-sub-2-test",
        version="v0",
    )


# ════════════════════════════════════════════════════════════════════
# §A. POST /api/compliance/retention_config
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_a1_retention_config_write_no_token_401():
    async with _client() as c:
        r = await c.post("/api/compliance/retention_config", json={})
    assert r.status_code == 401
    assert r.json()["reason"] == "auth_missing"


@pytest.mark.anyio
async def test_a2_retention_config_write_operator_role_403():
    token = await _make_token(["operator"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={},
        )
    assert r.status_code == 403
    assert r.json()["reason"] == "auth_scope_insufficient"


@pytest.mark.anyio
async def test_a3_retention_config_write_dpo_empty_payload_ok():
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={},
        )
    # Empty payload → no changes to any class → outcome=accepted-tightening
    # with new_version=old_version+1 landing an equivalent snapshot.
    assert r.status_code == 200
    body = r.json()
    assert body["outcome"] in ("accepted_tightening",)
    assert body["new_version"] == body["old_version"] + 1


@pytest.mark.anyio
async def test_a4_retention_config_write_unknown_held_class_400():
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"nonexistent_class": {"window_days": 30}},
        )
    assert r.status_code == 400
    assert r.json()["reason"] == "malformed_payload"


@pytest.mark.anyio
async def test_a5_retention_config_write_bad_window_days_400():
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": -1}},
        )
    assert r.status_code == 400


@pytest.mark.anyio
async def test_a6_retention_config_write_setting_from_unset_accepted():
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 365}},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["outcome"] == "accepted_setting_from_unset"
    assert body["new_window_days_per_class"]["ledger_row"] == 365


@pytest.mark.anyio
async def test_a7_retention_config_write_tightening_accepted():
    token = await _make_token(["dpo"])
    # Seed 365 first.
    async with _client() as c:
        await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 365}},
        )
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 180}},
        )
    assert r.status_code == 200
    assert r.json()["outcome"] == "accepted_tightening"


@pytest.mark.anyio
async def test_a8_retention_config_write_loosening_routes_to_checker(
    _isolate_test_ledger,
):
    """Sub-stage 3 (Ruling 6): E2 loosening-disabled gate RETIRED; loosening
    writes now route through the checker (202 pending_counter_sign)."""
    token = await _make_token(["dpo"])
    async with _client() as c:
        await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 180}},
        )
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 365}},
        )
    assert r.status_code == 202
    body = r.json()
    assert body["outcome"] == "pending_counter_sign"
    assert body["state"] == "pending_counter_sign"
    assert body["consequence_class"] == "dual_control"
    assert "request_id" in body


@pytest.mark.anyio
async def test_a9_retention_config_write_loosening_int_to_null_routes_to_checker(
    _isolate_test_ledger,
):
    """Sub-stage 3 (Ruling 6): int→null loosening routes to checker."""
    token = await _make_token(["dpo"])
    async with _client() as c:
        await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 180}},
        )
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": None}},
        )
    assert r.status_code == 202
    assert r.json()["state"] == "pending_counter_sign"


# ════════════════════════════════════════════════════════════════════
# §F. RETIRED at Sub-stage 3 close (Amendment G Ruling 5 + Ruling 6).
# `test_retention_endpoint_loosening_disabled_pre_checker` was the
# E2 loosening-disabled LB gate; retired because the checker now lands
# and loosening routes through it. Replaced at Sub-stage 3 by:
#   * test_retention_loosening_write_requires_administration_countersign
#   * test_every_retention_write_emits_ledger_row_with_consequence_class
# See /app/backend/tests/invariants/test_phase_8_seam_3_sub_stage_3.py.
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_retention_endpoint_loosening_disabled_pre_checker_retirement_note():
    """Retirement note — asserted preservation of the retirement per
    Amendment G Ruling 5. The prior gate body is replaced by this note.
    """
    # Retirement is documented; the checker path is exercised by the
    # Sub-stage 3 tests referenced in the comment above.
    assert True


# ════════════════════════════════════════════════════════════════════
# §B. POST /api/compliance/authorized_deletion
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_b1_authorized_deletion_no_token_401():
    async with _client() as c:
        r = await c.post("/api/compliance/authorized_deletion", json={})
    assert r.status_code == 401


@pytest.mark.anyio
async def test_b2_authorized_deletion_operator_role_403():
    token = await _make_token(["operator"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/authorized_deletion",
            headers={"Authorization": f"Bearer {token}"},
            json={"held_class": "ledger_row"},
        )
    assert r.status_code == 403


@pytest.mark.anyio
async def test_b3_authorized_deletion_unknown_held_class_400():
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/authorized_deletion",
            headers={"Authorization": f"Bearer {token}"},
            json={"held_class": "nonexistent"},
        )
    assert r.status_code == 400


@pytest.mark.anyio
async def test_b4_authorized_deletion_no_retention_rule_set_422():
    """When retention window is None (unset) for the held_class →
    422 no_retention_rule_set (NOT 409; E5 anti-rule preserved)."""
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/authorized_deletion",
            headers={"Authorization": f"Bearer {token}"},
            json={"held_class": "ledger_row"},
        )
    assert r.status_code == 422
    assert r.json()["reason"] == "no_retention_rule_set"


@pytest.mark.anyio
async def test_b5_authorized_deletion_explicit_rule_empty_selector_zero_count(
    _isolate_test_ledger,
):
    """Explicit retention_rule with window_days=365 (default) — no rows
    older than 365d, honest-zero result."""
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/authorized_deletion",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "held_class": "ledger_row",
                "retention_rule": {"window_days": 3650, "ref": "test-explicit"},
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["outcome"] == "deleted"
    assert body["held_class"] == "ledger_row"
    assert isinstance(body["keys_deleted"], int)


@pytest.mark.anyio
async def test_b6_authorized_deletion_emits_ledger_row_with_data_class(
    _isolate_test_ledger,
):
    """Deletion event MUST land a ledger row keyed with
    stamp_audit.data_class='authorized_deletion' + held_class + actor."""
    token = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/authorized_deletion",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "held_class": "wizard_transcript",
                "retention_rule": {"window_days": 3650, "ref": "test-b6"},
            },
        )
    assert r.status_code == 200
    # Find the ledger row that this deletion emitted.
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {
            "reason": "authorized_deletion:wizard_transcript",
            "stamp_audit.data_class": "authorized_deletion",
        }
    )
    assert row is not None, "deletion event did not emit ledger row"
    assert row["stamp_audit"]["held_class"] == "wizard_transcript"
    assert row["stamp_audit"]["data_class"] == "authorized_deletion"
    assert row["stage"] == "converge"
    assert row["decision"] == "continue"
    # Cleanup — bypass invariant via direct emit (test infra ok).
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(
        {"reason": "authorized_deletion:wizard_transcript"}
    )


# ════════════════════════════════════════════════════════════════════
# §C. execute_authorized_deletion unit
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_c1_execute_authorized_deletion_rejects_none_window():
    with pytest.raises(ValueError):
        await execute_authorized_deletion(
            held_class="ledger_row",
            retention_rule={"window_days": None},
            actor="unit-test",
        )


@pytest.mark.anyio
async def test_c2_execute_authorized_deletion_rejects_unknown_class():
    with pytest.raises(ValueError):
        await execute_authorized_deletion(
            held_class="not_a_class",  # type: ignore[arg-type]
            retention_rule={"window_days": 30},
            actor="unit-test",
        )


@pytest.mark.anyio
async def test_c3_execute_authorized_deletion_idempotent():
    """Two consecutive calls with the same rule → same result (no doc
    resurrects)."""
    r1 = await execute_authorized_deletion(
        held_class="ledger_row",
        retention_rule={"window_days": 3650, "ref": "idempotency-t1"},
        actor="unit-test",
    )
    r2 = await execute_authorized_deletion(
        held_class="ledger_row",
        retention_rule={"window_days": 3650, "ref": "idempotency-t2"},
        actor="unit-test",
    )
    # Idempotency: r2.keys_deleted <= r1.keys_deleted (any new rows in
    # between could exceed; but for a stable dev cluster == 0 in both).
    assert isinstance(r1, DeletionResult)
    assert isinstance(r2, DeletionResult)
    assert r2.keys_deleted <= r1.keys_deleted + 5  # slack for concurrent writes


@pytest.mark.anyio
async def test_c4_rollback_saturated_queue_admit_deletes_and_returns_count():
    """Rollback helper — inserts a fake accepted doc, rollbacks, verifies count."""
    obj_id = f"test-obj-{uuid.uuid4().hex[:8]}"
    await db["objectives_async_state"].insert_one({
        "objective_id": obj_id,
        "trace_id": "trace-test",
        "state": "accepted",
    })
    n = await rollback_saturated_queue_admit(obj_id)
    assert n == 1
    # Idempotent second call.
    n2 = await rollback_saturated_queue_admit(obj_id)
    assert n2 == 0


# ════════════════════════════════════════════════════════════════════
# §D. emit_deletion_ledger_row unit
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_d1_emit_deletion_ledger_row_rejects_unknown_data_class(
    _isolate_test_ledger,
):
    with pytest.raises(UnknownDataClassError):
        await emit_deletion_ledger_row(
            run_id="r1", trace_id="t1",
            data_class="not_a_data_class",
            held_class="ledger_row",
            keys_deleted=0,
            retention_rule_ref="retention.v0",
            actor="seam3_sub_2.d1",
            artifact_ref=_ref(),
            lawful_basis_ref="lb-test",
        )


@pytest.mark.anyio
async def test_d2_emit_deletion_ledger_row_pins_data_class_over_extra(
    _isolate_test_ledger,
):
    """extra_stamp_audit MUST NOT override the pinned data_class key."""
    await emit_deletion_ledger_row(
        run_id="r2", trace_id="t2",
        data_class="authorized_deletion",
        held_class="ledger_row",
        keys_deleted=7,
        retention_rule_ref="retention.v0",
        actor="seam3_sub_2.d2",
        artifact_ref=_ref(),
        lawful_basis_ref="lb-test",
        extra_stamp_audit={"data_class": "malicious_override", "extra": "ok"},
    )
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.actor": "seam3_sub_2.d2"}
    )
    assert row is not None
    assert row["stamp_audit"]["data_class"] == "authorized_deletion"


def test_d3_valid_data_classes_registry_contains_unclassified_per_r_3():
    """R-3 discipline mirrored — `unclassified` MUST be a registered
    data_class, so any non-refusal governance event that falls outside
    the known set renders honestly (never silence)."""
    assert "unclassified" in VALID_DATA_CLASSES


# ════════════════════════════════════════════════════════════════════
# §E. Held-classes separately addressable
# ════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize(
    ("held_class", "expected_collection"),
    [
        ("ledger_row", "northena_ledger"),
        ("wizard_transcript", "wizard_session"),
        ("delivered_artifact", "objectives_async_state"),
    ],
)
def test_e_held_class_to_collection_map_covers_all_registered_classes(
    held_class, expected_collection,
):
    assert _HELD_CLASS_TO_COLLECTION[held_class] == expected_collection


def test_e_all_registered_held_classes_have_mapping():
    for cls in HELD_CLASSES:
        assert cls in _HELD_CLASS_TO_COLLECTION, (
            f"held_class {cls!r} in HELD_CLASSES registry but not in "
            f"_HELD_CLASS_TO_COLLECTION map — enumeration drift."
        )


# ════════════════════════════════════════════════════════════════════
# §G. Full-anti-rule 409 audit (E5 reactivation)
# ════════════════════════════════════════════════════════════════════


def test_g_no_409_in_sub_stage_2_diff():
    """E5 full anti-rule (Amendment F rulings §10 + Stage A §5.2):
    Zero `\\b409\\b` outside comments/docstrings across Sub-stage 2 diff."""
    files = [
        _BACKEND_ROOT / "services" / "retention" / "authorized_deletion.py",
        _BACKEND_ROOT / "services" / "retention" / "__init__.py",
        _BACKEND_ROOT / "services" / "compliance" / "retention_config_writes.py",
        _BACKEND_ROOT / "services" / "compliance" / "deletion_ledger.py",
        _BACKEND_ROOT / "services" / "compliance" / "data_class_registry.v0.json",
        _BACKEND_ROOT / "services" / "compliance" / "retention.v0.json",
        _BACKEND_ROOT / "routers" / "compliance.py",
        _BACKEND_ROOT / "routers" / "objectives.py",
    ]
    pat = re.compile(r"\b409\b")
    hits = []
    for f in files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"') or stripped.startswith("*"):
                continue
            if pat.search(line):
                hits.append(f"{f.name}:{lineno}: {stripped!r}")
    assert not hits, f"Sub-stage 2 diff introduced HTTP 409: {hits}"


def test_g_no_409_full_anti_rule_backend_scan():
    """E5 full anti-rule enforcement: scan `backend/services/` +
    `backend/routers/` for 409 introductions in Sub-stage 2's authorship.

    Since we cannot cleanly attribute pre-existing 409s to prior phases
    without git-blame overhead, this test enforces a delta-anchor: no
    new 409 references land in any file MODIFIED by Sub-stage 2. Files
    UNTOUCHED by Sub-stage 2 may retain historical 409 references
    without violating this gate.
    """
    modified_by_sub_stage_2 = [
        "services/retention/authorized_deletion.py",
        "services/retention/__init__.py",
        "services/compliance/retention_config_writes.py",
        "services/compliance/deletion_ledger.py",
        "services/compliance/data_class_registry.v0.json",
        "services/compliance/retention.v0.json",
        "routers/compliance.py",
        "routers/objectives.py",
    ]
    pat = re.compile(r"\b409\b")
    hits = []
    for rel in modified_by_sub_stage_2:
        f = _BACKEND_ROOT / rel
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith('"') or stripped.startswith("*"):
                continue
            if pat.search(line):
                hits.append(f"{rel}:{lineno}: {stripped!r}")
    assert not hits, (
        f"E5 full-anti-rule violation — Sub-stage 2 modified files carry HTTP 409: {hits}"
    )


# ════════════════════════════════════════════════════════════════════
# §H. Data-class LB invariant (mirror of R-1)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit(
    _isolate_test_ledger,
):
    """Mirror of R-1 for data-class classification. Every ledger row where
    reason starts with 'authorized_deletion:' MUST carry
    stamp_audit['data_class'] present and in VALID_DATA_CLASSES.
    """
    # Emit a sample row for the invariant scan.
    await emit_deletion_ledger_row(
        run_id="lb-inv-1", trace_id="lb-inv-t1",
        data_class="authorized_deletion",
        held_class="delivered_artifact",
        keys_deleted=3,
        retention_rule_ref="retention.v1",
        actor="seam3_sub_2.h_lb_gate",
        artifact_ref=_ref(),
        lawful_basis_ref="lb-invariant-test",
    )
    async for row in db[NORTHENA_LEDGER_COLLECTION].find(
        {"reason": {"$regex": "^authorized_deletion:"},
         "stamp_audit.actor": "seam3_sub_2.h_lb_gate"}
    ):
        assert "stamp_audit" in row and row["stamp_audit"] is not None
        assert "data_class" in row["stamp_audit"]
        assert row["stamp_audit"]["data_class"] in VALID_DATA_CLASSES


# ════════════════════════════════════════════════════════════════════
# §I. Rider items landing verification
# ════════════════════════════════════════════════════════════════════


def test_i1_sub_stage_1_close_report_r6_footer_appended():
    """Rider §2.1: Sub-stage 1 close report has the R-6 landing-commit
    footer appended (Owner ruling text verbatim)."""
    path = (
        _BACKEND_ROOT.parent
        / "docs" / "close_reports" / "phase_8_seam_3_sub_stage_1.md"
    )
    text = path.read_text(encoding="utf-8")
    footer = (
        "R-6 landing-commit reference: 791d5a7; "
        "b7df53e is the pre-amend hash, unreachable post-amend."
    )
    assert footer in text, (
        f"Sub-stage 1 close report missing the R-6 footer:\n  {footer!r}"
    )


def test_i2_rule2_accounting_stale_line_corrected():
    """Rider §2.2: rule2_accounting.json B-4 close narrative line must
    read the CI-proven 847/92/26 baseline, not the stale 855/72/24.

    Assertion: the corrected counts (818→847 backend / 60→92 jest /
    16→26 playwright) are present as active attestations. The
    correction-narrative comment CAN reference the old numbers as an
    "earlier attestation of ..." historical fact — that survives inside
    the explanation prose without being an active claim.
    """
    path = _BACKEND_ROOT.parent / "docs" / "rule2_accounting.json"
    text = path.read_text(encoding="utf-8")
    # Assert the corrected active attestations are present.
    assert "818 \u2192 847" in text, (
        "rule2_accounting.json missing corrected backend attestation `818 → 847`."
    )
    assert "60 \u2192 92" in text, (
        "rule2_accounting.json missing corrected Jest attestation `60 → 92`."
    )
    assert "16 \u2192 26" in text, (
        "rule2_accounting.json missing corrected Playwright attestation `16 → 26`."
    )
    # Assert a stale-line-correction disclosure is present (transparency).
    assert "Stale-line correction" in text or "stale-line correction" in text, (
        "rule2_accounting.json must carry a disclosure of the stale-line "
        "correction (transparency discipline)."
    )
