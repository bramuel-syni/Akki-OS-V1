# Outstanding Work & Gap Register · v1.4 · 2026-07-14
**Authority:** Owner-ratified via ruling `docs/rulings/mc_e1_to_e6_2026-07-14.md`. **Purpose:** the single authoritative record of all outstanding work and all discovered-gap fixes as of this date. Survives context compaction on either side: where any future in-context summary conflicts with this document, THIS DOCUMENT GOVERNS until an Owner ruling supersedes it. **This register contains no schedule.** Sequencing inside sanctioned lanes is the ruling authority's; owner decisions are marked OWNER; nothing here is deadline-bearing. **This register adds no scope.** Every item cites its origin. A work item not traceable to this register or a later ruling is defect D7.

## §1 · Proven state (context, one paragraph)
BCR v1.5 mandate-complete (2026-07-10). Engine conformance audit (2026-07-12): Solva 12/12, Targeta 11/11, Mtafiti 7/7, Northena 7/7 BUILT against on-disk mandates; SyniSense 19 rows with one PARTIAL (custody chain, closed at IF-1 2026-07-14). Registry Doctrine v1.0 in force; Registry populated (46 promises · 66+ functions · v0 + supplements v0.1/v0.2/v0.3/v0.4/v0.5); machine-readable form + parser/validator live. Operating Values v1.0 on-disk. Deviation audit baseline: 64,762 live LoC; 24-row deviation table on-disk. **G-10/G-7 PROMOTE closed 2026-07-14:** TraceReceiptPage promoted to public `/trace/:traceId`; seven other legacy pages + AppShell chrome retired; 1241 backend tests + 154 jest tests + 3 playwright smokes all GREEN. **Multi-Instance Capability MC-E1..MC-E6 closed 2026-07-14 (this amendment):** four capabilities landed atomic — structured connector class (MC-E1 α), S2.onboard surface (MC-E3 α + MC-E4 α), multi-instance operability v1 (MC-E2 α + 8,657-row backfill), RMS de-tuning (MC-E5 α contract-tier preserved + MC-E6 β headers/env-vars hard cutover); 1250 backend tests + 154 jest tests + Playwright smokes all GREEN; instance-fixture-B walks end-to-end.

## §2 · In-flight (dispatched, close owed)
*None.* IF-1 closed 2026-07-14 (custody-chain reconnection · dead-code shave · triad reconciliation). G-10/G-7 PROMOTE closed 2026-07-14. Multi-Instance Capability MC-E1..MC-E6 closed 2026-07-14 (this amendment). Next dispatched item is Owner's to signal.

## §3 · Loose threads (status owed in next builder reply)
**LT-1 · Standing Queries as CI:** SQ-E1 ruled γ + condition; execution ordered; no close returned. Status: closed/in-progress/not-started, with evidence.
**LT-2 · sequencing_harness_stage_a.md** exists on-disk but was never dispatched. Provenance: when created, by what instruction. If unsanctioned pre-work: D7 finding, file held (not deleted) pending Owner disposition.

