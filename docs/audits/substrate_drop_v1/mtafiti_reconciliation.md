# Mtafiti Reconciliation — Substrate-Drop v1

**Canonical source:** `/app/docs/mandates/RMS_Mtafiti_Specification.md` (SHA-256 in `MANIFEST.md`).
**Cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §24.
**Reconciled artifact:** `/app/docs/g4_prep/mtafiti_prep.md`.

**Discipline:** source wins; sketch corrects to source; no shipped Mtafiti code exists.

## 1. Two-layer measure (spec §3)

**Verdict: MATCH.** Prep §3 + §4 correctly describes deterministic declaration baseline + learned inference overlay. Baseline stands alone until V3 admits overlay.

## 2. Detect-versus-decide boundary (spec §4 + §10 + §11)

**Verdict: MATCH.** Prep §6 asserts: inference emits detections only, never verdict; verdict is Matrix lookup carrying `matrix_rule_ref`; inference module never imports `verdict.py`. Aligned with spec §10 + §11.

## 3. Module layout (spec §7)

Spec §7:
```
services/mtafiti/
  census.py            # estate walk; enumerates sources; objective-blind
  declaration.py       # feed-level source-standing baseline (deterministic)
  inference.py         # learned detectors: attachment / genre-form / corrob.
  measure.py           # composes baseline + detections -> score_vector
  verdict.py           # Qualification Matrix lookup -> defensibility_class
  registry.py          # append/update Registry records; freshness
  interfaces.py        # opaque handles (MatrixHandle) — boundary types
contracts/
  registry_record.py   # frozen: RegistryRecord
routers/
  mtafiti.py           # census status + registry read API
```

Prep §7 previously listed: `census.py, declaration_baseline.py, inference_overlay.py, registry_writer.py, matrix_handle.py, freshness.py, routers/mtafiti.py`. Missing separate `measure.py, verdict.py, interfaces.py`; incorrectly named `declaration_baseline.py` (spec: `declaration.py`), `inference_overlay.py` (spec: `inference.py`), `registry_writer.py` (spec: `registry.py`), `matrix_handle.py` (spec: in `interfaces.py`), `freshness.py` (spec: in `registry.py`).

**Verdict: SKETCH_CORRECTION.** Prep §7 updated to spec §7 layout verbatim.

## 4. Data contracts (spec §13)

Spec §13 declares:
- `RegistryRecord` (frozen contract) — `source_ref, region, feed_id, sensitivity, defensibility_measure (ScoreVector), defensibility_runtime_mode, freshness_stamp`.
- `ScoreVector` — with fields `source_standing, attachment, corroboration, recency_validity, contested`.
- `FreshnessStamp` — `{ logged_date, structural_sig }`.

Prep §5 correctly names `contracts/registry_record.py` and identifies `ScoreVector` + `FreshnessStamp` as sub-shapes with CONFIRM markers.

**Verdict: MATCH.**

## 5. Inference overlay — detections only (spec §10)

Spec §10 declares `Detections` dataclass:
```python
attachment_markedness: float
genre_form: str
corroboration: float
confidences: Mapping[str, float]
```

Prep §4 correctly lists these detections and enforces that inference emits Detections only, never `defensibility_class`.

**Verdict: MATCH.**

## 6. Governed verdict (spec §11)

Spec §11 declares `assign_verdict(claim_genre, context, matrix: MatrixHandle) -> Verdict` — deterministic Matrix lookup recording `matrix_rule_ref`.

Prep §5 and §6 confirm the discipline. **MATCH.**

## 7. V3 admission gate (spec §12)

Spec §12: overlay admitted only when `fact_precision >= threshold.fact_precision` AND `genre_accuracy >= threshold.genre_accuracy`. Failure → baseline-only, Registry marks `defensibility_runtime_mode='declaration_baseline'`.

Prep §4 also mentions `inter_annotator_floor` (kappa). Spec §12 discusses this obliquely ("inter-annotator kappa >= floor before accuracy is computed"). Product Spec 2.1 §29.2 confirms κ ≥ 0.70 as V3 discipline. Kept in prep as it aligns with cross-referenced parent.

**Verdict: MATCH.** All three thresholds preserved.

## 8. Freshness (spec §13)

