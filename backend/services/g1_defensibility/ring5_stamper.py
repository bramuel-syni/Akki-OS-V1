"""Ring-5 stamper — emits the Defensibility ring at composition time.

Approved signature (stakeholder option (b)):
    stamp(unit, genre_result, source_standing, matrix_loader, solva_depth)
        -> tuple[DefensibilityRing, StampAuditEntry]

DefensibilityRing stays byte-identical to the G0 freeze — we do not
touch the schema. The refusal trace lands in StampAuditEntry, recorded
by the caller via `stamp_audit.record(entry)`. At G2, Northena's ledger
absorbs the audit; the stamper signature does not change.

Cousin substrate:
  * /reference/akki-legacy/backend/services/work_studio/confidence_scorer.py
    — scoring substrate shape.
  * /reference/akki-legacy/backend/services/synisense/engine/signal_derivation.py
    — deterministic-derivation pattern (we LIFT the discipline: the
    output is fully determined by inputs, no LLM in the loop).
"""
from __future__ import annotations

from typing import Tuple

from contracts.five_rings import (
    DefensibilityClass, DefensibilityRing, NormalizedUnit, ScoreVector,
)
from contracts.qualification_matrix.loader import (
    QualificationMatrix, load_qualification_matrix,
)
from services.g1_defensibility.genre_classifier import GenreClassificationResult
from services.g1_defensibility.source_standing_reader import SourceStanding
from services.g1_defensibility.solva_depth.governor import SolvaDepthGovernor
from services.g1_defensibility.stamp_audit import StampAuditEntry

# corroboration + contested_status zero at G1 (Relational ring traversal
# is a G2 deliverable that will backfill these). Forward note: this is
# logged in BUILD_JOURNAL's "G2 swap-in points" list.
_RECENCY_DEFAULT = 0.5  # neutral; declaration baseline doesn't drive recency


def _unknown_genre_ring(unit: NormalizedUnit) -> DefensibilityRing:
    return DefensibilityRing(
        defensibility_class=DefensibilityClass.NON_FACTUAL,
        score_vector=ScoreVector(),
        # When we cannot resolve genre, we still need a matrix_rule_ref
        # (required field). We point at a sentinel "unresolved" rule on
        # v0 — panel_debate.wire_republish is the lowest-ceiling row that
        # exists today; we use it as the fail-closed default.
        matrix_rule_ref="panel_debate.wire_republish@v0",
        runtime_mode="declaration_baseline",
    )


def stamp(
    unit: NormalizedUnit,
    genre_result: GenreClassificationResult,
    source_standing: SourceStanding | None,
    matrix_loader: QualificationMatrix | None = None,
    solva_depth: SolvaDepthGovernor | None = None,
) -> Tuple[DefensibilityRing, StampAuditEntry]:
    matrix = matrix_loader or load_qualification_matrix("v0")
    judge = solva_depth or SolvaDepthGovernor(matrix=matrix)

    # 1) Unknown genre -> non_factual + refuse audit.
    if genre_result.genre == "unknown" or source_standing is None:
        ring = _unknown_genre_ring(unit)
        reason = (
            "genre unresolved against matrix v0"
            if genre_result.genre == "unknown"
            else f"no declared source_standing for {unit.provenance.source_ref!r}"
        )
        audit = StampAuditEntry(
            unit_id=unit.unit_id,
            decision="refuse",
            reason=reason,
            judged_signal_dimensions=judge.judged_dimensions(unit),
            floor_violation=True,
            runtime_mode="declaration_baseline",
        )
        return ring, audit

    # 2) Matrix lookup.
    rule = matrix.find(genre_result.genre, source_standing.value)
    if rule is None:
        # No matrix row for this (genre, source_standing) pair — refuse.
        ring = _unknown_genre_ring(unit)
        audit = StampAuditEntry(
            unit_id=unit.unit_id,
            decision="refuse",
            reason=(
                f"no matrix v0 rule for genre={genre_result.genre!r} "
                f"source_standing={source_standing.value!r}"
            ),
            judged_signal_dimensions=judge.judged_dimensions(unit),
            floor_violation=True,
            runtime_mode="declaration_baseline",
        )
        return ring, audit

    # 3) Build the candidate ring; Solva judges depth.
    candidate = DefensibilityRing(
        defensibility_class=rule.asserts_what,
        score_vector=ScoreVector(
            genre_ceiling=genre_result.confidence,
            source_standing=1.0,  # declared baseline: trust the declaration fully
            corroboration=0.0,    # G2 backfill from Relational ring traversal
            recency=_RECENCY_DEFAULT,
            contested_status=0.0, # G2 backfill
        ),
        matrix_rule_ref=matrix.rule_ref(rule),
        runtime_mode="declaration_baseline",
    )

    decision = judge.judge(unit, candidate)
    if decision.decision == "refuse":
        # Demote to non_factual on Solva refusal.
        ring = DefensibilityRing(
            defensibility_class=DefensibilityClass.NON_FACTUAL,
            score_vector=candidate.score_vector,
            matrix_rule_ref=candidate.matrix_rule_ref,
            runtime_mode="declaration_baseline",
        )
        audit = StampAuditEntry(
            unit_id=unit.unit_id,
            decision="refuse",
            reason=f"solva-depth: {decision.category}: {decision.reason}",
            judged_signal_dimensions=judge.judged_dimensions(unit),
            floor_violation=(decision.category == "floor_violation"),
            runtime_mode="declaration_baseline",
        )
        return ring, audit

    # 4) Accept.
    audit = StampAuditEntry(
        unit_id=unit.unit_id,
        decision="accept",
        reason=None,
        judged_signal_dimensions=judge.judged_dimensions(unit),
        floor_violation=False,
        runtime_mode="declaration_baseline",
    )
    return candidate, audit
