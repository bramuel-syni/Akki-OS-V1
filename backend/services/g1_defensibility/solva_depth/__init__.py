"""Solva depth-governor reshape v1 — ported substrate vs net-new.

LIFT vs RESHAPE ledger (Rule 2 visibility, journaled in BUILD_JOURNAL):

  LIFTED FROM COUSIN (shape only, content net-new):
    * /reference/akki-legacy/backend/services/solva_v2/engines/refusal.py
      — structured-refusal-result discipline. We port the dataclass
        shape (decision/category/confidence/reason). The corporate-
        governance refusal categories DO NOT port.
    * /reference/akki-legacy/backend/services/solva_v2/integrity_validators.py
      — ValidatorOffender + ValidationResult shape, per-check function
        list pattern. We port the discipline of returning structured
        offenders, not booleans. Content (citation_lint, calibration,
        etc.) DOES NOT port — those are session-shaped, ours is
        unit-shaped.

  NET-NEW (no cousin equivalent):
    * Catalogue validator: signal dimensions ⊆ SIGNAL_RING_DIMENSIONS_V0.
    * Matrix-ceiling validator: proposed defensibility_class respects
      the Qualification Matrix row's ceiling.
    * Governor composition: single-call judge over (unit, proposed_ring).

  DELIBERATELY NOT PORTED (Rule 2 watch):
    * solva_v2/state_machine.py — session orchestrator. Solva is no
      longer session-shaped at G1.
    * engines/{frame_audit, candidate_generation, probability_weighting,
      reflection, tension_detector}.py — LLM-driven session reasoning.
      G1's Solva is a deterministic depth judge over a unit. If a future
      revisit needs any of these, that's Rule 2 territory — STOP and
      surface.
"""
