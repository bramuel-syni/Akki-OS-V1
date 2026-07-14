# Tiered Ruling Model — Standing Governance

**Source:** Owner Message post-8-EXT ratification (2026-07-08).
**Effect:** Effective immediately upon landing of this file.
**Precedes:** All prior "verbatim rulings on every escalation" doctrine. This tiered model REPLACES that doctrine at Artifact Store Stage A dispatch and forward.

**Standing Rule v3 preserved:** this doc lives on disk. Reply body carries SHA + tier tags only.

---

## §0. Verbatim carrier (Owner text, no paraphrase)

> Governance correction, effective now — rules carry a stated basis and block function only where a client promise is at risk:
>
> Tier 1 — client-promise (full rigor): provenance/audit integrity, security boundaries (auth scope, key custody, raw-never-egresses), honesty grammar (class-with-claim, refusal-first, no hidden mocks, no fabricated values), frozen wire contracts. Verbatim rulings and named gates stay.
>
> Tier 2 — cost/rework (proportionate): bands, rates, split thresholds. Disclosure, never blocking — a miss is a line in the close, not a halt.
>
> Tier 3 — hygiene (silent default): naming, glyphs, doc/registry mechanics, backlog accuracy. Builder defaults + one disclosure line. No escalations, no round-trips.
>
> Operational: escalations arrive pre-tiered — Tier 3 never escalates; Tier 2 only at thresholds; Tier 1 keeps verbatim treatment. Pre-flight attestations end unless the dispatch touches Tier-1 surface — the green-light is implicit in the dispatch. Before any rule blocks function: name the promise it protects, or the rule yields with a one-line log.

---

## §1. Tier 1 — Client-Promise (Full Rigor)

**Definition (Owner verbatim):** *"client-promise (full rigor): provenance/audit integrity, security boundaries (auth scope, key custody, raw-never-egresses), honesty grammar (class-with-claim, refusal-first, no hidden mocks, no fabricated values), frozen wire contracts. Verbatim rulings and named gates stay."*

### §1.1 Surface list (non-exhaustive; extend at dispatch time)

- **Provenance / audit integrity:** `NorthenaLedgerRow_v1` shape and emission discipline, trace_id chain integrity, `stamp_audit.data_class` sidecar registry additivity.
- **Security boundaries:**
  - **Auth scope:** own-vs-foreign gates (`require_own_scope_or_deny` and equivalents); 4-code auth-refusal registry closure; JWT class/claim discipline.
  - **Key custody:** `SYNISENSE_MASTER_SECRET`, trust-receipt signature invariants, HMAC/signature boundaries.
  - **Raw-never-egresses:** raw content bytes do not leave the boundary without authz having fired first (mechanism-not-convention).
- **Honesty grammar:**
  - **Class-with-claim:** every disposition/refusal carries a class label.
  - **Refusal-first:** authorization checks precede content emission.
  - **No hidden mocks:** if a value is stubbed for dev-tier, it is loudly disclosed at close.
  - **No fabricated values:** empirical rates come from observed builds, not aspirational figures.
- **Frozen wire contracts:** 28 Pydantic snapshot bijection (V1-G7 assertion set). Any addition is a Tier-1 escalation (parity delta requires Owner rulings).

### §1.2 Discipline

- **Escalations:** verbatim ruling loop (existing template: Class / Question / Authority-source language / Options α/β/γ / Recommended). Owner ruling required BEFORE execution.
- **Named gates:** stay. Grep-negative anti-rule gates stay. Attestation cells stay.
- **Pre-flight attestation:** required only when the dispatch touches Tier-1 surface.
- **Promise-naming rule:** *"Before any rule blocks function: name the promise it protects, or the rule yields with a one-line log."*

---

## §2. Tier 2 — Cost / Rework (Proportionate)

**Definition (Owner verbatim):** *"cost/rework (proportionate): bands, rates, split thresholds. Disclosure, never blocking — a miss is a line in the close, not a halt."*

### §2.1 Surface list

