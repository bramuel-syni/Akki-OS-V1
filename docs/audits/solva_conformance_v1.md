# Solva-depth-v1 Conformance Audit — G1 retrospective

**Reference:** Solva Mandate & Engineering Spec
(https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/xpiuddby_RMS_Solva_Mandate_and_Engineering_Spec.docx).

**Implementation-bound-to:** G1 Solva-depth-v1 (Ring 5 stamp), built against
paraphrased spec at G1 close. `/app/backend/services/g1_defensibility/*`.

**Discipline (norm #9):** conformance audit; G1 stays closed; MATERIAL_GAPs
would be HAZARD-STOP #4 territory. Findings only — no code rework.

**Legend:** `MATCH` · `SPEC_EXPANSION_HONOURED` · `MATERIAL_GAP` · `PENDING_G3`
(scope belongs to G3 by spec §4 vs §5 split, so absence at G1 is correct).

## 1. G1 obligations per Solva spec §4

| Spec §4 requirement | G1 impl | Verdict |
|---|---|---|
| "Wide-bar" reshape v1 mode | `services/g1_defensibility/solva_depth/*` — reshape-v1 discipline held (BUILD_JOURNAL G1 close entry) | **MATCH** |
| Judge which signal descriptors / relational edges / defensibility refinements to preserve for the mandate-class | `solva_depth/governor.py::depth_judge` + `integrity_validators.py::ValidatorOffender` shape + `preservation_depth` inputs; G1 identifies preserve/refuse per unit | **MATCH** |
| Emit Ring 5 defensibility stamp at convergence | `ring5_stamper.py::stamp_ring5` — emits `DefensibilityRing` shape (per `five_rings@v0`) with `floor_violation` flag | **MATCH** |
| Record refusal reasons in stamp-audit side-channel | `stamp_audit.py::StampAuditEntry` — ring buffer per §7.3 swap-in (G2 absorption already wired via `services/northena/ledger.py::absorb_stamp_audit`) | **MATCH** |

## 2. Solva binding invariants (12 total per spec §8)

Solva invariants apply full-system; G1 covers a subset because the assertion
boundary + five-stage pipeline are G3-scoped (spec §5). PENDING_G3 = correct
absence at G1.

| # | Invariant (verbatim) | G1 verdict | Evidence |
|---|---|---|---|
| 1 | Solva reasons; never extracts, never reaches operator primitives | **MATCH** | G1 stamper reads Layer C outputs; does not extract; no Akki-primitive imports (grep confirmed) |
| 2 | Issues operations and interprets results | **PENDING_G3** | G1 stamps per-unit; multi-op orchestration is G3 five-stage |
| 3 | Two faculties (free reasoning + bound assertion) | **PENDING_G3** | G3 obligation — no five-stage at G1 |
| 4 | Seam is one-way (reasoning cannot cross into assertion via strength) | **MATCH** | G1 has no reasoning-strength input; stamps derive from source_standing declaration + governor floor check |
| 5 | Class = floor over load-bearing units' classes | **PENDING_G3** | Load-bearing selection is G3 (five-stage Reflection); G1 is per-unit only |
| 6 | Reasoning strength not an input; cannot raise class | **MATCH** | G1's `stamp_ring5` signature carries no confidence parameter; class derives from Ring 5 vector + declaration baseline |
| 7 | Utterance-class conclusion asserted as "was stated," never as fact | **MATCH** | `DefensibilityClass` enum drives G1's stamp; utterance-class stamp does not become fact — validated at Ring 5 vector composition |
| 8 | Solva identifies load-bearing units; does not choose the class those units imply | **PENDING_G3** | Load-bearing identification is G3 |
| 9 | Floor + Matrix verdict are read-only to Solva | **MATCH** | G1's `source_standing_reader.py` reads MEA declaration; no writes into `qualification_matrix@v0`; no floor mutation |
| 10 | Solva reasons within them and refuses below floor; never sets or relaxes | **MATCH** | `governor.py` L52 refuses on `floor_violation`; does not relax any floor |
| 11 | Refusal below floor is structured, visible | **MATCH** | `refusal.py::DepthRefusalResult` — structured `(category, reason, floor_violation)`; ring-buffer visible via `/api/v1/stamp_audit/recent` |
| 12 | Every extraction-time judgment produces a trace (path + load-bearing + class) | **PENDING_G3** | G1 records `StampAuditEntry` per unit stamp; multi-unit trace with reasoning-path + load-bearing is G3 |

**G1 invariant coverage: 7 MATCH / 5 PENDING_G3 / 0 MATERIAL_GAP.**

The 5 PENDING_G3 invariants are correct absences: spec §5 explicitly assigns
five-stage reasoning + assertion boundary + trace to G3. G1's Ring 5 stamper
is per-unit depth judgment, not multi-unit conclusion synthesis.

## 3. Spec-expansions vs paraphrased-spec-at-G1-close

| Expansion in the consolidated spec | G1 impl status | Verdict |
|---|---|---|
| Refusal visibility (structured + visible, not silently downgraded) | Implemented as `DepthRefusalResult` + `/api/v1/stamp_audit/recent` HTTP surface | **SPEC_EXPANSION_HONOURED** (impl leads spec) |
| `unverifiable-substrate-absent` labelling when integration point can't resolve | Post-G2a lift-manifest lint enforces exactly this state (Condition 2). G1's own transitive lifts (`integrity_validators.py`) journal cousin absence honestly | **SPEC_EXPANSION_HONOURED** — the discipline the spec names is already CI-enforced |
| Tension stage: surface contradiction/retraction rather than averaging | **PENDING_G3** — Tension is one of the five G3 stages; not a G1 obligation |

## 4. §18 — no governance items pending for Solva

Confirmed by spec: no design decision is left open. Solva is a build-time
choice bounded by its invariants. Distinct from Targeta (yield-layer
thresholds pending owner), Mtafiti (V3 thresholds + declaration table
pending owner/MEA), Northena (Ledger retention pending DPO).

`/app/docs/g4_prep/OPEN_GOVERNANCE.md` updated to record Solva has **NO**
governance items.

## Summary

- **7 MATCH · 5 PENDING_G3 · 3 SPEC_EXPANSION_HONOURED · 0 MATERIAL_GAP**
- G1 Solva-depth-v1 conforms to the consolidated Solva spec for G1's scope.
- The 5 PENDING_G3 invariants are structural — spec-required at G3 (five
  stages + boundary + trace); intentionally absent at G1.
- **NO HAZARD-STOP.** G1 stays closed. G3 dispatch will pick up the
  PENDING_G3 invariants directly.
