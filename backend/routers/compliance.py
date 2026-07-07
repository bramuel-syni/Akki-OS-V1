"""Phase 8 Stage B-5a Block 1 — Compliance Console read/prove router.

Endpoints (all under `/api/compliance`):
  * GET  /api/compliance/retention_config  — v2.1 §4.3 substrate
      (3 held-classes separately addressable, inheritance-as-default,
       honest-when-unset for B5a-G3).
  * GET  /api/compliance/refusals?month=YYYY-MM  — v2.1 §4.1 refusals
      card substrate (family-classified count over NorthenaLedgerRow_v1).

Owner E2 taxonomy: all denials 401/403 `{reason, detail}` — 4-code
registry only. NO new codes at B-5a.

Auth scope: `dpo` OR `admin` (per Stage A §3A dev default) — mirrored
by `_has_dpo_authority` below. Master_admin role explicitly NOT granted
compliance-read scope by default (Compliance and Administration are
distinct consoles per v2.1 §4 and §6); use `admin` if a caller needs
both (the seeded super-role).
"""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.compliance.coverage_marker import compose_coverage_marker
from services.compliance.deletion_ledger import emit_deletion_ledger_row
from services.compliance.refusals_aggregate import (
    MalformedMonthError,
    aggregate_refusals_by_month,
)
from services.compliance.retention_config import read_retention_config
from services.compliance.retention_config_writes import (
    LoosengingRefused,
    write_retention_config,
)
from services.retention.authorized_deletion import (
    _HELD_CLASS_TO_COLLECTION,
    execute_authorized_deletion,
)
from services.compliance.held_class_registry import HELD_CLASSES
from contracts.northena_ledger import LedgerArtifactRef


router = APIRouter(prefix="/compliance", tags=["compliance"])


def _has_dpo_authority(identity: Identity) -> bool:
    """A caller may view Compliance Console surfaces iff they carry the
    `dpo` role (or `admin`, the seeded super-role)."""
    roles = set(identity.roles)
    return "dpo" in roles or "admin" in roles


