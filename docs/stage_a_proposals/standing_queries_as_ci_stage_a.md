# Stage A · Standing Queries as CI (Registry Doctrine §8.1.a)

**Dispatch class:** Registry Doctrine v1.0 §8.1.a — the three standing queries (Q1 redundancy · Q2 orphans · Q3 gaps) as executable checks over the machine-readable Registry.
**Dispatched:** 2026-07-11 (post-MRR self-ratification · Owner process correction internalized).
**Doctrine SHA:** `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` (in force).
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 · §12/§12.1/§12.2/§13/§14 · Defect D7 binds.
**Prior close:** Machine-Readable Registry §8.1.d · self-ratified via §12 · 2026-07-11.

---

## §1. Scope + source lock

**Owner dispatch verbatim (2026-07-11):**
> "Q1 (redundancy: same promise + same surface → merge candidates, ranked by cost), Q2 (orphans: empty or unresolvable promise/service_trace), Q3 (gaps: promise or Part-II journey step with no enforcing function) — executable checks over `registry.yaml` per doctrine §3.4.
>
> Report-level, never build-failing: queries produce findings artifacts under `docs/registry/queries/`; retirements and merges remain ruled actions per §3.4 tiering. A query that auto-retires anything is a defect. Findings are inputs to rulings, not actions.
>
> Baseline attest as the acceptance gate: the first run must reproduce the known state — all 11 ruled findings appear with their ruled statuses, zero phantom findings, zero losses. The engine proves itself against the record before it's trusted on anything new.
>
> Rung 1 throughout. R4 rows land via the §14 supplement pattern. D-10 self-audit rides per standing."

**Sources (locked):**
- `/app/docs/registry/machine/registry.yaml` @ SHA `226c298a…` (query input — parser output, regenerated on demand from `v0.md + v0.1_supplement`).
- `/app/docs/registry/function_promise_registry_v0.md` @ SHA `598a7ad4…` **byte-identical throughout** (source of truth · v0.md remains untouched).
- `/app/docs/registry/function_promise_registry_v0.1_supplement.md` @ SHA `2822f99e…` **byte-identical throughout** (locked once landed; per §14 discipline).
- `/app/docs/rulings/registry_findings_01_to_11.md` @ SHA `20e03f40…` (11 ruled findings verbatim carrier · baseline attest source).
- `/app/backend/services/registry/validator.py` @ SHA `7ac8b790…` (carries `PART_II_JOURNEY_STEPS` frozenset · governance-amendment-only).

---

## §2. Query semantics (mechanical spec · zero ambiguity)

### §2.1 Q1 · Redundancy (same promise + same surface → merge candidates)

**Mechanical definition:**
- Iterate pairs `(a, b)` of function rows where `a != b`.
- **Same promise:** set-equality on `PROM-*`-prefixed tokens (adjacent non-PROM tokens like `governance §8` are documentation cross-references per MRR-G2 β discipline; not primary attributions).
- **Same surface:** exact string equality on the `surface` field.
- **Emit:** pair `(a.function_id, b.function_id)`, shared PROM-set, shared surface, cost rank.

**Cost ranking:** per Owner dispatch verbatim (*"sum of the pair's cost fields where numeric; `unknown` sorts to end"*):
- Pairs where both `a.cost` and `b.cost` contain a leading numeric prefix (e.g., `1 cell`, `13 cells`) → rank by sum ascending.
- Pairs with any `unknown` cost → rank after all numeric pairs (unknown sorts to end).

**Output:** `/app/docs/registry/queries/q1_redundancy.md` — markdown table of merge candidates.

**Baseline expectation:** v0.md carries **zero Q1 findings table**. Baseline for Q1 = `{}` empty (any candidate the engine surfaces is a NEW finding needing Owner ruling · Owner-explicit "findings are inputs to rulings, not actions").

### §2.2 Q2 · Orphans (function-row property scan · 4 sub-cases)

