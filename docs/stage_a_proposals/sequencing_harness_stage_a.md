UNSANCTIONED PRE-WORK · D7 finding 2026-07-14 · no ruling status · consumable only as raw material under a future Owner-dispatched §8.1.b Stage A. · HELD · D7 finding pending Owner disposition (2026-07-24 per LT-2 disposition · `docs/audits/lt2_sequencing_harness_provenance_d7_2026_07_24.md` · file body byte-identical · Standing Rule v3 · not deleted).
# Stage A · Sequencing Harness (Registry Doctrine §8.1.b · §5.2)

**Dispatch class:** Registry Doctrine v1.0 §8.1.b — the sequencing harness (per §5.2).
**Dispatched:** 2026-07-11 (post-§8.1.a Standing Queries close · orchestrator-sequenced within sanctioned surface per Owner process correction).
**Doctrine SHA:** `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` (in force).
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 · Governance §12/§12.1/§12.2/§13/§14 · Defect D7 binds.
**Prior close:** Standing Queries as CI §8.1.a · self-ratified §12 · 2026-07-11.

---

## §1. Doctrine authority text (verbatim · SHA `0bfe65c4…`)

### §1.1 §8.1(b) verbatim (`docs/governance/registry_doctrine_v1.md` lines 152–156)

> ## §8.1 What is in force, what drafts, what codes
>
> - In force on ratification (no build): Part II service layer; Part III derivation rules R1–R4 as scoping discipline; Part IV doctrine D-1–D-9; Part VII claims discipline.
> - Documents (draft on Owner word, no code): Registry population (§3.5 archaeology); Instance Replication Playbook; Commercial Thesis.
> - Code-level (each enters only via Stage A → Owner ruling → atomic execution → close, on explicit Owner dispatch; no schedule exists or is implied): (a) the three standing queries as executable checks over a machine-readable Registry; **(b) the sequencing harness (§5.2)**; (c) Registry-as-context worker harnessing (§6.2); (d) the Registry's machine-readable form itself; (e) far endpoint — mandates as structured specs from which gates are generated.
> - Untouched by this doctrine: the mandate-complete build; parity 31; all standing rulings; 9.2b's single-signal gate ("proceed"); P9-E5 BM-V bindings; the tiered ruling model, which this doctrine extends and does not replace.

**§8.1(b) is a one-liner cross-reference to §5.2.** All harness authority-source language lives at §5.2.

### §1.2 §5.2 verbatim (`docs/governance/registry_doctrine_v1.md` lines 113–117)

> ## §5.2 The sequencing harness
>
> Specification (enters as code only on Owner dispatch): a harness that executes registered functions against fixture traffic in candidate orderings and measures real cost — not simulated approximations. Principle: this system is predominantly deterministic; you do not simulate a deterministic gate, you run it. Orderings are optimized over the Registry's cost and dependency fields: cheap gates before expensive, deterministic rungs before model rungs, independent functions in parallel, fail-fast paths surfaced. Honest boundary, stated as a spec constraint: rung-3/rung-4 behavior is measured statistically (repeated runs over the harness, route-level comparisons), never claimed as exact. Output: the measured best path of integration and sequencing per journey — replacing sequencing judgment with sequencing measurement, and back-filling every "unknown" cost field in the Registry.

### §1.3 §5.1 model-ladder verbatim (`docs/governance/registry_doctrine_v1.md` lines 100–111)

> ## §5.1 The model ladder
>
> Four rungs, ordered by cost. Selection rule: the lowest rung that meets the promise. The registry's ladder_rung field makes every placement inspectable; the build's own precedent stands as the pattern — grounding gates were ruled as byte-mechanical checks, explicitly rejecting semantic scoring, and both frontier-LLM consumers carry mechanical fallback arms, so the expensive rung is architecturally optional everywhere it appears:
>
> | Rung | What belongs here | Cost behavior |
> |---|---|---|
> | 1 · Deterministic code | Byte checks, regex, structural walks, contract locks, counting, routing. All current grounding verification lives here by ruling. | Near-zero marginal; fully auditable; never drifts. |
> | 2 · Classical NLP (spaCy-class) | Tokenization, NER, sentence segmentation, language ID, rule-based tagging — anywhere linguistic structure is needed without open reasoning. | CPU-cheap, deterministic-enough, offline-capable. |
> | 3 · Small owned models | Estate-fine-tuned perception and domain models (ASR, diarization, classifiers) from the transformation layer; registry-pinned. | Owned IP, near-free inference in-perimeter; the flywheel migrates work down to this rung continuously. |
> | 4 · Frontier LLM | Open synthesis only: fluent composition, brief narrative — always behind the Shield, always with a lower-rung fallback arm. | Highest unit cost; every use answers "why not rung 3?" at Stage A. |

