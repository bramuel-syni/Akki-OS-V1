# §3.8 Answer Fluency — Rulings Record (AF-E1..AF-E4)

**Dispatch:** Owner ruling on Answer Fluency Stage A escalations (2026-07-10 · post-Fixture-Refresh-ratification).
**Basis:** Stage A proposal at `/app/docs/stage_a_proposals/answer_fluency.md` (SHA `363c0ee55d6c0c9f97b01237f7597f8ea2fe458efe8c40ac7b11a2c4d0c0c49e`).
**Standing Rule v3:** on-disk canonical. This file is the persistent record of Owner rulings + execution disposition.
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Metric-verdict in raw LoC per §9. Data-blind posture §8. 9.2-OWN resolution at new §11 landed same commit.
**Execution close:** `/app/docs/close_reports/answer_fluency.md`.

---

## §1. Owner rulings — verbatim carriers

### §1.1 AF-E1 β + 2 conditions — Per-sentence structured anchor mapping + numeric verification + full-response reject-on-fail (Owner-ruled)

> **AF-E1 — β, two conditions.** Per-sentence structured anchor mapping — positive attribution, mechanically checkable, 9.2a-E1 pattern. Conditions closing the self-declaration gap (a fabricated sentence can cite a real unit_id): (1) numeric grounding is verified, not declared — every numeral in a sentence must appear verbatim in that sentence's anchored units; mechanical check, no semantic scoring. (2) Any unanchored or failing sentence → grounding REJECT → whole response falls to the mechanical arm — the gate never patches prose.

**Disposition — applied verbatim:**

- **β anchor-mapping mechanic:** the LLM MUST emit `{prose, per_sentence: [{sentence_text, unit_ids: [...]}]}` structured JSON (Shield-side schema enforcement in `services/synisense/shield/fluency_synthesizer.py`). Grounding gate at `services/service_1/answer_grounding.py::verify_grounding(...)`:
  - **(A) unit_id ∈ set gate:** every declared `unit_id` in `per_sentence[*].unit_ids` MUST be in the caller's `load_bearing_unit_ids`. Any foreign unit_id → REJECT.
  - **(B) sentence-anchor coverage gate:** every sentence in `prose` (segmented into sentences by a mechanical splitter — see §3 below) MUST correspond to a `per_sentence[i]` entry with a non-empty `unit_ids` list. Any sentence in prose that is not covered by a per_sentence anchor entry → REJECT.
  - **(C) numeric-verification gate (Condition 1 · Owner-verbatim):** *"every numeral in a sentence must appear verbatim in that sentence's anchored units; mechanical check, no semantic scoring."* Numerals defined mechanically as: contiguous runs matching `[0-9]+(?:[.,][0-9]+)*(?:%)?` in the sentence text. For each numeral, if it does not appear verbatim (byte-exact substring match, case-insensitive-not-applicable-to-digits) in the concatenated text of the sentence's anchored units → REJECT.
  - **(D) full-response REJECT (Condition 2 · Owner-verbatim):** *"any unanchored or failing sentence → grounding REJECT → whole response falls to the mechanical arm — the gate never patches prose."* On any (A)/(B)/(C) failure at any sentence, the whole fluent draft is discarded; the mechanical arm produces the `answer_text`; `fluency_mode=mechanical`, `_grounding_reject_reason` populated with the specific gate that failed (e.g., `foreign_unit_id` / `sentence_not_anchored` / `numeric_verification_failed:sentence=<idx>:numeral=<value>`).

- **Sentence splitter (Tier-3 default):** mechanical regex splitter on sentence-terminating punctuation `[.!?]` followed by whitespace/EOF; not an LLM-based segmenter (a subtle failure mode would be an LLM-based splitter drifting from the anchor mapping). Whitespace normalisation before comparison.