- **Bands:** Owner-anchored LoC/cell bands per phase (`[bottom, top]` snapshot_lloc_in_band verdict).
- **Rates:** amortised cell-cost rates (12 LoC/cell backend Pytest shared-helper · 9 LoC/cell Playwright data-testid · 16 LoC/cell frontend Jest standalone · endpoint/component amortisation rates).
- **Split thresholds:** `§4.2` pre-authorized split (currently 1,500 LoC / 60 cells).

### §2.2 Discipline

- **Escalations:** only at threshold-adjacent choices (e.g., "if the adapter surface exceeds the split threshold, land put_once as commit A and get+head as commit B"). Format: one-paragraph `if X, then split` statement. NO Owner ruling required unless threshold hits AT EXECUTION TIME.
- **Miss handling:** a band miss is a line in the close report, not a halt to execution. Symmetric miss-disclosure per Ruling 5 stays.
- **No pre-flight round-trip.**

---

## §3. Tier 3 — Hygiene (Silent Default)

**Definition (Owner verbatim):** *"hygiene (silent default): naming, glyphs, doc/registry mechanics, backlog accuracy. Builder defaults + one disclosure line. No escalations, no round-trips."*

### §3.1 Surface list

- **Naming:** module names, function names, file names, path conventions.
- **Glyphs:** middle-dot U+00B7, em-dash U+2014, hyphen U+002D discipline — EXCEPT where a glyph carries a Tier-1 promise (e.g., anti-slop charCodeAt gates on UI Spec verbatim copy stay Tier 1 because they protect the "honesty grammar / no fabricated values" surface).
- **Doc/registry mechanics:** file layout, section numbering conventions, close-report skeleton, rulings-record skeleton.
- **Backlog accuracy:** sequence lines, dispatch-order strings.

### §3.2 Discipline

- **NO escalation.**
- **NO Owner round-trip.**
- **Builder chooses default** based on repo conventions + Read-First / Reuse-Always mandate.
- **ONE disclosure line** in the close report using the format:
  ```
  [Tier 3 default] {item} → {chosen default} — {one-line rationale}.
  ```

---

## §4. Operational rules (Owner verbatim carrier)

> Operational: escalations arrive pre-tiered — Tier 3 never escalates; Tier 2 only at thresholds; Tier 1 keeps verbatim treatment. Pre-flight attestations end unless the dispatch touches Tier-1 surface — the green-light is implicit in the dispatch. Before any rule blocks function: name the promise it protects, or the rule yields with a one-line log.

### §4.1 Escalations arrive pre-tiered

Every escalation at Stage A carries an explicit tier tag: `[Tier 1]`, `[Tier 2]`, or `[Tier 3]`. Untagged escalations are a Stage A defect.

### §4.2 Pre-flight attestation

- **Tier-1 surface touched:** pre-flight attestation still required (existing pattern).
- **Tier-1 surface NOT touched:** pre-flight attestation ends. Green-light is IMPLICIT in the dispatch.

### §4.3 Promise-naming rule

Before any rule blocks function: name the promise the rule protects, or the rule yields with a one-line log.

Format for a yielding rule (in close report):
```
[Rule yield] {rule name} yielded on {surface} — {no client promise identified}.
```

### §4.4 Report cadence

- Stage A reply lands → main agent relays [Tier 1] escalations verbatim to Owner. [Tier 2] and [Tier 3] items are disclosure-only, no Owner round-trip.
- **Zero [Tier 1] escalations** → dispatch is complete on Owner side; agent receives implicit green-light and proceeds to execution immediately.
- **≥1 [Tier 1] escalation** → verbatim relay + Owner rulings loop, same as prior.

---

## §5. What stays unchanged

