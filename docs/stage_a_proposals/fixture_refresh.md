# Fixture Refresh mini-phase · Stage A Proposal (post-9.2a · Owner Ancillary 2 · 2026-07-10)

**Dispatch:** Owner Ancillary 2 ratified 2026-07-10; Fixture Refresh mini-phase Stage A green-lit post-9.2a-close.
**Basis:** governance §8 data-blind posture (Owner-verbatim 2026-07-09 landed at `docs/governance/tiered_ruling_model.md` §8). Prior disclosures at TF Item 3 (deferred broader refresh) + STEP A commit `b3ac048` (scan disclosure: 10 test files + 1 config as root pre-descriptions).
**Sequence position:** post-9.2a-ratification; ahead of §3.8 Answer fluency; ahead of Opportunity Briefs; ahead of production housing.
**Governance model:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Escalations pre-tiered per §4.4.
**Standing Rule v3:** on-disk canonical. Reply body carries file SHA + line-range map + tier-tagged escalation IDs only.
**Metric-verdict discipline (governance §9):** band derived and verdict rendered in raw LoC.
**9.2 split (governance §10):** no 9.2b work touched.

---

## §0. Owner text — verbatim carriers

### §0.1 Owner Ancillary 2 verbatim (from post-9.2a dispatch, 2026-07-10)

> correctly escalated, and the answer is a scoped mini-phase after 9.2a close, not a ride-along. The builder's instinct to stop was right — a HAZARD-STOP-protected fixture plus a v0→v1 registry bump plus a ~10-file cascade is a coordinated change, and coordinated changes don't ride housekeeping commits. It queues as a named mini-phase post-9.2a: one Stage A (small), the HAZARD-STOP posture question surfaced there as its Tier-1 item, license_class_map v0→v1 additive per standing pattern. Until then it stays deferred-and-disclosed, which is its current honest state.

### §0.2 Governance §8 data-blind posture verbatim carrier (Owner, 2026-07-09)

> The build makes no assumptions about the content, genre, composition, or shape of the RMS estate. Fixtures, examples, adversarial cases, admin binding copy, and rulings-text all use content-neutral placeholders (`region_a..region_h`, `unclassified`, `content_type_placeholder`); no region name, no content-type category, no editorial-slot label leaks in as a pre-description. Estate description is a census-run output, not a pre-build assumption. Pre-build data request to RMS is prohibited by this posture. First contact = census.

### §0.3 HAZARD-STOP semantics (on-disk documentation, verbatim)

From `services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py:1` docstring:

> Adversarial synthetic fixture generator — CONTRACT-SHAPE emit (post-HAZARD-STOP #1). Emits units conforming to frozen `five_rings@v0` verbatim (NormalizedUnit). No `unit_type`, no `content`, no `freshness_stamp`, no `_fixture` at the unit top-level.

From `services/data_source/synthetic_assets/rms_adversarial_v1/rejected/REJECTION.md`:

> Adopting the incoming shape would require **mutating** the frozen `NormalizedUnit` contract — a HAZARD-STOP (a) cascade through `LedgerRow.artifact_ref`, Layer C stamp emission, and V1/V3 harnesses.

**Builder reading (disclosure at Stage A · not Owner text):** HAZARD-STOP #1 protected the *frozen-contract shape* of `NormalizedUnit` from cascading mutation. Regenerating the fixture with different *content* (broadcaster names → neutralized placeholders) while preserving the five_rings@v0 contract shape is NOT the HAZARD-STOP #1 concern — but it IS the Tier-1 question the Owner has explicitly named for this Stage A (FR-E1 [Tier 1] below): the on-disk documentation names "HAZARD-STOP" specifically for contract-shape hazards; whether a content-neutralization regeneration is inside or outside the HAZARD-STOP posture requires Owner ruling.

---

## §1. Cell-density assumption (rates carried forward from governance §6)

### §1.1 Empirical baseline (all codifications up to 9.2a atomic `3720fb6`)

| Class | Rate | Basis | Applies at Fixture Refresh? |
|---|---:|---|---|
| Backend Pytest shared-helper amortised | 12 LoC/cell | §6.1 | YES — attest cells |
| Backend endpoint impl 3-share amortised | 40 LoC/endpoint | §6.2 | N/A — no new endpoints |
| Backend service module standalone | 100 LoC/module | §6.3 | N/A — no new modules (edits to existing) |
| Frontend Jest structural fallback | 16 LoC/cell | §6.4 | N/A — no frontend surface |
| Playwright chromium data-testid | 9 LoC/cell | §6.5 | N/A — no UI |
| Frozen Pydantic contract class | 60 LoC/class | §6.6 | N/A — parity 31 stands |
| Frozen contract snapshot JSON | ~155 LoC/snapshot | §6.7 | N/A — no new snapshots |
| **Verbatim-carrier overhead** | **~100-150 LoC/carrier** | **§6.9** | **YES — 1 carrier (this Stage A + rulings + close carry Owner Ancillary 2 verbatim + governance §8 + §0.3 HAZARD-STOP docs)** |
| **AST/reflection gate cell** | **~40 LoC/cell** | **§6.10** | **YES — 1 candidate cell (feed-id-usage AST-scan reflection to enforce v1 alias discipline; contingent on FR-E2 α ruling · see §5.2)** |
| **Async httpx auth-overhead cell** | **~25 LoC/cell** | **§6.11** | N/A — no E2E cells; the refresh operates on config + tests, not new endpoints |

### §1.2 Watched rate classes (per governance §6.8; empty as of 2026-07-10)

- Empty. Two first-observation candidates from 9.2a close (CPU/GPU dual-mode gate cells at 9.2a-G2 · model-provenance attestation cells at 9.2a-G1) — Fixture Refresh does NOT trigger either. Watch list stays empty at this phase.

### §1.3 Mini-phase-specific cell classes

None emerge. Refresh decomposes into standard shapes (config edit, snapshot re-bless, test-file surgery, docs).

---

## §2. Matrix enumeration

### §2.1 HAZARD-STOP-adjacent adversarial fixture

**Path:** `backend/services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json` (993 lines · SHA `f137c6ed8d013892cb413cf3f06c86301d0217d08615e61f4cb1c09f91bca423`).
**Generator:** `backend/services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py`.

**Current pre-descriptions embedded:**
- 8 broadcaster feed_ids: `citizen_tv_news`, `citizen_archive`, `citizen_drama`, `wire_kna`, `radio_jambo_callin`, `aggregator_blog`, `x_ingest`, `unclassified` (8th is content-neutral).
- 1 programme name `Social Ingest` + 1 speaker `handle_xyz` + 1 embedded assertion `"BREAKING: bridge on Thika road imeanguka, cars stuck everywhere!!"` (Kenya-specific location + Swahili-mix language).
- Language-mix arrays containing `sw`, `en`, `sheng` (East Africa-specific).

**What "HAZARD-STOP protection" means (from on-disk documentation):** the fixture was regenerated after HAZARD-STOP #1 — a frozen-contract-mutation cascade risk. Preserving contract-shape (five_rings@v0 verbatim) is the load-bearing posture. Content changes (feed_id names, programme names) are OUTSIDE the frozen-contract-shape locus — but whether they land inside or outside the HAZARD-STOP posture requires Owner ruling (**FR-E1 [Tier 1]** · §5.1).

**Proposed refresh under FR-E1 α (regenerate with neutralized content):** feed_ids → `feed_a..feed_h`; programme names → `programme_a..programme_c`; embedded assertion → content-neutral (e.g., `"BREAKING: incident-neutral-placeholder"`); language-mix arrays → generalised (`lang_a`, `lang_b`, `lang_c`) or removed. SHA changes (obviously); contract shape byte-identical.

**Proposed refresh under FR-E1 β (leave fixture untouched, refresh elsewhere only):** fixture stays byte-identical; downstream carriers (§2.2..§2.6) rename via v0→v1 additive alias tables. Cost: distributed alias resolution at every consumer.

### §2.2 `license_class_map.v0.json` v0 → v1 additive

**Path:** `backend/services/service_1/license_classes.v0.json` (35 lines · SHA `3351496c…`).

**Current v0 `feed_id_to_license_class` entries (5):**
```json
{
  "citizen_tv_news": "editorial_use",
  "ktn_news": "syndication",
  "ntv_news": "syndication",
  "print_edition": "editorial_use",
  "wire_kna": "training_data"
}
```

**Proposed v1 additive (standard v0→v1 bump per B-5b Ruling E3 γ + P8E-E7 α + CD-E3 α + 9.2a-E1 α precedent):**
- Land `backend/services/service_1/license_classes.v1.json` with:
  - v0 entries preserved verbatim (backward-compat during transitional window).
  - NEW neutralized entries: `feed_a: editorial_use` (aliases citizen_tv_news) · `feed_b: syndication` (aliases ktn_news) · `feed_c: syndication` (aliases ntv_news) · `feed_d: editorial_use` (aliases print_edition) · `feed_e: training_data` (aliases wire_kna).
  - Additional data-blind entries for the other 3 fixture broadcasters not currently in the license map (`citizen_archive`, `citizen_drama`, `radio_jambo_callin`, `aggregator_blog`, `x_ingest` → mapped to `feed_f..feed_j`).
- Loader `services/service_1/*` reads highest-version (v1). Runtime prefers v1; consumers keep v0-keyed lookups working during transitional window OR migrate to v1-keyed lookups per FR-E2 ruling.
- Verbatim carrier: Owner Ancillary 2 text embedded in v1.json as `authority_source` field (matches models_registry.v0.json + census_content_surfaces.v0.json convention).

### §2.3 Source-standing placeholder table

**Path:** `backend/services/mtafiti/source_standing.py::_PLACEHOLDER_TABLE` (lines 37-46).

**Current state:** already self-declared `synthetic_placeholder=True` + `editorial_authority=False` (partial mitigation from prior data-blind discipline). But table KEYS are still broadcaster-derived (`citizen_tv_news`, `citizen_archive`, `citizen_drama`, `wire_kna`, `radio_jambo_callin`, `aggregator_blog`, `x_ingest`, `unclassified`).

**Proposed refresh (contingent on FR-E1 α + FR-E2 ruling on distributed vs centralized):**
- If FR-E1 α + FR-E2 α (centralized single-source): drop the `_PLACEHOLDER_TABLE` here; consumers read from `license_class_map.v1.feed_id_to_source_standing` (extend v1 with the source_standing column).
- If FR-E1 α + FR-E2 β (distributed cascade): rename keys in `_PLACEHOLDER_TABLE` to `feed_a..feed_h` inline; comment carries prior mapping trace.
- If FR-E1 β (fixture untouched): keys stay; carry `synthetic_placeholder=True` flag as-is; add module-level comment stating "keys aliased from fixture; see license_class_map.v1.json for neutralized aliases."

### §2.4 Outer-gate feed_id bucket table

**Path:** `backend/services/outer_gate/transform.py::_FEED_ID_BUCKET` (lines 42-51).

**Current state:** 4 entries mapping broadcaster names → `broadcast_news` / `broadcast_print` categories. Used at k-anonymity generalisation for irreversibility transform.

**Proposed refresh (symmetric with §2.3):**
- FR-E2 α (centralized): move mapping into `license_class_map.v1.json` `feed_id_to_bucket_category` field.
- FR-E2 β (distributed): rename keys inline to neutralized aliases; behavior preserved.
- FR-E1 β: keys stay; comment references v1 alias table.

### §2.5 Test file cascade (~10 files enumerated at STEP A `b3ac048` scan)

Files identified at scan (10 files) with per-file assumption + refresh scope:

| # | File | Content-type assumption | Proposed refresh scope |
|---:|---|---|---|
| 1 | `tests/invariants/test_mtafiti_invariants.py` | `citizen_tv_news` seed rows for source-standing test | rename to neutralized alias per FR-E2 |
| 2 | `tests/invariants/test_dispatch_shape_responsive.py` | `citizen_tv_news` inline literal for license-class filter (line 420) | rename via v1 alias |
| 3 | `tests/invariants/test_qualified_data_selection.py` | multiple broadcaster feed_ids as seed rows | rename via v1 aliases; also `wire_kna` |
| 4 | `tests/invariants/test_outer_gate_irreversibility.py` | `citizen_tv_news` in `canonical` dict for outer-gate transform snapshot test (line 210) | see FR-E3 [Tier 1] · snapshot re-bless question |
| 5 | `tests/invariants/test_qualified_data_outer_gate_ride.py` | `citizen_tv_news` as scope_ref | rename via v1 alias |
| 6 | `tests/invariants/test_phase_5_stage_b_async_delivery.py` | `citizen_tv_news` as fixture-derived feed_id | rename via v1 alias |
| 7 | `tests/invariants/test_targeta_invariants.py` | multiple broadcaster feed_ids (citizen_tv_news + wire_kna) | rename via v1 aliases |
| 8 | `tests/invariants/test_trace_lens_cross_engine_correlation.py` | `citizen_tv_news` cross-engine correlation seed | rename via v1 alias |
| 9 | `tests/invariants/test_feasibility_honesty_under_absence.py` | multiple broadcaster feed_ids + explicit data-blind note | rename via v1 aliases (data-blind note preserved) |
| 10 | `tests/invariants/test_composed_conclusion_dispatch.py` | `citizen_tv_news` as canonical claim seed | rename via v1 alias |

**Downstream test impact:** each rename is a mechanical literal-string substitution. Assertion behavior is preserved because the v1 alias maps to the same license class + same source_standing + same bucket category. Test cells continue to assert the SAME license class outcomes; only the input feed_id string changes.

### §2.6 Snapshot re-bless posture — `outer_gate_transform.snapshot.json`

**Path:** `backend/tests/invariants/outer_gate_transform.snapshot.json` (contains `feed_id: "citizen_tv_news"` inside `canonical_input`).

**Status:** NOT a frozen-contract snapshot (V1-G7 counts `*.contract_snapshot.json` only · this is `.snapshot.json` transform-golden). Byte-identity attested at `test_outer_gate_irreversibility.py:219-223` with re-bless discipline ("re-bless in review if intentional").

**Proposed refresh (contingent on FR-E1 + FR-E3):** re-bless snapshot with neutralized feed_id in `canonical_input` + updated egress artifact fields. SHA changes; re-bless discipline honored. **FR-E3 [Tier 1] escalation** enumerates the on-disk-canonical-vs-re-bless question — see §5.3.

### §2.7 Named gate roster

| Gate | Class | Cells | Rate | Purpose |
|---|---|---:|---:|---|
| **FR-G1** license_class_map v0 preserved byte-identical | classic (§6.1) | 1 | ~12 | v0.json SHA unchanged post-commit; append-only additive discipline honored. |
| **FR-G2** license_class_map v1 present with additive entries | classic (§6.1) | 1 | ~12 | v1.json loads; contains v0 entries + new neutralized aliases. |
| **FR-G3** Loader reads highest version (v1 preferred) | classic (§6.1) | 1 | ~12 | `services/service_1/*_loader` returns v1 keys; v0 keys resolved via alias. |
| **FR-G4** No unaliased broadcaster feed_id in NEW code | AST/reflection (§6.10) | 1 | ~40 | AST-scan reflection over service modules verifying no NEW code introduces v0-style broadcaster keys directly. Contingent on FR-E2 α. |
| **FR-G5** Adversarial fixture SHA attest (or re-blessed) | classic (§6.1) | 1 | ~12 | Contingent on FR-E1: (α) new SHA + generator update attested; (β) SHA byte-identical preserved. |
| **FR-G6** Test cascade assertion parity | classic (§6.1) | 1 | ~12 | Each of the 10 test files' cell count + assertion count preserved through refresh. Pytest count MUST land 1143 → 1143 (or +/- explicit disclosure). |
| **FR-G7** `outer_gate_transform.snapshot.json` re-bless (or preserve) | classic (§6.1) | 1 | ~12 | Contingent on FR-E3: (α) re-bless SHA attest; (β) SHA byte-identical preserved. |
| **V1-G7** parity 31 attest | classic (§6.1) | 1 | ~12 | 31 frozen contract snapshots byte-identical unchanged (no new contracts). |
| **4-code auth-refusal registry** re-attest | classic (§6.1) | 1 | ~12 | Standing re-attestation. |
| **E5** no HTTP 409 in Fixture Refresh new/modified files | classic (§6.1) | 1 | ~12 | Standing anti-rule attest. |

**Backend cell count total: 10 cells** (9 classic §6.1 + 1 AST/reflection §6.10). No frontend cells.

### §2.8 UI Spec binding-copy adjacency

**Scan result (this Stage A):** grep across `docs/mandates/RMS_UI_Specification*.md` + `docs/mandates/RMS_Build_Completion_Requirements*.md` for broadcaster names — **ZERO hits**. UI Spec binding copy does NOT reference specific content types or broadcaster names. No Tier-1 UI-adjacency escalation required.

---

## §3. Owner-anchored band derivation (raw LoC per governance §9)

Applying §1.1 rates to the §2 matrix. Band structure contingent on FR-E1 + FR-E2 rulings (α scenario = full refresh; β = minimal).

### §3.1 Line-items

| Line-item | Basis | Raw LoC (α scenario) | Raw LoC (β scenario) |
|---|---|---:|---:|
| `license_classes.v1.json` additive | flat + verbatim carrier subfrac | ~60 | ~60 |
| Loader edits (services/service_1) — highest-version discovery | §6.3 subfrac (~20 LoC) | ~20 | ~20 |
| `source_standing.py` refresh (§2.3) | inline edits (~20 LoC α · ~10 LoC β · comment only) | ~20 | ~10 |
| `outer_gate/transform.py` refresh (§2.4) | inline edits (~20 LoC α · ~10 LoC β) | ~20 | ~10 |
| Adversarial fixture regenerate (§2.1) — generator delta + fixture body | ~30 LoC generator edit + ~995 fixture body (byte-changed but same shape) | ~1,025 (α) | 0 (β — untouched) |
| Test cascade — 10 files × ~3-5 renames each | mechanical replaces (~3 LoC delta/file) | ~30 | ~15 (β minimum — some tests keep old keys) |
| `outer_gate_transform.snapshot.json` re-bless (α) or preserve (β) | ~15 LoC delta if re-blessed | ~15 | 0 |
| Backend gate cells: 9 classic × §6.1 | 9 × 12 | ~108 | ~108 |
| Backend gate cell: 1 AST/reflection × §6.10 (FR-G4) | ~40 | ~40 | ~40 (or 0 under β if FR-G4 becomes non-applicable) |
| Verbatim carrier (§6.9) | 1 carrier ~40 raw (light-end · this file + rulings + close carriers) | ~40 | ~40 |
| Docs (this Stage A · rulings record · close report) | prose | ~200 | ~200 |
| **Point-estimate (raw LoC)** | | **~1,578** (α with full fixture regen) | **~503** (β minimal) |
| **Point-estimate excluding fixture body** | | **~583** (α without the 995 fixture bytes counted as "LoC") | **~503** (β) |

**Note on fixture-body LoC counting:** the adversarial fixture JSON is a machine-generated data payload of 993 lines. Counting it as "LoC" per §6.x rate ledger is honest only under the raw-wc-l metric-verdict rule (§9); it's a structural transposition of content-neutral placeholders into pre-existing shape, not authored logic. **Disclosed as line-item; the band assumes the fixture body is counted per §9 raw-LoC verdict discipline.**

### §3.2 Proposed Owner-anchored band (raw LoC · per governance §9)

**Two scenarios:**

- **Scenario α (FR-E1 α — fixture regenerate):** point-estimate ~1,578 raw · **proposed band `[1,200, 1,800]`** (mid ~1,500).
- **Scenario β (FR-E1 β — fixture untouched):** point-estimate ~503 raw · **proposed band `[380, 600]`** (mid ~490).

**Both scenarios' §4.2 thresholds:**
- §4.2 pre-authorized raw LoC split: 1,500 → **triggered under α** (single atomic acceptable per §4.1 baseline · Owner ruled split disposition at CD's +26% miss); **not triggered under β**.
- §4.2 pre-authorized cell split: 60 → **NOT triggered** in either scenario (10 cells).

**Snapshot raw LoC in-band:** projected yes for whichever scenario Owner rules.

### §3.3 Metric-verdict discipline (governance §9)

Verdict rendered in raw LoC. LLoC + cell-count + fixture-body ratio may appear as disclosure lines only.

---

## §4. Dispatch discipline

### §4.1 Baseline

Single atomic first-commit per §4.1. Under Scenario α, §4.2 pre-authorized LoC split may be invoked at execution IF surface coherence is preserved with a two-commit split (fixture regen commit + test-cascade commit); disclosure-only decision per Tier-2. Under Scenario β, single atomic commit is the default.

### §4.2 Pre-authorized split thresholds

| Threshold | Value | Status α | Status β |
|---|---:|---|---|
| §4.2 pre-authorized raw LoC split | 1,500 | **triggered** (point-estimate 1,578) | NOT triggered |
| §4.2 pre-authorized cell split | 60 | NOT triggered (10 cells) | NOT triggered |

### §4.3 Dispatch-independence + [OWNER] gates

- Fixture Refresh is dispatch-independent from 9.2-OWN-1..3 (not gated on venue/deployment/BM-V).
- No new [OWNER] gates emerge from Fixture Refresh.
- AS-OWN-1 (production object-store) still open — dispatch-independent.
- §3.8 answer fluency STILL_QUEUED at BCR §5.1 line 336 (Owner Message 565 status) — not this phase's scope.

### §4.4 Escalation tiering (governance §4.4 pre-tiered)

- **Tier-1 (verbatim relay before execution):** FR-E1, FR-E2, FR-E3 (§5.1..§5.3).
- **Tier-2 (disclosure-only at close · no ruling):** FR-E4 (§5.4).
- **Tier-3 (silent · one-line disclosure at close):** FR-T1..FR-T7 (§5.5).

---

## §5. Escalations — PRE-TIERED per governance §4.1

### §5.1 FR-E1 [Tier 1] · HAZARD-STOP posture — can the adversarial fixture be regenerated with neutralized content? (Owner-named)

**Class:** frozen wire contract discipline (governance §1.1 last bullet · HAZARD-STOP #1 lineage) + data-blind posture (governance §8) + honesty grammar.

**Question:** the adversarial fixture at `services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json` was regenerated once after HAZARD-STOP #1 (contract-shape mutation cascade). Its on-disk documentation names "HAZARD-STOP" only for CONTRACT-SHAPE hazards. Can a Fixture Refresh regenerate the fixture with NEUTRALIZED CONTENT (broadcaster feed_ids → `feed_a..feed_h`; programme names → `programme_a..programme_c`; embedded assertions → content-neutral placeholders; language-mix arrays → generalised) while preserving five_rings@v0 contract shape byte-identical? OR does HAZARD-STOP protection extend to CONTENT as well (fixture untouched · alias-only refresh)?

**Authority-source language (on-disk documentation, verbatim):**

> Adversarial synthetic fixture generator — CONTRACT-SHAPE emit (post-HAZARD-STOP #1). Emits units conforming to frozen `five_rings@v0` verbatim (NormalizedUnit).

> Adopting the incoming shape would require **mutating** the frozen `NormalizedUnit` contract — a HAZARD-STOP (a) cascade through `LedgerRow.artifact_ref`, Layer C stamp emission, and V1/V3 harnesses.

**Promise-protected:** (i) frozen wire contract shape discipline (HAZARD-STOP #1 concern); (ii) governance §8 data-blind posture (which is the promise motivating this Refresh phase); (iii) audit clarity — the fixture is the seed for many downstream test-consumers; changing its content changes their inputs.

**Options:**

- **α (regenerate with neutralized content · contract shape byte-identical):** regenerate `fixture.json` via `generate_fixture.py` with a data-blind-compliant content set: feed_ids → `feed_a..feed_h`; programme names → `programme_a..programme_c`; embedded assertions → generic content-neutral English (e.g., `"BREAKING: incident-neutral-placeholder"`); language-mix arrays → `["lang_a", "lang_b"]`. Contract shape (five_rings@v0) preserved byte-identical — HAZARD-STOP #1 remains honored. Fixture SHA changes (obviously); downstream consumers (10 test files) rename via v1 alias table.
- **β (fixture untouched · v1 alias table added elsewhere · no fixture regen):** fixture stays byte-identical. `license_classes.v1.json` adds v0-keyed entries preserved + new v1-keyed aliases. Downstream consumers can rename to v1-keyed aliases OR keep v0-keyed lookups. Fixture content remains as data-blind-posture-violating tokens but is DECLARED as `synthetic_placeholder=True` at every carrier's runtime lookup (already the pattern at `source_standing.py`).
- **γ (retire the fixture entirely):** rejected — adversarial fixture is load-bearing on many V1/V3 harnesses and NormalizedUnit contract-shape tests. Retirement would cascade beyond Fixture Refresh scope.

**Recommended:** **α (regenerate with neutralized content).** Rationale: (1) governance §8 data-blind posture is load-bearing; a fixture containing real broadcaster feed_ids IS a pre-description of estate shape, regardless of `synthetic_placeholder=True` runtime flags — the STRINGS themselves leak assumptions into every consumer's test data; (2) HAZARD-STOP #1 doctrine on-disk is explicit about CONTRACT-SHAPE hazard, not content hazard — the content of the fixture is orthogonal to HAZARD-STOP #1; (3) contract-shape preservation is easy to attest (five_rings@v0 conformance test still lands GREEN post-regen); (4) β leaves the data-blind violation intact and adds an alias layer that just papers over it.

**Escalation surface:** frozen wire contract discipline (HAZARD-STOP #1) + data-blind posture (§8) + honesty grammar. Full-rigor Tier-1. Owner ruling required BEFORE execution.

---

### §5.2 FR-E2 [Tier 1] · Source-of-truth posture — centralized single-source registry OR distributed cascade?

**Class:** honesty grammar (governance §1.1 · "class-with-claim" · single-source-of-truth adjacency) + cost/rework (§6.2 rate-of-change concern).

**Question:** the broadcaster-name pre-descriptions currently live in FIVE places (fixture body · `license_classes.v0.json feed_id_to_license_class` · `source_standing.py _PLACEHOLDER_TABLE` · `outer_gate/transform.py _FEED_ID_BUCKET` · 10 test files as literals). Should the refresh CENTRALIZE these into a single-source-of-truth (e.g., `license_classes.v1.json` extended with per-feed_id attributes for source_standing + bucket_category + license_class) with all consumers reading from it, OR apply DISTRIBUTED cascade (each carrier keeps its own table with rename-only refresh)?

**Authority-source language (governance §8 · Owner-verbatim landed at `docs/governance/tiered_ruling_model.md:238`):**

> Pre-build data request to RMS is prohibited by this posture. First contact = census.

**Authority-source language (Owner Ancillary 2 verbatim):**

> license_class_map v0→v1 additive per standing pattern

**Promise-protected:** (i) honesty grammar — multiple sources of truth for the same fact (which feed_id maps to which category) creates disclosure fragmentation; (ii) governance §6.x rate-of-change discipline — a centralized source ages once at v1→v2; distributed cascade ages 5x per rename.

**Options:**

- **α (centralized single-source):** extend `license_classes.v1.json` schema to include per-feed_id attributes: `license_class` (existing) + `source_standing` (new; migrated from `source_standing.py::_PLACEHOLDER_TABLE`) + `bucket_category` (new; migrated from `outer_gate/transform.py::_FEED_ID_BUCKET`). Consumers read via `license_class_map` module functions. Distributed tables removed (deleted at v1; v0 preserved byte-identical).
- **β (distributed cascade · rename-only):** each existing table renames its keys in-place via v1 aliases; consumers keep reading from their existing tables. `license_classes.v1.json` bumps additive-only; `source_standing.py` + `outer_gate/transform.py` receive inline edits (~10 LoC each).
- **γ (hybrid · centralized for new tables · distributed for existing):** license_classes stays as license-only; new `feed_registry.v1.json` centralizes the OTHER attributes (source_standing + bucket_category). Three-artefact refresh instead of one.

**Recommended:** **α (centralized).** Rationale: (1) single-source-of-truth reduces future maintenance cost; (2) matches CD-E3 α register-before-validate pattern (single registry-as-authority · additive bump); (3) matches models_registry.v0 → v(N+1) pattern from 9.2a-E1 α; (4) β leaves the "which is authoritative" ambiguity unresolved; (5) γ triples the mental-model surface without proportional gain.

**Escalation surface:** honesty grammar + cost/rework strategy. Full-rigor Tier-1. Owner ruling required BEFORE execution.

---

### §5.3 FR-E3 [Tier 1] · Historical snapshot posture — re-bless `outer_gate_transform.snapshot.json` or preserve byte-identical?

**Class:** frozen wire contract adjacency (snapshot re-bless discipline) + Standing Rule v3 (on-disk canonical) + audit clarity.

**Question:** `outer_gate_transform.snapshot.json` (NOT one of the 31 frozen-contract snapshots; a `.snapshot.json` transform-golden) contains `feed_id: "citizen_tv_news"` in its `canonical_input`. The snapshot has an explicit re-bless discipline in its test (`test_outer_gate_irreversibility.py:222`: `"outer_gate_transform snapshot drifted; re-bless in review if intentional."`). Does the Fixture Refresh re-bless the snapshot with neutralized `canonical_input` (SHA changes; re-bless discipline honored) OR preserve it byte-identical (assumption: the snapshot's `canonical_input` is an internal test-golden not a runtime-consumed fixture)?

**Also implicitly asks:** historical close reports (`docs/close_reports/*.md`) carry references to broadcaster names as prose. Standing Rule v3 says close reports are on-disk canonical. Does the refresh amend historical closes OR leave them byte-identical (correct-on-sight vs preserve-canonical)?

**Authority-source language (test verbatim):**

> outer_gate_transform snapshot drifted; re-bless in review if intentional.

**Authority-source language (governance Standing Rule v3):** on-disk canonical.

**Options:**

- **α (re-bless the transform-golden · leave historical closes byte-identical):** re-bless `outer_gate_transform.snapshot.json` with neutralized `canonical_input.feed_id` (e.g., `feed_a`) + regenerated egress artifact (via `transform_artifact`). Historical closes stay byte-identical (per Standing Rule v3 on-disk canonical). The re-bless discipline exists FOR THIS PURPOSE.
- **β (preserve everything byte-identical · consumers keep old feed_id literal):** transform-golden snapshot stays; `test_outer_gate_irreversibility.py::canonical` continues using `citizen_tv_news` as the seed literal (isolated test-only usage). Historical closes byte-identical.
- **γ (amend historical closes too):** re-bless snapshot AND amend historical closes to use neutralized names. Violates Standing Rule v3 posture that on-disk canonical should preserve; also creates disclosure drift (close report claims X, actual git-log shows re-write).

**Recommended:** **α (re-bless transform-golden · preserve historical closes byte-identical).** Rationale: (1) the re-bless discipline exists explicitly for intentional drift ("re-bless in review if intentional"); (2) transform-golden is NOT parity-critical (parity counts contract snapshots only); (3) historical close reports are on-disk canonical per Standing Rule v3 — amending them creates historical revisionism; (4) γ violates Standing Rule v3.

**Escalation surface:** frozen wire contract adjacency (snapshot posture) + Standing Rule v3. Full-rigor Tier-1. Owner ruling required BEFORE execution.

---

### §5.4 FR-E4 [Tier 2] · v0 → v1 alias vs v0 → v1 rename semantics (disclosure-only)

**Class:** cost/rework · versioning (governance §2 · additive-only discipline).

**Statement:** the standard v0 → v1 additive pattern (B-5b Ruling E3 γ + P8E-E7 α + CD-E3 α + 9.2a-E1 α) preserves v0 byte-identical and ADDS entries at v1. This Refresh's v1 file will add NEW aliases (`feed_a..feed_j`) as ADDITIONS while ALSO carrying the v0 entries verbatim for transitional compatibility. Under FR-E2 α (centralized), the v1 schema also extends the entry shape to include new fields (`source_standing` + `bucket_category`). This is technically a shape-extension via additive-only, not a rename.

**Expected outcome:** disclosure-only at close; no ruling required. Autonomous decision per Tier-2 discipline.

---

### §5.5 Tier-3 defaults (silent · one-line disclosure at close per governance §3.2)

Format: `[Tier 3 default] {item} → {chosen default} — {one-line rationale}.`

1. **`[Tier 3 default]` v1 registry filename** → `services/service_1/license_classes.v1.json` — matches CD + TF + 9.2a versioning pattern (bump filename, not embedded version-string).
2. **`[Tier 3 default]` Alias key naming scheme** → `feed_a..feed_j` (10 aliases) — matches `region_a..region_g` neutralization pattern from TF Item 3 correction.
3. **`[Tier 3 default]` Adversarial fixture regeneration seed control** → deterministic (fixed random seed in `generate_fixture.py`) — reproducibility across CI runs.
4. **`[Tier 3 default]` Loader migration path** → new `services/service_1/license_class_loader.py` helper reading highest-version-file; consumers migrated from direct-JSON-load to helper (single seam).
5. **`[Tier 3 default]` Test-file rename mechanics** → mechanical `sed`-based literal replacement in each test file; assertion behavior preserved (rename is source-string-only, not semantic).
6. **`[Tier 3 default]` Audio-fixture README (Owner opinion at 9.2a ratification)** → landed at `backend/tests/fixtures/audio/README.md` alongside Fixture Refresh close per Owner "natural slot" suggestion. Dev's judgment: land in this Refresh's atomic commit (not a separate housekeeping).
7. **`[Tier 3 default]` Docs skeleton** → this Stage A + rulings record `docs/rulings/fixture_refresh_fr_e1_to_e3.md` + close report `docs/close_reports/fixture_refresh.md`.

---

## §6. Standing constraints preserved

| Constraint | Attestation planned at Fixture Refresh close |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | `test_v1_g7_attestation_parity_31_at_fixture_refresh_close`. |
| 4-code auth-refusal registry closed | `test_auth_refusal_registry_still_closed_at_four_codes_at_fixture_refresh_close` re-run. |
| E5 no HTTP 409 in refresh new/modified files | grep-negative on all Refresh-touched files. |
| E7 middle-dot / P9-E6 α em-dash | No UI copy at this phase. No enforcement cell. |
| Standing Rule v3 (on-disk canonical) | Historical close reports preserved byte-identical per FR-E3 α. |
| AS-H1 retention held-class (no direct DELETE) | Refresh adds no DELETE handlers. Grep-negative attest. |
| Governance §4.3 promise-naming rule | Each FR-E1..FR-E3 landing carries the promise it protects. |
| **Governance §8 data-blind posture** | Refresh EXECUTES the posture on the identified carriers. |
| **Governance §9 metric-verdict-in-derivation-unit** | Band + verdict rendered in raw LoC per §3 derivation. |
| **Governance §10 9.2 split ruling** | Fixture Refresh is dispatch-independent from 9.2b (venue/deployment/census/BM-V all out of scope). |
| **9.2a-E1 α models_registry seed correction** | Fixture Refresh does NOT touch `models_registry.v0.json`; whisper-tiny CI fixture entry preserved. |
| **CD-E2 ↔ CD-E4 coupling** | Not touched at Fixture Refresh. |

---

## §7. §0.2 Plan-debts status + [OWNER] gates

- **AS-OWN-1** (production object-store choice) — still open, NOT gating this phase; dispatch-independent.
- **9.2-OWN-1..3** — NOT gating Fixture Refresh (per governance §10). Carry to 9.2b unchanged.
- **§3.8 answer fluency** — STILL_QUEUED at BCR §5.1 line 336; not this phase's scope.
- **New [OWNER] gates from Fixture Refresh:** NONE anticipated. FR is dispatch-independent by ruling.

═══════════════════════════════════════════════════════════════════

*End of Fixture Refresh mini-phase Stage A proposal. Standing Rule v3: on-disk canonical. Reply body carries file SHA + line-range map + tier-tagged escalation IDs.*