- **Anchoring reflection cell:** AF-G6b (§6.10 reflection class) attests that `services/service_1/answer_grounding.py` implements exactly gates (A)+(B)+(C)+(D) with no additional semantic-scoring branches (grep-negative on `similarity` / `overlap` / `jaccard` / `embedding` in the module).

### §1.2 AF-E2 — Amended boundary set (Owner-ruled · owner-value amendment to BCR anchor)

> **AF-E2 — amended boundary set, not α.** Basis: α contradicts AF-E4's own anchor. "Upgrade path, not a replacement" — yet α makes the LLM a single point of failure: provider down → request 503s while a complete, correct mechanical answer sits available. The promise the anchor protects is refusal-taxonomy closure, and the amended set honors it fully:
>
> **Config defects fail loud → 503:** Emergent key missing/invalid only. A misconfigured deployment must not run silently degraded.
>
> **Runtime transients degrade gracefully → mechanical arm:** provider down, rate-limited, Shield timeout, structured-output parse failure. Response succeeds, fluency_mode=mechanical, telemetry carries the reason (llm_unavailable / llm_timeout / llm_parse_failure / grounding_reject). Never a refusal envelope.
>
> **Grounding REJECT → mechanical arm, as proposed.**

**Disposition — applied verbatim.** See §1.2.1 owner-value-amendment subsection immediately below (BCR anchor line "unavailability surfaces as 503" is superseded for runtime transients per this ruling).

**Boundary set as executed:**

| Failure mode | Route | Response | fluency_mode | Telemetry reason |
|---|---|---|---|---|
| Emergent LLM key missing / invalid | **503 (fail loud)** | infra-fault response | (n/a) | (n/a — 503 body) |
| Sonnet provider down | mechanical arm | 200 · ComposedConclusion_v0 | `mechanical` | `llm_unavailable` |
| Sonnet rate-limited | mechanical arm | 200 · ComposedConclusion_v0 | `mechanical` | `llm_unavailable` |
| Shield boundary timeout (30s) | mechanical arm | 200 · ComposedConclusion_v0 | `mechanical` | `llm_timeout` |
| Structured-output parse failure | mechanical arm | 200 · ComposedConclusion_v0 | `mechanical` | `llm_parse_failure` |
| Grounding gate REJECT (any sub-gate) | mechanical arm | 200 · ComposedConclusion_v0 | `mechanical` | `grounding_reject` (+ `_grounding_reject_detail`) |
| Grounding gate PASS | fluent arm | 200 · ComposedConclusion_v0 | `llm` | (n/a — success) |

**Never a refusal envelope** on any runtime transient. Refusal taxonomy (`admission_refusal` + `service_1_refusal`) untouched at Answer Fluency scope.

#### §1.2.1 Owner-value-amendment rationale (BCR anchor line supersession · Standing Rule v3 record)

**BCR v1.4 anchor line quoted (pre-ruling):** *"unavailability surfaces as 503."*

**Owner ruling text supersessioning the anchor for runtime transients (verbatim):** *"The BCR anchor line ('unavailability surfaces as 503') is superseded for runtime transients by this ruling — recorded as an owner-value amendment in the rulings record with this rationale."*

**Rationale (Owner-verbatim):** *"α contradicts AF-E4's own anchor. 'Upgrade path, not a replacement' — yet α makes the LLM a single point of failure: provider down → request 503s while a complete, correct mechanical answer sits available. The promise the anchor protects is refusal-taxonomy closure, and the amended set honors it fully."*

**Effect:** for the Answer Fluency phase and forward, LLM unavailability at runtime (provider down, rate-limited, Shield timeout, structured-output parse failure) degrades gracefully to the mechanical arm rather than 503. The 503 path is preserved for config defects only (Emergent key missing/invalid), because a misconfigured deployment MUST fail loud rather than run silently degraded. Refusal-taxonomy closure — the promise the BCR anchor protected — is honored more fully by the amended set than by the original 503 boundary (a 503 with mechanical output sitting available is a worse honesty posture than a graceful mechanical-arm response).

