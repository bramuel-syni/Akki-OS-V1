"""Phase 8 Stage B-5b — B-4 retrofit voiding logic per Owner Ruling B5b-E4.

At B-4 retrofit landing (compliance rule classes flip to read-only on
Administration Console), in-flight admin-initiated compliance-rule
checker requests are VOIDED. Each voided request emits a ledger row
with data_class="retrofit_authority_voided" + reason="retrofit_authority_transfer".
Grandfathering REJECTED — write-effect authority in both consoles
simultaneously is the RT-R2 violation in miniature.

Trivially green on today's null population (checker landed at Sub-stage 3
with zero admin-initiated compliance-rule writes yet); permanent LB
thereafter.
"""
from __future__ import annotations

import logging
import uuid
from typing import List

from contracts.northena_ledger import LedgerArtifactRef
from core import db
from services.checker.rule_change_request import (
    RuleChangeRequest,
    STATE_PENDING_COUNTER_SIGN,
    STATE_PENDING_DELAY,
    STATE_SUSPENDED,
    now_iso,
)
from services.checker.state_machine import CHECKER_COLLECTION
from services.compliance.deletion_ledger import emit_deletion_ledger_row

log = logging.getLogger(__name__)

# Compliance rule classes per BCR §3.13 RT-R1: retention, disclosure,
# lawful_basis, source_standing.
_COMPLIANCE_RULE_CLASSES = {
    "retention_windows",
    "disclosure_thresholds",
    "lawful_basis_registry",
    "source_standing_table",
}


async def void_admin_initiated_compliance_pending() -> List[dict]:
    """Void all in-flight admin-initiated compliance-rule checker requests
    per Owner Ruling B5b-E4. Emits a `retrofit_authority_voided` ledger
    row per voided item.

    Returns the list of voided items (may be empty — trivially green on
    today's null population).
    """
    query = {
        "state": {"$in": [STATE_PENDING_COUNTER_SIGN, STATE_PENDING_DELAY]},
        "initiator_role": "admin",  # admin capacity role (Ruling 2)
        "rule_class": {"$in": list(_COMPLIANCE_RULE_CLASSES)},
    }
    voided: List[dict] = []
    async for doc in db[CHECKER_COLLECTION].find(query):
        prior_state = doc["state"]
        voided_at = now_iso()
        await db[CHECKER_COLLECTION].update_one(
            {"request_id": doc["request_id"]},
            {"$set": {
                "state": STATE_SUSPENDED,  # reuse suspended-terminal semantic
                "prior_state": prior_state,
                "suspended_by_id": "system:retrofit",
                "suspended_by_role": "system",
                "suspend_reason": "retrofit_authority_transfer",
                "suspended_at": voided_at,
            }},
        )
        await emit_deletion_ledger_row(
            run_id=f"rtr-{uuid.uuid4().hex[:12]}",
            trace_id=f"rtr-trace-{uuid.uuid4().hex[:12]}",
            data_class="retrofit_authority_voided",
            held_class=doc["rule_class"],
            keys_deleted=0,
            retention_rule_ref=f"retrofit-void:{doc['rule_class']}",
            actor="system:retrofit",
            artifact_ref=LedgerArtifactRef(
                artifact_type="objective_request",  # vestigial-by-ruling per Ruling 1(i)
                artifact_id=f"retrofit-void-{doc['request_id']}",
                version=doc["request_id"],
            ),
            lawful_basis_ref="compliance:retrofit_authority_transfer",
            extra_stamp_audit={
                "rule_class": doc["rule_class"],
                "request_id": doc["request_id"],
                "voided_at": voided_at,
                "reason": "retrofit_authority_transfer",  # Owner verbatim
                "prior_state": prior_state,
                "prior_initiator_id": doc.get("initiator_id"),
                "prior_initiator_role": doc.get("initiator_role"),
            },
        )
        voided.append({
            "request_id": doc["request_id"],
            "rule_class": doc["rule_class"],
            "prior_state": prior_state,
        })
    log.info("retrofit_authority_transfer_voided_count=%d", len(voided))
    return voided
