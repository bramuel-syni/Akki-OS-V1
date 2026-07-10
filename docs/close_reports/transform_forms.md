# Transform Forms · Close Report (BCR §3.7 · Knowledge Artifact + Callable Skill)

**Close date:** 2026-07-09
**Sequence position:** BCR §5.1 line 315 · post-Artifact-Store · active lane per Owner update.
**Dispatch discipline:** §4.1 baseline single atomic first-commit under 3-tier governance model.
**Standing Rule v3:** on-disk canonical. Reply body carries SHA + tier tags only.

---

## §1. Artefact map (SHA-256 anchored)

### §1.1 New files landed at Transform Forms

| Path | SHA-256 | LoC | Purpose |
|---|---|---:|---|
| `backend/contracts/knowledge_artifact_v0.py` | `9ba68a3645e84d6d8fe49fcc7bf2a6288591469cbf8bee219f80d3e438b95c5d` | 134 | TF-E1 α: `KnowledgeArtifactV0` frozen contract + nested `KnowledgeArtifactNode` + `KnowledgeArtifactEdge` sub-models. |
| `backend/tests/invariants/knowledge_artifact_v0.contract_snapshot.json` | `5fa711f3049d8093938537afda44917464ffc2035c4fbde24945863b970e6eb9` | 146 | KA v0 JSON Schema snapshot (sub-models under `$defs`). |
| `backend/contracts/callable_skill_provisioning_v0.py` | `d61a446c9ba130347320085b3de95f198c2e5bb7d1503c3af524a7b1535fa391` | 101 | TF-E2 α: `CallableSkillProvisioningV0` frozen contract with `ConfigDict(frozen=True)` per TF-E4 (b) β. |
| `backend/tests/invariants/callable_skill_provisioning_v0.contract_snapshot.json` | `d173e0d187707a0c2721c1ef8462cc183ab0ff65a23d7daf3814687bce0d5ec9` | 71 | Callable Skill provisioning JSON Schema snapshot. |
| `backend/services/transform_forms/__init__.py` | `f565b61e57d6855b06e3e71952d3e3c48d7a2b74aaee673d210214292ab7e074` | 33 | Package barrel. |
| `backend/services/transform_forms/defensibility_classes.v0.json` | `8d492442c897006a403dc7f9852b05c06cabad46ff5daab170b3e30b2f0355d4` | 19 | TF-E3 α condition: canonical registry seeded VERBATIM from live composition path vocabulary `{fact, utterance, non_factual}`. |
| `backend/services/transform_forms/defensibility_loader.py` | `9f751ed31a1eea0e54b2be2b8222ac7631113f1eaddf626bbb2f28f84c1c8135` | 54 | Registry loader + validator (`validate_defensibility_class`). |
| `backend/services/transform_forms/knowledge_artifact.py` | `067b4bcf3c271cb0708a0c8e29c20e4964ba6d056936b2a234b7b6fe42429ca1` | 75 | KA assembly service (`build_knowledge_artifact`). |
| `backend/services/transform_forms/callable_skill_gate.py` | `02d5674517a804eb93ba5c8b1ab1d64368294650294a3a32a6164396c99b3871` | 144 | TF-E4 (a) α · per-call inner gate decorator + response class-inline mutation + refusal envelope. |
| `backend/services/transform_forms/callable_skill_persistence.py` | `0590339f1efe1bb5944aeba57037f9fa27dae71cb7eb116565f1792227a5c428` | 111 | TF-E4 (b) α · `insert_one`-only provisioning + `update_one`-on-`revoked_at`-ONLY revocation. |
| `backend/routers/transform_forms.py` | `7ae5382f5676406450f3c77e525140f08dda70ade5c03d7506e5ee9a95e0b099` | 124 | Router: KA produce + skill provision + skill query. |
| `backend/tests/invariants/test_transform_forms.py` | `cdefaf7578a21ec42777e2f32f01893366b8a464836896c77f4c707fc445150e` | 422 | 21 cells: TF-G1..G9 + V1-G7@31 + v0 preservation + 4-code + E5 no-409 + KA assembly smoke. |
| `docs/rulings/transform_forms_tf_e1_to_e4.md` | *(SHA at commit-time)* | 108 | Owner TF-E1..E4 verbatim rulings on-disk. |
| `docs/close_reports/transform_forms.md` (this file) | *(SHA at commit-time)* | — | Close report. |