async def _require_dpo_or_deny(request: Request):
    """Return (identity, None) on permit, (None, JSONResponse) on deny.
    Two-step gate mirroring the master_admin router pattern (B-4)."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return None, result
    identity: Identity = result
    if not _has_dpo_authority(identity):
        return None, auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Compliance Console requires the `dpo` role (or `admin`). "
                "The caller identity is authenticated but lacks compliance "
                "authority."
            ),
        )
    return identity, None


@router.get("/refusals_coverage")
async def get_refusals_coverage(request: Request):
    """Sub-stage 1 Seam 3 substrate — refusals coverage marker.

    Returns per-family since-dates (E3.β query-time first-timestamp-per-family
    per Amendment E), the earliest date across seam-3-covered families, and
    an honest empty-state note when no refusal-terminal row carries a
    registered `stamp_audit["refusal_family"]` yet.

    Rendered by the Compliance Console §4.1 Refusals card rider as the
    Owner-supplied coverage-marker binding-copy (middle-dots `·` per E7).
    """
    _, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    resp = await compose_coverage_marker()
    return resp.model_dump(mode="json")


@router.get("/retention_config")
async def get_retention_config(request: Request):
    """v2.1 §4.3 substrate — read-only retention posture.

    Returns 3 held-classes with per-class posture (inheriting / explicit
    / unset) plus global_default. B5a-G3 substrate: when nothing set,
    all 3 classes render as unset and the surface fires the honest
    banner from v2.1 §4.3 line 76 verbatim.
    """
    _, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    resp = read_retention_config()
    return resp.model_dump(mode="json")


@router.get("/refusals")
async def get_refusals_by_month(request: Request, month: str = ""):
    """v2.1 §4.1 substrate — refusals-this-month aggregate.

    Query param `month=YYYY-MM` required. Returns family-classified
    totals over `NorthenaLedgerRow_v1` where `decision == "refused"`
    within the month window. Auth 403s + validation 422s STRUCTURALLY
    excluded (they don't write to the ledger).
    """
    _, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    try:
        resp = await aggregate_refusals_by_month(month)
    except MalformedMonthError as e:
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_month",
                "detail": str(e),
            },
        )
    return resp.model_dump(mode="json")


# ────────────────────────────────────────────────────────────────────
# Phase 8 Seam 3 Sub-stage 2 — retention-config WRITE + authorized-deletion
# ────────────────────────────────────────────────────────────────────


@router.post("/retention_config")
async def post_retention_config(request: Request):
    """Sub-stage 2 Seam 3 — retention-config write endpoint.

    Auth: DPO or admin.
    Body: `{held_class_name: {window_days: int|null}, ...}` — any subset of
        the 3 held-classes may be included.
    Behavior:
      - Validates payload shape (fail-fast on unknown held_class or bad shape).
      - Classifies each per-class delta as loosening / tightening /
        setting_from_unset / unchanged.
      - E2 binding condition (Amendment F rulings §10; Stage A §5.1):
        Any loosening in the payload refuses the ENTIRE write with
        HTTP 403 + body `{reason: "auth_scope_insufficient", detail:
        "awaiting_consequence_class_checker: ..."}`. Ledger row NOT
        written for refused loosening (LB gate assertion).
      - Accepted writes persist as `retention.v{N+1}.json` (append-only)
        AND emit a `NorthenaLedgerRow_v1` with `stamp_audit.data_class =
        "authorized_deletion"` NOT applicable — this is a config-write
        event, not a deletion. However, per Amendment F rulings §10 and
        Standing Discipline (governance-audit-trail), the write itself
        MAY emit a ledger row keyed by data_class in future dispatches.
        Sub-stage 2 does NOT ledger the config-write itself (deferred to
        Sub-stage 3 checker path); it ledgers ONLY deletion events.
      - Response: `{outcome, old_version, new_version, persisted_path,
        old_window_days_per_class, new_window_days_per_class}`.
    """
    identity, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_body",
                "detail": "Request body MUST be valid JSON.",
            },
        )
    try:
        attempt = await write_retention_config(
            payload=payload,
            actor_user_id=identity.user_id,
            actor_email=identity.email,
        )
    except LoosengingRefused as e:
        # Amendment G Ruling 6: loosening writes route through the checker
        # (rather than 403 refuse pre-checker). Retire the E2 loosening-
        # disabled gate; emit a ledger row + kick off dual-control state.
        import uuid as _uuid
        from services.checker import state_machine as _sm
        from services.compliance.deletion_ledger import emit_deletion_ledger_row as _emit
        from contracts.northena_ledger import LedgerArtifactRef as _AR
        try:
            init_result = await _sm.initiate(
                rule_class="retention_windows",
                from_value_ref=str(sorted(e.attempt.old_window_days_per_class.items())),
                to_value_ref=str(sorted(e.attempt.new_window_days_per_class.items())),
                initiator_id=identity.email,
                initiator_role="compliance",  # capacity role — Ruling 2
            )
        except Exception as init_exc:
            return JSONResponse(
                status_code=500,
                content={
                    "reason": "checker_infra_fault",
                    "detail": f"checker initiate failed: {init_exc}",
                },
            )
        # Ruling 6: emit a ledger row carrying stamp_audit.consequence_class.
        await _emit(
            run_id=f"ret-{_uuid.uuid4().hex[:12]}",
            trace_id=f"ret-trace-{_uuid.uuid4().hex[:12]}",
            data_class="unclassified",  # config-write itself is unclassified per registry v1
            held_class="retention_windows",
            keys_deleted=0,
            retention_rule_ref="retention.pending",
            actor=identity.email,
            artifact_ref=_AR(
                artifact_type="objective_request",
                artifact_id=f"retention-config-write-{init_result.request_id}",
                version=init_result.request_id,
            ),
            lawful_basis_ref="compliance:retention_config_write_pending",
            extra_stamp_audit={
                "consequence_class": init_result.consequence_class,  # Ruling 6
                "request_id": init_result.request_id,
                "state": init_result.state,
                "action": "loosening_pending_countersign",
            },
        )
        return JSONResponse(
            status_code=202,
            content={
                "outcome": "pending_counter_sign",
                "request_id": init_result.request_id,
                "state": init_result.state,
                "consequence_class": init_result.consequence_class,
                "detail": "Loosening/lengthening retention windows requires Administration counter-sign per §8 CK-B3 symmetry.",
            },
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": str(e)},
        )
    # Ruling 6: every accepted write emits a ledger row with consequence_class.
    import uuid as _uuid2
    from services.compliance.deletion_ledger import emit_deletion_ledger_row as _emit2
    from contracts.northena_ledger import LedgerArtifactRef as _AR2
    await _emit2(
        run_id=f"ret-{_uuid2.uuid4().hex[:12]}",
        trace_id=f"ret-trace-{_uuid2.uuid4().hex[:12]}",
        data_class="unclassified",
        held_class="retention_windows",
        keys_deleted=0,
        retention_rule_ref=f"retention.v{attempt.new_version}",
        actor=identity.email,
        artifact_ref=_AR2(
            artifact_type="objective_request",
            artifact_id=f"retention-config-v{attempt.new_version}",
            version=str(attempt.new_version),
        ),
        lawful_basis_ref="compliance:retention_config_write_tightening",
        extra_stamp_audit={
            "consequence_class": "tightening_unilateral",  # Ruling 6
            "action": attempt.outcome,
            "old_version": attempt.old_version,
            "new_version": attempt.new_version,
        },
    )
    return JSONResponse(
        status_code=200,
        content={
            "outcome": attempt.outcome,
            "old_version": attempt.old_version,
            "new_version": attempt.new_version,
            "persisted_path": attempt.persisted_path,
            "old_window_days_per_class": attempt.old_window_days_per_class,
            "new_window_days_per_class": attempt.new_window_days_per_class,
        },
    )


@router.post("/authorized_deletion")
async def post_authorized_deletion(request: Request):
    """Sub-stage 2 Seam 3 — authorized-deletion executor endpoint.

    Auth: DPO or admin.
    Body: `{held_class: str, retention_rule?: {window_days: int, ref?: str}}`.
        If `retention_rule` is absent, the endpoint looks up the current
        retention.vN.json for that held_class. If lookup returns
        `window_days: null` → 422 refusal `no_retention_rule_set`.
    Behavior:
      - Fires `execute_authorized_deletion(...)` (the ONLY authorized
        deletion I/O site under `no_unauthorized_deletion_path`).
      - Emits a `NorthenaLedgerRow_v1` via `emit_deletion_ledger_row`
        with `stamp_audit.data_class = "authorized_deletion"` +
        held_class + keys_deleted + retention_rule_ref + actor.
      - Response: `{outcome: "deleted", held_class, keys_deleted,
        retention_rule_ref}`.
    """
    identity, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_body",
                "detail": "Request body MUST be valid JSON.",
            },
        )
    if not isinstance(payload, dict):
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_payload",
                "detail": "Body MUST be an object.",
            },
        )
    held_class = payload.get("held_class")
    if held_class not in HELD_CLASSES:
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_payload",
                "detail": (
                    f"held_class must be one of {list(HELD_CLASSES)}; "
                    f"got {held_class!r}."
                ),
            },
        )
    rule = payload.get("retention_rule")
    if rule is None:
        # Look up current retention.vN.json for this held_class.
        from services.compliance.retention_config_writes import read_current_config
        current, version = read_current_config()
        days = current["held_classes"][held_class]["window_days"]
        rule = {"window_days": days, "ref": f"retention.v{version}"}
    if not isinstance(rule, dict) or "window_days" not in rule:
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_payload",
                "detail": "retention_rule must be {window_days:int|null[, ref:str]}.",
            },
        )
    if rule.get("window_days") is None:
        return JSONResponse(
            status_code=422,
            content={
                "reason": "no_retention_rule_set",
                "detail": (
                    f"Cannot execute authorized deletion for held_class "
                    f"{held_class!r}: no retention window set (window_days is null). "
                    "DPO must first set a retention window via POST "
                    "/api/compliance/retention_config."
                ),
            },
        )
    result = await execute_authorized_deletion(
        held_class=held_class,
        retention_rule=rule,
        actor=identity.email,
    )
    # Emit the deletion-event ledger row per E1.γ registry pattern.
    import uuid
    run_id = f"del-{uuid.uuid4().hex[:12]}"
    trace_id = f"del-trace-{uuid.uuid4().hex[:12]}"
    await emit_deletion_ledger_row(
        run_id=run_id,
        trace_id=trace_id,
        data_class="authorized_deletion",
        held_class=held_class,
        keys_deleted=result.keys_deleted,
        retention_rule_ref=result.retention_rule_ref,
        actor=result.actor,
        artifact_ref=LedgerArtifactRef(
            # LedgerArtifactRef.artifact_type is a frozen Literal
            # ('portfolio_mandate' | 'objective_request') at contract v1.
            # Deletion events use 'objective_request' as closest fit
            # (deletions target the request/state history). Documented
            # in Sub-stage 2 close report §12 pragmatic-choice note.
            artifact_type="objective_request",
            artifact_id=f"deletion-{held_class}",
            version=result.retention_rule_ref,
        ),
        lawful_basis_ref="compliance:dpo_authorized_deletion",
    )
    return JSONResponse(
        status_code=200,
        content={
            "outcome": "deleted",
            "held_class": result.held_class,
            "collection": result.collection,
            "keys_deleted": result.keys_deleted,
            "retention_rule_ref": result.retention_rule_ref,
            "actor": result.actor,
            "executed_at": result.executed_at,
        },
    )