- **Standing Rule v3** — on-disk canonical is the record. Reply body carries SHA + one-line quotes / tier tags.
- **§4.1 baseline atomic first-commit discipline.**
- **§4.2 pre-authorized split thresholds** (LoC and cell numbers; the threshold values themselves are Tier 2 per this model — miss disclosure not blocking).
- **28 frozen contracts + 28 snapshot bijection (V1-G7).** (Post-Artifact-Store bumped additively to 29/29; V1-G7 assertion set at 29.)
- **4-code auth-refusal registry closure.**
- **BCR §5.1 sequence + [OWNER] gate lines.**

---

## §6. Codified rate ledger

Rates below are the on-disk canonical record; Stage A proposals cite this section rather than restating.

### §6.1 Backend Pytest — shared-helper amortised · **12 LoC/cell**

Empirical basis: multiple prior closes (9.1, 9.3, 8-EXT).
Trigger: cells in the "classic shared-helper class" (sync client, shared fixture, ~3-5 assertions per cell).

### §6.2 Backend endpoint impl — amortised 3-share · **40 LoC/endpoint**

Empirical basis: 8-EXT actual (3 grant endpoints via `require_own_scope_or_deny`).

### §6.3 Backend service module — standalone · **100 LoC/module**

Empirical basis: 8-EXT `engineer_scope.py` (84) + `engineer_invites.py` (170) 2-share.

### §6.4 Frontend Jest structural — standalone fallback · **16 LoC/cell**

Empirical basis: pre-9.1 codification; 8-EXT observed −50 delta on `renderHook` micro-cells (rate-composition finding, not rate-shift).

### §6.5 Playwright chromium data-testid amortised · **9 LoC/cell**

Empirical basis: codified at 9.1/9.3.

### §6.6 Frozen Pydantic contract class · **60 LoC/class**

Empirical basis: `OuterGateReceipt_v1` at AS close (103 LoC actual; 60 LoC class body + ~40 LoC docstrings/verbatim-Owner-carriers). Rate cites the class-only shape; verbatim docstrings are one-off overhead.

### §6.7 Frozen contract snapshot JSON — standalone · **~155 LoC/snapshot**

**Codified at 2026-07-08 post-Artifact-Store close.**

- **Class label:** *"snapshot = schema size"* — the LoC of a snapshot reflects the Pydantic-auto-generated JSON Schema's expansion of nested `$defs`, `enum`, and field-description shape. It is a mechanical function of the contract's field graph, NOT of developer effort.
- **Empirical basis:** `OuterGateReceipt_v1` snapshot at AS close — **155 LoC actual vs 20 planned (+735%).** The contract inherits `LedgerArtifactRef` + transitive types; those get spelled out under `$defs` in the JSON Schema.
- **Amortisation trigger:** NONE. Standalone class. Snapshots do not share code with other cells; each frozen contract emits exactly one snapshot; the size is a byte-cost of schema honesty on disk.
- **Named trigger:** *"Any Stage A adding a new frozen contract MUST price its snapshot at ~155 LoC/snapshot standalone in §3 band derivation. No hidden buffering; no padding; explicit line-item."*
- **Deviation clause:** if a specific contract's snapshot lands materially above or below 155 LoC (>±30%), disclose the delta at close per Tier-2 discipline (governance §2.2 — cost/rework class).

### §6.8 Watched rate classes (NOT YET codified — require second observation)

Per Ruling 5 discipline: a rate class is codified only after two observations. The following are candidates:

*(No entries as of 2026-07-10.)*

**Watched list is empty as of 2026-07-10; new watched classes admitted per Ruling 5 on first observation.**

**Codification retirements 2026-07-09 (post-TF ratification · Owner Message 565):**
- ~~**AST/reflection gate cells**~~ — second observation confirmed at TF-G9 (`services/transform_forms/callable_skill_persistence.py` write-once slice-freeze grep-negative walker) matching AS-G6 magnitude (~40 LoC/cell). CODIFIED at §6.10 below.
- **NEW:** **Verbatim-carrier overhead** — three-observation retrospective (AS Owner-verbatim docstrings · TF Owner-verbatim TF-E1..E4 α/β/γ carriers · TF governance §8 data-blind posture carrier). CODIFIED at §6.9 below — Owner Message 565 dispatched the codification by retrospective across three datapoints rather than waiting for a fourth.

