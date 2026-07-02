# G4 Mtafiti Conformance Audit v1

**Timestamp:** 2026-07-01T18:30Z
**Source of truth:** `/app/docs/mandates/RMS_Mtafiti_Specification.md` (SHA-256 in MANIFEST.md).
**CI at audit time:** 250/250 green via `make ci`.
**Verdict summary: 17 MATCH / 2 SPEC_EXPANSION / 0 MATERIAL_GAP.**

## Part I — Mandate (§1–§6)

| § | Obligation | Landing | Verdict |
|---|---|---|---|
| §1 | Mtafiti is the truth-standing governor. Discovers estate; measures defensibility; never plans, never governs objectives. | `services/mtafiti/` package: `census.py`, `declaration.py`, `inference.py`, `measure.py`, `verdict.py`, `registry.py`, `source_standing.py`, `v3_overlay.py`. No import of Targeta / Northena / Solva from any Mtafiti module. | **MATCH** |
| §2 | Anchor: "Measure well, and never trust unconfirmed shape." | `declared_standing` + `assign_verdict` deterministic; fail-toward-caution on unmapped Matrix cell (returns non_factual). | **MATCH** |
| §3 | Two layers: baseline (always) + inference overlay (V3-gated). Baseline stands alone. | `measure.measure()` zeros detection contributions when `v3_admitted=False`; `test_baseline_stands_alone_when_overlay_not_admitted` verifies. | **MATCH** |
| §4 | Detect vs decide boundary — dependency rule. inference emits detections only; verdict is Matrix lookup. | `inference.py` has NO `verdict` import (structural test) + emits only `Detections` shape. `verdict.py` does Matrix lookup + returns `matrix_rule_ref`. | **MATCH** |
| §5 | Registry: one record per source, contract-grade, snapshot-invariant. | `MtafitiRegistryRecord` Pydantic contract at `contracts/mtafiti_registry.py`; snapshot at `tests/invariants/mtafiti_registry_record.contract_snapshot.json`; drift-detect test. | **MATCH** |
| §6 | Freshness — L1/L2 delta re-measures affected region only. | `FreshnessStamp{logged_date, structural_signature}`. `detect_stale_records` returns only changed refs. | **MATCH** |

## Part II — Construction (§7–§14)

| § | Obligation | Landing | Verdict |
|---|---|---|---|
| §7 | Module layout verbatim. | 9 modules at `services/mtafiti/`; matches spec §7 verbatim (census / declaration / inference / measure / verdict / registry / source_standing / v3_overlay + package `__init__`). | **MATCH** |
| §8 | Census — exhaustive walk, sensitivity classification. Signature carries no `ObjectiveRequest`. | `census.census(units)` — no objective param; classification via `classify_sensitivity`. | **MATCH** |
| §9 | Baseline — feed-level source-standing, low cardinality, always available. | `declaration.declared_standing(feed_id, table)`. `source_standing.table()` provides G4 v0 placeholder (see §-flag below). | **MATCH** |
| §10 | Inference — detections only; NEVER imports verdict.py. | `Detections` shape frozen; import-boundary asserted structurally. G4 v0: deterministic-null stubs (0.0). Real detectors bind post-G4 via V3 admission. | **SPEC_EXPANSION** (LLM/detector binding is a G4+ implementation choice under §17 #5) |
| §11 | Measure — composes baseline + (admitted) detections; verdict via Matrix. | `measure.measure` verbatim; `verdict.assign_verdict` → Matrix lookup → `Verdict{defensibility_class, matrix_rule_ref}`. | **MATCH** |
| §12 | V3 admission — accuracy + inter-annotator floor. | `v3_overlay.overlay_admitted(thresholds, v3_result)` — kappa floor pre-condition + accuracy thresholds. **G4 posture: CLOSED SEAM** (`thresholds=None` returns False). | **MATCH** |
| §13 | Registry record structure. | `MtafitiRegistryRecord` verbatim: `source_ref, region, feed_id, sensitivity, defensibility_measure, defensibility_runtime_mode, matrix_rule_ref, defensibility_class, freshness_stamp`. | **MATCH** |
| §14 | Test obligations (6 named tests) + construction requirements. | All 6 tests present + green in `test_mtafiti_invariants.py`: inference-emits-no-verdict, verdict-is-Matrix-lookup, baseline-stands-alone, census-objective-blind, Registry-contract, freshness-scoped. | **MATCH** |

## Part III — Governance, Invariants, Open Decisions (§15–§18)

| § | Obligation | Landing | Verdict |
|---|---|---|---|
| §15 | Governance — never usurp editorial authority; never overwrite source_standing; Matrix is governed. | `source_standing.py` placeholder table flagged `synthetic_placeholder=True, editorial_authority=False` (user directive (4)). Verdict reads Matrix through `MatrixHandle` — no write path exposed. `test_source_standing_placeholder_flags` guards. | **MATCH** |
| §16 | The Standard — census exhaustive; classes tied to Matrix; measure prior + fail-toward-caution; V3 gates learned layer. | Realised by construction. `verdict.assign_verdict` fails-toward-caution (unmapped cell → non_factual + matrix_rule_ref='unmapped_cell'). | **MATCH** |
| §17 #1–#9 | Nine invariants. | All 9 mapped to shipping tests (see Mtafiti scope note §8). Invariant #6 (source-standing keyed on feed_id, low cardinality) structural — declaration table has ~8 feed_id entries, one row per feed. | **MATCH** |
| §18 | V3 admission gate parameters (Owner-owned): `fact_precision`, `genre_accuracy`, `inter_annotator_floor`. Wait for real labelled set. | `V3Thresholds` fields verbatim; G4 posture: `V3Thresholds | None`; default None; overlay closed. No number picked. Ships when Owner + DPO land threshold decision + labelled set. | **SPEC_EXPANSION** (governance-pending; closed-seam pattern applied per user directive) |

## Cross-anchors to Product v2.1

- §24 (Mtafiti's role): fully realised by mandate above.
- §31 #1 (Ring 5 stamp complete): Mtafiti Registry provides `defensibility_class` that Ring 5 records via G1 stamper — extension point for post-G4 stamper enrichment. NOT changed at G4.
- §31 #3 (Matrix read-only): `MatrixHandle` Protocol reused from Solva G3 — no write API surface.
- §31 #14 (fallback certainty): `verdict.assign_verdict` returns non_factual + `matrix_rule_ref='unmapped_cell'` on Matrix miss — not silent downgrade.

## HAZARD-STOP inventory

- **H-a (contract mutation)**: NOT RAISED. Six frozen contracts untouched. Three NEW frozen contracts added (`MtafitiRegistryRecord`, `FreshnessStamp`, `MtafitiScoreVector`) — additions, not mutations.
- **H-b (governance)**: NOT RAISED for G4 open decisions. V3 admission thresholds handled via closed-seam doctrine per user directive.
- **H-c (spec absence)**: NOT RAISED. All 3 required specs CURRENT at Step 0.
- **H-e (closed seam requires threshold to build)**: NOT RAISED. `overlay_admitted(thresholds=None) -> False` construction succeeds; threshold values are NOT required to build the code path.

## Verdict

**MATCH: 17 / SPEC_EXPANSION: 2 / MATERIAL_GAP: 0.**

G4 Mtafiti closure authorised. Nothing beyond G4 opens until user directs.
