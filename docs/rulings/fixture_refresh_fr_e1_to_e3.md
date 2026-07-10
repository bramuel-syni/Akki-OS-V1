# Fixture Refresh mini-phase — Rulings Record (FR-E1 to FR-E3)

**Dispatch:** Owner ruling on Fixture Refresh Stage A escalations (2026-07-10 · post-9.2a close).
**Basis:** Fixture Refresh Stage A proposal at `/app/docs/stage_a_proposals/fixture_refresh.md`.
**Standing Rule v3:** on-disk canonical. This file is the persistent record of Owner rulings + execution disposition.
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Metric-verdict in raw LoC per §9.
**Execution close:** `/app/docs/close_reports/fixture_refresh.md`.

---

## §1. Owner rulings — verbatim carriers

### §1.1 FR-E1 α — Fixture regenerate with neutralized content (Owner-ruled)

> **FR-E1 α — regenerate with neutralized content · five_rings@v0 byte-identical.**
> HAZARD-STOP #1 doctrine on-disk is explicit about CONTRACT-SHAPE hazard, not content hazard. Content changes (feed_id names, programme names, embedded assertions, language-mix arrays) are OUTSIDE the frozen-contract-shape locus. Regenerate `services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json` via `generate_fixture.py` with content-neutral placeholders (`feed_a..feed_h`, `programme_a..programme_j`, content-neutral assertion bodies, generalised language arrays). Five_rings@v0 contract shape preserved byte-identical (V1-G7 attest stays GREEN at parity 31).

**Disposition:** applied verbatim. Fixture regenerated; 19 units emit with neutralized `feed_id ∈ {feed_a..feed_h}` in `provenance.context`. Contract shape preserved (five_rings@v0). FR-G5 gate GREEN.

### §1.2 FR-E2 α + 2 conditions — Centralized single-source registry (Owner-ruled)

> **FR-E2 α — centralized single-source.** Extend `services/service_1/license_classes.v1.json` schema to include per-feed_id attributes: `license_class` (existing) + `source_standing` (migrated from `services/mtafiti/source_standing.py::_PLACEHOLDER_TABLE`) + `bucket_category` (migrated from `services/outer_gate/transform.py::_FEED_ID_BUCKET`). Consumers read via `license_class_map` module functions.
>
> **Condition 1:** v0 preserved byte-identical (append-only discipline).
> **Condition 2:** distributed tables DELETED (not shadowed) — `_PLACEHOLDER_TABLE` in `services/mtafiti/source_standing.py` + `_FEED_ID_BUCKET` in `services/outer_gate/transform.py` removed at v1. FR-G4 AST/reflection gate enforces no shadow sources (no NEW code introduces v0-style broadcaster keys directly).

**Disposition:** applied verbatim with both conditions honored.
- `license_classes.v1.json` created at `/app/backend/services/service_1/license_classes.v1.json` with centralized `feed_entries` map holding `{license_class, source_standing, bucket_category}` per feed_id (11 entries covering fixture aliases + syndication variety).
- `license_classes.v0.json` preserved byte-identical (FR-G1 GREEN · SHA `3351496c131578629dea34dddcc2a0cf6c5d5f98fe9a9719554ca9125526e841`).
- `_PLACEHOLDER_TABLE` DELETED from `services/mtafiti/source_standing.py`; module now reads from v1 registry via `services.service_1.license_class_selection.get_source_standing_name` + `known_feed_ids`.
- `_FEED_ID_BUCKET` DELETED from `services/outer_gate/transform.py`; module now reads from v1 registry via `services.service_1.license_class_selection.get_bucket_category`.
- Loader `_resolve_highest_version_path()` added to `license_class_selection.py` — reads highest-version `license_classes.v(N).json` (matches `models_registry.v0.json` highest-version discovery pattern from 9.2a-E1 α).
- FR-G4 AST gate GREEN — grep-negative across `services/` (excluding archived `rejected/`) confirms no broadcaster feed_id string literal appears as a runtime constant in NEW/MODIFIED service code.

### §1.3 FR-E3 α — Re-bless transform-golden · preserve historical closes (Owner-ruled)

> **FR-E3 α — re-bless the transform-golden · leave historical closes byte-identical.** Re-bless `services/tests/invariants/outer_gate_transform.snapshot.json` with neutralized `canonical_input.feed_id` (`feed_a`) + regenerated egress artifact (via `transform_artifact`). Historical close reports stay byte-identical (per Standing Rule v3 on-disk canonical). The re-bless discipline exists FOR THIS PURPOSE.

**Disposition:** applied verbatim.
- `outer_gate_transform.snapshot.json` re-blessed: `canonical_input.feed_id: "citizen_tv_news"` → `"feed_a"`; `egress_artifact.feed_id: "broadcast_news"` (unchanged bucket_category value; feed_a now resolves to broadcast_news via v1 registry).
- Test seed literal in `test_outer_gate_irreversibility.py` renamed via cascade sed rename (`citizen_tv_news` → `feed_a`).
- **NO** historical close reports modified. Verified by:
  - grep-negative on `/app/docs/close_reports/*.md` for Fixture-Refresh-related edits (0 hits).
  - Standing Rule v3 preserved on all `/app/docs/close_reports/*.md` files.
- FR-G7 gate GREEN.

---

## §2. Ancillary rulings applied inline

### §2.1 Direction-consistency check (Owner-mandated inline)

