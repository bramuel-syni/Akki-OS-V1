# G-3 · Operating Values v1.1 · Stage A Proposal · 2026-07-15

**Dispatch:** OWNER · G-3 · Operating Values v1.1 (standard loop · Stage A → Tier-1 relay → rulings → execution → close).
**Predecessor artifacts:** Operating Values v1.0 (`docs/requirements/operating_values_v1.md` · SHA `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee`) · Registry v1 (`docs/registry/function_promise_registry_v1.md` · SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`) · EAB Tier-1 Adoption Spec v1.1 (`docs/requirements/eab_tier1_adoption_spec_v1.1.md` · SHA `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9`) · Critic Seam Spec v1.0 (`docs/requirements/critic_seam_spec_v1.md` · SHA `110a0d0448f66f44461190cd01c2f8e92513bafdc7aeb9a4ff2bd7f748841b35`).
**Governance stack:** Standing Rule v3 · Registry Doctrine v1.0 · Tiered-Ruling §14 additive-supplement + §18 Critic Seam · Registry Doctrine Part IV §16 D-10 standing corrective · SQ-E1 γ · D-11 · D-7.

═══════════════════════════════════════════════════════════════════

## §1 · Scope (Owner-dispatched · verbatim absorption)

One revision, all folds, citing Registry v1 throughout:

**A · Part VII absorption (EAB adoption spec v1.1):**
- **F1** · Per-language model-serving accuracy gates — ASR ≤1.0pp WER, tagging ≤1.5 F1, per-language; **no ASR efficiency valve** (perception NEVER serves degraded without its per-language gate; text-tagging MAY carry first-run-only valve).
- **F2** · Quarantine systemic-halt threshold — **2% DEFAULT**, per-instance, S2.onboard-set per MC-E3 α; **sixth seam value**; SeamValues model extends; onboard ledger writes **8 rows** (was 5 rows post-MC-E3 α; adds 3 more attest-rows for the 6th value + telemetry: initial-set-value · initial-set-ledger · dual-control-swap-cell).
- **F3** · Run-telemetry rule — **no run without telemetry**; cost columns dormant until compute is metered.

**B · Conformance corrections (G-3's original register scope):**
- **spaCy NER** enters §1 as **rung-2 row** (`en_core_web_trf/sm`, fail-closed de-identification role, live in the Shield — **FACT**).
- **Diarization row** reconciled to built-state + decided-target: **Silero VAD integrated (FACT · live) · pyannote decided with license-verify-at-acquisition flag (NORM) · NeMo fallback (NORM)**.
- **Solva Bayesian weighting** recorded as measurement-era seat under `extraction_params@v0` — **equal-weight default (FACT)** per audit finding (`docs/audits/engine_conformance_v1.md:26`).

**C · Version discipline (register-precedent sibling pattern):**
- **v1.0 immutable** · **v1.1 lands as sibling** with amendment ruling (identical pattern to `outstanding_work_and_gap_register_v1.{0..4}.md` precedent).
- **§15 pointer updates** path + SHA in `docs/governance/tiered_ruling_model.md` (Amendment 15.1 · single §15 delta line · zero other governance line changes).
- **Evidence classes carried on every changed row** (FACT / NORM / DEFAULT) per Op. Values v1.0 §7 discipline.

═══════════════════════════════════════════════════════════════════

## §2 · Band (Governance §9 · raw LoC verdict-unit)

| Line item | LoC est. |
|---|---|
| v1.1 markdown fold (v1.0 body + §1 rung-2 rows added + §6 sixth-seam-value line + §12 F1..F3 folds + §13 conformance amendments + §15 doc-preamble bump) | ~800 |
| SeamValues model extension (`backend/services/multi_instance/onboard_context.py` — 6th field + validator + docstring update) — **CONDITIONAL on G3-E1 ruling** | ~40–120 (β sibling path ≈ 120; α additive ≈ 40; γ external ≈ 60) |
| S2.onboard ledger row-count fold (5→8 initial-set writes) — `backend/services/multi_instance/s2_onboard_service.py` writer + attest cell | ~80 |
| §1 spaCy NER row: registry row addition to Op. Values §1 (markdown-only) | ~15 |
| Diarization + Solva Bayesian conformance rows (markdown-only) | ~40 |
| Ruling record `docs/rulings/g3_op_values_v1_1_2026-07-XX.md` | ~120 |
| PHASE_STATE pointer #6 append + tiered_ruling_model.md §15 delta | ~10 |
| R4 sidecar `docs/registry/function_promise_registry_v1_g3_sidecar.md` (v1-era pattern per §14) | ~180 |
| Close report | ~250 |
| Test cells (F1 per-language gate schema · F2 sixth-seam-value initial-set + ledger · F3 telemetry-required-per-run · spaCy NER rung-2 assertion · Solva equal-weight default) | ~350 |
| **Raw total (projected)** | **~1,880–1,960 LoC** |

**Band ratified for Owner review:** `[1,600, 2,300]` raw LoC · verdict rendered in raw LoC per Governance §9.
**Split-threshold clause:** projected raw 1,900 > 1,500 → **pre-authorized Tier-2 split** available at execution (§4.2 Owner-standing clause). Candidate seams if Owner splits: (A) F2 sixth-seam-value + SeamValues extension + S2.onboard ledger (5→8 rows) → discrete atomic unit · (B) v1.1 markdown fold + §1 conformance rows + doc sibling landing → discrete atomic unit · (C) F1/F3 gates + telemetry test cells → discrete atomic unit.

═══════════════════════════════════════════════════════════════════

## §3 · Fold enumeration · row-by-row

### §3.A · Part VII absorption

| # | Fold | Source (v1.md line ref OR OpValues v1.0 line ref OR EAB v1.1 line ref) | Target (v1.1 section) | Evidence class |
|---|---|---|---|---|
| A.F1a | Per-language WER gate ≤1.0pp | EAB v1.1 §Part VII F1 (`eab_tier1_adoption_spec_v1.1.md:157`) · v1.md §v0-body §3.a `synisense.contracts.frozen_31` (attest surface) | v1.1 new §12.F1 subsection under (§ Serving discipline) | **NORM** (published-baseline anchored) |
| A.F1b | Per-language tagging F1 gate ≤1.5 points | EAB v1.1 §Part VII F1 line 157 | v1.1 §12.F1 | **NORM** |
| A.F1c | Perception NO efficiency valve (absolute) | EAB v1.1 §Part VII F1 line 157 | v1.1 §12.F1 rule row | **FACT** (architectural absolute) |
| A.F1d | Text-tagging first-run-only valve permitted | EAB v1.1 §Part VII F1 line 157 | v1.1 §12.F1 rule row | **NORM** |
| A.F2  | Quarantine systemic-halt threshold = 6th seam value | EAB v1.1 §Part VII F2 line 159; MC-E3 α ledger semantics | v1.1 §6.6 (§6 seam-value family extension; count goes 5→6) | **DEFAULT** (2% · S2.onboard-set · dual-control on change per §6) |
| A.F3  | Run-telemetry rule (no run without telemetry) | EAB v1.1 §Part VII F3 line 161; §Part VIII ES-3 line 169 | v1.1 §12.F3 (§ Serving discipline · post-§6) | **FACT** (posture-independent) |

### §3.B · Conformance corrections (G-3 original scope)

| # | Fold | Source | Target (v1.1 section) | Evidence class |
|---|---|---|---|---|
| B.1 | spaCy NER as rung-2 row (`en_core_web_trf`/`en_core_web_sm`) — fail-closed de-id role | `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md:13` verbatim; `docs/audits/deviation_audit_v1.md:14` (RECONNECTED IF-1); v1.md §v0.3-supplement-body IF1-G2 row `synisense.shield.fail_closed_deidentify_blocks_llm` | v1.1 §1 (add row: spaCy NER · MIT/CC-BY-SA · Rung 2 · Fail-closed de-id · live in Shield) | **FACT** |
| B.2a | Diarization built-state: Silero VAD integrated (MIT · FACT) | Op. Values v1.0 §1 row `VAD Silero VAD (as integrated)`; source-of-truth `services/perception/gpu_execution/*` | v1.1 §1 diarization row reconciled: Silero VAD status **FACT · live** | **FACT** |
| B.2b | Diarization decided-target: pyannote (open-weights · license-verify-at-acquisition flag) | Op. Values v1.0 §1 row `Diarization pyannote speaker-diarization` | v1.1 §1 diarization row: **NORM** class · license-verify-at-acquisition FLAG retained | **NORM · FLAG** |
| B.2c | Diarization fallback: NeMo (Apache-2.0) | Op. Values v1.0 §1 row `If current license text fails commercial use: fall back to NeMo-class (Apache-2.0)` | v1.1 §1 diarization row: NeMo fallback preserved verbatim | **NORM** |
| B.3 | Solva Bayesian weighting = measurement-era seat, equal-weight default | `docs/audits/engine_conformance_v1.md:26` (PARTIAL verdict: "G3 v0 honest default: equal-weight candidates"); v1.md §v0-body §3.c `solva.reasoning.probability_bayesian` (PARTIAL row); mandate §18 seat | v1.1 new §12.Solva-Bayesian-seat subsection: `extraction_params@v0.solva_weighting_method = "equal_weight"` (DEFAULT); Bayesian weighting = future measurement-era seat, dispatched on measured shortfall | **DEFAULT** |

### §3.C · Version discipline

| # | Fold | Source | Target | Evidence class |
|---|---|---|---|---|
| C.1 | v1.0 preserved byte-identical on-disk (Standing Rule v3) | `docs/requirements/operating_values_v1.md` SHA `a6c4a455…` (immutable) | v1.0 unchanged · attested at close with `git diff --stat HEAD` empty | **FACT** |
| C.2 | v1.1 lands as sibling at `docs/requirements/operating_values_v1_1.md` | Register-precedent pattern (`outstanding_work_and_gap_register_v1.{0..4}.md`) | v1.1 sibling file · own SHA · own amendment section | **FACT** |
| C.3 | tiered_ruling_model.md §15 pointer amendment: v1.0 SHA + v1.1 pointer added | `docs/governance/tiered_ruling_model.md:348-354` §15 body | Single amendment block appended under §15 · zero other governance stack lines touched | **FACT** |
| C.4 | Evidence classes carried on every changed row | Op. Values v1.0 §7 "every value below carries an evidence class per the Solva discipline" | Every row in v1.1 changed_since_v1.0 table carries FACT / NORM / DEFAULT | **FACT** |

═══════════════════════════════════════════════════════════════════

## §4 · Registry v1 citations (D-11 canon-before-attest · v1.md is active source)

Every fold cites Registry v1 (SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`). Zero citations to v0.md or supplements as active source (archaeological reference only per G-2 close).

| Fold | Registry v1 row cited | Line-range in v1.md |
|---|---|---|
| A.F1a/A.F1b | `synisense.contracts.frozen_31` · `perception.model_registry_pinned_provenance` · `perception.pinned_model_provenance` | §v0-body §3.a + §v0.5-supplement-body §S1 |
| A.F1c/A.F1d | `perception.execution_mode_telemetry` (9.2a-E1 α row) · `perception.pinned_model_provenance` | §v0-body §3.a + §v0.5-supplement-body §S1 |
| A.F2 | `akki.backend.s2_onboard_receiver_persists_instance_scoped` · `akki.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` · `akki.backend.tenant_entities_populates_from_s2_onboard` (v0.5 §S2 rows) · §Q3-Amendments Q3-02 BUILT | §v0.5-supplement-body §S2 + §Q3-Amendments |
| A.F3 | `perception.execution_mode_telemetry` · `northena.ledger.append_only_gate` | §v0-body §3.a + §v0-body §3.b |
| B.1 | `synisense.shield.fail_closed_deidentify_blocks_llm` (IF1-G2 · SUCCESS · live) · `synisense.shield.custody_chain_wired` (IF1-G1) | §v0.3-supplement-body §S1 |
| B.2a | `perception.vad_integrated_silero` (implicit from §Conformance-Evidence-Registry — Silero VAD integrated via `services/perception/gpu_execution/`) | §Conformance-Evidence-Registry |
| B.2b/B.2c | `perception.model_registry_pinned_provenance` (license-class rides receipt discipline) | §v0.5-supplement-body §S1 |
| B.3 | `solva.reasoning.probability_bayesian` (PARTIAL verdict at IF-1 audit; measurement-era seat) · §Conformance-Evidence-Registry line `solva.compliance.prove_one_run` | §v0-body §3.c + §Conformance-Evidence-Registry |

**D-11 attest:** every claim above traces to on-disk read via `sha256sum` + `grep -n` + `sed -n`; zero LLM-memory recall. Reads log in §8 below.

═══════════════════════════════════════════════════════════════════

## §5 · Tier-1 escalation surfaces (pre-named per Owner)

### §5.1 · G3-E1 · Sixth-seam-value contact with OnboardContextV0 · **Tier-1**

**Class:** Versioned surface schema extension (Registry Doctrine §14 additive-supplement clause vs. sibling-precedent version discipline).

**Question:** How does the sixth seam value (F2 quarantine systemic-halt threshold · 2% DEFAULT · per-instance) land onto the current `OnboardContextV0` composition, given that (a) the class name carries `V0` suffix — versioned surface, and (b) `onboard_version: str = Field(default="v0", frozen=True)` field-level frozen — but (c) the class is NOT sealed by a Parity 31 contract snapshot (no `onboard_context.contract_snapshot.json` under `backend/tests/invariants/`)?

**D-11 canon reads (on-disk state):**
- `backend/services/multi_instance/onboard_context.py:35-46` — current `SeamValues` model with **5 fields** (deletion_consequence_classes · rule_tightening_delay_hours · objection_escalation_days · suspension_re_review_days · outer_gate_manual_review_threshold).
- `backend/services/multi_instance/onboard_context.py:49-68` — `OnboardContextV0` composes `SeamValues`; `onboard_version` field frozen at `"v0"`.
- `ls backend/tests/invariants/*.contract_snapshot.json | wc -l` = **31** — no snapshot for OnboardContextV0 (not in Parity 31).
- MC-E3 α ruling (`docs/rulings/mc_e1_to_e6_2026-07-14.md`) — "initial-set writes ledger row" semantics; no bytes-frozen-at-v0 clause.
- EAB v1.1 F2 (line 159 verbatim): "The seam-value set becomes six; MC-E3 α initial-set/ledger semantics apply unchanged."

**Options (Owner rules):**

| Option | Description | Version-discipline consequence |
|---|---|---|
| **α** (additive in-place) | Extend `SeamValues` in-place: add `quarantine_systemic_halt_threshold_percent: float = Field(default=2.0)` as a 6th field. `OnboardContextV0` class name unchanged (v0 "evolved additively"). Track schema evolution by field-name registry, not class-name version. | Fastest; least code churn. **Breaks V0 semantic contract** (v0 was the 5-value seam-set at MC-E3 α landing). Field-name tracking only works because there's no contract snapshot enforcing byte-identity; if EAB-2's Parity 31→32 seal event later covers `OnboardContextV0`, this α becomes a byte-drift finding in retrospect. |
| **β** (sibling · register-precedent) | Mint `SeamValuesV1` (6 fields) as sibling to `SeamValues` (unchanged, 5 fields). `OnboardContextV0` gains an optional `seam_values_v1: Optional[SeamValuesV1] = None` field OR (stricter) mint `OnboardContextV1` sibling class. New instances write `SeamValuesV1`; existing v0 instances keep 5-value `SeamValues` byte-identical. S2.onboard writer routes new instances through V1 path. Register-precedent (v1.0→v1.1 sibling, `outstanding_work_and_gap_register_v1.{0..4}` sibling chain). | Maximally-conservative version discipline. Owner sibling-pattern precedent already ratified (Op. Values v1.0→v1.1 itself; register v1.0→v1.1..v1.4). Slightly higher code cost (~120 LoC vs. ~40 for α). Preserves V0 byte-identity forward. |
| **γ** (external field) | Sixth seam value lives OUTSIDE `SeamValues` composition — as top-level field on `OnboardContextV0` named `quarantine_systemic_halt_threshold_percent: float`. Sidesteps SeamValues extension. | Decouples seam-value evolution from OnboardContext class evolution. **BUT contradicts EAB v1.1 F2 explicit language:** "joins the governance seam values (§6 family)". Would place the 6th value structurally outside the family it explicitly joins. Not doctrinally coherent. |

**Builder analysis (does NOT resolve):**
- α is the pattern of expansion-under-a-fixed-label — cheap now, contingent on nothing external sealing `OnboardContextV0`. If EAB-2 seals it at Parity 31→32, this becomes a retroactive byte-drift finding.
- β matches Owner's own sibling-precedent (v1.0→v1.1 documents; v1.0..v1.4 registers). Extends the exact discipline the Owner has ratified across five prior artifact families. Highest code cost.
- γ solves a versioning problem the Owner did NOT ask to solve, and contradicts EAB v1.1 F2 verbatim "joins §6 family".

**Reflexive R4 attest (post-ruling):** the sixth-seam-value schema attest cell (`test_seam_values_carries_six_fields_post_g3` or `test_seam_values_v1_sibling_landed_carries_six_fields` per Owner ruling) attaches to `PROM-S1-frozen-wire-contract` (existing v0.md §2 promise) via foreign-key resolution. Zero new promises minted.

### §5.2 · G3-E2 · §1 model-row change contradicting a standing ruling · **DOWNGRADE to Tier-3** (Owner-expected none · none found)

**Class:** Registry §1 conformance-correction check against standing rulings.

**D-11 canon reads (on-disk state):**
- `grep -RIn "spaCy\|pyannote\|NeMo\|Silero\|diarization\|Bayesian\|weighting" docs/rulings/ docs/audits/`
- **spaCy NER** entry authorized verbatim at `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md:13` — "spaCy NER enters Operating Values v1.1 as a rung-2 row (en_core_web_trf/sm, fail-closed de-id role). Rides the v1.1 revision." **No contradiction.**
- **Silero VAD FACT-live** — v0.md §1 row + `services/perception/gpu_execution/` implementation. **No contradiction.**
- **pyannote NORM + license-flag** — Op. Values v1.0 §1 row verbatim; flag preserved. **No contradiction.**
- **NeMo fallback** — Op. Values v1.0 §1 row verbatim. **No contradiction.**
- **Solva Bayesian equal-weight default** — `docs/audits/engine_conformance_v1.md:26` PARTIAL verdict + "G3 v0 honest default: equal-weight candidates". **No contradiction.**

**Verdict:** zero §1 row changes contradict any standing ruling. **Downgrade to Tier-3** per builder judgment. Owner-expectation ("expect none") matches finding.

### §5.3 · Tier-3 remainder (dev Tier-3 judgment · disclosed at close)

| Fold | Tier-3 rationale |
|---|---|
| F1 per-language WER + tagging F1 gates | NORM-anchored numeric thresholds; matches published-baseline convention (WER 4-12% clean speech per Op. Values §3 anchor); no promise-text mutation; no contract touch. |
| F1 perception no-valve architectural rule | FACT-class architectural absolute; matches Solva "Layer 0 sentence" discipline; matches Registry Doctrine D-3 conflation test. |
| F1 text-tagging first-run-only valve permission | NORM-anchored; scoped to text-tagging only (per EAB v1.1 F1 verbatim). |
| F3 telemetry-required-per-run rule | ES-3 behavioral rule already binding per EAB v1.1 §Part VIII line 169; F3 records it in Op. Values v1.1 for discoverability. |
| Solva Bayesian seat under `extraction_params@v0` | DEFAULT `equal_weight`; measurement-era build seat (dispatched on measured shortfall); no in-flight build. |
| Diarization built-state (Silero) reconciliation | FACT-class status update (row already at NORM in v1.0; reconciles NORM→FACT with live-implementation citation). |
| Diarization pyannote/NeMo target discipline | NORM class preserved verbatim from v1.0; license-verify-at-acquisition flag preserved. |
| Evidence-class carriage on every row | FACT-class discipline extension per Op. Values v1.0 §7. |
| S2.onboard ledger 5→8 rows | Additive per MC-E3 α ledger-semantics-unchanged clause. |

═══════════════════════════════════════════════════════════════════

## §6 · R4 sidecar rows (v1-era sidecar pattern per Tiered-Ruling §14 + G-2 §M precedent)

**Sidecar path (proposed):** `docs/registry/function_promise_registry_v1_g3_sidecar.md`.
**Not created this Stage A** — enumerated only. Landed with atomic execution.
**Namespace:** `akki.registry.*` (post-MC-E6 β cutover · consistent with G-2 §M).
**Conservation posture:** zero new promises · all attach to existing v1 promises via foreign-key resolution.

Proposed row count: **6 R4 rows**.

| # | Proposed row ID | Cell (attest location) | Promise attachment (existing v1) | Rung |
|---|---|---|---|---|
| 1 | `akki.registry.op_values_v1_1_sibling_landed_v1_0_byte_identical` | `backend/tests/registry/test_op_values_v1_1_sibling.py::test_v1_0_diff_empty_at_v1_1_landing` | `PROM-S1-frozen-wire-contract` | 1 |
| 2 | `akki.registry.seam_values_carries_six_fields_post_g3` (schema-shape attest — pattern per α; β variant name: `..._v1_sibling_landed_carries_six_fields`) | `backend/tests/registry/test_seam_values_sixth_field.py::test_seam_values_has_quarantine_threshold_field` | `PROM-S1-frozen-wire-contract` | 1 |
| 3 | `akki.registry.s2_onboard_writes_eight_initial_set_rows` (was 5 pre-G-3 per MC-E3 α; 5→8 additive per F2 landing) | `backend/tests/registry/test_s2_onboard_initial_set_ledger_g3.py::test_initial_set_writes_eight_rows` | `PROM-S3-audit-trail-immutable` | 1 |
| 4 | `akki.registry.op_values_v1_1_per_language_gates_present_in_doc` (F1 markdown-schema attest) | `backend/tests/registry/test_op_values_v1_1_content.py::test_f1_per_language_gates_present` | `PROM-S1-frozen-wire-contract` | 1 |
| 5 | `akki.registry.op_values_v1_1_no_run_without_telemetry_rule_present` (F3 markdown-schema attest) | `backend/tests/registry/test_op_values_v1_1_content.py::test_f3_telemetry_rule_present` | `PROM-S3-audit-trail-immutable` | 1 |
| 6 | `akki.registry.op_values_v1_1_spacy_ner_rung_2_row_present` (§1 conformance-correction attest — B.1) | `backend/tests/registry/test_op_values_v1_1_content.py::test_spacy_ner_row_present_at_rung_2` | `PROM-S1-frozen-wire-contract` | 1 |

**Attribution summary:** 4 × `PROM-S1-frozen-wire-contract` + 2 × `PROM-S3-audit-trail-immutable`. **Zero new promises.** All rows attach via foreign-key resolution to existing v0.md §2 promises (preserved in v1.md §v0-body byte-identical per RM-E1 α). Ladder rung 1 (Deterministic) for all — schema/shape attests only.

═══════════════════════════════════════════════════════════════════

## §7 · D-7 fence attestation

| Fence | Compliance |
|---|---|
| **No EAB build items** | PASS · this Stage A folds Part VII **values into Op. Values** only; EAB-1/2/3 build phases remain dispatch-lane, un-initiated. |
| **No Critic Seam code** | PASS · Item 1 (Critic Seam Spec landing) is doc-only per Owner dispatch; this Stage A does not touch `/tools/critic/` or any critic-adjacent code. |
| **No calibration machinery** | PASS · F2's mechanism (per-instance quarantine-rate metering, dual-control swap, threshold-hit halt-and-notify) is EAB/QA-phase territory per Owner verbatim; this Stage A lands VALUES and GATES only. |
| **No model acquisition** | PASS · zero `pip install spacy en_core_web_*` · zero `curl` of pyannote / NeMo / Silero model weights · zero HuggingFace download. spaCy NER row is an on-disk-conformance recording of what is ALREADY live (`services/synisense/shield/deidentifier.py` uses spaCy pre-installed via `requirements.txt`). |
| **Standing Rule v3 · v0.md + supplements** | PASS · zero touches to v0.md + v0.1..v0.5 in this Stage A (doc-only proposal at `docs/stage_a_proposals/`). |
| **Standing Rule v3 · v1.md** | PASS · v1.md byte-identical (SHA `d6ad136f…`); zero touch. |
| **Standing Rule v3 · prior rulings** | PASS · all 21 pre-G-3 rulings under `docs/rulings/` diff-empty. |
| **Standing Rule v3 · prior registers** | PASS · v1.0..v1.4 register siblings diff-empty. |
| **Standing Rule v3 · Op. Values v1.0** | PASS · v1.0 will be preserved byte-identical at execution close (sibling pattern C.1 · attested at close). |
| **Parity 31** | PASS · zero contract touches this Stage A; execution contract touches will happen only if Owner G3-E1 β-path (SeamValues sibling) requires — but `OnboardContextV0` is NOT in Parity 31 (no `.contract_snapshot.json`); so Parity 31 unaffected either way. |
| **`/app/salvage/`** | PASS · zero touches. |
| **Testing subagent** | PASS · banned · not invoked. |
| **No unprompted next-surface Stage A** | PASS · this Stage A is dispatch-authorized (G-3 dispatch line 1). No G-4 / EAB-1 / Critic-Seam Stage As drafted this turn. |

═══════════════════════════════════════════════════════════════════

## §8 · D-10 self-audit table (D-1..D-11 · Owner-ratified STANDING PRACTICE)

| Defect | Verdict | One-line rationale |
|---|---|---|
| **D-1** · Byte-identity violation on verbatim carriers | **PASS** | All Owner-dispatched fold clauses (F1/F2/F3, conformance corrections list, version discipline) quoted verbatim from dispatch text; source citations use `sed -n 'A,Bp'` pattern where applicable. |
| **D-2** · Off-canon content injection | **PASS** | Every fold in §3 traces to an on-disk source (Op. Values v1.0 line · EAB v1.1 line · audit file line · v1.md row · ruling record line). Zero LLM-memory recall. |
| **D-3** · Unprompted execution beyond dispatch scope | **PASS** | Doc-only proposal at `docs/stage_a_proposals/g3_operating_values_v1_1_stage_a.md`. Zero code mutation this Stage A. Zero test files added. Zero registry v1.md touch. Zero Op. Values v1.0 touch. |
| **D-4** · Ruling-authority foreclosure | **PASS** | G3-E1 α/β/γ options presented; builder analysis explicitly "does NOT resolve"; Owner rules. G3-E2 downgraded with evidence-backed rationale (not builder-fiat). |
| **D-5** · Cross-phase content leakage | **PASS** | Zero EAB build content · zero Critic Seam code · zero calibration mechanism · zero model acquisition (§7 fence table). §11 sequencing anchor carries reference only. |
| **D-6** · Silent scope drift | **PASS** | R4 sidecar conservation posture held (zero new promises · all attach to existing v1 promises). Parity 31 unaffected (`OnboardContextV0` not in the sealed 31). |
| **D-7** · Scope-fence discipline | **PASS** | §7 explicit fence-compliance table. All eleven fences enumerated. |
| **D-8** · Testing-agent invocation | **PASS** | Banned · not invoked. Local pytest verification only at execution close. |
| **D-9** · Awaiting-signal turn ending | **PASS** | Stage A file lands on-disk; terminal reply (parent) closes with IDLE per Owner reply-structure spec. |
| **D-10** · Menu-emission / dispatch-authorization confusion | **PASS** | No menus to Owner in reply body; G3-E1 α/β/γ enumeration is Owner-ruling surface per Tiered-Ruling §4.4 (not builder decision). Standing practice: this table appears on every Stage-A/close-report reply per Owner ratification. |
| **D-11** · Canon-before-ruling / LLM-memory recall | **PASS** | §9 read log below enumerates 17 files with paths + line ranges read on-disk. Every fold sub-claim citation-backed. Zero recall. |

═══════════════════════════════════════════════════════════════════

## §9 · D-11 canon-before-ruling read log

**Files read on-disk (with paths + line ranges) before drafting this Stage A:**

| # | Path | SHA-256 (attest at Stage A landing) | Ranges read |
|---|---|---|---|
| 1 | `docs/requirements/operating_values_v1.md` | `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee` | 1-133 (full) |
| 2 | `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9` | 1-216 (full; §Part VII lines 155-165 verbatim absorption) |
| 3 | `docs/requirements/critic_seam_spec_v1.md` | `110a0d0448f66f44461190cd01c2f8e92513bafdc7aeb9a4ff2bd7f748841b35` | 1-175 (full; QA-2 line 127-128; §6.2 lines 99-109) |
| 4 | `docs/registry/function_promise_registry_v1.md` | `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` | 419 (spaCy shield row); §Conformance-Evidence-Registry (Silero · pyannote · Solva); §Q3-Amendments |
| 5 | `docs/audits/engine_conformance_v1.md` | *(diff-empty)* | 26 (Solva PARTIAL / Bayesian equal-weight default) |
| 6 | `docs/audits/deviation_audit_v1.md` | *(diff-empty)* | 14 (spaCy RECONNECTED at IF-1) |
| 7 | `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md` | *(diff-empty)* | 13 (spaCy NER enters Op. Values v1.1 as rung-2) |
| 8 | `docs/rulings/mc_e1_to_e6_2026-07-14.md` | `d49e3be19142c00dd261c1b406c6f318b14ca17feeca97be73ba6f22aac7e0b2` | MC-E3 α ruling body (initial-set + ledger semantics) |
| 9 | `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md` | `c7ce185735b50c08944a908c10b040428fb10ae8d397435b7758c5b03870e85a` | 1-53 (full; ruling body verbatim) |
| 10 | `docs/rulings/9_2a_e1_to_e4.md` | *(diff-empty)* | 28-54 (diarization/ASR telemetry pattern) |
| 11 | `docs/governance/tiered_ruling_model.md` | `f16bca32e0145466b83a21e9f4f2689fa631c30e1cc1c445d2d4db2c764bbb32` | §14 additive-supplement clause · §15 Op. Values pointer · §16 D-10 · §17 EAB · §18 Critic Seam (just landed this turn) |
| 12 | `docs/governance/registry_doctrine_v1.md` | `9dd1cc4bee310ad36780d182377ae8f3e25b7a681430c982dda18d76a408fbcf` | 87-97 (D-1..D-11 verbatim) · Part VII · §14 |
| 13 | `backend/services/multi_instance/onboard_context.py` | *(git-tracked · content read)* | 1-69 (full; SeamValues 5-field composition + OnboardContextV0 · onboard_version frozen field · no Parity 31 snapshot) |
| 14 | `backend/services/synisense/shield/llm_router.py` | *(git-tracked · content read for Critic-Seam consistency scan)* | 78-297 (invoke + invoke_with_metering signatures · no conversation-state persistence) |
| 15 | `docs/briefs/outstanding_work_and_gap_register_v1.4.md` | `1e67daaba99e3319a80ed30ee09dc42221dc734b1c0cc40d94e0d7e7a70f1172` | 11 (LT-1 status-truth precedent) · §14 Amendment 4 (G-2 close) |
| 16 | `docs/close_reports/g2_registry_maintenance.md` | `7713146daa3e855fbc9df0d14f274ca33b0b1901dc10a508911bfbcb8d537ca8` | §1..§11 (full · G-2 close · Registry v1 as active source) |
| 17 | `backend/contracts/*.py` (Parity 31 enumeration) | *(31 files · diff-empty)* | file listing only (Parity count verification) |

**Attest:** every sub-claim in §1..§7 traces to one of the 17 reads above via specific line-range citation. Zero content from LLM memory. Zero recall. Standing Rule v3 held: no touches to any of the 17 read files (except tiered_ruling_model.md, touched THIS turn by Item 1 §18 append per Owner dispatch — sibling turn, disclosed here for provenance).

═══════════════════════════════════════════════════════════════════

*End of G-3 Operating Values v1.1 Stage A Proposal · 2026-07-15. Owner-authorized standard-loop dispatch. Stage A is a landing per Governance §11.a; execution phase awaits Owner rulings on G3-E1 (Tier-1) and confirmation on G3-E2 downgrade + Tier-3 remainder. Standing Rule v3 · on-disk canonical.*
