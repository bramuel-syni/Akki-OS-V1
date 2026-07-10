# Census-dimensions mini-phase · Close Report (Owner Message 565 · CD-E1..CD-E4)

**Close date:** 2026-07-10
**Sequence position:** post-TF-ratification (Owner Message 565); ahead of Phase 9 Stage B; ahead of Opportunity Briefs; ahead of Answer fluency (§3.8).
**Dispatch discipline:** §4.1 baseline single atomic first-commit under 3-tier governance model.
**Standing Rule v3:** on-disk canonical. Reply body carries SHA + tier tags only.
**Parent chain:** `a73a3ea` (Stage A) → `93334fb` (STEP A housekeeping) → `7a5f3bd` (TF close) → this atomic execution commit.

---

## §1. Artefact map (SHA-256 anchored)

### §1.1 New files landed at Census-dimensions

| Path | SHA-256 | LoC (raw / lloc) | Purpose |
|---|---|---:|---|
| `backend/services/census_dimensions/__init__.py` | `4dc998793c795840ad90bc59954283d8d3d14a34e9ea112a163698c6ac1b8594` | 50 / 26 | Package barrel + Owner-verbatim carrier for CD-E1..CD-E4 rulings. |
| `backend/services/census_dimensions/dimensions_loader.py` | `08b1d03a1e2c655c46e213094861a85addbda3e42062f9d6ae7492db11d5e7da` | 132 / 76 | Registry version discovery + `register_observation` (additive v(N)→v(N+1) bump) + `validate_content_surface` / `validate_genre` (pure check). |
| `backend/services/census_dimensions/dimensions_service.py` | `d5f2eb1b61c97434b1da771025b801935a2d54f24d563523b7462ef486d4e9a2` | 189 / 104 | `CensusContentDimension` Pydantic runtime validator (UNFROZEN per CD-E2 α ↔ CD-E4 coupling) + symmetric contradiction validator (CD-E1 α) + `record_census_dimension` register-before-validate orchestration (CD-E3 α) + `read_census_dimensions_for_feed` + `list_registry`. |
| `backend/services/census_dimensions/census_content_surfaces.v0.json` | `c91bbd2a06275b38d0646a88b7c35f170d897c8b3168dba88457fa976fafee19` | 6 / 6 | Registry seed v0 — EMPTY per data-blind posture governance §8. |
| `backend/services/census_dimensions/census_genres.v0.json` | `0aac507cc3367f5a98f97dc3e4baccaaa3db193076b105557b0b7b49af307452` | 6 / 6 | Registry seed v0 — EMPTY per data-blind posture governance §8. |
| `backend/routers/census_dimensions.py` | `4876424f8876d3e3784fa96c3c69716994da4746b5c67d59a0bc2fdd32841a32` | 55 / 36 | Read-only router: `GET /api/census/dimensions/{feed_id}` + `GET /api/census/dimensions/registry/{kind}`. No POST/PUT/DELETE (census-run-only writes via in-process service call). |
| `backend/tests/invariants/test_census_dimensions.py` | `0b4aecbd503e418f265ba041e9b0a907ef561d6e18ccde59efe1a5efb2375f7d` | 382 / 241 | CD-G1 (three-op signatures + registries seed EMPTY) + CD-G2 (symmetric contradiction × both directions) + CD-G4 (registration-path cell × sync + E2E async httpx) + V1-G7 parity 31 attest + 4-code auth registry re-attest + E5 no-409 attest. |
| `backend/tests/invariants/test_census_dimensions_wire_shape.py` | `d1f9f4cdaf8a2e6089c41b3dce903b276c7a90e34c8f4ae5812ec3c6d6863fe3` | 141 / 77 | CD-E4 α load-bearing wire-shape gate — 5 pinned governance-key fields + tolerance clause for additive fields. |
| `backend/tests/invariants/test_census_dimensions_ast_gate.py` | `6d777724966669a8f091ce9329a295442b1d157bbadc98d5dd12d8531042e2bb` | 128 / 94 | CD-G3 AST/reflection gate (§6.10 rate class) — no in-code hard-coded dimension values in production paths + no direct Mongo write bypasses `record_census_dimension`. Two reflection cells. |
| `docs/rulings/census_dimensions_cd_e1_to_e4.md` | *(SHA at commit-time)* | — | Owner rulings CD-E1..CD-E4 verbatim + CD-E2 ↔ CD-E4 coupling clause verbatim. |
| `docs/close_reports/census_dimensions.md` (this file) | *(SHA at commit-time)* | — | Close report. |

