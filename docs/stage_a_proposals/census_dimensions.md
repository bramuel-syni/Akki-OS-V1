# Census-dimensions mini-phase · Stage A Proposal (BCR §3.7 sidecar · post-TF-ratification)

**Dispatch:** Owner Message 565 (post-TF-ratification, 2026-07-09).
**Sequence position:** post-TF-ratification, ahead of Phase 9 Stage B. Mini-phase scope (smaller than a full BCR §3.x phase); additive sidecar only.
**Governance model:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Escalations pre-tiered per §4.1.
**Standing Rule v3:** on-disk canonical. Reply body carries file SHA + line-range map + tier-tagged escalation IDs only.
**Data-blind posture (governance §8):** load-bearing throughout. Registries seed EMPTY; dimensions are census-measurement outputs, never pre-descriptions. No fixture, example, or binding-copy content-type assumption is presented as the estate's shape.

---

## §0. Owner text — verbatim carrier

Owner Message 565 named this mini-phase without a single quoted directive; the substance flows from the TF close §6 "Item 4 · Census-dimensionality check" reply, which the Owner ratified alongside the TF close. The load-bearing text is the TF close §6.3 recommendation (Owner-ratified 2026-07-09):

> Both gaps are addressable via the established sidecar/registry pattern (B-5b Ruling E3 γ · P8E-E7 α · TF-E3 α precedent). **No frozen-contract mutation required; parity 31 preserved.** Estimated cost: ~150 LoC (one new collection + two seed registry JSON files + 3-4 cells).

And the framing text from TF close §6.1-6.2 (which describes the shape being proposed):

> Additive path (proposal, no contract mutation):
> - New MongoDB collection `census_content_dimensions`, keyed by `feed_id` (matches the declaration-baseline pattern from `mtafiti_registry`).
> - Fields: `feed_id`, `content_surface: Optional[str]` (censused label; empty until the census populates it), `content_surface_source: Literal["census_observed", "manifest_declared", null]` — matches the data-blind posture ("nothing pre-describes it").
> - Registry-driven vocabulary at `census_content_surfaces.v0.json`, seeded empty; populated additively by the census.
> - Sidecar join on `feed_id` at read time; `MtafitiRegistryRecord` unchanged (parity 31 preserved).

---

## §1. Cell-density assumption (rates carried forward from governance §6)

Rates cited from the on-disk codified rate ledger; no restatement.

### §1.1 Empirical baseline (all codifications carried forward through STEP A commit `93334fb`)

| Class | Rate | Basis |
|---|---:|---|
| Backend Pytest shared-helper amortised | 12 LoC/cell | §6.1 |
| Backend endpoint impl 3-share | 40 LoC/endpoint | §6.2 |
| Backend service module standalone | 100 LoC/module | §6.3 |
| Frontend Jest structural fallback | 16 LoC/cell | §6.4 (N/A — no frontend cells this phase) |
| Playwright chromium data-testid | 9 LoC/cell | §6.5 (N/A — no UI this phase) |
| Frozen Pydantic contract class | 60 LoC/class | §6.6 (N/A — no new frozen contract) |
| Frozen contract snapshot JSON standalone | ~155 LoC/snapshot | §6.7 (N/A — no new snapshot) |
| **Verbatim-carrier overhead** (per carrier) | **~100-150 LoC** | **§6.9 (this phase: 1 carrier at light end — Owner text is compact per §0)** |
| **AST/reflection gate cell** (standalone) | **~40 LoC/cell** | **§6.10 (this phase: 1 candidate cell — registry-superset gate; see §2.4 CD-G3)** |

### §1.2 Watched rate classes (per governance §6.8; NOT codified until second observation)

- **Async httpx backend Pytest cells** — ~25 LoC/cell empirical at AS. Census-dimensions has ≤ 3 async client cells expected (sidecar write E2E + sidecar-join-at-read E2E + registry-superset E2E). If they land at ~25 LoC/cell → second observation triggers codification eligibility.

### §1.3 Mini-phase-specific cell classes

None emerge. Sidecar collection + registry JSONs + loader all decompose into standard shapes (service module, JSON registry, Pytest cell, AST gate). No new rate class.

### §1.4 Re-derivation rule

If execution observes a class not present in the rate ledger, disclose at close with cell count + LoC actuals; codify only if a second observation confirms the class per Ruling 5.

---

## §2. Matrix enumeration

### §2.1 Frozen contracts to add

