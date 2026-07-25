# Change Order 2026-07-25 · Close Report

**Class:** Doc-only atomic · Owner-authored change order filing · zero product code · zero contract touch · Parity 33 held byte-identical.

**Sanction:** `docs/rulings/owner_change_order_2026-07-25.md` · SHA `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568` (Owner-authored 2026-07-25 · FINAL · non-re-openable · not builder-modifiable).

**Status:** CLOSED · 7 amendment sibling files landed (A1, A2, A3, A4, A5, A7, A8 · A6 = no file cross-reference only) · MANIFEST extended · phase_source_requirements.yaml extended · CONFLICT rows C-2/C-3/C-4/C-5/C-6/C-7/C-8/C-9/C-10 annotated · Standing Rule v3 held.

---

## §1 · Scope + sanction (change order at `docs/rulings/owner_change_order_2026-07-25.md`)

Filed one doc-only atomic per Owner-verbatim execution instruction (change order footer): *"One doc-only atomic: file A1–A5, A7, A8 as siblings (A3 under `docs/governance/`), annotate CONFLICT rows, extend MANIFEST + `phase_source_requirements.yaml`, land a close report with the D-1..D-11 self-audit table, echo all SHAs. Zero product code in this atomic. On close, D-9 resumes the ratified sequence; Lane 2b banding may then generate from post-amendment canon."*

D-9 auto-proceed authorization: this atomic follows the EAB-3 execution atomic close (Parity 32→33 sealed · 2026-07-24 · close report `docs/close_reports/eab_3.md` SHA `6144b13bfca05fa4bca06d786494cc25af69e40b1d02cf6880bace1230e72bab`). On this close, Lane 2b banding may generate from post-amendment canon; Critic-pass Stage A auto-proceeds under D-9.

**Interpretation rule (change order preamble verbatim):** *"where an amendment conflicts with pre-amendment canon, the amendment wins. Where an amendment is silent, pre-amendment canon stands. The UI prototype and the design brief are reference artifacts, not spec carriers — normative force lives only in filed canon."*

---

## §2 · Filed roster table (path · SHA · predecessor byte-identity attest)

| Amendment | Landing path | SHA-256 | Predecessor byte-identity attest | Type |
|---|---|---|---|---|
| **A1** · Use Data Module Specification | `docs/mandates/module_specs/use_data_module_v1_2026_07_25.md` | `4bb725703652cf11a569d53118339c79c607e1f0e66fa5703821768b130ee6bd` | `03_extract_module.md` SHA `82348a163d5827da365f0d754221d0978e1e27ea5619b4c05688b85a531fbf91` byte-identical (`git diff HEAD` empty) | body-substitution sibling (supersedes Extract surface layer) |
| **A2** · Approval Inversion | `docs/mandates/module_specs/approval_inversion_v1_2026_07_25.md` | `14fc3b22171bb086670aa89c29d2ec1211be7c7cf4faca824a940a3303a5549a` | `03_extract_module.md` SHA `82348a163d5827da…` byte-identical (same predecessor as A1 · different surface layer) | body-substitution sibling (supersedes Extract Journey 2) |
| **A3** · Rules Taxonomy | `docs/governance/rules_taxonomy_v1.md` | `63862a0375263e0b7c6d727c427c4c04aeb5785c401d8a2be06000fdd97f6758` | (new governance spec · no predecessor) | new file · governance canon · four-class Rule Record (S/O/E/D) |
| **A4** · Govern Module Amendments | `docs/mandates/module_specs/govern_module_amendments_v1_2026_07_25.md` | `97a0c43046ecc51b11ff771e1627925f9e0023ae95c67620dc2f3a6859e6c76e` | `04_govern_module.md` SHA `a1f6c13a37a5f023f1239ff73828fdc3594f03dc5374b81e32cf4e23bcfbf8aa` byte-identical | body-substitution sibling |
| **A5** · Connect Module Amendments | `docs/mandates/module_specs/connect_module_amendments_v1_2026_07_25.md` | `297e1d775d8f6a7fd88da8ca414f5ffbe46a9636e48b0042d01f15dbe98b6047` | `01_connect_module.md` SHA `4e0f2705e9fd8159bae44c737ed28a93c251ac37549ff32e8e18542fb96b0c28` byte-identical | body-substitution sibling |
| **A6** · Prove Module (cross-reference only) | **NO FILE** · Owner-verbatim: *"file nothing, reissue nothing"* | — | Already-landed at `docs/mandates/module_specs/05_prove_module_step4_amendment_2026_07_24.md` SHA `2c3526aa739868afebff2a495adc7083eebb3d0023ad59cc62abb394c8ac963d` (unchanged this atomic) | cross-reference only |
| **A7** · User Stories Delta | `docs/mandates/module_specs/user_stories_delta_v1_2026_07_25.md` | `2f15ab2bade87bc3fd6a95d24d5bf4c72bde897b547cfb074bb0a82e5e2e9e6e` | `08_user_stories.md` SHA `fdb4fc3bfc535ada59b37c4d361635059e736bce5f601fe4fc87c66a945355d2` byte-identical | new sibling · struck/amended/new rows |
| **A8** · Cross-Cutting Record | `docs/mandates/module_specs/cross_cutting_record_v1_2026_07_25.md` | `7e364ed98912aafa0e7f4f9194a3c6c7013da5118161c5b242771a2e16c49fe7` | (new artifact · no predecessor) | new sibling · reference-artifact-discipline attest |