### §1.2 Modified files at Transform Forms

| Path | Δ LoC | Purpose |
|---|---:|---|
| `backend/server.py` | +5 | Mount `transform_forms_router` on `/api`. |
| `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` | +2 | Add KA v0 + CallableSkillProvisioning v0 to `CONTRACT_TO_SNAPSHOT` map. |
| `backend/tests/invariants/test_8_ext.py` | +1 −1 | Parity assertion 29 → 31 (running total post-Artifact-Store + TF). |
| `backend/tests/invariants/test_composed_conclusion_v0_contract_frozen.py` | +1 −1 | Parity 29 → 31. |
| `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` | +1 −1 | Parity 29 → 31. |
| `backend/tests/invariants/test_phase_7_stage_b_3_wizard.py` | +1 −1 | Parity 29 → 31. |
| `backend/tests/invariants/test_phase_9_sub_stage_9_1_and_9_3.py` | +1 −1 | Parity 29 → 31. |
| `backend/tests/invariants/test_artifact_store.py` | +7 −3 | AS-close parity assertion 29 → 31 with docstring note about running total. |
| `backend/tests/invariants/feasibility_fixture_augmentation.json` | +1 −1 | **Fixture audit (Item 3):** 8 content-type-loaded region names neutralized to content-neutral placeholders (`region_a..region_g` + `unclassified`). Per Owner data-blind posture 2026-07-09. |
| `docs/governance/tiered_ruling_model.md` | +14 | **Item 1:** §8 data-blind posture verbatim carrier landed. |
| `memory/PHASE_STATE.md` | +9 −1 | **Item 2:** 9.2-OWN-3 restatement (post-census validation slice only). |
| `memory/PRD.md` | +1 −1 | **Item 2:** 9.2-OWN-3 pointer to PHASE_STATE carrier. |

### §1.3 v0 byte-identity attestation

29 pre-TF snapshots preserved byte-identical (attested by `test_v0_paths_byte_identical_at_transform_forms_close` GREEN). Parity moves from 29 → 31 (+2 additive: KA v0 + CallableSkillProvisioning v0). No pre-existing contract mutated.

---

## §2. Gate roster verification

| Gate | Cell(s) | Result |
|---|---|---|
| **TF-G1** KA v0 frozen + snapshot at parity 30 | `test_tf_g1_ka_v0_frozen_and_snapshot_present` | ✅ GREEN |
| **TF-G2** Callable Skill frozen + snapshot at parity 31 | `test_tf_g2_callable_skill_provisioning_frozen_config` + `test_tf_g2_callable_skill_provisioning_shape_matches_bcr_verbatim` + `test_tf_g2_provisioning_frozen_hardening_raises_on_mutation` | ✅ GREEN (3 sub-cells) |
| **TF-G3** Every KA node carries class + trace_id inline | `test_tf_g3_every_ka_node_has_class_and_trace_id_inline` + `test_tf_g3_ka_construction_requires_class_and_trace_id` | ✅ GREEN (2 sub-cells) |
| **TF-G4** Below-floor → refusal envelope | `test_tf_g4_below_floor_response_raises_refusal` + `test_tf_g4_at_or_above_floor_returns_mutated_response` | ✅ GREEN (2 sub-cells) |
| **TF-G5** Slice-freeze immutability (ConfigDict(frozen=True) attest) | `test_tf_g5_slice_bound_at_freeze_no_mutation` | ✅ GREEN |
| **TF-G6** Relation Literal closed at 3 values | `test_tf_g6_relation_literal_closed_at_three` | ✅ GREEN |
| **TF-G7** Per-response class inline | `test_tf_g7_skill_query_response_has_class_inline` | ✅ GREEN |
| **TF-G8** Registry ⊇ live composition vocabulary (TF-E3 α condition) | `test_tf_g8_defensibility_registry_superset_live_composition_path` + `test_tf_g8_no_second_vocabulary_diverges_from_registry` + `test_tf_g8_validate_rejects_unknown_class` | ✅ GREEN (3 sub-cells) |
| **TF-G9** No `update_one` touches `corpus_slice_ref` (AST scan · TF-E4 (b) α) | `test_tf_g9_no_update_one_touches_corpus_slice_ref` | ✅ GREEN |
| **V1-G7** Parity 31 attest + KA + CallableSkillProvisioning additive | `test_v1_g7_attestation_parity_31_byte_identical_at_transform_forms_close` + `test_v0_paths_byte_identical_at_transform_forms_close` | ✅ GREEN (2 cells) |
| 4-code auth-refusal registry closed | `test_auth_refusal_registry_still_closed_at_four_codes_at_tf_close` | ✅ GREEN |
| E5 no HTTP 409 in TF new files | `test_no_http_409_in_transform_forms_new_files` | ✅ GREEN |
| KA assembly smoke (E2E) | `test_ka_assembly_smoke_end_to_end` + `test_ka_assembly_rejects_unknown_class` | ✅ GREEN (2 cells) |