### §1.2 Modified files at Census-dimensions

| Path | Delta | Purpose |
|---|---|---|
| `backend/server.py` | +8 LoC | Mount `routers/census_dimensions.py` under `/api` prefix + startup index creation on `census_content_dimensions` (unique on `feed_id`). |
| `memory/PHASE_STATE.md` | *(landed at STEP A `93334fb`; further updated at this close)* | Live-state transition to CD RATIFIED post-close. |
| `memory/PRD.md` | *(landed at STEP A `93334fb`; further updated at this close)* | Current-gate status transition. |

### §1.3 v0 byte-identity attestation

31 pre-existing snapshots preserved byte-identical (V1-G7 attested at 31 unchanged). **NO new frozen contracts landed** per CD-E2 α ↔ CD-E4 coupling ruling — parity stays 31/31 byte-identical.

---

## §2. Gate roster verification

| Gate | Cell(s) | Result |
|---|---|---|
| **CD-G1** Registries seed EMPTY at v0 + three-op sidecar signatures | `test_cd_g1_registries_seed_empty_at_v0` + `test_cd_g1_three_op_sidecar_signatures_present` | ✅ GREEN (2 cells) |
| **CD-G2** Symmetric contradiction validator (both directions rejected) | `test_cd_g2_contradiction_value_present_source_null` + `test_cd_g2_contradiction_value_null_source_present` + `test_cd_g2_contradiction_both_absent_accepted` + `test_cd_g2_contradiction_both_present_accepted` + `test_cd_g2_contradiction_applies_to_both_dimension_pairs` + `test_cd_g2_source_literal_closed_at_two` | ✅ GREEN (6 cells) |
| **CD-G3** AST/reflection gate — no hard-coded dimension values + no direct Mongo write bypass | `test_cd_g3_no_hardcoded_dimension_values_in_production_paths` + `test_cd_g3_no_direct_mongo_write_bypasses_service` | ✅ GREEN (2 reflection cells; §6.10 rate class applied) |
| **CD-G4** Registration-path cell — census_observed register-before-validate + manifest_declared hard-fail | `test_cd_g4_census_observed_novel_value_registers_and_writes` + `test_cd_g4_manifest_declared_novel_value_hard_fails` + `test_cd_g4_register_observation_idempotent_by_value` + `test_cd_g4_registry_history_is_audit_trail` + `test_cd_g4_e2e_record_census_dimension_registers_and_persists` (async httpx) + `test_cd_g4_e2e_manifest_declared_novel_hard_fails` (async httpx) + `test_cd_g4_e2e_manifest_declared_existing_value_writes` (async httpx) | ✅ GREEN (7 cells; 3 async httpx observations — see §4.1 watched rate class) |
| **Wire-shape gate** (CD-E4 α · 5 governance-key fields + additive tolerance) | `test_cd_e4_five_governance_key_fields_pinned_by_name` + `test_cd_e4_pinned_fields_required_flag` + `test_cd_e4_source_fields_are_optional_literal_of_two` + `test_cd_e4_tolerance_additive_fields_do_not_reject_gate` + `test_cd_e4_pinned_fields_type_annotations_stable` | ✅ GREEN (5 cells) |
| **V1-G7** Parity 31 attest (unchanged — CD-E2 α ↔ CD-E4 coupling · no additions) | `test_v1_g7_attestation_parity_31_at_census_dimensions_close` | ✅ GREEN |
| **4-code auth-refusal registry closure** re-attest | `test_auth_refusal_registry_still_closed_at_four_codes_at_cd_close` | ✅ GREEN |
| **E5** no HTTP 409 in CD new files | `test_no_http_409_in_census_dimensions_new_files` | ✅ GREEN |

**Backend CD cell count total: 25.**

**Frontend cells: 0** (no UI surface at this mini-phase; sidecar is consumed by Mtafiti Registry admin views already landed at Phase 9 Sub-stage 9.1).

---

## §3. LoC / cell actuals vs Owner-anchored band

### §3.1 Cell count

| Bucket | Proposal projection | Actual | Delta |
|---|---:|---:|---:|
| Backend Pytest classic-amortised cells (§6.1) | 8 | 15 | +7 (+88%) |
| Backend Pytest AST/reflection cells (§6.10) | 1 | 2 | +1 (+100%) |
| Backend Pytest async httpx cells (watched §6.8) | ≤3 | 3 | 0 |
| CD-E4 wire-shape gate cells | (bundled) | 5 | + explicit |
| **Total backend cells** | **12 (projection)** | **25** | **+13 (+108%)** |

