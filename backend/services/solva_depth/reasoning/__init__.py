"""Solva reasoning faculty — the five stages (FREE).

Package layout per G3 phase brief step 3: one file per stage.
Source spec §8 stage NAMES: Frame · Candidate · Tension · Probability · Reflection.

HARD CONSTRAINT: no stage module imports `DefensibilityClass` (the enum
lives in `contracts.five_rings`), no stage function has `-> ConclusionClass`
return annotation, no stage constructs a `DefensibilityClass` value.
Enforced by `test_reasoning_faculty_isolation`.
"""