**Backend TF cell count total: 21.**

**Frontend cells: 0** (per TF-R3 verbatim: grain-compatibility matrix already encodes both forms; wizard offerability opens as config, not build).

---

## §3. LoC / cell actuals vs Owner-anchored band

### §3.1 Cell count

| Bucket | Proposal projection | Actual | Delta |
|---|---:|---:|---:|
| Backend Pytest cells | 12 | 21 | +9 (+75%) |
| Frontend Jest cells | 0 | 0 | 0 |
| Playwright chromium | 0 | 0 | 0 |
| **Total** | **12** | **21** | **+9** |

Cell overshoot drivers (per proposal §1.4 watched-rate observation slots):
- **TF-E3 α condition:** owner explicitly said "~+1 cell disclosed at close" → actual is +3 sub-cells for TF-G8 (registry-superset + second-vocabulary + validator rejection).
- **TF-E4 (b) α + β:** owner said "belt-and-suspenders" → +1 cell for `test_tf_g5_slice_bound_at_freeze_no_mutation` (already in proposal) + +1 for TF-G9 grep-negative + +1 for provisioning-frozen-hardening (redundant with TF-G5 but keeps sub-cell readability).
- **KA structural attestations:** `test_tf_g1_ka_v0_frozen_and_snapshot_present` (attests `$defs` shape) + `test_tf_g3_ka_construction_requires_class_and_trace_id` (Pydantic ValidationError paths) + KA-assembly smoke split into happy + rejects = +3 sub-cells.

### §3.2 LoC (raw)

| Bucket | Actual LoC |
|---:|---:|
| Backend contracts (KA + Skill py + snapshots) | 452 |
| Backend service modules (init + registry JSON + loader + KA assembly + gate + persistence) | 436 |
| Backend router | 124 |
| Backend tests (`test_transform_forms.py`) | 422 |
| Modifications (server.py + 6 parity tests + 1 map + fixture audit) | ~20 |
| Rulings record | 108 |
| **Total TF (excluding this close report)** | **~1,562 LoC** |

### §3.3 Tier-2 miss disclosure (per governance §2.2 · disclosure not blocking)

**Owner-anchored band:** `[880, 1,240]` LoC (Owner explicitly ratified as UNCHANGED at rulings message despite E3 +1 cell + E4 belt-and-suspenders addenda).

**Actual:** **~1,562 LoC** → **ABOVE TOP by ~26%** (`snapshot_lloc_in_band=no`).

**Symmetric miss-disclosure (Ruling 5 · Tier-2 discipline):**

Drivers:

1. **Contract file LoC** (planned 60/class = 120; actual 235 = 134 + 101) — Owner-verbatim docstrings inline (mirroring AS-E1 pattern). +115 LoC.
2. **Snapshot JSON** (planned 2 × 155 = 310; actual 217 = 146 + 71) — **UNDER by 93 LoC.** KA schema uses `$defs` for 4 sub-models; CallableSkillProvisioning is a flat 8-field record with no nested types. Snapshot expansion below the codified rate of 155/each because these two contracts are less deeply nested than `OuterGateReceipt_v1`. **Deviation −30%** (right at the ±30% disclosure threshold from governance §6.7). Rate does NOT re-derive; snapshot size varies with contract shape and 155 remains the appropriate central estimate. Watched at next Stage A that adds a frozen contract.
3. **Service modules LoC** (planned 270; actual 436) — 4 modules landed with substantial Owner-verbatim docstrings inline (defensibility_loader + KA assembly + gate + persistence) + `callable_skill_gate.py` at 144 LoC hosts three exported symbols (`require_governed_skill_query` + `ensure_response_carries_class` + `below_floor_refusal_envelope` + `BelowFloorError` + `_CLASS_RANK` map). +166 LoC.
4. **Test file LoC** (planned 184; actual 422) — same rate-composition finding as Artifact Store: async httpx cells (not present in TF because router does not require live DB for cells; skipped) + AST scan cell (TF-G9 grep-negative at ~40 LoC standalone) + Pydantic validation cells (multiple field-required attestations). 21 actual cells at ~20 LoC/cell avg vs the 12 LoC/cell class assumption. **Rate-composition finding, not a rate-shift.** +238 LoC.

**Watched rate class observations (governance §6.8):**
- **Async httpx backend Pytest cells:** ZERO observed at TF (router endpoints tested via Pydantic + service-module unit paths, not via `AsyncClient`). Codification remains pending; the AS observation was ~25 LoC/cell empirical, no second data point at TF.
- **AST/reflection gate cells:** ONE observation at TF (TF-G9 grep-negative on `update_one({..., corpus_slice_ref: ...})`) at ~40 LoC/cell (matches AS-G6 empirical). This is the **second observation** of the AST/reflection gate class → per governance §6.8, class is **eligible for codification.** Follow-up small housekeeping commit can codify at 40 LoC/cell standalone if Owner directs.

### §3.4 §4.2 pre-authorized split thresholds — status

**Thresholds:** ≥1,500 LoC **OR** ≥60 cells → autonomous split.

**Actuals:** 1,562 LoC (**104% of LoC threshold → HIT**) · 21 cells (35% of cell threshold → not hit).

**Split status:** LoC threshold crossed. Same reasoning as Artifact Store (surface coherence): the KA contract + assembly + endpoint depend on the defensibility registry which depends on the loader; splitting KA vs Callable Skill across two commits would fragment the shared registry infrastructure. Single-commit landing chosen. Disclosed per new governance §2.2.

**Third §4.2 threshold hit in the last three phases:** B-5b (1,622 LoC), AS (1,674 LoC), TF (1,562 LoC). Rate-composition finding on test file dominates all three. Recommend Owner review of the 12 LoC/cell class assumption once more phases confirm the pattern — but current data (3 observations) reads as "amortised 12 LoC/cell holds for phases with pure classic shared-helper Pytest cells; phases mixing AST scans + async httpx + Pydantic-validation micro-cells land closer to 20-26 LoC/cell." Not a rate-shift disclosure; a distribution-shape finding. **Watched at TF close.**

---

## §4. Standing constraints preserved

| Constraint | Attestation |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at 31) | `test_v1_g7_attestation_parity_31_byte_identical_at_transform_forms_close` GREEN. |
| 29 pre-TF snapshots byte-identical during TF addition | `test_v0_paths_byte_identical_at_transform_forms_close` GREEN. |
| 4-code auth-refusal registry closed (P9-E3 / P8E-E4 α pre-carry) | `test_auth_refusal_registry_still_closed_at_four_codes_at_tf_close` GREEN. |
| E5 (no HTTP 409 in TF new files) | `test_no_http_409_in_transform_forms_new_files` GREEN (7 files scanned). |
| AS-H1 (deletion only via Seam 3; rollback = mechanics, not deletion) | TF adds no DELETE handlers; `revoke_skill` is `revoked_at` timestamp only, not a deletion. |
| Standing Rule v3 | Rulings + close + Stage A on disk. |
| Governance §4.3 promise-naming | TF-E1 (frozen wire honesty) + TF-E2 (buyer-facing slice-freeze) + TF-E3 (class-with-claim, no widening Literal) + TF-E4 (security boundary + immutability) — all landings carry the protected promise. |
| TF-E3 α condition · registry ⊇ live composition path vocabulary | TF-G8 GREEN. Second-vocabulary check: `mtafiti_registry.MtafitiRegistryRecord.defensibility_class` Literal args equal `ALLOWED_DEFENSIBILITY_CLASSES`. |
| TF-E4 (b) α · no `update_one` touches `corpus_slice_ref` | TF-G9 GREEN. AST walker over `backend/**/*.py`; zero violations. |

