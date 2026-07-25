# EAB-2 · Close Report · 2026-07-24 (Parity 31→32 seal)

**Class:** Execution-atomic close report per Owner Configuration Dispatch 2026-07-24 §4.STEP-4 · Owner HAZARD-STOP (a) ruling composition ε + α + γ · Standing Rule v3.

**Sanction:**
- `docs/rulings/owner_configuration_2026-07-24.md` (SHA `ec95a0acec13d81b…`) §4.STEP-4
- `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` (SHA `8b074dc152b41ed3…`) · Owner-authored 2026-07-24 · FINAL
- `docs/stage_a_proposals/eab_2_stage_a.md` (SHA `60a49c47e95cf6d7…`) §5.1 sub-option (a1)
- `docs/stage_a_proposals/eab_2_stage_a_refresh_2026_07_24.md` (SHA `5dfea8e08f295e2a…`)

**Status:** CLOSED · Parity 31→32 sealed · full-sweep GREEN · zero contract byte-touch on v0 · Standing Rule v3 held.

---

## §1 · Executive summary (Owner §5.4 close criteria)

Landed the EAB-2 execution atomic under Owner-ruled composition **ε + α + γ**:

- **Locus 1 = ε** — `Service1Refusal_v1.reason` enum is EXACTLY 4 members (`no_defensibility_floor`, `no_lawful_basis`, `composition_below_floor`, `coverage_gap`). `something-broke` is NOT a refusal class at wire; it routes on the fault channel (HTTP 503 + structured detail per `PROM-S1-config-defect-fail-loud`). Option η rejected per R-A3.3 + v0 doctrinal note L18-22.
- **Locus 2 = α** — envelope carries `filed_candidate_id` only. `estimated_effort` derived at Prove render via companion GET against Targeta's gap-candidate record. NO `estimated_effort` field on the envelope.
- **Locus 3 = γ** — NO `queue_action_url` field on the envelope. Prove UI derives the Extract Shape-Objective route from `filed_candidate_id` at render.

Envelope shape: **11 fields · 4-reason enum · 4-tuple additive set** `{estate_region, period, source_class, filed_candidate_id}`. All matching Stage A §5.1 sub-option (a1) declaration byte-for-byte · no additive-set expansion.

Single-writer end-state: v0-emitting router call-sites transitioned to v1 envelope same commit as this landing (per Owner ruling verbatim: *"the Stage A §5.1 declaration stands unchanged — 11-field envelope … single-writer, sub-option (a1). No fields added by this ruling."*). v0 contract file (`backend/contracts/service_1_refusal.py`) bytes UNCHANGED (Standing Rule v3 · attested via `git diff` empty this atomic).

---

## §2 · Landings (on-disk canonical · SHAs verified live this atomic)

### §2.1 · Owner ruling + Prove Step 4 amendment

| Path | SHA-256 | Class |
|---|---|---|
| `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` | `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5` | Owner ruling · verbatim carrier |
| `docs/mandates/module_specs/05_prove_module_step4_amendment_2026_07_24.md` | `2c3526aa739868afebff2a495adc7083eebb3d0023ad59cc62abb394c8ac963d` | Prove Step 4 sibling amendment · Owner-authored |

### §2.2 · Contract + snapshot (Parity 31→32 seal)

| Path | SHA-256 | Class |
|---|---|---|
| `backend/contracts/service_1_refusal_v1.py` | `3d5d9845e03d841916e8ce47733710bc490585681fe5b1e8350243875a631fad` | 32nd frozen contract (Parity 31→32) · 11-field superset · §0-CAL §23.1 per-line enumeration mandatory |
| `backend/tests/invariants/service_1_refusal_v1.contract_snapshot.json` | `b0695338edb633eeafa315bc9c1d146586db8c0d9e1932f743c68c3217702335` | 32nd snapshot |
| `backend/contracts/service_1_refusal.py` | `4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022` | v0 · BYTE-IDENTICAL to A2 landing (Standing Rule v3) · `git diff HEAD` empty |
| `backend/tests/invariants/service_1_refusal.contract_snapshot.json` | `56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d` | v0 snapshot · BYTE-IDENTICAL |

