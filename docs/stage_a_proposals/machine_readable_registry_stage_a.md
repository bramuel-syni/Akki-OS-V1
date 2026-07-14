# Stage A · Machine-Readable Registry (Doctrine §8.1.d)

**Dispatch class:** Registry Doctrine v1.0 §8.1.d (Registry's machine-readable form itself).
**Dispatched:** 2026-07-11 (Owner directive post-Registry-Findings-01..11 close).
**Doctrine SHA:** `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` (in force).
**Standing constraints:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R1..R4 + D-1..D-10 + D1..D7 defect classes · Defect D7 binds · MANDATE-COMPLETE 2026-07-10 held · Parity 31/31.
**Governance basis:** §12 (close-ratification-on-own-text) · §12.1 (Tier-2 driver disclosures never-blocking) · §12.2 (registry doctrine supersession) · §13 (Registry Doctrine v1.0 admitted).

---

## §1. Scope + source-of-truth lock (Owner-verbatim)

**Owner dispatch verbatim (2026-07-11):**
> "Dispatch — Machine-Readable Registry Stage A. Standard loop: Stage A → verbatim relay of Tier-1s → rulings → execution → close.
>
> Scope anchors:
> - Source of truth: `function_promise_registry_v0.md` (SHA `598a7ad4…`) as ruled — **conversion, not authorship**. Every row, finding disposition, and `[OWNER: …]` marker carries over losslessly; **zero content changes ride this phase**.
> - Form: structured file(s) under `docs/registry/` — schema per doctrine §3.2, eleven fields, plus findings status. Format choice (JSON/YAML/one-file/split) is Tier-3 unless the builder identifies a Tier-1 surface in it.
> - Integrity: the human-readable v0 doc and the machine-readable form must not diverge — the mechanism binding them (**generation direction, or a conformance check**) is an expected Tier-1 escalation; do not resolve it silently.
> - Validation: schema conformance mechanically checkable (all mandatory fields, `service_trace` values within S1–S5 vocabulary, governor within the constitution's taxonomy, `unknown` legal where §3.2 says so).
> - R4 reflexive + D-10 self-audit per standing.
> - Out of scope, D7 binding: the standing queries as CI checks (next candidate, separate dispatch), sequencing harness, worker context-harnessing, any Registry content changes, Q2-05 reads.
> - Stage A returns: band in raw LoC with derivation, escalations pre-tiered, verbatim relay for Tier-1s.
> - Parallel, mine, on your word only: Instance Replication Playbook and Commercial Thesis."

**Source-of-truth lock:**
- **`/app/docs/registry/function_promise_registry_v0.md` @ SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`.**
- **Contents:** 47 promises (§2) + 66 function rows (§3) + 5 Q2 orphans (§4) + 6 Q3 gaps (§5) + 11 RULED findings (§7 archival) = **135 domain rows**.
- **Ancillary bound source:** `/app/docs/rulings/registry_findings_01_to_11.md` @ SHA `20e03f4079797307cf08773543577bced2a77fa945cb7cb81e77db5378c94019` (findings dispositions verbatim carrier).

**Conversion posture:** lossless. Zero content authoring. Zero row edits. Zero interpretive additions. Zero synthesis. Every `[RULED · …]` tag, `[OWNER: …]` marker, and doctrine cross-reference carries over byte-identical.

---

## §2. Format shortlist + selection stance (Tier-3 default · Tier-1 surface flagged)

### §2.1 Shortlist considered

| Format | Row density (est. LoC/row) | Human-diff-friendly | Machine-parse-cost | Comments/annotations preserved | Split-friendly |
|---|---:|---|---|---|---|
| **YAML** (single-file) | ~14–18 | GOOD (line-diff clean) | LOW (`pyyaml`/`ruamel`) | YES (native) | YES |
| **JSON** (pretty-printed, 2-space) | ~20–24 | MEDIUM (nested braces noisy) | ZERO (stdlib) | NO (JSON-Schema `description` field only) | YES |
| **JSONL** (line-delimited JSON) | ~1 minified · ~4 pretty | GOOD (row-diff clean) | ZERO (line iterate) | NO | YES (natural) |
| TOML | ~15–20 | MEDIUM (list-of-tables verbose) | LOW (stdlib 3.11+) | YES | MEDIUM |
| CSV | ~1 | POOR (nested arrays lost) | ZERO | NO | POOR |

**Ruled out:** CSV (loses nested `source_citations` arrays + prose fields · violates lossless conversion). TOML (list-of-tables for 66 rows is verbose without gain).

**Working shortlist:** YAML · JSON · JSONL.

### §2.2 Split-file dimension

- **α · single-file** — atomic diff · atomic scan · one file to `sha256sum` for round-trip attest.
- **β · split-by-governor** — 5 governor files (SyniSense/Northena/Mtafiti/Targeta/Solva) + `named_surfaces` + `reflexive_registry_population` + top-level `promises.yaml` + `findings.yaml`. Reduces per-file diff noise; loses atomic-file discipline (round-trip check must aggregate).
- **γ · split-by-record-class** — three files: `promises.{yaml,json}` · `functions.{yaml,json}` · `findings.{yaml,json}`. Preserves atomic top-level record-class discipline; three round-trip attestations instead of one.

### §2.3 Selection stance (Tier-3 default · **coupling to Tier-1 flagged**)

**Builder recommendation (Tier-3 default):** **YAML · γ (split-by-record-class: `promises.yaml` + `functions.yaml` + `findings.yaml`)**.

**Rationale:**
- YAML preserves the comment-carrying discipline of the v0.md source (`[RULED · …]` tags, `source_citations`, doctrine cross-refs land as native YAML strings without escape burden).
- γ split-by-record-class matches the v0.md's own §2/§3/§4-5-7 structural discipline (one file per record class), keeping per-file diffs small and per-file round-trip attest cleanly scoped.
- YAML's line-diff cleanness supports the archival-preservation posture (Standing Rule v3): a superseded finding annotation reads as one comment/field addition, not a nested-brace re-flow.

**Owner-explicit Tier-3 permission:** *"Format choice (JSON/YAML/one-file/split) is Tier-3 **unless the builder identifies a Tier-1 surface in it**."*

**Tier-1 surface identified in format choice: NO — direct format choice is Tier-3.**

**BUT — format choice is materially coupled to MRR-E1 (integrity binding direction)** — see §3.1 below. Depending on MRR-E1 ruling, format choice may be reopened as a downstream ramification (Tier-3 with disclosure). Builder does NOT unilaterally choose format ahead of MRR-E1 ruling.

---

## §3. Pre-tiered escalation matrix (Tier-1 · Tier-2 · Tier-3)

### §3.1 MRR-E1 · Integrity binding direction (**Owner-anticipated Tier-1**)

**Verbatim Owner text:** *"the mechanism binding them (generation direction, or a conformance check) is an expected Tier-1 escalation; do not resolve it silently."*

**Options:**

| Option | Direction | Pros | Cons |
|---|---|---|---|
| **α** | `function_promise_registry_v0.md` (human) → machine form (derived by parser) | Single source of authorship · v0.md remains hand-edited · matches doctrine §3.1 "begins as a governed document and graduates to a machine-readable artifact" | Parser depends on stable v0.md pipe-table format · schema drift in v0.md requires parser rework · machine-form regeneration = automated (no hand-edit permitted) |
| **β** | machine form (hand-authored) → `function_promise_registry_v0.md` (derived by generator) | Machine form is the primary artifact from graduation forward · programmatic queries + sequencing harness operate on canonical source · v0.md becomes rendered view | Owner-directed doctrine says v0.md IS the source-of-truth this phase · β would flip that after Owner-explicit lock · humans lose hand-edit control over the doc |
| **γ** | both hand-maintained + **MRR-G3 conformance-check gate** (mechanical byte-identical round-trip: parse v0.md → serialize machine → parse machine → re-render v0.md diff = empty) | Both forms first-class · humans edit whichever surface fits · gate ensures no drift | Duplicate maintenance burden · edits in one form must be replicated in the other before gate green · gate flakes create merge friction |

**Reflexive R4 registry row** (part of Tier-1 ruling surface) — see §4 below (`registry.machine_form.round_trip`).

**Builder analysis (does NOT resolve):** α is the doctrine-native reading (§3.1 verbatim: *"graduates to a machine-readable artifact"*). β re-anchors the graduation on the machine form (natural once §8.1.a queries + §8.1.b harness land, but premature this phase). γ is the most conservative during graduation transition (both first-class), highest cost. **All three options touch promise-integrity via MRR-G3 mechanism definition — Tier-1.**

### §3.2 MRR-E2 · Findings-status representation shape (**Tier-1 · archival-preservation-posture-touching**)

**Owner-explicit trigger:** *"Findings-status representation shape (in-line tags on rows vs separate findings-table with row-references — if this touches archival-preservation posture, that's Tier-1)."*

**Archival-preservation posture** (Standing Rule v3 · §7 [SUPERSEDED · not deleted]): the v0.md preserves BOTH the original §7 escalation list AND the RULED tags inline in §4/§5 rows. Both surfaces co-exist. The machine form must preserve this **posture** (both surfaces) or lose it (one surface only) — this touches Standing-Rule-v3 archival integrity → **Tier-1**.

**Options:**

| Option | Representation | Preserves archival posture? |
|---|---|---|
| **α** | Inline `rulings: [{id, tag, ref}]` field on affected function/finding rows only. Original §7 not carried in machine form. | NO — original §7 escalation surface (as archival record) is dropped from machine form. Standing Rule v3 archival posture PARTIALLY LOST. |
| **β** | Separate top-level `findings_supersession_ledger` array with per-finding `{finding_id, original_state, superseded_state, ruling_ref}` records; function/finding rows unchanged. | PARTIAL — archival record preserved but disconnected from row-level RULED tags. |
| **γ** | BOTH — inline `rulings` on affected rows + top-level `findings_supersession_ledger` with cross-references. | YES — matches v0.md's dual-surface archival posture 1:1. Lossless. |

**Builder analysis (does NOT resolve):** γ is the byte-identical archival preservation reading; α + β each drop one archival surface. Owner ruling anchors the archival-preservation-posture commitment.

**Reflexive R4 row:** see §4 (`registry.machine_form.findings_coverage`).

### §3.3 MRR-E3 · Vocabulary lock scope (**Tier-1 · promise-integrity-touching**)

**Owner-explicit trigger:** *"Validation gate scope (semantic vs purely mechanical — if the vocabulary lock touches promises-are-honest class, that's Tier-1)."*

**Options:**

| Option | Scope | Class touched |
|---|---|---|
| **α** | Mechanical-only enum lock: `service_trace ∈ {S1.*, S2.*, S3.*, S4.*, S5.*}` · `governor ∈ {SyniSense, Northena, Mtafiti, Targeta, Solva, <named-surface-id>, <registry-population-reflexive>}` · `ladder_rung ∈ {1..4}` · `unknown` accepted where §3.2 permits. Enforces enum membership only. | Mechanical (Tier-3 default IF this is the whole gate). |
| **β** | Semantic promise-integrity lock: **α + `promise` field must reference an existing §2 promise_id (foreign-key style)** — any function citing a promise_id not in the top-level `promises` file fails MRR-G2. | Promise-integrity (promises-are-honest class) — TIER-1. |
| **γ** | Full semantic lock: **β + `service_trace` values must exist in doctrine §Part II journey vocabulary** (validated against a doctrine-derived enum file). Any drift = fail. | Promise-integrity + doctrine-vocab-integrity — TIER-1 with additional coupling to future doctrine-derived vocab file. |

**Builder analysis (does NOT resolve):** α is Tier-3-safe but doesn't attest the lossless-conversion promise (a typo `PROM-S1-external-scoped-acces` [sic] would pass α but silently orphan the row). β catches promise-integrity drift; γ additionally catches service-trace drift. Owner ruling anchors the vocab-integrity commitment.

**Reflexive R4 row:** see §4 (`registry.machine_form.vocabulary_lock`).

### §3.4 MRR-E4 · R4 reflexive placement given source-of-truth lock (**Tier-1 · doctrine-tension-touching**)

**Tension identified (builder analysis):**
- Doctrine R4 verbatim (§3.3): *"New functions register before they land. From ratification forward, any Stage A proposal introducing a gate or worker obligation includes its Registry row; the row is part of the Tier-1 ruling surface."*
- Owner directive verbatim: *"Source of truth: `function_promise_registry_v0.md` (SHA `598a7ad4…`) as ruled — **conversion, not authorship**. … **zero content changes ride this phase**."*

**Tension:** this phase introduces gates (MRR-G1..MRR-G-DataBlind). R4 requires their Registry rows be added. But zero content changes to v0.md means the rows CAN'T land in v0.md this phase. Where do they land?

**Options:**

| Option | Placement | Doctrine posture |
|---|---|---|
| **α** | Rows land in the machine-readable form only (as an appendix section or as first-class function rows). v0.md remains byte-identical at SHA `598a7ad4…`. | Machine form becomes MORE than a conversion of v0.md — it accrues content v0.md lacks. Violates "conversion, not authorship" reading? Or extends it (the reflexive rows are THIS PHASE'S own gates, which is exactly what R4 requires be authored). |
| **β** | Rows land in a supplementary sidecar `function_promise_registry_v0.1_supplement.md` at close, keeping v0.md at SHA `598a7ad4…` byte-identical. Machine form is a lossless conversion of v0.md + supplement together. | Preserves "v0.md byte-identical" reading + honors R4 · adds one artifact class (supplement) previously not extant. |
| **γ** | Rows land in this Stage A proposal (as §4 R4 reflexive attest) and in the close report ONLY. Machine form does NOT carry MRR-* rows; source-of-truth v0.md remains byte-identical; R4 reflexive-attest satisfies §3.3 R4 via the Stage A + close report record, not via Registry membership. | Cleanest source-of-truth-lock reading · leaves R4 reflexive discipline as attest-only (rows exist in on-disk record but not in queryable Registry) · loses reflexive-Registry-membership guarantee for MRR-* gates going forward (they'd have to be added by a future dispatched phase). |

**Builder analysis (does NOT resolve):** all three options honor different aspects of the dispatch. **α** stretches "conversion" but honors R4 reflexive membership; **β** cleanest for lock, adds artifact class; **γ** cleanest for lock, weakens R4 reflexive (attest-only, not queryable). Owner ruling anchors R4-reflexive-membership vs source-of-truth-lock priority.

**Reflexive R4 row FOR THIS ESCALATION ITSELF:** see §4 (`registry.machine_form.reflexive_placement_pending_owner_ruling`) — placement TBD per MRR-E4 outcome.

### §3.5 Tier-2 disclosures (never-blocking · §12.1)

| Disclosure ID | Class | Trigger |
|---|---|---|
| MRR-D2-band | Band-vs-§4.2 threshold position | Estimated band `[1,600, 2,900]` raw LoC crosses §4.2 raw-LoC ceilings materially in some options; §12.1 non-blocking; disclosure ships in close §4.3. |
| MRR-D2-format-scenarios | LoC delta between α/β/γ format options | Format choice materially changes deliverable LoC (700 to 2,900 range across shortlist × split combinations); Tier-3 pending MRR-E1 coupling ramifications. |
| MRR-D2-carve-out-not-applicable | §3.6 governance-doc carve-out precedent NOT applied | Per RP-E5 α (2026-07-11): no case-by-case carve-out precedent. Band applies as-stated per §4.2 raw-LoC discipline. Below/above-band is disclosed, not exempted. |

### §3.6 Tier-3 defaults (builder-decides absent Owner ruling)

| Default ID | Class | Builder default |
|---|---|---|
| MRR-T3-format | Format choice | YAML · γ split (`promises.yaml` + `functions.yaml` + `findings.yaml`) — recommended in §2.3; may reopen post-MRR-E1 ruling. |
| MRR-T3-check-placement | MRR-G3 conformance-check gate placement | Native pytest cell under `/app/backend/tests/registry/test_machine_form_roundtrip.py` (matches existing invariant test convention). |
| MRR-T3-file-location | Machine-form file directory | `/app/docs/registry/machine/` — sibling to v0.md, discoverable by convention. |
| MRR-T3-versioning | Machine-form version tag | `machine_registry_v0.*.yaml` — mirrors `function_promise_registry_v0.md` version tag. |
| MRR-T3-encoding | Character encoding + line-endings | UTF-8 · LF · no BOM (matches all `/app/` conventions). |

### §3.7 Counts

- **Tier-1 count:** **4** (MRR-E1 integrity direction · MRR-E2 findings representation · MRR-E3 vocabulary lock scope · MRR-E4 R4 reflexive placement).
- **Tier-2 count:** 3 (MRR-D2-band · MRR-D2-format-scenarios · MRR-D2-carve-out-not-applicable).
- **Tier-3 count:** 5 (MRR-T3-format · MRR-T3-check-placement · MRR-T3-file-location · MRR-T3-versioning · MRR-T3-encoding).

---

## §4. Registry rows for this phase's own gates (R4 reflexive · §3.2 schema · placement TBD per MRR-E4)

Per Registry Doctrine v1.0 R4: this phase's own gates registered here as part of the Tier-1 ruling surface. **Placement in the machine form vs sidecar vs attest-only depends on MRR-E4 ruling.**

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `registry.machine_form.schema_conformance` (MRR-G1) | Registry (reflexive) | Built to attest every mandatory §3.2 field is present in every row of the machine form and every value matches the schema type. | PROM-registry-schema-integrity (**candidate · new promise · pending Owner ruling on introduction**) | (Registry infrastructure — not a Layer 0 journey step; sub-covered by Q3-real "the Registry itself is a first-class Governor artifact" doctrine §3.6) | `docs/registry/machine/{promises,functions,findings}.yaml` (or per MRR-T3-format) + `backend/tests/registry/test_schema_conformance.py` | Schema validator (pydantic model OR jsonschema lib · pytest cell) | unknown (measured by sequencing harness per §3.2) | v0.md source · schema formalization from doctrine §3.2 | 1 · Deterministic | Owner |
| `registry.machine_form.vocabulary_lock` (MRR-G2) | Registry (reflexive) | Built to attest `service_trace ∈ {S1.*, S2.*, S3.*, S4.*, S5.*}` · `governor ∈` constitution taxonomy · `unknown` accepted only where §3.2 permits. Scope of lock (mechanical vs semantic) per MRR-E3 ruling. | PROM-registry-vocab-integrity (**candidate · new promise · pending Owner ruling**) | (Registry infrastructure) | `backend/tests/registry/test_vocabulary_lock.py` | Enum lint (grep-negative OR jsonschema `enum:` block) | unknown | MRR-E3 ruling (mechanical vs semantic scope) · doctrine §Part II vocab (if MRR-E3 γ) | 1 · Deterministic | Owner |
| `registry.machine_form.round_trip` (MRR-G3) | Registry (reflexive) | Built to attest v0.md ↔ machine form remain in lockstep per MRR-E1 direction: (α) parse v0.md → serialize → diff machine form = empty · (β) parse machine → generate v0.md → diff v0.md = empty · (γ) bidirectional. | PROM-registry-lockstep-integrity (**candidate · new promise · pending Owner ruling**) | (Registry infrastructure) | `backend/tests/registry/test_roundtrip.py` (per MRR-T3-check-placement) | Round-trip generator + byte-identical diff · pytest cell | unknown | MRR-E1 ruling (direction determines the specific generator/parser code) | 1 · Deterministic | Owner |
| `registry.machine_form.findings_coverage` (MRR-G4) | Registry (reflexive) | Built to attest all 11 findings from `rulings/registry_findings_01_to_11.md` are carried in the machine form with disposition tags matching verbatim (`Q2-01 CORRECTED` · `Q2-02 ACCEPTED` · `Q2-03 ACCEPTED` · `Q3-01 RECLASSIFIED` · `Q3-02 OPEN-BY-DESIGN` · `Q3-03 STAYS-IN-L0` · `Q3-05 RECORDED` · `Q3-06 RECORDED` · `Q2-04 ATTACHED-NOT-RETIRED` · `Q2-05 HOLD` · `Q3-04 CONFIRMED-BY-DESIGN`) including all `[OWNER: ...]` markers byte-identical. Representation shape per MRR-E2 ruling. | PROM-registry-findings-preservation (**candidate · new promise · pending Owner ruling**) | (Registry infrastructure · archival posture) | `backend/tests/registry/test_findings_coverage.py` · grep-verify or YAML/JSON-path check | Grep-verify (`assert 11 findings tagged; grep-count match rulings/registry_findings_01_to_11.md`) OR structured-path check | unknown | rulings/registry_findings_01_to_11.md · v0.md §4/§5/§7 · MRR-E2 ruling | 1 · Deterministic | Owner |
| `registry.machine_form.parity_31` (MRR-G-Parity) | Registry (reflexive) | Built to attest V1-G7 parity 31/31 byte-identical is unaffected by this phase (both counts + hashes preserved). | PROM-S1-frozen-wire-contract (**existing** · §2 v0.md line 42 — no new promise) | S1.call (via frozen-wire-contract inheritance) | `backend/tests/invariants/*.contract_snapshot.json` + `backend/contracts/*.py` | `ls | wc -l` + hash-diff | 1 cell · µs class | Existing V1-G7 parity gate | 1 · Deterministic | Owner |
| `registry.machine_form.data_blind` (MRR-G-DataBlind) | Registry (reflexive) | Built to attest no secrets, keys, tokens, or credential material appear in the machine form (regex-negative on standard secret patterns). | PROM-data-blind-posture (**candidate · new promise · pending Owner ruling**) OR PROM-S3-audit-trail-immutable (existing · adjacent · §2 v0.md) | (Registry infrastructure · governance §8 data-blind adjacency) | `backend/tests/registry/test_data_blind.py` | `grep -E "mongodb://[^:]+:[^@]+@|eyJ[A-Za-z0-9_\-]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"` negative | µs class · 1 cell | governance §8 data-blind posture · existing v0.md convention | 1 · Deterministic | Owner |
| `registry.machine_form.reflexive_placement` (MRR-E4-attest) | Registry (reflexive) | Built to attest that MRR-* rows land per MRR-E4 Owner ruling (α machine form · β sidecar supplement · γ attest-only-in-Stage-A-plus-close). Reflexive-of-reflexive: this row itself lands per the same ruling. | PROM-registry-r4-reflexive-membership (**candidate · new promise · pending Owner ruling**) | (Registry infrastructure · doctrine §3.3 R4) | this Stage A §4 table + eventual close-report attest | Doctrine R4 reflexive attest (docs-only) | µs class · 0 cells | MRR-E4 ruling | 1 · Deterministic | Owner |

**Notes on candidate promises:** 5 new promise IDs proposed above (`PROM-registry-schema-integrity` · `PROM-registry-vocab-integrity` · `PROM-registry-lockstep-integrity` · `PROM-registry-findings-preservation` · `PROM-data-blind-posture` OR reuse existing PROM-S3-audit-trail-immutable · `PROM-registry-r4-reflexive-membership`). **Any promise introduction is Tier-1** (touches §2 promise table). Whether these are new promises or subsumed under existing promises is an Owner decision at execution — this Stage A registers the reflexive-R4 candidates only.

**Reflexive of reflexive:** the introduction of new promises for reflexive gates is itself the R4-tension that MRR-E4 escalates (source-of-truth lock says zero content changes to v0.md · but promise introduction is content change).

---

## §5. Schema formalization (per doctrine §3.2 verbatim)

### §5.1 Function-row schema (11 mandatory fields · doctrine §3.2)

| Field | Type | Enumeration / discipline | Source |
|---|---|---|---|
| `function_id` | string · non-empty · unique across Registry · namespaced dot-notation | never reused (§3.2) | doctrine §3.2 line 1 |
| `governor` | string · enum | `SyniSense` \| `Northena` \| `Mtafiti` \| `Targeta` \| `Solva` \| `<named-surface-id>` \| `<registry-population-reflexive>` — no new top-level categories without Owner ruling (§3.2) | doctrine §3.2 line 2 + §3.1 verbatim |
| `mandate` | string · non-empty · active voice · starts with "Built to …" | one sentence, testable, describes what not how (§3.2) | doctrine §3.2 line 3 |
| `promise` | string · non-empty · pipe-delimited multi-value permitted · foreign-key style ref to §2 promise_id (per MRR-E3 β/γ ruling) | R1: no gate without a promise (§3.3) | doctrine §3.2 line 4 |
| `service_trace` | string · non-empty · pipe-delimited multi-value permitted · each ∈ `{S1.*, S2.*, S3.*, S4.*, S5.*}` (per MRR-E3) | R2: no promise without service trace (§3.3) | doctrine §3.2 line 5 |
| `surface` | string · non-empty | module path OR route OR contract OR console element (§3.2) | doctrine §3.2 line 6 |
| `enforcement` | string · enum-class · non-empty | `byte-identity lock` \| `AST/reflection walk` \| `grep-negative` \| `runtime check` \| `E2E cell` \| `type-level wall` \| `constraint-architecture` — `NL-only` illegal per D2 (§3.2) | doctrine §3.2 line 7 + defect D2 |
| `cost` | string · non-empty | free-form; `unknown` legal per §3.2 line 8 verbatim | doctrine §3.2 line 8 |
| `dependencies` | string · may be empty | functions or data required ordered-before (§3.2) | doctrine §3.2 line 9 |
| `ladder_rung` | string · enum | `1 · Deterministic` \| `2 · Classical-NLP` \| `3 · Owned-Model` \| `4 · Frontier-LLM` — written justification required for any rung above cheapest plausible (§3.2) | doctrine §3.2 line 10 + §5.1 |
| `owner` | string · enum | `Owner` \| `builder-Tier-3` \| `dual-control` (§3.2) | doctrine §3.2 line 11 |

### §5.2 Promise-row schema (5 fields · v0.md §2 shape)

| Field | Type | Discipline | Source |
|---|---|---|---|
| `promise_id` | string · non-empty · unique · dot-notation | e.g., `PROM-S1-shield-single-source` | v0.md §2 convention |
| `text` | string · non-empty | promise text phrased so its breach is observable (§3.2 R2 posture) | v0.md §2 + doctrine §3.2 line 4 |
| `active` | boolean | v0.md §2 uses `yes/no` — lossless map to `true/false` | v0.md §2 convention |
| `functions_that_cite` | integer · ≥ 1 (per R1) | number of §3 rows citing this promise | v0.md §2 convention |
| `source_citations` | array of strings · non-empty | verbatim doctrine / mandate / close-report references | v0.md §2 convention |

### §5.3 Finding-row schema (v0.md §4/§5 shape)

| Field | Type | Discipline |
|---|---|---|
| `finding_id` | string · non-empty · unique | `Q2-01`..`Q2-05` · `Q3-01`..`Q3-06` |
| `subject` | string · non-empty | gate identifier(s) OR journey step |
| `source` | string · non-empty | close-report path OR doctrine §-ref |
| `observation` | string · non-empty | verbatim from v0.md §4/§5 |
| `escalation_marker` | string · optional | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` OR similar |
| `ruling_ref` | string · optional | `rulings/registry_findings_01_to_11.md §N` |
| `ruling_tag` | string · optional | `[RULED · Q2-01-CORRECTED · …]` verbatim |
| `owner_markers` | array of strings · optional | `[OWNER: future phase]` · `[OWNER: buyer-commercial-tier]` · etc. |

### §5.4 Findings-supersession-ledger (per MRR-E2 γ · IF ruled)

| Field | Type | Discipline |
|---|---|---|
| `finding_id` | string · non-empty · unique | matches §5.3 `finding_id` |
| `original_state` | string · non-empty | pre-ruling escalation state (verbatim from v0.md §7 original enumeration) |
| `superseded_state` | string · non-empty | `[SUPERSEDED · RULED …]` verbatim from v0.md §7 annotation |
| `ruling_ref` | string · non-empty | `rulings/registry_findings_01_to_11.md §N` |
| `ruling_date` | string (ISO date) | `2026-07-11` |

---

## §6. Validation gates (proposed · scope depends on Tier-1 rulings)

| Gate | Purpose | Test cell (per MRR-T3-check-placement default) | Depends on |
|---|---|---|---|
| **MRR-G1** | Schema conformance — every mandatory §5.1/§5.2/§5.3 field present + types match. | `test_schema_conformance.py` | schema formalization (§5) |
| **MRR-G2** | Vocabulary lock — enum membership + `unknown` acceptance per §3.2. Scope: MRR-E3 ruling (α mechanical · β +promise-FK · γ +service-trace-doctrine-vocab). | `test_vocabulary_lock.py` | MRR-E3 |
| **MRR-G3** | Round-trip integrity — human ↔ machine lockstep per MRR-E1 direction. | `test_roundtrip.py` | MRR-E1 |
| **MRR-G4** | Findings-status coverage — all 11 RULED findings + all `[OWNER: …]` markers carried byte-identical; representation shape per MRR-E2. | `test_findings_coverage.py` | rulings/registry_findings_01_to_11.md · MRR-E2 |
| **MRR-G-Parity** | V1-G7 parity 31/31 byte-identical unaffected. | existing `test_parity_31.py` (already green) | none new (existing gate) |
| **MRR-G-DataBlind** | No secrets/keys/tokens in machine form. | `test_data_blind.py` | governance §8 data-blind |

**All gates ladder_rung 1 · Deterministic. All gates enforcement-class mechanical (schema validator · enum lint · round-trip diff · grep-verify · fs-count · grep-negative-regex).**

---

## §7. Findings status carry-over verification (11 items · verbatim from `rulings/registry_findings_01_to_11.md` + v0.md §4/§5/§7)

Every finding below MUST appear in the machine form with its `[RULED · …]` tag byte-identical, including all `[OWNER: …]` markers. Verified against source docs at Stage A time; this list is the MRR-G4 attest surface at execution.

| # | Finding | RULED tag (verbatim) | `[OWNER: …]` marker | Ruling ref |
|---|---|---|---|---|
| 1 | Q2-01 | `[RULED · Q2-01-CORRECTED · rulings/registry_findings_01_to_11.md §1 · attach to new PROM-S1-external-scoped-access (BCR §3.9 EE-R2 + EE-R4 verbatim); strike tentative PROM-S1-provable-envelope-inheritance; trace S1.register + S1.scoped-key confirmed.]` | — | rulings §1 |
| 2 | Q2-02 | `[RULED · Q2-02-ACCEPTED]` | — | rulings §2 |
| 3 | Q2-03 | `[RULED · Q2-03-ACCEPTED · policy-prose-recovery-is-legitimate-archaeology]` | — | rulings §3 |
| 4 | Q3-01 | `[RULED · Q3-01-RECLASSIFIED · narrowed-scope · envelope-completeness-cell-is-legitimate-future-check]` | — | rulings §4 |
| 5 | Q3-02 | `[RULED · Q3-02-OPEN-BY-DESIGN · never-retired · never-papered]` | `[OWNER: future phase]` | rulings §5 |
| 6 | Q3-03 | `[RULED · Q3-03-STAYS-IN-L0 · surface-restores-when-a-commercial-posture-is-ruled · retiring-would-let-implementation-event-edit-product-definition]` | `[OWNER: buyer-commercial-tier]` | rulings §6 |
| 7 | Q3-05 | `[RULED · Q3-05-RECORDED · candidate + sub-coverage-indirect]` | — | rulings §7 |
| 8 | Q3-06 | `[RULED · Q3-06-RECORDED · candidate + half-surface-tested-is-what-Q3-exists-to-show]` | — | rulings §8 |
| 9 | Q2-04 | `[RULED · Q2-04-ATTACHED-NOT-RETIRED · PROM-S1-frozen-wire-contract · Q1-candidate]` | — | rulings §9 |
| 10 | Q2-05 | `[RULED · Q2-05-HOLD · individual-read-at-future-Registry-maintenance · AF-G1-repointed-rows-keep-attachment]` | — | rulings §10 |
| 11 | Q3-04 | `[RULED · Q3-04-CONFIRMED-BY-DESIGN · closed]` | — | rulings §11 |

**Attest at Stage A time:** all 11 present in v0.md §4/§5 (grep-verified) and §7 (SUPERSEDED archival). Byte-identical carry-over is the MRR-G4 acceptance criterion at execution.

---

## §8. Band in raw LoC (α/β/γ scenarios · derivation stated)

### §8.1 Derivation

**Domain-row inventory (from v0.md @ SHA `598a7ad4…`):**
- 47 promise rows (§2) — 5 fields each per §5.2 schema.
- 66 function rows (§3) — 11 fields each per §5.1 schema.
- 11 finding rows (§4 + §5 · 5 Q2 + 6 Q3) — ~8 fields each per §5.3.
- Optional §5.4 supersession ledger — 11 records × 5 fields (only if MRR-E2 γ ruled).

**Structural cost:** schema definition file (~40-80 LoC), governance header (~10-30 LoC per file), gate cell attests (6 MRR gates × ~10-25 LoC per pytest cell · **NOT in the machine form itself — the pytest cells are separate; the machine form only carries the R4 reflexive Registry rows if MRR-E4 rules α**).

### §8.2 Scenario table (raw LoC)

Per-format estimates rounded from row-density × row-count + structural overhead. **These are ESTIMATES computed at Stage A; execution band actuals will be reported per §9.**

| Scenario | Format · split | Est. raw LoC (deliverable file[s] only) | R4 reflexive rows (per MRR-E4) |
|---|---|---:|---|
| **α₁** | YAML · single-file (`machine_registry_v0.yaml`) | **~1,700 – 2,200** (16 LoC/row × 124 rows + 200 LoC overhead) | +100–140 LoC if MRR-E4 α (rows in file); +0 if γ (attest-only) |
| **α₂** | YAML · γ split (3 files: promises/functions/findings) | **~1,800 – 2,400** (as α₁ + 3 file headers + optional supersession ledger if MRR-E2 γ ~50-100 LoC) | same as α₁ |
| **β₁** | JSON · single-file (pretty-printed) | **~2,400 – 2,900** (22 LoC/row × 124 rows) | same |
| **β₂** | JSON · γ split | **~2,600 – 3,100** | same |
| **γ₁** | JSONL · single-file (line-per-record, pretty inner) | **~550 – 900** (4 LoC/row × 124 rows) | same |
| **γ₂** | JSONL · γ split (3 `.jsonl` files) | **~600 – 950** | same |

### §8.3 Proposed band + §4.2 disclosure

**Proposed band (encompassing shortlist α₁..β₂ excluding JSONL outliers):** **`[1,600, 3,000]` raw LoC.**

- **JSONL (γ₁/γ₂) — below-band-bottom by ~65-70%** if selected; disclosed as Tier-2 (MRR-D2-format-scenarios) non-blocking per §12.1. JSONL's high compression is a genuine efficiency signal, not under-population.
- **YAML α₁/α₂** — within band.
- **JSON β₁/β₂** — within band or top-edge; β₂ may exceed band ceiling → Tier-2 (MRR-D2-band) disclosure at close per §12.1.
- **§4.2 raw-LoC thresholds:** ~2,900 raw LoC is a materially high per-file value; §12.1 states thresholds are Tier-2 disclosures never blocking. Fixture Refresh precedent (782 vs `[1,200, 1,800]` accepted-as-disclosed) + Registry Population precedent (458 vs `[1,300, 2,900]` BELOW-BOTTOM accepted-as-disclosed) apply.
- **§3.6 governance-doc carve-out precedent:** per RP-E5 α (2026-07-11) — NOT applied case-by-case; band applies as-stated. Explicit disclosure at close §4.3.

### §8.4 R4 reflexive placement LoC delta (per MRR-E4 ruling)

- **MRR-E4 α** (rows in machine form): +100–140 LoC (7 reflexive rows × ~15-20 LoC in YAML).
- **MRR-E4 β** (rows in sidecar supplement): +0 LoC in machine form; ~150 LoC in new sidecar file (separately banded).
- **MRR-E4 γ** (attest-only in Stage A + close): +0 LoC in machine form; already counted in this Stage A doc.

---

## §9. Out-of-scope statement (D7 binding · Owner-verbatim)

**Verbatim from Owner dispatch (§1 above):**
> "Out of scope, D7 binding: the standing queries as CI checks (next candidate, separate dispatch), sequencing harness, worker context-harnessing, any Registry content changes, Q2-05 reads."

**Explicitly out of scope this phase:**
1. **Standing queries as CI checks** — doctrine §8.1.a · **next candidate, separate dispatch** (Owner-verbatim). This Stage A does NOT scaffold, preview, or reference-as-next any specific Q1/Q2/Q3 executable-check cells.
2. **Sequencing harness** — doctrine §8.1.b + §5.2 · not touched.
3. **Worker context-harnessing** — doctrine §8.1.c + §6.2 · not touched.
4. **Any Registry content changes** — source-of-truth locked at `function_promise_registry_v0.md` @ SHA `598a7ad4…`. Zero authoring, zero row edits, zero content additions to v0.md this phase. (R4 reflexive placement for MRR-* gates is exactly the MRR-E4 Tier-1 escalation.)
5. **Q2-05 reads** — Owner-explicit HOLD 2026-07-11 per `rulings/registry_findings_01_to_11.md §10`. Individual-read is future Registry-maintenance turn; no touch this phase.

**Parallel Owner-side items (builder does NOT touch, does NOT reference-as-next):**
- **Instance Replication Playbook** — doctrine §8.1 documents class · **"Parallel, mine, on your word only"** (Owner-verbatim).
- **Commercial Thesis** — doctrine §8.1 documents class · **"Parallel, mine, on your word only"** (Owner-verbatim).

**D7 defect class binding:** any scope beyond this dispatch = defect D7. Gap-fill cells and future dispatches are candidates for future Owner-dispatched phases, NOTHING MORE.

---

## §10. D-10 self-audit (rides submission · Registry Doctrine v1.0 verbatim)

Per doctrine D-10: *"every proposal self-audits against defect classes D1–D7 before submission."*

| Class | Verdict | One-line reason |
|---|---|---|
| **D1 · Orphan gate** | **PASS** | Every MRR-G# gate in §4 has a promise field stated (candidate or existing) + service_trace context (`Registry infrastructure` sub-covered by doctrine §3.6 "Registry pays rent") + surface + enforcement class. Zero orphans in Stage A itself; final promise reconciliation lands at Owner Tier-1 ruling on candidate promises. |
| **D2 · NL-only enforcement** | **PASS** | Every MRR-G# gate's enforcement class is machine-mechanical (schema validator · enum lint · round-trip diff · grep-verify · fs-count · grep-negative-regex). Zero NL-only values proposed. |
| **D3 · Curated verdict** | **PASS** | Escalation matrix (§3) surfaces all Owner-anticipated Tier-1s + builder-identified Tier-1s (MRR-E4 R4 reflexive tension) without pre-resolving. Format shortlist (§2) states shortlist + rationale; no favorability bias. Findings carry-over §7 is grep-verified against v0.md + rulings verbatim. |
| **D4 · Rung inflation** | **PASS** | All 6 MRR-G# gates ladder_rung `1 · Deterministic`. Zero rung inflation. Justification: each gate is a mechanical check (schema · enum · diff · grep · fs-count) — deterministic is the cheapest plausible rung. |
| **D5 · Meta-spiral** | **PASS** | This Stage A proposes the machine-readable form of the existing Registry — NOT a new governance layer above the Registry. The Registry remains the primary artifact per doctrine §3.6. Reflexive R4 rows (§4) register the phase's own gates INTO the Registry (per MRR-E4 α/β) OR attest them via the Stage A + close on-disk record (per MRR-E4 γ); either way, no second-order governance layer created. |
| **D6 · Service conflation** | **PASS** | Registry infrastructure is service-blind (doctrine §3.6 "Registry pays rent" — one canonical artifact serving S1..S5 uniformly). No persona optimization. `governor: Registry (reflexive)` used for MRR-* rows explicitly denotes non-service-persona. |
| **D7 · Invented schedule or scope** | **PASS** | Only the 4 Owner-directed workstreams surfaced (schema formalization · format shortlist · integrity binding escalation · R4 reflexive attest). Explicit out-of-scope list at §9 verbatim from Owner. Zero references to standing queries as CI · sequencing harness · worker context-harnessing · Registry content changes · Q2-05 reads. Zero references to Instance Replication Playbook or Commercial Thesis (Owner-parallel). Zero next-cell scaffolds. |

**Self-audit verdict:** all 7 defect classes **PASS**. Doctrine D-10 discipline held.

---

## §11. Reply body per Standing Rule v3 (to be emitted by builder to Owner after this Stage A lands)

The builder emits to Owner:
1. SHA of `/app/docs/stage_a_proposals/machine_readable_registry_stage_a.md` (this file).
2. Pre-tiered escalation matrix summary: **Tier-1 count 4** · **Tier-2 count 3** · **Tier-3 count 5**.
3. Tier-1 surfaces named verbatim: **MRR-E1** (integrity binding direction · α/β/γ) · **MRR-E2** (findings-status representation shape · α/β/γ) · **MRR-E3** (vocabulary lock scope · α mechanical / β +promise-FK / γ +service-trace-doctrine-vocab) · **MRR-E4** (R4 reflexive placement given source-of-truth lock · α machine form / β sidecar supplement / γ attest-only).
4. D-10 self-audit result: **D1..D7 all PASS** (one-line reason each per §10).
5. R4 reflexive attest: **7 gates registered at §4** (MRR-G1 schema · MRR-G2 vocab · MRR-G3 round-trip · MRR-G4 findings-coverage · MRR-G-Parity · MRR-G-DataBlind · MRR-E4-attest) — placement TBD per MRR-E4 ruling.
6. Band raw LoC scenarios with derivation: **shortlist band `[1,600, 3,000]`** (YAML α₁/α₂ within; JSON β₁/β₂ within or top-edge; JSONL γ₁/γ₂ below-band-bottom by ~65-70% · disclosed Tier-2).
7. Confirmation: source-of-truth locked at v0.md SHA `598a7ad4…` · zero content changes · zero authoring · lossless conversion.
8. Format shortlist + selection stance: shortlist YAML · JSON · JSONL · γ split-by-record-class recommended (YAML γ default per Tier-3 §3.6 MRR-T3-format) · **Tier-1 surface in format choice: NO** direct; **format choice is materially coupled to MRR-E1 ramifications** — reopen post-ruling permitted under Tier-3 disclosure.

---

## §12. Standing constraints preserved

- **Defect D7 binds:** no code · no CI · no query automation · no harness · no worker wiring · no Playbook/Thesis content · no Registry content changes · no Q2-05 reads · no next-cell scaffolds.
- **MANDATE-COMPLETE 2026-07-10 held.** Registry Doctrine v1.0 in force. R4 reflexive + D-10 self-audit applied at Stage A time (this doc).
- **Parity 31/31 preserved:** doc-only Stage A landing.
- **Standing Rule v3:** on-disk canonical · SHA in reply body · no inline code dumps.
- **Governance §12/§12.1/§12.2/§13** in force. Shield chokepoint · 4-code refusal registry closed · MONGO_URL / DB_NAME / REACT_APP_BACKEND_URL protected variables untouched.
- **Standing loop:** Stage A → verbatim Tier-1 relay to Owner → rulings → atomic execution → close. **No execution this reply.** No file writes to `docs/registry/*.json` or `*.yaml`. No conversion performed yet.

═══════════════════════════════════════════════════════════════════

*End of Stage A · Machine-Readable Registry. Landing per Standing Rule v3 · on-disk canonical. Reflexive R4 attest at §4. D-10 self-audit at §10. 4 Tier-1 escalations pre-tiered at §3 for verbatim relay to Owner. Post-landing state: idle awaiting Owner Tier-1 rulings via verbatim relay.*