**Codification retirements 2026-07-10 (post-Census-dimensions ratification · Owner post-CD dispatch):**
- ~~**Async httpx backend Pytest cells**~~ — second observation confirmed at CD-G4 E2E cells (`test_census_dimensions.py::test_cd_g4_e2e_*`) matching AS-close magnitude (~25 LoC/cell). CODIFIED at §6.11 below.

### §6.9 Verbatim-carrier overhead — per carrying module · **~100-150 LoC/carrier**

**Codified at 2026-07-09 post-Transform-Forms ratification (Owner Message 565).**

- **Class label:** *"verbatim = one-off overhead per Owner-supplied text carrier."* Any module, ruling, docstring, gate, or governance section that must reproduce Owner-supplied text VERBATIM (no paraphrase, no shortening, no glyph-substitution) carries an amortisation-immune LoC cost roughly equal to the text's on-disk footprint plus a small structural frame (docstring quotes, sentinel comments, section headers).
- **Empirical basis (three-observation set):**
  - **AS close (2026-07-08):** `OuterGateReceipt_v1` module carried ~40 LoC of Owner-verbatim docstring/rationale text alongside the 60 LoC class body (103 LoC total; verbatim overhead ~40). Additional AS-close rulings-record carriers (`docs/rulings/artifact_store_as_e1_to_e4.md`) landed at ~120 LoC across four rulings.
  - **TF close (2026-07-09):** `KnowledgeArtifactV0` + `CallableSkillProvisioningV0` + `callable_skill_gate.py` collectively carried ~110 LoC of Owner-verbatim TF-E1..E4 ruling-condition text embedded as docstrings/module comments; `docs/rulings/transform_forms_tf_e1_to_e4.md` landed at ~108 LoC.
  - **TF governance §8 carrier (2026-07-09):** data-blind posture Owner text landed verbatim at ~9 LoC prose + ~5 LoC framing = ~14 LoC in this file's §8 (single carrier; light-end of range because the Owner text was compact).
- **Trigger:** any dispatch containing at least one Owner-supplied verbatim condition, ruling, or posture statement that must land on-disk without paraphrase MUST price a verbatim-carrier line-item at ~100-150 LoC per carrying module in the §3 band derivation. Multiple verbatim blocks WITHIN a module amortise into that band; distinct modules each carry their own line-item.
- **Amortisation trigger:** NONE across modules. WITHIN a module, multiple verbatim blocks amortise into the ~100-150 LoC range regardless of block count.
- **Named trigger:** *"Any Stage A whose Owner-supplied verbatim text will land inside a source module, contract file, service module, gate module, ruling record, or governance section MUST price a verbatim-carrier line-item at ~100-150 LoC per carrier in §3 band derivation. No hidden buffering; no padding; explicit line-item."*
- **Deviation clause:** if a specific carrier lands materially above or below the 100-150 LoC band (>±30% of band midpoint 125 → below ~87 or above ~163), disclose the delta at close per Tier-2 discipline (governance §2.2 — cost/rework class). Compact-text carriers (single-paragraph postures) may land ~15-40 LoC honestly — disclose as under-band on the light side; multi-ruling carriers stacking 4+ verbatim blocks in one module may land ~180-220 LoC — disclose as over-band on the heavy side.

### §6.10 AST/reflection gate class — standalone · **~40 LoC/cell**

**Codified at 2026-07-09 post-Transform-Forms ratification (second observation satisfied · Owner Message 565).**

