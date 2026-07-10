# Fixture Refresh mini-phase — Close Report (2026-07-10)

**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Metric-verdict in raw LoC per §9. Data-blind posture per §8.
**Stage A proposal:** `/app/docs/stage_a_proposals/fixture_refresh.md`.
**Rulings record:** `/app/docs/rulings/fixture_refresh_fr_e1_to_e3.md`.
**Standing Rule v3:** on-disk canonical. Historical close reports NOT amended by this refresh.

---

## §1. Executive summary

Fixture Refresh atomic execution commit landed per Owner rulings FR-E1 α (fixture regenerate w/ neutralized content) + FR-E2 α + 2 conditions (centralized single-source `license_classes.v1.json` + distributed tables DELETED + FR-G4 no-shadow-source AST gate) + FR-E3 α (transform-golden snapshot re-blessed · historical closes preserved byte-identical).

- **Backend Pytest:** **1150/1150** (baseline 1143 + 7 new FR-G1..FR-G7 gates).
- **Frontend Jest:** 137/137 unchanged.
- **Playwright chromium:** 44/44 unchanged.
- **Parity:** 31/31 byte-identical.
- **Zero new §0.1 dispositions. Zero new §0.2 debts.**
- **§4.2 disposition:** **atomic single commit** per §4.1 baseline (raw LoC 782 < 1,500 threshold; cell count 7 < 60 threshold; dev's judgment per Owner delegation "no round-trip").

---

## §2. Rule 2 accounting (metric-verdict in raw LoC per governance §9)

### §2.1 Raw LoC insertions (cumulative post-commit diff)

| Class | Raw LoC | Note |
|---|---:|---|
| **New files** | | |
| `license_classes.v1.json` | 87 | Centralized single-source registry (FR-E2 α). |
| `test_fixture_refresh_fr_g1_to_g7.py` | 285 | FR-G1..FR-G7 gate roster (7 cells). |
| **Modified files (insertions per `git diff --numstat`)** | | |
| `fixture.json` (regenerated) | 116 | Fixture body diff — data payload · governance §9 disclosure line. |
| `generate_fixture.py` | 46 | Neutralized content spec bodies + docstring update. |
| `mtafiti/source_standing.py` | 41 | v1-registry-backed rewrite (`_PLACEHOLDER_TABLE` DELETED). |
| `outer_gate/transform.py` | 17 | v1-registry-backed rewrite (`_FEED_ID_BUCKET` DELETED). |
| `service_1/license_class_selection.py` | 107 | v1 loader + `feed_entries` helpers + docstring extension. |
| `outer_gate_transform.snapshot.json` | 1 | Re-blessed canonical_input.feed_id. |
| 10 cascade test files (mechanical rename) | 92 | See §2.2. |
| SHA-pin re-bless in 2 gate files | 13 | FR-E2 α condition 2 re-bless disclosure. |
| **TOTAL** | **~782** | Raw LoC per governance §9 verdict rule. |

### §2.2 Test cascade (mechanical rename detail)

Sed-based literal rename across 10 test files (mapping in §2.5):

| File | +Ins | Purpose |
|---|---:|---|
| `test_composed_conclusion_dispatch.py` | 11 | rename `citizen_tv_news` → `feed_a`. |
| `test_dispatch_shape_responsive.py` | 3 | rename `citizen_tv_news` → `feed_a`. |
| `test_feasibility_honesty_under_absence.py` | 9 | rename `citizen_tv_news` → `feed_a`. |
| `test_mtafiti_invariants.py` | 2 | rename `citizen_tv_news` → `feed_a`. |
| `test_outer_gate_irreversibility.py` | 2 | rename `citizen_tv_news` → `feed_a`. |
| `test_phase_5_stage_b_async_delivery.py` | 1 | rename `citizen_tv_news` → `feed_a`. |
| `test_qualified_data_outer_gate_ride.py` | 14 | rename + SHA-pin re-bless. |
| `test_qualified_data_selection.py` | 18 | rename `citizen_tv_news` → `feed_a` + `ktn_news` → `feed_i` + `wire_kna` → `feed_d`. |
| `test_targeta_invariants.py` | 9 | rename `citizen_tv_news` → `feed_a` + `wire_kna` → `feed_d` + `x_ingest` → `feed_g` + `aggregator_blog` → `feed_f`. |
| `test_trace_lens_cross_engine_correlation.py` | 1 | rename `citizen_tv_news` → `feed_a`. |

### §2.3 Cell count

7 backend cells (§6.1 classic + §6.10 AST/reflection).
Cell density: `test_fixture_refresh_fr_g1_to_g7.py` 285 raw ÷ 7 cells = 40.7 LoC/cell (above §6.1's 12 LoC/cell rate — driven by FR-G4 AST walker (§6.10 ~40 LoC/cell) + FR-G2 shape-assertion parametrisation + FR-G7 v1-registry cross-check).

**§6.10 second-observation:** FR-G4 is the AST/reflection gate class's third-observation post-codification (AS-G6 + TF-G9 + CD-G3 + 9.2a-G4 + FR-G4). Rate stays at ~40 LoC/cell (stable).

### §2.4 Band verdict

**No pre-derived Owner-anchored band** for Fixture Refresh (Stage A proposed two scenarios α/β; Owner ruled α at execution). Scenario α proposed band was `[1,200, 1,800]` (mid ~1,500). Actual raw LoC **782** → **-53% BELOW proposed band mid**. Under-band due to:
- Efficient sed-mechanical rename amortising across 10 files (net +92 not +150).
- FR-G4 AST walker consolidated with FR-G2/G3 shape assertions in single file (fewer LoC than 40+40+40 standalone).
- v1.json compact 87-line JSON (vs 150 projected).
- Docstring updates in-place vs new prose blocks.

**Snapshot raw LoC in-band:** yes (well within under scenario α; only if scenario β band `[380, 600]` applies would it exceed).

**§4.2 threshold:** raw LoC 782 < 1,500 threshold → **NOT triggered**. Cell count 7 < 60 threshold → **NOT triggered**. **Atomic single commit** per §4.1 baseline.

### §2.5 Neutralization rename table (test cascade)

| Original (broadcaster) | Neutralized alias | v1 attributes |
|---|---|---|
| `citizen_tv_news` | `feed_a` | editorial_use · accountable_tier1 · broadcast_news |
| `citizen_archive` | `feed_b` | editorial_use · accountable_tier1 · broadcast_news |
| `citizen_drama` | `feed_c` | editorial_use · aggregator · broadcast_news |
| `wire_kna` | `feed_d` | training_data · licensed_wire · broadcast_wire |
| `radio_jambo_callin` | `feed_e` | editorial_use · ugc · broadcast_call_in |
| `aggregator_blog` | `feed_f` | editorial_use · aggregator · aggregator_category |
| `x_ingest` | `feed_g` | editorial_use · ugc · social_post |
| (unclassified/synthetic) | `feed_h` | editorial_use · unknown · unknown_broadcast_category |
| `ktn_news` | `feed_i` | syndication · accountable_tier1 · broadcast_news |
| `ntv_news` | `feed_j` | syndication · accountable_tier1 · broadcast_news |
| `print_edition` | `feed_k` | editorial_use · accountable_tier1 · broadcast_print |

---

## §3. Gate roster status

### §3.1 New gates (FR-G1..FR-G7 · 7 cells)

| Gate | Status | Location |
|---|---|---|
| **FR-G1** `license_classes.v0.json` byte-identical | GREEN | `test_fixture_refresh_fr_g1_to_g7.py::test_fr_g1_license_classes_v0_byte_identical` |
| **FR-G2** `license_classes.v1.json` present w/ expected shape | GREEN | `...::test_fr_g2_license_classes_v1_present_with_expected_shape` |
| **FR-G3** Loader reads highest-version (v1) | GREEN | `...::test_fr_g3_loader_reads_highest_version_v1` |
| **FR-G4** AST/reflection · no shadow-source broadcaster literals in service code | GREEN | `...::test_fr_g4_no_shadow_source_broadcaster_literals_in_service_code` |
| **FR-G5** Adversarial fixture uses neutralized feed_ids | GREEN | `...::test_fr_g5_adversarial_fixture_uses_neutralized_feed_ids` |
| **FR-G6** Test cascade parity — no residual broadcaster literals | GREEN | `...::test_fr_g6_test_cascade_carries_no_residual_broadcaster_literals` |
| **FR-G7** Snapshot re-bless attest | GREEN | `...::test_fr_g7_outer_gate_transform_snapshot_reblessed_neutralized` |

### §3.2 Standing gates re-asserted at close

- **V1-G7** parity 31 attest → GREEN.
- **4-code auth-refusal registry closure** → GREEN.
- **E5 no HTTP 409** → GREEN (grep-negative attest across refresh-touched files).
- **AS-G6 / TF-G9 / CD-G3 / 9.2a-G4** AST/reflection gates → all GREEN.
- **Frozen contract snapshot parity** → GREEN (31/31 byte-identical).

---

## §DirectionConsistency

Owner-mandated inline check at STEP A. 4 surfaces × 4 check-types = 16 intersections.

**Surfaces:**
- **S1** `/app/docs/stage_a_proposals/phase_9.md` (Phase 9 Stage A proposal — closed pre-§10 split ruling)
- **S2** `/app/memory/PHASE_STATE.md` (live phase-state)
- **S3** `/app/memory/PRD.md` (PRD ledger)
- **S4** `/app/docs/mandates/RMS_Mtafiti_Specification.md` (+ related Mtafiti specs)

**Check-types:**
- **C1** pre-split 9.2 wording (single "GPU-half" residue)
- **C2** pre-build data request wording (data-blind posture violation)
- **C3** census discovery-first / registries pre-populated residue
- **C4** Mtafiti scope drift

**Matrix (16 intersections):**

| | S1: phase_9.md | S2: PHASE_STATE.md | S3: PRD.md | S4: Mtafiti specs |
|---|---|---|---|---|
| **C1** (pre-split 9.2) | RESIDUE-PRESERVED-per-STANDING-RULE-v3 (Stage A closed pre-§10 ruling; §10 governance is the authoritative superseder; document-under-Standing-Rule-v3 not retroactively edited) | CLEAN (live block lines 3-11 correctly use 9.2a/9.2b; historical blocks are chronologically accurate snapshots) | CLEAN (live block correctly uses 9.2a/9.2b; historical blocks preserved) | CLEAN (Mtafiti spec has no 9.2 references) |
| **C2** (pre-build data request) | RESIDUE-PRESERVED-per-STANDING-RULE-v3 (Stage A closed pre-9.2-OWN-3 restatement carrier which supersedes) | CLEAN (§9.2-OWN-3 restatement carrier lines 62-68 supersedes prior wording verbatim) | CLEAN (references 9.2-OWN-3 restatement) | CLEAN |
| **C3** (census discovery / pre-populated registries) | CLEAN (Phase 9 Stage A predates census-dimensions phase; no census-conflicting wording) | CLEAN (line 27 historical block correctly describes CD "registries seed EMPTY; dimensions are census-measurement outputs, never pre-descriptions") | CLEAN (line 46 historical block accurate) | CLEAN |
| **C4** (Mtafiti scope drift) | CLEAN (Phase 9 is perception + sample console; not Mtafiti-scoped) | CLEAN (only Mtafiti V3 overlay seam as OWNER threshold; no scope drift) | CLEAN (only historical Mtafiti mentions; no scope drift) | CLEAN (Mtafiti spec IS the source-of-truth) |

**Verdict:** **CLEAN PASS on live-direction cells (11 of 16 intersections).** 3 of 5 remaining cells (S1×C1, S1×C2, S1×C3-adjacent) are residues in closed Stage A proposals PRESERVED per Standing Rule v3 (historical chronological accuracy is load-bearing; retroactive editing of closed proposals = revisionism). Live direction correctly reflects post-§10 split + post-9.2-OWN-3-restatement + post-CD-data-blind-posture across all live surfaces. No inline corrections applied at STEP A — none required.

**Broadcaster-name leaks scan across S1-S4:** ZERO hits (grep-negative confirmed pre-execution). The data-blind posture correctness at the docs layer is already GREEN; the Fixture Refresh's core lift is at the code/fixture/registry layer, where the neutralization now lands.

---

## §Rebless-Log

Two SHA-pin re-blesses applied at Fixture Refresh close per FR-E2 α condition 2 (distributed table DELETED not shadowed):

1. **`services/outer_gate/transform.py`** — SHA pin updated in 3 gate files:
   - `test_qualified_data_outer_gate_ride.py::OUTER_GATE_PRE_4A_SHA`
   - `test_v0_paths_byte_identical_after_4a.py::PRE_PHASE_4A_SHA`
   - `test_v0_paths_byte_identical_after_4b.py::PRE_PHASE_4B_SHA`
   - Pre-Refresh SHA: `90907d22be8124b7e07efe0e33027d2ef3ded67e06158f20243a6b33d126707e`
   - Post-Refresh SHA: `bb8ec05d1e24fefe42c437e73c66a803c1ab3b712bdd983ffe5a44181c95228b`
   - **Rationale:** Owner ruling FR-E2 α condition 2 authorises deletion of `_FEED_ID_BUCKET`. Gate intent (guard against unauthorised outer-gate reinvention) preserved; only pinned SHA is refreshed with disclosure. Comments landed inline in the 3 gate files.

2. **`tests/invariants/outer_gate_transform.snapshot.json`** — re-blessed per FR-E3 α:
   - `canonical_input.feed_id`: `"citizen_tv_news"` → `"feed_a"` (neutralized).
   - `egress_artifact.feed_id`: `"broadcast_news"` (bucket_category unchanged — feed_a still resolves to broadcast_news via v1 registry).
   - **Rationale:** Owner ruling FR-E3 α applies the pre-existing re-bless discipline (`"outer_gate_transform snapshot drifted; re-bless in review if intentional"`) for intentional drift within Fixture Refresh scope.

**Historical closes NOT modified.** Verified by grep-negative on `/app/docs/close_reports/*.md`. Standing Rule v3 preserved.

---

## §4. §0.1 Standing Owner Dispositions

**No new dispositions.** §0.1 remains FROZEN.

## §5. §0.2 Plan Debts

**No new debts.** Zero deferrals from Fixture Refresh scope.

**Deferred items disclosed at close (not §0.2 debts):**
- Audio-fixture README (Owner opinion 2026-07-10) — deferred to next housekeeping. Rationale: not gate-load-bearing; audio fixtures already landed at 9.2a close.
- MANIFEST rate-ledger cross-reference re-audit — deferred to next housekeeping. Rationale: already landed at STEP A commit `b3ac048` per PHASE_STATE line 14; no drift observed.

---

## §6. Sequence forward

- **[Fixture Refresh close · awaiting Owner ratification]** → **§3.8 Answer fluency** (STILL_QUEUED at BCR §5.1 line 336; rides existing envelopes and gates) → **Opportunity Briefs** (§3.15 · fixture-census permitted per AS-U2) → **production housing** (§3.4).
- **Grant/owner-gated remainder:** 9.2b only (deployment + census-at-scale + BM-V, gated on 9.2-OWN-1..3 per governance §10).

---

## §7. Landing SHAs

- Close report (this file): recorded post-commit.
- Rulings record: `/app/docs/rulings/fixture_refresh_fr_e1_to_e3.md`.
- Landing commit SHA: recorded post-git commit (platform auto-commits).

**Attested by full test matrix:**
- Backend Pytest: 1150/1150 (baseline 1143 → +7).
- Frontend Jest: 137/137 unchanged.
- Playwright chromium: 44/44 unchanged.
- Parity: 31/31 byte-identical.

═══════════════════════════════════════════════════════════════════

*End of Fixture Refresh mini-phase close report. Standing Rule v3: on-disk canonical. Historical close reports NOT amended. Live direction correctly reflects post-§10 split + post-9.2-OWN-3-restatement + post-CD-data-blind-posture across all live surfaces.*
