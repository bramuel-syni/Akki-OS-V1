# Solva Reconciliation — Substrate-Drop v1

**Canonical source:** `/app/docs/mandates/RMS_Solva_Specification.md` (SHA-256 in `MANIFEST.md`).
**Cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §23 (parent).
**Reconciled artifact:** `/app/docs/g3_prep/solva_prep.md` (read-only G3 prep sketch).

**Discipline:** source wins; sketch corrects to source; no shipped Solva G3 code exists — CODE_IMPACT is limited to G2a's `services/solva_depth/admit_assist.py` (Northena's admit-assist shim), which is Northena-owned per the previous reconciliation.

## Legend: as per Northena reconciliation.

## 1. Two faculties + one-way seam (spec §3)

**Verdict: MATCH.** Prep §2 correctly describes: free reasoning faculty (5 stages) + bound assertion boundary (single function `conclusion_class`). Prep matches spec §3 verbatim.

## 2. Five stages (spec §8)

**Verdict: MATCH.** Prep §2.1 enumerates Frame / Candidate / Tension / Probability / Reflection with spec-aligned one-liners.

## 3. Assertion boundary — `conclusion_class` (spec §10)

**Verdict: MATCH.** Prep §2.2 shows `conclusion_class(load_bearing_units: list[UnitRef]) -> str` — takes only load-bearing units, no confidence parameter. Spec §10 confirms exact same signature: "conclusion_class takes NO confidence argument." Construction-as-guard property preserved.

## 4. Module layout (spec §7)

Spec §7 declares:
```
services/solva_depth/
  reasoning.py          # 5 stages: frame/candidate/tension/probability/reflection
  load_bearing.py       # identifies load-bearing units (a reasoning judgment)
  assertion.py          # computes defensibility class = floor over load-bearing
  enforce.py            # applies the floor from the Objective Request; refuses
  stamp.py              # Ring 5 emission at convergence
  trace.py              # records path + load-bearing + class + conclusion
  interfaces.py         # opaque handles (MatrixHandle, FloorSpec) — read-only
routers/
  solva.py              # enforcement + trace read surfaces
```

Prep §5 previously used `services/solva_g3/` namespace with per-stage files (`boundary.py, frame.py, candidate.py, tension.py, probability.py, reflection.py`).

**Verdict: SKETCH_CORRECTION.** Sketch has been rewritten to reflect spec §7 module layout:
- **BEFORE**: `services/solva_g3/boundary.py + frame.py + candidate.py + tension.py + probability.py + reflection.py`
- **AFTER**: `services/solva_depth/{reasoning.py, load_bearing.py, assertion.py, enforce.py, stamp.py, trace.py, interfaces.py}` + `routers/solva.py`

Corrections applied in-place to `docs/g3_prep/solva_prep.md` §5 (see BUILD_JOURNAL entry).