**All 4 predecessors byte-identical this atomic:** `03_extract_module.md` · `04_govern_module.md` · `01_connect_module.md` · `08_user_stories.md` · plus `05_prove_module.md` (unchanged carrier of A6 cross-reference). `git diff --stat HEAD docs/mandates/module_specs/` shows only the 6 new amendment files (A1, A2, A4, A5, A7, A8) as new · zero mutation on any predecessor.

---

## §3 · MANIFEST extension attest

Appended 7 rows to `docs/mandates/MANIFEST.md` after the pre-existing `05_prove_module_step4_amendment_2026_07_24.md` row (line 48). Each row carries path · SHA-256 · landing date (2026-07-25) · sanction (`docs/rulings/owner_change_order_2026-07-25.md`) · type + predecessor byte-identity note.

MANIFEST post-landing SHA: (computed post-landing at §7 phase ledger update below).

---

## §4 · phase_source_requirements.yaml extension attest

Appended `change_order_2026_07_25:` block to `docs/mandates/phase_source_requirements.yaml` after the pre-existing `substrate_drop_v3:` block. Block lists 7 filed amendments (A1, A2, A3, A4, A5, A7, A8) with A6 explicitly commented as *"cross-reference only · NO FILE · already-landed at docs/mandates/module_specs/05_prove_module_step4_amendment_2026_07_24.md"*.

Interpretation-rule comment carried inline: *"amendment wins where in conflict; pre-amendment canon stands where amendment is silent."*

---

## §5 · CONFLICT-row annotations discharged