- **Class label:** *"reflection-gate = walker + whitelist + violation formatter."* Any Pytest gate that uses `ast.walk` / `ast.parse` / `inspect.signature` / regex-over-parsed-code / other codebase-reflective techniques to enforce a grep-negative or grep-positive invariant carries a standalone per-cell LoC cost that does NOT amortise into classic shared-helper cells (§6.1).
- **Empirical basis (two-observation set):**
  - **AS-G6 (2026-07-08):** grep-negative AST walker over `services/artifact_store/adapter.py` enforcing `_get_raw` privacy (whitelist of allowed callers + AST walker + violation formatting) — ~40 LoC/cell.
  - **TF-G9 (2026-07-09):** grep-negative AST walker over `services/transform_forms/callable_skill_persistence.py` enforcing write-once slice-freeze — verifying `update_one({..., corpus_slice_ref: ...})` never appears (whitelist + AST walker + violation formatting) — ~40 LoC/cell.
- **Trigger:** any Stage A introducing a reflection/AST-based gate MUST price the gate cell at ~40 LoC/cell standalone in §3 band derivation. This overrides the classic §6.1 12 LoC/cell amortisation for the specific reflection cell(s); non-reflection cells in the same test file continue to amortise per §6.1.
- **Amortisation trigger:** NONE. Standalone class per cell. Multiple reflection gates in the same file each carry their own ~40 LoC baseline (walker structure + violation formatting are not shareable across distinct invariants without collapsing the invariants themselves, which is unacceptable per Tier-1 honesty grammar).
- **Named trigger:** *"Any Stage A adding a reflection/AST gate cell MUST price it at ~40 LoC/cell standalone in §3 band derivation. No hidden amortisation into §6.1; no shared-helper wishing. Explicit line-item."*
- **Deviation clause:** if a specific reflection gate lands materially above or below 40 LoC (>±30% → below ~28 or above ~52), disclose the delta at close per Tier-2 discipline. Reflection gates with unusually complex whitelist logic (cross-module regex fusion, multi-file AST parse) may run higher — disclose, do not hide.

### §6.11 Async httpx auth-overhead cell class — standalone · **~25 LoC/cell**

**Codified at 2026-07-10 post-Census-dimensions ratification (second observation satisfied · Owner post-CD dispatch).**

- **Class label:** *"async httpx auth-overhead cell = multi-step auth setup performing at least 3 auth-overhead lines per cell (mint token + inject header + assert on protected endpoint response)."* Any Pytest cell that spins up an `AsyncClient` (or equivalent async HTTP client) and performs multi-step auth setup as a fixture-owned per-cell operation carries a standalone per-cell LoC cost that does NOT amortise into classic shared-helper cells (§6.1).
- **Empirical basis (two-observation set):**
  - **AS close (2026-07-08):** async httpx cells performing token-mint + Authorization header injection + trace/artifact provisioning + response assertion — ~25 LoC/cell empirical (vs ~22 standalone / ~12 amortised for a classic §6.1 shared-helper cell). Cell count: 4 async httpx cells.
  - **CD close (2026-07-10):** CD-G4 E2E cells (`test_cd_g4_e2e_record_census_dimension_registers_and_persists` + `test_cd_g4_e2e_manifest_declared_novel_hard_fails` + `test_cd_g4_e2e_manifest_declared_existing_value_writes`) performing motor test-db fixture + Mongo unique-index assertion + upsert + read-back at ~25 LoC/cell empirical.
- **Named trigger:** *"async httpx cells performing multi-step auth setup (mint token + inject header + assert) — 3+ auth-overhead lines per cell."* Applied strictly: cells NOT performing auth-overhead (e.g., a service-level unit test with in-process fixtures) continue to amortise per §6.1.
- **Trigger:** any Stage A introducing async httpx cells with the auth-overhead pattern MUST price them at ~25 LoC/cell standalone in §3 band derivation. This overrides the classic §6.1 12 LoC/cell amortisation for the specific auth-overhead cell(s).
- **Amortisation trigger:** NONE. Standalone class per cell. Shared fixtures reduce cell-body LoC by ~5-8 but the per-cell auth-overhead lines are not shareable without collapsing the invariant coverage.
- **Deviation clause:** if a specific cell lands materially above or below 25 LoC (>±30% → below ~17 or above ~33), disclose the delta at close per Tier-2 discipline. Cells performing multi-endpoint auth flows (register + login + protected + refresh) may run heavier — disclose, do not hide.