**ZERO new frozen contracts.** Parity stays 31/31 byte-identical. This is Load-bearing on the proposal — the whole point of the sidecar pattern (per TF close §6.3, B-5b E3 γ + P8E-E7 α + TF-E3 α precedent) is that census dimensions land as versioned registry JSONs + Mongo-schema-only sidecar, NOT as a Pydantic frozen contract.

**Trade-off explicitly disclosed at CD-E2 [Tier 1].** If the Owner rules that the sidecar record MUST land as a frozen Pydantic contract (α option there), parity 31 → 32 and §6.6/§6.7 line-items ADD (60 + 155 = 215 LoC).

### §2.2 Registries to seed

Two versioned registry JSONs, both **seeded EMPTY** per data-blind posture governance §8:

| Path | Purpose | Seed content |
|---|---|---|
| `backend/services/census_dimensions/census_content_surfaces.v0.json` | Vocabulary for `content_surface` field (broadcast / print / streaming / social / etc.) | `{"version": "v0", "surfaces": []}` — EMPTY. |
| `backend/services/census_dimensions/census_genres.v0.json` | Vocabulary for `genre` field (news / talk / drama / sport / etc.) | `{"version": "v0", "genres": []}` — EMPTY. |

Population happens ONLY at census run time (post-grant compute per governance §8 · TF close §6.1). Any pre-populated value is a data-blind posture defect — Tier-3 correct-on-sight.

### §2.3 Service module

**`backend/services/census_dimensions/`** — NEW package.

- `__init__.py` — barrel (~30 LoC).
- `dimensions_loader.py` — registry load + validate + `validate_content_surface(v)` + `validate_genre(v)` (~60 LoC standalone service module per §6.3; smaller than 100 because registries are simple string lists).
- `dimensions_service.py` — sidecar write (`record_census_dimension`) + sidecar read (`get_dimensions_for_feed`) + registry-superset check helper (~90 LoC).

Total service module LoC: ~180.

### §2.4 Sidecar collection shape (Mongo-schema-only; NOT a Pydantic contract per §2.1)

MongoDB collection `census_content_dimensions`, unique index on `feed_id`.

| Field | Type | Notes |
|---|---|---|
| `feed_id` | str | Primary key; matches `MtafitiRegistryRecord.feed_id` (declaration baseline). |
| `content_surface` | `Optional[str]` | Nullable until census populates. Must validate against `census_content_surfaces.v0.json`. |
| `content_surface_source` | `Optional[str]` | See CD-E1 [Tier 1]. |
| `genre` | `Optional[str]` | Nullable until census populates. Must validate against `census_genres.v0.json`. |
| `genre_source` | `Optional[str]` | Symmetric with `content_surface_source`. |
| `censused_at` | `Optional[str]` (ISO 8601 UTC) | Timestamp of census-run observation; null until observed. |
| `notes` | `Optional[str]` | Free-form annotation from census-run operator (empty by default). |

**No `_id` collision with mtafiti_registry** — this is a separate collection. Read-time join by `feed_id`.

### §2.5 Endpoints (read-only at this mini-phase; writes come from census run at Phase 9)

Two read-only GET endpoints on new router `backend/routers/census_dimensions.py`:

- **`GET /api/census/dimensions/{feed_id}`** — returns sidecar record for one feed_id (404 if not present).
- **`GET /api/census/dimensions`** — paginated list; supports filter by `has_content_surface: bool` / `has_genre: bool` (both default null → returns all).

**No POST endpoint at this mini-phase.** Writes are census-run-only; the census-run harness lands at Phase 9 Sub-stage 9.2 and uses `dimensions_service.record_census_dimension(...)` directly (in-process, not via HTTP). This preserves the "census discovers the estate" invariant (governance §8) — no ad-hoc human writes into the dimensions sidecar via API.

Endpoint LoC: 2 endpoints × ~40 LoC/endpoint amortised (§6.2 rate) = ~80 LoC.

### §2.6 Named gates roster