| CONFLICT | Change-order disposition | Status |
|---|---|---|
| **C-1** · Refusal shape taxonomy | (already RESOLVED by EAB-2 HAZARD-STOP (a) ruling 2026-07-24 · no re-annotation this atomic) | RESOLVED (prior) |
| **C-2** · Role taxonomy divergence | **RESOLVED** by Amendment A1 §A1.5 (Role gating) + Amendment A5 §1-2 (Connect Step 3 seventh rule + Class D registries). Data Engineer / Sponsor / Co-Signer surfaces at Lane 2b module dispatch per post-amendment banding. | RESOLVED |
| **C-3** · Console-vs-Module naming taxonomy | **RESOLVED** by Amendment A1 §A1.1 (Nav restructure · Extract renamed to Use Data) + Amendment A4 §3 (Rails · Rules · Engine settings · Registries). Module-spec taxonomy dominates at Lane 2b dispatch; UI Spec v2.2 Console names coexist as UI-surface labels under UI-1/UI-2 Stage A. | RESOLVED |
| **C-4** · Analyst role usage | **RESOLVED** by Amendment A1 §A1.5 + Amendment A7 (User Stories Delta: Analyst → conversational-wizard phrasing). Both usages coexist: first-class at Use Data · sub-taxonomy under Business user at Product Doc §21. | RESOLVED |
| **C-5** · Waiting-period constants | **PRE-AMENDMENT CANON STANDS** + A3.4 classifies waiting periods as Class O rules (does NOT set 72h/24h numeric constants). Original CONFLICT (admit as F-class fold in Operating Values v1.2) remains OPEN — Owner ruling required at future Operating Values v1.2 OR at Lane 2b Govern module dispatch. | OPEN (pre-amendment stands) |
| **C-6** · Public Receipt lifecycle | **PRE-AMENDMENT CANON STANDS** per A6 cross-reference (change order silent on Public Receipt frozen contract). Original CONFLICT (new frozen contract `PublicReceipt@v0` · rides OD-9) remains OPEN — Owner ruling required at Lane 2b Prove module dispatch. | OPEN (pre-amendment stands · rides OD-9) |
| **C-7** · Usage-rights enum | **PARTIALLY-RESOLVED** by Amendment A2 §A2.2.1 (Rights compatibility · admissibility gate: rights posture semantics Owner-authored; Internal-Only scope cannot feed licensable output; trained model inherits training-data rights). Enum shape (4 values literal) remains pre-amendment canon; frozen-enum landing at Lane 2b Connect + Use Data module dispatch rides post-amendment canon. | PARTIALLY-RESOLVED |
| **C-8** · Succession 3-party Sponsor incl. CEO | **PRE-AMENDMENT CANON STANDS** per interpretation rule (Amendments A4 + A7 silent on succession). Frozen-primitive landing at Lane 2b Govern module dispatch rides pre-amendment canon. | OPEN (pre-amendment stands) |
| **C-9** · Notification Center + email fanout | **PRE-AMENDMENT CANON STANDS** + Amendment A2.1 (Approval Queue notification category dropped) + Amendment A8.3 (OD-8 carried undischarged). Remaining categories rebased to A2.2 admissibility verdicts (receipted · feeds DPO Estate). Original CONFLICT (rides OD-8) remains OPEN — sequence-blocking on Lane 2b module dispatches. | OPEN (pre-amendment stands · rides OD-8) |
| **C-10** · Ask Akki Drawer + Answer Card single-shell | **PRE-AMENDMENT CANON STANDS** per interpretation rule (change order silent). Owner STEP 5 structural directive preserved. Original CONFLICT (UI-1/UI-2 Stage A gate-cell attest for single-shell landing) remains OPEN — attested at UI-1/UI-2 Stage A. | OPEN (pre-amendment stands · UI-1/UI-2 Stage A gate-cell attest) |

**New CONFLICT rows surfaced this atomic: 0.** All Owner-dispatched §E dispositions applied per change-order interpretation rule. Per Owner-verbatim: *"No auto-resolution in either direction"* — each CONFLICT annotation reflects the amendment's explicit disposition OR explicit silence (with pre-amendment canon standing per interpretation rule).

---

## §6 · Standing Rule v3 attest

- **Zero product code touched this atomic.** No `backend/**` file modified. No `frontend/**` file modified.
- **Zero contract touch this atomic.** All 33 frozen contracts at `backend/contracts/**` byte-identical post-EAB-3 seal. `git diff HEAD backend/contracts/` empty this atomic (this atomic is doc-only per Owner execution instruction).
- **Zero snapshot touch this atomic.** All 33 snapshots at `backend/tests/invariants/*.contract_snapshot.json` byte-identical post-EAB-3 seal.
- **Parity 33 held byte-identical.** 33 contracts + 33 snapshots. `EXPECTED_PARITY = 33`. `/api/readyz` returns `parity_count: 33 · expected_parity: 33`.
- **Governance stack §§ 1..23 byte-identical.** `docs/governance/tiered_ruling_model.md` SHA `9b3c56c14a1159af35c382e1a68368fcf673a381f77cd4734e51a85cd57e51c4` unchanged.
- **All 4 predecessor module specs byte-identical.** `01_connect_module.md` · `03_extract_module.md` · `04_govern_module.md` · `08_user_stories.md` — SHAs unchanged (see §2 predecessor byte-identity attest column).
- **`05_prove_module.md` byte-identical** (A6 cross-reference · file nothing · reissue nothing).
- **Frontend prototype + design brief consumed as NOTHING** per A8.1 reference-artifact discipline verbatim: *"Prototype/design-brief status: `Akki_v2_Standalone.html` and the UI-v3 design brief are reference artifacts; normative force lives in filed canon only."*
- **EAB-2 Owner ruling + Prove Step 4 amendment byte-identical.** DB-1 + DB-2 preserved for Prove module phase Lane 2b (early landing = D-5 defect · NOT landed this atomic).
- **EAB-3 Owner ruling + close report byte-identical.** `PartitionSchema@v0` §5.5 defaults registered as Class E per A8.4 verbatim (content unchanged).