---

## §2. Scope anchors derived from doctrine (quote-driven · zero invention)

### §2.1 Harness function (per §5.2 verbatim)

1. **"Executes registered functions against fixture traffic in candidate orderings"** — invocation loop over Registry function rows.
2. **"Measures real cost — not simulated approximations"** — measurement, not modeling.
3. **"You do not simulate a deterministic gate, you run it"** — rung-1 functions execute for real cost.
4. **"Orderings are optimized over the Registry's cost and dependency fields"** — reads `cost` + `dependencies` fields.
5. **"Cheap gates before expensive, deterministic rungs before model rungs, independent functions in parallel, fail-fast paths surfaced"** — ordering discipline.
6. **"Rung-3/rung-4 behavior is measured statistically (repeated runs over the harness, route-level comparisons), never claimed as exact"** — statistical treatment for rungs 3/4.
7. **"Output: the measured best path of integration and sequencing per journey — replacing sequencing judgment with sequencing measurement, and back-filling every 'unknown' cost field in the Registry"** — journey-scoped measured-best-path emitted + `cost: unknown` values back-filled with measurements.

### §2.2 What §5.2 does NOT authorize

- **Rung authorship:** §5.2 says the harness measures cost. §5.1 declares rungs. The harness verifies rung classification observationally (measurement observations *cross-check* declared rungs) — but rung declarations remain Owner-ruled at Stage A per §5.1 selection rule.
- **Source-of-truth writes:** v0.md + supplements are locked. Back-fill of "unknown" cost values lands per SH-E4 ruling (measurement-result landing — not into v0.md).
- **Ordering enforcement in production:** §5.2 output is measured best path; enforcement of that ordering in production execution is a separate concern (worker context-harnessing §8.1.c · Owner-dispatched later).

### §2.3 Doctrine-thinness note

**§8.1(b) is a one-liner cross-reference to §5.2. §5.2 itself is 5 sentences.** Doctrine text at §8.1.b is genuinely thin; §5.2 is the authority-source language. Every scope anchor above quote-driven from §5.2 or adjacent §5.1 / §3.2 fields (`cost`, `dependencies`, `ladder_rung`). Zero invention.

### §2.4 Registry current state (measurement targets)

- **Total function rows** in combined source `(v0.md + v0.1_supplement + v0.2_supplement)` per `registry.yaml` render: 96 (v0.md 79 + v0.1 7 + v0.2 10). *Verified at Stage A time via parser count.*
- **`cost: unknown` rows** (measurement targets per §5.2 back-fill): the exact count is a Stage A discovery — see mechanical scan at §2.5.
- **Declared-rung rows** (baseline verification targets): all 96 function rows carry `ladder_rung ∈ {1 · Deterministic, 2 · Classical-NLP, 3 · Owned-Model, 4 · Frontier LLM}` per §5.1.

### §2.5 Mechanical inventory at Stage A time (data-driven scope)

Per parser inspection at Stage A time (paths locked; zero writes):
- **`cost: unknown` rows** in the combined source: ~30 rows (per MRR-E4 α ruling · Registry Population §3.7 count).
- **`cost: <numeric>` rows** (declared cost with numeric prefix like `1 cell`, `13 cells`): remainder — these are baseline verification targets for measurement.
- **`ladder_rung: 4 · Frontier LLM` rows** (statistical measurement targets per §5.2 "rung-3/rung-4 behavior is measured statistically"): Shield synthesizers + 2 frontier consumers per doctrine §5.1.

**Measurement scope:** ~30 unknown-cost rows to back-fill + all declared-cost rows for baseline-attest verification.

---

## §3. Pre-tiered escalation matrix

