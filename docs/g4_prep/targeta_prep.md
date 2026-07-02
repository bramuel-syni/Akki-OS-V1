# Targeta G4 prep — read-only sketch

**Source:** `/app/docs/mandates/RMS_Targeta_Specification.md` (SHA-256 in `/app/docs/mandates/MANIFEST.md`). **Read now, act at G4.** No code written this pass.
**Parent cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §25.
**Reconciliation:** `/app/docs/audits/substrate_drop_v1/targeta_reconciliation.md` (Substrate-Drop v1, 2026-07-01).

## 1. Purpose (G4 role)

Targeting engine that plans the order of mining/extraction for Akki Retrieval. Two modes:

- **Portfolio (Day Zero)** — ranks the whole estate against the Portfolio Mandate to select strata for seeding.
- **Per-run (Day-to-Day)** — ranks sources for one Objective Request under a `defensibility_floor`.

## 2. Inputs (from services G4 must have)

- **Registry** — from Mtafiti (source estate + sensitivity + defensibility measures). CONFIRM at G4.
- **Governing artifacts** — Portfolio Mandate (portfolio mode) OR `ObjectiveRequest` w/ `defensibility_floor` (per-run mode).
- **Mining history** — for yield-layer training; admitted only after gate validation.

## 3. Deterministic eligibility CORE (stands alone at G4; spec §3 + §9)

- Inspectable, versioned function.
- Applies `defensibility_floor` as HARD immutable filter.
- Ranking is a fixed function of `objective_relevance` + `registry_defensibility`. No ML, no learned weights.
- **Correct alone**: mandatory fallback if yield-layer fails/is absent.
- Frozen contracts: `MiningPlan` (snapshot + invariant), `TargetLocation` (Akki Retrieval locator shape).
- `EligibleCandidate` remains a core-internal frozen dataclass (spec §8) — carries the raw `registry_defensibility` measure. **Never** crosses to the yield layer.

## 4. Objective-conditioned yield-layer (gated on owner-signed thresholds; spec §4 + §11)

- Learns to refine mining order *within* the core's already-cleared eligible set.
- Sees ONLY `YieldCandidate` (spec §8): `source_ref, features (opaque), objective_shape`. **Cannot** access floor values, raw defensibility metrics, or eligibility logic. Structural boundary — the guarded values are absent from what it receives.
- Returns `Permutation = Sequence[str]` — an ordering of source_refs, nothing more.
- **Two-arm admission gate** at `services/targeta/gate.py` (spec §5 + §12):
  - **Arm 1 — Helps** (spec verbatim): on held-out past objectives, yield ordering reaches objective-satisfaction in fewer mined units than the core. Threshold: `min_efficiency_gain` (**PENDING owner sign-off**).
  - **Arm 2 — Coverage veto**: yield layer must NOT drive mining rate of any eligible class below `coverage_alpha` × core rate. Veto overrides efficiency. Threshold: `coverage_alpha` (**PENDING owner sign-off**).
- Fallback: if gate fails, plan reverts to core ordering (core is never blocked). Plan stamped `yield_layer_version = 'core-only'`.

## 5. Data contracts (spec §8)

Four types carry Targeta's data:

- `EligibleCandidate` — **core-internal, frozen dataclass** (in-module; not contract-grade). Carries `source_ref, region, objective_relevance, registry_defensibility, baseline_rank`.
- `YieldCandidate` — **the only type the yield layer sees**. Carries `source_ref, features, objective_shape` — excludes floor + raw measure by construction.
- `YieldInput = Sequence[YieldCandidate]`
- `Permutation = Sequence[str]`

Frozen contract:

- **`contracts/targeta_plan.py`** — `MiningPlan(plan_id, mode, governing_artifact_ref, registry_snapshot_ref, ordered_targets, defensibility_floor, core_baseline_ranking, yield_layer_version, generated_at)`. Snapshot + invariant at freeze time. Sub-shapes `FloorSpec` + `TargetLocation`: CONFIRM against `five_rings@v0`, `objective_request@v0`, Registry contract.

## 6. Nine binding invariants (spec §16)

Spec §16 lists **9 binding invariants**.