---

## §7. Backlog correction (Owner verbatim carrier)

> Backlog correction: strike "§5.4 Dual-actor Integration Console" — 8-EXT was §5.4; done, not queued.

**Effect:** the backlog line *"§5.4 Dual-actor Integration Console"* is STRUCK from PHASE_STATE.md and PRD.md. 8-EXT (closed 2026-07-08, ratified in this same Owner message) IS §5.4.

═══════════════════════════════════════════════════════════════════

## §8. Data-blind posture (Owner, 2026-07-09) — verbatim carrier

> Data-blind posture (Owner, 2026-07-09). The build makes no assumptions about the content, genre, composition, or shape of the RMS estate. The product is built against fixtures and closed against gates — no RMS material in the build path at any phase, and no pre-build data request to RMS exists. First contact with real data is the census, at scale, on grant compute, after the product exists. The census discovers the estate; nothing pre-describes it. All downstream activities — validation slices, training baselines, opportunity analysis, product prioritization — draw from measured census composition, never from any prior picture of "what RMS airs." Any fixture, example, binding copy, or spec text that encodes a content-type assumption as if it were the estate's shape is a defect against this posture, corrected on sight, Tier-3, no escalation.

**Effect (governance-tier mapping):**
- Fixture / example / binding-copy content-type assumptions presented as estate shape → **Tier-3 defect · correct-on-sight · no escalation.**
- Downstream activities (validation slices, training baselines, opportunity analysis, product prioritization) MUST cite measured census composition, never prior estate assumptions → **Tier-1 (honesty grammar · no fabricated values, applied to estate description).**
- Pre-build data request to RMS is prohibited by this posture. First contact = census.

═══════════════════════════════════════════════════════════════════

## §9. Metric-verdict-in-derivation-unit ruling (Owner, 2026-07-10) — verbatim carrier

> Metric ruling, binding on all closes (Owner, 2026-07-10): a band's compliance verdict is rendered in the unit the band was derived in — currently raw LoC. LLoC (or any alternate unit) is welcome as a disclosure line, never as the verdict. A builder who believes a different unit is honester proposes it at the next Stage A, where derivation and verdict move together.

Corollaries (builder disclosure, not Owner text):

- **Current unit:** raw LoC. Bands are derived from §6 rate ledger against raw wc-l counts; verdicts are rendered against raw wc-l counts.
- **Disclosure lines allowed:** LLoC, cell count, cyclomatic complexity, docstring density, and any other unit a builder finds informative. These appear as disclosure lines in the close report; they do NOT overturn the raw-LoC verdict.
- **Unit change discipline:** any builder proposing a different unit MUST land the proposal at the next Stage A, with derivation and verdict both in the proposed unit. Mid-close unit-substitution is prohibited.
- **Prior CD close (2026-07-10):** the census-dimensions +45% raw miss is accepted as disclosed under this rule; LLoC 89%-of-top-of-band recorded as disclosure line, not verdict.

═══════════════════════════════════════════════════════════════════

## §10. 9.2 split ruling (Owner, 2026-07-10) — verbatim carrier

> 9.2 split (Owner, 2026-07-10). 9.2a = real perception workers, built and closed on fixtures, venue-agnostic. 9.2b = deployment + census-at-scale + BM-V, gated on 9.2-OWN-1 (topology — owner decision, staked default compute-to-data per the extraction architecture; no external agreement pre-answers it), 9.2-OWN-2 (archive access path — follows OWN-1), 9.2-OWN-3 (post-census validation slice, as restated). P9-E5 bindings carry to 9.2b unchanged: BM-V verdict inside Phase 9, closes on INVESTIGATE, V1 stays PARTIAL until PASS, no production mining on INVESTIGATE.

Applied structural consequences (builder disclosure, not Owner text):