| Gate | Class | Rate | Purpose |
|---|---|---:|---|
| **CD-G1** Registries seed EMPTY at v0 | classic Pytest (§6.1) | 12 LoC/cell | Loads both v0.json files at test time and asserts `surfaces == []` and `genres == []`. Data-blind posture attestation. |
| **CD-G2** Sidecar record accepts EMPTY content_surface + genre | classic Pytest (§6.1) | 12 LoC/cell | Write a `census_content_dimensions` record with all optional fields null → succeeds. Ensures no pre-population is required. |
| **CD-G3** Registry-superset gate (**AST/reflection cell**) | §6.10 reflection | ~40 LoC/cell | AST-walker over `services/census_dimensions/dimensions_service.py` verifying every `content_surface` / `genre` value assigned in code must appear in the corresponding registry v0.json. Grep-negative on `content_surface="hard_coded_value"` patterns. Similar to TF-G9 in shape (walker + whitelist + violation formatter). |
| **CD-G4** Read-time join preserves `MtafitiRegistryRecord` byte-identical | classic Pytest (§6.1) | 12 LoC/cell | Sidecar join at read time returns a composite dict but does NOT mutate the underlying `MtafitiRegistryRecord` bytes (contract stays frozen). |
| **CD-G5** No POST endpoint on census-dimensions router | classic Pytest (§6.1) | 12 LoC/cell | Router introspection: `POST /api/census/dimensions/*` returns 404/405. Enforces census-run-only-write invariant. |
| **CD-G6** V1-G7 parity 31 attest (unchanged) | classic Pytest (§6.1) | 12 LoC/cell | Re-run V1-G7 asserting parity stays 31/31 byte-identical post-mini-phase. |
| **4-code auth-refusal registry closed** | classic Pytest (§6.1) | 12 LoC/cell | Re-run of standing gate. |
| **E5 no HTTP 409 in new files** | classic Pytest (§6.1) | 12 LoC/cell | Grep-negative on new files under `services/census_dimensions/` + `routers/census_dimensions.py`. |

**Total cell count projection:** 8 classic Pytest cells + 1 reflection cell = **9 cells.**

**Plus E2E cells (async httpx · watched at §6.8):** ≤ 3 async client cells — sidecar write E2E + sidecar-join-at-read E2E + registry-superset E2E. At ~25 LoC/cell if the AS pattern holds → ~75 LoC.

### §2.7 Verbatim carrier — 1 carrier at light end