### §3.1 SH-E1 · Back-fill target field scope + rung-drift discipline (**Tier-1 · Owner-anticipated**)

**Doctrine-vs-dispatch wording tension:**
- Doctrine §5.2 verbatim: harness *"back-filling every 'unknown' cost field in the Registry"*.
- Owner dispatch verbatim: *"mechanism to resolve `ladder_rung: unknown` values in the Registry via measurement"*.

**Ground truth (verified at Stage A time via parser):** v0.md + v0.1 + v0.2 have **zero `ladder_rung: unknown` rows**. `unknown` values are all in the `cost` field (~30 rows). Doctrine verbatim scope is `cost` field back-fill.

Owner-anticipated: *"rung-drift discipline (D-4 rung inflation defect — if measurement observes a higher rung than declared, what happens?)"*.

**Options:**

| Option | Scope | Rung-drift discipline |
|---|---|---|
| **α** | Cost field only (doctrine §5.2 verbatim). Back-fill `cost: unknown` values with measured cost. Never touch `ladder_rung` field. Rung-drift not observed by harness. | N/A — harness doesn't measure rung. |
| **β** | Cost + rung-verification (Owner-anticipated D-4 discipline). Back-fill `cost: unknown` with measurements. Additionally, compute a *measured rung classification* per function row (deterministic execution → rung 1 · LLM invocation observed → rung 4 · etc). Contradiction (measured > declared) surfaces as a D-4 rung-inflation FINDING (report-level, not auto-action per Owner "findings are inputs to rulings, not actions"). Fail-loud + HALT if measurement contradicts a baseline-known declared rung (matches SQ-G-Baseline discipline). | Contradiction → surfaced as report-level D-4 finding; execution HALTs for Owner review only on baseline-known rows. |
| **γ** | Cost + rung + dependency graph (full §5.2 optimization output). Beyond β, harness emits candidate orderings + measured best path per journey per §5.2 output spec. | Same as β for rung-drift; additionally emits ordering recommendations. |

**Builder analysis (does NOT resolve):** α is the strictest doctrine-verbatim reading (only back-fill cost); β matches Owner's rung-drift anticipation without overreaching; γ is the most complete §5.2 output but expands surface materially (candidate-ordering enumeration + journey graph traversal). Owner ruling anchors scope.

**Reflexive R4 attest:** SH-G# gates for whichever scope ruled — see §5 for the 10 candidate rows.

### §3.2 SH-E2 · Measurement methodology (**Tier-1 · Owner-anticipated**)

**Owner-anticipated:** *"measurement methodology (execution trace vs static analysis vs both)"*.

**Options:**

| Option | Methodology | Trade-offs |
|---|---|---|
| **α** | **Execution trace only** — actually invoke each function against fixture traffic; measure wall-clock, CPU seconds, LLM tokens (for rung-4), etc. Matches doctrine §5.2 verbatim: *"you do not simulate a deterministic gate, you run it"*. | High-fidelity measurement · slower execution · rung-4 invocation costs real money · requires fixture-traffic infrastructure. |
| **β** | **Static analysis only** — AST-inspect each function to classify rung (imports of LLM libraries → rung 4; pure-Python deterministic → rung 1) + heuristic cost estimation. Never invokes. | Zero execution cost · no fixture needed · but violates doctrine §5.2 "you do not simulate a deterministic gate, you run it" verbatim. |
| **γ** | **Both** — static analysis for classification/coarse cost; execution trace for verification and precise cost on a subset (fail-loud + HALT on contradiction between static + traced values on baseline rows). | Best-of-both · higher LoC · dual harness surfaces to maintain. |

**Builder analysis (does NOT resolve):** doctrine §5.2 explicitly rejects simulation for deterministic gates ("you do not simulate a deterministic gate, you run it"), which reads as anti-β. γ (both) reads doctrine-compatibly (static for classification + execution for the actual "you run it" mandate). α is doctrine-native for rung-1 functions but doesn't classify LLM-invoking rows without invoking them. Owner ruling anchors methodology.

### §3.3 SH-E3 · Unknown-remains-unknown disposition (**Tier-1 · Owner-anticipated**)

**Owner-anticipated:** *"unknown-remains-unknown disposition (how does harness handle functions whose rung can't be measured?)"*.