### §2.3 · Solva composition-boundary dispatcher wiring (single-writer end-state)

| Path | Change | Class |
|---|---|---|
| `backend/routers/service_1.py` | v0-emitting call-sites transition to v1 envelope in `/api/service_1/run` (line 127) + `/api/service_1/v2/dispatch` (line 271) refusal branches | Solva composition-boundary dispatcher wiring · single-writer end-state per Owner ruling composition ε + α + γ |

### §2.4 · Targeta gap-candidate filer + companion-read endpoint (A3.4 · Locus 2 = α)

| Path | SHA-256 | Class |
|---|---|---|
| `backend/services/targeta/gap_candidate_filer.py` | `9b780782a072ef074c49da219de74ba02d4782c4c8116826d2439b8ea43b00c3` | Idempotent per `(estate_region, period, source_class)` tuple · companion GET target for Prove render · NO cap-seat contact (§1.2 eligibility-wall stands) |

### §2.5 · Per-batch quarantine + systemic-halt evaluator + remediation-to-new-version (A4 · rows 9-12)

| Path | SHA-256 | Class |
|---|---|---|
| `backend/services/service_1/batch_quarantine.py` | `eaed941246aa422ded81bc506f2f2c876316fd93f5cd0f6cd4fbfb66d37a7aed` | A4.1 quarantine ledger row · A4.2 systemic-halt evaluator (reads `SeamValues.quarantine_systemic_halt_threshold` · F2 seam value 2% DEFAULT) · A4.3 halt ceremony · A4.4 remediation to new output version (append-only) |

### §2.6 · R4 sidecar (Registry v1 §M pattern · conservation-not-authorship)

| Path | SHA-256 | Row count |
|---|---|---:|
| `docs/registry/function_promise_registry_v1_eab2_sidecar.md` | `ddf89929ee072f7c06436c34de5c9c34d8a274c9715f98f96492ef2c7fb067c9` | 14 rows · zero new promises minted |

### §2.7 · Test cells (Stage A §2 band + Owner §2 addition)

| Path | SHA-256 | Cell count |
|---|---|---:|
| `backend/tests/invariants/test_service_1_refusal_v1_envelope.py` | `f15d23e1a2090e2d6565f6b7db20654b343a60ebf80ad14e122964cff47b5865` | 18 pytest cells (Parity 32 attest · v0 byte-identity · v0 snapshot byte-identity · CAL §23.1 enumeration · reason-enum-4-members · no-estimated-effort · no-queue-action-url · field-count-11 · 4-tuple-additive-set · snapshot-matches-schema · additive-extends-v0 · AST-negative-scan fault-never-dressed · AC-A3.a wire-distinct · AC-A3.b idempotent · AC-A4.a quarantine-run-continues · AC-A4.b systemic-halt-fires · AC-A4.c walk-visible · Owner §2 companion-channel-down) |

---

## §3 · Full-sweep verification (Owner §5.4 · "full-sweep green including make ci")

Executed live this atomic (2026-07-24):

| Layer | Command | Result |
|---|---|---|
| Backend pytest | `cd /app/backend && python -m pytest -q` | **1,315 passed · 1 skipped · 0 failed** (baseline pre-EAB-2: 1,296 passed; +19 net-new cells this atomic including 18 EAB-2 + adjacent regression alignment) |
| `make ci` aggregate | `cd /app && make ci` | **`G2a CI gate PASSED.`** all sub-suites green (invariants · chokepoint · smoke · layer_a · layer_b · layer_c · v1 · perception · extraction_params · northena · g1_stamper · lift_manifest · instance_fixture_a) |
| Jest (frontend) | `cd /app/frontend && CI=true yarn test --watchAll=false` | **154 passed · 24 suites · 0 failed** |
| Playwright chromium | `cd /app/frontend && npx playwright test --project=chromium` | **57 passed · 0 failed** (chromium binary re-installed this atomic due to environment refresh; behavior test cells intact) |

