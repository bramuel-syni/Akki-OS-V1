# Mtafiti G4 prep — read-only sketch

**Source:** `/app/docs/mandates/RMS_Mtafiti_Specification.md` (SHA-256 in `/app/docs/mandates/MANIFEST.md`). **Read now, act at G4.** No code written this pass.
**Parent cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §24.
**Reconciliation:** `/app/docs/audits/substrate_drop_v1/mtafiti_reconciliation.md` (Substrate-Drop v1, 2026-07-01).

## 1. Purpose (G4 role)

Discovery engine. Censuses the estate exhaustively, writes the Registry. What exists, at what sensitivity, how defensible each source is. Objective-blind — measures the estate as it is; one Registry serves all objectives. Runs once at standup, then freshness-mechanism maintains it. Substrate for Targeta (mining) and Layer C (Ring 5 defensibility stamps).

## 2. Inputs (CONFIRM at G4)

- Estate-walk interface (from estate substrate).
- MEA-owned per-feed source-standing table (declaration baseline content, populated by MEA).
- Qualification Matrix via opaque `MatrixHandle` for deterministic lookup (`qualification_matrix@v0` already frozen).

## 3. Objective-blind census + declaration baseline (STANDS ALONE without V3; spec §8 + §9)

- **Census** (spec §8): walks the estate; enumerates sources; classifies sensitivity; attaches feed identity. Emits `SourceCandidate`. No defensibility inference here.
- **Declaration baseline** (spec §9): reads RMS per-feed source-standing declaration; applies to all sources under that feed. Deterministic, low-cardinality (5 values: `accountable | licensed_wire | aggregator | ugc | unknown`), stable, estate-wide, always available. Serves as the certain floor. Never per-item.
- **Registry record (partial)**: `source_ref`, `region`, `feed_id`, `sensitivity`, `freshness_stamp`, `defensibility_measure = ScoreVector(source_standing, recency_validity, contested)`, and `defensibility_runtime_mode = "declaration_baseline"`.
- **This subset ships at G4 without waiting for V3**. Baseline stands alone.

## 4. Inference overlay (GATED on V3 real labelled slice; spec §10 + §12)

- Learned detectors that refine baseline from content.
- Emits `Detections` (spec §10): `attachment_markedness (float [0,1]), genre_form (str — detected form label, not a verdict), corroboration (float [0,1]), confidences (Mapping[str, float])`.
- **MUST NOT** import `verdict.py`. **MUST NOT** assign `defensibility_class` (spec §17.3).
- Admitted only after V3 gate passes (spec §12):
  - **fact-class precision** ≥ `v3_result.thresholds.fact_precision` (**PENDING owner sign-off**).
  - **genre accuracy** ≥ `v3_result.thresholds.genre_accuracy` (**PENDING owner sign-off**).
  - **inter-annotator kappa** ≥ `v3_result.thresholds.inter_annotator_floor` (**PENDING owner sign-off**; computed before accuracy — per Product Spec 2.1 §29.2, floor κ ≥ 0.70).
- When admitted: `defensibility_measure` gains `{attachment, corroboration}` alongside baseline components; `runtime_mode` flips to `"overlay"`.

## 5. Frozen contracts Mtafiti introduces or references

- **`contracts/registry_record.py`** — new frozen contract at G4 (spec §13). Snapshot + invariant. Records `defensibility_runtime_mode`.
  - Sub-shapes: `ScoreVector(source_standing, attachment, corroboration, recency_validity, contested)`; `FreshnessStamp({logged_date, structural_sig})`. CONFIRM against `five_rings@v0` at G4.
- References: `qualification_matrix@v0` (via `MatrixHandle`), MEA source-standing declaration artifact (external, CONFIRM).

## 6. Nine binding invariants (spec §17)

Spec §17 lists **9 binding invariants** — canonical count per Substrate-Drop v1.

| # | Invariant | G4 landing shape |
|---|---|---|
| 1 | Discovers + measures; does not extract, target, govern; census exhaustive + objective-blind | `census.py` — no objective read; import assertion |
| 2 | Two-layer measure (deterministic feed-level declaration baseline + learned content inference overlay); baseline always available and stands alone when overlay not admitted | `measure.py::measure(cand, standing, detections, v3_admitted)` |
| 3 | Inference overlay emits detections only; never assigns defensibility verdict; never imports verdict.py | `test_inference_emits_no_verdict` — import assertion |
| 4 | Defensibility verdict assigned by Qualification Matrix by deterministic lookup; records `matrix_rule_ref`; no learned weight assigns a verdict | `test_verdict_is_matrix_lookup` |
| 5 | Measure is a targeting + flooring prior, not truth verdict; fails toward caution; reliance on overlay V3-gated; baseline + governed verdict do not depend on it | `overlay_admitted(v3_result)` gate; baseline path independent |
| 6 | Source-standing declared once per feed — low cardinality, never per item | `declaration.py::declared_standing(feed_id, table)` |
| 7 | Registry record is contract-grade — versioned, snapshot-and-invariant — records defensibility runtime mode (baseline or overlay) | `contracts/registry_record.py` + snapshot `tests/invariants/registry_record.contract_snapshot.json` |
| 8 | Freshness re-measures only affected region on detected structural change; never the whole estate silently | `test_freshness_scoped_rediscovery` |
| 9 | Objective-blind: one measure serves every objective; measure never conditioned on a particular objective | `test_census_objective_blind` |

## 7. Test obligations (spec §14 — 6 tests)

At G4 dispatch, land all 6 spec-named tests:

1. `test_inference_emits_no_verdict` — `inference.py` never imports `verdict.py` and never returns a `defensibility_class` (structural + import assertion).
2. `test_verdict_is_matrix_lookup` — every verdict carries a `matrix_rule_ref` resolving to a governed Matrix rule; no learned weight assigns the class.
3. `test_baseline_stands_alone` — with the overlay not admitted, `measure()` uses the declaration baseline only and the record marks `declaration_baseline`.
4. `test_census_objective_blind` — census consults no objective; one census output serves all objectives.
5. `test_registry_record_frozen` — `RegistryRecord` conforms to its snapshot; a schema change fails CI.
6. `test_freshness_scoped_rediscovery` — a structural delta re-measures only the affected region, not the estate.

## 8. G4 module layout (spec §7 — canonical, per Substrate-Drop v1)

**Substrate state as of 2026-07-01**: no Mtafiti-adjacent cousin in-pod (settled directive; `/reference/akki-legacy/` unreachable). G4 Mtafiti modules will land `mandate-forced-net-new` or `transitive` via existing intermediates.

Spec §7 canonical layout:

```
services/mtafiti/
  census.py           # estate walk; enumerates sources; objective-blind
  declaration.py      # feed-level source-standing baseline (deterministic)
  inference.py        # learned detectors: attachment / genre-form / corroboration
  measure.py          # composes baseline + detections -> score_vector
  verdict.py          # Qualification Matrix lookup -> defensibility_class
  registry.py         # append/update Registry records; freshness (L1 logged-date + L2 structural-delta)
  interfaces.py       # opaque handles (MatrixHandle) — boundary types
contracts/
  registry_record.py  # frozen: RegistryRecord
routers/
  mtafiti.py          # census status + registry read API
```

Lift manifest expectation per module:

| Module | Expected `lift_kind` | Cousin / chain candidate |
|---|---|---|
| `services/mtafiti/census.py` | `mandate-forced-net-new` | Spec §8 census is objective-blind — no in-pod analogue |
| `services/mtafiti/declaration.py` | `transitive` | via `services/g1_defensibility/source_standing_reader.py` (baseline reader already exists at G1) |
| `services/mtafiti/inference.py` | `mandate-forced-net-new` | Spec §10 declares learned detectors net-new; V3-gated |
| `services/mtafiti/measure.py` | `mandate-forced-net-new` | Spec §11 composes baseline + detections — mandate-forced |
| `services/mtafiti/verdict.py` | `transitive` | via `contracts/qualification_matrix/loader.py` (deterministic Matrix lookup pattern) |
| `services/mtafiti/registry.py` | `transitive` | via `services/northena/ledger.py::record` (append-only writer pattern) + freshness net-new |
| `services/mtafiti/interfaces.py` | `mandate-forced-net-new` | Spec §7 declares opaque `MatrixHandle` boundary type |
| `contracts/registry_record.py` | `mandate-forced-net-new` | Spec §13 forces contract shape; freeze-discipline reused from `northena_ledger.py` |
| `routers/mtafiti.py` | `transitive` | via `routers/northena.py` + `routers/contracts.py` |

**Expected Rule 2**: mandate-heavy phase; overall net-new probably > lifted. Discretionary should stay ≤ 2× lifted.

## 9. Pending governance items (see `docs/g4_prep/OPEN_GOVERNANCE.md`)

Spec §18 declares two open decisions:

1. **V3 admission thresholds** (project owner; shared with the V3 gate): `fact_precision, genre_accuracy, inter_annotator_floor`. Blocks admission of the inference overlay only. Not a blocker for the census or the declaration baseline, which ship and run without them.
2. **Feed source-standing declaration table** (MEA): content of the per-feed declaration table. Blocks population of declaration baseline at deploy. Mechanism is buildable without.

CONFIRM markers throughout spec — resolve at G4.

---

## G4 TODO — structural_signature primitive (from Substrate-Drop v1)

Carried forward from Substrate-Drop v1 fixture-substrate rejection (2026-07-01). The one genuinely-new signal in the rejected incoming fixture was `freshness_stamp.structural_signature` (a 16-hex sha256 of unit content), which maps to **Mtafiti Spec §13 L2-freshness mechanism**:

- L1 = `logged_date` (existing; wall-clock timestamp of ingestion)
- L2 = `structural_signature` (new; content-hash primitive detecting substantive change under stable ingestion time)

At G4 opening:
1. Surgically extend on-disk `services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` to emit a `structural_signature: str` (16-hex sha256 of unit content) on each unit. Do NOT relocate this into a new `freshness_stamp` sub-shape unless the frozen `NormalizedUnit` contract is re-blessed to house it — the incoming fixture's `freshness_stamp` top-level object was one of the reasons it failed contract conformance. Land the signature inside `provenance.locator` or as a top-level string field only after frozen-schema re-bless.
2. Wire `services/mtafiti/registry.py::freshness_check(record)` to consume L1 (existing timestamp) + L2 (new `structural_signature`); re-measure only the affected region on L2 delta.
3. Add `test_freshness_scoped_rediscovery` (per Mtafiti spec §14 obligation #6): a structural delta re-measures only the affected region, not the estate.

**Do NOT implement now.** This is a G4-scope reminder only. Contract additions (if any) must go through frozen-schema re-bless.

**Source references:**
- `docs/audits/substrate_drop_v1/fixture_substrate_diff.md` §5 — diff report showing `structural_signature` shape.
- `services/data_source/synthetic_assets/rms_adversarial_v1/rejected/REJECTION.md` — rejection record + preservation.
- Mtafiti Spec §13 (`RMS_Mtafiti_Specification.md`) — L1/L2 freshness mechanism.