- **9.2a scope:** real perception workers (ASR Whisper-class + diarization) + GPU execution layer + CPU-mode CI + full V1-G roster re-asserted against real workers + P9-E7 rider cell. Data-blind CI (synthetic/public-domain audio fixtures only).
- **9.2a dispatch-independence:** 9.2a is NOT gated on 9.2-OWN-1..3 facts (venue-agnostic build). 9.2b IS gated.
- **9.2b scope:** deployment + census-at-scale + BM-V execution + venue configuration + P9-E5 bindings.
- **9.2b [OWNER] gates carry as originally cited:** 9.2-OWN-1 (topology; owner decision, staked default compute-to-data per extraction architecture; no external agreement pre-answers it) → 9.2-OWN-2 (archive access path; follows OWN-1) → 9.2-OWN-3 (post-census validation slice; restated per 2026-07-09 Owner amendment carrier).
- **P9-E5 bindings** land at 9.2b unchanged: BM-V verdict inside Phase 9, closes on INVESTIGATE, V1 stays PARTIAL until PASS, no production mining on INVESTIGATE.

═══════════════════════════════════════════════════════════════════

## §11. 9.2-OWN resolution (Owner, 2026-07-10) — verbatim carrier

> 9.2-OWN resolution (Owner, 2026-07-10). The extraction topology question is closed on the architecture's own staked default — it was designed, not open.
>
> OWN-1 — RESOLVED: compute-to-data. GPU workers deploy adjacent to the archive, within RMS custody. Raw material never leaves the estate; extracted NormalizedUnits are the only thing that travels. This is the posture the extraction architecture was built around (pull-based seam, purge-per-job with attestation, raw-never-egresses) and it stands as the ruling, not a default awaiting confirmation.
>
> OWN-2 — RESOLVED by consequence: local access at the archive. Workers read RMS storage directly at the venue (mount or local transfer on premises). The physical mechanics — what the archive sits on, what the deployment machines can mount — are day-one deployment findings, not pre-decisions. Same pattern as format/codec verification.
>
> OWN-3 — already satisfied by sequencing. Post-census slice, as restated; nothing exists to do early. Correction riding this ruling: the on-disk OWN-3 wording "on grant compute" is replaced with "at ingest, wherever the run occurs" — venue-neutral, removing a residue of an earlier conflation between an external compute grant and this architecture. No other OWN-3 text changes.
>
> Consequence — 9.2b's gate list collapses to two external actions, both owner-side, neither a design decision: (1) the RMS licensing/access agreement permitting deployment at the archive and read access to it; (2) GPU hardware physically arranged at that venue. When both exist, 9.2b dispatches: deploy → census at scale → BM-V per P9-E5 (closes on PASS or INVESTIGATE; no production mining until PASS). Nothing else gates it.
>
> Update PHASE_STATE and PRD to match: strike "9.2-OWN-1..3 pending owner decisions"; replace with "9.2b awaits: RMS agreement + hardware at venue (owner-side actions). Topology ruled: compute-to-data (§11)."

Applied structural consequences (builder disclosure · not Owner text):

- **9.2-OWN-1 topology:** compute-to-data. Design default; ruled, not open.
- **9.2-OWN-2 archive access path:** local at venue; day-one deployment findings replace pre-decisions.
- **9.2-OWN-3 wording correction:** on-disk carriers replace "on grant compute" with "at ingest, wherever the run occurs" per Owner ruling. Other OWN-3 text unchanged.
- **9.2b gate collapse:** two owner-side external actions remain (RMS agreement + hardware at venue). No design decisions gating 9.2b.
- **P9-E5 bindings unchanged** at 9.2b: BM-V verdict inside Phase 9, closes on PASS or INVESTIGATE, no production mining until PASS.

═══════════════════════════════════════════════════════════════════

## §12 · Close-ratification discipline (Owner, 2026-07-10)

A close whose named gates are green and whose rulings are attested as applied ratifies on its own text. Post-close evidence questions are permitted only where a specific Tier-1 gate is alleged defective, with the allegation named. Conditions attach at ruling time, never at close time. No conditional ratifications on meta-evidence.