**Mechanical definition — 4 sub-cases (Owner-verbatim):**
- **(a)** empty `promise` field on a function row.
- **(b)** `promise` field where NO `PROM-*` token resolves to a `promise_id` in the top-level `promises` array (MRR-G2 β foreign-key check re-applied at query-level · **READ-ONLY report**, never auto-retiring). Adjacent non-PROM tokens do not trigger (b) unless there are ZERO resolving PROM-tokens; consistent with MRR-G2 β discipline.
- **(c)** empty `service_trace` field on a function row.
- **(d)** `service_trace` steps that don't resolve to `PART_II_JOURNEY_STEPS` frozenset (MRR-G2 addition applied at query-level · **READ-ONLY**). Parenthetical annotation strip applied per MRR-G2 (`S1.call (advisory)` → `S1.call`). Whitelist `S1..S5` reflexive coverage marker per MRR-G2.

**Output:** `/app/docs/registry/queries/q2_orphans.md`.

**Baseline expectation:** v0.md has 5 ruled Q2 findings (Q2-01..Q2-05). **CRITICAL — SEE SQ-E1 TIER-1 ESCALATION §3.1:** these 5 findings reference **gate identifiers** (`EE-G1..G4` · `MAN-G1..G3` · `RT-*` · `V1-G0..G6` · legacy pre-doctrine gates) that are **NOT function rows in v0.md**. Mechanical scan of function rows (which is what Q2 mechanically does) CANNOT reproduce these archaeologically-derived findings. Reproduction requires an archaeological carry-over source.

### §2.3 Q3 · Gaps (promise or Part-II journey step with no enforcing function)

**Mechanical definition — 2 sub-cases (Owner-verbatim):**
- **(a)** every `promise_id` in top-level `promises` where zero function rows reference it (promise-without-function).
- **(b)** every step in `PART_II_JOURNEY_STEPS` frozenset where zero function rows carry that step in `service_trace` (journey-step-without-function). Parenthetical-strip applied per MRR-G2. Sanctioned aliases (`S3.prove` ↔ `S3.prove-end-to-end` · `S4.verify` ↔ `S4.verify-receipt`) resolve to the same underlying step for gap detection (either presence satisfies coverage).

**Output:** `/app/docs/registry/queries/q3_gaps.md`.

**Baseline expectation:** v0.md has 6 ruled Q3 findings. **CRITICAL — SEE SQ-E1:**
- Q3-01 `S1.pass-receipts-through` — cited by `synisense.shield.llm_single_source_boundary`; mechanical Q3 (b) does NOT flag it as gap (has a function). v0.md's Q3-01 finding is that no CI cell attests downstream trust — that's post-boundary archaeology, not mechanical.
- Q3-02 `S2.onboard-context` — is any function row's `service_trace` mapping this? Verification pending at Stage A time; if any function row cites it, mechanical Q3 (b) doesn't flag.
- Q3-03 `S4.license` — cited by `northena.artifact.outer_gate_receipt_v1`. Mechanical Q3 (b) does NOT flag it. v0.md's Q3-03 is post-commercial-cut archaeology.
- Q3-04 S5 — no journey steps in `PART_II_JOURNEY_STEPS` (S5 explicitly excluded per doctrine "no journey steps land as service_trace"). Mechanical Q3 (b) doesn't apply. v0.md's Q3-04 is a doctrine narrative gap.
- Q3-05 `S1.scoped-key` — cited by `ui.engineer.onboarding`. Mechanical Q3 (b) does NOT flag. v0.md's Q3-05 is about direct-cell absence (sub-covered indirectly).
- Q3-06 `bookkeeping.audit_ledger` walk — mandate-named (northena.md prose), not a Part-II step. Mechanical Q3 (b) doesn't detect (not in PART_II_JOURNEY_STEPS).

**Zero mechanical reproduction of v0.md's 6 Q3 archaeological findings by pure scan of function rows against `PART_II_JOURNEY_STEPS`.**

---

## §3. Pre-tiered escalation matrix

### §3.1 SQ-E1 · Q2/Q3 archaeological-vs-mechanical divergence in baseline attest (**Tier-1 · Owner-value seam identified**)

**Class:** baseline-attest semantic definition.

**Tension identified:**
- Owner-verbatim: *"the first run must reproduce the known state — all 11 ruled findings appear with their ruled statuses, zero phantom findings, zero losses."*
- Owner-verbatim (Q2/Q3 mechanical definitions): scan **function rows** for the 4 Q2 sub-cases + 2 Q3 sub-cases.
- Mechanical scan of function rows CANNOT reproduce:
  - **5 Q2 findings** (Q2-01..Q2-05) — subjects are **gate identifiers** (EE-G, MAN-G, RT-*, V1-G, legacy) NOT function rows.
  - **6 Q3 findings** — most `service_trace` steps referenced (`S1.pass-receipts-through`, `S4.license`, `S1.scoped-key`) ARE cited by function rows in v0.md, so mechanical Q3 (b) does NOT flag them. Q3-06 is mandate-named prose. Q3-04 S5 has no PART_II steps to flag.

