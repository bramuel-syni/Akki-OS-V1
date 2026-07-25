# Critic-pass · Stage A Proposal

**Phase:** Critic-pass · Tier-2 harness + CR-7 checklist amendment + CIF §6 A5 rubric cell + CIF manifest schema fields + archive ledger
**Dispatch class:** D-9 auto-proceed under standing ruling `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` (SHA `1f5ea9de8031cde255db0efd476074c9c3c9f8cc05ead2f20171dbb5c0d81d1d`) following clean close of EAB-3 execution atomic (2026-07-24 · Parity 32→33 sealed · full-sweep 1,549 cells green) + Change Order Filing (2026-07-25 · 7 amendments landed · CONFLICT rows disposed).
**Sequence position:** 4 of 7 (per phase ledger `docs/registers/phase_ledger_v1.md` §5).
**Source of truth (multi-anchor):**
- `docs/requirements/critic_seam_spec_v1.md` (SHA `110a0d0448f66f44461190cd01c2f8e92513bafdc7aeb9a4ff2bd7f748841b35`) — Part A canonical body
- `docs/requirements/critic_seam_spec_v1_1.md` (SHA `ad4529b9462cf789ab577f7f8a4ba4ed1fe8f33a096fce6a70669a826b8c5605`) — Part B pointer to TQ §7
- `docs/requirements/transformation_quality_spec_v1.md` (SHA `78af90cf64409364c9b9d97bbc2b7f0507f6b824ee1bc41bd610a79f1a44967e`) — §7 Production QA machinery (the Critic Seam's Part B — same three tiers, second domain)
- `docs/requirements/cif_spec_v1.md` (SHA `eb5a9e8bacdfc6d1d9f35cad41ff24b66a3127648a9f4aaeffe32b90973e7c1d` · Owner-cited SHA `110a0d0448f66f44` was stale · this atomic uses live on-disk SHA per D-11 canon-before-attest) — §6 A5 rubric + §12 enforcement map + §14 execution + archive ledger
- `docs/rulings/owner_change_order_2026-07-25.md` (SHA `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568`) — **post-amendment canon · consumed by Critic-pass Stage A per Owner ITEM 2 close discipline**
- `docs/governance/rules_taxonomy_v1.md` (SHA `63862a0375263e0b7c6d727c427c4c04aeb5785c401d8a2be06000fdd97f6758`) — A3.4 Rules Taxonomy classification (S/O/E/D)

---

## §1 · Purpose + scope (Owner-dispatched · verbatim absorption)

Critic Seam Spec v1.0 §5 verbatim: *"§5 — Tier 1: deterministic record-verification (rung 1). Six check families, all mechanical, all resolving against the repository. They run on the two artifact classes of the loop — Stage A proposals and close reports — and on ruling-authority documents at landing time. Each check emits PASS or a finding row; findings are inputs to rulings except where QA-2 scopes a hard gate."*

Critic Seam Spec v1.0 §6 verbatim: *"§6 — Tier 2: the critic pass (rung 3/4). §6.1 The rubric — the Owner's catch history, made standing. CR-1 anti-re-derivation · CR-2 anti-fabrication · CR-3 conflation test (D-3) · CR-4 scope semantics (D7) · CR-5 enforcement honesty (D-5) · CR-6 self-audit audit. §6.2 Independence and harness rules · No self-review (QA-3): the critic instance is never the instance that produced the artifact; where both are the same base model, independence is by context isolation."*

Critic Seam Spec v1.0 §7 verbatim: *"§7 — Tier 3: human calibration sampling. Verdict sampling · Seeded-defect audits · The calibration ledger: catch-rate and false-alarm rate per worker class and per rubric item, versioned like model calibration."*

Critic Seam Spec v1.1 §Part B verbatim: *"The Critic Seam's build-loop-worker architecture (Tier 1 deterministic record-verification · Tier 2 independent critic pass · Tier 3 human calibration sampling) applies identically to production pipeline output. The Transformation Quality & Output Acceptance Specification v1.0 §7 is the Critic Seam's Part B. QA-7 custody boundary from TQ §7 binds jointly with QA-1..QA-6."*

TQ §7 verbatim (line 115): *"§7 — Production QA machinery (the Critic Seam's Part B — same three tiers, second domain). The Critic Seam guards what workers produce; this section applies the identical architecture to what the pipeline produces. One QA design, two production domains, one calibration discipline."*

TQ §7 QA-7 verbatim (line 125): *"QA-7 — the custody boundary (RULED): quality of PROTECTION escalates as governance; quality of PRODUCT routes as findings. A de-identification recall breach, detected by any tier, is a governance failure: the affected batch quarantines fail-closed (the per-batch quarantine machinery, adopted). Utility-class findings (WER, F1, mapping fidelity) never block — detect-never-decide holds everywhere else."*

CIF §6 A5.1 verbatim: *"A5.1 · The coach's correction history is maintained as a readable pre-ship checklist of known failure classes, applied to picks and verdicts before shipping."*

CIF §6 A5.2 verbatim: *"A5.2 · The checklist is replay-only: it applies known classes, never claims novelty coverage, and labels its output a known-pattern check. It enters standing machinery as a Critic Seam rubric amendment (CR-7)."*

CIF §12 enforcement map verbatim (line 152 · manifest schema): *"Manifests: schema-required fields on every verdict-bearing artifact (Stage As, close reports, plan objects, training-run records, acceptance verdicts); an unmanifested verdict rejects at submission — the standing format-gate pattern, form only."*

CIF §12 enforcement map verbatim (line 154 · archive): *"Archive: entries as append-only ledger rows; a standing query surfaces evaluated-but-unarchived ideas as findings."*

CIF §14.2 verbatim: *"The archive initializes as a governed file with CIF as entry #1. A5's checklist lands as the CR-7 rubric amendment with its carrying phase."*

**Builder Tier-3 disclosure: NO SPLIT** — Critic-pass Tier-2 harness + CR-7 checklist amendment + CIF §6 A5 rubric cell + CIF manifest schema fields + archive ledger co-land as a single execution atomic. Rationale:
1. The five sub-components interlock on the Tier-2 harness anchor: CR-7 IS a Critic Seam rubric amendment per CIF A5.2 verbatim (*"enters standing machinery as a Critic Seam rubric amendment (CR-7)"*); CIF manifest schema is the format-gate substrate CR-6 self-audit reads from; archive ledger is where CIF §12 verdicts land (entry #1 = CIF itself per §13.3 verbatim); Tier-3 sampling scaffold is Owner-side but the calibration ledger reads from CR-1..CR-7 output.
2. §IX-analog discipline (no split-family named for Critic-pass; Critic Seam v1.0 §11 execution model: *"this document lands as a governed artifact; QA-1..QA-6 bind behaviorally at once (they are disciplines, costing nothing)"* — one landing atomic).
3. Splitting CR-1..CR-6 (Critic Seam v1.0) from CR-7 (CIF §6 A5) would contradict CIF A5.2 verbatim (CR-7 IS the rubric amendment · not a separate rubric).
4. Splitting the CIF manifest schema from the CR-6 self-audit consumer would land the schema without its proving consumer (contradicting D-12).

**Adopted mechanics landing in Critic-pass:**

**Tier 1 (§5 Critic Seam v1.0 · already-riding EAB phases per TQ §11):**
- RV-1..RV-6 check families run at Stage A + close-report + ruling-authority submission boundaries.
- RV-4 = format-gate hard gate per QA-2 (schema-completeness · missing sections including D-10 table reject the submission).
- Registered in Registry v1 with R4 rows (they are functions · pay rent like all functions).
- **On-disk status:** RV-4 format-gate substrate already lands as `test_substrate_drop_gate.py` + related pytest cells; this Stage A extends the RV-1..RV-6 family as executable cells at submission boundaries.

**Tier 2 (§6 Critic Seam v1.0 + CR-7 amendment from CIF A5.2):**
- CR-1 anti-re-derivation · CR-2 anti-fabrication · CR-3 conflation test (D-3) · CR-4 scope semantics (D7) · CR-5 enforcement honesty (D-5) · CR-6 self-audit audit · **CR-7 CIF selection-defect checklist** (Owner-verbatim coach-correction-history rubric · replay-only · labels output "known-pattern check").
- §6.2 independence and harness: no self-review (QA-3); critic instance ≠ produced instance; context isolation measured by seeded audits.
- Asynchronous · never blocks execution (QA-1: detect, never decide).

**Tier 3 (§7 Critic Seam v1.0 · Owner-side sampling instruments):**
- Verdict sampling (20% findings · 10% all-clears · DEFAULT).
- Seeded-defect audits (1/5 phases · DEFAULT · never in landing artifacts).
- Calibration ledger with staleness window (10 phases · DEFAULT · findings render UNCALIBRATED past window).
- **Owner-side scope**: builder lands the calibration-ledger machinery + sampling scaffold; Owner performs the sampling ceremonies. Fence: no builder-driven "verdict sample" this atomic.

**CIF manifest schema fields (§12 line 152):**
- Schema-required fields on verdict-bearing artifacts: (a) Stage-A proposals · (b) close reports · (c) plan objects · (d) training-run records · (e) acceptance verdicts.
- Fields per §4 Definitions: `manifest_entries: List[ManifestEntry]` where `ManifestEntry = {assumption_text: str, evidence_class: Literal["fact", "recalled", "inferred"], flip_condition: str}`.
- Format-gate at submission (QA-2-precedent · form only · unmanifested verdict rejects).

**Archive ledger (§12 line 154 + §14.2):**
- Append-only ledger row per evaluated idea · standing query surfaces evaluated-but-unarchived findings.
- Rides existing Northena ledger machinery per `PROM-S3-append-only-ledger` — same discipline as EAB-2 quarantine ledger + EAB-3 partition-promotion ledger.
- CIF is entry #1 per §13.3 verbatim.

**TQ §7 Part B (production critic · same three tiers second domain):**
- Tier 1: statistical tripwires per batch (empty-output rates · distribution shifts vs census baseline · confidence-profile anomalies) · zero serving-path cost.
- Tier 2: production critic reviews SAMPLE of outputs (initial DEFAULT: 1% of production volume OR 100 items/class/period, whichever is smaller).
- Tier 3: matrix stratified human samples double as calibration (staleness-marked · findings render UNCALIBRATED past window).
- QA-7 custody boundary (RULED): protection quality escalates as governance (fail-closed per-batch quarantine); utility-class findings never block.

**Post-amendment canon reconciliation (per Owner ITEM 2 close discipline):**

| Amendment | Contact with Critic-pass scope | Verdict |
|---|---|---|
| **A1 · Use Data Module** | A1.5 role gating: Model Acceptance + A2 hold-resolution are approver/DPO surfaces. Critic-pass Tier-2 findings feed Estate view (A4.1) but are non-blocking (QA-1) — never touch Commission card admissibility (A2.2 is machine-checked). | **NO CONFLICT** |
| **A2 · Approval Inversion** | A2.2 admissibility gate is fail-closed, machine-checked at Commission card. Critic-pass Tier-2 verdicts are asynchronous, post-landing, non-blocking (QA-1 verbatim). Verdicts FEED enforcement counts via Northena ledger; are ORTHOGONAL to A2.2 refuse-at-card discipline. QA-7 custody boundary (protection breach → per-batch quarantine fail-closed) reuses the EAB-2 quarantine machinery already landed at `backend/services/service_1/batch_quarantine.py` (SHA `eaed941246aa422ded81bc506f2f2c876316fd93f5cd0f6cd4fbfb66d37a7aed`). | **NO CONFLICT** — QA-7 rides existing A4 quarantine machinery |
| **A3 · Rules Taxonomy** | Critic-pass parameters classified per A3.4 in §4/§5.5. QA-1..QA-6 behavioral rules = Rails (S). Sampling rates + thresholds = Rules (O) OR Engine settings (E) (§4 disclosure per parameter). Seeded-defect corpus = Registries (D). CR-1..CR-7 rubric items = Rails (S). CIF manifest schema fields = Rails (S) at format-gate discipline. | **CLASSIFIED per A3.4** (see §4/§5.5) |
| **A4 · Govern Module** | A4.1 Estate view shows all four classes with enforcement counts. Critic-pass verdicts feed enforcement/violation counts via Northena ledger (per CIF §12 line 154 · same discipline). | **CONFORMS** |
| **A5 · Connect Module** | A5.1 seventh rule + A5.2 Class D registries. Critic-pass does not touch Connect surfaces. | **NO CONFLICT** |
| **A6 · Prove Module (cross-reference only)** | A6 already-landed at Prove Step 4 amendment. Critic-pass does not touch Prove surfaces (DB-1 + DB-2 preserved for Prove module phase Lane 2b · early landing = D-5 defect). | **NO CONFLICT** |
| **A7 · User Stories Delta** | No Critic-pass user-story surface. | **NO CONFLICT** |
| **A8 · Cross-Cutting** | A8.1 reference-artifact discipline: prototype + design brief consumed as NOTHING. A8.4 EAB-3 §5.5 defaults classified as Class E per A3.4. Critic-pass §5.5 defaults ALSO classified per A3.4 (§4/§5.5). | **CONFORMS** |

**Zero HAZARD-STOP surfaced.** Every post-amendment contact reconciles without conflict.

**Explicitly out of scope (fences):**
- G-13 · Registry Doctrine §8.1 additive-surface completion (Commercial Thesis Owner-side per Change Order) — separate phase.
- UI-1 (Extraction Console → Use Data Console post-A1 rename) — separate phase.
- UI-2 (Integration Console + S1 memory plane) — separate phase.
- Any Lane 2b module scope.
- Any Lane 1 GPU scope · model acquisition.
- **DB-1 + DB-2** (from Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` §4) — Prove-module-phase items · early landing at Critic-pass = D-5 cross-phase leakage defect. Explicitly OUT.
- **Owner-side Tier-3 sampling ceremonies** — builder lands the calibration-ledger + seeded-defect audit scaffold; builder does NOT execute the sampling ceremonies (§7 Tier-3 verbatim: *"The Owner's reviewing role compresses; it does not disappear."*).
- Frontend prototype + design brief (A8.1 reference-artifact discipline · consume as NOTHING).

**Parity fence:** Parity 33 held byte-identical this Stage A. Builder Tier-3 analysis at §5.1 recommends **NO Parity 33→34 seal at Critic-pass execution atomic** (CIF manifest schema lands as document-frontmatter format-gate + additive fields on existing artifact contracts where required, not a new frozen contract). If Owner rules otherwise at §5.1, a Parity 33→34 seal executes then.

---

## §2 · Band (Governance §9 · raw LoC verdict-unit · §4.2 split-threshold citation · §6 rate ledger applied)

Per `docs/governance/tiered_ruling_model.md` §9 (raw LoC verdict-unit ruling) and §2.1 / §4.2 (pre-authorized split threshold: 1,500 LoC / 60 cells · Tier 2 · disclosure-not-blocking). Rate ledger applied per §6.1–§6.11.

**Every LoC figure · cell-count figure · band figure below carries the Owner-mandated verbatim tag** (Owner Configuration Dispatch §4.STEP-5 + Owner HAZARD-STOP ruling §5.5 + Owner CRITIC-PASS STAGE A confirmation alignment): **"Provisional planning anchor — not a commitment. Relative weight only."** No exceptions. This tag applies verbatim to every LoC-low, LoC-high, band-total, and cell-count cell in the table below (row-level and total-level), and to the split-threshold total, and to any derived aggregate figure.

| Component | LoC low | LoC high | Rate ledger row |
|---|---:|---:|---|
| Tier-1 RV-1..RV-6 check-family cells (6 cells extending format-gate substrate at submission boundaries) | 100 | 160 | §6.10 · AST/reflection gate class ~40 LoC/cell × amortized |
| Tier-2 harness · critic-pass service (`backend/services/critic_pass/`) · CR-1..CR-7 rubric applier (7 rubric items · context-isolation independence rule per §6.2) | 180 | 280 | §6.3 · backend service module 100 LoC/module × sub-modules |
| CR-7 CIF selection-defect checklist (Owner-verbatim coach-correction-history · replay-only · known-pattern-check labeling) | 60 | 100 | §6.3 partial · piggybacks Tier-2 harness |
| CIF manifest schema · document-frontmatter validator (Stage A + close report submission boundaries + plan-object + training-run record + acceptance-verdict envelopes) | 100 | 150 | §6.10 · reflection gate class ~40 LoC/cell |
| CIF manifest schema · additive `manifest_entries: List[ManifestEntry]` on plan-object + training-run + acceptance-verdict contracts (**if** additive path selected at §5.1 · else E1 seal event lands at Parity 33→34) | 60 | 120 | §6.6 · frozen contract additive 60 LoC/cls (bounded on §5.1 ruling posture) |
| Archive ledger (rides existing Northena append-only ledger · CIF entry #1 seed row · standing-query for evaluated-but-unarchived) | 60 | 100 | §6.3 partial |
| Tier-3 calibration-ledger machinery + seeded-defect audit scaffold (Owner-side execution; builder lands machinery only) | 80 | 140 | §6.3 backend service module |
| TQ §7 Part B production-critic sampling scaffold (Tier 1 statistical tripwires per batch + Tier 2 sample-selection primitive + QA-7 custody-boundary handoff to EAB-2 quarantine machinery) | 100 | 160 | §6.3 backend service module |
| Pytest cells (RV-1..RV-6 substrate + CR-1..CR-7 rubric-item cells + QA-1 detect-never-decide attest + QA-2 format-gate attest + QA-3 no-self-review attest + QA-4 finding-honesty-grammar attest + QA-5 layer-pays-rent attest + QA-6 frame-authority-untouchable attest + QA-7 custody-boundary attest + CIF manifest schema format-gate attest + archive-ledger append-only attest + calibration-ledger-staleness attest + seeded-defect-audit scaffold attest + A3.4 classification attest + post-amendment reconciliation attest) | 200 | 320 | §6.1 · 12 LoC/cell · ~20 cells (Tier-1 + Tier-2 + QA-1..QA-7 + CIF + calibration) |
| §6.9 verbatim-carrier overhead (CR rubric text carried in critic-pass module + QA-1..QA-7 discipline text carried in harness module + §6.2 independence + §7 sampling text) | 60 | 100 | §6.9 · verbatim-carrier ~100-150 LoC/carrier partial |
| §6.10 AST/reflection gate class (Parity 33 attest cell + AST negative-scan on CR-7 checklist consumer / producer separation + Change Order A3.4 classification attest cell) | 60 | 100 | §6.10 · AST/reflection gate ~40 LoC/cell × 2-3 cells |
| Contract touch (**Parity 33 held byte-identical THIS STAGE A**; Parity 33→34 seal event contingent on §5.1 Tier-1 ruling) | 0 | 0 | Parity 33 baseline; +1 (`CIFManifest@v0`) at execution ONLY IF Owner rules Tier-1 E1 posture (a2) · otherwise Parity 33 held |

**Total band estimate: raw LoC `[low=1,000, high=1,730]`.**

**Cell count estimate: `[low=20, high=25]`.**

**Provisional planning anchor — not a commitment. Relative weight only.**

**§2.1/§4.2 split-threshold disclosure:** governance threshold is **1,500 LoC / 60 cells** (`docs/governance/tiered_ruling_model.md` §2.1 verbatim). If total execution LoC exceeds 1,500 raw LoC OR total cell count exceeds 60 cells at execution time, the seam splits as **commit A = Tier-1 + Tier-2 + CR-7 + CIF manifest schema** (harness + rubric + schema landing) and **commit B = archive ledger + Tier-3 calibration scaffold + TQ §7 Part B production-critic scaffold** (operational machinery against sealed harness). NO Owner ruling required unless threshold hits at execution time (§4.2 · disclosure-not-blocking · Tier 2). Rationale: commit A lands the load-bearing harness + rubric + schema; commit B lands the operational machinery against the sealed harness. **Provisional planning anchor — not a commitment. Relative weight only.**

---

## §3 · Registry v1 citations (D-11 canon-before-attest)

Every fold cites `docs/registry/function_promise_registry_v1.md` (SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`) as active source.

**Aggregate citation count in this Stage A: 10 distinct v1.md rows** cited across §4 folds + §5 escalations + §6 sidecar enumeration:

1. `PROM-S1-frozen-wire-contract` — CIF manifest schema (format-gate structural invariance) + potential Tier-1 E1 landing
2. `PROM-S1-additive-versioning` — CIF manifest additive fields on existing artifact contracts (if additive path selected)
3. `PROM-S1-honesty-grammar-source-labels` — CR-2 anti-fabrication + QA-4 finding-honesty-grammar
4. `PROM-S1-refusal-taxonomy-closed` — QA-1 detect-never-decide (findings never emit refusals · orthogonal to refusal envelope)
5. `PROM-S3-append-only-ledger` — archive ledger (CIF §12 line 154 · rides existing Northena ledger)
6. `PROM-S3-audit-trail-immutable` — calibration ledger + archive ledger immutability
7. `PROM-S3-frozen-contract-parity-attest` — Parity 33 attest cell (held byte-identical this atomic)
8. `PROM-S3-mechanical-audit-of-promotion` — CR-6 self-audit-audit (mechanical audit precedent extended from container/partition promotion to self-audit-table verification)
9. `akki.instance.seams_scoped_by_instance_id` (v1 §S1) — Critic-pass per-instance calibration ledger (MC-E2 α reflexive discipline extended)
10. §14 sidecar pattern (v1 §M · G-2 R4 reflexive-rows precedent + EAB-1/EAB-2/EAB-3 sidecar precedents) — Critic-pass sidecar filing

---

## §4 · Fold enumeration · row-by-row (each fold FACT/NORM/DEFAULT-classed per Op. Values §7 + Class S/O/E/D-classified per A3.4)

### §4.A · Tier-1 RV-1..RV-6 folds (§5 Critic Seam v1.0)

- **RV-1 · assertion-boundary trace** — **FACT-class · Class S (Rails)** — every claim resolves to a citation or is marked recalled/inferred with the class visible. Registry: `PROM-S1-honesty-grammar-source-labels`.
- **RV-2 · scope-anchor trace** — **FACT-class · Class S (Rails)** — proposals cite the dispatched anchor § or line. Registry: `PROM-S1-frozen-wire-contract` (structural invariance).
- **RV-3 · registry attribution** — **FACT-class · Class S (Rails)** — every fold cites a v1.md row. Registry: `PROM-S1-frozen-wire-contract`.
- **RV-4 · schema-completeness (QA-2 hard gate)** — **FACT-class · Class S (Rails)** — Stage As carry band + derivation + pre-tiered escalations + R4 rows + D-10 self-audit table; closes carry gate roster + artifact SHAs + R4/negative attest + D-10 table. Missing sections reject at submission (QA-2 hard gate · form only). Registry: `PROM-S1-frozen-wire-contract`.
- **RV-5 · Standing Rule v3 predecessor byte-identity attest** — **FACT-class · Class S (Rails)** — every landing verifies predecessor byte-identity via `git diff HEAD`. Registry: `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning`.
- **RV-6 · Parity attest** — **FACT-class · Class S (Rails)** — contract count + snapshot count == EXPECTED_PARITY. Registry: `PROM-S3-frozen-contract-parity-attest`.

### §4.B · Tier-2 CR-1..CR-7 folds (§6 Critic Seam v1.0 + CIF §6 A5.2)

- **CR-1 · anti-re-derivation** — **NORM-class · Class S (Rails)** — critic receives Registry (machine form) + mandate documents' section inventory; answers semantically. Registry: `PROM-S1-frozen-wire-contract`.
- **CR-2 · anti-fabrication** — **NORM-class · Class S (Rails)** — no assertion stronger than evidence class permits · no recalled dressed as fact · no value without basis. Registry: `PROM-S1-honesty-grammar-source-labels`.
- **CR-3 · conflation test (D-3)** — **NORM-class · Class S (Rails)** — every proposed function traces to a named service sentence · trace real not decorative. Registry: `PROM-S1-frozen-wire-contract`.
- **CR-4 · scope semantics (D7)** — **NORM-class · Class S (Rails)** — beyond RV-2 mechanical trace · work's substance stays inside dispatch intent · sequencing not invented under cover · scope not smuggled as "riders". Registry: `PROM-S1-frozen-wire-contract`.
- **CR-5 · enforcement honesty (D-5)** — **NORM-class · Class S (Rails)** — no rule proposed whose only enforcement is prose · no gate claimed that no cell proves. Registry: `PROM-S3-mechanical-audit-of-promotion`.
- **CR-6 · self-audit audit** — **NORM-class · Class S (Rails)** — artifact's D-10 table's reasoning holds · no reflexive PASS-stamping. Registry: `PROM-S3-mechanical-audit-of-promotion`.
- **CR-7 · CIF selection-defect checklist** (per CIF A5.2 verbatim: *"enters standing machinery as a Critic Seam rubric amendment (CR-7)"*) — **NORM-class · Class S (Rails)** — Owner's coach-correction-history rubric · replay-only · labels output "known-pattern check" · never claims novelty coverage. Registry: `PROM-S1-honesty-grammar-source-labels`.

### §4.C · QA-1..QA-7 behavioral rule folds (§8 Critic Seam v1.0 + TQ §7 QA-7)

- **QA-1 · detect, never decide** — **FACT-class · Class S (Rails)** — no finding blocks execution, edits artifact, or gates phase; one scoped exception: QA-2. Registry: `PROM-S1-refusal-taxonomy-closed`.
- **QA-2 · the format gate** — **FACT-class · Class S (Rails)** — RV-4 schema-completeness is single hard gate; form never substance. Registry: `PROM-S1-frozen-wire-contract`.
- **QA-3 · no self-review** — **FACT-class · Class S (Rails)** — critic instance ≠ produced instance; context isolation measured by seeded audits. Registry: `PROM-S1-frozen-wire-contract`.
- **QA-4 · findings carry honesty grammar** — **FACT-class · Class S (Rails)** — every finding evidence-classed and cited. Registry: `PROM-S1-honesty-grammar-source-labels`.
- **QA-5 · the layer pays rent** — **FACT-class · Class S (Rails)** — catch/false-alarm ledger standing; no critic-of-the-critic. Registry: `PROM-S3-audit-trail-immutable`.
- **QA-6 · frame authority is untouchable** — **FACT-class · Class S (Rails)** — no check disputes Owner ruling · service sentence · frame decision. Registry: `PROM-S1-frozen-wire-contract`.
- **QA-7 · custody boundary (RULED · TQ §7 line 125)** — **FACT-class · Class S (Rails)** — protection quality escalates as governance (fail-closed per-batch quarantine); utility-class findings never block. Rides EAB-2 quarantine machinery at `backend/services/service_1/batch_quarantine.py`. Registry: `PROM-S3-audit-trail-immutable`.

### §4.D · CIF manifest schema folds (§12 line 152)

- **A.CIF.1 · manifest schema-required fields on Stage-A proposals + close reports** — **FACT-class · Class S (Rails)** — document-frontmatter format-gate at submission (QA-2-precedent · form only). Registry: `PROM-S1-frozen-wire-contract`.
- **A.CIF.2 · manifest schema-required fields on plan objects + training-run records + acceptance verdicts** — **FACT-class · Class S (Rails)** — additive Pydantic fields on existing artifact envelopes (if §5.1 (a1) selected · builder Tier-3 recommendation) OR new frozen contract `CIFManifest@v0` at Parity 33→34 seal (if §5.1 (a2) selected · Owner ruling required). Registry: `PROM-S1-additive-versioning` (a1 path) OR `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` (a2 path).
- **A.CIF.3 · manifest evidence-class enum** — **FACT-class · Class S (Rails)** — `Literal["fact", "recalled", "inferred"]` per §4 Definitions verbatim. Registry: `PROM-S1-honesty-grammar-source-labels`.
- **A.CIF.4 · flip condition per manifest entry** — **FACT-class · Class S (Rails)** — per §4 Definitions verbatim: *"the counterfactual probe: what, if false, flips this?"*. Registry: `PROM-S1-honesty-grammar-source-labels`.

### §4.E · Archive ledger folds (§12 line 154 + §14.2)

- **A.ARC.1 · append-only ledger entry per evaluated idea** — **FACT-class · Class S (Rails)** — rides existing Northena ledger machinery. Registry: `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable`.
- **A.ARC.2 · CIF as entry #1** — **FACT-class · Class S (Rails)** — per §13.3 verbatim + §14.2 verbatim: *"The archive initializes as a governed file with CIF as entry #1"*. Seed row landed at execution atomic. Registry: `PROM-S3-append-only-ledger`.
- **A.ARC.3 · standing query for evaluated-but-unarchived findings** — **FACT-class · Class S (Rails)** — CIF §12 verbatim: *"a standing query surfaces evaluated-but-unarchived ideas as findings"*. Registry: `PROM-S3-audit-trail-immutable`.

### §4.F · Tier-3 calibration folds (§7 Critic Seam v1.0 · Owner-side sampling · builder lands machinery)

- **A.CAL.1 · calibration ledger with staleness field** — **FACT-class · Class E (Engine settings)** — staleness window 10 phases DEFAULT · per-worker-class + per-rubric-item + versioned. Registry: `PROM-S3-audit-trail-immutable`.
- **A.CAL.2 · seeded-defect audit scaffold** — **NORM-class · Class D (Registries · seeded-defect corpus is a governed reference registry)** — cadence 1/5 phases DEFAULT · drawn across fall classes · never in landing artifacts. Registry: `PROM-S3-retention-held-class-no-delete`.
- **A.CAL.3 · verdict sampling scaffold** — **DEFAULT-class · Class O (Rules)** — 20% findings + 10% all-clears sampling rate DEFAULT · decays as measured reliability accumulates · **Owner-side execution ceremony** (builder lands scaffold only). Registry: `PROM-S3-audit-trail-immutable`.

### §4.G · TQ §7 Part B production-critic folds

- **A.TQ7.1 · Tier-1 statistical tripwires per batch** — **NORM-class · Class E (Engine settings)** — empty-output rates · distribution shifts vs census baseline · confidence-profile anomalies · zero serving-path cost. Registry: `PROM-S1-frozen-wire-contract`.
- **A.TQ7.2 · Tier-2 sample selection primitive** — **DEFAULT-class · Class E (Engine settings)** — 1% of production volume OR 100 items/class/period DEFAULT · initial. Registry: `PROM-S1-frozen-wire-contract`.
- **A.TQ7.3 · QA-7 custody boundary · protection → quarantine · utility → findings** — **FACT-class · Class S (Rails)** — rides EAB-2 quarantine machinery (`batch_quarantine.py`). Registry: `PROM-S3-audit-trail-immutable`.

### §4.H · A3.4 classification tally (Owner ITEM 1 forward-binding annotation applied)

| Fold family | Class per A3.4 | Count |
|---|---|---:|
| §4.A RV-1..RV-6 | S · Rails | 6 |
| §4.B CR-1..CR-7 | S · Rails | 7 |
| §4.C QA-1..QA-7 | S · Rails | 7 |
| §4.D CIF manifest schema | S · Rails | 4 |
| §4.E Archive ledger | S · Rails | 3 |
| §4.F Tier-3 calibration · staleness window | E · Engine settings | 1 |
| §4.F Tier-3 calibration · seeded-defect corpus | D · Registries | 1 |
| §4.F Tier-3 calibration · verdict sampling rate | O · Rules | 1 |
| §4.G TQ §7 Part B · statistical tripwire thresholds | E · Engine settings | 1 |
| §4.G TQ §7 Part B · sample selection rate | E · Engine settings | 1 |
| §4.G TQ §7 Part B · QA-7 custody boundary | S · Rails | 1 |
| **TOTAL** | | **33** |

**33 folds classified per A3.4** (27 Rails · 3 Engine settings · 1 Rules · 1 Registries · 1 additional Rails-boundary for QA-7). Class E parameters (staleness window · tripwire thresholds · sample selection rate) pinned per engine version · runtime tunability requires E→O promotion per A3.2 · no other route (Owner ITEM 1 forward-binding annotation applied verbatim).

---

## §5 · Tier-1 escalation surfaces (pre-named)

### §5.1 · E1 · CIF manifest schema landing shape · **Tier-1** (Parity 33→34 seal contingent on Owner ruling)

**Surface:** CIF §12 line 152 verbatim: *"Manifests: schema-required fields on every verdict-bearing artifact (Stage As, close reports, plan objects, training-run records, acceptance verdicts); an unmanifested verdict rejects at submission — the standing format-gate pattern, form only."*

Verdict-bearing artifacts span two classes: (i) markdown documents (Stage-A proposals · close reports) and (ii) on-disk Pydantic-contract records (plan objects at `backend/contracts/targeta_plan.py` · training-run records · acceptance verdicts). The markdown-document path is uncontested (document-frontmatter format-gate cell at submission · no frozen contract touch). The Pydantic-record path is the Tier-1 escalation.

**Builder analysis (does NOT resolve):** three structurally distinct posture options exist and Owner rules.

**Owner ruling surface:**

- **(a1) Additive fields on existing frozen contracts** — extend `targeta_plan.py` + training-run records + acceptance-verdict envelopes with `manifest_entries: List[ManifestEntry]` where `ManifestEntry` is a **shared additive substructure** (declared inline OR imported from a shared module):
  - Byte-level: `+ manifest_entries: List[ManifestEntry] = Field(default_factory=list, description="CIF §12 schema-required verdict manifest · load-bearing assumptions evidence-classed · unmanifested verdict rejects at submission")`. `ManifestEntry(assumption_text: str, evidence_class: Literal["fact","recalled","inferred"], flip_condition: str)` sub-dataclass.
  - Parity 32→33 seal impact: **PROCEEDS UNBLOCKED** (additive-versioning per `PROM-S1-additive-versioning` · zero mutation of existing 33 contracts · zero Parity seal event).
  - Standing Rule v3 impact: PRESERVED (additive · no byte contact with prior 33 contracts).
  - Trade-off: shared additive substructure across multiple contracts couples the substructure's schema evolution to every consumer.
  - Precedent alignment: matches EAB-2 A3 additive-4-tuple posture on `Service1Refusal_v1` (Owner ruled additive · not new-contract).

- **(a2) New frozen contract `CIFManifest@v0`** at `backend/contracts/cif_manifest.py` + snapshot at `backend/tests/invariants/cif_manifest_v0.contract_snapshot.json` · Parity 33→34 seal · single-contract carrier of the manifest schema referenced by FK from plan-object + training-run + acceptance-verdict contracts:
  - Byte-level: new frozen contract with fields `verdict_id: str · manifest_entries: List[ManifestEntry] · verdict_type: Literal["stage_a", "close_report", "plan_object", "training_run", "acceptance_verdict"] · authored_at: str · instance_id: str`. Existing artifact contracts add `manifest_ref: str` FK to `CIFManifest@v0` records.
  - Parity 33→34 seal impact: SEAL EXECUTES (V1-G7 assertion set bumps 33→34).
  - Standing Rule v3 impact: PRESERVED (both additive · new contract + FK additive fields).
  - Trade-off: cleaner separation of manifest from verdict-bearing envelope; but heavier ceremony (Parity seal event) + additional runtime read at manifest resolution.
  - Precedent alignment: matches EAB-3 (a1) posture single-contract landing pattern for a NEW artifact class.

- **(b) Extend an existing frozen envelope in place** (e.g., in-place mutate `targeta_plan.py` to add `manifest_entries` field with byte contact to existing 33 contracts):
  - Byte-level: existing frozen envelope's field list mutates in place; no new contract; no additive-versioning ceremony; existing 33 contract SHAs change.
  - Parity 33→34 seal impact: NO seal event (in-place mutation, not a new contract).
  - **Standing Rule v3 impact: WOULD VIOLATE** — `PROM-S1-frozen-wire-contract` requires structural invariance of already-landed frozen wire contracts; `PROM-S1-additive-versioning` requires additive versioning (v0→v1) for schema extension, NOT in-place mutation. Byte contact to any of the 33 already-landed frozen contract files breaks Standing Rule v3's "protected artifacts remain byte-identical" invariant.
  - Trade-off: none live — this posture is a Standing Rule v3 violation at pre-name.
  - Precedent alignment: none — no phase has ever in-place-mutated a landed frozen contract; EAB-2 A3 additive-4-tuple + EAB-3 (a1) landing both use additive-versioning, not in-place mutation.
  - **REJECTED at pre-name by Standing Rule v3.** Named to complete enumeration.

- **(c) Sidecar telemetry only** (manifest lives in `PROM-S1-runtime-transient-never-refusal` sidecar or unfrozen dict on non-frozen scratch/telemetry path):
  - Byte-level: no contract touch; manifest entries stored as transient JSON blob or Python dict on a scratch path not part of the frozen wire.
  - Parity 33→34 seal impact: NO seal event (no contract touch).
  - **Standing Rule v3 impact: WOULD PRESERVE the 33 contract byte-identity** (no contract touch) BUT would VIOLATE the schema-required + fail-closed discipline mandated by CIF §12 line 152 verbatim ("*schema-required fields on every verdict-bearing artifact*" + "*unmanifested verdict rejects at submission — the standing format-gate pattern, form only*"). Sidecar telemetry is transient/non-blocking by definition per `PROM-S1-runtime-transient-never-refusal`; a schema-required + fail-closed field cannot ride a transient/non-blocking substrate.
  - Trade-off: none live — this posture violates CIF §12 line 152 verbatim requirement (schema-required + format-gate cannot be carried by transient/non-blocking sidecar).
  - Precedent alignment: none — sidecar telemetry per AF-E3 α + AF-E4 α precedent covers non-verdict-bearing latency/timing telemetry, NOT verdict-bearing schema-required fields.
  - **REJECTED at pre-name by CIF §12 line 152 verbatim.** Named to complete enumeration.

**Builder Tier-3 recommendation: (a1)** — additive fields on existing frozen contracts. Rationale:
1. Additive-versioning simplicity: each verdict-bearing artifact contract adds a `manifest_entries` field; no new frozen contract; no Parity seal ceremony this atomic; Parity 33 held byte-identical.
2. Precedent alignment with EAB-2 A3 (Owner ruled additive-4-tuple on `Service1Refusal_v1` · not a new contract with FK).
3. D-6-cleanest linear-additive progression: Parity 31→32 (EAB-2) → Parity 32→33 (EAB-3) → **Parity 33 held** (Critic-pass) → future phase seal if needed.
4. Lower runtime overhead: manifest is co-located with verdict envelope · zero additional read at manifest resolution.
5. **The primary contact surface is markdown documents** (Stage A + close report + ruling-authority documents) which are already-plain-text and lean on document-frontmatter format-gate at submission · not Pydantic contracts.

**Fence carried into this Stage A:** if Owner rules (a1), Parity 33 held byte-identical this atomic and at execution. If Owner rules (a2), Parity 33→34 seal executes at Critic-pass execution atomic. Zero contract file created this Stage A.

### §5.2 · E2 · Archive ledger contract shape · (downgrade to no-live-ruling-surface · disclosed)

**Surface:** CIF §12 line 154 verbatim: *"Archive: entries as append-only ledger rows; a standing query surfaces evaluated-but-unarchived ideas as findings."*

**Builder analysis (resolves at Tier-3 authority):** Archive ledger rides existing Northena ledger machinery via `PROM-S3-append-only-ledger` — same discipline as EAB-2 batch-quarantine ledger + EAB-3 partition-promotion ledger (both landed with in-memory ledger row dataclasses inside their respective service modules · not new frozen contracts). Archive ledger row is a dataclass at `backend/services/critic_pass/archive.py::ArchiveLedgerRow` — no new frozen Pydantic contract required.

**Downgrade rationale (D-11 read):** `PROM-S3-append-only-ledger` covers this exact pattern; CIF §12 line 154 says "entries as append-only ledger rows" — rides existing ledger with new row-type discriminator. Precedent alignment with EAB-2 `QuarantineEvent` + EAB-3 `PartitionPromotionLedgerRow` dataclass pattern.

Disclosed as pre-named per §IX-analog; downgraded on evidence (dataclass posture is builder Tier-3-cleanest · no ruling required).

### §5.3 · E3 · CR-7 checklist landing shape · (downgrade to no-live-ruling-surface · disclosed)

**Surface:** CIF §6 A5.2 verbatim: *"It enters standing machinery as a Critic Seam rubric amendment (CR-7)."*

**Builder analysis (resolves at Tier-3 authority):** CR-7 is a Tier-2 rubric-item amendment · lands alongside CR-1..CR-6 as an executable rubric cell in `backend/services/critic_pass/rubric.py` (or module of that shape) · not a menu option · one live posture: extend the Tier-2 rubric with CR-7 as the 7th rubric item.

**Downgrade rationale (D-11 read):** CIF A5.2 verbatim mandates the discipline · builder implements as executable rubric cell alongside CR-1..CR-6 · no ruling required · no alternative postures.

Disclosed as pre-named per Critic-pass mechanics; downgraded on evidence.

### §5.4 · E4 · Tier-3 sampling ceremony authority · (downgrade to Owner-side scope · disclosed)

**Surface:** Critic Seam v1.0 §7 verbatim (Tier-3 human calibration sampling): *"The Owner's reviewing role compresses; it does not disappear."*

**Builder analysis (resolves at Tier-3 authority):** Builder lands the calibration-ledger machinery + seeded-defect audit scaffold; Owner executes the sampling ceremonies (verdict sampling ceremony · seeded-defect audit ceremony · calibration-number-versioning ceremony). Fence: **no builder-driven "verdict sample" this atomic** — builder Tier-3 recognizes this as Owner-side scope.

**Downgrade rationale (D-11 read):** Critic Seam v1.0 §7 verbatim reserves Tier-3 for Owner-side execution. Sampling parameters (20% findings · 10% all-clears · 1/5 phases seeded audit cadence · 10-phase staleness window) are DEFAULT-class per Op. Values §7 discipline · versioned like model calibration. Builder lands machinery only.

Disclosed as pre-named per §IX-analog; downgraded on evidence (Owner-side scope discipline · Lane 1 parallel).

### §5.5 · Tier-3 remainder — Rules Taxonomy classification lens (DEFAULT-class builder-Tier-3 decisions disclosed · S/O/E/D per A3.4 · Owner ITEM 1 forward-binding annotation applied)

Per Owner ITEM 1 forward-binding annotation verbatim (from EAB-3 E1 ruling): *"all five §5.5 defaults are Class E engine parameters under the Rules Taxonomy filed at ITEM 2 (A3.4) — pinned per engine version, changed only via version bumps with evaluation verdicts; any future runtime tunability takes the E→O promotion path (A3.2), no other route."*

Owner alignment (this Stage A): the **Rules Taxonomy classification table** lands here at §5.5 as the parameter classification lens — every parameter row cites the A3.4 register entry it maps to.

**Critic-pass parameter classification table (S/O/E/D per A3.4 · one row per DEFAULT-class parameter):**

| # | Parameter | Source (verbatim) | Class per A3.4 | A3.4 register entry citation | Runtime-tunability path | Note |
|---:|---|---|:---:|---|---|---|
| 1 | Calibration ledger staleness window (DEFAULT 10 phases · findings render UNCALIBRATED past window) | Critic Seam v1.0 §9 | **E** · Engine settings | A3.4 verbatim: *"Engine settings (E): dedupe fingerprint distance · VAD threshold · batch windows · sample-rate/window constants · EAB-3 §5.5 defaults (partition-shape enum · refresh cadence · eviction policy · latency-telemetry storage · AC-A5.b latency budget)"* — Critic-pass staleness window is a **window constant** in the same class as EAB-3 §5.5 defaults (Owner ITEM 1 forward-binding applied identically) | E→O promotion via A3.2 (proposal-gated · one-way per event · engine owner files promotion note · parameter enters Class O via spec amendment · leaves engine-pinned config at next engine version bump) | Pinned per engine version · findings render UNCALIBRATED past window per Critic Seam v1.0 §9 verbatim |
| 2 | Verdict sampling rate DEFAULT (20% findings · 10% all-clears · decays as measured reliability accumulates) | Critic Seam v1.0 §7 | **E** · Engine settings | A3.4 verbatim: *"sample-rate/window constants"* — verdict sampling rate is a **sample-rate constant** directly named in A3.4 Engine-settings class | E→O promotion via A3.2 (builder Tier-3 disclosure at §5.5 recommendation note below: this is a plausible early-E→O-promotion candidate; ceremony NOT this atomic) | Pinned per engine version · initially Class E per Owner ITEM 1 forward-binding · A3.2 promotion required for runtime tunability |
| 3 | Seeded-defect audit cadence DEFAULT (1/5 phases · drawn across fall classes · never in landing artifacts) | Critic Seam v1.0 §7 | **E** · Engine settings | A3.4 verbatim: *"sample-rate/window constants"* — audit cadence is a **window constant** (phase interval) in Engine-settings class | E→O promotion via A3.2 | Pinned per engine version · seeded-defect corpus itself is separately Class D (row 8 below) |
| 4 | Critic catch-rate target DEFAULT (≥80% on seeded defects across fall classes · DEFAULT · revised on evidence) | Critic Seam v1.0 §9 | **E** · Engine settings | A3.4 verbatim: *"EAB-3 §5.5 defaults"* class-equivalence — catch-rate target is a **performance-threshold constant** in same Engine-settings class as EAB-3 §5.5 defaults per Owner ITEM 1 forward-binding | E→O promotion via A3.2 (revision ceremony rides F-class seam-value dual-control precedent) | Pinned per engine version · breach triggers governance ceremony not runtime edit |
| 5 | Critic false-alarm rate DEFAULT (≤20% of findings ruled non-findings · DEFAULT · breach triggers rubric review) | Critic Seam v1.0 §9 | **E** · Engine settings | A3.4 verbatim: *"EAB-3 §5.5 defaults"* class-equivalence — false-alarm rate is a **performance-threshold constant** in same Engine-settings class per Owner ITEM 1 forward-binding | E→O promotion via A3.2 (rubric-review triggered by breach is governance ceremony · not runtime edit) | Pinned per engine version · breach → rubric review (governance) |
| 6 | TQ §7 Part B sample selection rate DEFAULT (1% of production volume OR 100 items/class/period whichever is smaller) | TQ v1.0 §7 line 121 | **E** · Engine settings | A3.4 verbatim: *"sample-rate/window constants"* — production-critic sample-selection rate is a **sample-rate constant** directly named in A3.4 Engine-settings class | E→O promotion via A3.2 | Pinned per engine version · initial DEFAULT per TQ §7 line 121 verbatim |
| 7 | TQ §7 Part B statistical tripwire thresholds (empty-output rate + distribution-shift + confidence-profile threshold constants · unspecified numeric DEFAULT · authored at execution time) | TQ v1.0 §7 line 117-119 | **E** · Engine settings | A3.4 verbatim: *"EAB-3 §5.5 defaults"* class-equivalence — tripwire thresholds are **performance-threshold constants** in same Engine-settings class per Owner ITEM 1 forward-binding | E→O promotion via A3.2 | Pinned per engine version · numeric DEFAULT authored at execution atomic |
| 8 | Seeded-defect corpus (governed reference registry · drawn across fall classes · versioned) | Critic Seam v1.0 §7 | **D** · Registries | A3.4 verbatim: *"Registries (D): shield-against/pseudonymization registry · protected-terms lists · DPO extraction filter lists"* — seeded-defect corpus is a **governed reference registry** in the same class as protected-terms lists (schema defined once · Class E rule references registry by version · A3.3 lifecycle: upload → validation → diff view → confirm → versioned/receipted/effective-from · additions immediate · removals+edits gated) | A3.3 lifecycle (Class D governance ceremony · not E→O · Class D is not runtime-tunable per its own definition) | Corpus versioned; Class E rows 2/3 reference this registry by version |

**Additional Class-S/O rows already-classified at §4.H tally (referenced here for the S/O/E/D lens completeness · not re-tabulated):**

| Class | Count in §4.H tally | Nature |
|:---:|---:|---|
| **S** · Rails | 28 | RV-1..RV-6 (6) + CR-1..CR-7 (7) + QA-1..QA-7 (7) + CIF manifest schema folds (4) + Archive-ledger folds (3) + QA-7 Rails-boundary (1 · already inside QA count) — every rail bound by hard-fail cell at execution atomic (A3.1 verbatim: *"a rail without a hard-fail cell does not exist"*) |
| **O** · Rules | 1 | Verdict sampling rate — **initially Class E per Owner ITEM 1 forward-binding** (row 2 above); disclosed as future O-promotion candidate only. No Class O rule lives in Critic-pass at Stage A landing. |
| **E** · Engine settings | 7 | Rows 1-7 above (staleness window · verdict sampling rate · seeded-defect audit cadence · catch-rate target · false-alarm rate · TQ §7 Part B sample rate · TQ §7 Part B tripwire thresholds) |
| **D** · Registries | 1 | Seeded-defect corpus (row 8 above) |
| **TOTAL** | **36 parameters** | 28 S + 0 O (live) + 7 E + 1 D · Owner ITEM 1 forward-binding annotation applied identically to Critic-pass §5.5 defaults as to EAB-3 §5.5 defaults · verdict sampling rate is INITIALLY Class E · disclosed only as future O-promotion candidate |

**Builder Tier-3 recommendation note (disclosed at close · non-binding):** the sampling-rate parameter (row 2) is a plausible early-E→O-promotion candidate — the Owner may want to tune sampling rates operationally without engine version bumps as measured reliability accumulates (Critic Seam v1.0 §7 verbatim: *"decays as measured reliability accumulates"* implies operational tuning surface). Disclosed for Owner awareness only; **E→O promotion executes per A3.2 ceremony** (not this atomic · Critic-pass Stage A carries no promotion motion · this Stage A lands the parameters at Class E per Owner ITEM 1 forward-binding).

**Reconciliation with §4.H tally (33 folds classified):** §4.H tallies **folds** (RV/CR/QA/CIF/Archive/Tier-3-calibration/TQ-Part-B). §5.5 tallies **parameters** (individual DEFAULT-class settings). Each Tier-3 calibration fold at §4.F expands to multiple parameters at §5.5 (e.g., §4.F A.CAL.1 staleness-window fold = §5.5 row 1 parameter; §4.F A.CAL.3 verdict-sampling fold = §5.5 row 2 parameter). The two tallies are lenses over the same substrate: §4.H is the fold-family lens, §5.5 is the parameter-classification lens per Owner alignment.

---

## §6 · R4 sidecar (enumerated only · NOT created this Stage A)

Per Registry Doctrine §5 v1-era pattern + Registry v1 §M G-2 R4 reflexive-rows precedent + EAB-1 sidecar precedent (13 rows) + EAB-2 sidecar precedent (14 rows) + EAB-3 sidecar precedent (15 rows + 1 reflexive).

**Proposed sidecar path:** `docs/registry/function_promise_registry_v1_critic_pass_sidecar.md`

**Row count proposed: 18 rows** (+ 1 reflexive-carrier at execution atomic · 19 total), all attaching to existing v1.md §2 promises via foreign-key resolution (**zero new promises minted** · conservation-not-authorship posture per §M):

| # | Proposed sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 1 | `akki.critic.rv1_assertion_boundary_trace_cell` | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 2 | `akki.critic.rv2_scope_anchor_trace_cell` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.critic.rv3_registry_attribution_cell` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 4 | `akki.critic.rv4_schema_completeness_hard_gate_qa2` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` (RV-4 = QA-2 hard gate) |
| 5 | `akki.critic.rv5_standing_rule_v3_predecessor_byte_identity` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 6 | `akki.critic.rv6_parity_attest` | 1 · Deterministic | `PROM-S3-frozen-contract-parity-attest` |
| 7 | `akki.critic.cr1_anti_re_derivation_rubric_cell` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 8 | `akki.critic.cr2_anti_fabrication_rubric_cell` | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 9 | `akki.critic.cr3_conflation_test_d3_rubric_cell` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 10 | `akki.critic.cr4_scope_semantics_d7_rubric_cell` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 11 | `akki.critic.cr5_enforcement_honesty_d5_rubric_cell` | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 12 | `akki.critic.cr6_self_audit_audit_rubric_cell` | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 13 | `akki.critic.cr7_cif_selection_defect_checklist_rubric_amendment` | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` (CIF A5.2 verbatim · CR-7 IS the rubric amendment) |
| 14 | `akki.critic.qa1_detect_never_decide_binding` | 1 · Deterministic | `PROM-S1-refusal-taxonomy-closed` |
| 15 | `akki.critic.qa7_custody_boundary_protection_governance_utility_findings` | 1 · Deterministic | `PROM-S3-audit-trail-immutable` (rides EAB-2 quarantine machinery) |
| 16 | `akki.critic.cif_manifest_schema_format_gate_at_submission` | 1 · Deterministic | `PROM-S1-frozen-wire-contract` (CIF §12 line 152 verbatim) |
| 17 | `akki.critic.archive_ledger_append_only_cif_entry_1_seed` | 1 · Deterministic | `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable` |
| 18 | `akki.critic.calibration_ledger_staleness_window_class_e` | 1 · Deterministic | `PROM-S3-audit-trail-immutable` (Class E per A3.4 · Owner ITEM 1 forward-binding) |

**Reflexive-sidecar-row placeholder:** the sidecar file itself will land as a 19th reflexive row at execution atomic per EAB-1/EAB-2/EAB-3 sidecar precedents (`akki.registry.critic_pass_sidecar_reflexive_row` · attaches to Registry v1 §M sidecar-pattern authority).

**Zero new promises minted** (conservation-not-authorship posture per Registry v1 §M).

**Sidecar file NOT created this Stage A** (per Owner-verbatim REPLY FORMAT §6 · "enumerated only · NOT created").

---

## §7 · D-7 fence attestation

Verdicts uncurated per D-7. QA-2 hard gate (RV-4 schema-completeness) and all Tier-1/Tier-2 cells resolve against on-disk repository state, not curated summary.

**No G-13 content:** Registry Doctrine §8.1 additive-surface completion (Commercial Thesis Owner-side) — G-13 scope.

**No UI-1 content:** Extraction Console → Use Data Console (per A1 rename) — UI-1 scope.

**No UI-2 content:** Integration Console + S1 memory plane — UI-2 scope.

**No Lane 2b module scope:** Connect · Registry · Use Data · Govern · Prove · Team · Shared Components module-phase execution — downstream of UI-1/UI-2.

**No Lane 1 GPU / model acquisition:** zero curl of model weights · zero perception model registry touch this atomic.

**No refusal-envelope contact:** EAB-2 sealed Service1Refusal@v1. QA-1 detect-never-decide preserves the boundary; Critic-pass findings NEVER emit as refusals (they emit as Northena ledger findings rows).

**No Targeta cap-seat contact:** Critic-pass reads from Northena ledger + verdict artifacts; NEVER writes to Targeta gate/yield_layer. AST negative-scan cell at execution atomic enforces at CI.

**No DB-1 · No DB-2:** Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` §4 preserves DB-1 + DB-2 for Prove-module-phase Lane 2b — early landing = D-5 defect. Explicitly OUT.

**No OD-8 / OD-9 / OD-10 contact:** D-11 verified this session — no Critic Seam / CIF / TQ mandate carries mail-provider · public-surface · scheduler-primitive content. Confirmed no HAZARD-STOP surface.

**No re-landing of prior Tier-1 surfaces:** F2 (G-3) · Service1Refusal@v0 (A2) · Service1Refusal@v1 (EAB-2) · PartitionSchema@v0 (EAB-3). Critic-pass consumes none.

**No re-surfacing of ruled items:** Loci 1/2/3 EAB-2 · Surfaces 1/2/3 STEP-2 · LT-1 · Canonical Name Register · Product Doc v3.1 · EAB-3 E1 · Change Order amendments A1..A8 — all closed FINAL.

**A8.1 reference-artifact discipline:** frontend prototype + UI-v3 design brief consumed as NOTHING per change-order A8.1 verbatim.

**Parity fence:** Parity 33 held byte-identical this Stage A (contingent on §5.1 posture (a1) at execution · if (a2) selected, Parity 33→34 executes at execution atomic).

**Governance-stack byte-identity:** §§1..23 sanctioned amendment blocks unchanged this atomic.

**Standing Rule v3:** all protected artifacts remain byte-identical — v0..v32 lineage + PartitionSchema@v0 (v33) + Owner rulings + all 7 amendment sibling files (A1/A2/A3/A4/A5/A7/A8) + Prove Step 4 amendment + all 4 predecessors (01_connect · 03_extract · 04_govern · 08_user_stories) byte-identical.

---

## §8 · D-10 self-audit table (D-1..D-12 · standing practice per QA-2)

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every fold in §4 traces to a Critic Seam v1.0 §5/§6/§7/§8 verbatim line + CIF §6/§12/§14 verbatim line + TQ §7 verbatim line + Registry v1 row citation. Every AC (Critic Seam §8 QA-1..QA-6 + TQ §7 QA-7) traces verbatim. |
| D-2 | NL-only claim | PASS | Every claim disk-verifiable (Critic Seam v1.0 SHA `110a0d0448f66f44` + v1.1 SHA `ad4529b9462cf789` + TQ v1.0 SHA `78af90cf64409364` + CIF SHA `eb5a9e8bacdfc6d1` verified live · Owner-cited CIF SHA `110a0d0448f66f44` was stale · corrected per D-11 canon-before-attest). |
| D-3 | Curated verdict | PASS | 18 R4 rows enumerated (+ 1 reflexive) · 7 QA rules enumerated (QA-1..QA-7) · 7 CR rubric items enumerated (CR-1..CR-7) · 6 RV cells (RV-1..RV-6) · 4 CIF manifest schema folds · 3 archive-ledger folds · 3 Tier-3 calibration folds · 3 TQ §7 Part B folds · **33 total folds classified per A3.4** (§4.H) · **36 parameters classified per A3.4 Rules Taxonomy lens** (§5.5 · 28 S + 0 O live + 7 E + 1 D). One Tier-1 surface named (E1 · CIF manifest schema landing shape · four sub-options a1/a2/b-rejected/c-rejected with Standing Rule v3 preservation attest per option) · 3 pre-named surfaces downgraded on evidence (§5.2 archive ledger dataclass posture · §5.3 CR-7 rubric extension · §5.4 Tier-3 Owner-side scope). §5.5 Rules Taxonomy classification table lands as parameter classification lens per Owner CRITIC-PASS STAGE A confirmation alignment · every parameter row cites A3.4 register entry. |
| D-4 | Rung inflation | PASS | All 18 sidecar rows at Rung-1 Deterministic. No fold proposed at rung above what §5-§6 mechanics or CIF §12 enforcement map require. |
| D-5 | Cross-phase content leakage | PASS | Zero G-13 / UI-1 / UI-2 / Lane 2b / Lane 1 content. DB-1 + DB-2 explicitly OUT · preserved in EAB-2 ruling §4 for Prove module phase. §7 fence attest lists each explicit exclusion. |
| D-6 | Silent scope drift | PASS | Split/merge decision at §1 disclosed builder Tier-3 with rationale (D-12-aligned: single-seam execution · CR-7 IS the rubric amendment per CIF A5.2 · not a separate rubric). §2.1/§4.2 split-threshold at 1,500 LoC / 60 cells (governance canon) pre-authorized-disclosed. |
| D-7 | Invented scope | PASS | Every acceptance criterion (QA-1..QA-6 + QA-7) is verbatim from Critic Seam v1.0 §8 or TQ v1.0 §7 line 125. Every CR rubric item (CR-1..CR-7) is verbatim from Critic Seam v1.0 §6.1 or CIF A5.2. Every fold traces to a verbatim spec line. §7 explicit D-7 attest carried. |
| D-8 | Silent drift | PASS | Parity 33 attest carried in §2 band table (contract touch = 0/0 this Stage A · contingent on §5.1 posture) and in §7 fence attest. §14 sidecar pattern cited for R4 rows. All Standing Rule v3 artifacts named for byte-identity guard at close (33 prior contracts + 33 snapshots · governance §§1..23 · post-Change-Order predecessors). |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked at Stage A landing. Native pytest cell suite proposed for execution atomic per §2 band table (~20-25 cells). |
| D-10 | Menu emission | PASS | Zero permission-menu emitted this Stage A. Tier-1 surface §5.1 states four ruling options (a1/a2/b-rejected/c-rejected) as *Owner ruling surface enumeration* with Standing Rule v3 preservation attest per option, not builder menu — pre-named per CIF §12 line 152 + structured per EAB-1/EAB-2/EAB-3 Stage A §5.1 precedents (Owner CRITIC-PASS STAGE A confirmation alignment mirror). |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Full canon read log at §9 below with live-verified SHAs + line ranges. Every Critic Seam v1.0/v1.1 mandate citation traces to a live-command-verified line range this session; every CIF §6/§12/§14 citation traces to a live grep this session; every TQ §7 citation traces to a live grep this session; every prior-phase-artifact SHA traces to a live `sha256sum` this session. Corrected Owner-cited stale CIF SHA per D-11 canon-before-attest discipline. |
| **D-12** | **Experimentation at system level only** | PASS | Every fold in §4 deploys in force with known parameters: QA-1..QA-7 bind behaviorally at once on adoption (Critic Seam v1.0 §11 verbatim: *"this document lands as a governed artifact; QA-1..QA-6 bind behaviorally at once (they are disciplines, costing nothing)"*). QA-2 RV-4 format gate hard-gates at submission (fail-closed · not warns). CR-1..CR-7 rubric cells are executable (measurement on real artifact composition, not curated). CIF §12 line 152 mandates format-gate-at-submission (fail-closed on unmanifested verdicts). Archive ledger CIF-entry-#1 seeds at execution atomic in force. §5.5 Class E defaults deploy pinned per engine version with pre-declared success parameters (Rules Taxonomy A3.2 · in force with known conditions of success). **Zero observe-first · zero shadow phase · zero trial modes · zero staged proving.** |

---

## §9 · D-11 canon-before-ruling read log

Files read during Stage A authoring (this session):

| File | SHA-256 | Line range read | Purpose |
|---|---|---|---|
| `docs/requirements/critic_seam_spec_v1.md` | `110a0d0448f66f44461190cd01c2f8e92513bafdc7aeb9a4ff2bd7f748841b35` | §5 L63-77 (Tier-1 RV-1..RV-6) + §6 L81-109 (Tier-2 critic pass + CR-1..CR-6 + §6.2 independence + counter-check) + §7 L111-121 (Tier-3 sampling instruments + calibration ledger + counter-check) + §8 L123-135 (QA-1..QA-6 behavioral rules) + §9 L137-148 (verification set) + §10 L150-160 (what this layer is not) | Part A canonical body · RV/CR/QA enumeration · discipline anchors |
| `docs/requirements/critic_seam_spec_v1_1.md` | `ad4529b9462cf789ab577f7f8a4ba4ed1fe8f33a096fce6a70669a826b8c5605` | §Part A + §Part B + §Sibling discipline (full body) | Part B pointer + QA-7 joint binding |
| `docs/requirements/transformation_quality_spec_v1.md` | `78af90cf64409364c9b9d97bbc2b7f0507f6b824ee1bc41bd610a79f1a44967e` | §7 L115-129 (Production QA machinery · Tier 1/2/3 · QA-7 custody boundary RULED · calibration mechanism) + §8 L131-140 (three-stage coverage) + §11 L169-175 (Not adopted · execution model · build entry) | TQ §7 Part B mechanics · QA-7 custody boundary discipline |
| `docs/requirements/cif_spec_v1.md` | `eb5a9e8bacdfc6d1d9f35cad41ff24b66a3127648a9f4aaeffe32b90973e7c1d` (live SHA · corrected from Owner-cited stale `110a0d0448f66f44` per D-11) | §4 L45-63 (Definitions · Manifest + Frame + Cycle) + §5 L65-83 (A1.1-A2.4 core practice) + §6 L85-93 (A4.1-A5.2 selection quality + CR-7 amendment) + §10 L126-136 (Operative parameters OP-1..OP-5) + §11 L138-148 (Quality parameters QA-a..QA-f) + §12 L150-164 (Enforcement map · Manifests + Archive + Metabolization + Selection-defects CR-7) + §13 L166-174 (Governance) + §14 L176-182 (Execution) | CIF §6 A5 rubric + §12 enforcement map + §14.2 archive-as-CIF-entry-#1 |
| `docs/registry/function_promise_registry_v1.md` | `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` | §2 promises + §S1 seams-scoped-by-instance + §M sidecar pattern authority | Row citations for §3 aggregate (10 rows) + §4 folds + §5 escalations + §6 sidecar (18 rows) |
| `docs/rulings/owner_change_order_2026-07-25.md` | `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568` | A1..A8 body + preamble interpretation rule + execution instruction | Post-amendment canon reconciliation (§1 table) |
| `docs/governance/rules_taxonomy_v1.md` | `63862a0375263e0b7c6d727c427c4c04aeb5785c401d8a2be06000fdd97f6758` | §A3.1 four-class table + §A3.2 E→O promotion + §A3.3 Class D lifecycle + §A3.4 initial register | A3.4 classification of Critic-pass parameters (§4/§5.5) |
| `docs/close_reports/eab_3.md` | `6144b13bfca05fa4bca06d786494cc25af69e40b1d02cf6880bace1230e72bab` | §9 parameter table (Class E annotation · Owner ITEM 1 forward-binding) + Parity 32→33 baseline SHAs | EAB-3 close preconditions verified · Parity 33 baseline · Owner forward-binding annotation applied |
| `docs/close_reports/change_order_2026_07_25.md` | `8def7256f1be9768bcd3fe93106056a7e83fe62e46f8824e0f95d664dc8ec539` | §5 CONFLICT-row annotations disposition + §7 D-1..D-12 self-audit + §8 phase ledger L-6 | Post-amendment reconciliation baseline · Standing Rule v3 continuity |
| `docs/stage_a_proposals/eab_3_stage_a.md` | `907ac439f05dd7b00985ce568228bc24e0e903f40c2d5986dfaa73d592d642c7` | §5 layout (§5.1 E1 live · §5.2 E2 downgrade · §5.3 E3 downgrade · §5.4 E4 downgrade · §5.5 Tier-3 remainder) | Structural precedent · Owner CRITIC-PASS STAGE A confirmation alignment cited this SHA for §5 layout mirror discipline |
| `docs/registers/phase_ledger_v1.md` | `92a65435759d9fca5b42e318cef6af6df343a47ce0dd1961cc0a4a0cb4f71c85` | §5 SEQUENCE (Critic-pass position 4) + §1 EAB-3 CLOSED row + §3 Critic-pass defined-undispatched row + §4 terminal figure 40/46 = 87.0% + §7 L-6 row (Change Order close) | Sequence position + D-9 auto-proceed context + Phase Ledger update discipline |
| `docs/governance/tiered_ruling_model.md` | `9b3c56c14a1159af35c382e1a68368fcf673a381f77cd4734e51a85cd57e51c4` | §2.1 L60 (split-threshold 1,500 LoC / 60 cells) · §6 rate ledger §6.1/§6.3/§6.9/§6.10/§6.11 · §14 sidecar pattern · §23 §0-CAL per-line enumeration mandate | Band derivation + sidecar pattern citation + §23 §0-CAL discipline |
| `backend/contracts/service_1_refusal_v1.py` | `3d5d9845e03d841916e8ce47733710bc490585681fe5b1e8350243875a631fad` (unchanged post-EAB-3) | Standing Rule v3 continuity attest | v1 refusal envelope byte-identical · Critic-pass does NOT touch |
| `backend/contracts/partition_schema.py` | `bdc4f6d34c94943c5dbf160208386fdd834b1049327358cfbc85e40aa7627d68` (unchanged post-EAB-3 seal) | Standing Rule v3 continuity attest | PartitionSchema@v0 byte-identical · Critic-pass does NOT touch |
| `backend/services/service_1/batch_quarantine.py` | `eaed941246aa422ded81bc506f2f2c876316fd93f5cd0f6cd4fbfb66d37a7aed` | EAB-2 batch-quarantine machinery module | QA-7 custody boundary rides this machinery (protection breach → per-batch quarantine fail-closed) |
| `backend/services/health/parity_counter.py` | Verified `EXPECTED_PARITY = 33` on-disk post-EAB-3 landing | Field-line inspection | Parity attest source for §2 band table |

**Zero recall from memory or summary presented as fact.** All row citations, SHAs, line ranges verified this session. **Owner-cited stale CIF SHA corrected per D-11 canon-before-attest discipline** (Owner ITEM 1 anchor block cited `110a0d0448f66f44` for CIF · live on-disk CIF SHA is `eb5a9e8bacdfc6d1d9f35cad41ff24b66a3127648a9f4aaeffe32b90973e7c1d` · this Stage A uses the live SHA per D-11).

---

## §10 · QA-1..QA-6 attest (Critic Seam Spec v1.0 §5 gates apply · v1.1 Part B pointer active · **recursive meta-application**)

Critic Seam Spec v1.0 (SHA `110a0d0448f66f44`) + v1.1 sibling (SHA `ad4529b9462cf789`) apply as landed requirements canon. **Meta-application:** this Stage A is the load-bearing implementation of Critic Seam Spec itself, so QA-1..QA-6 attest here is doubly load-bearing (this document must satisfy the discipline it authorizes).

| Gate | Attest |
|---|---|
| **QA-1** · Trace lens · every claim resolvable to on-disk source | PASS — every §4 fold traces to Critic Seam v1.0 §5-§7 verbatim line + CIF §6/§12/§14 verbatim line + TQ §7 verbatim line + Registry v1 row; §9 read log carries SHAs; §5.1 Tier-1 E1 traces to CIF §12 line 152 verbatim. |
| **QA-2** · Format gate · standing practice · D-10 table with D-1..D-12 rows | PASS — §8 D-10 table carries all 12 rows verbatim with D-12 as heavy-weight row. |
| **QA-3** · Fence explicit · scope out-of-scope named | PASS — §7 fence attest carries G-13 / UI-1 / UI-2 / refusal-envelope / Targeta cap-seat / Lane 2b / Lane 1 / DB-1 / DB-2 / OD-8/9/10 / re-surfacing-of-ruled-items / A8.1 reference-artifact-discipline exclusions explicitly + Parity fence explicit + Standing Rule v3 byte-identity guard explicit. |
| **QA-4** · Uncurated verdict · verdicts drawn from measured composition | PASS — §7 D-7 attest reinstates the discipline; RV-1..RV-6 mechanical + CR-1..CR-7 rubric cells + Tier-3 seeded-defect audits are D-7 exemplars (measurement on real artifact composition · fixed verdict pathway); D-12 §8 row reinforces. |
| **QA-5** · Zero-secret · data-blind extended | PASS — this Stage A carries no secrets/keys/tokens; grep-negative on standard secret patterns is standing practice for all governance-tier artifacts. |
| **QA-6** · Registry attribution · every fold cites v1.md row | PASS — §3 aggregate 10 rows cited; §6 sidecar 18 rows enumerated with promise-attachment column; §4 folds carry inline Registry-anchor citations per fold. |

**QA-7 · custody boundary (TQ §7 line 125 · joint binding per Critic Seam v1.1 Part B):** PASS — §4.G A.TQ7.3 fold classifies QA-7 as Class S · rides EAB-2 quarantine machinery. Protection breach at Critic-pass → per-batch quarantine fail-closed via `backend/services/service_1/batch_quarantine.py::quarantine_batch()` (already-landed at EAB-2 close · SHA `eaed941246aa422ded81bc506f2f2c876316fd93f5cd0f6cd4fbfb66d37a7aed`). Utility-class findings never block per QA-1.

Part B pointer (per Critic Seam v1.1 · TQ v1.0 §7): Tier-1 RV cells + Tier-2 CR-1..CR-7 rubric cells + Tier-3 sampling scaffold for Critic-pass folds will ride the atomic execution close, not Stage A. This Stage A is the standard *"Stage A landing → verbatim Tier-1 relay → rulings → atomic execution → close"* loop first step.

---

## §11 · Phase Ledger update (Stage A landing transition)

**Part A transitions (upon this Stage A landing):**
- §2 (open) N=0 → **N=1** (Critic-pass transitions defined-undispatched → open at Stage A landing per row-schema convention).
- §3 (defined-undispatched) N=5 → **N=4** (Critic-pass removed from defined-undispatched · row-lifecycle annotation `OPEN 2026-07-24 · Stage A landed docs/stage_a_proposals/critic_pass_stage_a.md` added to §3 row for sequence traceability).
- **§4 (Terminal figure)** — `closed 40 · open 1 · defined-undispatched 4 · HELD-D7 1 · denominator 46 · **figure `40/46 = 87.0%`**` — figure holds at 40/46 = 87.0% (denominator unchanged; open/defined-undispatched shuffle inside denominator per row-schema note).

**Part B:** no state changes this Stage A landing (owner-side deliverables unaffected).

**§7 (Owner Configuration Dispatches):** no new L-row this Stage A landing (Stage A is a builder-authored artifact · not an Owner-tier ruling · L-rows accrue on Owner ruling landings).

**Sequence progress:** EAB-3 CLOSED 2026-07-24 → Change Order 2026-07-25 filed 2026-07-24 → **Critic-pass Stage A OPEN** (this atomic) → **Owner rules Tier-1 E1 (§5.1 CIF manifest schema landing shape · a1 vs a2)** → Critic-pass execution atomic auto-proceeds under D-9 → Critic-pass CLOSED → G-13 auto-proceeds next (position 5 of 7 · Commercial Thesis Owner-side per Change Order A8.3).

---

*Critic-pass · Stage A Proposal · Landed 2026-07-24 · D-9 auto-proceed authorization from EAB-3 close + Change Order Filing close · Owner rules Tier-1 escalation §5.1 (E1 · CIF manifest schema landing shape · four ruling options a1/a2/b-rejected/c-rejected with Standing Rule v3 preservation attest per option · builder Tier-3 recommendation = (a1) additive) · builder Tier-3 downgrades of §5.2 (archive ledger dataclass posture · rides existing Northena) · §5.3 (CR-7 rubric extension · single live posture per CIF A5.2) · §5.4 (Tier-3 sampling Owner-side scope) disclosed. §5.5 Rules Taxonomy classification table (36 parameters · 28 S + 0 O live + 7 E + 1 D · every row citing A3.4 register entry) lands as parameter classification lens per Owner CRITIC-PASS STAGE A confirmation alignment (SHA `907ac439f05dd7b0` EAB-3 Stage A §5 layout precedent mirrored). Companion to: Critic Seam Spec v1.0 (Part A) · Critic Seam Spec v1.1 (Part B pointer) · Transformation Quality Spec v1.0 §7 · CIF Spec v1.0 · Registry v1 · Op. Values v1.1 · TQ v1.0 · SyniSense mandate · Change Order 2026-07-25 (7 amendments filed) · Rules Taxonomy v1 · Owner ruling composition (a1) (EAB-3 close) · Owner ruling composition ε + α + γ (EAB-2 close) · Prove Step 4 amendment (Owner-authored). Under D-12: every fold deploys in force with known parameters; if Parity 33→34 seal fires at §5.1 (a2) ruling, it lands as a sealed schema at execution, not staged; if (a1) ruled, Parity 33 held byte-identical throughout. §0-CAL §23.1 per-line enumeration MANDATORY for backend/contracts/** (additive fields if any) + backend/services/critic_pass/** + test invariant cells at execution atomic (this Stage A is doc-only; §23.1 gate-cell roster pre-declared for execution). **Every LoC/cell-count/band figure at §2 carries the Owner-mandated verbatim tag: "Provisional planning anchor — not a commitment. Relative weight only." — no exceptions.** Post-amendment canon reconciliation attested: A1..A8 disposition = zero conflict · A3.4 classification applied to 33 folds (§4.H fold-family lens: 27 Rails · 3 Engine settings · 1 Rules · 1 Registries · 1 Rails-boundary QA-7) and 36 parameters (§5.5 parameter-classification lens: 28 S · 0 O live · 7 E · 1 D). Parity 33 held byte-identical this Stage A · Standing Rule v3 attest carried.*
