"""Critic-pass Tier-2 rubric — CR-1..CR-7 executable rubric cells.

Owner ruling: `docs/rulings/critic_pass_e1_2026_07_25.md` (2026-07-25 · FINAL).

Critic Seam Spec v1.0 §6.1 verbatim rubric:
    "CR-1 anti-re-derivation · CR-2 anti-fabrication ·
     CR-3 conflation test (D-3) · CR-4 scope semantics (D7) ·
     CR-5 enforcement honesty (D-5) · CR-6 self-audit audit."

CIF §6 A5.2 verbatim (CR-7 amendment):
    "It enters standing machinery as a Critic Seam rubric amendment (CR-7)."

QA-1 (Critic Seam v1.0 §8): *"detect, never decide — no finding blocks
execution, edits artifact, or gates phase."*
QA-3 (Critic Seam v1.0 §8): *"no self-review — the critic instance is
never the instance that produced the artifact."*
QA-4 (Critic Seam v1.0 §8): *"findings carry honesty grammar — every
finding evidence-classed and cited."*
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Literal, Optional


RubricItemId = Literal[
    "CR-1", "CR-2", "CR-3", "CR-4", "CR-5", "CR-6", "CR-7",
]

ALL_RUBRIC_ITEMS: tuple[RubricItemId, ...] = (
    "CR-1", "CR-2", "CR-3", "CR-4", "CR-5", "CR-6", "CR-7",
)


@dataclass(frozen=True)
class RubricFinding:
    """Tier-2 finding row (QA-1 detect, QA-4 honesty grammar).

    Findings NEVER block execution (QA-1); consumed only by rulings.
    """

    rubric_item: RubricItemId
    artifact_ref: str
    finding_text: str
    evidence_class: Literal["fact", "recalled", "inferred"]
    citation: str  # source line-anchor or SHA reference


@dataclass(frozen=True)
class RubricItem:
    """One rubric cell — CR-1..CR-7 (Critic Seam v1.0 §6.1 + CIF §6 A5.2 CR-7)."""

    item_id: RubricItemId
    label: str
    verbatim_anchor: str  # spec line-anchor for the rubric statement
    checker: Callable[[str, str], Optional[RubricFinding]] | None = None
    # `None` at Stage A landing · concrete checkers land at execution phase
    # per each artifact-consumer path; here the RubricItem shape is
    # authoritative and executable-in-principle.


def _mk_item(
    item_id: RubricItemId,
    label: str,
    verbatim_anchor: str,
) -> RubricItem:
    return RubricItem(item_id=item_id, label=label, verbatim_anchor=verbatim_anchor)


TIER_2_RUBRIC: Dict[RubricItemId, RubricItem] = {
    "CR-1": _mk_item(
        "CR-1",
        "anti-re-derivation",
        "Critic Seam v1.0 §6.1 verbatim: 'CR-1 anti-re-derivation'",
    ),
    "CR-2": _mk_item(
        "CR-2",
        "anti-fabrication",
        "Critic Seam v1.0 §6.1 verbatim: 'CR-2 anti-fabrication'",
    ),
    "CR-3": _mk_item(
        "CR-3",
        "conflation test (D-3)",
        "Critic Seam v1.0 §6.1 verbatim: 'CR-3 conflation test (D-3)'",
    ),
    "CR-4": _mk_item(
        "CR-4",
        "scope semantics (D7)",
        "Critic Seam v1.0 §6.1 verbatim: 'CR-4 scope semantics (D7)'",
    ),
    "CR-5": _mk_item(
        "CR-5",
        "enforcement honesty (D-5)",
        "Critic Seam v1.0 §6.1 verbatim: 'CR-5 enforcement honesty (D-5)'",
    ),
    "CR-6": _mk_item(
        "CR-6",
        "self-audit audit",
        "Critic Seam v1.0 §6.1 verbatim: 'CR-6 self-audit audit'",
    ),
    "CR-7": _mk_item(
        "CR-7",
        "CIF selection-defect checklist (Owner-verbatim coach-correction-history · replay-only)",
        "CIF §6 A5.2 verbatim: 'It enters standing machinery as a Critic Seam rubric amendment (CR-7).'",
    ),
}


def get_rubric_item(item_id: RubricItemId) -> RubricItem:
    """Return the RubricItem for a given CR-N identifier."""
    return TIER_2_RUBRIC[item_id]


def apply_rubric(
    artifact_ref: str,
    artifact_content: str,
    producing_instance_id: str,
    critic_instance_id: str,
) -> List[RubricFinding]:
    """Apply Tier-2 rubric CR-1..CR-7 to an artifact.

    QA-3 enforcement: raises `ValueError` if the critic instance equals
    the producing instance (no self-review).

    Returns a list of RubricFinding rows; QA-1 discipline: findings
    NEVER block · they are consumed by rulings only.

    Concrete rubric checker functions land per-artifact-consumer at
    subsequent execution phases (this scaffold is the executable rubric
    surface; each checker is a Tier-2 seam per §6.2 independence rule).
    """
    if critic_instance_id == producing_instance_id:
        raise ValueError(
            "QA-3 violation: critic instance MUST NOT equal producing "
            "instance (no self-review)."
        )
    findings: List[RubricFinding] = []
    # Concrete checker execution is per-consumer at the execution phase;
    # the rubric shape is authoritative and hard-fail-testable here.
    for item_id in ALL_RUBRIC_ITEMS:
        item = TIER_2_RUBRIC[item_id]
        if item.checker is None:
            continue  # Stage A: rubric surface authoritative · checkers land per-consumer
        finding = item.checker(artifact_ref, artifact_content)
        if finding is not None:
            findings.append(finding)
    return findings