| # | Invariant | G4 landing shape |
|---|---|---|
| 1 | Targeta plans the order of extraction; does not extract, does not govern | Module structure + import assertions |
| 2 | Deterministic eligibility core never learns — no model, no adaptive weight; ranking fixed + inspectable; core alone is complete + correct | `test_core_has_no_ml_import` (import assertion) |
| 3 | Yield layer may only reorder the eligible set the core cleared; non-permutation is a type error | `interface.py::apply_yield` raises `NonPermutationError` |
| 4 | Defensibility floor applied by core alone as hard filter; yield never receives floor | `YieldCandidate` shape has no floor field (spec §8); `test_yield_never_sees_floor` |
| 5 | Learning may improve order; may never change what is eligible; bias hazard denied by construction | Structural (§10) — apply_yield validates set-equal input/output |
| 6 | Yield admitted only through two-arm gate; Arm 2 (coverage) is a veto that overrides Arm 1 (helps) | `gate.py::evaluate_gate` returns `admitted=(helps and not veto)` |
| 7 | On gate failure, Targeta runs on the deterministic core; core never blocked by yield layer's failure | `plan.py` fallback path + `yield_layer_version = 'core-only'` stamp |
| 8 | Every plan is reproducible for a given Registry state, artifact, and yield-layer version; records that version | `test_plan_reproducible` |
| 9 | Targeta never widens scope or lowers floor; boundary is SyniSense, run governance is Northena | Orthogonality grep-guard (analogue of N-INV-11) |

## 7. Test obligations (spec §13 — 7 tests)

At G4 dispatch, land all 7 spec-named tests:

1. `test_yield_output_is_permutation` — yield fn returning a dropped/added/duplicated member raises `NonPermutationError`; no plan is built from it.
2. `test_yield_never_sees_floor` — `YieldCandidate` has no floor and no raw-measure field; `to_yield_input` carries neither.
3. `test_floor_is_hard_filter` — a source below the floor never appears in the eligible set, regardless of yield ordering.
4. `test_fallback_to_core` — gate failure (either arm) → plan uses core ordering; `yield_layer_version == 'core-only'`.
5. `test_coverage_veto_overrides_helps` — a yield fn that improves efficiency but starves a class is not admitted.
6. `test_plan_reproducible` — same Registry state + artifact + yield-layer version → byte-identical plan.
7. `test_core_has_no_ml_import` — `core.py` imports no ML library (import assertion).

## 8. G4 module layout (spec §7 — canonical, per Substrate-Drop v1)

**Substrate state as of 2026-07-01 (grep result):** no existing Targeta-adjacent cousin in-pod. `/reference/akki-legacy/` remains architecturally unreachable (settled substrate directive norm #8). Every G4 Targeta module will land `mandate-forced-net-new` or `transitive` via existing in-pod intermediates.

Spec §7 canonical layout:

```
services/targeta/
  core.py              # deterministic eligibility + ranking; never imports yield
  yield_layer.py       # learned reorderer; imports ONLY interface types
  interface.py         # the one-way set-preserving boundary (the guard)
  gate.py              # two-arm admission gate (Arm 1 Helps, Arm 2 Coverage veto)
  plan.py              # MiningPlan assembly + version stamping
  modes.py             # portfolio / per-run orchestration
contracts/
  targeta_plan.py      # frozen: MiningPlan
routers/
  targeta.py           # plan + status API
```

Lift manifest expectation per module:

| Module | Expected `lift_kind` | Cousin / chain candidate |
|---|---|---|
| `services/targeta/core.py` | `mandate-forced-net-new` | Spec §3 + §9 (deterministic core) declares net-new by name |
| `services/targeta/yield_layer.py` | `mandate-forced-net-new` | Spec §11 declares learned layer net-new |
| `services/targeta/interface.py` | `mandate-forced-net-new` | Spec §10 declares one-way set-preserving guard net-new; type-error-on-non-permutation is the guard |
| `services/targeta/gate.py` | `transitive` | via `services/synisense/shield/purpose_validator.py` (allow-list + two-arm structured refusal shape) |
| `services/targeta/plan.py` | `mandate-forced-net-new` | Spec §7 declares assembly + version stamping net-new |
| `services/targeta/modes.py` | `mandate-forced-net-new` | Spec §7 + §6 (two-mode orchestration) declares net-new |
| `contracts/targeta_plan.py` | `mandate-forced-net-new` | Spec §8 forces contract shape; freeze-discipline reused from `northena_ledger.py` |
| `routers/targeta.py` | `transitive` | via `routers/contracts.py` + `routers/northena.py` |

**Expected Rule 2**: overall net-new likely > lifted (like G2a's mandate-forced state machine). Discretionary should stay ≤ 2× lifted.

## 9. Pending governance items (see `docs/g4_prep/OPEN_GOVERNANCE.md`)

Spec §17 declares one open decision — yield-gate thresholds — with proposed values for sign-off:

- `min_efficiency_gain` (Arm 1 — Helps) — proposed: median ≥ 0.15 reduction in mined units, no objective worsened beyond a small tolerance.
- `coverage_alpha` (Arm 2 — Coverage veto) — proposed: 0.90.
- **Held-out set composition** — representative across objective shapes, floors, estate classes; sized so per-class coverage is measurable.

**All PENDING owner sign-off.** Blocks yield-layer admission only; deterministic core ships and runs without them.

CONFIRM markers throughout spec — resolve at G4 against actual Registry / locator shapes / storage substrate.