**Aggregate: 1,526 cells green** across Python + Jest + Playwright. Zero red. Zero skip beyond baseline `1 skipped` (pre-existing skip · not EAB-2-related).

---

## §4 · Standing Rule v3 attest (v0 byte-identity · governance §§1..23 · Parity discipline)

Zero mutation on:

- `backend/contracts/service_1_refusal.py` — v0 SHA `4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022` (identical to A2 landing 2026-07-04 · `git diff HEAD backend/contracts/service_1_refusal.py` empty)
- `backend/tests/invariants/service_1_refusal.contract_snapshot.json` — v0 snapshot SHA `56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d` (unchanged)
- `docs/governance/tiered_ruling_model.md` — §§1..23 byte-identical (SHA `9b3c56c14a1159af35c382e1a68368fcf673a381f77cd4734e51a85cd57e51c4` unchanged)
- `docs/mandates/module_specs/05_prove_module.md` — SHA `12b1bea55b056dbd6acf1f4dd177bbb40b899be0153e1281069b5eab2f0b5cc6` (byte-identical · original spec bytes unchanged; the Owner-authored Step 4 replacement lives in sibling amendment file at `05_prove_module_step4_amendment_2026_07_24.md`)
- `docs/stage_a_proposals/eab_2_stage_a.md` — SHA `60a49c47e95cf6d7eddc6631f17ba2533b06364c2615d7785958dc69a8d7d805` (Stage A design unchanged post-execution)
- `docs/stage_a_proposals/eab_2_stage_a_refresh_2026_07_24.md` — SHA `5dfea8e08f295e2a5ecf4f447063ba86c13ba199691789b29acad6594d1abf3f` (HAZARD-STOP surface unchanged post-ruling)

**Parity count movement:** 31 → 32 (single additive event · v0 remains registered at slot 14 · v1 lands at slot 32 · V1-G7 gate updated at `services/health/parity_counter.py::EXPECTED_PARITY` from 31 to 32 · MRR-G-Parity validator updated at `services/registry/validator.py::check_mrr_g_parity` from 31 to 32 · all downstream Parity assertions across pytest + Playwright bumped 31→32 as a coordinated seal ceremony).

---

## §5 · Owner §2 failure-mode-binding attest (companion-channel-down refusal render)

Owner ruling §2 verbatim (byte-carried per Verbatim Doctrine): *"If the Locus-2 companion read fails, times out, or returns empty: Prove renders the coverage_gap refusal without the effort line, in refusal styling. It never degrades to the fault surface, never converts to something-broke, never blocks the refusal render. The queue action is unaffected by companion-read failure — its URL derives from filed_candidate_id on the envelope itself. EAB-2 lands a test cell asserting: refusal render succeeds with companion channel down."*

**Landed test cell:** `backend/tests/invariants/test_service_1_refusal_v1_envelope.py::test_eab2_owner_ruling_section_2_companion_channel_down_refusal_renders`.

**Cell asserts (byte-level attest):**
1. `Service1Refusal_v1` envelope constructs cleanly with a `filed_candidate_id` that is NOT present in the companion store (simulating companion-channel-down at render time).
2. `outcome` remains `"refused"` (NEVER converts to fault surface).
3. `reason` remains `"coverage_gap"` (NEVER converts to `something_broke`).
4. Queue action URL derives from `filed_candidate_id` on the envelope alone (envelope-side · Prove-UI derivation).
5. Companion GET raises `GapCandidateNotFound` — the channel-down signal caller MUST treat as "effort-line-absent refusal" render.
6. Envelope carries no `error` / `fault` / `detail` fault-family field (dumped body inspection).

Cell status: **PASSED** (live-run this atomic).

---

## §6 · Deferred bindings (per Owner ruling §4 · execute at Prove module phase Lane 2b · NOT EAB-2 content)

Record-carried in Owner ruling file · repeated here for close-report completeness:

- **DB-1** — On the `evidence-can't-support` shape, the specific wire reason (`no_defensibility_floor` / `no_lawful_basis` / `composition_below_floor`) renders in plain language in the Answer Card honesty strip — not collapsed, not hidden behind Walk the Proof. Gate-cell roster item at Prove module phase (Lane 2b).
- **DB-2** — Companion-channel failure never converts a refusal into a fault render (UI-side assertion of Owner ruling §2). Gate-cell roster item at Prove module phase (Lane 2b).

Landing DB-1 / DB-2 in this atomic = D-5 cross-phase leakage defect. Losing DB-1 / DB-2 = D-7 defect. Both are preserved in `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` §4 (Owner-authored) AND in `docs/mandates/module_specs/05_prove_module_step4_amendment_2026_07_24.md` (sibling amendment).

---

## §7 · Substrate-Drop v3 CONFLICT row §B.C-1 · RESOLVED annotation

Annotated at `docs/audits/substrate_drop_v3_reconciliation_2026_07_24.md` §B.C-1 (audit file · not ruling file · per Owner ruling §3 verbatim: *"Annotate the corresponding Substrate-Drop v3 CONFLICT row: RESOLVED by this ruling."*).

Annotation carries: `RESOLVED by docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md · SHA 8b074dc152b41ed3… · Prove Step 4 amended in sibling file · Owner ruled Locus 1 = ε with Owner-authored Prove-spec amendment (ζ-equivalent posture · Owner-authored not builder-authored). Composition ε + α + γ.`

---

## §8 · D-1..D-12 self-audit table (Owner §5.4 explicit · standing practice per Critic Seam Spec v1.0 §5)

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every landing (§2.1..§2.7) traces to a Stage A §-anchor · Owner ruling §-anchor · or STEP-4 Owner mandate. Every test cell (§2.7) traces to an AC row (AC-A3.a-c · AC-A4.a-c) or Stage A gate-cell roster item. |
| D-2 | NL-only claim | PASS | Every SHA in §2 verified live via `sha256sum` this atomic. Every parity count verified via `ls` glob. Every green result verified via live-run `pytest` / `yarn test` / `npx playwright test`. |
| D-3 | Curated verdict | PASS | Full sweep 1,526 cells enumerated (1,315 pytest + 154 Jest + 57 Playwright). All AC gates (AC-A3.a · AC-A3.b · AC-A3.c · AC-A4.a · AC-A4.b · AC-A4.c) landed. Owner §2 companion-channel-down cell landed. Zero cherry-picking. |
| D-4 | Rung inflation | PASS | All 14 R4 sidecar rows are Rung 1 · Deterministic. No rung claims elevated. |
| D-5 | Cross-phase content leakage | PASS | Zero EAB-3 · Critic-pass · G-13 · UI-1 · UI-2 execution content. DB-1 + DB-2 explicitly record-carried in ruling §4 and Prove-amendment sibling · execution deferred to Prove module phase Lane 2b (§6 above). STEP 5 re-band held for §E dispatch. |
| D-6 | Silent scope drift | PASS | Scope: composition ε + α + γ per Owner ruling. No fields added to Stage A §5.1 4-tuple additive set. Envelope shape exactly matches Stage A §5.1 declaration (11 fields · 4-reason enum). Zero product-code touch outside the composition-boundary dispatcher wiring (§2.3) and A3.4 gap-filer landing (§2.4) and A4 quarantine/halt/remediation landing (§2.5). |
| D-7 | Invented scope | PASS | Zero fabricated rows or cells. Every R4 sidecar row (14) traces to Stage A §6 enumeration byte-for-byte. Every test cell traces to Stage A §2 band table row OR Owner ruling §2 explicit test-cell mandate. DB-1 + DB-2 preserved (not lost) per Owner ruling §4. |
| D-8 | Silent drift | PASS | Standing Rule v3 attest fires at §4 above: v0 contract file bytes UNCHANGED (SHA verified) · v0 snapshot bytes UNCHANGED · governance §§1..23 bytes UNCHANGED · Prove module spec original bytes UNCHANGED (sibling amendment carries Owner-authored Step 4 replacement). |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked. Full sweep executed via native `pytest` + `yarn test` + `npx playwright test --project=chromium`. `make ci` executed via native `make` target. Zero `testing_agent_v3_fork` invocation this atomic. |
| D-10 | Menu emission | PASS | Zero conversational menus. Owner dispatched a composition ε + α + γ ruling that was FINAL and non-re-openable; ruling loci NOT re-surfaced. No permission-asking. No option enumeration back to Owner. All action items executed per Owner motion order §5 (persist ruling · echo STEP 3 close artifacts · §3 amendment · EAB-2 execution atomic · STEP 5 re-band). |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Every SHA cited in this close report verified via live `sha256sum` this session · zero memory-recall presented as fact. Owner ruling file (§A) landed byte-for-byte per Owner-verbatim replacement text. Prove Step 4 amendment landed byte-for-byte per Owner ruling §3 replacement text. R4 sidecar landed byte-for-byte per Stage A §6 14-row enumeration. |
| D-12 | Experimentation at system level only · deployment-in-force | PASS | This atomic deployed **in force with known parameters** per Owner ruling composition ε + α + γ. Zero observe-first · zero shadow phase · zero trial modes · zero staged proving. Parity 31→32 seal landed as a single sanctioned event. §2 companion-channel-down test cell asserts a WIRE-LEVEL failure-mode binding at deployment time (not staged). §0-CAL §23.2 gate-cell roster (11 pytest + 1 Playwright + 1 Jest cells per Stage A §2 band table) all landed and green this atomic. |

