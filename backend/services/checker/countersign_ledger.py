"""§8 checker ledger emitters — rule-change events.

Ruling 1(i)+(ii) applied disposition:
    * `artifact_ref` is REQUIRED on `NorthenaLedgerRow_v1` → uses the
      vestigial-by-ruling pattern from Sub-stage 2 (artifact_type=
      "objective_request"). Honest event class lives at
      `stamp_audit["data_class"]`.
    * The existing Sub-stage 2 `emit_deletion_ledger_row` performs the
      `data_class` registry validation. We call the same code path to
      guarantee the LB gate covers our new rule-change classes too.

Ruling 3 semantics:
    * `emit_countersign_ledger_row` — dual-control countersigned event
      (`data_class="countersigned_rule_change"`). Ruling 2: uses CAPACITY
      roles at initiator_role/checker_role.
    * `emit_tightening_effective_row` — tightening becomes effective at
      delay expiry (`data_class="tightening_effective"`).
    * `emit_tightening_objected_row` — objection annotation event
      (`data_class="tightening_objected"`); does NOT halt tightening.
    * `emit_owner_suspended_row` — owner-suspend action
      (`data_class="owner_suspended_tightening"`); the ONLY halt action.
"""
from __future__ import annotations

import logging
from typing import Optional

from contracts.northena_ledger import LedgerArtifactRef
from services.compliance.deletion_ledger import emit_deletion_ledger_row

log = logging.getLogger(__name__)


def _vestigial_artifact_ref(rule_class: str, request_id: str) -> LedgerArtifactRef:
    """Per Ruling 1(i): governance-event rows reuse Sub-stage 2's
    artifact_type="objective_request" pragmatic-choice pattern. The honest
    event class lives at stamp_audit["data_class"]."""
    return LedgerArtifactRef(
        # NOTE: vestigial-by-ruling per Amendment G Ruling 1(i). On
        # governance-event rows, artifact_type is non-authoritative;
        # data_class in stamp_audit is the event class.
        artifact_type="objective_request",
        artifact_id=f"rule-change-{rule_class}-{request_id}",
        version=request_id,
    )


async def _emit_rule_change_row(
    *,
    data_class: str,
    run_id: str,
    trace_id: str,
    rule_class: str,
    request_id: str,
    stamp_extras: dict,
    lawful_basis_ref: str,
):
    """Common emit path — reuses Sub-stage 2 deletion_ledger's registry
    validation + stamp_audit sidecar shape. That covers Ruling 1(ii):
    the same LB gate covers new rule-change classes because the same
    writer + registry are used."""
    return await emit_deletion_ledger_row(
        run_id=run_id,
        trace_id=trace_id,
        data_class=data_class,
        held_class=rule_class,  # `held_class` slot repurposed for rule_class label
        keys_deleted=0,  # not-a-deletion; honest zero
        retention_rule_ref=f"rule-change:{rule_class}",
        actor=stamp_extras.get("actor", "checker"),
        artifact_ref=_vestigial_artifact_ref(rule_class, request_id),
        lawful_basis_ref=lawful_basis_ref,
        extra_stamp_audit={
            **stamp_extras,
            "rule_class": rule_class,
            "request_id": request_id,
        },
    )


async def emit_countersign_ledger_row(
    *,
    run_id: str,
    trace_id: str,
    rule_class: str,
    request_id: str,
    consequence_class: str,
    initiator_id: str,
    initiator_role: str,
    checker_id: str,
    checker_role: str,
    initiated_at: str,
    countersigned_at: str,
    lawful_basis_ref: str = "compliance:dual_control_countersign",
):
    """CK-B1 dual-identity pinned-key emission."""
    return await _emit_rule_change_row(
        data_class="countersigned_rule_change",
        run_id=run_id,
        trace_id=trace_id,
        rule_class=rule_class,
        request_id=request_id,
        stamp_extras={
            "consequence_class": consequence_class,
            "initiator_id": initiator_id,
            "initiator_role": initiator_role,  # capacity role per Ruling 2
            "checker_id": checker_id,
            "checker_role": checker_role,  # capacity role per Ruling 2
            "initiated_at": initiated_at,
            "countersigned_at": countersigned_at,
            "actor": checker_id,
        },
        lawful_basis_ref=lawful_basis_ref,
    )


async def emit_tightening_effective_row(
    *,
    run_id: str,
    trace_id: str,
    rule_class: str,
    request_id: str,
    consequence_class: str,
    initiator_id: str,
    initiator_role: str,
    initiated_at: str,
    effective_at: str,
    effective_delay_seconds: int,
    lawful_basis_ref: str = "compliance:unilateral_tightening_effective",
):
    return await _emit_rule_change_row(
        data_class="tightening_effective",
        run_id=run_id,
        trace_id=trace_id,
        rule_class=rule_class,
        request_id=request_id,
        stamp_extras={
            "consequence_class": consequence_class,
            "initiator_id": initiator_id,
            "initiator_role": initiator_role,
            "initiated_at": initiated_at,
            "effective_at": effective_at,
            "effective_delay_seconds": effective_delay_seconds,
            "actor": initiator_id,
        },
        lawful_basis_ref=lawful_basis_ref,
    )


async def emit_tightening_objected_row(
    *,
    run_id: str,
    trace_id: str,
    rule_class: str,
    request_id: str,
    consequence_class: str,
    objector_id: str,
    objector_role: str,
    objection_reason: str,
    objected_at: str,
    underlying_state: str,
    lawful_basis_ref: str = "compliance:tightening_objection_annotation",
):
    """Ruling 3: annotate + escalate. NEVER a halt. underlying_state is
    typically `pending_delay` — tightening continues in that state."""
    return await _emit_rule_change_row(
        data_class="tightening_objected",
        run_id=run_id,
        trace_id=trace_id,
        rule_class=rule_class,
        request_id=request_id,
        stamp_extras={
            "consequence_class": consequence_class,
            "objector_id": objector_id,
            "objector_role": objector_role,
            "objection_reason": objection_reason,
            "owner_escalated": True,
            "objected_at": objected_at,
            "underlying_state": underlying_state,
            "actor": objector_id,
        },
        lawful_basis_ref=lawful_basis_ref,
    )


async def emit_owner_suspended_row(
    *,
    run_id: str,
    trace_id: str,
    rule_class: str,
    request_id: str,
    consequence_class: str,
    suspended_by_id: str,
    suspended_by_role: str,
    reason: str,
    suspended_at: str,
    prior_state: str,
    lawful_basis_ref: str = "compliance:owner_suspend_tightening",
):
    """Ruling 3: the ONLY halt action."""
    return await _emit_rule_change_row(
        data_class="owner_suspended_tightening",
        run_id=run_id,
        trace_id=trace_id,
        rule_class=rule_class,
        request_id=request_id,
        stamp_extras={
            "consequence_class": consequence_class,
            "suspended_by_id": suspended_by_id,
            "suspended_by_role": suspended_by_role,
            "reason": reason,
            "suspended_at": suspended_at,
            "prior_state": prior_state,
            "actor": suspended_by_id,
        },
        lawful_basis_ref=lawful_basis_ref,
    )