**Options:**

| Option | Baseline-attest reproduction path | Engine posture |
|---|---|---|
| **α** | Engine has TWO output classes: **(1) mechanical scan** of function rows (finds new candidates the archaeology may have missed) **(2) archaeological carry-over** of v0.md §4/§5 findings via machine-form `findings` section (parser already extracts these · lossless). Baseline attest = archaeological-carry-over covers all 11 · mechanical scan produces additional Q1/Q2/Q3 candidates for Owner review at future Registry-maintenance turn. | Engine is mechanical-scanner + archaeological-carrier. |
| **β** | Baseline attest **redefined**: engine reproduces v0.md's ruled findings via carry-over ONLY. Mechanical scan runs as separate diagnostic; its output is NOT part of baseline reproduction check. Baseline check = "all 11 ruled findings appear in engine output via archaeological carry-over"; mechanical scan output = advisory. | Engine is archaeological-carrier + mechanical-scanner (with clean split). |
| **γ** | Two separate output files per query class: `q{n}_archaeological.md` (v0.md carry-over, byte-identical to §4/§5) + `q{n}_mechanical.md` (fresh scan over function rows). Baseline attest = archaeological files only. Mechanical files are surface for future rulings. | Engine emits two files per query · sharper audit trail. |

**Builder analysis (does NOT resolve):** All three preserve the "engine proves itself against the record" intent. **α** is the tightest (single output file per query, dual-content). **β** matches Owner's language most literally (carry-over IS the reproduction; mechanical is new). **γ** is the cleanest for archival auditing (two files make the archaeological/mechanical split byte-visible). Owner ruling anchors baseline-attest semantics.

**Reflexive R4 attest:** the SQ-G-Baseline gate's spec is per MRR-E4 rulings — placement in `v0.2_supplement.md` (see §5).

### §3.2 Tier-2 disclosures (never-blocking · §12.1)

| Disclosure ID | Class | Trigger |
|---|---|---|
| SQ-D2-baseline-mechanical-additions | Mechanical scan will surface additional Q1/Q2/Q3 candidates beyond the 11 ruled findings | Owner-explicit "findings are inputs to rulings, not actions" · reports at query artifacts · zero auto-action · disclosed at close. |
| SQ-D2-cost-ranking-mostly-unknown | Cost ranking: most function rows have `cost: unknown` per MRR ruling · ranking degrades gracefully (unknowns sort to end per Owner dispatch verbatim) · well-defined but Q1 output likely mostly-unknown-tail. Disclosed at close §4.3. |
| SQ-D2-carve-out-not-applicable | §3.6 governance-doc carve-out NOT applied case-by-case per RP-E5 α (2026-07-11). Band applies as-stated. |

### §3.3 Tier-3 defaults (builder-decides absent Owner ruling)

| Default ID | Class | Builder default |
|---|---|---|
| SQ-T3-engine-location | Query engine module | `/app/backend/services/registry/queries.py` (sibling to parser + validator). |
| SQ-T3-check-placement | Gate cell placement | `/app/backend/tests/registry/test_standing_queries_sq_g1_to_g_dataBlind.py` (matches MRR-G naming convention). |
| SQ-T3-cli | Query run CLI | `/app/tools/registry/run_queries.py` (matches `regenerate.py` sibling convention). |
| SQ-T3-artifact-dir | Findings artifact directory | `/app/docs/registry/queries/`. |
| SQ-T3-supplement-file | R4 reflexive supplement placement | **`v0.2_supplement.md`** (new supplement · additive per §14 · preserves per-phase supplement discipline; v0.1_supplement remains locked at MRR SHA). |
| SQ-T3-artifact-header | Findings artifact line-1 disclaimer verbatim (Owner-dispatch spec) | `THIS ARTIFACT IS REPORT-LEVEL · NEVER BUILD-FAILING · RETIREMENT/MERGE REMAINS RULED ACTION` |
| SQ-T3-artifact-metadata | Per-artifact metadata block | `header timestamp · source_sha of registry.yaml consulted · run count · disclaimer` (Owner-dispatch spec). |