Cell-count overage is transparent: the projection counted the wire-shape gate as a single "cell", the AST gate as one cell, and CD-G2 as one cell. Actual landing enumerates the invariants at the sub-cell level (6 CD-G2 cells enumerating the closed 2-set + both-absent + both-present axes; 5 wire-shape gate cells enumerating field presence + required flag + Literal args + tolerance + type stability; 2 AST cells enumerating hardcoded-value scan + direct-Mongo-write scan). Enumeration is a cost/rework class (Tier 2) — disclosure, not blocking.

### §3.2 LoC actuals

| Line-item | Basis | Projected | Actual (raw / lloc) |
|---|---|---:|---:|
| Service module (`__init__` + loader + service) | §6.3 (~180) | ~180 | 371 / 206 |
| Router endpoints × 2 | §6.2 (2 × 40) | ~80 | 55 / 36 |
| 2 registry JSONs (empty seeds) | flat | ~10 | 12 / 12 |
| 15 classic Pytest cells (shared-helper amortised §6.1) | 15 × 12 | ~180 | (part of test files) |
| 2 AST/reflection gate cells (§6.10) | 2 × 40 | ~80 | 128 / 94 |
| 3 async httpx E2E cells (watched §6.8) | 3 × 25 | ~75 | (part of test files) |
| 5 wire-shape gate cells (post-hoc explicit) | ~28/cell | (bundled) | 141 / 77 |
| Verbatim carrier for Owner text (§6.9) | 1 carrier ~40 | ~40 | ~120 (across 3 modules) |
| **Total backend + tests (new files)** | — | **~671** (with docs ~150) | **1,089 raw / 666 lloc** |

### §3.3 Band verdict (governance §2.2 · Tier-2 miss = disclosure not blocking)

- **Owner-anchored band:** `[500, 750]` LoC (mid ~625; Owner rulings note: "E1 ~+5 LoC, E3 ~+30–50 — inside [500, 750] expected; disclose actual at close").
- **Raw LoC actual: 1,089** → +45.2% ABOVE top-of-band.
- **LLoC actual: 666** → **WITHIN BAND** (89% of top-of-band; -11.2% below top-of-band).
- **snapshot_lloc_in_band: yes** (LLoC-based verdict).
- **snapshot_raw_in_band: no** (raw-based verdict; +45% over).

**Overage composition (honest attribution per Ruling 5):**
1. **Verbatim carriers (~§6.9 rate class applied 3 modules × ~40 raw each = ~120 raw):** `__init__.py` + `dimensions_loader.py` + `dimensions_service.py` each carry Owner-verbatim CD-E1..CD-E4 ruling text as module docstrings for on-disk audit clarity. This is standard §6.9 behaviour — the raw/LLoC gap widens by ~44 LoC of verbatim text per module.
2. **AST reflection gate double-cell:** 128 raw / 94 lloc for 2 cells → ~64 raw/cell → deviation vs §6.10 40 LoC/cell (>±30% band). Composition: whitelist logic + violation formatter × 2 invariants (hardcoded-value scan + direct-Mongo-write scan). Disclose per §6.10 deviation clause.
3. **Test file docstring density:** `test_census_dimensions.py` at 382 raw / 241 lloc — the ~1.6× raw/lloc ratio is typical for Pytest cells with explanatory docstrings + Owner-ruling citations.
4. **Wire-shape gate landed as 5 sub-cells rather than 1 bundled cell:** Ruling 5-consistent enumeration; each pinned invariant tested as its own cell for post-hoc audit clarity.

**Deviation from watched §6.8 async httpx class:**
- 3 async httpx cells landed at empirical rates ~25 LoC/cell as predicted. **This is the second observation of the async httpx rate class** (first was AS-close). Per Ruling 5, the async httpx cell rate is eligible for codification via a companion Stage A rate note at next appropriate housekeeping dispatch. Watched rate class §6.8 accordingly.

### §3.4 §4.2 threshold trigger status

| Threshold | Value | Trigger? |
|---|---:|---|
| §4.2 pre-authorized LoC split | 1,500 | **NO** (1,089 < 1,500 · single commit acceptable) |
| §4.2 pre-authorized cell split | 60 | **NO** (25 < 60) |

Single atomic commit for surface coherence per §4.1. No split-disposition invoked.