## §12.1 · Remaining gates (Owner, 2026-07-10) — complete list

- Tier-1 verbatim ruling loop (frozen contracts, security boundaries, honesty grammar, client promises) — the product itself.
- P9-E5 BM-V bindings (no production mining until PASS) — client-facing quality claim.
- 9.2b's two owner actions (RMS access, hardware at venue) — physical reality, not process.
- §4.2 thresholds and band disclosures — Tier-2, disclosure-only, never blocking.
- Nothing else blocks anything.

## §12.2 · Supersession note (Owner, 2026-07-11)

§12.2 — Supersession note (Owner, 2026-07-11). Two lines of the §12.1 carrier are superseded by later rulings; the carrier above remains byte-identical as historical record.

(a) Line 308 ("9.2b's two owner actions (RMS access, hardware at venue)") is superseded by the §11 correction: 9.2b's gate is the single Owner signal "proceed." The enumeration of owner-side items is struck from all live readings; §11 is authoritative.

(b) Line 310 ("Nothing else blocks anything") is superseded in scope by Registry Doctrine v1.0: from doctrine ratification forward, R4 (Registry row as part of the Tier-1 ruling surface) and D-10 (proposal-time self-audit against D1–D7) are standing submission requirements on every Stage A proposal. They are process obligations, not blocks on the build state — mandate-complete status and the exhaustivity of §12.1's gate list at its time of writing are unaffected.

PBK-1b is discharged by this note.

═══════════════════════════════════════════════════════════════════

## §13 · Registry Doctrine v1.0 in force

§13 — Registry Doctrine v1.0 in force; R4 applies to all subsequent Stage A proposals; defect classes D1–D7 reportable on sight; D-10 self-audit required on every proposal.

Artifact: `/app/docs/governance/registry_doctrine_v1.md` · SHA-256 `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471`.

═══════════════════════════════════════════════════════════════════

## §14 · R4 reflexive placement standing consequence (Owner, 2026-07-11 · from MRR-E4 β)

**§14 — R4 reflexive placement standing consequence (Owner, 2026-07-11 · from MRR-E4 β).** Future phases' R4 reflexive rows land as additive supplements beside a locked source, consolidated into the next Registry version at a future owner-dispatched maintenance turn. MRR-G3's round-trip operates over (v0.md + supplements) ↔ machine form as one set. Applies to any Stage-A → execution phase where a locked source-of-truth prevents in-place R4 row addition.

Ruling ref: `/app/docs/rulings/machine_readable_registry_mrr_e1_to_e4.md`.

═══════════════════════════════════════════════════════════════════

## §15 · Operating Values v1.0 in force (Owner, 2026-07-11)

Operating Values v1.0 in force; consumed by the de-risking sequence, 9.2b deployment, S2.onboard/S4 phases, and BM-C operations; DEFAULT-class values revise via dual-control config swap without reopening the artifact; artifact at `docs/requirements/operating_values_v1.md` SHA-256 `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee`.

═══════════════════════════════════════════════════════════════════

## §16 · D-11 admitted to Registry Doctrine Part IV (Owner, 2026-07-14)

D-11 · Canon before ruling — admitted to Registry Doctrine Part IV at `/app/docs/governance/registry_doctrine_v1.md:97` (SHA of doctrine file post-D-11 = `9dd1cc4bee310ad36780d182377ae8f3e25b7a681430c982dda18d76a408fbcf`). Standing corrective (verbatim): "A closed loop never authorizes the next surface's Stage A; dispatch is the only authorization."

═══════════════════════════════════════════════════════════════════

*End of standing governance record. Effective 2026-07-08 forward + §8 amendment 2026-07-09 + §9 + §10 amendments 2026-07-10 + §11 amendment 2026-07-10 + §12 + §12.1 amendments 2026-07-10 + §13 admission 2026-07-10 + §14 admission 2026-07-11 + §15 admission 2026-07-11 + §16 admission 2026-07-14. On-disk canonical per Standing Rule v3.*