**Scope of supersession:** runtime transients ONLY. Config defects (Emergent key missing/invalid) remain 503. This is a narrow owner-value amendment to the BCR anchor line as it applies to `answer_fluency`; other phases retain the BCR anchor's original semantic unless separately amended by Owner ruling.

**Timeout stays at 30s (Tier-3 default preserved):** *"Timeout stays 30s; β is moot under fallback (a slow LLM costs latency, not availability)."*

### §1.3 AF-E3 α — Sidecar telemetry · envelope byte-identical · parity 31 (Owner-ruled)

> **AF-E3 — α.** Sidecar telemetry, envelope byte-identical, parity 31, per the 9.2a-E2 precedent. Fluency mode is operational metadata, not a truth claim — no honesty gap on the wire. β acknowledged as the future additive path if a client-facing disclosure need ever emerges; not selected.

**Disposition — applied verbatim:**

- `services/service_1/fluency_mode_telemetry.py` created (mirrors `execution_mode_telemetry.py` from 9.2a-E2 α condition 2).
- `annotate_result(request_id, telemetry_dict)` returns a NEW dict (non-mutating) with `fluency_mode` + `_fluency_attribution_trace_id` + optionally `_grounding_reject_reason` / `_grounding_reject_detail`.
- `ComposedConclusion_v0` frozen contract NOT mutated. Snapshot byte-identical. **Parity 31 preserved** (attested at AF-G4).
- β (contract additive field) acknowledged as future path but NOT selected. Reserved as an option for a subsequent Owner ruling if a client-facing disclosure need emerges.

### §1.4 AF-E4 α + 1 ordering condition — Byte-identical mechanical baseline + capture-then-refactor discipline (Owner-ruled)

> **AF-E4 — α, one ordering condition:** golden snapshots are captured from the pre-3.8 code path before any refactor lands — capture-then-refactor, or the baseline is self-referential. AF-G1 compares byte-identically thereafter.

**Disposition — applied verbatim with ordering strictly enforced:**

- **STEP A ordering condition:** golden snapshots captured from the pre-3.8 `composed_conclusion.py` mechanical-composer f-string at lines 330-335 BEFORE any composer refactor lands, via distinct capture cell landed at STEP A. Snapshots persisted at `/app/backend/tests/goldens/answer_fluency/pre_3_8/mechanical_baseline.json` — a JSON file containing representative `{load_bearing_unit_ids, computed_class, expected_answer_text}` cases derived from the exact pre-3.8 f-string.
- **AF-G1 gate wiring:** compares the extracted `synthesise_mechanical_answer_text(...)` function's output byte-identically against the persisted golden `expected_answer_text`. Any drift → AF-G1 FAIL.
- **Refactor discipline:** the extracted mechanical composer at `services/service_1/mechanical_composer.py` is a byte-identical lift of the pre-3.8 f-string — no logic changes, no formatting changes, no docstring alterations to the f-string itself. Only the surrounding function scaffolding is new.

---

## §2. Ancillary applied

### §2.1 §11 9.2-OWN resolution ride-along (governance amendment · same commit)

