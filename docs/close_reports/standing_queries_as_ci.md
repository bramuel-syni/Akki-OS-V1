# Close Report · Standing Queries as CI (Registry Doctrine §8.1.a)

**Phase class:** Registry Doctrine v1.0 §8.1.a — three standing queries (Q1 redundancy · Q2 orphans · Q3 gaps) as executable checks over the machine-readable Registry.
**Landed:** 2026-07-11 (atomic single commit).
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 · Governance §12/§12.1/§12.2/§13/§14 · Defect D7 binds.
**Prior close:** Machine-Readable Registry §8.1.d · self-ratified §12 · 2026-07-11.

---

## §1. Artifact roster (SHAs)

| Artifact | Path | SHA-256 | LoC |
|---|---|---|---:|
| Stage A proposal (reference) | `/app/docs/stage_a_proposals/standing_queries_as_ci_stage_a.md` | `942c9f73…` | 273 |
| **Owner rulings record** (NEW) | `/app/docs/rulings/standing_queries_sq_e1.md` | `705dc3df…` | 74 |
| **v0.2 Supplement** (NEW · 10 SQ-G# R4 rows per §14) | `/app/docs/registry/function_promise_registry_v0.2_supplement.md` | `25c5dd5a…` | 51 |
| Query engine (NEW) | `/app/backend/services/registry/queries.py` | `a615e279…` | 645 |
| Query CLI (NEW) | `/app/tools/registry/run_queries.py` | `355fba80…` | 57 |
| Pytest cells (NEW · 15 tests · SQ-G1..SQ-G-DataBlind) | `/app/backend/tests/registry/test_standing_queries_sq_g1_to_g10.py` | `016728ff…` | 322 |
| **Q1 archaeological artifact** (NEW) | `/app/docs/registry/queries/q1_archaeological.md` | `f2cc4c8f…` | 28 |
| **Q1 mechanical artifact** (NEW) | `/app/docs/registry/queries/q1_mechanical.md` | `40e74db8…` | 25 |
| **Q2 archaeological artifact** (NEW) | `/app/docs/registry/queries/q2_archaeological.md` | `5fabdb52…` | 25 |
| **Q2 mechanical artifact** (NEW) | `/app/docs/registry/queries/q2_mechanical.md` | `a91088d8…` | 23 |
| **Q3 archaeological artifact** (NEW) | `/app/docs/registry/queries/q3_archaeological.md` | `2c38f267…` | 26 |
| **Q3 mechanical artifact** (NEW) | `/app/docs/registry/queries/q3_mechanical.md` | `098cf832…` | 34 |
| Parser (MODIFY · +v0.2 path) | `/app/backend/services/registry/parser.py` | `84d6ab4e…` | 495 |
| Machine form (regenerated · includes v0.2 supplement) | `/app/docs/registry/machine/registry.yaml` | `708ddec7…` | 2,053 |
| **v0.md** (LOCKED · byte-identical) | `/app/docs/registry/function_promise_registry_v0.md` | `598a7ad4…` **UNCHANGED** | 307 |
| **v0.1 supplement** (LOCKED · byte-identical) | `/app/docs/registry/function_promise_registry_v0.1_supplement.md` | `2822f99e…` **UNCHANGED** | 48 |
| **consolidation log v0** (LOCKED · byte-identical) | `/app/docs/registry/consolidation_log_v0.md` | `2c604255…` **UNCHANGED** | 157 |
| Rulings carrier (LOCKED) | `/app/docs/rulings/registry_findings_01_to_11.md` | `20e03f40…` | 153 |

---

## §2. Source-of-truth byte-identity attest (pre + post commit)

- **v0.md:** `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0` — byte-identical.
- **v0.1_supplement:** `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092` — byte-identical.
- **consolidation_log_v0:** `2c60425599afbd59cb083cc8a391a94b717598a796a8028ca28ca4176ab26062` — byte-identical.

**SQ-G-NoRetirement gate GREEN** — zero writes to source-of-truth during query runs.

---

## §3. Gate roster (10/10 GREEN)

| Gate | Purpose | Enforcement | Status |
|---|---|---|---|
| **SQ-G1** | Q1 (redundancy) mechanical correctness — pair-scan for same PROM-token-set + same surface | pytest cell | **GREEN** |
| **SQ-G2** | Q2 (orphans) mechanical correctness — 4 sub-cases (a/b/c/d) over function rows | pytest cell | **GREEN** |
| **SQ-G3** | Q3 (gaps) mechanical correctness — (a) promise-without-function · (b) Part-II-step-without-function with alias equivalence | pytest cell | **GREEN** |
| **SQ-G-Baseline** | Archaeological files reproduce v0.md §4 (5 Q2) + §5 (6 Q3) + consolidation_log §1 (4 MERGE + 4 TIE-BROKE) byte-identical · fail-loud + HALT on any deviation | pytest cell + structured-path diff | **GREEN** (11/11 Q2/Q3 · 8/8 CL entries) |
| **SQ-G-CrossRef** | Mechanical entries whose subject overlaps an archaeological finding carry `overlaps: <finding_id>` annotation · PERMANENT (not first-run-only) | pytest cell over emitted artifacts | **GREEN** (2 legitimate overlaps annotated · zero phantoms in new-candidates sections) |
| **SQ-G-NoRetirement** | Zero writes to source-of-truth artifacts during query runs | pre/post SHA-diff | **GREEN** |
| **SQ-G-ReportLevel** | Findings artifacts regenerate deterministically + REPORT-LEVEL disclaimer present on all 6 files | pytest cell (double-render byte-diff empty) | **GREEN** |
| **SQ-G-Rung1** | Query engine has zero LLM imports — AST negative-scan | pytest cell (AST walk on `queries.py`) | **GREEN** |
| **SQ-G-Parity** | V1-G7 31/31 byte-identical unaffected | fs-count + hash-diff | **GREEN** (31/31) |
| **SQ-G-DataBlind** | Zero secrets/keys/tokens in 6 findings artifacts | grep-negative regex | **GREEN** |

**10 of 10 gates GREEN.**

---

## §4. Baseline-attest result (Owner-explicit close requirement)

### §4.1 Archaeological carry-over (11/11 ruled findings)

**Q1 archaeological (consolidation_log_v0.md §1 · 8 entries):**
- MERGE entries: CL-1.1..CL-1.4 (4 merges — PROM-S1-byte-verbatim-anchor-grounding · PROM-S1-no-semantic-scoring · PROM-S1-frozen-wire-contract · PROM-S1-class-honesty-render-time).
- TIE-BROKE-TOWARD-DISTINCT entries: CL-1.5..CL-1.8 (4 tie-breaks per RP-E1 α).

**Q2 archaeological (v0.md §4 · 5 findings):**
- Q2-01 · Q2-02 · Q2-03 · Q2-04 · Q2-05 — all with `[RULED · …]` tags byte-identical.

**Q3 archaeological (v0.md §5 · 6 findings):**
- Q3-01..Q3-06 — all with `[RULED · …]` tags + `[OWNER: …]` markers preserved byte-identical (`Q3-02` carries `[OWNER: future phase]`; `Q3-03` carries `[OWNER: buyer-commercial-tier]`).

**Total ruled-findings carried:** 11/11 (Q2 + Q3) + 8/8 (Q1 consolidation log). Byte-identical reproduction verified.

### §4.2 Mechanical candidate counts (per query)

| Query | New mechanical candidates | Overlapping archaeological subjects | Total emitted |
|---|---:|---:|---:|
| **Q1** | 1 | 0 | 1 |
| **Q2** | 0 | 0 | 0 |
| **Q3** | 7 | 2 | 9 |

**Q1 new candidate** (1 pair): `registry.doctrine_v1_reference` ↔ `registry.population.gaux_doctrine_ref` — shared `PROM-S3-governance-doc-on-disk` + shared surface `This file §1`. Both are R4 reflexive rows from Registry Population §3.g referencing the doctrine document. Legitimate dedup candidate for future Owner-dispatched Registry-maintenance turn.

**Q3 new candidates (7):**
- (a) `PROM-S5-substrate-not-optimized-against` — zero citations (expected per doctrine "S5 registered so nothing optimizes against it").
- (a) `PROM-fixture-refresh-source-of-truth` — zero citations.
- (b) `S2.census-fills` · `S2.sample` · `S3.change-rules-with-ceremony` · `S3.pick-run` · `S3.see-retention` — PART_II journey steps with zero citing function rows in the current Registry.

**Q3 overlapping (2 · annotated `overlaps: …` per SQ-G-CrossRef PERMANENT rule):**
- `S2.onboard-context` → `overlaps: Q3-02` (Q3-02 archaeological finding subject matches).
- `PROM-S1-config-defect-fail-loud` → `overlaps: CL-1.5` (CL tie-break entry mentions this promise).

**Cross-reference discipline attested:** zero mechanical overlaps in the "New candidates" section of any mechanical file (verified by SQ-G-CrossRef test cell running the engine + inspecting emitted artifacts).

### §4.3 Baseline failure mode

**Configured as ruled:** fail-loud + HALT for Owner on any deviation from byte-identical archaeological reproduction. Matches MRR-G3 discipline. **No auto-heal. No auto-degrade.** Consistent with Owner-explicit *"The engine proves itself against the record before it's trusted on anything new."*

---

## §5. Cross-reference condition attested (Owner-explicit permanent · SQ-G-CrossRef)

Owner-verbatim: *"where a mechanical entry's subject overlaps an existing archaeological finding (now or in any future run), the mechanical file annotates with the finding id (`overlaps: Q3-05`) rather than raising it as new — 'zero phantom findings' applies to the mechanical surface too, permanently, not just at baseline."*

**Implementation attest:**
- `backend/services/registry/queries.py::build_archaeological_index` builds subject→finding-id lookup at scan time.
- `overlaps_for()` returns matching archaeological finding IDs per mechanical entry's `subject_identifiers`.
- Rendering functions split output into two sections: **New candidates** (no arch overlap) + **Overlaps with archaeological subjects** (annotated with `overlaps: <finding_id>`).
- SQ-G-CrossRef test cell asserts zero `overlaps:` strings appear in the New-candidates section of any mechanical file.
- **Discipline is PERMANENT — not first-run heuristic.** Applies to every subsequent regeneration.

---

## §6. Band actual + verdict

### §6.1 Owner-enumerated deliverables (canonical band actual)

Per Owner atomic-commit spec verbatim: *"Band actual (raw LoC via wc -l across engine + CLI + supplement + tests + six artifacts) vs ratified [650, 1,400]"*.

| Artifact | LoC |
|---|---:|
| Query engine (`queries.py`) | 645 |
| CLI (`run_queries.py`) | 57 |
| v0.2 Supplement | 51 |
| Test cells | 322 |
| Q1 archaeological | 28 |
| Q1 mechanical | 25 |
| Q2 archaeological | 25 |
| Q2 mechanical | 23 |
| Q3 archaeological | 26 |
| Q3 mechanical | 34 |
| **Total** | **1,236** |

**Verdict (§9 band-relative trichotomy):** **WITHIN band** `[650, 1,400]` by 164 LoC below ceiling · `snapshot_raw_in_band=yes`.

### §6.2 §3.6 governance-doc carve-out

NOT applied case-by-case per RP-E5 α (2026-07-11). Band applies as-stated.

---

## §7. §12 close-ratification-on-own-text attest

Per governance §12 (Owner 2026-07-10 verbatim: *"A close whose named gates are green and whose rulings are attested as applied ratifies on its own text."*):

- **(a) Named gates green:** **YES** — SQ-G1..SQ-G-DataBlind all GREEN (§3). 15 new pytest cells + 14 MRR pre-existing + 1,202 prior all GREEN.
- **(b) SQ-E1 γ + cross-reference condition + baseline failure mode attested as applied:**
  - SQ-E1 γ applied: two files per query (arch + mech) · dual-surface archival split byte-visible · §4.1.
  - Cross-reference condition applied: SQ-G-CrossRef GREEN · overlaps annotated in all 6 files · new-candidates sections zero-phantom · PERMANENT rule enforced by test cell.
  - Baseline failure mode applied: fail-loud + HALT posture · §4.3.
  - Band `[650, 1,400]` ratified: band actual 1,236 WITHIN · §6.
  - Governance §14 applied: v0.2 supplement additive · v0.1 + v0.md byte-identical · MRR-G3 round-trip extends to `(v0.md + v0.1 + v0.2)` ↔ registry.yaml · §2.
- **(c) No new Tier-1 escalation surfaced during execution:** **YES** — mechanical candidates surfaced (1 Q1 · 7 Q3 · 2 overlaps annotated) are DELIVERABLES per SQ-E1 γ (findings-as-report), NOT Tier-1s. Q1 new candidate + 7 Q3 new candidates await future Owner-dispatched Registry-maintenance turn (D7 respected · no auto-action).

**Close ratifies on its own text per §12.**

---

## §8. D-10 self-audit (rides close · Registry Doctrine v1.0 verbatim)

Per doctrine D-10: *"every proposal self-audits against defect classes D1–D7 before submission."*

| Class | Verdict | Reason |
|---|---|---|
| **D1 · Orphan gate** | **PASS** | All 10 SQ-G# rows in v0.2_supplement carry promise (reused from v0.md §2) + service_trace + surface + enforcement. Zero orphans. |
| **D2 · NL-only enforcement** | **PASS** | All 10 gates mechanical (pytest cells · AST negative-scan · fs-count + hash-diff · byte-identity lock · grep-negative regex). |
| **D3 · Curated verdict** | **PASS** | Rulings applied verbatim (Owner verbatim carrier at `705dc3df…`). Mechanical + archaeological outputs both surface without curation. Cross-reference is mechanical subject-match. Owner's "provenance-paired facts applied reflexively" framing pinned in ruling record §2. |
| **D4 · Rung inflation** | **PASS** | All 10 SQ-G# rows `1 · Deterministic`. Zero LLM invocation added this phase. SQ-G-Rung1 AST-negative-scans queries.py for LLM imports; GREEN. |
| **D5 · Meta-spiral** | **PASS** | Queries are Registry consumers, not a new governance layer. Findings are inputs to rulings, not actions. Registry remains primary artifact per doctrine §3.6. Provenance-paired-facts framing applies doctrine to itself reflexively (per Owner) — not a new layer, doctrine-consistent. |
| **D6 · Service conflation** | **PASS** | `governor: Named surfaces (Registry infrastructure · reflexive)` on all 10 SQ-G rows. Zero persona optimization. |
| **D7 · Invented schedule or scope** | **PASS** | Only the Owner-dispatched workstreams executed: Q1/Q2/Q3 engine + 6 findings artifacts + 10 gates + v0.2 supplement + close. Explicit out-of-scope §9 verbatim from Owner. Zero refs to sequencing harness · worker context-harnessing · Registry content changes to v0.md · v0.1_supplement · consolidation_log · Q2-05 reads · Playbook/Thesis · next-cell scaffolds. Zero candidate promises minted (all 10 SQ-G rows reuse v0.md §2 promises). Machine form regenerated (derived · not source-of-truth write) with v0.2 in path per §14. |

**Self-audit verdict:** all 7 defect classes **PASS**.

---

## §9. Out-of-scope statement (D7 · Owner-verbatim)

**Verbatim from Owner dispatch:**
> "D7 binds: no sequencing harness code, no worker context-harnessing, no Registry content changes, no Q2-05 reads, no Playbook/Thesis references, no next-cell scaffolds beyond queries scope."

**Explicitly out of scope:** sequencing harness (§8.1.b · next candidate) · worker context-harnessing (§8.1.c) · Registry content changes (v0.md · v0.1 · consolidation_log byte-identical) · Q2-05 individual reads (maintenance-turn business) · Instance Replication Playbook · Commercial Thesis (Owner-parallel).

---

## §10. Test triad

- **Pytest:** **1,231 passed + 1 skipped** (was 1,216 + 1 · +15 new SQ gate cells · zero regression). All new cells GREEN.
- **Jest / Playwright:** NOT re-run (backend-only change per Owner). Prior state held: Jest 151/151 · Playwright chromium 55/55.
- **Parity 31/31 byte-identical** (envelope untouched).
- **Lint:** ruff/pyflakes clean on all new Python files.

---

## §11. Tier-3 defaults (one-line each · disclosed at close)

| Default | Landed |
|---|---|
| Engine module | `backend/services/registry/queries.py` |
| CLI | `tools/registry/run_queries.py` |
| Artifact directory | `docs/registry/queries/` |
| Supplement file | `v0.2_supplement.md` (additive per §14) |
| Artifact metadata | `run_timestamp` + `source_shas` block + REPORT-LEVEL disclaimer line 3 + cross-reference `overlaps: <finding_id>` inline |
| Test file naming | `test_standing_queries_sq_g1_to_g10.py` |

---

## §12. Standing constraints preserved

- **D7 respected:** no code beyond ruled scope · no CI · v0.md + v0.1 + consolidation_log byte-identical · no Q2-05 reads · no Playbook/Thesis · no next-cell scaffolds beyond queries.
- **MANDATE-COMPLETE 2026-07-10 held.** Registry Doctrine v1.0 + §14 in force. Parity 31/31.
- **Standing Rule v3:** on-disk canonical · SHAs above · zero inline code dumps.
- **Governance §12/§12.1/§12.2/§13/§14** in force.
- **Cross-reference discipline is PERMANENT** (Owner-explicit) — attested by SQ-G-CrossRef test cell on every run.
- **Governance §14 extended** to N supplements: `(v0.md + v0.1_supplement + v0.2_supplement)` ↔ `registry.yaml` as one set. MRR-G3 GREEN.

---

## §13. Registry Doctrine additive surface progress

**3 / 8 items landed:**
1. Registry Population §3.5 · self-ratified §12 · 2026-07-11.
2. Machine-Readable Registry §8.1.d · self-ratified §12 · 2026-07-11.
3. **Standing Queries as CI §8.1.a · self-ratified §12 · 2026-07-11** (this phase).

**Next candidate in sequence (orchestrator-dispatched):** §8.1.b Sequencing harness (logical dependency: needs the queries just landed).

═══════════════════════════════════════════════════════════════════

*End of Standing Queries as CI close report. All 4 Owner rulings applied verbatim (SQ-E1 γ + cross-reference condition PERMANENT + baseline failure mode fail-loud + band `[650, 1,400]` ratified). Governance §14 extended to N supplements. Source-of-truth artifacts byte-identical throughout. 10 gates GREEN. Parity 31/31. Pytest 1,231+1 skipped. D-10 all-PASS. §12 auto-ratifies on own text. Standing Rule v3 · on-disk canonical.*