## §4 · Gap register — every discovered gap and its fix
| # | Gap | Evidence | Fix | Authority/status |
|---|---|---|---|---|
| G-1 | Shield custody chain unreachable from live LLM path | Conformance Part A.5 | Reconnection per IF-1 | **CLOSED 2026-07-14 (IF-1)** |
| G-2 | Registry lags conformance reality | Conformance tables vs registry v0 + supplements | Registry maintenance turn: fold conformance results | SANCTIONED lane; awaits Owner sequencing |
| G-3 | Operating Values v1.0 predates conformance findings | §1 model census omits spaCy NER; diarization row states pyannote decision while build carries Silero(+seat) | Revise to v1.1 | SANCTIONED; rides after G-2 |
| G-4 | S1 envelope-completeness has no direct cell | Registry Q3-01 | Candidate cell lands in next test-bearing phase | SANCTIONED |
| G-5 | S1.scoped-key has only indirect coverage | Q3-05 | Direct cell, same vehicle as G-4 | SANCTIONED |
| G-6 | Northena audit-walk: view-side covered, walk-side uncovered | Q3-06 | Walk-side cell, same vehicle as G-4 | SANCTIONED |
| G-7 | SolvaTrace three-lens UX commitment | Surface existed; promoted to public `/trace` + `/trace/:traceId` | Promoted + smoke test | **CLOSED 2026-07-14 (G-10/G-7 PROMOTE)** |
| G-8 | S2.onboard journey step + full requirements exist; no surface | Q3-02, ruled open-by-design | S2.onboard surface built at Multi-Instance Capability close 2026-07-14 (POST /api/instance/{id}/onboard with Op. Values §8 payload · initial-set ledger discipline · MC-E3 α · MC-E4 α) | **CLOSED 2026-07-14 (Multi-Instance Capability MC-E3 α + MC-E4 α)** |
| G-9 | S4 buyer-commercial tier | Q3-03 ruling | Restores when Owner rules a commercial posture | OWNER (standing ruling) |
| G-10 | Frontend /legacy/* (1,118 LoC) disposition | At IF-1 close: only live consumer of `/legacy/*` was Ask Console's Trust receipt hrefs → TraceReceiptPage | **CLOSED 2026-07-14 (G-10/G-7 PROMOTE)** |
| G-11 | Two perception paths | Bundle finding | NOT a defect | RECORD in G-2 |
| G-12 | SyniSense lacks its own Mandate & Engineering Spec | Amendment 2026-07-12 · v1.1 §11 | Owner authors from built reality | OWNER (OD-7) |
| G-13 | ALLOWED_PURPOSES cousin's chat.* vocabulary | Amendment 2026-07-12 · v1.1 §11 | Prune to RMS-live purposes | **CLOSED 2026-07-14 (IF-1)** |
| G-14 | Platform-agnostic split unclarified: platform code, contracts, and vocabulary carry organization identity | Dispatch 2026-07-14 principle: "the platform is organization-agnostic; the estate's contents — never the customer's identity — decide which capabilities do work" | RMS de-tuning capability-4 (MC-E5 α + MC-E6 β + MC-E6 α + retired-gate preservation): contract-tier tokens preserved as class-(c) historical; live-code env vars + HTTP headers hard-cutover to `AKKI_*` / `X-Akki-*` (no external integrators — evidence-based ruling); DB_NAME variable preserved (value is instance identity, config-resident); class-(a) branding moved to `/api/instance/config` + `useInstanceConfig` hook; class-(b) fixture dir renamed to `instance_fixture_a`. | **CLOSED 2026-07-14 (Multi-Instance Capability MC-E5 α + MC-E6 β + MC-E6 α)** |
| G-15 | Multi-instance operability absent: one-codebase, per-instance isolation | Dispatch 2026-07-14 item 3 | MC-E2 α constraint architecture: mandatory `instance_id` field on every persistent row + `scoped_accessor` refuses unscoped queries + compound `(instance_id, ...)` indexes + backfill migration attested 8,657 rows across 9 collections + adversarial cross-instance cells prove denial; instance-fixture-B walks end-to-end (onboard → connect → census → brief → answer). | **CLOSED 2026-07-14 (Multi-Instance Capability MC-E2 α + backfill condition)** |

## §5 · Engine seats — designed-empty, NOT gaps
Solva Probability weighting: equal-weight default. Targeta yield layer: waits for mining history. Rung-3 owned text models: dependency-gated on estate corpus.

## §6 · Owner-decision register (raised; no deadlines; no defaults)
~~OD-1 S2.onboard build timing (G-8).~~ **DISCHARGED 2026-07-14 (Multi-Instance Capability dispatch):** Owner ordered instance-#2 capability which cannot onboard without S2.onboard; surface built in the same phase. Recorded per Owner: "OD-1 (S2.onboard build timing): RESOLVED BY CONSEQUENCE." ~~OD-2 /legacy/* disposition (G-10, after evidence).~~ **DISCHARGED 2026-07-14 (G-10/G-7 PROMOTE).** OD-3 Single-ingress navigation. OD-4 9.2b "proceed". OD-5 PH-R2/R3/R4 bindings. ~~OD-6 Trace-lens build timing IF G-7 returns data-only.~~ **DISCHARGED 2026-07-14 (three-lens surface is live-visible).** OD-7 SyniSense Mandate & Engineering Spec authoring (G-12).

## §7 · Proceed-gated register (environment; no build motion possible)
Rung-1 domain-transfer measurement → adapter decisions → BM-V (bar: Op. Values §4) → BM-C operations (§5). Production model acquisition per §1/§2. PBK-2 deploy-attest at PH-R2/R4 window. All activate on OD-4/OD-5; none is builder motion today.

## §8 · Undispatched doctrine surface (no schedule exists or is implied)
§8.1.b sequencing harness (pending LT-2 provenance) · §8.1.c worker context-harnessing · §8.1.e mandates→specs→gates endpoint · MRR-E1 β graduation (future governance amendment) · Instance Replication Playbook · Commercial Thesis (ruling-authority drafts, on Owner word).

## §9 · Binding disciplines carried (violations are D-10-class findings)
Canon before ruling (D-11) · no re-derivation · complete dispatches · decisions-not-menus to Owner · rules pay rent · verdicts never curated · no invented schedules (D7) · evidence-classed assertions (Solva discipline).

## §10 · What this document is not
Not a schedule. Not new scope. Not a secondary goal carrier: no item herein authorizes work beyond its stated fix; product specs and function requirements are altered only by Owner ruling, never by register drift. Supersession: only by Owner ruling recorded in docs/rulings/.

## §11 · Amendment 1 · 2026-07-12 (Owner-ratified) — carried from v1.1 §11
Predecessor: v1.0 at SHA cce17296a70b46ae6e1a1c64be1e9e3f18ca3f86a716758899037cf31f4d63d4. Ruling: docs/rulings/outstanding_register_v1_amendment_2026-07-12.md (SHA 06f51bf67d3c3b34024a814fd5d00bc6eb62c749181ac8945cf45f56f309ba27). Body of amendment as recorded in v1.1 §11 (carried by reference — v1.1 remains canonical for the amendment text at SHA `01016e2f679064613f6290ee4f50bdaa9874fb2e6b3c3973ccad53d3339f3224`).

## §12 · Amendment 2 · 2026-07-14 (Owner-ratified) — G-10/G-7 PROMOTE close · carried from v1.2 §12
Predecessor: v1.1 at SHA `01016e2f679064613f6290ee4f50bdaa9874fb2e6b3c3973ccad53d3339f3224`. Ruling: `docs/rulings/g10_g7_promote_2026-07-14.md`. Body carried by reference — v1.2 remains canonical for the amendment text at SHA `b8b45d2424ecfcce5f84593b1f6142104d734fb805c3e6b132b4e9953e72c90b`.

## §13 · Amendment 3 · 2026-07-14 (Owner-ratified) — Multi-Instance Capability MC-E1..MC-E6 close
Predecessor: v1.2 at SHA `b8b45d2424ecfcce5f84593b1f6142104d734fb805c3e6b132b4e9953e72c90b`. Ruling: `docs/rulings/mc_e1_to_e6_2026-07-14.md`.

Multi-Instance Capability phase closed. Four capabilities landed atomic (Tier-3 split judgment: atomic — capabilities interlocked, partial state worse than atomic):

1. **Structured-source connector class (MC-E1 α · zero contract mutation).** Generic tabular ingest → NormalizedUnits via existing five_rings@v0 shape (modality=text, locator dict `{table, row, cols}`, extraction_params satisfies text-modality catalogue). `services/data_source/structured_connector.py`. Parity 31 held byte-identical.
2. **S2.onboard surface (MC-E3 α · initial-set ledgered · MC-E4 α · internal_only default).** `POST /api/instance/{instance_id}/onboard` accepts Op. Values §8 payload (estate inventory · org vocabulary · rights posture per source · DPO contact · five §6 seam values · objective priorities). Initial-set writes single-operator; every seam-value set writes a `northena_ledger` row with `initial_set: true`. Subsequent onboard call returns 409 pending §6 ceremony. License_class default = `internal_only`, fail-closed at outer gate.
3. **Multi-instance operability v1 (MC-E2 α · constraint architecture + backfill condition).** `services/multi_instance/scoped_accessor.py` provides `sfind`, `sfind_one`, `sinsert_one`, `scount_documents` — refuses queries without positional `instance_id`. Backfill migration `tools/migrations/backfill_instance_id_2026_07_14.py` set `instance_id="instance_1"` on 8,657 pre-existing rows across 9 collections; 0 unscoped rows post-migration. Compound `(instance_id, ...)` indexes on 11 collections. Adversarial cross-instance cells prove denial. Instance-fixture-B (`services/data_source/synthetic_assets/instance_fixture_b/`) walks end-to-end.
4. **RMS de-tuning (MC-E5 α class-(c) preserved contracts · MC-E6 β hard cutover headers/env vars · MC-E6 α DB_NAME preserved · retired-token gates verbatim).** STEP 1 cutover guard result: **AUTHORIZED** (0 non-fixture external integrators with live keys; 1 fixture-record `b2-scope-gate-test` disqualifies per fixture-shaped identifier). Contracts + snapshots (`backend/contracts/**` + `backend/tests/invariants/*.contract_snapshot.json`) preserved BYTE-IDENTICAL. HTTP headers renamed hard cutover: `X-RMS-App-ID` → `X-Akki-App-ID`; `X-RMS-Webhook-URL` → `X-Akki-Webhook-URL` (13 occurrences). Env vars renamed hard cutover: 139 `RMS_*` → `AKKI_*` occurrences across 26 live files (values preserved byte-identical). `DB_NAME` variable name UNCHANGED; instance-#1 value stays `rms_intelligence`. `test_master_admin_auth_reconciliation.py` retired-token grep-negative gate PRESERVED VERBATIM (Owner ruling: retired-token gates test that retired tokens are not emitted; renaming defeats semantics). Class-(a) branding moved to `/api/instance/config` (public) + `useInstanceConfig` hook. Class-(b) fixture dir renamed: `rms_adversarial_v1/` → `instance_fixture_a/`; `real_rms.py` → `real_estate_adapter.py`.

Register status updates:
- §4 · new closed rows G-14 (platform-agnostic split) and G-15 (multi-instance operability) discharged same commit.
- §6 · OD-1 (S2.onboard build timing): CLOSED · DISCHARGED-BY-CONSEQUENCE at Owner dispatch 2026-07-14.
- §8 · no additions (Owner-side sequencing lane per §11).

Post-phase sanctioned sequencing (unchanged): G-2 (Registry maintenance) then G-3 (Operating Values v1.1).

**Exit gates satisfied:**
| Gate | Result | Command |
|---|---|---|
| Cutover guard (STEP 1 pre-flight) | AUTHORIZED — 0 non-fixture external integrators | Motor query on 16 live collections |
| Backend full sweep | **1250 passed · 1 skipped · 0 failed** | `pytest tests/ -q` |
| Contract invariants (Parity 31) | **1001 passed · 1 skipped** — 31 snapshots byte-identical | `pytest tests/invariants/ -q` |
| Instance isolation gates (MC-E2 α) | **5/5 GREEN** — refuses unscoped, cross-instance denial, backfill attest, compound-index shape | `pytest tests/registry/test_instance_isolation.py -q` |
| Instance-fixture-B walkthrough (MC-E2 α proof) | **4/4 GREEN** — fixture shape · connector produces valid units · license_class fail-closed · onboard→ledger→isolation | `pytest tests/registry/test_instance_fixture_b_walkthrough.py -q` |
| Backfill migration | **8,657 rows backfilled across 9 collections · 0 unscoped rows remaining** | `python -m tools.migrations.backfill_instance_id_2026_07_14` |
| Frontend UI-spec gates | **154 passed · 24/24 suites** | `yarn test --watchAll=false` |
| Playwright smokes (chromium) | **2 passed (1.1s)** — trace surface unchanged | `npx playwright test e2e/trace_smoke.spec.ts` |
| MRR gates (G1-G4 + Parity + DataBlind + SourceSHA) | **7/7 GREEN** | `python -m tools.registry.regenerate --check` |
| Registry run_queries coherence | **OK · 6 artifacts · no source-of-truth drift** | `python -m tools.registry.run_queries --check` |
| v0.5 supplement | 21 R4 reflexive rows · sections §S1..§S6 · zero new promises | fs-verify |

**Parity 31 held.** 31 contract snapshots byte-identical; 1001 invariant tests GREEN; contracts/ diff-empty; snapshots diff-empty.

## §14 · Amendment 4 · 2026-07-14 (Owner-ratified) — G-2 Registry Maintenance Turn close

Predecessor: v1.3 at SHA `855392daa79a0e223db9c21fc12601f9b2d2bc23a827eb548291f827ecbecb94`. Ruling: `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md`.

G-2 Registry Maintenance Turn closed. Six deltas landed:

- **Delta 1 · §4 G-2 line status:** `[QUEUED · Stage A drafted 2026-07-14]` → `[EXECUTED · atomic-commit 2026-07-14 · close_reports/g2_registry_maintenance.md]`.
- **Delta 2 · §5 Registry version pin:** `v0.md + v0.1..v0.5 supplements` → **`v1 consolidated`** (`docs/registry/function_promise_registry_v1.md` · SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`; v0 lineage immutable on-disk per Standing Rule v3; v1 becomes active source; MRR-G3 round-trip re-pinned to v1).
- **Delta 3 · §5 Q2-05 disposition:** `[HELD · pre-doctrine-close-reports · read-required]` → `[READ · per-gate rulings recorded in docs/registry/queries/q2_05_individual_reads.md · zero retirements · all 7 close-report groups RECOVERED]`.
- **Delta 4 · §5 Q3-02:** `[RULED · Q3-02-OPEN-BY-DESIGN 2026-07-11 · [OWNER: future phase]]` → `[RE-RULED · Q3-02-BUILT 2026-07-14 · MC-E3 α close · services/multi_instance/onboard_context.py · routers/s2_onboard.py]`.
- **Delta 5 · §5 Q4 standing query:** `(absent)` → `[STANDING · first-run findings recorded as DELIVERABLE per Owner RM-E3 α · docs/registry/queries/q4_archaeological.md + q4_mechanical.md · CLIENT-PROMISE UNVERIFIED flagging + advisory remedy-candidate:P4 marker permitted]`.
- **Delta 6 · §17 (sequencing anchor · maintained verbatim):** G-2 → G-3 → EAB-1/2/3 lane carried unchanged.

**Consolidation posture (RM-E1 α byte-carriage):** every promise-text field in v1 is byte-identical to its source (v0.md + v0.1..v0.5). Zero in-flight edits. Machine-enforced by `backend/tests/registry/test_registry_v1_consolidation_byte_identity.py::test_v1_promise_text_byte_identical_to_source`.

**Alias canonicalization (governance-amendment-only clause satisfied):** `PART_II_JOURNEY_STEPS` frozenset in `backend/services/registry/validator.py` canonicalizes to short forms (`S3.prove`, `S4.verify`); legacy long-form aliases (`S3.prove-end-to-end`, `S4.verify-receipt`) retired. Machine-enforced by `backend/tests/registry/test_part_ii_journey_steps_alias_canonicalization.py`.

**8-row conservation posture:** all 8 new R4 rows in v1 §M attach to existing promises (6 × `PROM-S1-frozen-wire-contract` + 2 × `PROM-S3-audit-trail-immutable`) via foreign-key resolution. Zero new promises minted.

**D-10 STANDING PRACTICE (Owner-ratified):** every Stage-A / close-report terminal reply carries D-1..D-11 self-audit table.

Register status updates:
- §4 · G-2 row now `[EXECUTED · atomic-commit 2026-07-14]`.
- §5 · Registry version pin flipped to v1.
- §5 · Q2-05 flipped to `[READ]`.
- §5 · Q3-02 flipped to `[RE-RULED · BUILT]`.
- §5 · Q4 line added: `[STANDING · first-run findings DELIVERABLE]`.

Post-phase sanctioned sequencing (unchanged): **G-3 (Operating Values v1.1 fold)** dispatch-only; EAB-1/2/3 phases enter standard loop after G-3 close.

**Exit gates satisfied:**

| Gate | Result | Command |
|---|---|---|
| RM-E1 α byte-identity gate | **GREEN** · 0 drift findings · v1 promise-text byte-identical to source | `pytest tests/registry/test_registry_v1_consolidation_byte_identity.py -q` |
| Q4 standing query cells (6 gates) | **GREEN** · run · reproduction · report-level · client-promise flagging · cross-ref · parity · data-blind | `pytest tests/registry/test_q4_gates.py -q` |
| Alias canonicalization gate | **GREEN** · canonical short forms present · legacy long-form aliases rejected | `pytest tests/registry/test_part_ii_journey_steps_alias_canonicalization.py -q` |
| Parity 31 | **31/31** held byte-identical · contracts/ + snapshots diff-empty | `ls backend/contracts/*.py \| wc -l` + `git diff HEAD backend/contracts/` |
| Machine-form re-pin | **v1-source** SHA `e8cdf3c8b29f94e8da92d62df80a03cbddeb41969d37eec4ea0540910d98cd90` | `python -m tools.registry.regenerate` |
| Standing Rule v3 · v0 lineage | **diff-empty** on v0.md + v0.1..v0.5 supplements | `git diff HEAD docs/registry/function_promise_registry_v0*.md` |
| Standing Rule v3 · prior rulings/registers | **diff-empty** on docs/rulings/ + docs/briefs/outstanding_work_and_gap_register_v1.{0..3}.md | `git diff HEAD docs/rulings/ docs/briefs/` |
| Q2-05 individual reads landed | **7 groups · zero retirements** · docs/registry/queries/q2_05_individual_reads.md · SHA `69de26552a179d3778eed1980d04157ebed5b26f04d9c56c6c984774ab29677f` | fs-verify |
| Q4 artifacts landed | **2 files** · q4_archaeological.md SHA `6c6e69cee090963c888bcc0929bd17a5a56475957e6a2d398b8272731bbd39de` · q4_mechanical.md SHA `2f9090ec348d06c300e2b4de10c5aff908d41355a5492c8832735795d112689f` | fs-verify |

═══════════════════════════════════════════════════════════════════

*End of register v1.4. Standing Rule v3 · on-disk canonical.*
