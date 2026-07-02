# Mtafiti scope from source — G4 pre-code note

**Source:** `/app/docs/mandates/RMS_Mtafiti_Specification.md` (SHA-256 `8e4a7ece…a7db` in `MANIFEST.md`).
**Parent cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §24.
**Freshness:** all 3 required specs (Mtafiti, Targeta, Product v2.1) classified CURRENT at Step 0 substrate gate.
**Discipline:** source wins. All 6 existing frozen contracts UNTOUCHED unless HAZARD-STOP (a) is surfaced.

## 1. Registry structure (source §5, §13)

Mtafiti writes one **Registry record per source**. Frozen contract with snapshot + invariant (mandate §7 + §13).

Source §13 fields:
```python
@dataclass(frozen=True)
class RegistryRecord:
    source_ref: str
    region: str
    feed_id: str
    sensitivity: str
    defensibility_measure: ScoreVector       # baseline + (admitted) detections
    defensibility_runtime_mode: str          # 'declaration_baseline' | 'overlay'
    freshness_stamp: FreshnessStamp          # { logged_date, structural_signature }
```

**New frozen contracts to author at G4** (additions — NOT mutations of existing 6):
1. `MtafitiRegistryRecord` (Pydantic; snapshot + invariant at `tests/invariants/mtafiti_registry_record.contract_snapshot.json`).
2. `FreshnessStamp` — `{ logged_date: str, structural_signature: Optional[str] }` (L2 nullable at v0 until fixture extension lands).
3. `MtafitiScoreVector` — `{ source_standing: str, attachment: float, corroboration: float, recency_validity: float, contested: bool }`. **This is distinct from `contracts/five_rings.py::ScoreVector`** (which is Ring 5 signal-strength). Mtafiti's ScoreVector is the defensibility-measure composed at Registry-write time. Naming: `MtafitiScoreVector` to disambiguate.

CONFIRM check (source §13 line: "CONFIRM: ScoreVector + FreshnessStamp against five_rings@v0"):
- `contracts/five_rings.py::ScoreVector` is a Ring-5 field: `{ authorship, timing, source_standing }` (nested inside Defensibility). Distinct role from Mtafiti's Registry ScoreVector. No mutation to five_rings@v0 needed.
- **H-a (contract mutation) NOT RAISED.**

## 2. Census procedure (source §8)