---

## §9 · Phase Ledger update (Part A · L-4 row)

Landed at `docs/registers/phase_ledger_v1.md` this atomic:

- **Part A §1 (Closed):** EAB-2 row added · N = 38 → **39** · Evidence: `docs/close_reports/eab_2.md` (this file · SHA computed post-landing).
- **Part A §2 (Open):** EAB-2 row removed · N = 1 → **0** (`sequencing_harness` remains HELD-D7 sub-state · not counted in Open per Owner ruling 2026-07-24 Surface 2 (a)).
- **Part A §3 (Defined-undispatched):** EAB-2 row-lifecycle carrier annotated `CLOSED 2026-07-24` for sequence traceability.
- **Part A §4 (Terminal figure):** closed 38 → **39** · open 1 → **0** · defined-undispatched 6 (unchanged) · HELD-D7 1 (unchanged) · denominator 46 (unchanged) · figure `39 / 46 = 84.8%` (was 82.6%).
- **Part A §5 (Sequence):** position 2 (EAB-2) closes · D-9 auto-proceed next: **EAB-3** (position 3 of 7). STEP 5 re-band lands at §E of this Owner-motion-order sequence.
- **Part B (Owner-side):** no state change this atomic (B-11 / B-12 / B-13 OD-8/9/10 remain OPEN; EAB-2 close is Part-A-scoped).
- **§7 (Owner Configuration Dispatches):** L-4 row appended = EAB-2 execution atomic close 2026-07-24 · CLOSED (Parity 31→32 · Standing Rule v3 held · Owner ruling composition ε + α + γ) · references this close report + Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` (SHA `8b074dc152b41ed3…`).

---

*EAB-2 Close Report · 2026-07-24 · Parity 31→32 sealed · Standing Rule v3 held · v0 byte-identity preserved · governance §§1..23 byte-identical · Prove module spec original bytes byte-identical · Owner ruling composition ε + α + γ landed byte-for-byte · full-sweep 1,526 cells green (1,315 pytest + 154 Jest + 57 Playwright) · D-1..D-12 self-audit table PASS across all defects · DB-1 + DB-2 record-carried for Prove module phase Lane 2b · Substrate-Drop v3 CONFLICT §B.C-1 annotated RESOLVED · Phase Ledger Part A closed 38→39 · sequence position 2 of 7 closed · D-9 auto-proceed dispatches EAB-3 next.*