---

## §4. Rate-class observations

### §4.1 Watched: async httpx backend Pytest cells (§6.8)

- **AS-close observation (2026-07-08):** ~25 LoC/cell empirical.
- **CD-close observation (2026-07-10):** 3 async httpx cells landed at ~25 LoC/cell empirical (matches AS).
- **Codification eligibility:** SECOND observation confirmed → per Ruling 5, this class is now eligible for codification (§6.11 or replacement of §6.8) at next housekeeping dispatch. Owner discretion whether to codify by retrospective (Message-565-style) or wait for a third natural observation.

### §4.2 Codified rates applied at CD execution

| Rate | Applied | Deviation? |
|---|---|---|
| §6.1 backend Pytest shared-helper amortised (12 LoC/cell) | 15 classic cells | Within band |
| §6.2 backend endpoint impl 3-share (40 LoC/endpoint) | 2 endpoints | Within band |
| §6.3 backend service module standalone (100 LoC/module) | 3 modules (bundled) | Within band |
| §6.6 frozen Pydantic contract class (60 LoC/class) | N/A — no new contract | — |
| §6.7 frozen contract snapshot JSON (~155 LoC/snapshot) | N/A — no new snapshot | — |
| **§6.9 Verbatim-carrier overhead (~100-150 LoC/carrier)** | 3 carriers at ~40 raw each (~120 total) | **Below band** (~40 vs 100-150) — carriers landed compact because Owner ruling text was itself compact per ruling. Deviation disclosed per §6.9 deviation clause. |
| **§6.10 AST/reflection gate class (~40 LoC/cell)** | 2 cells at ~64 raw each | **Above band** (>+30% deviation). Whitelist + violation formatter × 2 distinct invariants. Deviation disclosed per §6.10 deviation clause. |

---

## §5. Parity 31 attestation (CD-E2 α ↔ CD-E4 coupling)

- **Parity at close:** 31/31 byte-identical (V1-G7 attested via `test_v1_g7_attestation_parity_31_at_census_dimensions_close`).
- **No new frozen contracts:** `CensusContentDimension` is a Pydantic runtime validator (UNFROZEN); no snapshot; parity unchanged.
- **Coupling clause carried forward:** `docs/rulings/census_dimensions_cd_e1_to_e4.md` §2 records the CD-E2 ↔ CD-E4 anti-regression discipline verbatim.

---

## §6. Standing constraints attested at close

| Constraint | Attestation |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical | `test_v1_g7_attestation_parity_31_at_census_dimensions_close` ✅ |
| 4-code auth-refusal registry closed | `test_auth_refusal_registry_still_closed_at_four_codes_at_cd_close` ✅ |
| E5 no HTTP 409 in CD new files | `test_no_http_409_in_census_dimensions_new_files` ✅ |
| AS-H1 no DELETE handlers | Router file grep-negative on `@router.delete` / `HTTP_METHODS=["DELETE"]` — 0 hits (router lands only GET) ✅ |
| Standing Rule v3 (on-disk canonical) | This close + rulings + Stage A all on disk ✅ |
| Governance §8 data-blind posture load-bearing | CD-G1 (registries seed EMPTY) + CD-G2 (sidecar accepts null dimensions) + CD-G3 (registry-superset via AST + runtime) + CD-G4 (register-before-validate) ✅ |
| Governance §4.3 promise-naming rule | Each CD-E1..CD-E4 ruling carries the promise it protects (see rulings record) ✅ |

---

## §7. Test suite results at close

| Suite | Pre-CD | Post-CD | Δ | Result |
|---|---:|---:|---:|---|
| Backend Pytest (`pytest -q`) | 1,089 | **1,114** | **+25** | ✅ GREEN |
| Frontend Jest (`ui_spec_v1`) | 137 | **137** | 0 | ✅ GREEN (22 suites; no frontend at CD) |
| Playwright chromium (`test:e2e --project=chromium`) | 44 | **44** | 0 | ✅ GREEN |

Parity 31/31 byte-identical.

---

## §8. Tier-3 defaults (one-line disclosures per governance §3.2)

Format: `[Tier 3 default] {item} → {chosen default} — {one-line rationale}.`

