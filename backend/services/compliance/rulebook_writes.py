"""Phase 8 Stage B-5b — shared compliance-rulebook writer helper.

Routes writes for the compliance rule classes through the §8 consequence-
class checker landed at Sub-stage 3. Ruling B5b-E3 (γ) applied for
disclosure_type: constrained-str + JSON registry (`disclosure_types.v0.json`).
Ruling B5b-E2 (α) applied: server-side validation only; frontend renders
the plain-language error verbatim. Ruling B5b-G4 applied: every write
emits a ledger row with `stamp_audit["consequence_class"]`.
"""
from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Optional

from contracts.northena_ledger import LedgerArtifactRef
from services.checker import state_machine
from services.checker.effective_delay import consequence_class_for
from services.compliance.deletion_ledger import emit_deletion_ledger_row

_COMPLIANCE_DIR = Path(__file__).parent
_DISCLOSURE_TYPES_PATH = _COMPLIANCE_DIR / "disclosure_types.v0.json"

# Constrained-str regex for disclosure_type. Registry-mirrored per Ruling
# B5b-E3 (γ). New entries land as registry bumps + regex extension.
_DISCLOSURE_TYPE_PATTERN = re.compile(r"^(k_anonymity|l_diversity|dp_budget)$")


class RulebookWriteError(ValueError):
    """Server-side rulebook validation failure. Router encodes as 400."""


def load_disclosure_types() -> dict:
    with _DISCLOSURE_TYPES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_disclosure_type(value: str) -> str:
    """Constrained-str per Ruling B5b-E3 (γ). Registry-mirrored regex."""
    if not isinstance(value, str) or not _DISCLOSURE_TYPE_PATTERN.match(value):
        raise RulebookWriteError(
            f"disclosure_type={value!r} not in disclosure_types.v0.json "
            f"pattern; expected one of k_anonymity | l_diversity | dp_budget"
        )
    return value


async def initiate_and_ledger(
    *,
    rule_class: str,
    from_value_ref: str,
    to_value_ref: str,
    initiator_id: str,
    initiator_role: str,  # capacity role per Ruling 2
    lawful_basis_ref: str,
) -> dict:
    """Route a rulebook write through the checker + emit ledger row.

    Returns response body suitable for HTTP 202 pending state or the
    same shape for tightening_unilateral pending_delay.

    Ruling B5b-G4: every write emits a ledger row carrying
    stamp_audit["consequence_class"] (registry-valid per
    consequence_class.v0.json).
    """
    init_result = await state_machine.initiate(
        rule_class=rule_class,
        from_value_ref=from_value_ref,
        to_value_ref=to_value_ref,
        initiator_id=initiator_id,
        initiator_role=initiator_role,
    )
    await emit_deletion_ledger_row(
        run_id=f"rbw-{uuid.uuid4().hex[:12]}",
        trace_id=f"rbw-trace-{uuid.uuid4().hex[:12]}",
        data_class="unclassified",  # config-write ledger row itself is unclassified per registry v1
        held_class=rule_class,
        keys_deleted=0,
        retention_rule_ref=f"rulebook-write:{rule_class}",
        actor=initiator_id,
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",  # vestigial-by-ruling per Ruling 1(i)
            artifact_id=f"{rule_class}-write-{init_result.request_id}",
            version=init_result.request_id,
        ),
        lawful_basis_ref=lawful_basis_ref,
        extra_stamp_audit={
            "consequence_class": init_result.consequence_class,  # B5b-G4
            "request_id": init_result.request_id,
            "state": init_result.state,
            "rule_class": rule_class,
            "action": "rulebook_write_pending",
        },
    )
    return {
        "outcome": "pending_counter_sign"
        if init_result.state == "pending_counter_sign"
        else "pending_delay",
        "request_id": init_result.request_id,
        "state": init_result.state,
        "consequence_class": init_result.consequence_class,
        "rule_class": rule_class,
    }