`census.py` exhaustively walks the estate and produces `SourceCandidate` per source. Objective-blind (**invariant #1, #9**). Reads on-disk fixture feeds via the existing `SyntheticPlumbingDataSource`.

```python
def census(estate) -> Iterator[SourceCandidate]:
    for source in estate.walk():
        yield SourceCandidate(
            source_ref=source.ref,
            region=source.region,
            feed_id=source.feed_id,
            sensitivity=classify_sensitivity(source),
        )
```

Source §14 line "Estate → census: exhaustive walk of the estate; CONFIRM the walk interface": the walk interface is `SyntheticPlumbingDataSource.iter_units()` at G4 (fixture-backed); real-estate walk lands at G5+.

## 3. Declaration baseline (source §9 — LIVE at G4)

`declaration.py` reads MEA-owned per-feed source-standing declaration. Values (source §9): `accountable | licensed_wire | aggregator | ugc | unknown`. Baseline is deterministic, low-cardinality, feed-level, always available.

MEA table content is placeholder per user directive (4): `synthetic_placeholder=True`, `editorial_authority=False`, but every fixture feed_id must have an entry (empty would break plumbing).

## 4. V3 overlay (source §10, §12 — DARK closed seam at G4)

`inference.py` emits `Detections` (attachment_markedness, genre_form, corroboration, confidences). Never imports `verdict.py`. Never assigns `defensibility_class`. Import-boundary enforced by structural test.

**V3 admission gate** (source §12):
```python
def overlay_admitted(v3_result) -> bool:
    return (v3_result.fact_precision >= v3_result.thresholds.fact_precision
            and v3_result.genre_accuracy >= v3_result.thresholds.genre_accuracy)
```

**Threshold field names** (from source §12 + §18 open decisions):
- `fact_precision`
- `genre_accuracy`
- `inter_annotator_floor` (used as pre-condition before accuracy is computed)

Owner-owned per §18. G4 lands as **`V3Thresholds | None`**; overlay_admitted returns `False` when `None`. Closed-seam pattern per user directive (3).

## 5. Freshness (source §13)

Two-level check: L1 = `logged_date` (deterministic timestamp), L2 = `structural_signature` (16-hex sha256 of source content).

**L1 at G4**: LIVE. Baseline-recording writes `logged_date` = ISO-8601 UTC of the Registry-write moment.

**L2 at G4**: deferred to distinct sub-task. Requires surgical extension of `services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` per Substrate-Drop v1 G4-prep TODO (`docs/g4_prep/mtafiti_prep.md`). If extension can fit under `provenance.locator` (already free-form `Dict`), no contract change. If it demands `NormalizedUnit` shape change → HAZARD-STOP (a).

**Landing shape at G4**: `FreshnessStamp.structural_signature: Optional[str] = None`. Registry accepts None until fixture emits it. When fixture emits it, backfill on next census.

## 6. Source-standing interface (source §14 + user directive (4))

Interface (source §14): "Feed declaration → baseline: MEA-owned per-feed source-standing table". Content is MEA-owned; interface is Mtafiti's to declare.

`config/source_standing.yaml` (or `services/mtafiti/source_standing.py`) provides a placeholder table covering the on-disk fixture's feed IDs. Real table swap-in by config.

## 7. Ring 5 / signal-ring integration

Source §13: "CONFIRM: ScoreVector + FreshnessStamp against five_rings@v0." Confirmed above (§1). **NO frozen-contract mutation.**

Source §11: "measure composes deterministic baseline + (admitted) detections into a score vector, verdict is Matrix lookup." Matrix is `contracts/qualification_matrix/loader.py::QualificationMatrix` — read via `MatrixHandle` (Protocol already defined at G3 in `solva_depth/interfaces.py`).

Cross-anchor to Product v2.1 §15 (Ring 5 defensibility): Mtafiti Registry provides the `defensibility_class` that Ring 5 records at per-unit stamp time (via G1 stamper). Existing G1 `services/g1_defensibility/ring5_stamper.py` continues to stamp; at G4, when Mtafiti Registry is available, the stamper consults it as an additional signal. **This is a lookup extension, not a re-freeze.**

## 8. Nine invariants (source §17)

| # | Invariant | Landing at G4 | Test |
|---|---|---|---|
| 1 | Mtafiti discovers + measures; census objective-blind | `census.py` accepts no ObjectiveRequest param | `test_mtafiti_census_objective_blind` |
| 2 | Two-layer measure; baseline always available | `measure.py` composes baseline; when overlay not admitted, only baseline enters | `test_mtafiti_baseline_stands_alone` |
| 3 | Inference emits detections only; never imports verdict.py | Grep: `inference.py` has no `import verdict`; no `DefensibilityClass(` construction | `test_mtafiti_inference_emits_no_verdict` |
| 4 | Verdict via Matrix deterministic lookup; carries `matrix_rule_ref` | `verdict.py::assign_verdict` returns `Verdict(matrix_rule_ref=rule.ref)` | `test_mtafiti_verdict_is_matrix_lookup` |
| 5 | Measure is prior + fails toward caution; overlay gated by V3 | `overlay_admitted()` returns False when thresholds None | `test_mtafiti_v3_overlay_closed_seam` |
| 6 | Source-standing declared once per feed, low-cardinality | `declaration.py::declared_standing` keys on `feed_id`, not source_ref | (structural — one row per feed) |
| 7 | Registry record is contract-grade + snapshot-invariant + records runtime mode | `MtafitiRegistryRecord.defensibility_runtime_mode` field | `test_mtafiti_registry_contract` |
| 8 | Freshness re-measures affected region only | `registry.py::freshness_check` returns region ids to re-measure | `test_mtafiti_freshness_l1_l2` |
| 9 | Objective-blind: one Registry serves every objective | `census.py` + `declaration.py` + `measure.py` accept no ObjectiveRequest | (covered by #1) |

## 9. Contract-mutation hazard check

Reviewed all six frozen contracts: `five_rings@v0`, `objective_request@v0`, `qualification_matrix@v0`, `signal_ring_dimensions@v0`, `extraction_params@v0`, `northena_ledger_row@v0`.

- `five_rings@v0`: Mtafiti's `MtafitiScoreVector` is a NEW type (distinct from Ring 5 `ScoreVector`). No mutation.
- `qualification_matrix@v0`: verdict.py CONSUMES via `MatrixHandle` — read-only. No mutation.
- `northena_ledger_row@v0`: Mtafiti does not write to Ledger. No touch.
- Others: no interaction.

**Contract-mutation demands detected: NONE.**
**HAZARD-STOP (a) NOT RAISED.**

## Ready-to-code checklist

- [x] Source §-anchors mapped
- [x] All 3 new frozen contracts (MtafitiRegistryRecord, FreshnessStamp, MtafitiScoreVector) identified as ADDITIONS not mutations
- [x] V3 threshold field names identified (`fact_precision`, `genre_accuracy`, `inter_annotator_floor`)
- [x] Closed-seam pattern applies to V3 overlay
- [x] MEA placeholder table plan established
- [x] L1 freshness live; L2 deferred behind Substrate-Drop v1 fixture-extension gate
- [x] 9 invariants mapped to tests
