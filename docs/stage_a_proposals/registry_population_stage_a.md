# Registry Population Stage A · §3.5 archaeology

**Dispatch:** Owner 2026-07-11 · Registry Population (§3.5 archaeology of the Function & Promise Registry per Registry Doctrine v1.0).
**Basis:** `/app/docs/governance/registry_doctrine_v1.md` SHA `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` · §3.2 schema · §3.4 queries · §3.5 population posture · §3.6 rent-paying discipline.
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md` (through §13). §9 metric-verdict-in-raw-LoC. §12 close-ratification-on-own-text. **§13 Registry Doctrine v1.0 in force.**
**Standing Rule v3:** on-disk canonical.
**MANDATE-COMPLETE 2026-07-10 held.** Parity 31. This is a doc-only extraction phase — no code, no CI change, no query automation, no harness, no worker wiring.

---

## §1. Owner dispatch — verbatim carrier

> Dispatch — Registry Population Stage A (§3.5 archaeology). Standard loop: Stage A → verbatim relay of Tier-1s → rulings → execution → close.
>
> Scope anchors:
> - Extraction, not authorship: populate the Registry per doctrine §3.2 schema from the on-disk record — governor mandate documents, rulings records, close-report gate rosters, BCR v1.5. Every Tier-1 escalation already carries a "Promise protected" line; that is the primary vein.
> - Promise-first ordering: extract the promise set first (expected: dozens, not hundreds), then attach functions to promises. The small set is the product; the function rows are the derivation.
> - Coverage target: every gate in the current CI roster (~1,400 cells map to far fewer named functions — cells group under their gate/function identity), every governor behavior named in the mandates, every console guarantee under UI-Spec binding copy.
> - Q2/Q3 as first outputs: where extraction finds a gate whose promise cannot be recovered → Q2 orphan finding, listed, not invented around. Where a Layer 0 journey step resolves to no function → Q3 gap finding, listed. These findings lists are deliverables of this phase, not defects in it — the Registry earning rent on day one.
> - Format: `docs/registry/function_promise_registry_v0.md` — one artifact, §3.2 schema, human-readable tables. Machine-readable form is explicitly out of scope (future dispatch).
> - Cost fields: "unknown" is legal per §3.2; populate what the close reports already state (cell counts, rate classes), estimate nothing.
> - Stage A returns: band in raw LoC (doc LoC counts; derivation stated), escalations pre-tiered — expected Tier-1 surfaces: promise-consolidation judgment calls (when two "Promise protected" lines are one promise vs two) and any Q2/Q3 finding that touches a client promise. R4 applies reflexively: this phase's own checks register themselves.
> - Out of scope, D7 binding: no code, no CI changes, no query automation, no harness, no worker wiring, no Playbook/Thesis content.

---

## §2. Scope + design

### §2.1 What lands (execution scope · informs Stage A gate roster)

**Target artifact (single deliverable):**

`/app/docs/registry/function_promise_registry_v0.md` — one human-readable markdown file · §3.2 schema · sectioned as follows:

- **§0 · Preamble** — doctrine reference · population methodology · rent-paying attest (§3.6).
- **§1 · Layer 0 service sentences (S1–S5)** — quoted verbatim from Registry Doctrine v1.0 Part II · read-only anchor (Owner-authoritative).
- **§2 · Promise table** — the extracted small set. Columns: `promise_id · promise_text · client_facing? · protected_by (count of functions) · source_citations`. Expected count: dozens, not hundreds. Consolidation rule ruled at RP-E1.
- **§3 · Function tables per governor** — one table per S1..S5 governor (SyniSense · Northena · Mtafiti · Targeta · Solva) + one table for UI-console guarantees. Each row: §3.2 schema (11 fields) verbatim.
- **§4 · Q2 orphan findings** — gates whose promise cannot be recovered from the on-disk record. Listed, not invented around. Deliverable of this phase per Owner-explicit framing.
- **§5 · Q3 gap findings** — Layer 0 journey steps with no enforcing function. Listed. Deliverable of this phase.
- **§6 · Coverage attest** — CI roster count (observed) vs extracted function count · consolidation ratio · Q2/Q3 counts.
- **§7 · R4 reflexive rows** — this Stage A's own gates (RP-G1..RP-G6) plus the Registry-population-phase functions themselves, registered per §3.2 schema (recursion closed at rent-paying attest).

**Machine-readable form: OUT OF SCOPE (D7 binding).** No JSON/YAML derivation, no schema validator, no runtime introspection. Doctrine §8.1 code-level item (a) enters only via future Owner dispatch.

### §2.2 What is preserved byte-identical (Tier-1 non-negotiable)

- **All 31 frozen contracts** — untouched. Parity stays at 31 (RP-G-Parity attests).
- **4-code auth-refusal registry** — untouched.
- **Refusal taxonomy** — untouched.
- **Shield chokepoint** (`test_no_direct_llm_calls_outside_shield`) — untouched. This phase does no LLM code work.
- **All CI test files** — untouched. This phase READS from them; adds nothing.
- **All mandate documents** — read-only extraction source. Never amended.
- **All rulings records** — read-only. Standing Rule v3 archival immutability held.
- **All close reports** — read-only. Standing Rule v3 held.
- **Registry Doctrine v1.0** — read-only. Doctrine is authority-source; this phase applies it.
- **Governance §13 §12.2 §12.1 §12** — read-only. Doctrine + supersession note held.
- **MANDATE-COMPLETE 2026-07-10 status** — held.

### §2.3 Extraction methodology (promise-first ordering)

**Primary vein: Tier-1 "Promise protected" lines from rulings + Stage A proposals.**

Verbatim mechanical extraction from:
- `/app/docs/rulings/*.md` (11 files) — every Tier-1 escalation carries the phrase.
- `/app/docs/stage_a_proposals/*.md` — Tier-1 escalation blocks quote "Promise protected:" verbatim (35+ matches observed at Stage A scan).

Each hit is a candidate promise-row. Consolidation judgment (RP-E1) determines when two hits collapse to one promise.

**Secondary veins:**

1. **Governor behaviors named in mandate documents** — extraction sources:
   - `/app/docs/mandates/RMS_Product_Engineering_Spec_v3.md`
   - `/app/docs/mandates/RMS_UX_Architecture_v2.md`
   - `/app/docs/mandates/RMS_UI_Specification_v1.md`
   - `/app/docs/mandates/RMS_UI_Specification_v2_1.md`
   - `/app/docs/mandates/RMS_UI_Specification_v2_2.md`
   - `/app/docs/mandates/RMS_Build_Completion_Requirements_v1_5.md`
   - `/app/docs/mandates/RMS_Mtafiti_Specification.md`
   - `/app/docs/mandates/RMS_Solva_Specification.md`
   - `/app/docs/mandates/RMS_Targeta_Specification.md`
   - `/app/docs/mandates/northena.md`
2. **Console guarantees under UI-Spec binding copy** — UI Specification v1/v2.1/v2.2 §-labeled promises (e.g., §3.1 Ask "single-ingress" · §3.2 Answer "class + receipt intact").
3. **Close-report gate rosters** — `/app/docs/close_reports/*.md` (31 files). Each close's gate table names its Tier-1 gates + their promises.
4. **BCR v1.5** — `/app/docs/mandates/RMS_Build_Completion_Requirements_v1_5.md` §3.1..§3.15 lands the product-level promise catalog.

**Function attachment:** every named gate identifier (pattern `[GOVERNOR]-G[N]` / `[GOVERNOR]-E[N]` / `[GOVERNOR]-R[N]`) in the close-report roster becomes a candidate function row. Cells grouped under their gate/function identity (e.g., `PH-G3` has 4 cells but registers as one function).

**Observed CI roster (as of Stage A scan, 2026-07-11):**
- Pytest total cells: **1,202 passed + 1 skipped** (per PH-R1 close · same 1,202 baseline held through §12.2 landing).
- Jest cells: **151** (post Ask Console nav landing).
- Playwright chromium cells: **55**.
- **Grand total: 1,408 cells** (aligns with Owner's "~1,400 cells" estimate).
- **Distinct named-gate identifiers observed:** 134 unique `[XX]-G[N]` / `[XX]-E[N]` / `[XX]-R[N]` patterns across `docs/close_reports/*.md`. This is the upper bound of function-row count before promise-consolidation grouping.
- **Expected extracted function count:** 60–100 named functions after cell-grouping + consolidation (RP-E1). Cells collapse into functions via shared gate identity; functions collapse into promises via shared "Promise protected" text at RP-E1 α (proposed).

### §2.4 Data-blind + honesty-grammar posture attest

- **Governance §8 data-blind posture:** the Registry catalogues promise-text verbatim from on-disk sources; **NO secret values** may appear in any registry row. All secret material stays in vault-class stores (per PH-E1 α).
- **Registry Doctrine D-3 (conflation test):** every proposed row cites its Layer 0 sentence (S1–S5) in the `service_trace` field. Rows failing this attest are Q2 orphan findings (deliverable, not invented around).
- **Registry Doctrine D-5 (NL-only enforcement is defect D2):** the enforcement field values are restricted to the §3.2 enumeration (`byte-identity lock · AST/reflection walk · grep-negative · runtime check · E2E cell · type-level wall · constraint-architecture`). "NL-only" is NOT a legal value.
- **Registry Doctrine D-8 (reduction applies to its own output):** the Registry itself is subject to the three queries; if it stops earning rent it retires under Owner ruling (§3.6).
- **Registry Doctrine §3.5 archaeology, not authorship:** where an extracted gate lacks a recoverable promise, it becomes a Q2 finding — the raw material is on disk, we invent nothing.
- **Standing Rule v3:** on-disk canonical.
- **Governance §9 metric-verdict-in-raw-LoC:** deliverable band derived from raw LoC of the target artifact.
- **Governance §11 (9.2b single-signal gate):** untouched.
- **P9-E5 bindings:** untouched.

---

## §3. Band derivation — RAW LoC per governance §9

The deliverable is a single doc `function_promise_registry_v0.md`. Section-by-section LoC estimates:

| Section | Rate class | Est. LoC (α · full) | Est. LoC (β · consolidated) | Est. LoC (γ · minimal-skeleton) |
|---|---|---:|---:|---:|
| §0 Preamble (doctrine ref · methodology · rent attest) | §6.9 verbatim carrier | 80 | 60 | 40 |
| §1 Layer 0 (S1–S5 verbatim from doctrine) | §6.9 verbatim carrier | 40 | 40 | 40 |
| §2 Promise table (~80 α · ~60 β · ~40 γ rows @ 6 LoC/row incl header) | §6.1 catalog table | 500 | 380 | 260 |
| §3.a SyniSense function table (~30 α · ~22 β · ~14 γ rows @ 14 LoC/row incl schema block) | §6.1 catalog table | 460 | 340 | 220 |
| §3.b Northena function table (~15 · ~11 · ~7 rows) | §6.1 catalog table | 230 | 170 | 110 |
| §3.c Mtafiti function table (~12 · ~9 · ~6 rows) | §6.1 catalog table | 180 | 140 | 90 |
| §3.d Targeta function table (~8 · ~6 · ~4 rows) | §6.1 catalog table | 130 | 100 | 65 |
| §3.e Solva function table (~10 · ~7 · ~5 rows) | §6.1 catalog table | 150 | 110 | 80 |
| §3.f UI console guarantees (~15 · ~11 · ~8 rows) | §6.1 catalog table | 230 | 170 | 130 |
| §4 Q2 orphan findings (est. 5–15 · 20–40 LoC per finding) | §6.1 finding table | 320 | 220 | 120 |
| §5 Q3 gap findings (est. 3–10 · 25–50 LoC per finding) | §6.1 finding table | 280 | 200 | 100 |
| §6 Coverage attest | §6.1 classic | 60 | 50 | 40 |
| §7 R4 reflexive rows (this phase's own gates RP-G1..G6) | §6.1 catalog | 90 | 90 | 90 |
| **Total raw LoC** | | **2,750** | **2,070** | **1,385** |

**Proposed band (raw LoC per §9):** `[1,300, 2,900]` — brackets all three scenarios with headroom (γ at 1,385 · β at 2,070 · α at 2,750).

Band-relative trichotomy per §9:
- below-bottom (< 1,300) — Tier-2 driver disclosure
- in-band ([1,300, 2,900]) — no disclosure beyond snapshot line
- above-top (> 2,900) — Tier-2 driver disclosure

### §3.1 §4.2 threshold statement (Tier-2 disclosure · never blocking per §12.1)

- **Raw LoC threshold (1,500):** **projected-CROSSED in α and β scenarios · projected-NOT-crossed in γ.** Doc-only extraction phase; disclosure per §12.1 (Tier-2, disclosure-only, never blocking).
- **Cell count threshold (60):** N/A — this phase adds NO test cells. R4 reflexive rows (§7) are Registry rows, not test cells.
- **Governance-doc carve-out precedent (§3.8 STEP-A → close reasoning):** the target artifact `function_promise_registry_v0.md` is a governance-class deliverable (Registry per doctrine §3.6 pays rent via §3.4 queries, not via LoC). Per the §3.8 close precedent — governance/rulings docs never counted in the band's derivation — reasoning is presented explicitly here for Owner ruling: **is the Registry an artifact whose LoC counts in the band derivation (α), or is it governance-class (β) and the band is derived only from the ancillary rulings + close reports at execution close?** RP-E5 escalates this posture.
- **Disposition anticipated: atomic single commit per §4.1 baseline** (doc lands as one artifact + close report). Dev's judgment per Owner delegation; split-fallback autonomous if extraction narrative fractures at a natural seam.

---

## §4. Standing constraints preserved at close (attested pre-execution)

| Constraint | Attest at execution |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical | GREEN — no code, no contract touch (RP-G-Parity attests) |
| 4-code auth-refusal registry closed | GREEN — no auth surface touched |
| No HTTP 409 in new/modified files (E5) | GREEN — doc-only |
| Standing Rule v3 (on-disk canonical) | GREEN — Stage A + rulings + close all on-disk |
| AS-H1 retention held-class (no DELETE) | GREEN — no DELETE surface touched |
| Governance §8 data-blind posture | GREEN — no secret values in registry rows (RP-G-DataBlind attests) |
| Governance §9 metric-verdict-in-raw-LoC | GREEN — verdict in raw LoC |
| Governance §10 9.2 split ruling | GREEN — Registry Population is dispatch-independent from 9.2a/9.2b |
| Governance §11 9.2b single-signal gate | GREEN — untouched |
| Governance §12/§12.1/§12.2 | GREEN — Registry Doctrine v1.0 authoritative post-§13 |
| Governance §13 Registry Doctrine v1.0 in force | GREEN — this Stage A is Registry Doctrine's first invocation |
| Shield chokepoint | GREEN — no LLM code work |
| MONGO_URL / DB_NAME / REACT_APP_BACKEND_URL protected variables | GREEN — never modified |
| P9-E5 BM-V bindings (no production mining until PASS) | GREEN — untouched |
| MANDATE-COMPLETE 2026-07-10 | GREEN — held (Registry population extends, does not re-open) |
| Registry Doctrine R1..R4 | GREEN — R4 applied reflexively (§7) |
| Registry Doctrine D-1..D-10 | GREEN — D-10 self-audit landed §7.1 |
| Registry Doctrine D1..D7 defect classes | GREEN — Q2/Q3 findings surface D1 orphans + D6 conflations as deliverables, not defects in this phase |

---

## §5. Gate roster (RP-G1..RP-G6 + auxiliary · R4 reflexive)

**Doc-only phase · zero code cells.** These gates are Registry-check functions to be attested at close-time on the extracted deliverable itself. Enforcement class: mechanical text-inspection of `function_promise_registry_v0.md`.

| Gate | Tier | Enforcement class | Purpose |
|---|---|---|---|
| **RP-G1** promise-set-completeness | Tier-1 (client-promise vein integrity) | grep-negative + AST-of-markdown | Every "Promise protected" line in the source corpus resolves to a promise-row in §2 of the deliverable OR appears in §4 Q2 orphan (recoverable-promise-fail). |
| **RP-G2** function-attachment-completeness | Tier-1 (§3.3 R3) | grep-negative | Every named gate identifier in the CI roster / close-report gate rosters has a function-row in §3 OR appears in §4 Q2 orphan. |
| **RP-G3** schema-conformance | Tier-1 (§3.2 R1) | table-shape lint | Every function-row in §3 populates all 11 §3.2 fields. `unknown` legal for cost only. |
| **RP-G4** service-trace-integrity | Tier-1 (§3.3 R2 + D-3 conflation test) | reference-check | Every `service_trace` field cites at least one S1..S5 sentence + a journey step named in doctrine Part II. Empty/invalid = D1 orphan finding. |
| **RP-G5** Q2-orphan-coverage | Tier-1 (rent-paying deliverable) | inclusion-check | Every gate whose promise CANNOT be recovered from the on-disk record appears in §4 Q2 list. Deliverable of the phase (Owner-explicit framing). |
| **RP-G6** Q3-gap-coverage | Tier-1 (rent-paying deliverable) | inclusion-check | Every Layer 0 journey step (S1..S5 journey enumeration in doctrine Part II) that resolves to zero registered functions appears in §5 Q3 list. Deliverable of the phase. |
| **RP-G-Parity** parity 31 preserved | Tier-1 (frozen contracts) | fs-count | 31 frozen contracts + 31 snapshots byte-identical at close. |
| **RP-G-DataBlind** no secret values | Tier-1 (§8) | grep-negative | Registry rows contain no MongoDB URI · JWT · sk-* · AKIA* · %s secret-shaped tokens. |
| **RP-G-Docs** artifact + rulings + close all on-disk | Tier-3 (Standing Rule v3) | file-existence | `docs/registry/function_promise_registry_v0.md` + `docs/rulings/registry_population_rp_e1_to_e5.md` + `docs/close_reports/registry_population.md` all present at close. |
| **RP-G-DoctrineRef** deliverable cites doctrine SHA | Tier-3 (verbatim doctrine) | grep-positive | Deliverable §0 preamble cites `registry_doctrine_v1.md` by path + SHA. |

**Total: 10 named gate families · zero test-cells (doc-only extraction · gates are attest-at-close text-inspections executed by hand OR by grep + wc at close).**

---

## §6. Escalation matrix — PRE-TIERED (verbatim relay to Owner)

Owner-named Tier-1 surfaces (verbatim from dispatch): **promise-consolidation judgment calls** + **Q2/Q3 findings that touch a client promise**. Anticipated additional Tier-1 surfaces: scope-boundary judgments · ladder-rung assignment · cost field disposition.

### §6.1 Tier-1 escalations (exactly 5 · verbatim relay format)

**RP-E1 · Promise-consolidation judgment posture (Tier-1 · Owner-named)**

> **Promise protected:** the promise set is the small canonical anchor of the Registry — dozens, not hundreds. Consolidation that under-collapses inflates promise count and reintroduces the meta-spiral the doctrine forbids; over-collapsing merges distinct client-promises into one row and loses the honesty grammar of what the platform actually protects.
>
> **Escalation:** two "Promise protected:" lines from different Tier-1 escalations may resolve to (a) the same underlying promise, or (b) two distinct promises. The judgment is often non-mechanical.
>
> **Options (pre-authorised menu):**
> - **α · Verbatim-line-equivalence with builder-triage sidecar.** Two "Promise protected:" lines consolidate iff their core promise-clause tokens overlap ≥60% AND both share the same governor + surface class. Otherwise distinct. Builder maintains a consolidation-log sidecar noting each merge with the two verbatim source lines quoted + the merge rationale. Owner reviews the log at close-time; disagreements escalate as Tier-1 amendments (bounded volume: expected 10–20 non-trivial merges).
> - **β · Preserve-every-line-as-distinct-promise (no consolidation).** Every unique "Promise protected:" text becomes its own promise-row. Simplest to defend at close (no builder judgment); risks inflating promise count beyond doctrine's "dozens, not hundreds" target (projected: 80–120 rows). Doctrine §3.6 rent-check would flag inflation on the first Q1 redundancy query.
> - **γ · Escalate every consolidation to Owner ruling before landing.** Zero builder discretion. Delivers a smaller landed set but explodes the Tier-1 escalation surface (projected: 30–60 individual consolidation escalations). Doctrine D-7 tension: this is not "invented schedule" but heavy Tier-1 traffic.
>
> **Builder-recommendation: α.** The doctrine locates the small canonical set as the product; the sidecar log preserves auditability without flooding the Tier-1 loop. β under-delivers on doctrine §3.6 rent-paying; γ over-uses Tier-1. If Owner rules α, the consolidation-log becomes a co-landed artifact (`docs/registry/consolidation_log_v0.md`) noted in Tier-3 defaults §6.3.
>
> **R4 reflexive Registry row:**
>
> | Field | Value |
> |---|---|
> | function_id | `registry.population.promise_consolidation_judgment` |
> | governor | (named surface: Registry) |
> | mandate | Built to render a two-source-line promise-pair to one or two promise-rows in the Registry, verbatim source-line preservation in a sidecar log. |
> | promise | The small canonical anchor set is preserved; consolidation is auditable; the meta-spiral is prevented at population time. |
> | service_trace | S3.prove (Compliance can trace which underlying "Promise protected:" line each row consolidates from). |
> | surface | `docs/registry/function_promise_registry_v0.md §2` + `docs/registry/consolidation_log_v0.md` (Tier-3 default artefact). |
> | enforcement | grep-negative on §2 promise-row count vs source-line count · consolidation-log inclusion-check |
> | cost | unknown (extraction phase; cost measurable at first Q1 query run) |
> | dependencies | Registry Doctrine v1.0 §3.2 schema + §3.4 Q1 query |
> | ladder_rung | 1 · Deterministic code (token-overlap check + governor/surface match), OR — for edge cases — rung 3/4 assistance escalates via RP-E1 Tier-1 path |
> | owner | Owner (α ruling required) |
>
> **Class:** Tier-1 (client-promise vein integrity · doctrine §3.6 rent).
> **Ruling required BEFORE execution.**

**RP-E2 · Q2/Q3 findings that touch a client promise (Tier-1 · Owner-named)**

> **Promise protected:** client-promise-bearing findings are Owner-ruled surfaces — Q2 orphans over client-promise gates or Q3 gaps in Layer 0 journey steps expose live liability; builder-triage would risk silent retirement of a gate the Owner considers load-bearing.
>
> **Escalation:** every Q2 orphan whose gate protects a client-promise class (Tier-1 verbatim ruling loop per §12.1:306: frozen contracts, security boundaries, honesty grammar, client promises) AND every Q3 gap whose journey step is client-promise-bearing must surface as a Tier-1 escalation.
>
> **Options (pre-authorised menu):**
> - **α · Publish findings verbatim in the deliverable · escalate at close · no builder-retirement.** Every client-promise-touching Q2 lists with source citations + recoverability failure rationale. Every client-promise-touching Q3 lists with the S-sentence + journey step. Owner rules retirement/gap-fill at a subsequent turn; the deliverable ships regardless of open findings (findings are the deliverable per Owner framing).
> - **β · Builder-triages non-client-promise Q2s (near-orphan retirements at Tier-3) · client-promise Q2s escalate.** Non-client-promise Q2s (e.g., internal-only sanity checks with no cross-surface impact) retire under Tier-3 hygiene in a sidecar log. Client-promise Q2s remain Tier-1. Reduces close-time Tier-1 volume.
> - **γ · Bulk-escalate all Q2/Q3 to Owner before landing the deliverable.** Deliverable does not land until every finding is ruled. Maximum Owner control; longest deliverable-landing latency; may exceed Owner's escalation-budget per Registry Doctrine D-8 (reduction).
>
> **Builder-recommendation: α.** Owner framed Q2/Q3 as "deliverables of this phase, not defects in it — the Registry earning rent on day one." α preserves that framing: findings land, Owner rules, then subsequent Registry-maintenance phases execute the retirements. β would silently retire in the very first population — inconsistent with archaeology-not-authorship. γ blocks the deliverable on Owner throughput.
>
> **R4 reflexive Registry row:**
>
> | Field | Value |
> |---|---|
> | function_id | `registry.population.q2_q3_client_promise_escalation` |
> | governor | (named surface: Registry) |
> | mandate | Built to route every Q2 orphan touching a client-promise gate AND every Q3 gap over a client-promise journey step to Owner ruling verbatim, with source citations. |
> | promise | Client-promise gates are not retired silently; client-promise-bearing journey steps are not silently un-gated. |
> | service_trace | S1.call (integrating app inheriting provability) · S3.prove (Compliance) · S4.receive (buyer verification). |
> | surface | `docs/registry/function_promise_registry_v0.md §4 §5` |
> | enforcement | grep-negative — every listed Q2/Q3 that references a client-promise class is quoted verbatim from source + escalated to Owner at close |
> | cost | unknown (depends on extracted finding count) |
> | dependencies | RP-G1..RP-G6 |
> | ladder_rung | 1 · Deterministic (classification of Q2/Q3 by client-promise class via keyword match against §12.1:306 vocabulary) |
> | owner | Owner (α ruling required) |
>
> **Class:** Tier-1 (client-promise vein integrity · doctrine §3.6 rent · Owner-named).
> **Ruling required BEFORE execution.**

**RP-E3 · Scope-boundary: governor behavior vs implementation detail (Tier-1 · anticipated)**

> **Promise protected:** the Registry taxonomy — every function belongs to SyniSense · Northena · Mtafiti · Targeta · Solva · or a named surface (doctrine §3.1). Over-registering implementation sub-steps inflates row count (defect D5 meta-spiral risk); under-registering misses named governor behaviors (Q3 gap risk).
>
> **Escalation:** mandate documents (e.g., `RMS_Product_Engineering_Spec_v3.md`, `RMS_Mtafiti_Specification.md`) describe governor behaviors at multiple granularities — top-level ("Mtafiti extracts NormalizedUnits from raw sources") vs sub-step ("Mtafiti's ASR pass emits transcript_v0 with pinned model provenance"). Which granularity is Registry-visible?
>
> **Options (pre-authorised menu):**
> - **α · Register only mandate-Tier-1 vocabulary (named-and-testable behaviors).** A governor behavior registers iff (i) it is explicitly named in the mandate's Tier-1 vocabulary (§-section or numbered clause), AND (ii) it has a testable machine-enforceable surface (a gate, contract, or E2E cell references it). Sub-steps that are implementation of a named behavior fold into the parent row's `mandate` field.
> - **β · Register every named behavior at every granularity.** Every §-clause and every sub-clause becomes its own row. Higher row count; more surface area for Q1 redundancy queries; potentially more useful for future workers wiring.
> - **γ · Register only what a CI cell references.** Rows exist iff a currently-passing CI cell attests to them. Simplest; misses governor promises not yet tested (contradicts Q3 gap-finding as a deliverable).
>
> **Builder-recommendation: α.** Balances doctrine §3.1 taxonomy with §3.6 rent-paying. Sub-step visibility recoverable via future dispatched query automation.
>
> **R4 reflexive Registry row:**
>
> | Field | Value |
> |---|---|
> | function_id | `registry.population.governor_scope_boundary_ruling` |
> | governor | (named surface: Registry) |
> | mandate | Built to classify each mandate-named behavior as Registry-visible (row) or implementation-detail (sub-step folded into parent row's mandate field). |
> | promise | The Registry taxonomy stays at doctrine's small canonical set; implementation sub-steps do not inflate the meta-layer. |
> | service_trace | S2.commission (Operator sees the same governor names the mandate promises). |
> | surface | `docs/registry/function_promise_registry_v0.md §3` |
> | enforcement | grep-positive — every §3 row cites its mandate-source §-clause; sub-step behaviors are grep-negative on §3 |
> | cost | unknown |
> | dependencies | mandate documents (see §2.3 secondary vein 1) |
> | ladder_rung | 1 · Deterministic (mandate-clause reference match) with rung-3/4 escalation at edge cases (RP-E3) |
> | owner | Owner (α ruling required) |

**RP-E4 · Ladder-rung assignment ambiguity (Tier-1 · anticipated)**

> **Promise protected:** cheapest-sufficient rung (doctrine D-4) — model-ladder rung assignment governs which functions bear cost inflation review at future Stage As. Silent rung inflation is defect D4.
>
> **Escalation:** for many extracted functions the §5.1 rung is not explicit in the source (e.g., a §3.14 census-dimension gate — is it rung 1 deterministic FS-walk, or does it invoke a rung-3 owned model at inference time?). Silent guess = D4 risk.
>
> **Options (pre-authorised menu):**
> - **α · Mark "unknown" per §3.2 (legal initial value).** Rows where rung is not evident from source mark `ladder_rung: unknown`. Doctrine §3.2 permits this; §5.2 sequencing harness measurement (future Owner dispatch) resolves.
> - **β · Builder-best-guess with rationale in sidecar.** Rows guess a rung + attach a one-line rationale to a `ladder_rung_rationale` sidecar column. Owner reviews at close.
> - **γ · Escalate every unknown rung as an individual Tier-1.** Would flood the escalation surface (projected 40–70 individual rung escalations for a landing without α unknown-legality).
>
> **Builder-recommendation: α.** Doctrine explicitly permits `unknown`. The correct time to resolve is via the sequencing harness (future dispatch), not by builder guesswork. β risks introducing untested rungs to the record. γ over-uses Tier-1.

**RP-E5 · §4.2 threshold + governance-doc carve-out precedent applicability (Tier-1 · anticipated)**

> **Promise protected:** honest LoC accounting per §9 metric-verdict-in-raw-LoC. The Registry deliverable is a doctrine-mandated governance-class artifact (§3.6 rent-paying); the §3.8 close precedent excluded governance/rulings docs from the band derivation. Does the same reasoning apply?
>
> **Escalation:** proposed band `[1,300, 2,900]` includes the deliverable's own LoC (α = 2,750 · β = 2,070 · γ = 1,385). Two dispositions available.
>
> **Options (pre-authorised menu):**
> - **α · Band applies to the deliverable's raw LoC as stated (§4.2 disclosure Tier-2, non-blocking).** Precedent-compatible with all prior closes; simplest bookkeeping.
> - **β · Governance-doc carve-out — Registry deliverable exempt from band derivation.** Reasoning: doctrine §3.6 makes the Registry rent-payable via the §3.4 queries (Q1/Q2/Q3), not via LoC. LoC of a Registry that surfaces genuine Q2/Q3 findings is not the same class of cost as production code. Band would then derive only from ancillary rulings + close reports (much smaller LoC), and the Registry itself is reported separately as a page count with promise-count / function-count / findings-count metrics.
>
> **Builder-recommendation: α.** Simpler; preserves the standing LoC discipline; §4.2 disclosure is always Tier-2 non-blocking per §12.1 so no risk. β sets a doctrinal-carve-out precedent that could be misapplied in future extraction phases (Registry population is not the only future extraction under §3.5's archaeology posture). If Owner wants β, note the Registry-class carve-out in a governance amendment cycle rather than case-by-case here.

### §6.2 Tier-2 disclosures (cost/rework · no round-trip · lines in close report)

- **T2-D1:** proposed raw-LoC band `[1,300, 2,900]` per §3 accounting table.
- **T2-D2:** §4.2 raw threshold 1,500 projected-crossed in α and β scenarios (Tier-2 disclosure per §12.1 · never blocking).
- **T2-D3:** cell count: **zero new test cells** at Registry Population phase (doc-only). R4 reflexive rows in §7 are Registry rows, NOT test cells.
- **T2-D4:** verbatim-carrier overhead (§6.9) accounts for ~120 LoC (Layer 0 S1..S5 verbatim + doctrine reference).
- **T2-D5:** consolidation-log sidecar (`docs/registry/consolidation_log_v0.md`) if RP-E1 α ruled — additional ~150 LoC not counted in above table (Tier-3 default artifact).
- **T2-D6:** rulings record at `docs/rulings/registry_population_rp_e1_to_e5.md` + close report at `docs/close_reports/registry_population.md` — governance-doc class, precedent-excluded from band derivation per §3.8.
- **T2-D7:** snapshot in-band verdict rendered post-execution against raw `wc -l`; verdict discipline unchanged.

### §6.3 Tier-3 defaults (silent · one-line notes in close report · per §6.3)

- **[Tier 3]** file names: `docs/registry/function_promise_registry_v0.md` (deliverable) · `docs/registry/consolidation_log_v0.md` (RP-E1 α sidecar iff ruled) · `docs/rulings/registry_population_rp_e1_to_e5.md` · `docs/close_reports/registry_population.md`.
- **[Tier 3]** promise-row identifier format: `PROM-<S#>-<slug>` (e.g., `PROM-S1-provable-envelope-inheritance`).
- **[Tier 3]** function-row identifier format: `<governor>.<surface_class>.<slug>` per doctrine §3.2 example (`northena.ledger.append_only_gate`).
- **[Tier 3]** journey-step vocabulary source: doctrine Part II verbatim journey-step lists per S1..S5.
- **[Tier 3]** table style: markdown pipe-tables · one row per function · header row per governor section.
- **[Tier 3]** Q2 finding record shape: `{finding_id, gate_identifier_from_source, source_citation, why_promise_unrecoverable, client_promise_class?}`.
- **[Tier 3]** Q3 finding record shape: `{finding_id, S_sentence, journey_step, why_no_function_found, client_promise_bearing?}`.
- **[Tier 3]** coverage-attest metric shape: `{observed_ci_cell_count, observed_named_gate_identifier_count, extracted_function_row_count, extracted_promise_row_count, consolidation_ratio}`.
- **[Tier 3]** deliverable §0 preamble MUST cite `registry_doctrine_v1.md` by path + SHA (RP-G-DoctrineRef enforcement).
- **[Tier 3]** verbatim doctrine passages (S1..S5 · D-1..D-10 · D1..D7) quoted from `registry_doctrine_v1.md` at the same SHA cited in §0.
- **[Tier 3]** if RP-E4 α ruled and Registry has many `unknown` rungs, the coverage attest reports the count as an honest disclosure (not a defect).

### §6.4 Escalation matrix counts (summary)

- **Tier-1 anticipated: 5** (RP-E1 promise-consolidation · RP-E2 client-promise Q2/Q3 · RP-E3 governor-scope-boundary · RP-E4 rung-ambiguity · RP-E5 §4.2 carve-out).
- **Tier-2 disclosures: 7** (T2-D1..T2-D7).
- **Tier-3 defaults: 10** (per §6.3).

---

## §7. Registry Doctrine reflexive attest — this phase's own gates

Per **R4 reflexive** (Owner directive: "R4 applies reflexively: this phase's own checks register themselves"), each RP-G* gate carries its Registry row here. These rows will co-land inside the deliverable at close as §7.

### §7.a Gate Registry rows (§3.2 schema · this phase's own gates)

| Field | RP-G1 promise-set-completeness |
|---|---|
| function_id | `registry.population.g1_promise_set_completeness` |
| governor | (named surface: Registry) |
| mandate | Built to attest that every "Promise protected" line in the source corpus resolves to a promise-row in Deliverable §2 OR appears in §4 Q2 orphan list. |
| promise | The extraction is complete on its primary vein; no source-line silently drops. |
| service_trace | S3.prove (Compliance can trace any promise to at least one source citation OR to the Q2 record explaining why it did not become a promise). |
| surface | `docs/registry/function_promise_registry_v0.md §2 + §4` |
| enforcement | grep-negative — every source-line either matches a promise-row citation OR appears in a Q2 record |
| cost | unknown (measurable on first Q1 query run · target-artifact grep cost) |
| dependencies | Source corpus: `docs/rulings/*.md` + `docs/stage_a_proposals/*.md` |
| ladder_rung | 1 · Deterministic (grep + reference-check) |
| owner | Owner |

| Field | RP-G2 function-attachment-completeness |
|---|---|
| function_id | `registry.population.g2_function_attachment_completeness` |
| governor | (named surface: Registry) |
| mandate | Built to attest that every named gate identifier in the CI roster / close-report gate rosters has a function-row in §3 OR appears in §4 Q2 orphan. |
| promise | Doctrine §3.3 R3 (No journey step without enforcement) — every enforcement citation resolves to a Registry row or a Q2 finding. |
| service_trace | S3.prove (auditability of gate roster) · S1.call (integrating app trust surface). |
| surface | `docs/registry/function_promise_registry_v0.md §3 + §4` |
| enforcement | grep-negative on close-report gate rosters vs §3 function-row identifiers |
| cost | unknown |
| dependencies | `docs/close_reports/*.md` (31 files) · `backend/tests/invariants/*_g*.py` (18 files) |
| ladder_rung | 1 · Deterministic |
| owner | Owner |

| Field | RP-G3 schema-conformance |
|---|---|
| function_id | `registry.population.g3_schema_conformance` |
| governor | (named surface: Registry) |
| mandate | Built to attest that every function-row in §3 populates all 11 §3.2 schema fields, with `unknown` legal only for `cost`. |
| promise | Doctrine §3.2 R1 — schema discipline; no partial rows. |
| service_trace | S3.prove (Registry is a well-formed audit surface). |
| surface | `docs/registry/function_promise_registry_v0.md §3` |
| enforcement | table-shape lint (markdown pipe-table column-count check) |
| cost | unknown (per-row inspection) |
| dependencies | §3.2 schema literal from `docs/governance/registry_doctrine_v1.md` |
| ladder_rung | 1 · Deterministic |
| owner | builder-Tier-3 (mechanical) |

| Field | RP-G4 service-trace-integrity |
|---|---|
| function_id | `registry.population.g4_service_trace_integrity` |
| governor | (named surface: Registry) |
| mandate | Built to attest that every `service_trace` field cites at least one S1..S5 sentence + a journey step named in doctrine Part II. |
| promise | Doctrine R2 (No promise without a service trace) + D-3 conflation test (which Layer 0 sentence does this serve?). |
| service_trace | S1..S5 (self-referential: RP-G4 attests the traceability of every other row's service_trace). |
| surface | `docs/registry/function_promise_registry_v0.md §3` |
| enforcement | reference-check — every `service_trace` field regex-matches `S[1-5]\.[a-z_]+` and the journey-step token appears in doctrine Part II verbatim |
| cost | unknown |
| dependencies | doctrine Part II verbatim journey-step vocabulary |
| ladder_rung | 1 · Deterministic |
| owner | Owner |

| Field | RP-G5 Q2-orphan-coverage |
|---|---|
| function_id | `registry.population.g5_q2_orphan_coverage` |
| governor | (named surface: Registry) |
| mandate | Built to attest that every gate whose promise cannot be recovered from the on-disk record appears in §4 Q2 list of the deliverable. |
| promise | Doctrine §3.5 (archaeology, not authorship — where extraction finds a gate whose promise cannot be recovered, that is a Q2 finding, not a writing prompt) + Q2 verbatim (§3.4). |
| service_trace | S3.prove (Compliance sees every orphan explicitly). |
| surface | `docs/registry/function_promise_registry_v0.md §4` |
| enforcement | inclusion-check — every RP-G1 / RP-G2 grep-fail generates a §4 entry |
| cost | unknown |
| dependencies | RP-G1 · RP-G2 |
| ladder_rung | 1 · Deterministic |
| owner | Owner |

| Field | RP-G6 Q3-gap-coverage |
|---|---|
| function_id | `registry.population.g6_q3_gap_coverage` |
| governor | (named surface: Registry) |
| mandate | Built to attest that every Layer 0 journey step (S1..S5 journey enumeration in doctrine Part II) that resolves to zero registered functions appears in §5 Q3 list. |
| promise | Doctrine R3 (No journey step without enforcement — an unprotected step is an exposed liability and is reported, not assumed safe) + Q3 verbatim (§3.4). |
| service_trace | S3.prove (Compliance sees every gap explicitly) · applies across S1..S5 journeys. |
| surface | `docs/registry/function_promise_registry_v0.md §5` |
| enforcement | inclusion-check — every doctrine Part II journey-step with zero §3-row citations generates a §5 entry |
| cost | unknown |
| dependencies | RP-G4 · doctrine Part II journey enumeration |
| ladder_rung | 1 · Deterministic |
| owner | Owner |

### §7.b Auxiliary gate Registry rows (§3.2 schema)

| Field | RP-G-Parity parity 31 preserved |
|---|---|
| function_id | `registry.population.gaux_parity_31_preserved` |
| governor | SyniSense (frozen-contract discipline) |
| mandate | Built to attest 31 frozen contracts + 31 snapshots byte-identical at Registry Population close. |
| promise | Frozen wire contract discipline (Tier-1 verbatim ruling loop per §12.1:306) — no code touch during a doc-only extraction phase leaves parity untouched. |
| service_trace | S1.call (integrating app inherits contract stability). |
| surface | `backend/tests/invariants/*.contract_snapshot.json` count == 31 |
| enforcement | fs-count (shared parity_counter.py from PH-E3 α) |
| cost | O(31) fs glob · already measured (PH-G-Parity · trivial) |
| dependencies | `backend/services/health/parity_counter.py` |
| ladder_rung | 1 · Deterministic |
| owner | builder-Tier-3 |

| Field | RP-G-DataBlind no secret values in registry rows |
|---|---|
| function_id | `registry.population.gaux_data_blind` |
| governor | SyniSense (§8 data-blind posture) |
| mandate | Built to attest that Registry rows contain no MongoDB URI · JWT · sk-* · AKIA* or otherwise secret-shaped tokens. |
| promise | Governance §8 data-blind — the Registry is a governance artifact; no secret material leaks into it. |
| service_trace | S3.prove (Compliance surface data-blind). |
| surface | `docs/registry/function_promise_registry_v0.md` (grep-negative pattern set) |
| enforcement | grep-negative (regex set: `mongodb://[^:]+:[^@]+@`, `eyJ[A-Za-z0-9_\-]{20,}`, `sk-[A-Za-z0-9]{20,}`, `AKIA[0-9A-Z]{16}`) |
| cost | O(deliverable_LoC) grep · trivial |
| dependencies | Deliverable itself |
| ladder_rung | 1 · Deterministic |
| owner | builder-Tier-3 |

| Field | RP-G-Docs artifact + rulings + close all on-disk |
|---|---|
| function_id | `registry.population.gaux_docs_on_disk` |
| governor | (named surface: Registry · Standing Rule v3) |
| mandate | Built to attest that the deliverable + rulings record + close report all land on disk at Standing Rule v3 canonical paths. |
| promise | On-disk canonical (Standing Rule v3) — the phase's deliverables are traceable. |
| service_trace | S3.prove. |
| surface | `docs/registry/function_promise_registry_v0.md` · `docs/rulings/registry_population_rp_e1_to_e5.md` · `docs/close_reports/registry_population.md` |
| enforcement | file-existence checks |
| cost | trivial |
| dependencies | Standing Rule v3 governance |
| ladder_rung | 1 · Deterministic |
| owner | builder-Tier-3 |

| Field | RP-G-DoctrineRef deliverable cites doctrine SHA |
|---|---|
| function_id | `registry.population.gaux_doctrine_ref` |
| governor | (named surface: Registry) |
| mandate | Built to attest that Deliverable §0 preamble cites `registry_doctrine_v1.md` by path + SHA-256. |
| promise | Verbatim doctrine anchoring — the Registry cites its authority source. |
| service_trace | S3.prove (any Registry row's doctrine anchor is auditable at the exact SHA). |
| surface | `docs/registry/function_promise_registry_v0.md §0` |
| enforcement | grep-positive on doctrine path + full SHA-256 |
| cost | trivial |
| dependencies | `docs/governance/registry_doctrine_v1.md` SHA `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` |
| ladder_rung | 1 · Deterministic |
| owner | builder-Tier-3 |

### §7.1 D-10 self-audit (this Stage A · against defect classes D1–D7)

Per Registry Doctrine D-10 verbatim (from `registry_doctrine_v1.md` line 96): *"Builder conduct standard. Meticulousness is enforced by structure, not assumed: every proposal self-audits against defect classes D1–D7 before submission, and a proposal arriving with a defect the self-audit would have caught is itself a reportable finding."*

| Class | Pass/Fail | One-line reason |
|---|---|---|
| **D1 · Orphan gate** | **PASS** | Every RP-G* gate in §7.a/§7.b has a promise field populated + service_trace citing S1..S5 · zero orphans in this Stage A's own reflexive rows. |
| **D2 · NL-only enforcement** | **PASS** | Every RP-G* enforcement value is a machine-enforceable class (`grep-negative`, `reference-check`, `fs-count`, `file-existence`, `table-shape lint`, `inclusion-check`) · no "NL-only" values. |
| **D3 · Curated verdict** | **PASS** | Q2/Q3 findings are extracted mechanically from what exists (grep on source corpus vs registry-row citations); Q2/Q3 outputs are not curated by favorability — they are the mechanical residue of the extraction. |
| **D4 · Rung inflation** | **PASS** | Every RP-G* row's `ladder_rung` is `1 · Deterministic` — the cheapest sufficient rung. RP-E1/RP-E4 escalations preserve this posture (rung-3/4 assistance only for edge-case Tier-1 promise-consolidation calls, escalated verbatim). No silent rung inflation. |
| **D5 · Meta-spiral** | **PASS** | This Stage A populates the Registry (the primary artifact per doctrine §3.6) — it does NOT create a second governance layer above the Registry. RP-E5 explicitly asks whether the Registry deliverable's LoC is band-counted (α) or governance-doc carve-out (β), preventing a silent meta-layer creation. |
| **D6 · Service conflation** | **PASS** | Every RP-G* row's `service_trace` cites an S1..S5 sentence (mostly S3.prove for Compliance-facing Registry surfaces · plus S1.call/S4.receive where client-facing). Zero end-user-persona optimization in the phase's own gates. |
| **D7 · Invented schedule or scope** | **PASS** | §8 out-of-scope statement lists every item Owner-explicitly excluded: no code · no CI changes · no query automation · no harness · no worker wiring · no Playbook/Thesis content · no machine-readable Registry. Doctrine §8.1 code-level items enumerated explicitly as future-owner-dispatch only. |

**Self-audit verdict:** all 7 defect classes PASS. Stage A submits.

---

## §8. Out-of-scope statement (D7 binding · Owner verbatim)

Per Owner dispatch verbatim: *"Out of scope, D7 binding: no code, no CI changes, no query automation, no harness, no worker wiring, no Playbook/Thesis content."*

Additionally out of scope per Owner-explicit dispatch instructions:

- **No code** — this phase modifies zero `.py`, `.js`, `.jsx`, `.ts`, `.tsx`, `.json`, or `.env` files. Zero backend touch. Zero frontend touch. Zero test-file touch.
- **No CI changes** — the ~1,400 test cells across Pytest/Jest/Playwright are read-only extraction sources; none are added, modified, or reordered.
- **No query automation** — doctrine §3.4 Q1/Q2/Q3 queries execute by-hand (grep + inspection) at close-time; no executable check lands. Doctrine §8.1 code-level item (a) is future-owner-dispatch only.
- **No sequencing harness** — doctrine §5.2 code-level spec is future-owner-dispatch only.
- **No worker context-harnessing** — doctrine §6.2 code-level spec is future-owner-dispatch only.
- **No Instance Replication Playbook** — doctrine §8.1 documents (draft on Owner word) — not dispatched.
- **No Commercial Thesis** — doctrine §8.1 documents (draft on Owner word) — not dispatched.
- **No machine-readable Registry** — doctrine §8.1 code-level item (d) — future-owner-dispatch only. The deliverable is markdown pipe-tables (human-readable) exclusively.
- **No changes to any existing on-disk file** except the two Standing-Rule-v3 canonical carriers landed at execution close: `docs/rulings/registry_population_rp_e1_to_e5.md` (rulings) + `docs/close_reports/registry_population.md` (close). All other files (`docs/registry/function_promise_registry_v0.md`) are new.
- **No amendments to the governance stack** — `tiered_ruling_model.md` + `registry_doctrine_v1.md` are read-only authority sources during execution.
- **No consolidation-log sidecar unless RP-E1 α ruled** — the `docs/registry/consolidation_log_v0.md` file lands only if the Owner rules RP-E1 α (Tier-3 default artifact under that ruling).

**Defect D7 binds:** the builder does not schedule, defer, or invent any owner-side workstream beyond this list. No "next phase" is proposed here. The next motion after this Stage A → Owner ruling → execution → close is Owner-signaled or not signaled.

---

## §9. Sequence forward (post-close)

Owner-signal driven only. This Stage A anticipates:

1. Owner verbatim rulings on RP-E1 through RP-E5 (Tier-1 relay to Owner is the next expected motion).
2. On ruling receipt: atomic execution commit landing `function_promise_registry_v0.md` (+ optional `consolidation_log_v0.md` if RP-E1 α) + rulings record + close report.
3. On close-landing: mandate-complete state preserved · Registry Doctrine v1.0 in force · Registry v0 landed as the first §3.5 archaeology artifact.
4. Post-close: **IDLE.** No self-dispatch (defect D7). Future Owner motions may dispatch: machine-readable Registry (doctrine §8.1.d), executable queries (§8.1.a), sequencing harness (§8.1.b), worker-context-harnessing (§8.1.c), Registry population maintenance, Instance Replication Playbook, Commercial Thesis, or 9.2b on Owner "proceed."

═══════════════════════════════════════════════════════════════════

*End of Registry Population Stage A proposal. Standing Rule v3 · on-disk canonical. Registry Doctrine v1.0 in force · R4 reflexive (§7 · own gates registered) · D-10 self-audit landed (§7.1 · D1–D7 all PASS). Awaiting Owner rulings on Tier-1 escalations RP-E1..RP-E5 (verbatim relay). Per governance §12 (2026-07-10): band/threshold disclosures are Tier-2, disclosure-only, never blocking; Tier-1 escalations return via verbatim relay before execution. Per §13: R4 applies; every gate in §5 carries its Registry row in §7.*