Owner PART 1 (verbatim in prior turn's dispatch) directed 9.2-OWN resolution to ride this commit's STEP A. Applied:

- **Governance §11 landing:** Owner PART 1 text (9.2-OWN-1 compute-to-data / 9.2-OWN-2 local access at archive / 9.2-OWN-3 correction from "on grant compute" to "at ingest, wherever the run occurs" / consequence → 9.2b's gate list collapses to two owner-side external actions) landed verbatim as new §11 in `/app/docs/governance/tiered_ruling_model.md`.
- **PHASE_STATE.md + PRD.md:** "9.2-OWN-1..3 pending owner decisions" wording struck; replaced with "9.2b awaits: RMS agreement + hardware at venue (owner-side actions). Topology ruled: compute-to-data (§11)."

### §2.2 §4.2 disposition — atomic single commit per §4.1 baseline

Actual raw LoC diff at close: recorded in `/app/docs/close_reports/answer_fluency.md` §2 (band derivation). §4.2 thresholds (1,500 raw LoC / 60 cells) NOT expected to trigger given Stage A estimates; atomic single commit per §4.1 baseline confirmed at execution.

### §2.3 Boundary-set expansion vs Stage A α

Owner amended α → amended boundary set (§1.2). Cell-count effect: AF-E2 amendment converts prior 503-cells to fallback-cells (~neutral); AF-E1 numeric-verification adds +1-2 cells; expected within band `[650, 950]` per Owner ruling: *"Band: E2 amendment converts 503 cells to fallback cells (~neutral); E1 numeric check +1–2 cells. Expected within [650, 950]; verdict in raw LoC per §9."*

---

## §3. Gate roster (AF-G1..AF-G8+ · executed)

| Gate | Tier | Purpose | Location |
|---|---|---|---|
| **AF-G1** | Tier-1 | Mechanical composer byte-identical to pre-3.8 f-string · golden diff | `test_answer_fluency_af_g1_to_g8.py::test_af_g1_mechanical_composer_byte_identical_to_golden` |
| **AF-G2a** | Tier-1 | Grounding gate (A) — every declared `unit_id` ∈ `load_bearing_unit_ids` | `...::test_af_g2a_foreign_unit_id_triggers_reject` |
| **AF-G2b** | Tier-1 | Grounding gate (B) — every sentence in prose covered by ≥1 anchor | `...::test_af_g2b_uncovered_sentence_triggers_reject` |
| **AF-G2c** | **Tier-1 (Owner Condition 1)** | Grounding gate (C) — numeric-verification (mechanical, no semantic scoring) | `...::test_af_g2c_unverified_numeral_triggers_reject` |
| **AF-G2d** | Tier-1 (Owner Condition 2) | Grounding gate (D) — any failure → mechanical arm; gate never patches prose | `...::test_af_g2d_any_failure_full_response_falls_to_mechanical` |
| **AF-G3a** | Tier-1 | AF-E2 amended: Emergent key missing → 503 (fail loud) | `...::test_af_g3a_missing_llm_key_fails_loud_503` |
| **AF-G3b** | Tier-1 | AF-E2 amended: provider down/rate-limited/timeout/parse-failure → mechanical arm | `...::test_af_g3b_runtime_transient_degrades_to_mechanical_arm` |
| **AF-G3c** | Tier-1 | AF-E2 amended: NEVER a refusal envelope on any transient | `...::test_af_g3c_never_refusal_envelope_on_runtime_transient` |
| **AF-G4** | **Tier-1 (frozen contract preservation)** | `ComposedConclusion_v0` snapshot byte-identical · parity 31 | `...::test_af_g4_composed_conclusion_snapshot_byte_identical_parity_31` |
| **AF-G5** | Tier-3 | Fluency-mode telemetry sidecar structure (mirrors execution_mode_telemetry) | `...::test_af_g5_fluency_mode_telemetry_sidecar_shape` |
| **AF-G6a** | Tier-1 | Shield chokepoint discipline (LLM call routes through Shield) | pre-existing `test_no_direct_llm_calls_outside_shield` |
| **AF-G6b** | **Tier-1 (§6.10 AST/reflection)** | `answer_grounding.py` implements exactly gates (A)+(B)+(C)+(D), no semantic branches | `...::test_af_g6b_answer_grounding_no_semantic_scoring_ast` |
| **AF-G7** | Tier-1 | Grounding-gate reject NOT a refusal · quality-gate outcome preserved as mechanical | `...::test_af_g7_grounding_reject_falls_through_not_refusal` |
| **AF-G8** | **Tier-1 (§6.10 · data-blind posture)** | Prompt template file contains no broadcaster/genre/regional residues | `...::test_af_g8_prompt_template_data_blind_no_residues` |

**Total: 14 gate cells** (Stage A estimate 15 → -1 via AF-G6a re-use of pre-existing `test_no_direct_llm_calls_outside_shield`; AF-E1 numeric-verification split into AF-G2c distinct cell honors Owner Condition 1's mechanical-check semantics).

---

## §4. Standing constraints preserved (attested at close)

| Constraint | Attestation |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | GREEN — Answer Fluency touches no frozen contract; snapshots byte-identical. |
| 4-code auth-refusal registry closed | GREEN — Answer Fluency is not an auth surface. |
| No HTTP 409 in new/modified files (E5 discipline) | GREEN — 503 only on config defect per amended AF-E2. |
| Standing Rule v3 (on-disk canonical) | GREEN — historical closes preserved. |
| AS-H1 retention held-class (no direct DELETE) | GREEN — no DELETE handlers added. |
| Governance §8 data-blind posture | GREEN — AF-G8 attests prompt template. |
| Governance §9 metric-verdict-in-derivation-unit | GREEN — band + verdict in raw LoC. |
| Governance §10 9.2 split ruling | GREEN — fluency dispatch-independent from 9.2a/9.2b. |
| Governance §11 9.2-OWN resolution (landed this commit) | GREEN — see §2.1 above + close report §3. |
| FR-G4 no-shadow-source AST posture | GREEN — prompt template contains no broadcaster residues (AF-G8). |
| CD-E2 ↔ CD-E4 coupling | N/A (census scope). |

---

## §5. Provenance

- **Stage A proposal:** `/app/docs/stage_a_proposals/answer_fluency.md` (SHA `363c0ee55d6c0c9f97b01237f7597f8ea2fe458efe8c40ac7b11a2c4d0c0c49e`)
- **Rulings record (this file):** `/app/docs/rulings/answer_fluency_af_e1_to_e4.md`
- **Close report:** `/app/docs/close_reports/answer_fluency.md`
- **§11 governance amendment:** `/app/docs/governance/tiered_ruling_model.md` new §11
- **Golden snapshots (AF-E4 pre-refactor capture):** `/app/backend/tests/goldens/answer_fluency/pre_3_8/mechanical_baseline.json`
- **Landing SHA:** recorded in close report §7 post-commit.
- **Backend Pytest:** attested at close.
- **Frontend Jest:** unchanged (137/137).
- **Playwright chromium:** unchanged (44/44).
- **Parity:** 31/31 byte-identical.

---

## §6. Post-ratification note (Owner, 2026-07-10)

§3.8 Answer Fluency close was ratified unconditionally by Owner on 2026-07-10. The slice-identity evidence-line condition (issued pre-ratification and satisfied in the close report addendum §12) was withdrawn by Owner as over-gating; the addendum stands on-disk unchanged per Standing Rule v3 (historical carriers preserved), but its status is recategorized here per Owner's correction.

**Owner correction verbatim (2026-07-10):** *"The §3.8 status tracking wasn't over-gating: it caught the builder's sequence table silently dropping a mandate item, which is exactly the kind of thing tracking exists for. It resolved correctly and is simply done — listing it as 'retired over-gating' miscategorizes a check that worked, and teaches the builder the wrong lesson about which checks were the problem."*

**Owner ratification verbatim (2026-07-10):** *"§3.8 Answer Fluency close: RATIFIED — unconditionally. The slice-identity evidence line is withdrawn: five independent SHA-pin gates re-blessed green + AF-G1 golden baseline + 1,162 passing tests is the attestation; a re-description of the verification mechanism adds no protection the gates already carry. The condition was over-gating and is struck."*

**Effect:** the §3.8 close is complete and ratified. Standing Rule v3 preserves §12 addendum on-disk (evidence stands as a record of the addendum discipline; not amended). Governance §12 (close-ratification discipline) landed same 2026-07-10 turn as the standing rule going forward: conditions attach at ruling time, never at close time.