### §3.4 Counts

- **Tier-1 count: 1** (SQ-E1 · baseline-attest semantic definition — Owner-value seam identified by builder probe).
- **Tier-2 count: 3** (SQ-D2-baseline-mechanical-additions · SQ-D2-cost-ranking-mostly-unknown · SQ-D2-carve-out-not-applicable).
- **Tier-3 count: 7** (T3-engine-location · T3-check-placement · T3-cli · T3-artifact-dir · T3-supplement-file · T3-artifact-header · T3-artifact-metadata).

---

## §4. Gate roster (proposed · 9 gates)

| Gate | Purpose | Enforcement | Ladder rung |
|---|---|---|---|
| **SQ-G1** | Q1 mechanical correctness — every pair meeting promise-set + surface equality is emitted; nothing else. Cost ranking applies `unknown`-sorts-to-end. | pytest cell + fixture-based unit test | 1 · Deterministic |
| **SQ-G2** | Q2 mechanical correctness — all 4 sub-cases (a/b/c/d) covered. PROM-only lint for (b); parenthetical-strip for (d). | pytest cell | 1 · Deterministic |
| **SQ-G3** | Q3 mechanical correctness — both sub-cases (promise-without-function · Part-II-step-without-function). Alias-equivalence for step coverage. | pytest cell | 1 · Deterministic |
| **SQ-G-Baseline** | 11 ruled findings byte-identical reproduction. Semantic scope per SQ-E1 ruling (α/β/γ). | pytest cell + diff against `rulings/registry_findings_01_to_11.md` | 1 · Deterministic |
| **SQ-G-No-Retirement** | Zero writes to source-of-truth artifacts (`function_promise_registry_v0.md` · `v0.1_supplement.md` · `registry.yaml`) during query run. | pre/post SHA-diff · pytest cell | 1 · Deterministic |
| **SQ-G-Report-Level** | Findings artifacts regenerate deterministically + are NOT build gates. | pytest cell running engine twice → byte-diff empty; artifacts checked in but not gate-blocking | 1 · Deterministic |
| **SQ-G-Rung1** | Every query runs rung 1 (no LLM invocation · deterministic pure-function). | AST negative-scan on `queries.py` for LLM imports (matches `test_no_direct_llm_calls_outside_shield` pattern) | 1 · Deterministic |
| **SQ-G-Parity** | V1-G7 31/31 unaffected. | fs-count + hash-diff | 1 · Deterministic |
| **SQ-G-DataBlind** | grep-negative on secret patterns in findings artifacts. | grep-negative regex | 1 · Deterministic |

**9 gates · all rung 1 · all mechanical.**

---

## §5. R4 reflexive attest — SQ-G# rows land via §14 supplement pattern