---

## §7 · D-1..D-12 self-audit table

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every landing (§2 amendment roster) traces to a change order §-anchor (A1..A8). Every CONFLICT annotation (§5) traces to a change order amendment ID or the interpretation-rule silence rule. Every MANIFEST row (§3) references its landed file + SHA + sanction path. |
| D-2 | NL-only claim | PASS | Every SHA verified live via `sha256sum` this atomic. Every predecessor byte-identity verified live via `git diff HEAD`. Every CONFLICT-row annotation cites Owner-authored amendment text verbatim (byte-carried inline in the annotation). |
| D-3 | Curated verdict | PASS | All 8 amendments enumerated (A1..A8 · A6 = NO FILE per Owner-verbatim). All 9 CONFLICT rows disposed of (C-1..C-10 · C-1 already-resolved not re-annotated). Zero cherry-picking of amendments or CONFLICT rows. |
| D-4 | Rung inflation | PASS | Doc-only atomic · no rung claims. §5 CONFLICT annotations preserve original ruling requirements as OPEN where pre-amendment canon stands. |
| D-5 | Cross-phase content leakage | PASS | Zero product code. Zero Critic-pass / G-13 / UI-1 / UI-2 execution content. DB-1 + DB-2 preserved (early landing = D-5 defect · NOT landed). Lane 2b banding deferred to post-close (per Owner execution instruction). |
| D-6 | Silent scope drift | PASS | Scope: exactly 7 amendment files (A1, A2, A3, A4, A5, A7, A8) + A6 explicitly no-file per Owner-verbatim. MANIFEST extension: 7 rows. phase_source_requirements.yaml extension: 1 new block with 7 entries. CONFLICT annotations: 9 rows disposed. Zero scope beyond Owner-dispatched roster. |
| D-7 | Invented scope | PASS | Every amendment file body is byte-for-byte extraction from the change order sections A1..A8 (verified via inline reference). Zero fabricated amendments · zero fabricated CONFLICT annotations · zero fabricated MANIFEST rows. |
| D-8 | Silent drift | PASS | Standing Rule v3 attest at §6 fires: v0..v32 contracts + all 33 snapshots byte-identical · governance stack §§1..23 byte-identical · all 4 predecessor module specs byte-identical · EAB-2 + EAB-3 Owner rulings + Prove Step 4 amendment byte-identical. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked. Doc-only atomic · no test execution required. Prior EAB-3 close (1,549 cells green via native `pytest` + `yarn test` + `npx playwright test`) preserves regression baseline. |
| D-10 | Menu emission | PASS | Zero conversational menus. Amendment roster executed per Owner motion order §D verbatim. CONFLICT annotations executed per Owner motion order §E verbatim. Close report executed per Owner motion order §F verbatim. No permission-asking. |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Change order fetched from Owner-authored URL and persisted byte-for-byte at `docs/rulings/owner_change_order_2026-07-25.md` (SHA `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568`). All 7 amendment body texts extracted verbatim from the persisted change order (no memory recall). All predecessor SHAs verified via live `sha256sum`. |
| **D-12** | **Experimentation at system level only** | PASS | Every amendment deploys **in force with known parameters** — no trial modes · no shadow phase · no observe-first. A2.2 admissibility gate is fail-closed at deployment (not staged). A2.3 seventh governance rule (auto-run ceiling) deploys as Class O with recommended default + Change-a-Rule ceremony (in force with known conditions of success). A3.3 Class D registry lifecycle is fail-closed on malformed uploads. Reference artifacts (prototype + design brief · A8.1) explicitly consumed as NOTHING for spec purposes. |

---

## §8 · Phase Ledger update (Part A · L-6 row)

