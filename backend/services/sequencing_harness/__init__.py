"""G-13 · Sequencing harness (execution) · fresh authoring from Registry Doctrine §5.2 + §8.1(b).

Owner ruling `docs/rulings/g_13_e1_e2_e3_2026_07_25.md` verbatim on §5.5:
    "Class E defaults N=10 and α=0.05 approved as pinned values on
    sequencing-harness-v0; both are textbook Class E and neither shows a
    promotion trigger. No early E→O promotions."

Registry Doctrine §5.2 verbatim (line 119):
    "Specification (enters as code only on Owner dispatch): a harness that
    executes registered functions against fixture traffic in candidate
    orderings and measures real cost — not simulated approximations.
    Principle: this system is predominantly deterministic; you do not
    simulate a deterministic gate, you run it. Orderings are optimized
    over the Registry's cost and dependency fields: cheap gates before
    expensive, deterministic rungs before model rungs, independent
    functions in parallel, fail-fast paths surfaced. Honest boundary,
    stated as a spec constraint: rung-3/rung-4 behavior is measured
    statistically (repeated runs over the harness, route-level
    comparisons), never claimed as exact. Output: the measured best path
    of integration and sequencing per journey — replacing sequencing
    judgment with sequencing measurement, and back-filling every
    'unknown' cost field in the Registry."

FRESH AUTHORING DISCIPLINE: zero content lifted from held D7 file
`docs/stage_a_proposals/sequencing_harness_stage_a.md` per STEP-2
Surfaces ruling Surface 2 (a) verbatim.
"""

# Class E pinned parameters per Owner ruling · sequencing-harness-v0.
ENGINE_VERSION: str = "sequencing-harness-v0"

REPETITION_COUNT: int = 10  # N=10 rung-3/rung-4 statistical repetitions.
SIGNIFICANCE_ALPHA: float = 0.05  # α=0.05 route-level comparison threshold.