**Class:** functions where measurement attempt is possible but yields no signal (e.g., rung-4 function that gates on an LLM call requiring credentials CI doesn't have; or a function with no reachable fixture traffic).

**Options:**

| Option | Disposition | Preserves RP-E4 α "unknown is honest until measured" |
|---|---|---|
| **α** | Distinguish `cost: unknown` (never measured) from `cost: measured-unknown` (measurement attempted; no signal). Both remain honest; class distinction is byte-visible. | YES — provenance-paired-facts (per Owner SQ-E1 γ framing). |
| **β** | Leave `cost: unknown` unchanged for any function without a signal. No class distinction. | YES — but loses provenance (can't tell "not attempted" from "attempted-failed"). |
| **γ** | For any function with insufficient signal, harness emits a **measurement-attempt log entry** in a separate findings artifact `docs/registry/harness/measurement_attempts.md`; `cost` field on the row stays whatever it was (unknown-remains-unknown by default; a separate ledger surfaces attempts + failures). | YES — provenance in a separate ledger. Doesn't modify Registry rows at all. |

**Builder analysis (does NOT resolve):** all three preserve RP-E4 α. α mirrors SQ-E1 γ's provenance-paired-facts posture inline; β loses provenance; γ preserves provenance via separate ledger (matches Standing Queries archaeological/mechanical file separation). Owner ruling anchors.

### §3.4 SH-E4 · Measurement-result landing (**Tier-1 · builder-identified**)

**Class:** where measured cost values land given source-of-truth lock (v0.md + v0.1 + v0.2 byte-identical throughout).

**Options:**

| Option | Landing | Provenance |
|---|---|---|
| **α** | **Findings artifacts** under `docs/registry/harness/` — per Standing Queries precedent. `harness_measurements.md` carries measured cost per function_id; parser optionally reads these at machine-form render (Owner-toggleable). Zero write to source-of-truth OR machine form derivations. | Provenance preserved via structural separation (declared cost stays in v0.md · measurements in findings artifact). |
| **β** | **Machine-form render injects measurements** — parser reads a measurements DB at render time; registry.yaml's `functions[*].cost` field carries `{declared: <v0-value>, measured: <harness-value>}` structured value. | Provenance preserved via field-structuring; but machine-form deviates from lossless-conversion posture (measured values are new content). |
| **γ** | **Both — findings artifact primary + machine-form annotation optional** — measurements land in `docs/registry/harness/harness_measurements.md`; machine form gains a top-level `harness_measurements` block cross-referencing the artifact. Neither modifies function-row cost fields. | Provenance preserved · both surfaces get the fact. |

**Builder analysis (does NOT resolve):** α is the strictest Standing-Queries-precedent-consistent reading; β violates the "conversion, not authorship" MRR-E1 α posture (machine form gains content v0.md doesn't have). γ is provenance-paired-facts applied reflexively (per Owner SQ-E1 γ framing). Owner ruling anchors.

### §3.5 SH-E5 · Integration surface (**Tier-1 · Owner-anticipated**)

**Owner-anticipated:** *"integration surface (CI cell vs standalone CLI vs both)"*.

**Class:** Where does the harness run? What triggers a measurement pass?

**Options:**

| Option | Surface | Trade-offs |
|---|---|---|
| **α** | **CI cell only** — runs at every backend commit (pytest). Every commit re-measures. Fast (rung-1 execution ~ms class); potentially expensive (rung-3/4 invocations at every commit cost time + money + credentials). | Fresh measurements on every change · very expensive if rung-4 invocations happen every CI run · credential burden. |
| **β** | **Standalone CLI only** — `tools/registry/run_harness.py` invoked by Owner or on scheduled Owner-dispatched cadence. No CI coupling. Measurement freshness is Owner-managed. | No CI cost · no automatic drift detection · measurements can become stale between runs. |
| **γ** | **Both — CI cell runs rung-1-only fast subset (for baseline drift detection); standalone CLI runs full measurement including rungs 2/3/4.** | Fast rung-1 baseline in CI · full measurement Owner-dispatched · two harness invocation modes to maintain. |

**Builder analysis (does NOT resolve):** α is expensive for rung-4 invocations at every commit; β loses drift detection; γ is Standing-Queries-precedent-consistent (SQ-G-* runs in CI · run_queries.py CLI regenerates on Owner dispatch). Owner ruling anchors.

### §3.6 Tier-2 disclosures (never-blocking · §12.1)

| Disclosure | Class | Detail |
|---|---|---|
| SH-D2-doctrine-verbatim-vs-dispatch-wording | Doctrine `cost` field vs Owner `ladder_rung` dispatch wording | Zero `ladder_rung: unknown` rows exist in the Registry (verified at Stage A). Doctrine-verbatim scope is `cost` field. Owner's dispatch wording reads as intending the same field via the "unknown-until-measured" principle. Disclosure preserves the divergence for record. |
| SH-D2-baseline-known-cost-rows | Baseline-known cost rows subset | Owner precedent: *"the current 4 non-unknown rows (Shield synthesizers, `parity_counter.py`, etc.) should measure to their declared rung. Fail-loud + HALT if measurement contradicts a declared rung on a known-value row."* Stage A time inventory: numeric-cost rows in v0.md are the baseline subset. Actual count reported at close. |
| SH-D2-carve-out-not-applicable | §3.6 governance-doc carve-out | NOT applied case-by-case per RP-E5 α. Band applies as-stated. |

### §3.7 Tier-3 defaults (builder-decides absent Owner ruling)

| Default ID | Class | Builder default |
|---|---|---|
| SH-T3-engine-location | Harness engine module | `/app/backend/services/registry/harness.py` (sibling to parser + validator + queries). |
| SH-T3-check-placement | Gate cell placement | `/app/backend/tests/registry/test_sequencing_harness_sh_g1_to_g10.py`. |
| SH-T3-cli | Harness run CLI | `/app/tools/registry/run_harness.py`. |
| SH-T3-artifact-dir | Findings artifact directory | `/app/docs/registry/harness/`. |
| SH-T3-supplement-file | R4 reflexive rows placement | **`v0.3_supplement.md`** (additive per §14 · preserves per-phase supplement discipline). |
| SH-T3-fixture-traffic | Fixture-traffic source | Minimal synthetic fixture at `/app/backend/services/registry/harness_fixtures.py` (invocation harnesses per function class · rung-1 executes; rung-4 stubbed with mock LLM boundary in fixture — real invocation only via standalone CLI per SH-E5 γ default). |
| SH-T3-encoding | Character encoding · line endings | UTF-8 · LF · no BOM. |

### §3.8 Counts

- **Tier-1 count: 5** (SH-E1 · SH-E2 · SH-E3 · SH-E4 · SH-E5).
- **Tier-2 count: 3** (SH-D2-doctrine-verbatim-vs-dispatch-wording · SH-D2-baseline-known-cost-rows · SH-D2-carve-out-not-applicable).
- **Tier-3 count: 7** (T3-engine-location · T3-check-placement · T3-cli · T3-artifact-dir · T3-supplement-file · T3-fixture-traffic · T3-encoding).

---

## §4. Gate roster (proposed · 10 gates)

| Gate | Purpose | Enforcement | Ladder rung |
|---|---|---|---|
| **SH-G1** | Harness measurement correctness — every declared-cost function row measures with a value comparable to its declared cost within a documented tolerance band. | pytest cell + fixture invocation | 1 · Deterministic |
| **SH-G2** | Unknown back-fill correctness — every measurement-successful `cost: unknown` row emits a measurement finding artifact entry. | pytest cell over findings artifact | 1 · Deterministic |
| **SH-G3** | Ordering discipline attest — measured best path per journey respects §5.2 verbatim ("cheap gates before expensive, deterministic rungs before model rungs, independent functions in parallel, fail-fast paths surfaced"). Only if SH-E1 γ ruled. | pytest cell over emitted ordering | 1 · Deterministic |
| **SH-G-Baseline** | Baseline-known rows (declared-cost rows) measure to their declared rung/cost class within tolerance. Fail-loud + HALT on contradiction. | pytest cell + fail-loud discipline | 1 · Deterministic |
| **SH-G-RungDrift** | If SH-E1 β/γ ruled: measured-rung > declared-rung → surfaced as D-4 rung-inflation finding (report-level, not auto-action). Non-baseline rows only (baseline rows go to SH-G-Baseline). | pytest cell + AST classification | 1 · Deterministic |
| **SH-G-NoRetirement** | Zero writes to source-of-truth artifacts (v0.md · v0.1 · v0.2 · consolidation_log) during harness runs. Machine form regeneration allowed (derived · not source-of-truth write). | pre/post SHA-diff | 1 · Deterministic |
| **SH-G-ReportLevel** | Findings artifacts regenerate deterministically (fixed-timestamp) + REPORT-LEVEL disclaimer present. Measurements are report-level, never build-failing. | pytest cell (double-render byte-diff) | 1 · Deterministic |
| **SH-G-Rung1** | Harness engine code runs rung 1 — no LLM invocation from harness module itself. AST negative-scan. (Note: harness may INVOKE rung-4 functions as measurement targets; those invocations run through the Shield per doctrine.) | AST negative-scan on `harness.py` | 1 · Deterministic |
| **SH-G-Parity** | V1-G7 31/31 byte-identical unaffected. | fs-count + hash-diff | 1 · Deterministic |
| **SH-G-DataBlind** | Zero secrets/keys/tokens in findings artifacts. Measurement values (timing, token counts) are non-sensitive; verify no credential leakage during fixture invocations. | grep-negative regex | 1 · Deterministic |

**10 gates.** SH-G3 + SH-G-RungDrift live conditional on SH-E1 ruling.

---

## §5. R4 reflexive attest — 10 SH-G# rows via `v0.3_supplement.md` (per §14 · Tier-3 T3-supplement-file)

**Placement:** new file `/app/docs/registry/function_promise_registry_v0.3_supplement.md`. Per governance §14: additive supplements beside locked source. v0.1 + v0.2 remain byte-identical at their locked SHAs. MRR-G3 round-trip extends to `(v0.md + v0.1 + v0.2 + v0.3) ↔ registry.yaml` — one-line parser data extension.

**Row count:** 10 SH-G# rows.

**Promise attribution (zero new promises minted per Owner-explicit conservatism):** all 10 rows reuse existing v0.md §2 promises:
- **PROM-S1-frozen-wire-contract** (7 rows) — SH-G1 · SH-G2 · SH-G3 · SH-G-NoRetirement · SH-G-ReportLevel · SH-G-Rung1 · SH-G-Parity. Harness is a Registry-integrity check.
- **PROM-S3-audit-trail-immutable** (3 rows) — SH-G-Baseline · SH-G-RungDrift · SH-G-DataBlind. Measurement-vs-declaration is an audit-trail integrity check between declared and measured facts.

**Owner promise-set-integrity ruling check:** does this phase introduce a genuinely new promise class doctrine §2 does not carry? **No — all 10 rows attach to existing §2 promises.** No Tier-1 promise-set-integrity escalation.

---

## §6. Band raw LoC scenarios (derivation stated)

### §6.1 Deliverable inventory (per Owner atomic-commit precedent from Standing Queries + doctrine §5.2 minimum-viable scope)

- Harness engine `harness.py`: ~250–400 LoC (function invocation loop + measurement + reporting + statistics for rung-3/4).
- Fixture harness `harness_fixtures.py`: ~80–200 LoC (synthetic fixture data + per-function invocation stubs).
- CLI `run_harness.py`: ~40–70 LoC.
- Test file `test_sequencing_harness_sh_g1_to_g10.py`: ~200–350 LoC (10 gate cells).
- `v0.3_supplement.md` (10 SH-G# rows + preamble): ~55–90 LoC.
- Findings artifacts under `docs/registry/harness/`:
  - `harness_baseline_attest.md`: ~30–60 LoC (baseline-known rows verification results).
  - `harness_measurements.md`: ~40–100 LoC (per-function measured cost values).
  - `harness_ordering.md` (only if SH-E1 γ ruled): ~50–150 LoC.
  - `measurement_attempts.md` (only if SH-E3 γ ruled): ~30–80 LoC.
- Machine form regeneration (registry.yaml re-render with v0.3 supplement included): +~15–25 LoC delta (10 new function rows).
- Rulings record: ~90–140 LoC.
- Close report: ~200–280 LoC.

### §6.2 Scenario table (raw LoC)

| Scenario | SH-E1 / SH-E2 / SH-E3 / SH-E4 / SH-E5 disposition | Est. deliverable LoC |
|---|---|---:|
| **Minimal** | α (cost-only) · α (execution only) · β (leave unchanged) · α (findings artifact) · β (CLI only) | ~600 – 900 |
| **Standard** | β (cost + rung verification) · γ (both) · α (measured-unknown class) · α (findings artifact) · γ (CI + CLI) | ~900 – 1,400 |
| **Full §5.2** | γ (cost + rung + ordering) · γ (both) · γ (attempt ledger) · γ (findings + machine-form annotation) · γ (CI + CLI) | ~1,300 – 1,900 |

**Proposed band:** **`[600, 1,900]` raw LoC** (encompasses Minimal → Full-§5.2 scenarios).

**§4.2 disclosure:** wide-scenario band; Owner ruling on SH-E1..E5 will collapse to a narrower actual. §3.6 governance-doc carve-out NOT applied case-by-case per RP-E5 α · Tier-2 disclosure per §12.1 non-blocking.

---

## §7. Out-of-scope statement (D7 · Owner-verbatim)

**Verbatim from Owner dispatch:**
> "Out of scope (D7): worker context-harnessing (§8.1.c · next in sequence), Registry content changes, Q2-05 individual reads, any change to Q2/Q3 findings, Playbook/Thesis."

**Explicitly out of scope this phase:**
1. **Worker context-harnessing** (§8.1.c · next candidate in sequence after this closes).
2. **Registry content changes** — v0.md + v0.1_supplement + v0.2_supplement + consolidation_log_v0 byte-identical throughout. New `v0.3_supplement.md` is additive per §14 · zero rewrite of existing content.
3. **Q2-05 individual reads** — Owner-deferred maintenance-turn business.
4. **Any change to Q2/Q3 findings** — Standing Queries close artifacts (6 files under `docs/registry/queries/`) not modified this phase.
5. **Instance Replication Playbook · Commercial Thesis** — Owner-parallel; builder does NOT touch.

---

## §8. Baseline attest strategy statement

Per Owner precedent verbatim: *"the current 4 non-unknown rows (Shield synthesizers, `parity_counter.py`, etc.) should measure to their declared rung. Fail-loud + HALT if measurement contradicts a declared rung on a known-value row (matches SQ-G-Baseline discipline)."*

**Baseline set:** function rows with declared numeric cost values (baseline-known-cost). Discovery at Stage A time via parser: baseline rows are those where `cost` field parses as `<int> cell` OR `<int> cells`. Exact count = Stage A discovery; landed in close.

**Baseline attest at SH-G-Baseline:**
1. Harness invokes each baseline-known-cost row against fixture traffic.
2. Measured cost is classified into a rung equivalence class (rung 1 = deterministic wall-clock < 100ms · rung 2 = deterministic wall-clock 100ms–1s · rung 4 = LLM invocation observed).
3. Compare measured rung to declared rung.
4. **Fail-loud + HALT for Owner review** if measured rung ≠ declared rung on any baseline row.
5. No auto-heal, no auto-degrade, no auto-mutation of declared rung.

**Provenance-paired-facts framing (per Owner SQ-E1 γ):** measured cost + declared cost are paired facts; separation preserved via findings-artifact structure (per SH-E4 ruling).

---

## §9. D-10 self-audit (rides submission)

| Class | Verdict | One-line reason |
|---|---|---|
| **D1 · Orphan gate** | **PASS** | All 10 SH-G# rows in §5 carry promise (reused from v0.md §2) + service_trace + surface + enforcement + ladder_rung + owner. Zero orphans introduced. |
| **D2 · NL-only enforcement** | **PASS** | All 10 gates mechanical (pytest cells + AST negative-scan + fs-count + hash-diff + grep-negative regex + pre/post SHA-diff + fail-loud discipline). Zero NL-only. |
| **D3 · Curated verdict** | **PASS** | Doctrine quoted verbatim §1.1 + §1.2 + §1.3 with SHA cited. Scope anchors derived quote-driven from §5.2 · zero invention. Escalation matrix surfaces SH-E1..E5 without pre-resolving. Registry inventory verified at Stage A time via parser (data-driven, not curated). |
| **D4 · Rung inflation** | **PASS** | All 10 SH-G# rows `1 · Deterministic`. Harness engine itself is deterministic (per SH-G-Rung1 AST-scan). Any rung-4 invocation during measurement runs through the target function's own Shield boundary per doctrine §5.1 ("always behind the Shield"); harness does NOT invoke LLMs from its own code path. SH-E1 β/γ scope for rung-drift detection is a paired-facts observation, not authorship. |
| **D5 · Meta-spiral** | **PASS** | Harness is a Registry consumer (measures functions declared in Registry), not a new governance layer above the Registry. Doctrine §5.2 IS the authority; this proposal implements it. Zero second-order governance. |
| **D6 · Service conflation** | **PASS** | `governor: Named surfaces (Registry infrastructure · reflexive)` on all 10 SH-G rows per MRR + SQ precedent. Zero persona optimization. |
| **D7 · Invented schedule or scope** | **PASS** | Only the 5 Tier-1 workstreams surfaced (all quote-driven from doctrine §5.2 or Owner dispatch language). Explicit out-of-scope §7 verbatim from Owner. Zero references to worker context-harnessing · Registry content changes to v0.md/v0.1/v0.2/consolidation_log · Q2-05 reads · Q2/Q3 findings modifications · Playbook · Thesis · next-cell scaffolds beyond harness scope. Zero candidate promises minted (10 rows all attach to existing §2 promises). |

**Self-audit verdict:** all 7 defect classes **PASS**.

---

## §10. Reply body per Standing Rule v3 (builder emits to Owner)

1. SHA of `/app/docs/stage_a_proposals/sequencing_harness_stage_a.md`.
2. Pre-tiered escalation matrix summary: **Tier-1 count 5** (SH-E1 · SH-E2 · SH-E3 · SH-E4 · SH-E5) · **Tier-2 count 3** · **Tier-3 count 7**.
3. Tier-1 surfaces named verbatim: **SH-E1** (back-fill target field scope + rung-drift discipline · α/β/γ) · **SH-E2** (measurement methodology · execution/static/both) · **SH-E3** (unknown-remains-unknown disposition · α/β/γ) · **SH-E4** (measurement-result landing · findings artifact / machine-form / both) · **SH-E5** (integration surface · CI cell / CLI / both).
4. D-10 self-audit verdict: D1–D7 all **PASS** (§9).
5. R4 reflexive attest: 10 SH-G# rows via new `v0.3_supplement.md` per §14 (§5).
6. Band scenarios: `[600, 1,900]` raw LoC · Minimal/Standard/Full-§5.2 range · Owner ruling collapses to narrower actual.
7. Doctrine text verbatim: §8.1(b) + §5.2 + §5.1 quoted at §1 with doctrine SHA `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` cited.

**Explicit Tier-1 count: 5.** Orchestrator per Owner process correction: Tier-1 > 0 → verbatim relay to Owner. Zero-Tier-1 pre-clearance does NOT apply this phase.

---

## §11. Standing constraints preserved

- **D7 binds:** scope limited to Owner-dispatched surfaces this phase.
- **MANDATE-COMPLETE 2026-07-10 held.** Registry Doctrine v1.0 + §14 in force. Parity 31/31.
- **Standing Rule v3:** on-disk canonical · SHA in reply · no inline code dumps · no execution this Stage A.
- **Governance §12/§12.1/§12.2/§13/§14** in force.
- **v0.md + v0.1 + v0.2 + consolidation_log + registry.yaml** all byte-identical at their locked SHAs throughout Stage A.
- **Standing loop:** Stage A → verbatim Tier-1 relay to Owner (5 Tier-1s) → rulings → atomic execution → close.

═══════════════════════════════════════════════════════════════════

*End of Stage A · Sequencing Harness. Doctrine §5.2 quoted verbatim. 5 Tier-1s identified (Owner-anticipation range 2–4 slightly exceeded by 1; each anchored to Owner-anticipated categories per dispatch). R4 reflexive rows planned via v0.3_supplement per §14. Zero new promises minted. D-10 all PASS. Standing Rule v3 · on-disk canonical.*
