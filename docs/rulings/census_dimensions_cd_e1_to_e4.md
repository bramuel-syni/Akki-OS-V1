# Census-dimensions mini-phase · Owner Rulings CD-E1..CD-E4

**Dispatch:** Owner Message post-Stage-A relay (2026-07-10).
**Applies to:** Stage A proposal `docs/stage_a_proposals/census_dimensions.md` SHA `53151d2c72a9f150b30e4cea5174bd9a0276a14e803c6ffdd9a7c43ee43a6cdb` (321 lines).
**Governance model:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`.
**Standing Rule v3:** on-disk canonical. Reply body carries file SHA + line-range map + tier tags only.

---

## §1. Owner rulings — VERBATIM

### §1.1 CD-E1 — α, contradiction validator made symmetric

> α, contradiction validator made symmetric. The proposal rejects value-null + source-present; the mirror is the real fabrication risk and must also reject: value present + source null. Rule: value and source present together or absent together; either lone state fails validation. β rejected — a required "unknown" label fabricates a value to represent absence.

**Applied at execution:**
- `CensusContentDimension` `model_validator(mode='after')` `_symmetric_contradiction` enforces the rule bidirectionally over both `(content_surface, content_surface_source)` and `(genre, genre_source)` pairs.
- `source` field is `Optional[Literal["census_observed", "manifest_declared"]]` (closed 2-set; no "unknown" fabrication).

### §1.2 CD-E2 — α, explicitly coupled to CD-E4

> α, explicitly coupled to CD-E4. Per the B-3 D4b package: the container stays unfrozen because the wire-shape gate lands; if CD-E4 ever regressed, this ruling flips to freeze. Record the coupling in the rulings record so neither is relaxed alone. Parity stays 31.

**Applied at execution:**
- `CensusContentDimension` uses `ConfigDict(extra="forbid")` — **UNFROZEN** (no `frozen=True`). No snapshot; parity stays 31/31 byte-identical.
- Runtime Pydantic validator at write-time via `record_census_dimension(...)`.
- Load-bearing wire-shape gate lands alongside (CD-E4 α; see §1.4 below).

### §1.3 CD-E3 — α, with the registration mechanism added

> α, with the registration mechanism added — as framed it deadlocks. Both registries seed empty; a hard write-time error against an empty registry means the first census run can never write. Fix: the census write path registers before it validates. First-observed census_observed values extend the registry via the additive versioned bump (v0→vN) during the census run, then the sidecar write validates against the now-current registry. manifest_declared values get no such path — they pre-exist in the registry or fail hard; a manifest cannot invent vocabulary, only observation can. The registry's version history becomes the audit trail of when each vocabulary item was first observed. CD-G3 stands as belt-and-suspenders.

**Applied at execution:**
- `dimensions_loader.register_observation(kind, value)` — writes v(N+1).json byte-preserving v(N).json; idempotent-by-value.
- `dimensions_service.record_census_dimension(...)` orchestrates register-before-validate: if `source == "census_observed"` and value not in registry → `register_observation(...)` bumps → then `validate_content_surface(...)`/`validate_genre(...)` runs against the now-current registry.
- If `source == "manifest_declared"` and value not in registry → the validator raises `ValueError` immediately (hard fail; no bump).
- CD-G3 AST/reflection gate lands as belt-and-suspenders (`test_census_dimensions_ast_gate.py`).

### §1.4 CD-E4 — α, required

> α, required. Five governance-key fields pinned (presence + name + type), tolerance test asserting additive fields pass — Phase 9 census integration will add fields; the gate rejects drift without rejecting growth.

**Applied at execution:**
- `test_census_dimensions_wire_shape.py` lands the 5-field pinning gate. Pinned fields: `feed_id` (required, str), `content_surface` (Optional[str]), `content_surface_source` (Optional[Literal[census_observed, manifest_declared]]), `genre` (Optional[str]), `genre_source` (Optional[Literal[census_observed, manifest_declared]]).
- Tolerance test `test_cd_e4_tolerance_additive_fields_do_not_reject_gate` asserts current additive fields (`censused_at`, `notes`) do NOT cause gate rejection; adding NEW additive fields is permitted per the tolerance clause.

---

## §2. Load-bearing coupling — CD-E2 ↔ CD-E4 (Owner recorded verbatim)

> **CD-E2 ↔ CD-E4 coupling (Owner ruled 2026-07-10):** Container stays unfrozen because the load-bearing wire-shape gate (CD-E4 α) lands alongside it. If CD-E4 ever regresses or is relaxed, this ruling flips to freeze. Neither may be relaxed alone; both are relaxed together or both are enforced together.

**Anti-regression discipline:** any future dispatch that touches either `CensusContentDimension` (removing the wire-shape gate, changing to freeze, changing pinned-field set) MUST reference this coupling clause and either:
1. Preserve both α rulings unchanged, OR
2. Escalate the coupled change as a joint CD-E2 + CD-E4 Tier-1 escalation to the Owner. Isolated changes to either ruling are rejected on sight.

**Precedent basis:** Owner cited B-3 D4b ruling (`test_engineer_key_grant_load_bearing_wire_shape.py`) as the pattern — "container's unfrozen status is contingent on this gate; without it, freeze would be the ruling."

---

## §3. Ruling recorder

- **Owner text on disk (this file):** all rulings verbatim, no paraphrase, no trimming.
- **Applied-at-execution notes** are the builder's disclosure of how the ruling landed in code.
- **Coupling clause** is landed as its own §2 so future readers see the package deal without hunting through §1.

═══════════════════════════════════════════════════════════════════

*End of Census-dimensions Owner rulings record. Standing Rule v3: on-disk canonical.*