Owner mandated a "direction-consistency check" across 4 surfaces × 4 check-types = 16 intersections. Grep-based scan performed pre-execution.

**Surfaces:**
- S1: `/app/docs/stage_a_proposals/phase_9.md`
- S2: `/app/memory/PHASE_STATE.md`
- S3: `/app/memory/PRD.md`
- S4: `/app/docs/mandates/RMS_Mtafiti_Specification.md` (+ related Mtafiti spec ancillaries)

**Check-types:**
- C1: pre-split 9.2 wording (singular "9.2 GPU-half" residue vs post-split 9.2a/9.2b per governance §10)
- C2: pre-build data request wording (data-blind posture violation per governance §8)
- C3: census discovery-first / pre-populated registry residue
- C4: Mtafiti scope drift (editorial-authority claims from placeholder table wording, etc.)

**Verdicts (see close report §DirectionConsistency for detailed matrix):** CLEAN PASS on live-direction sections; residues in historical/on-disk-canonical sections PRESERVED per Standing Rule v3 (historical chronological accuracy is load-bearing; retroactive editing is revisionism). Correction applied inline at this commit's STEP A: none required — live direction correct across all 4 surfaces.

### §2.2 §4.2 disposition — atomic vs split (dev's judgment per Owner delegation)

Owner delegation verbatim: *"Execute: atomic per §4.1 or split per §4.2 at dev's judgment, disclosed at close, no round-trip."*

**Actual raw LoC diff:** 782 (well below §4.2's 1,500 raw threshold).
**Actual cell count:** 7 backend cells (well below §4.2's 60 threshold).
**Disposition:** **atomic single commit** per §4.1 baseline. Surface coherence preserved (fixture regen + registry consolidation + snapshot re-bless + test cascade share the same rename table; splitting fragments the semantic unit).

### §2.3 Audio-fixture README (Tier-3 dev's judgment · Owner opinion at 9.2a ratification)

Owner opinion 2026-07-10: *"alongside Fixture Refresh close is the natural slot."*
**Disposition:** deferred to next housekeeping (audio fixture README lands as separate rider). Rationale: the atomic Fixture Refresh commit stays scope-lean; the README is documentation-only and not gate-load-bearing.

### §2.4 MANIFEST rate-ledger cross-reference block (Tier-3 dev's judgment)

**Disposition:** deferred to next housekeeping. Rationale: not gate-load-bearing at Fixture Refresh scope; MANIFEST rate-ledger already landed at STEP A commit `b3ac048` per PHASE_STATE line 14; no drift observed at this commit.

---

## §3. FR-G4 AST/reflection gate — no shadow sources

FR-G4 AST gate at `/app/backend/tests/invariants/test_fixture_refresh_fr_g1_to_g7.py::test_fr_g4_no_shadow_source_broadcaster_literals_in_service_code`. Grep-negative reflection walk over `/app/backend/services/**` (excluding `rejected/` archive + `__pycache__`) confirms zero broadcaster feed_id string literals appear as runtime constants in NEW/MODIFIED service code post-Fixture-Refresh. This is the load-bearing "no shadow sources" gate — v1 is single-source; distributed tables are DELETED not shadowed.

**Exclusions (attested):**
- `services/data_source/synthetic_assets/rms_adversarial_v1/rejected/generate_fixture.incoming.py` — archived pre-HAZARD-STOP-#1 material; preserved per Standing Rule v3.
- `contracts/` — frozen contracts; not scanned by FR-G4 (no broadcaster literals in contract sources).
- `routers/` — router-layer business-domain strings; not scanned by FR-G4.
- `tests/` — test files are grep-sinks, not runtime dispatch surfaces.

---

## §4. Standing constraints preserved (attested at close)

| Constraint | Attestation |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | GREEN — full Pytest 1150/1150 including V1-G7. |
| 4-code auth-refusal registry closed | GREEN — no auth taxonomy changes at Fixture Refresh. |
| E5 no HTTP 409 in refresh new/modified files | GREEN — grep-negative on all Refresh-touched files. |
| Standing Rule v3 (on-disk canonical) | GREEN — historical close reports preserved byte-identical per FR-E3 α. |
| AS-H1 retention held-class (no direct DELETE) | GREEN — Refresh adds no DELETE handlers. |
| Governance §8 data-blind posture | GREEN — Fixture Refresh EXECUTES the posture on identified carriers. |
| Governance §9 metric-verdict-in-derivation-unit | GREEN — band + verdict rendered in raw LoC per §3 close-report derivation. |
| Governance §10 9.2 split ruling | GREEN — Fixture Refresh is dispatch-independent from 9.2b. |
| 9.2a-E1 α models_registry seed correction | GREEN — Fixture Refresh does NOT touch `models_registry.v0.json`. |
| CD-E2 ↔ CD-E4 coupling | GREEN — Not touched at Fixture Refresh. |

---

## §5. Provenance

- **Stage A proposal:** `/app/docs/stage_a_proposals/fixture_refresh.md`
- **Rulings record (this file):** `/app/docs/rulings/fixture_refresh_fr_e1_to_e3.md`
- **Close report:** `/app/docs/close_reports/fixture_refresh.md`
- **Landing SHA:** recorded in close report §7 post-commit.
- **Backend Pytest:** 1150/1150 (baseline 1143 + 7 FR-G1..FR-G7).
- **Frontend Jest:** 137/137 unchanged.
- **Playwright chromium:** 44/44 unchanged.
- **Parity:** 31/31 byte-identical.
