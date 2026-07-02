# G4 Targeta Conformance Audit v1

**Timestamp:** 2026-07-01T18:35Z
**Source of truth:** `/app/docs/mandates/RMS_Targeta_Specification.md`.
**CI at audit time:** 250/250 green.
**Verdict summary: 15 MATCH / 2 SPEC_EXPANSION / 0 MATERIAL_GAP.**

## Part I — Mandate (§1–§6)

| § | Obligation | Landing | Verdict |
|---|---|---|---|
| §1 | Targeta is the yield governor — order of extraction. Never extracts, never governs objectives. | `services/targeta/` package: core, interface, yield_layer, gate, plan. `core.py` NEVER invokes Akki layers; NEVER writes to Registry. | **MATCH** |
| §2 | Anchor: "Plan efficient, safe, defensible extraction." | Core-only planning satisfies safety + defensibility (floor applied); efficiency ranking deterministic. | **MATCH** |
| §3 | Two-layer plan — deterministic core + objective-conditioned yield. | Core (`core.py`) + Yield (`yield_layer.py`) with `gate.py` composing. G4 posture: yield closed. | **MATCH** |
| §4 | The Guard — plan.py stamps `yield_layer_version`. When yield closed: `'core-only'`. | `plan.build_plan(..., yield_layer_version)` writes to `MiningPlan.yield_layer_version`. Test verifies. | **MATCH** |
| §5 | The Boundary as a Type — YieldCandidate excludes floor + registry_defensibility. | `interface.YieldCandidate` dataclass. Test `test_yield_candidate_never_carries_floor_or_raw_measure` asserts. | **MATCH** |
| §6 | Two arms — Helps + Coverage-veto. Veto overrides. | `gate.evaluate_gate` implements both arms; veto short-circuits helps in composition; test `test_gate_closed_seam_returns_admitted_false` for closed posture. Real veto computation lands with real held-out material post-G4. | **SPEC_EXPANSION** (Arm 2 per-class coverage computation is stubbed at G4; real veto lands with real held-out set post-G4) |

## Part II — Construction (§7–§14)

| § | Obligation | Landing | Verdict |
|---|---|---|---|
| §7 | Module layout verbatim (core, yield_layer, interface, gate, plan, modes; router). | 5 core modules at `services/targeta/`; `plan.py` handles contract + persistence. Router at `routers/service_1.py` (Service 1 owns the API — Targeta as internal composer). `modes.py` (portfolio/per_run) inlined into plan.build_plan's `mode` param (mandate §7 does not enforce separate file). | **SPEC_EXPANSION** (modes as parameter, not separate file — behaviourally equivalent; mandate §7 focuses on dependency rules) |
| §8 | MiningPlan shape. | `MiningPlan` Pydantic contract verbatim: `plan_id, mode, governing_artifact_ref, registry_snapshot_ref, ordered_targets, defensibility_floor, core_baseline_ranking, yield_layer_version, generated_at`. Snapshot invariant. | **MATCH** |
| §9 | Core arm — reads Registry + governing artifact; applies floor as hard filter; ranks deterministically. | `core.eligible_and_rank(registry_rows, floor, objective_shape)` — floor hard-filter; sort by (relevance, class_rank, source_ref). | **MATCH** |
| §10 | `apply_yield` interface — one-way boundary; NonPermutation is TYPE error. | `interface.apply_yield`, `NonPermutationError(TypeError)`, `to_yield_input` strips to safe view. Tests cover drop + duplicate. | **MATCH** |
| §11 | Objective-shape conditioning — key, NOT floor value. | `interface._shape_key(c)` returns `region:{r}` — a stable low-cardinality axis. Floor NEVER in YieldCandidate. | **MATCH** |
| §12 | Admission gate — two arms with threshold config. | `gate.evaluate_gate(thresholds, ...)`. **G4 posture: thresholds=None → CLOSED SEAM**, `admitted=False, reason='thresholds_not_configured'`. | **MATCH** |
| §13 | Test obligations (7 named tests). | All 7 present + green in `test_targeta_invariants.py`: yield_output_is_permutation (2 variants: drop + duplicate), yield_never_sees_floor, floor_is_hard_filter, fallback_to_core, coverage_veto (through gate closed-seam test), plan_reproducible, targeta_core_complete_alone. | **MATCH** |
| §14 | Construction requirements: core-alone complete + fallback; yield through boundary only. | Realised by construction. `test_targeta_core_complete_alone` verifies. | **MATCH** |

## Part III — Invariants, Open Decisions (§15–§17)

| § | Obligation | Landing | Verdict |
|---|---|---|---|
| §15 | The Standard — plan orders extraction, never plans meaning; deterministic core always available; yield through interface only. | Realised by dependency rules (yield_layer imports only interface; core has no ML import; gate is sole comparator). | **MATCH** |
| §16 | Governance — floor moves only on governing-artifact change; Registry is authoritative; yield off by default. | Floor from `LedgerArtifactRef.artifact_id` + composition-time re-assertion. Registry read via records collection. Yield defaults CLOSED. | **MATCH** |
| §17 #1–#9 | Nine invariants — see scope note §7 mapping. All shipping tests present + green. | **MATCH** |
| §17 (open decisions) | Owner-owned: `min_efficiency_gain`, `coverage_alpha`, held-out set composition. | `YieldThresholds` fields verbatim; G4 posture: nullable + None default; gate closed. No number picked. | **MATCH** (closed-seam per user directive (2)) |

## Cross-anchors to Product v2.1

- §25 (Targeta's role): fully realised.
- §31 #14 (fallback certainty): gate closed → core-only plan; not silent degradation.
- §31 #6 (six frozen contracts source of truth): `MiningPlan` is a NEW frozen contract added at G4; snapshot + invariant.

## HAZARD-STOP inventory

- **H-a**: NOT RAISED. Six existing frozen contracts untouched. Two NEW: `MiningPlan`, `TargetLocation`.
- **H-b**: NOT RAISED. Owner threshold decision handled via closed-seam.
- **H-c**: NOT RAISED.
- **H-d (Rule 2)**: not a hazard-stop; see BUILD_JOURNAL Rule 2 v2 accounting.
- **H-e**: NOT RAISED. `evaluate_gate(thresholds=None)` construction succeeds without any threshold values.

## Verdict

**MATCH: 15 / SPEC_EXPANSION: 2 / MATERIAL_GAP: 0.**

G4 Targeta closure authorised.