Spec §13: two-level freshness check (logged-date L1 + structural-delta L2) drives scoped re-discovery of only the affected region.

Prep §7 previously proposed `services/mtafiti/freshness.py` as a separate module. Spec §7 keeps freshness inside `registry.py`.

**Verdict: SKETCH_CORRECTION.** `freshness.py` folded into `registry.py` per spec §7.

## 9. Invariants (spec §17 — 9 invariants)

Spec §17 lists **9 binding invariants**. Prep §6 lists 12+ narrative bullet points.

**Verdict: SKETCH_CORRECTION.** Sketch §6 rewritten to reference spec §17's 9-invariant set with G4 landing shapes:

| # | Spec text (abbrev.) | G4 landing shape |
|---|---|---|
| 1 | Discovers + measures; does not extract, target, govern; census exhaustive + objective-blind | `census.py` — no objective read |
| 2 | Two-layer measure (declaration baseline + inference overlay); baseline always available and stands alone | `measure.py::measure(cand, standing, detections, v3_admitted)` |
| 3 | Inference emits detections only; never assigns class; never imports verdict.py | `test_inference_emits_no_verdict` |
| 4 | Verdict = deterministic Matrix lookup with `matrix_rule_ref` | `test_verdict_is_matrix_lookup` |
| 5 | Measure is targeting/flooring prior, not truth verdict; fails toward caution; overlay V3-gated | `overlay_admitted(v3_result)` gate |
| 6 | Source-standing declared once per feed — low cardinality, never per item | `declaration.py::declared_standing(feed_id, table)` |
| 7 | RegistryRecord is contract-grade — snapshot + invariant — records runtime mode | `contracts/registry_record.py` + `tests/invariants/registry_record.contract_snapshot.json` |
| 8 | Freshness re-measures only affected region on structural change | `test_freshness_scoped_rediscovery` |
| 9 | Objective-blind: one measure serves every objective | `test_census_objective_blind` |

## 10. Test obligations (spec §14 — 6 tests)

**Verdict: MATCH.** Prep §6 (updated) matches spec §14's 6 named tests:
1. `test_inference_emits_no_verdict`
2. `test_verdict_is_matrix_lookup`
3. `test_baseline_stands_alone`
4. `test_census_objective_blind`
5. `test_registry_record_frozen`
6. `test_freshness_scoped_rediscovery`

## 11. Product Spec 2.1 cross-reference

- §24 (Mtafiti parent behavioural description) — MATCH.
- §31 invariant #3 ("verdict is a governed Matrix lookup, never a learned weight") — MATCH.
- §31 invariant #4 ("Mtafiti's inference walled from the verdict") — MATCH.
- §29.2 V3 gate thresholds — cross-referenced.

## 12. Governance (spec §18)

Spec §18: two open decisions —
1. V3 admission thresholds (project owner; shared with V3 gate)
2. Feed source-standing declaration table content (MEA)

**Verdict: MATCH.** `OPEN_GOVERNANCE.md` §3 + §4 tracks both.

---

## CODE_IMPACT items

**none.** No shipped Mtafiti code exists.

## Corrections applied to `docs/g4_prep/mtafiti_prep.md`

1. §7 module layout: renamed `declaration_baseline.py → declaration.py`, `inference_overlay.py → inference.py`, `registry_writer.py → registry.py`; folded `freshness.py` into `registry.py`; folded `matrix_handle.py` into `interfaces.py`; added `measure.py, verdict.py, interfaces.py`.
2. §6 invariants list: rewritten from narrative 12-bullet form to canonical 9 invariants per spec §17.
3. §6 test obligations: aligned to spec §14's 6 named tests.
4. Frontmatter: source citation updated to on-disk canonical.

## Summary

- **MATCH: 7** (two-layer measure, detect-versus-decide, data contracts, detections, governed verdict, V3 gate, product spec cross-ref).
- **SKETCH_CORRECTION: 4** (module layout §3, freshness placement §8, invariants list §9, test obligations §10).
- **CODE_IMPACT: 0.**
- **HAZARD-STOP (a) raised: NO.**

**Verdict:** Mtafiti prep sketch corrected in-place. Ready for G4 dispatch when governance items 3 + 4 (owner / MEA) resolve.