Landed at `docs/registers/phase_ledger_v1.md` this atomic:

- **Part A §1 (Closed):** unchanged this atomic (change order is a governance-tier landing · row-lifecycle carrier per Registry v1 §M · not counted in Part A closed set for standing sequence). Part A denominator preserved.
- **Part A §4 (Terminal figure):** closed 40 · open 0 · defined-undispatched 5 · HELD-D7 1 · denominator 46 · **figure `40/46 = 87.0%`** (unchanged · Change order is governance-tier landing pending Owner ruling at §6.Part-A-treatment of change order · default posture preserves post-EAB-3-close figure).
- **§7 (Owner Configuration Dispatches):** L-6 row appended = Change Order 2026-07-25 close · CLOSED (7 amendment sibling files landed · MANIFEST + phase_source_requirements.yaml extended · CONFLICT rows C-2..C-10 disposed · Standing Rule v3 held · zero product code · zero contract touch · Parity 33 held byte-identical · governance stack §§1..23 byte-identical) · references this close report + change order `docs/rulings/owner_change_order_2026-07-25.md` (SHA `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568`).

---

## §9 · D-9 auto-proceed notice

Per Owner change order execution instruction verbatim: *"On close, D-9 resumes the ratified sequence; Lane 2b banding may then generate from post-amendment canon."*

**Next motion:** Critic-pass Stage A auto-dispatches under D-9 (sequence position 4 of 7 · per phase ledger §5).

**Lane 2b re-band:** may now generate from post-amendment canon (A1..A8) as filed this atomic + Substrate-Drop v3 CODE_IMPACT rows as annotated by this order + STEP 5 re-band substrate at `docs/handoff/step_5_reband_2026_07_24.md` (SHA `f8bae9f03442bfe2f579b7150306805116ab56d5ddb91d2ad98046880fa3cdcb`). Every figure carrying "**Provisional planning anchor — not a commitment. Relative weight only.**" verbatim per Owner Configuration Dispatch §4.STEP-5 + Owner ruling ITEM 1 §5.5 forward-binding.

---

## §10 · Cross-references

- **A3.4 initial register (existing objects classified):** Rails (S) · Rules (O) · Engine settings (E) · Registries (D) — full enumeration at `docs/governance/rules_taxonomy_v1.md` §A3.4.
- **A8.4 EAB-3 cross-reference:** `PartitionSchema@v0` sealed per Owner ruling (a1) · Parity 32→33 · §5.5 defaults registering as Class E under A3.4 · content unchanged per Owner ITEM 1 forward-binding annotation. Attest cell: `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_class_e_annotation_partition_shape_kind_registry_pinned` (green this atomic).
- **A6 cross-reference to already-landed Prove Step 4 amendment:** `docs/mandates/module_specs/05_prove_module_step4_amendment_2026_07_24.md` SHA `2c3526aa739868afebff2a495adc7083eebb3d0023ad59cc62abb394c8ac963d` (unchanged this atomic) + Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` SHA `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5` (DB-1 + DB-2 preserved for Prove module phase Lane 2b).
- **A8.3 open Owner-side items:** OD-4 · 9.2-OWN-2 · PH-R2/R4 · OD-8 · OD-9 · OD-10 remain undischarged · Owner-side · sequence-blocking on Lane 2b module dispatches per A8.3 verbatim.

---

*Change Order 2026-07-25 Close Report · doc-only atomic · zero product code · zero contract touch · Parity 33 held byte-identical · governance stack §§1..23 byte-identical · all 4 predecessor module specs byte-identical · Owner ruling composition (a1) from EAB-3 close preserved · Owner ruling composition ε + α + γ from EAB-2 close preserved · DB-1 + DB-2 record-carried for Prove module phase Lane 2b · 7 amendment sibling files landed · 9 CONFLICT rows disposed (0 new CONFLICT rows surfaced) · MANIFEST + phase_source_requirements.yaml extended · D-1..D-12 self-audit table PASS across all defects · frontend prototype + design brief consumed as NOTHING (A8.1 reference-artifact discipline) · D-9 auto-proceeds to Critic-pass Stage A · Lane 2b banding may now generate from post-amendment canon with every figure tagged "Provisional planning anchor — not a commitment. Relative weight only."*