**Placement:** new supplement file `/app/docs/registry/function_promise_registry_v0.2_supplement.md` (per Tier-3 SQ-T3-supplement-file). Per governance §14 (Owner 2026-07-11 · MRR-E4 β standing consequence): additive supplements beside the locked source, consolidated at future maintenance turn. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement)` ↔ machine form as one set (extension of §14 to N supplements).

**Row count:** 9 SQ-G rows (one per gate in §4).

**Promise attribution:** all 9 rows will reuse existing v0.md §2 promises (conservative D7 · zero new promise minting). Candidate promise mappings:
- SQ-G1 · SQ-G2 · SQ-G3 · SQ-G-Baseline · SQ-G-No-Retirement · SQ-G-Report-Level · SQ-G-Rung1 → **PROM-S1-frozen-wire-contract** (Registry query engine is a wire-contract-integrity check).
- SQ-G-Parity → **PROM-S1-frozen-wire-contract** (parity gate).
- SQ-G-DataBlind → **PROM-S3-audit-trail-immutable** (governance §8 data-blind adjacency; matches MRR-G-DataBlind precedent).

**Parser + validator extension:** `parser.py` needs `SUPPLEMENT_PATHS` extended to include `v0.2_supplement.md`. `validator.py` `check_mrr_g3_round_trip` unchanged (path-list drives the check). This is a one-line data extension, not a semantic change.

---

## §6. Band raw LoC scenarios (derivation stated)

### §6.1 Derivation

**Deliverable inventory (per Owner atomic-commit spec + §5 R4 supplement):**
- Query engine module `queries.py`: ~200–300 LoC.
- CLI `run_queries.py`: ~30–50 LoC.
- Test file `test_standing_queries_sq_g1_to_g_dataBlind.py`: ~200–300 LoC (9 gate cells × ~20–30 LoC).
- 3 findings artifacts (`q1_redundancy.md` · `q2_orphans.md` · `q3_gaps.md`): ~50–120 LoC each = ~150–360 LoC.
- `v0.2_supplement.md` (9 SQ-G rows + preamble): ~80–120 LoC.
- Parser one-line `SUPPLEMENT_PATHS` extension: +1 LoC.
- Machine form regeneration (registry.yaml re-render with v0.2_supplement included): +~140–180 LoC delta (9 new function rows).
- Rulings record (only if Tier-1 SQ-E1 escalated and ruled): ~60–100 LoC.
- Close report: ~150–250 LoC.

### §6.2 Scenario table (raw LoC)

| Scenario | SQ-E1 disposition | Deliverable LoC est. |
|---|---|---:|
| **α** (dual-content per query file) | Engine emits ONE file per query; content has archaeological + mechanical sections | ~700 – 1,100 |
| **β** (baseline redefined) | Engine emits ONE file per query; baseline check on carry-over only | ~650 – 1,000 |
| **γ** (two files per query) | Engine emits TWO files per query (arch + mech · 6 total) | ~850 – 1,300 |

**Proposed band:** **`[650, 1,400]` raw LoC** (encompasses α/β/γ · Owner-canonical enumeration below).

**Owner-canonical enumeration** (following MRR precedent: engine + findings artifacts + supplement + tests):
- queries.py + run_queries.py + test file + 3 findings artifacts + v0.2_supplement + registry.yaml delta.
- Estimate: 650–1,300 LoC across scenarios.

### §6.3 §4.2 disclosure

- Ratified band `[650, 1,400]` — spans below-band-risk for β and top-edge for γ. Tier-2 disclosure per §12.1 non-blocking (precedent: Fixture Refresh · Registry Population · MRR).
- **§3.6 governance-doc carve-out:** NOT applied case-by-case per RP-E5 α. Band applies as-stated.

---

## §7. Out-of-scope statement (D7 · Owner-verbatim)

**Verbatim from Owner dispatch:**
> "Out of scope, D7 binding: sequencing harness, worker context-harnessing, any Registry content changes, Q2-05 individual reads (maintenance-turn business, better armed once queries land)."

**Explicitly out of scope this phase:**
1. **Sequencing harness** (§8.1.b · next candidate after this closes per Owner-explicit).
2. **Worker context-harnessing** (§8.1.c).
3. **Any Registry content changes** — v0.md + v0.1_supplement + registry.yaml locked at their ruled SHAs. New `v0.2_supplement.md` for SQ-G reflexive rows is not a content change to existing rows (additive-supplement per §14).
4. **Q2-05 individual reads** — Owner-explicit deferred to maintenance-turn business "better armed once queries land."

**Parallel Owner-side (builder does NOT touch):** Instance Replication Playbook · Commercial Thesis · Owner-parallel items stated once in Owner's process correction; do not appear in subsequent builder communications.

---

## §8. Baseline attest strategy statement

**Semantic scope of "reproduction":** pending Owner ruling on SQ-E1.

**Mechanical shape (uniform across α/β/γ):**
1. Engine runs against `docs/registry/machine/registry.yaml` (freshly regenerated from `v0.md + v0.1_supplement + v0.2_supplement` if that regeneration is in-scope; else against the on-disk machine form).
2. Engine emits findings artifacts.
3. `SQ-G-Baseline` test cell compares engine output to `docs/rulings/registry_findings_01_to_11.md` ruled-findings snapshot.
4. **Byte-identical reproduction** required for the ruled portion: all 11 finding_ids present + all `[RULED · …]` tags byte-identical + all `[OWNER: …]` markers preserved (matches MRR-G4 discipline).
5. **Zero phantom findings** in the ruled-portion (engine doesn't invent findings not in v0.md's ruled record).
6. **Zero losses** (no ruled finding disappears).

**Recovery path if baseline fails:** **fail-loud + HALT for Owner** (matches MRR-G3 discipline — deterministic gates fail; execution halts for Owner review). No auto-heal, no auto-degrade. Consistent with Owner-explicit "The engine proves itself against the record before it's trusted on anything new."

---

## §9. D-10 self-audit (rides submission)

| Class | Verdict | One-line reason |
|---|---|---|
| **D1 · Orphan gate** | **PASS** | All 9 SQ-G# gates in §4 carry promise (reused v0.md §2) + surface + enforcement + service_trace inheritance from Registry-infrastructure adjacency (per doctrine §3.6 "Registry pays rent"). Zero orphans introduced. |
| **D2 · NL-only enforcement** | **PASS** | All 9 gates mechanical (pytest cells + AST negative-scan + fs-count + hash-diff + grep-negative). Zero NL-only. |
| **D3 · Curated verdict** | **PASS** | Escalation matrix (§3) surfaces SQ-E1 as identified Owner-value seam without pre-resolving. Q1/Q2/Q3 semantics quoted verbatim from Owner dispatch. Zero builder curation. |
| **D4 · Rung inflation** | **PASS** | All 9 gates rung 1 · Deterministic. Owner-explicit "Rung 1 throughout." Zero LLM invocation. `SQ-G-Rung1` cell mechanically enforces this. |
| **D5 · Meta-spiral** | **PASS** | Queries are consumers of the Registry, not a new governance layer over it. Findings are inputs to rulings, not actions (Owner-explicit). Registry remains the primary artifact per doctrine §3.6. |
| **D6 · Service conflation** | **PASS** | SQ-G# rows use `governor: Named surfaces (Registry infrastructure · reflexive)` per MRR precedent. Zero persona optimization. |
| **D7 · Invented schedule or scope** | **PASS** | Only the 3 Owner-directed queries (Q1/Q2/Q3) + baseline attest + 9 gates. Explicit out-of-scope §7 verbatim from Owner. Zero references to sequencing harness · worker context-harnessing · Registry content changes · Q2-05 reads · Playbook · Thesis · next-cell scaffolds. Zero candidate promises minted (all 9 SQ-G reuse existing v0.md §2 promises · conservative D7). Zero re-opening of v0.md or v0.1_supplement source-of-truth. |

**Self-audit verdict:** all 7 defect classes **PASS**.

---

## §10. Reply body per Standing Rule v3

The builder emits to Owner (per Owner's process correction — verbatim relay only for Tier-1):
1. SHA of `/app/docs/stage_a_proposals/standing_queries_as_ci_stage_a.md`.
2. Pre-tiered escalation matrix summary: **Tier-1 count 1** (SQ-E1 · not zero — verbatim relay to Owner) · **Tier-2 count 3** · **Tier-3 count 7**.
3. SQ-E1 verbatim block for Owner relay.
4. D-10 self-audit verdict.
5. R4 reflexive attest: 9 SQ-G# rows land via `v0.2_supplement.md` per §14 (Tier-3 SQ-T3-supplement-file).
6. Band scenarios (α/β/γ) with derivation.
7. Baseline attest strategy statement (fail-loud + halt).

---

## §11. Standing constraints preserved

- **D7 binds:** scope limited to Owner-dispatched surfaces this phase.
- **MANDATE-COMPLETE 2026-07-10 held.** Registry Doctrine v1.0 + §14 in force. Parity 31/31.
- **Standing Rule v3:** on-disk canonical · SHA in reply · zero inline code dumps · no execution this Stage A.
- **Governance §12/§12.1/§12.2/§13/§14** in force. v0.md + v0.1_supplement byte-identical at their locked SHAs.
- **Standing loop:** Stage A → verbatim Tier-1 relay to Owner (SQ-E1) → ruling → atomic execution → close.

═══════════════════════════════════════════════════════════════════

*End of Stage A · Standing Queries as CI. 1 Tier-1 identified (SQ-E1 · Q2/Q3 archaeological-vs-mechanical divergence in baseline attest) requires Owner ruling before execution can proceed. D-10 all PASS. R4 reflexive rows planned via v0.2_supplement per §14. Standing Rule v3 · on-disk canonical.*
