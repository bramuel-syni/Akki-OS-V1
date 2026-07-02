# Targeta scope from source — G4 pre-code note

**Source:** `/app/docs/mandates/RMS_Targeta_Specification.md` (SHA-256 `aae06440…89fad`).
**Parent cross-reference:** Product Spec v2.1 §25.
**Freshness:** all 3 required specs CURRENT at G4 Step 0.

## 1. Two-arm architecture (source §3, §6, §7)

Two-layer design: **deterministic eligibility core** + **objective-conditioned yield layer**. Core-only is complete (invariant #2). Yield admitted only through two-arm gate (invariant #6).

Module layout (source §7):
```
services/targeta/
    core.py         # deterministic eligibility + ranking; never imports yield
    yield_layer.py  # learned reorderer; imports ONLY interface types
    interface.py    # the one-way set-preserving boundary (the guard)
    gate.py         # yield admission: Arm 1 helps + Arm 2 veto
    plan.py         # MiningPlan assembly + version stamping
    modes.py        # portfolio / per_run
    contracts/
        targeta_plan.py   # frozen: MiningPlan (schema + snapshot + invariant)
    routers/
        targeta.py        # plan + status API
```

Dependency rules (source §7, enforced by import-assertion tests):
- `core.py` imports Registry read + governing artifact. NEVER imports `yield_layer`, NEVER imports any ML library.
- `yield_layer.py` imports ONLY interface types (`YieldInput`, `Permutation`). Never imports floor, raw measure, or core's eligibility.
- `gate.py` is the ONLY module that compares the two orderings.

## 2. `apply_yield` interface (source §10)

```python
class NonPermutationError(TypeError): ...

def to_yield_input(eligible) -> list[YieldCandidate]:
    return [YieldCandidate(source_ref=c.source_ref,
                           features=safe_features(c),
                           objective_shape=shape_key(c)) for c in eligible]

def apply_yield(eligible, yield_fn) -> list[EligibleCandidate]:
    order = yield_fn(to_yield_input(eligible))
    src = {c.source_ref for c in eligible}
    if len(order) != len(eligible) or set(order) != src:
        raise NonPermutationError('yield output is not a permutation')
    pos = {ref: i for i, ref in enumerate(order)}
    return sorted(eligible, key=lambda c: pos[c.source_ref])
```

Bias hazard: unrepresentable in types (YieldCandidate excludes floor + `registry_defensibility`). This is construction-as-guard, mirroring Solva's `conclusion_class` signature-as-guard.

## 3. Yield-gate thresholds (source §12, §17 open decision)

Owner-owned. Field names for G4 closed seam:
- `min_efficiency_gain` (Arm 1 — Helps): median gain ≥ threshold
- `coverage_alpha` (Arm 2 — Veto): per-class coverage ≥ alpha × core's rate; violation vetoes
- `held_out_set_composition` (governance parameter — held-out configuration is part of decision)

Proposed values (source §17 sign-off table — NOT invention, spec-cited): min_efficiency_gain ≥ 0.15, coverage_alpha = 0.90. **G4 does NOT pick these values.** Closed-seam pattern: `YieldThresholds | None` field on gate; `evaluate_gate(...)` returns `GateResult(admitted=False, helps=False, veto=False, reason='thresholds_not_configured')` when None.

## 4. Data contracts (source §8)

**Core-internal (dataclass, frozen, not Pydantic-frozen):**
- `EligibleCandidate` — carries `registry_defensibility`, `baseline_rank`, `objective_relevance`. NEVER crosses to yield layer.
- `YieldCandidate` — the ONLY thing yield sees. `{source_ref, features, objective_shape}`. Excludes floor + raw measure by construction.
- `YieldInput = Sequence[YieldCandidate]`
- `Permutation = Sequence[str]` (ordering of source_refs)

**Frozen contract (Pydantic + snapshot + invariant):**
- `MiningPlan` (source §8):
  ```python
  {
    plan_id: str,
    mode: Literal['portfolio', 'per_run'],
    governing_artifact_ref: ArtifactRef,
    registry_snapshot_ref: str,
    ordered_targets: Sequence[TargetLocation],
    defensibility_floor: FloorSpec,           # carried through to Layer A
    core_baseline_ranking: Sequence[str],     # for attribution / audit
    yield_layer_version: str,                  # or 'core-only'
    generated_at: str,
  }
  ```

CONFIRM check (source §8): "FloorSpec + TargetLocation against five_rings@v0, objective_request@v0, and the Registry contract."
- `FloorSpec` — already at `services/solva_depth/interfaces.py::FloorSpec` (G3-authored, frozen dataclass around `DefensibilityFloor`). Reuse verbatim; Targeta imports from Solva sibling.
- `TargetLocation` — NEW at G4: `{source_ref: str, region: str, defensibility_floor: FloorSpec}`. No mutation of any existing contract.
- `ArtifactRef` — already at `contracts/northena_ledger.py::LedgerArtifactRef` (G2a). Reuse.
- `registry_snapshot_ref` — string reference to a Registry snapshot id (Mtafiti-owned).

**Contract mutation demands: NONE.** HAZARD-STOP (a) NOT RAISED.

**New frozen contracts to author at G4:**
1. `MiningPlan` (Pydantic + snapshot + invariant at `tests/invariants/targeta_mining_plan.contract_snapshot.json`).
2. `TargetLocation` (Pydantic sub-model of MiningPlan).

## 5. Core arm completeness (source §14 construction requirement #1, §17 invariant #2)

**Source §14 verbatim**: "Build the deterministic eligibility core, the interface, the plan contract, and the two modes; **the core is a complete targeter and the fallback the yield layer degrades to.**"

**Source §17 #2 verbatim**: "The deterministic eligibility core never learns — no model, no adaptive weight; ranking fixed and inspectable. **Targeta on the core alone is complete and correct.**"

G4 ships core LIVE; yield DARK via closed-seam gate. Composition (gate) equals core output when yield closed.

## 6. Integration with Mtafiti Registry (source §14 interfaces)

Registry → core: reads `{source_ref, region, sensitivity, defensibility_measure, freshness}` per source. Reads `defensibility_runtime_mode` to know whether measure came from baseline-only or overlay.

Registry is objective-blind (Mtafiti §17 invariant #9). Targeta CONSULTS but never MUTATES. Read-only handle pattern (per G3 Solva `MatrixHandle` Protocol convention).

## 7. Seven invariants (source §17)

| # | Invariant | Landing at G4 | Test |
|---|---|---|---|
| 1 | Plans order of extraction; does not extract or govern | `core.py` + `plan.py` produce MiningPlan; NEVER invoke Akki layers | structural |
| 2 | Core never learns; complete and correct alone | `test_core_has_no_ml_import` grep-guard | `test_targeta_core_complete_alone` |
| 3 | Yield receives only YieldInput; returns Permutation | `apply_yield` type-checks; NonPermutationError raised | `test_yield_output_is_permutation` |
| 4 | Floor applied by core alone; yield never sees floor | `YieldCandidate` has no floor field | `test_yield_never_sees_floor` |
| 5 | Learning improves order only; never changes eligibility | apply_yield validates set-equal | `test_floor_is_hard_filter` |
| 6 | Yield admitted only through two-arm gate | `evaluate_gate` returns `admitted` compound | `test_coverage_veto_overrides_helps` |
| 7 | On gate failure → core ordering; never blocked | plan.py stamps `yield_layer_version='core-only'` | `test_fallback_to_core` |
| 8 | Plan reproducible for same inputs | plan_id derived from inputs deterministically | `test_plan_reproducible` |
| 9 | Never widens scope / lowers floor | no floor-mutation code path exists | (structural — no setter) |

## 8. Contract-mutation hazard check

Reviewed all six frozen contracts + G3-authored dataclasses:
- `objective_request@v0`: consumed for `DefensibilityFloor`. Read-only.
- `qualification_matrix@v0`: not touched.
- G3 `FloorSpec` (frozen dataclass): reused verbatim.
- `LedgerArtifactRef`: reused for `governing_artifact_ref`.

**Contract-mutation demands: NONE.** **HAZARD-STOP (a) NOT RAISED.**

## Ready-to-code checklist

- [x] Source §-anchors mapped
- [x] All 2 new frozen contracts (MiningPlan, TargetLocation) identified as ADDITIONS
- [x] Yield threshold field names identified (`min_efficiency_gain`, `coverage_alpha`, `held_out_set_composition`)
- [x] Closed-seam pattern applies to yield gate
- [x] `apply_yield` type-boundary faithful to source §10
- [x] Core-only completeness spec-cited (§14 + §17)
- [x] 9 invariants mapped to tests