---

## §5. Housekeeping items 1–3 folded into TF close commit

### §5.1 Item 1 · Data-blind posture landed in governance doc

`docs/governance/tiered_ruling_model.md` §8 "Data-blind posture (Owner, 2026-07-09) — verbatim carrier" landed. Full Owner text quoted on disk. Effect map:
- Fixture / example / binding-copy content-type assumptions presented as estate shape → Tier-3 defect · correct-on-sight.
- Downstream activities MUST cite measured census composition → Tier-1 honesty-grammar rule.
- Pre-build data request to RMS prohibited.

### §5.2 Item 2 · 9.2-OWN-3 restated in PHASE_STATE + PRD

**Struck (prior wording):** *"Hour A + Hour B + 300-unit human-qualified slice from RMS"*.

**Landed (Owner-verbatim replacement in PHASE_STATE.md §9.2-OWN-3):**

> *"9.2-OWN-3 — Post-census validation slice only. No pre-build data request to RMS exists. Format/codec verification occurs at ingest, on grant compute, as part of the census run — a decode failure there is a day-one grant finding, not a build gate. The 300-unit human-qualified reference slice is drawn post-census, from measured estate composition, once the census has shown what the archive actually contains. BM-V placement unchanged (P9-E5 stands: verdict inside Phase 9, closes on INVESTIGATE, V1 PARTIAL until PASS, no production mining on INVESTIGATE) — only the reference slice's source moves from pre-build request to post-census measurement."*

BM-V placement unchanged (P9-E5 stands). PRD.md points to the PHASE_STATE carrier line.

### §5.3 Item 3 · Fixture audit + neutralisation

**Scan scope:** `backend/tests/`, `frontend/src/__tests__/`, `frontend/e2e/`, `docs/mandates/`, `docs/close_reports/`, `docs/stage_a_proposals/`, `docs/rulings/`, `docs/governance/`.
**Search terms:** `radio · television · TV · Kikuyu · political speech · news segment · talk show · political discourse · BBC Archive`.

**Findings:**
- **1 real defect corrected:** `backend/tests/invariants/feasibility_fixture_augmentation.json` — the `documented_censused_regions` array previously listed 8 content-type-loaded region names (`citizen_tv_news`, `wire_kna`, `aggregator_blog`, `citizen_archive`, `citizen_drama`, `radio_jambo_callin`, `unclassified`, `x_ingest`) — a pre-description of estate shape. **Neutralized to content-neutral placeholders** (`region_a..region_g` + `unclassified`) per Owner data-blind posture. Verified via `pytest tests/invariants/test_feasibility_honesty_under_absence.py + test_dispatch_shape_responsive.py` all GREEN (16/16 dependent cells).
- **5 false positives** (`radiogroup` ARIA role in frontend tests; "radio-like options" in prior close report referring to UI radio buttons). Not defects; standing.
- **Broader deep-scan (out of scope for TF close):** the `outer_gate_transform.snapshot.json` + several fixture-consuming test files still carry the pre-neutralization region names as literal-string test fixtures. Neutralizing those would require a coordinated fixture-refresh pass across ~5-8 test files. **Deferred to a follow-up Tier-3 housekeeping commit** per Owner Item 3 judgment clause ("historical close reports may be preserved byte-identical if amending them would corrupt on-disk canonical; use judgment and disclose choice").

**One-line disclosure:** Files scanned: 8 dir trees; defects found: 1 (fixture region name list); defects corrected: 1 (neutralized in `feasibility_fixture_augmentation.json`); deferred: broader region-name refresh across ~5-8 test fixtures (Tier-3 follow-up).

