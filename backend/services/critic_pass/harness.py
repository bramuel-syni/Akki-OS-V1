"""Critic-pass Tier-2 harness · orchestrates RV/CR/QA disciplines.

Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` (2026-07-25 · FINAL).

Critic Seam Spec v1.0 §6.2 verbatim (Tier-2 independence rules):
    "No self-review (QA-3): the critic instance is never the instance
    that produced the artifact; where both are the same base model,
    independence is by context isolation."

QA-1 (detect, never decide): findings NEVER block execution.
QA-4 (findings carry honesty grammar): every finding evidence-classed
and cited.
QA-5 (the layer pays rent): catch/false-alarm ledger stands.

TQ §7 Part B verbatim (line 115): *"Production QA machinery (the Critic
Seam's Part B — same three tiers, second domain). The Critic Seam
guards what workers produce; this section applies the identical
architecture to what the pipeline produces."*

QA-7 custody boundary (TQ §7 line 125 · RULED): quality of PROTECTION
escalates as governance (fail-closed per-batch quarantine at
`backend/services/service_1/batch_quarantine.py`); quality of PRODUCT
routes as findings.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from services.critic_pass.rubric import RubricFinding, apply_rubric
from services.critic_pass.archive import append as archive_append
from services.critic_pass.calibration_ledger import (
    append_calibration_row,
    is_calibration_stale,
    sampling_rate_findings,
    sampling_rate_all_clears,
)


@dataclass(frozen=True)
class CriticPassVerdict:
    """A single Tier-2 critic-pass verdict on an artifact.

    QA-1: never blocks execution (returned as data, consumed by rulings).
    """

    artifact_ref: str
    findings: List[RubricFinding]
    critic_instance_id: str
    producing_instance_id: str


def run_critic_pass(
    artifact_ref: str,
    artifact_content: str,
    producing_instance_id: str,
    critic_instance_id: str,
    archive_verdict: bool = True,
) -> CriticPassVerdict:
    """Run the Tier-2 critic pass on an artifact.

    QA-3 enforcement: raises ValueError if critic_instance_id equals
    producing_instance_id.

    If `archive_verdict` is True, the verdict is appended to the archive
    ledger (per CIF §12 line 154 discipline).

    Returns the verdict (findings list · never gates the phase per QA-1).
    """
    findings = apply_rubric(
        artifact_ref=artifact_ref,
        artifact_content=artifact_content,
        producing_instance_id=producing_instance_id,
        critic_instance_id=critic_instance_id,
    )
    verdict = CriticPassVerdict(
        artifact_ref=artifact_ref,
        findings=findings,
        critic_instance_id=critic_instance_id,
        producing_instance_id=producing_instance_id,
    )
    if archive_verdict:
        archive_append(
            entry_type="critic_verdict",
            subject_ref=artifact_ref,
            evaluated_by=critic_instance_id,
            verdict_ref=f"critic:{artifact_ref}:{critic_instance_id}",
        )
    return verdict