1. **`[Tier 3 default]` Module layout** → `backend/services/census_dimensions/` — matches `services/transform_forms/` + `services/artifact_store/` conventions.
2. **`[Tier 3 default]` Registry filenames** → `census_content_surfaces.v0.json` + `census_genres.v0.json` — matches `defensibility_classes.v0.json` from TF + `disclosure_types.v0.json` from B-5b.
3. **`[Tier 3 default]` MongoDB collection name** → `census_content_dimensions` — matches TF close §6.1 verbatim.
4. **`[Tier 3 default]` MongoDB index** → unique index on `feed_id` (via startup `create_index`).
5. **`[Tier 3 default]` Router path** → `/api/census/dimensions/*` — surface concept is "census outputs", not "Mtafiti internals" (CD-E5 disclosure).
6. **`[Tier 3 default]` No frontend surface** → sidecar is read via existing Mtafiti Registry admin views (Phase 9 Sub-stage 9.1); no new UI cells this mini-phase.
7. **`[Tier 3 default]` Registry versioning mechanism** → additive vN → v(N+1) file writes; v(N) preserved byte-identical; new version carries `extends: "v{N}"` + `added_value` + `added_source` fields for on-disk audit trail per Owner CD-E3 α.
8. **`[Tier 3 default]` Persistence idempotency** → `record_census_dimension` uses `update_one({"feed_id": ...}, {"$set": ...}, upsert=True)` for idempotency by feed_id.
9. **`[Tier 3 default]` Upsert semantics** → re-records over existing feed_id at same key; register-before-validate re-checks vocabulary on every write.
10. **`[Tier 3 default]` MANIFEST rate-ledger cross-reference (Owner Message 565 · Tier-3 builder's judgment)** → **DEFERRED** to a later housekeeping dispatch. Rationale: this atomic commit already runs at +45% raw / -11% lloc vs band; adding a MANIFEST edit compounds the boundary-crossing without clarity gain — deferral preserves this close as scoped, and the rate-ledger cross-reference can land alongside the async-httpx codification housekeeping when that observation-set closes.

---

## §9. §0.1 Standing Dispositions / §0.2 Plan Debts

- **§0.1 FROZEN** — zero new Standing Dispositions at CD.
- **§0.2** — zero new Plan Debts at CD.
- **AS-OWN-1** (production object-store choice) — still open; dispatch-independent; CD uses Mongo (same as `mtafiti_registry`), no artifact-store dependency.
- **9.2-OWN-1..3** — in-motion Owner-side; CD is dispatch-independent (the SHAPE of the sidecar landed here; the POPULATION of the sidecar happens at Phase 9 census run per Owner-ratified data-blind posture governance §8).
- **§3.8 answer fluency** — STILL_QUEUED at BCR §5.1 line 336 per Owner Message 565 status check (this close does NOT re-open the queue).

---

## §10. Sequence position + downstream unlock

| Item | Status |
|---|---|
| Census-dimensions mini-phase (this close) | **CLOSED (awaiting Owner ratification).** |
| Phase 9 Stage B (Extraction GPU half) | Dispatch-independent of Census-dimensions; subject to 9.2-OWN-1..3 (Owner-side). Census-run integration will call `record_census_dimension(...)` in-process at census execution time. |
| Opportunity Briefs (§3.15) | Queued post-Phase-9 Stage B; requires populated Registry (fixture-census demo permitted per AS-U2). |
| Answer fluency (§3.8) | STILL_QUEUED at BCR §5.1 line 336 (post-B-5b; rides existing envelopes and gates). |
| Production housing (§3.4) | Queued post-Opportunity-Briefs. |
| AS-OWN-1 (production object-store choice) | Still open; adapter seam dispatch-independent. |

---

## §11. Watched rate observations for downstream Stage A authors

- **§6.8 async httpx watched → SECOND observation confirmed at CD.** Eligible for codification. AS + CD both landed ~25 LoC/cell.
- **§6.9 verbatim-carrier deviation:** landed below band (~40 vs 100-150) — Owner ruling text was compact; disclosed per deviation clause. Next Stage A with 4+ verbatim blocks in one module may land on the heavy side of §6.9's ~100-150 range; symmetric disclosure applies.
- **§6.10 AST/reflection gate deviation:** landed above band (~64 vs 40) — whitelist + violation formatter for a 2-invariant gate composed with a single walker skeleton. Reflection gates with combined-invariant walkers are eligible for a companion sub-rate note if the pattern recurs.

═══════════════════════════════════════════════════════════════════

*End of Census-dimensions mini-phase close report. Standing Rule v3: full text on disk. Reply body = SHA + tier tags + band-actual + gate roster + coupling clause. Awaits Owner ratification.*