Per §6.9, one verbatim carrier lands: the Owner text from §0 (TF close §6.3 + §6.1-6.2 recommendations) embedded as module docstring in `services/census_dimensions/__init__.py` + this Stage A proposal + close report. Text is compact (~2 short paragraphs); estimated overhead ~40 LoC (light-end of §6.9's 100-150 band; disclosed as under-band at close per §6.9 deviation clause).

---

## §3. Owner-anchored band derivation

Applying §1.1 rates to the §2 matrix:

| Line-item | Basis | LoC |
|---|---|---:|
| Service module — `dimensions_loader.py` + `dimensions_service.py` + `__init__.py` | §6.3 (~180) | ~180 |
| Router endpoints × 2 (amortised) | §6.2 (2 × 40) | ~80 |
| 2 registry JSONs (empty seeds) | flat | ~10 |
| 8 classic Pytest cells (shared-helper amortised) | §6.1 (8 × 12) | ~96 |
| 1 AST/reflection gate cell (CD-G3) | §6.10 (~40) | ~40 |
| ≤3 async httpx E2E cells (watched) | ~25 empirical | ~75 |
| Verbatim carrier (Owner text) | §6.9 light-end (~40) | ~40 |
| Docs (Stage A this file · close report · rulings) | prose | ~150 |
| **Point-estimate** | | **~671** |

Apply +15% deviation margin (per prior phases' underestimate history): **~770 LoC top of band.**

**Proposed Owner-anchored band: `[500, 750]` LoC** (mid ~625; point-estimate 671 sits at ~85% of top-of-band). Aligns with Owner's ~150 LoC hint at TF close §6.3 IF the Owner intended only the collection + registries + 3-4 cells excluding docs + endpoints + tests + reflection gate; the §6.3 estimate excluded these amortisation-detected line-items which the rate ledger now surfaces explicitly per §6.9/§6.10 codifications.

**Split thresholds NOT triggered** (671 < 1,500 LoC · 9 cells < 60 cells). §4.2 pre-authorized split irrelevant at this scale.

**Snapshot LoC in-band:** yes (projected).

---

## §4. §0.1 Standing Dispositions / §0.2 Plan Debts

- **§0.1 FROZEN** — zero new Standing Dispositions anticipated.
- **§0.2** — zero new Plan Debts anticipated.
- **AS-OWN-1** (production object-store choice) — still open, NOT gating; sidecar collection uses same Mongo instance as `mtafiti_registry` (no artifact-store dependency for the dimensions sidecar itself).
- **9.2-OWN-1..3** — in-motion Owner-side; NOT gating this mini-phase. Population of the sidecar happens at Phase 9 census run; the SHAPE of the sidecar (this mini-phase) is dispatch-independent of 9.2-OWN facts.
- **New [OWNER] gates from Census-dimensions:** NONE anticipated. Mini-phase is not gated on any Owner-side fact; Owner-Tier-1 rulings on CD-E1..CD-E4 are sufficient.

---

## §5. Escalations — PRE-TIERED per governance §4.1

### §5.1 CD-E1 [Tier 1] · `*_source` field discipline (Literal shape closure)

**Class:** honesty grammar (governance §1.1 · "class-with-claim" · "no fabricated values") + data-blind posture (governance §8).

**Question:** on `content_surface_source` and `genre_source`, what values are allowed and how is unknown-state represented?

**Authority-source language (TF close §6.1 verbatim, ratified):**

> `content_surface_source: Literal["census_observed", "manifest_declared", null]` — matches the data-blind posture ("nothing pre-describes it").

**Promise-protected (governance §4.3):** honesty grammar — the source label lets any downstream consumer verify the provenance of the dimension. A dimension without a source label is a fabricated value. Data-blind posture (governance §8) requires that any value NOT observed by the census carry a source label OTHER than `census_observed` — and if no manifest declared it either, the value must be null (not present) with an accompanying source label of null.

**Options:**

- **α** — Closed 2-set `Literal["census_observed", "manifest_declared"]` on the field, with the whole field nullable (`Optional[Literal[...]] = None`). If BOTH `content_surface` and `content_surface_source` are null → dimension is truly unknown. If `content_surface` is null but `content_surface_source == "manifest_declared"` → contradiction, rejected by validator. Explicit and structural.
- **β** — Closed 3-set `Literal["census_observed", "manifest_declared", "unknown"]` on the field, with the field required (non-nullable). Every record has an explicit source; `"unknown"` is the null-equivalent. Symmetric with existing 3-tier disposition patterns.
- **γ** — Open `str` (unbounded). Rejects Literal discipline. NOT recommended (Owner anti-pattern per BCR §3.11 CK-I1).

**Recommended:** **α**. Rationale: (1) matches Owner-ratified text at TF close §6.1 (`Literal["census_observed", "manifest_declared", null]` — literal readings maps cleanly to Optional[Literal[...]]); (2) closed 2-set + nullable field is minimum-honest — no fabricated `"unknown"` label; (3) matches TF-E3 α discipline (versioned registry over Literal-widening, applied here at the source label level).

**Escalation surface:** frozen wire contract shape + honesty grammar. Full-rigor Tier-1 treatment. Owner ruling required BEFORE execution.

---

### §5.2 CD-E2 [Tier 1] · Sidecar record — Mongo-schema-only vs frozen Pydantic contract

**Class:** frozen wire contract discipline (governance §1.1 last bullet).

**Question:** does the `census_content_dimensions` record land as a Mongo-schema-only sidecar (no Pydantic contract, no snapshot, parity stays 31), OR as a NEW frozen Pydantic contract `CensusContentDimensionV0` with snapshot (parity 31 → 32)?

**Authority-source language (TF close §6.3, ratified):**

> No frozen-contract mutation required; parity 31 preserved.

**Promise-protected:** (i) frozen wire contract discipline is Tier-1 whenever the record is a client-visible surface; (ii) the sidecar is INTERNAL (read via a joined GET endpoint but not directly exposed as a stable frozen shape). Analogous to TF-E2 β posture (service-layer dataclass, no snapshot) which the Owner ruled α (frozen) at TF because the record was load-bearing on the per-call inner gate. Here, the record is NOT load-bearing on any per-call gate; it is a read-time joined dimension.

**Options:**

- **α** — Mongo-schema-only sidecar. Pydantic validation happens at write-time via `dimensions_service.record_census_dimension(...)` using a Pydantic model that is NOT snapshot-frozen (unfrozen runtime validator; parity 31 preserved). Matches EngineerKeyGrantRegistration D4b Owner ruling (runtime Pydantic, unfrozen container, but pinned by a load-bearing wire-shape gate). Matches TF close §6.3 verbatim Owner ratification.
- **β** — Frozen Pydantic contract `CensusContentDimensionV0` + snapshot. Parity 31 → 32. Additional LoC: 60 + 155 = 215. Overrides TF close §6.3 text.
- **γ** — Raw dict, no validation. Rejects both Pydantic disciplines. NOT recommended.

**Recommended:** **α**. Rationale: (1) TF close §6.3 already ratifies parity-31-preserving path; (2) sidecar is internal, no external consumer relies on a stable snapshot; (3) load-bearing wire-shape gate (see CD-E4 [Tier 1] below) provides the audit clarity that a frozen snapshot would provide, at 40 LoC vs 215 LoC.

**Escalation surface:** frozen wire contract + parity assertion set. Full-rigor Tier-1 treatment. Owner ruling required BEFORE execution.

---

### §5.3 CD-E3 [Tier 1] · Registry-superset gate — enforce vs advisory

**Class:** honesty grammar (governance §1.1 · "no fabricated values") + security boundary indirect.

**Question:** does the registry-superset check (every `content_surface` / `genre` written to the sidecar must appear in the corresponding `*.v0.json` registry) enforce as a hard write-time error (α), OR log-and-continue with a Tier-2 disclosure (β), OR run only as a CI-time AST gate (γ · CD-G3)?

**Authority-source language (TF-E3 α precedent · TF close ratified):** *"class-with-claim: every disposition/refusal carries a class label."* Applied here: every dimension value must carry a class label that appears in the versioned registry.

**Promise-protected:** honesty grammar (no fabricated values) — a census-run writing a `content_surface="hard_coded_value_not_in_registry"` would silently create a defensibility gap. The registry IS the vocabulary; the sidecar record MUST speak that vocabulary.

**Options:**

- **α** — Write-time hard error via `dimensions_service.validate_content_surface(v)` / `validate_genre(v)`. Raises `ValueError` if `v` is not in the registry. CD-G3 AST gate additionally verifies no in-code hard-coded values bypass the validator (belt-and-suspenders). Symmetric with TF-E3 α (`validate_defensibility_class` runtime enforcement + TF-G8 registry-superset gate).
- **β** — Log-and-continue with Tier-2 disclosure. Softer; risks silent fabrication.
- **γ** — CI-time AST gate only (CD-G3), no runtime enforcement. Assumes census-run code paths are the only writers; if census-run adds a runtime path bypassing the validator, no guardrail.

**Recommended:** **α**. Rationale: (1) TF-E3 α + TF-G8 established the runtime-enforce + CI-attest pattern for registry-superset; (2) census-run is a scheduled process, not an interactive session — silent fabrication cannot be caught by human review at write time; (3) 40 LoC for the reflection gate + ~10 LoC for the runtime validator is cheap relative to the honesty-grammar promise it protects.

**Escalation surface:** honesty grammar + registry enforcement. Full-rigor Tier-1. Owner ruling required BEFORE execution.

---

### §5.4 CD-E4 [Tier 1] · Load-bearing wire-shape gate — required or optional under CD-E2 α

**Class:** frozen wire contract discipline (governance §1.1 last bullet) + honesty grammar.

**Question:** if CD-E2 lands as α (Mongo-schema-only sidecar, no snapshot), MUST the mini-phase land a load-bearing wire-shape gate pinning the sidecar record's field names + types (analogous to `test_engineer_key_grant_load_bearing_wire_shape.py` from B-3 · D4b UNFROZEN ruling)?

**Authority-source language (B-3 · Owner D4b ruling, ratified 2026-07-05):** *"container stays runtime Pydantic; NEW `test_engineer_key_grant_load_bearing_wire_shape.py` pins 7 governance-key fields presence + name + type; lifecycle-additive tolerance test explicitly asserts gate does NOT reject new lifecycle fields (expires_at, delegation, renewed_at, per-endpoint scoping). Container's unfrozen status is contingent on this gate; without it, freeze would be the ruling."*

**Promise-protected:** honesty grammar + audit clarity. Without a load-bearing wire-shape gate, an unfrozen container can drift silently across commits. The gate makes the shape's stability EVIDENT, not just intended.

**Options:**

- **α** — Landing REQUIRED. New `test_census_content_dimensions_load_bearing_wire_shape.py` (~50 LoC) pins 5 governance-key fields (`feed_id`, `content_surface`, `content_surface_source`, `genre`, `genre_source`) presence + name + type. Symmetric with B-3 D4b ruling.
- **β** — Optional; drop the gate, accept sidecar drift risk. NOT recommended — undermines CD-E2 α's audit clarity.
- **γ** — Load-bearing gate lives inside CD-G3 (the AST-reflection gate) as one composite gate. Compresses the surface but couples two distinct promises (registry-superset vs wire-shape stability). NOT recommended.

**Recommended:** **α**. Rationale: (1) B-3 D4b ruling established this pattern as the "unfrozen container + load-bearing gate" package deal; (2) sidecar drift is a real risk at Phase 9 census-run integration (new fields will land); the tolerance test (additive fields allowed; governance-key fields pinned) is exactly the discipline needed; (3) additional 50 LoC is affordable within the `[500, 750]` band.

**Escalation surface:** frozen wire contract shape (via load-bearing gate). Full-rigor Tier-1. Owner ruling required BEFORE execution.

---

### §5.5 CD-E5 [Tier 2] · Router mount path (disclosure-only, no ruling required)

**Class:** cost/rework · naming (governance §2.1 borderline with §3.1; disclosed at Tier-2 because the choice affects downstream census-run integration paths).

**Statement:** router mounts at `/api/census/dimensions/*` (matches Owner-visible surface language in TF close §6). Alternative was `/api/mtafiti/dimensions/*` (matches internal Mtafiti registry pattern). Chosen `/api/census/dimensions/*` because the surface concept is "census outputs", not "Mtafiti internals".

**Disclosure-only:** no Owner ruling required.

**Expected trigger:** NO. Path chosen at Stage A; disclosed here for completeness.

---

### §5.6 Tier-3 defaults (silent, disclosed at close, no escalation)

Per governance §3.2: builder defaults + one disclosure line per item. Format: `[Tier 3 default] {item} → {chosen default} — {one-line rationale}.`

Expected Tier-3 defaults at Census-dimensions execution:

1. **`[Tier 3 default]` Module layout** → `backend/services/census_dimensions/` (singular directory, descriptive-noun-plural for scope) — matches `services/transform_forms/` + `services/artifact_store/` conventions.
2. **`[Tier 3 default]` Registry filenames** → `census_content_surfaces.v0.json` + `census_genres.v0.json` — matches `defensibility_classes.v0.json` from TF-E3 α + `disclosure_types.v0.json` from B-5b E3 γ.
3. **`[Tier 3 default]` MongoDB collection name** → `census_content_dimensions` (matches TF close §6.1 verbatim).
4. **`[Tier 3 default]` MongoDB index** → unique index on `feed_id`; secondary index on `censused_at` for future range queries.
5. **`[Tier 3 default]` Router path** → `/api/census/dimensions/*` (per CD-E5).
6. **`[Tier 3 default]` No frontend surface** → the sidecar is read via Mtafiti Registry admin views which already exist; no new UI cells.
7. **`[Tier 3 default]` Docs skeleton** → `stage_a_proposals/census_dimensions.md` (this file) + `close_reports/census_dimensions.md` (at close) + `rulings/census_dimensions_cd_e1_to_e4.md` (Tier-1 rulings only).
8. **`[Tier 3 default]` Population source posture at close** → the mini-phase's close will attest registries seeded EMPTY and sidecar collection created empty; population is Phase 9 census-run scope.

---

## §6. Standing constraints preserved

| Constraint | Attestation at close |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | `test_v1_g7_attestation_parity_31_at_census_dimensions_close`. |
| 4-code auth-refusal registry closed | `test_auth_refusal_registry_still_closed_at_four_codes_at_cd_close` re-run. |
| E5 no HTTP 409 in mini-phase new files | grep-negative on `services/census_dimensions/*` + `routers/census_dimensions.py`. |
| E7 middle-dot / P9-E6 α em-dash | No UI copy at this mini-phase. No enforcement cell. |
| Standing Rule v3 (on-disk canonical) | Proposal + close + rulings on disk. |
| AS-H1 retention held-class (no direct DELETE) | Mini-phase adds no DELETE handlers. Grep-negative attest. |
| Governance §4.3 promise-naming rule | Each CD-E1..CD-E4 landing carries the promise it protects. |
| **Governance §8 data-blind posture (load-bearing this mini-phase)** | CD-G1 (registries seed EMPTY) + CD-G2 (sidecar accepts null dimensions) + CD-G3 (registry-superset gate) — three cells enforce the posture structurally. |

---

## §7. §0.2 Plan-debts status expected at close

- **No new debt anticipated.**
- **AS-OWN-1** still open (production object-store choice) — dispatch-independent.
- **9.2-OWN-1..3** in-motion Owner-side — dispatch-independent of Census-dimensions.
- **Answer fluency (§3.8)** — STILL_QUEUED at BCR §5.1 line 336 per Owner Message 565 status check; not this mini-phase's scope.

═══════════════════════════════════════════════════════════════════

*End of Census-dimensions mini-phase Stage A proposal. Standing Rule v3: on-disk canonical. Reply body carries file SHA + line-range map + tier-tagged escalation IDs.*