---

## §6. Item 4 · Census-dimensionality check (named reply line)

**Investigation scope:** `backend/contracts/mtafiti_registry.py` (Registry record shape) + `backend/services/mtafiti/registry.py` + `backend/services/mtafiti/census.py`.

### §6.1 Content surface (radio/TV/social) as queryable dimension on qualified units

**Answer: NO.**

The current `MtafitiRegistryRecord` (`contracts/mtafiti_registry.py:76-96`) carries these dimensions on qualified units:
`source_ref` · `region` (free-form str) · `feed_id` (declaration baseline key) · `sensitivity` · `defensibility_measure` · `defensibility_runtime_mode` · `matrix_rule_ref` · `defensibility_class`.

**No `content_surface` field.** `region` is a free-form str without a taxonomy binding it to broadcast/print/streaming/social.

**Additive path (proposal, no contract mutation):**
- New MongoDB collection `census_content_dimensions`, keyed by `feed_id` (matches the declaration-baseline pattern from `mtafiti_registry`).
- Fields: `feed_id`, `content_surface: Optional[str]` (censused label; empty until the census populates it), `content_surface_source: Literal["census_observed", "manifest_declared", null]` — matches the data-blind posture ("nothing pre-describes it").
- Registry-driven vocabulary at `census_content_surfaces.v0.json`, seeded empty; populated additively by the census.
- Sidecar join on `feed_id` at read time; `MtafitiRegistryRecord` unchanged (parity 31 preserved).

### §6.2 Genre / content-type as queryable dimension on qualified units

**Answer: NO.**

No `genre` or `content_type` field on `MtafitiRegistryRecord`. Not queryable today.

**Additive path (same pattern as §6.1):**
- Same `census_content_dimensions` collection, additional field `genre: Optional[str]` + `genre_source` metadata.
- Registry-driven vocabulary at `census_genres.v0.json`, seeded empty; populated additively by the census.

### §6.3 Recommendation

Both gaps are addressable via the established sidecar/registry pattern (B-5b Ruling E3 γ · P8E-E7 α · TF-E3 α precedent). **No frozen-contract mutation required; parity 31 preserved.** Estimated cost: ~150 LoC (one new collection + two seed registry JSON files + 3-4 cells).

**Sequencing:** Owner directs. Not gating Transform Forms close. Recommended: small housekeeping commit AFTER TF ratification, OR fold into Phase 9 Sub-stage 9.1 registry admin surface (already-landed as of Phase 9 stub substrate). Deferred pending Owner direction.

---

## §7. Test suite results at close

| Suite | Pre-TF | Post-TF | Δ | Result |
|---|---:|---:|---:|---|
| Backend Pytest (`pytest -q`) | 1,066 | **1,089** | **+23** | ✅ GREEN |
| Frontend Jest (`ui_spec_v1`) | 137 | **137** | 0 | ✅ GREEN (22 suites) |
| Playwright chromium (all) | 44 | **44** | 0 | ✅ GREEN |

Parity 31/31 byte-identical (V1-G7 attested at 31).

---

## §8. Sequence position + downstream unlock

| Item | Status |
|---|---|
| Transform Forms (this close) | **CLOSED (awaiting Owner ratification).** |
| Opportunity Briefs (§3.15) | Queued post-Phase-9 Stage B; requires populated Registry (fixture-census demo permitted per AS-U2). |
| Phase 9 Stage B (Extraction GPU half) | Dispatch-independent of Transform Forms; subject to 9.2-OWN-1 · 9.2-OWN-2 · 9.2-OWN-3 (post-census validation slice only per Owner amendment 2026-07-09). |
| Production housing (§3.4) | Queued post-Opportunity-Briefs. |
| AS-OWN-1 (production object-store choice) | Still open; adapter seam dispatch-independent; not gating anything. |

═══════════════════════════════════════════════════════════════════

*End of Transform Forms close report. Standing Rule v3: full text on disk. Reply body = SHA + tier tags + band-actual + gate roster + housekeeping items 1–4 resolution + census-dimensionality reply. Awaits Owner ratification.*
