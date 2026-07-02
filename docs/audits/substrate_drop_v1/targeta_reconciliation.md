# Targeta Reconciliation — Substrate-Drop v1

**Canonical source:** `/app/docs/mandates/RMS_Targeta_Specification.md` (SHA-256 in `MANIFEST.md`).
**Cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §25.
**Reconciled artifact:** `/app/docs/g4_prep/targeta_prep.md`.

**Discipline:** source wins; sketch corrects to source; no shipped Targeta code exists.

## 1. Two-layer design (spec §3)

**Verdict: MATCH.** Prep §3 + §4 correctly describes deterministic eligibility core + objective-conditioned yield layer with one-way relationship.

## 2. Eligibility guard (spec §4 + §10)

**Verdict: MATCH.** Prep §6 asserts yield-layer returns a permutation; non-permutation = type error. Aligned with spec §10 `apply_yield`.

## 3. Module layout (spec §7)

Spec §7:
```
services/targeta/
  core.py               # deterministic eligibility + ranking
  yield_layer.py        # learned reorderer; interface types only
  interface.py          # one-way set-preserving boundary (the guard)
  gate.py               # two-arm admission gate
  plan.py               # MiningPlan assembly + version stamping
  modes.py              # portfolio / per-run orchestration
contracts/
  targeta_plan.py       # frozen: MiningPlan
routers/
  targeta.py            # plan + status API
```

Prep §7 previously listed: `core.py, yield_layer.py, gate.py, eligibility.py, matrix_handle.py (was Mtafiti — actually irrelevant to Targeta)`. Missing: `interface.py, plan.py, modes.py`.

**Verdict: SKETCH_CORRECTION.** Sketch updated to spec §7 layout. `services/targeta/eligibility.py` proposal removed (spec §9 puts eligibility inside `core.py`). Added `interface.py, plan.py, modes.py`.

## 4. Data contracts (spec §8)

Spec §8 declares four types:
- `EligibleCandidate` (core-internal, frozen dataclass — carries raw measure)
- `YieldCandidate` (crosses to yield layer, stripped — carries only source_ref, features, objective_shape)
- `YieldInput = Sequence[YieldCandidate]`
- `Permutation = Sequence[str]`

Plus the frozen `MiningPlan` in `contracts/targeta_plan.py`.

Prep §5 previously mentioned `contracts/mining_plan.py` (wrong filename per spec §7) and `contracts/eligible_candidate.py` (spec §8 keeps EligibleCandidate as an internal frozen dataclass, not a contract-grade artifact).

**Verdict: SKETCH_CORRECTION.** Filename `contracts/mining_plan.py` → `contracts/targeta_plan.py`. `contracts/eligible_candidate.py` proposal deleted (spec §8 keeps it in-module).

## 5. Two-arm admission gate (spec §5 + §12)

Spec §5 names the arms:
- **Arm 1 — Helps.** Yield ordering reaches objective-satisfaction in fewer mined units than the core.
- **Arm 2 — Coverage veto.** Yield layer must not drive any eligible class's mining rate below the core's.

Prep §4 previously used "Arm 1 — Efficiency". 

**Verdict: SKETCH_CORRECTION.** Prep updated: "Arm 1 — Efficiency" → "Arm 1 — Helps" (spec verbatim).

## 6. Invariants (spec §16 — 9 invariants)

Spec §16 lists **9 binding invariants**. Prep §6 lists 5 items informally.

**Verdict: SKETCH_CORRECTION.** Sketch §6 rewritten to reflect all 9:

| # | Spec text (abbrev.) | G4 landing shape |
|---|---|---|
| 1 | Targeta plans order; does not extract or govern | Module structure + N-INV-analog grep-guards |
| 2 | Core never learns — no model, no adaptive weight | `test_core_has_no_ml_import` |
| 3 | Yield layer may only reorder the eligible set; non-permutation = type error | `interface.py::apply_yield` raises `NonPermutationError` |
| 4 | Floor applied by core alone as hard filter; yield never receives floor | `YieldCandidate` shape has no floor field |
| 5 | Learning improves order; never changes eligibility | Bias hazard denied by construction (§10 guard) |
| 6 | Yield admitted only through two-arm gate; Arm 2 veto | `gate.py::evaluate_gate` |
| 7 | On gate failure, Targeta runs on the core (never blocked) | `plan.py` fallback + `yield_layer_version = 'core-only'` stamp |
| 8 | Every plan reproducible for (Registry state, artifact, version) | `test_plan_reproducible` |
| 9 | Never widens scope or lowers floor; boundary is SyniSense, run governance Northena | Import assertions + orthogonality guard |

## 7. Test obligations (spec §13 — 7 tests)

**Verdict: SKETCH_CORRECTION.** Sketch §6 test list expanded from 5 to 7:
1. `test_yield_output_is_permutation`
2. `test_yield_never_sees_floor`
3. `test_floor_is_hard_filter`
4. `test_fallback_to_core`
5. `test_coverage_veto_overrides_helps`
6. `test_plan_reproducible`
7. `test_core_has_no_ml_import`

## 8. Product Spec 2.1 cross-reference

- §25 (Targeta parent behavioural description) — MATCH.
- §31 invariant #4 ("Targeta's learning walled from eligibility") — MATCH.
- §32 (open governance): yield-gate thresholds owned by project owner. MATCH `OPEN_GOVERNANCE.md`.

## 9. Governance (spec §17)

Spec §17: one open decision — yield-gate thresholds (`min_efficiency_gain`, `coverage_alpha`, held-out set composition). Owner: project owner. Proposals in §17 for sign-off (0.15, 0.90). Blocks yield-layer admission only; core ships without them.

**Verdict: MATCH.** `OPEN_GOVERNANCE.md` §2 lists these items with proposals in brackets, marked "DO NOT act on".

---

## CODE_IMPACT items

**none.** No shipped Targeta code exists.

## Corrections applied to `docs/g4_prep/targeta_prep.md`

1. §7 module layout: added `interface.py, plan.py, modes.py`; removed `eligibility.py`.
2. §5: `contracts/mining_plan.py` → `contracts/targeta_plan.py`; removed `contracts/eligible_candidate.py` (per spec §8 keep in-module).
3. §4: "Arm 1 — Efficiency" → "Arm 1 — Helps" (spec verbatim).
4. §6: expanded invariants list from 5 items to full 9 per spec §16.
5. §6: added 7 test obligations from spec §13.
6. §7 (Rule 2 substrate expectation): removed `services/targeta/eligibility.py` row; added rows for `interface.py, plan.py, modes.py`.

## Summary

- **MATCH: 4** (two-layer design, eligibility guard, product spec cross-ref, governance).
- **SKETCH_CORRECTION: 6** (module layout, data contracts, gate arm naming, invariants list, test obligations, contract filenames).
- **CODE_IMPACT: 0.**
- **HAZARD-STOP (a) raised: NO.**

**Verdict:** Targeta prep sketch corrected in-place. Ready for G4 dispatch when governance items 2 (owner) resolve.