**Note on existing `services/solva_depth/admit_assist.py`:** the file was placed there at G2a as the Northena-side Solva admit-assist shim (a sibling to G1's Solva depth v1 at `services/g1_defensibility/solva_depth/`). Spec §7 does NOT list `admit_assist.py` in Solva's module layout. This is deliberate — the admit-assist is Northena's caller-side shim, and the Solva-side implementation of `SolvaHandle` lands at G3 as part of `interfaces.py`. G3 reshape will move / rename accordingly; **not CODE_IMPACT** (G3-time restructure of a G2a-placed sibling module).

## 5. Read-only governed values (spec §11)

Spec §11: `enforce(conclusion, load_bearing_units, floor: FloorSpec) -> Result`. Floor + Matrix verdict read through read-only handles; Solva refuses below floor with structured reason.

Prep §3 confirms integration points against actually-frozen contracts:
- `defensibility_floor` from `ObjectiveRequest` — CONFIRMED against `contracts/objective_request.py` (@v0)
- `defensibility_class` enum — CONFIRMED against `contracts/five_rings.py::DefensibilityClass`
- `UnitRef` — CONFIRMED as `unit_id: str` from `contracts/five_rings.py::NormalizedUnit`
- `QualificationMatrix` verdict — CONFIRMED against `contracts/qualification_matrix/*`
- `StageRecord` / `SolvaTrace` — PENDING G3 (new frozen contracts)

**Verdict: MATCH.** Prep §3 aligns with spec §11 read-only handle discipline.

## 6. Trace-from-first-commit (spec §13)

Spec §13 declares `SolvaTrace` with `trace_id, stages, load_bearing, computed_class, conclusion`. Prep §4 shows the same shape and correctly identifies the Northena Ledger absorption seam (`LedgerRow.stamp_audit` as `Optional[Dict]` accepts free-form trace blob via a new `absorb_solva_trace` helper — mirroring the existing `absorb_stamp_audit` swap-in at `services/northena/ledger.py`).

**Verdict: MATCH.** No Northena contract change required — `stamp_audit` field already accepts the trace shape. G3 will add `absorb_solva_trace` helper.

## 7. Invariants (spec §17 — 9 invariants)

Spec §17 lists **9 binding invariants**. Prep §6 previously used the phrase "12 binding invariants" and lists 7 rows (with a "PENDING_G3" verdict at G1 audit).

**Verdict: SKETCH_CORRECTION.** The "12" count came from the pre-drop consolidated-Solva-spec ingested-then-discarded document (which mixed reasoning-stage substeps with invariants). The new canonical spec has **9 invariants**. Sketch has been updated in-place to reference §17's 9-invariant set:

| # | Spec text (abbrev.) | G3 landing shape |
|---|---|---|
| 1 | Solva reasons, never extracts | Stages 1–4 call operator primitives; Reflection interprets |
| 2 | Two faculties (free + bound) with one-way seam | `assertion.py` bound; five-stage `reasoning.py` free — dependency rule enforced by import assertion |
| 3 | Conclusion class = floor over load-bearing units' classes | `conclusion_class(load_bearing_units)` — no confidence input |
| 4 | Utterance-class asserted as "was stated", never fact | `Assertion` shape distinguishes claim + class; utterance path stamped explicitly |
| 5 | Solva identifies load-bearing; does not choose class | Stage 5 (Reflection) picks load-bearing; boundary computes class mechanically |
| 6 | Floor + Matrix verdict read-only | `FloorSpec` + `MatrixHandle` in `interfaces.py` — read-only |
| 7 | Below-floor conclusion refused with structured reason | `enforce.py` returns `Refusal(reason=..., computed_class=..., floor=...)` |
| 8 | Every judgment produces a trace | `SolvaTrace` frozen contract at G3 |
| 9 | Solva governs depth only; three axes never collapsed | Import assertion + N-INV-11 orthogonal grep |

## 8. Governance (spec §18)

Spec §18: *"No design decision in this mandate is left open."*

**Verdict: MATCH.** Prep §7 correctly states "No governance surface." `OPEN_GOVERNANCE.md` records Solva has zero pending governance items.

## 9. Test obligations (spec §14 — 7 tests)

| Spec test | G3 landing |
|---|---|
| `test_class_is_floor_over_load_bearing` | `services/solva_depth/tests/test_assertion.py` |
| `test_class_takes_no_confidence` | signature-inspection test |
| `test_utterance_never_asserted_as_fact` | boundary composition test |
| `test_refuse_below_floor` | `enforce.py` refusal test |
| `test_solva_reads_governed_values_readonly` | dependency-rule / import-assertion test |
| `test_solva_never_extracts` | dependency-rule test |
| `test_trace_records_load_bearing_and_class` | trace-frozen-shape test |

**Verdict: G3 obligation.** All 7 tests must land at G3 dispatch; sketch §5 test-list has been updated to reflect the 7 spec tests instead of an under-specified count.

## 10. Product Spec 2.1 cross-reference

- §23 (Solva parent behavioural description) — MATCH.
- §31 invariant #4 ("powerful part walled from governed decision — Solva's reasoning from the assertion ceiling") — MATCH.
- §31 invariant #5 (three governors on orthogonal axes) — MATCH.
- §26 Frozen Contract Set — Solva does not introduce a new frozen contract at G3 that appears in the six; `SolvaTrace` is a G3-forced contract (frozen but outside the parent six per spec §26 discipline). Clarified.

---

## CODE_IMPACT items

**none.**

No shipped Solva G3 code exists. The G2a-placed `services/solva_depth/admit_assist.py` is Northena's caller-side shim (governed by Northena spec §9 / §13). Its restructure at G3 is a scheduled reshape, not a contradiction.

## Corrections applied to `docs/g3_prep/solva_prep.md`

1. §5 (module layout) — namespace `services/solva_g3/` → `services/solva_depth/`; per-stage files → spec §7 layout (`reasoning.py + load_bearing.py + assertion.py + enforce.py + stamp.py + trace.py + interfaces.py + routers/solva.py`).
2. §6 (invariant count) — "12 binding invariants" → "9 binding invariants" (canonical spec §17); rebuilt table from the 9 canonical.
3. §5 (test list) — reworded to reflect spec §14's 7 named test obligations.
4. §3 (integration points) — added Product Spec 2.1 §31 invariant #4 cross-reference.
5. Frontmatter — source citation updated from "ingested-then-discarded" to the on-disk canonical.

## Summary

- **MATCH: 6** (two faculties, five stages, assertion boundary, read-only handles, trace shape, governance-none).
- **SKETCH_CORRECTION: 5** (module layout §4, invariant count/list §7, test obligations §9, integration cross-ref §10, source citation §11).
- **CODE_IMPACT: 0.**
- **HAZARD-STOP (a) raised: NO.**

**Verdict:** G3 prep sketch corrected in-place. Zero shipped-code contradictions. G3 opens against source when user dispatches.
