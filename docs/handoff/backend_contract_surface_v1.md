# Backend Contract Surface v1

**STATUS: FROZEN. READ-ONLY.**

This document is the complete backend contract surface that the frontend layer (Phase G5b) will consume. It is FROZEN as of the phase G6 close and READ-ONLY to any downstream consumer.

The frontend CONSUMES these contracts and routes. The frontend NEVER negotiates a change to them.

**A frontend need requiring a change to any contract or route defined here is a HAZARD-STOP (a) — not a handoff negotiation. Surface it as such, do not extend contracts to accommodate frontend convenience.**

Substrate: 14 frozen Pydantic/catalogue contracts, 20 registered `/api/*` routes (excluding FastAPI-managed docs surfaces), 7 filed source specs in `/app/docs/mandates/`.
Baseline CI at freeze time: 340/340 green.
Frozen contract mutations across all phases G0..G6: ZERO (additions only).

---

## §1. Frozen contracts (all 14)

| # | Contract | Version | File | Snapshot(s) | Source §-anchor | Phase | Purpose |
|---|---|---|---|---|---|---|---|
| 1 | `NormalizedUnit` (five_rings) | @v0 | `backend/contracts/five_rings.py` | `five_rings.contract_snapshot.json` | RMS Product Spec v2.1 §5 (Five Rings) | G0 | The atomic unit of RMS intelligence — carries the five Rings (Provenance, Signal, Relational, Re-extraction Handle, Defensibility). |
| 2 | `ObjectiveRequest` | @v0 | `backend/contracts/objective_request.py` | `objective_request.contract_snapshot.json` | RMS Product Spec v2.1 §4 (Objective language) | G0 | The user-facing request shape — objective_text + defensibility_floor + scope + mode. |
| 3 | `QualificationMatrix` | @v0 | `backend/contracts/qualification_matrix/loader.py` | `qualification_matrix.schema_snapshot.json` + `qualification_matrix.v0.content_snapshot.json` | RMS Product Spec v2.1 §6.4 (matrix rev + rule shape) | G0 | Governed table mapping signal profiles → defensibility class. |
| 4 | `SignalRing dimensions` (catalogue) | @v0 | `backend/contracts/signal_ring.py` | `signal_ring_dimensions.v0.content_snapshot.json` | RMS Product Spec v2.1 §5.3 | pre-G2 | Per-modality dimension catalogue (audio/video/image/text/composite) — content-frozen dict, not a Pydantic class. |
| 5 | `ExtractionParams` (catalogue) | @v0 | `backend/contracts/extraction_params.py` | `extraction_params.v0.content_snapshot.json` | RMS Product Spec v2.1 §5.5 | pre-G2 | Re-extraction Handle key catalogue — mandatory keys per modality + reproducibility keys. Content-frozen catalogue. |
| 6 | `LedgerRow` (`northena_ledger_row@v0`) | @v0 | `backend/contracts/northena_ledger.py` | `northena_ledger_row.contract_snapshot.json` | Northena §7.2 + §7.3 | G2a | The Northena Ledger row — one row per admit/gate/converge decision. `stamp_audit` permissively absorbs Solva traces, outer-gate receipts, V2 refusals. |
| 7 | `MtafitiRegistryRecord` | @v0 | `backend/contracts/mtafiti_registry.py` | `mtafiti_registry_record.contract_snapshot.json` | Mtafiti §7 + §11 | G4 | Per-source measurement record — declaration or overlay mode, defensibility class + score vector + freshness. |
| 8 | `MiningPlan` (Targeta) | @v0 | `backend/contracts/targeta_plan.py` | `targeta_mining_plan.contract_snapshot.json` | Targeta §7 + §17 | G4 | Deterministic mining plan — plan_id + registry_snapshot_ref + ordered_targets + defensibility_floor. |
| 9 | `TraceLensEnvelope` | @v0 | `backend/contracts/trace_lens.py` | `trace_lens_envelope.contract_snapshot.json` | Interface Spec §16 invariant #9 + Northena §7.2/§7.3/§12/§14 + Product v2.1 §8 | G5a | Cross-engine trace-correlation response — resolves 5-engine universe under one trace_id. |
| 10 | `LiftManifestEnvelope` | @v0 | `backend/contracts/lift_manifest_response.py` | `lift_manifest_envelope.contract_snapshot.json` | Interface Spec §16 governance-legibility | G5a | Lift manifest + spec fingerprints + Rule 2 v2 per phase. Governance read-surface. |
| 11 | `OuterGateReceipt` | @v0 | `backend/contracts/outer_gate_receipt.py` | `outer_gate_receipt.contract_snapshot.json` | Product v2.1 §21.2 + §22.1 | G6 | Irreversibility receipt for a successful outer-gate egress — transform_version, key_fingerprint, applied_transformations. Never contains plaintext. |
| 12 | `V2RefusalEnvelope` | @v0 | `backend/contracts/v2_refusal.py` | `v2_refusal_envelope.contract_snapshot.json` | Product v2.1 §29.1 + §30 | G6 | Structured V2 refusal — 4 reason codes. No partial-egress. |
| 13 | `CumulativeDisclosureLedger` | @v0 | `backend/contracts/cumulative_disclosure.py` | `cumulative_disclosure_ledger.contract_snapshot.json` | Product v2.1 §29.1 + §21.2 + §32 | G6 | Tracking-state for the V2 cumulative-disclosure arm. Closed-seam at v0 (`arm_admitted=False`). |

---

### §1.1 `NormalizedUnit` (five_rings@v0) — G0
- `unit_id: str` — REQUIRED. Stable UUID for this unit; cross-referenced by Relational edges.
- `provenance: ProvenanceRing` — REQUIRED. Origin metadata (source_ref, speaker_or_author, feed_id, structural_signature, author_labels, context).
- `signal: SignalRing` — Per-modality signal-depth dimensions. Values catalogue-frozen by contract #4.
- `relational: RelationalRing` — Cross-unit edges.
- `reextraction_handle: ReextractionHandleRing` — REQUIRED. Reproducibility metadata (extraction_params catalogue-frozen by contract #5).
- `defensibility: DefensibilityRing` — REQUIRED. Class + score + Solva stamp when present.

Modalities: `AUDIO`, `VIDEO`, `IMAGE`, `TEXT`, `COMPOSITE`. Defensibility classes: `fact`, `utterance`, `non_factual`.

### §1.2 `ObjectiveRequest@v0` — G0
- `objective_text: str` — REQUIRED. Author's free-form objective statement.
- `defensibility_floor: DefensibilityFloor` — REQUIRED. Minimum class the response must reach.
- `provenance_required: bool = True` — If true, every cited unit must carry a non-empty Provenance ring.
- `scope: EstateRegionSelector` — REQUIRED. Which portfolio region(s) apply.
- `mode: ObjectiveMode = PER_RUN` — `per_run` or `portfolio`.
- `tags: List[str]` — Optional author tags; surfaced in the Operator Console (G5b).

### §1.3 `QualificationMatrix@v0` — G0
- `matrix_rev: str` — REQUIRED. Governed rev id (e.g. `v0`).
- `rules: List[QualificationRule]` — REQUIRED. Each `QualificationRule` maps a signal-profile pattern → a defensibility class + reason.

### §1.4 `SignalRing dimensions@v0` (catalogue) — pre-G2
Not a Pydantic class — a frozen module-level dict + validation function. Structure:

```python
SIGNAL_RING_DIMENSIONS_V0 = {
    "audio":     ["prosody", "vocal_emphasis", "affect_valence", "affect_arousal", "speech_rate", "pause_density"],
    "video":     ["visual_emphasis", "scene_change_density", "framing_markedness"],
    "image":     ["visual_emphasis", "composition_markedness"],
    "text":      ["lexical_intensity", "stance_intensity", "hedging_density"],
    "composite": [],
}
```

Snapshot at `tests/invariants/signal_ring_dimensions.v0.content_snapshot.json`. `signal_ring_dimensions.rev` is `v0`.

### §1.5 `ExtractionParams@v0` (catalogue) — pre-G2
Not a Pydantic class — module-level catalogue + two validation functions:
- `reproducibility_keys(modality)` → subset of mandatory keys used for V1 two-run comparison (excludes `extracted_at`).
- `is_deterministically_reproducible(params)` → gate: refuses if `temperature > 0` per mandate.

Snapshot at `tests/invariants/extraction_params.v0.content_snapshot.json`.

### §1.6 `LedgerRow` (`northena_ledger_row@v0`) — G2a
- `run_id: str` — REQUIRED. UUID — one run has one closed Ledger.
- `trace_id: str` — REQUIRED. Joins ledger to unit-level intelligence and trace lenses.
- `stage: Literal["admit","gate","converge"]` — REQUIRED. (No new stage literal at G6.)
- `decision: Literal["admitted","refused","warm","fresh","terminate_success","terminate_budget","continue"]` — REQUIRED. Semantics per stage:
  - `admit` stage: `admitted` | `refused`
  - `gate` stage: `warm` | `fresh` | `refused` (V2 refusal = `refused`; outer-gate transform applied = `fresh`)
  - `converge` stage: `terminate_success` | `terminate_budget` | `continue`
- `reason: str` — REQUIRED. Deterministic reason string. Known prefixes:
  - `admitted:*` / `refused:*` / `warm:*` / `fresh:*`
  - `service_1_converged:units=<n>:plan=plan_<hex>` (G4)
  - `targeta_plan_built:{plan_id}` (G4)
  - `outer_gate_transform_applied:hmac-sha256-v1` (G6)
  - `v2_refused:<reason_code>` (G6)
- `artifact_ref: LedgerArtifactRef` — REQUIRED. Portfolio mandate / artifact identity.
- `lawful_basis_ref: str` — REQUIRED. What the file-out lawful-basis is (§30 purpose limitation).
- `stamp_audit: Optional[Dict] = None` — Permissive Dict side-channel. Absorbs:
  - Solva stamp (G1+G3): `{unit_id, decision, reason, judged_signal_dimensions, floor_violation, stages, computed_class, load_bearing_unit_ids, ...}`
  - Outer-gate receipt (G6): `{"outer_gate_receipt": OuterGateReceipt.dump()}`
  - V2 refusal (G6): `{"v2_refusal": V2RefusalEnvelope.dump()}`
- `at: datetime` — REQUIRED. When this row was written (Mongo native).

**Snapshot invariance guaranteed by** `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py::test_northena_ledger_row_contract_snapshot_unchanged_at_g6`.

### §1.7 `MtafitiRegistryRecord@v0` — G4
- `source_ref: str` — REQUIRED. Stable pointer (matches ProvenanceRing.source_ref).
- `region: str` — REQUIRED. Estate region key.
- `feed_id: str` — REQUIRED. Keys the declaration baseline.
- `sensitivity: str` — REQUIRED. DPA sensitivity classification (mandate §8).
- `defensibility_measure: MtafitiScoreVector` — REQUIRED. Composed measure (mandate §11).
- `defensibility_runtime_mode: Literal["declaration_baseline","overlay"] = "declaration_baseline"` — Which measurement mode produced this record. `overlay` mode is CLOSED SEAM at G6.
- `matrix_rule_ref: str` — REQUIRED. Governed Matrix rule id (mandate §17 #4). Auditable.
- `defensibility_class: Literal["fact","utterance","non_factual"]` — REQUIRED. Verdict from Matrix lookup.
- `freshness_stamp: FreshnessStamp` — REQUIRED. `{observed_at, feed_state_hash, ttl_seconds}` or equivalent.

### §1.8 `MiningPlan@v0` (Targeta) — G4
- `plan_id: str` — REQUIRED. Deterministic plan id; reproducible per Targeta §17 #8.
- `mode: Literal["portfolio","per_run"]` — REQUIRED.
- `governing_artifact_ref: LedgerArtifactRef` — REQUIRED.
- `registry_snapshot_ref: str` — REQUIRED. Mtafiti Registry snapshot id at plan-build time.
- `ordered_targets: List[TargetLocation]` — REQUIRED. Deterministic core ranking.
- `defensibility_floor: TargetaFloorSpec` — REQUIRED.
- `core_baseline_ranking: List[str]` — REQUIRED. Deterministic core ordering, for attribution/audit.
- `yield_layer_version: str = "core-only"` — `"core-only"` when yield closed (v0); version string when admitted (mandate §7 + §17 #7). CLOSED SEAM at G6.
- `generated_at: str` — REQUIRED. ISO-8601 UTC.

### §1.9 `TraceLensEnvelope@v0` — G5a
- `trace_id: str` — REQUIRED. The joining identifier.
- `resolved_at: str` — REQUIRED. ISO-8601 UTC of resolution moment.
- `run_ids: List[str]` — Unique run_ids observed for this trace_id (Northena §7.2 — one run has one closed Ledger; multiple runs may share a trace_id in the audit-lens read).
- `engines_touched: List[str]` — Sorted set membership from `{northena_ledger, solva, targeta, mtafiti, service_1}`.
- `ledger_rows: List[LedgerRow]` — All ledger rows matching this trace_id, oldest first.
- `solva_traces: List[ResolvedSolvaTrace]` — Solva reasoning traces embedded via stamp_audit side-channel. Shape: `{trace_id, question, stages: List[{stage_name, ...}], computed_class, load_bearing_unit_ids, conclusion, ...}`.
- `mining_plans: List[MiningPlan]` — Targeta plans referenced by ledger `reason` prefix `targeta_plan_built:{plan_id}`.
- `registry_records: List[MtafitiRegistryRecord]` — Mtafiti records resolved via `MiningPlan.ordered_targets.source_ref`.
- `registry_freshness: RegistryFreshnessMarker` — `{snapshot_pinned: bool = False, note: str}` — snapshot pinning is post-G5a enrichment.

### §1.10 `LiftManifestEnvelope@v0` — G5a
- `manifest_version: str` — REQUIRED.
- `manifest_semantics: str` — REQUIRED.
- `generated_at: str` — REQUIRED.
- `generated_by: str` — REQUIRED.
- `substrate_state: Dict` — REQUIRED. Substrate state markers (e.g., `reference_akki_legacy_present`).
- `substrate_settled_at: Optional[str] = None`.
- `entries: List[LiftEntry]` — REQUIRED. Each entry: `{module, lift_kind, resolves_by, transitive_chain, cousin_citation, shape_signature, notes}` (LiftEntry uses `extra="allow"` — permissive).
- `source_specs: List[SourceSpecFingerprint]` — Live-read from `docs/mandates/MANIFEST.md`. Each: `{filename, sha256}`.
- `phase_accounting: Dict[str, Rule2Accounting]` — Rule 2 v2 per phase. `Rule2Accounting = {lifted_verifiable, net_new_discretionary, mandate_forced_net_new, overall_ratio, discretionary_only_ratio, journal_ref}`. `journal_ref` is prepended with `[counting_standard: pre-§0]` or `[counting_standard: post-§0-strict]` per the freeze-and-handoff counting-standard annotation.

### §1.11 `OuterGateReceipt@v0` — G6
- `transform_version: Literal["hmac-sha256-v1"]` — REQUIRED. Deterministic label for the transform primitive (§21.2 "pseudonymisation with a purged mint").
- `key_fingerprint: str` (64 hex chars) — REQUIRED. SHA-256 hex of the mint key material. **NEVER the key itself.**
- `mint_window_id: str` — REQUIRED. UUID of the mint window; the window's key is purged at end.
- `applied_transformations: List[str]` — Ordered list of transformation labels (e.g. `["pseudonymise:unit_id", "pseudonymise:source_ref", "generalise:feed_id", "pseudonymise:load_bearing_unit_ids[]"]`). **Category labels only; no values.**
- `input_identifier_categories: List[str]` — Categories present in the pre-egress artifact.
- `applied_at: str` — REQUIRED. ISO-8601 UTC.
- `run_id: str`, `trace_id: str` — REQUIRED. Correlation.
- `artifact_ref: LedgerArtifactRef` — REQUIRED.
- `k_anonymity_bucket_size: Optional[int] = None` — k parameter (§21.2). None at v0 (closed-seam).
- `differential_privacy_epsilon: Optional[float] = None` — DP epsilon (§21.2). None at v0.

### §1.12 `V2RefusalEnvelope@v0` — G6
- `reason_code: Literal["lawful_basis_absent", "substrate_rights_expired", "sample_file_out_crypto_verify_failed", "cumulative_disclosure_risk"]` — REQUIRED. One of four V2 refusal grounds (§29.1 + §30). Unknown reason_code → pydantic ValidationError (no partial-egress escape hatch).
- `refused_at: str` — REQUIRED. ISO-8601 UTC.
- `run_id: str`, `trace_id: str`, `artifact_ref: LedgerArtifactRef` — REQUIRED.
- `lawful_basis_ref: Optional[str] = None` — What was checked (§30). None if refusal is `lawful_basis_absent`.
- `substrate_contract_ref: Optional[str] = None` — What was resolved against for rights (§29.1).
- `detail: str = ""` — Deterministic reason string, no PII (§30).

### §1.13 `CumulativeDisclosureLedger@v0` — G6
- `mint_window_id: str` — REQUIRED. UUID; window key purged at close.
- `egress_fingerprints: List[str]` — SHA-256 hex fingerprints of prior egress artifacts. Empty at G6 v0 (arm closed).
- `k_threshold: Optional[int] = None` — k in k-anonymity (§21.2). None at v0 (closed-seam).
- `l_threshold: Optional[int] = None` — l in l-diversity. None at v0.
- `epsilon_budget: Optional[float] = None` — cumulative DP epsilon budget. None at v0.
- `arm_admitted: bool = False` — Whether the arm is opened. False at v0 per §29.1 "Until V2 passes" + §32 DPO-owned pattern.

Config unlock path (mirrors `services/v2_gate/cumulative.py::cumulative_arm_admitted()`): set all three env vars `RMS_G6_K_ANONYMITY_THRESHOLD`, `RMS_G6_L_DIVERSITY_THRESHOLD`, `RMS_G6_DP_EPSILON_BUDGET`.

### §1.14 `Service1Refusal@v0` — A2 (post-G6 targeted freeze)
- `outcome: Literal["refused"] = "refused"` — REQUIRED. Load-bearing discriminator; distinguishes a governed refusal from FastAPI's default validation-422 (which has `detail: list` and NO `outcome`). Frontend keys on `body.outcome === "refused"`.
- `reason: str` — REQUIRED. One of `no_defensibility_floor` | `no_lawful_basis` | `composition_below_floor`.
- `run_id: str` — REQUIRED. Run correlation ID.
- `trace_id: str` — REQUIRED. Trace correlation ID.
- `asked: str` — REQUIRED. Plain-language objective (from request `objective_text`). Interface Spec §201 (`asked: <objective + required floor, in plain terms>`).
- `supported_class: Optional[DefensibilityClass] = None` — Highest class the input evidence supports (max over per-unit Ring-5-governed `defensibility_class`). `None` for pre-composition refusals (`no_defensibility_floor`, `no_lawful_basis`) where no aggregate has been computed. Interface Spec §186-190, §202-203.
- `what_would_raise_it: str` — REQUIRED. Actor-appropriate hint per Interface Spec §204 categories (corroboration / accountable source). Static per-reason lookup at `services/service_1/refusal_hints.py`.

**Envelope shape at HTTP layer:** flat top-level fields (Option A per A2 D3a). Returned by `POST /api/service_1/run` via `JSONResponse(status_code=422, content=refusal.model_dump())`. NOT nested under `detail`. This is the discriminating structural difference from FastAPI's validation-422 body.

**D6a doctrine:** `supported_class` reads the per-unit Ring-5-governed `defensibility_class` already stamped on each `NormalizedUnit.defensibility`. It never recomputes the class from Rings 1-4 signals. Single-source, no divergence surface.

---

## §2. API routes (20 registered `/api/*` routes)

| # | Path | Method | Request | Response | Errors | Read-only? | Source §-anchor | Phase |
|---|---|---|---|---|---|---|---|---|
| 1 | `/api/health` | GET | — | `{status, app, gate, time}` | — | Y | Boot sanity | G0 |
| 2 | `/api/system/state` | GET | — | Dict (gate, data_source, contracts_frozen, g5a_components, g6_components, closed_seams, engines_resolvable_by_trace_id, cumulative_arm_status, cumulative_arm_config_unlock_path) | — | Y | Deliverable 3.c | G0 |
| 3 | `/api/contracts/five_rings` | GET | — | JSON schema of `NormalizedUnit` | — | Y | OpenAPI contract surfacing | G0 |
| 4 | `/api/contracts/objective_request` | GET | — | JSON schema of `ObjectiveRequest` | — | Y | OpenAPI contract surfacing | G0 |
| 5 | `/api/contracts/qualification_matrix` | GET | — | JSON of Matrix v0 | — | Y | OpenAPI contract surfacing | G0 |
| 6 | `/api/v1/status` | GET | — | `V1StatusResponse` (harness state) | — | Y | Hard Rule 1 (V1) | G0.5/G1 |
| 7 | `/api/v3/status` | GET | — | `V3StatusResponse` (measurement harness) | — | Y | G1 substrate | G1 |
| 8 | `/api/v1/stamp_audit/recent` | GET | — | `List[StampAuditEntryDTO]` | — | Y | Ring buffer (G1) | G1 |
| 9 | `/api/v1/stamp_audit/by_unit/{unit_id}` | GET | — | `List[StampAuditEntryDTO]` | 404 | Y | Ring buffer (G1) | G1 |
| 10 | `/api/northena/status` | GET | — | Dict | — | Y | Northena §14 | G2a |
| 11 | `/api/northena/ledger/open_runs` | GET | — | `List[str]` (run_ids) | — | Y | Northena §7.2 | G2a |
| 12 | `/api/northena/ledger/by_run/{run_id}` | GET | — | `List[LedgerRow]` | — | Y | Northena §7.2 | G2a |
| 13 | `/api/northena/trace/{trace_id}` | GET | — | `TraceLensEnvelope` | 400 (malformed), 404 (not found), 405 (non-GET) | Y — write-delta invariant | Interface Spec §16 invariant #9 + Northena §7.2/§7.3/§12/§14 + Product v2.1 §8 | **G5a** |
| 14 | `/api/solva/status` | GET | — | Dict | — | Y | Solva §18 | G1/G3 |
| 15 | `/api/solva/trace/{trace_id}` | GET | — | Solva trace dict | 404 | Y | Solva §13 | G3 |
| 16 | `/api/service_1/status` | GET | — | Dict | — | Y | Product v2.1 §8.4 | G4 |
| 17 | `/api/service_1/run` | POST | `Service1RunRequest` (see below) | `Service1RunSummary` (200) OR `Service1Refusal@v0` (§1.14, 422 with `outcome="refused"`) | 422 governed refusal (see §2.1); 422 validation (Pydantic, `detail: list`, distinguishable from refusal by presence of `outcome`); 500 ONLY on infrastructure fault (`outcome` never == "refused") | N — WRITE endpoint | Product v2.1 §8.4 + §11; Interface Spec §5.4 refusal state | G4 + **A2 refusal envelope** |
| 18 | `/api/service_1/run/{run_id}` | GET | — | `Service1RunStatus` | 404 | Y | Product v2.1 §8.4 | G4 |
| 19 | `/api/discipline/lift_manifest` | GET | — | `LiftManifestEnvelope` | 405 (non-GET) | Y — write-delta invariant | Interface Spec §16 governance-legibility | **G5a** |
| 20 | `/api/handoff/backend_contract_surface_v1` | GET | — | `text/markdown` attachment (this document) | 404 (artifact absent, structured envelope `{reason:"handoff_artifact_not_found", path}`), 405 (non-GET) | Y — write-delta invariant | Interface Spec §16 governance-legibility (handoff artifact = governance record, download-scope of the same record) | **post-G6 freeze-handoff** |

**FastAPI-managed doc surfaces** (auto-generated by the framework; not application routes):
- `/api/openapi.json` — full OpenAPI 3.1 schema.
- `/api/docs` — Swagger UI.
- `/api/redoc` — ReDoc.

**G6 note**: no new HTTP route shipped at G6. Outer-gate receipts + V2 refusals absorb into ledger rows and surface via the existing `GET /api/northena/trace/{trace_id}` (route #13) as `LedgerRow.stamp_audit` payload. This is the spec-anchored "same record, two scopes" pattern (Interface Spec §16 invariant #9). Any future POST route for explicit outer-gate emit would be a G6+ extension surface.

### §2.1 Detailed route: `POST /api/service_1/run` (route #17)

Request contract: `Service1RunRequest` (defined in `backend/routers/service_1.py`):
```json
{
  "artifact_id": "portfolio-mandate-abc",
  "artifact_version": "v0",
  "lawful_basis": "dpa-lawful-basis-ref",
  "floor": "utterance",
  "scope_key": "portfolio",
  "objective_text": "did last week's coverage under-index electoral court decisions?",
  "units": [ /* array of NormalizedUnit@v0, see §1.1 */ ]
}
```

Success response (`200`): `Service1RunSummary`:
```json
{
  "run_id": "run-abc12345",
  "trace_id": "trace-xyz67890",
  "mining_plan_id": "plan_...",
  "registry_snapshot_ref": "snap-...",
  "converged_unit_count": 21,
  "defensibility_floor": "utterance",
  "ledger_correlation_ref": "run-abc12345",
  "yield_layer_version": "core-only"
}
```

Governed refusal response (`422` with `outcome="refused"`): `Service1Refusal@v0` (§1.14). Flat body, top-level fields. Example (composition-below-floor):
```json
{
  "outcome": "refused",
  "reason": "composition_below_floor",
  "run_id": "run-abc12345",
  "trace_id": "trace-xyz67890",
  "asked": "did last week's coverage under-index electoral court decisions?",
  "supported_class": "utterance",
  "what_would_raise_it": "No corroboration at the required standard was found for the load-bearing claims. Lower the floor, or narrow the objective to better-sourced material."
}
```

**Three refusal branches** (all return HTTP 422 with `outcome="refused"`):
1. `no_defensibility_floor` — `floor` field missing/null. `supported_class: null` (pre-composition; no aggregate computed).
2. `no_lawful_basis` — `lawful_basis` empty/whitespace. `supported_class: null` (pre-composition).
3. `composition_below_floor` — Targeta filtered every input unit out (`len(eligible) == 0`). `supported_class` = `max` over per-unit Ring-5-governed classes on the INPUT units.

**Validation-422 vs refusal-422:** the frontend distinguishes by BODY discriminator, NOT status code. A validation-422 (e.g. missing `artifact_id`) has `{"detail": [{...list of Pydantic error items...}]}` and NO top-level `outcome`. A refusal-422 has `outcome === "refused"` at top level. Never infer refusal from status code alone.

**Infrastructure fault (`500`):** any uncaught exception (Mongo outage, unexpected `ValidationError` deep in the composition pipeline, etc.) surfaces as a bare `500`. The body will NEVER carry `outcome === "refused"`. Distinguishable from refusal by absence of the discriminator; render as a system error, never as a refusal.

### §2.2 Detailed route: `GET /api/northena/trace/{trace_id}` (route #13)

Request: path param `trace_id: str` (1–128 chars, non-whitespace).
Response: `TraceLensEnvelope` (§1.9).
Errors:
- 400 `{"detail": {"reason": "malformed_trace_id", "trace_id": "..."}}` — path param empty/whitespace/>128 chars.
- 404 `{"detail": {"reason": "trace_id_not_found", "trace_id": "..."}}` — no ledger rows for this trace_id.
- 405 — any non-GET method.

Read-only invariant: `backend/tests/invariants/test_trace_lens_readonly.py` asserts Mongo `serverStatus.opcounters` write-delta == 0 across 200/404/400/405.

Cross-engine correlation guarantee: `test_trace_lens_cross_engine_correlation.py` — one trace_id resolves the 5-engine universe.

### §2.3 Detailed route: `GET /api/discipline/lift_manifest` (route #19)

Response: `LiftManifestEnvelope` (§1.10). Freshness: full disk-read of `docs/lift_manifest.json` + live-computed spec fingerprints per `docs/mandates/*.md` + Rule 2 accounting per phase on every hit. No cache.

Read-only invariant: same Mongo write-delta discipline.

---

## §3. Read-only invariants & correlation guarantees

### §3.1 Read-only routes (Mongo write-delta == 0)

Routes 13 (`/api/northena/trace/{trace_id}`) and 19 (`/api/discipline/lift_manifest`) are contract-frozen READ-ONLY: enforced via `test_trace_lens_readonly.py` opcounter snapshots before/after every hit across 200/404/400/405 case-classes.

Additionally, routes 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18 are GET-only by definition (any POST/PUT/PATCH/DELETE returns 405). Only route 17 (`POST /api/service_1/run`) is a write endpoint.

### §3.2 Cross-engine trace correlation guarantee

**One `trace_id` resolves unit / reasoning / audit across 5 engine boundaries:**
- `northena_ledger` — always resolved (admit + gate + converge rows).
- `solva` — resolved when `stamp_audit` contains a SolvaTrace shape.
- `targeta` — resolved via `LedgerRow.reason` prefix `targeta_plan_built:{plan_id}` → MiningPlan by id.
- `mtafiti` — resolved transitively via `MiningPlan.ordered_targets.source_ref` → Registry.
- `service_1` — resolved via `LedgerRow.reason` prefix `service_1_converged:`.

**Frontend obligation:** the Consumer Terminal's "trust-receipt" URL (design anchor 1 below) hits route 13 and expects this 5-engine resolution. If any engine fails to resolve for a trace_id that has that engine in its universe, the envelope surfaces the absent engine in `engines_touched` (sorted set); the frontend renders the partial reality, not a synthetic-complete lie.

### §3.3 Stamp-audit envelope discipline (Northena §14 side-channel)

**Zero field additions to `northena_ledger_row@v0` across G3, G4, G5a, G6.** All engine artifacts absorb into the permissive `stamp_audit: Optional[Dict]` field:

| Engine artifact | stamp_audit shape |
|---|---|
| Solva trace (G3+) | `{unit_id, decision, reason, stages: [...], computed_class, load_bearing_unit_ids, conclusion, ...}` — bare-key at top of stamp_audit |
| Outer-gate receipt (G6) | `{"outer_gate_receipt": {...OuterGateReceipt fields...}}` |
| V2 refusal (G6) | `{"v2_refusal": {...V2RefusalEnvelope fields...}}` |

**HAZARD-STOP (a) tripwires** (all currently pass):
- `test_northena_ledger_row_contract_snapshot_unchanged_at_g6` — snapshot byte-identical.
- `test_no_new_stage_literal_at_g6` — stage enum stays `{admit, gate, converge}`.
- `test_no_new_decision_literal_at_g6` — decision enum stays the 7 pre-G6 literals.

---

## §4. Refusal semantics (V2 + composition-time floors)

**The frontend MUST render refusals as a first-class state** (Gate Condition 2 per §5.4 below).

Every refusal path with contract + route + §-anchor:

| Refusal | Contract | Route where surfaced | Source §-anchor |
|---|---|---|---|
| **V2 refusal** (outer-gate egress) | `V2RefusalEnvelope@v0` (§1.12) | Absorbed via `POST /api/service_1/run` when the run terminates in a V2-refused egress; visible via `GET /api/northena/trace/{trace_id}` (`LedgerRow.stamp_audit.v2_refusal`) with `LedgerRow.decision == "refused"` and `reason` prefixed `v2_refused:`. | Product v2.1 §29.1 + §30 |
| **Service 1 composition-time floor refusal** | `Service1Refusal@v0` (§1.14) — six fields: `outcome`, `reason`, `run_id`, `trace_id`, `asked`, `supported_class`, `what_would_raise_it` | Returned inline by `POST /api/service_1/run` as HTTP `422` with flat body carrying `outcome="refused"`. Distinct from FastAPI validation-422 by the presence of the top-level `outcome` field. NOT a 500. See §2.1 for shape + 3 reason codes. | Product v2.1 §8.4 + Interface Spec §183-210 (behavioural refusal table) + Interface Spec §201/§186-190/§204 (`asked` / `supported` / `to_raise` semantics) |
| **Solva assertion-boundary refusal** | Solva trace with `computed_class = "non_factual"` (or below-floor) | Absorbed into `LedgerRow.stamp_audit` on the converge row; visible via `GET /api/northena/trace/{trace_id}` (`solva_traces` in envelope). | Solva Spec §7 assertion boundary |
| **Northena Admit refusal** | `LedgerRow` with `stage="admit", decision="refused"` | `GET /api/northena/ledger/by_run/{run_id}` and `GET /api/northena/trace/{trace_id}`. | Northena §12 |
| **Northena Gate refusal** (routing) | `LedgerRow` with `stage="gate", decision="refused"` | Same as above. Distinguished from V2 refusal by `reason` prefix (Northena gate refusals are out-of-scope routing; V2 refusals prefix `v2_refused:`). | Northena §12 + Product v2.1 §22.1 |

**Structural discipline:** every refusal envelope carries `reason`/`reason_code` + correlation identifiers (`run_id`, `trace_id`, `artifact_ref`). The `Service1Refusal@v0` envelope carries the four surface-rendering fields the frontend needs verbatim (`asked`, `supported_class`, `what_would_raise_it`, plus `outcome` as discriminator). The frontend renders "asked / supported class / what would raise it" per §5.4 obligation — for Service 1 refusals this is backed directly by the frozen envelope; for other refusal types (V2, Solva, Northena) the frontend synthesises the render from the correlated ledger row + stamp-audit payload.

---

## §5. G5b design anchors and load-bearing gates (locked by user)

### §5.1 Design Anchor 1 — Trust-receipt URL

- Resolves by `trace_id`, read-only, the SAME record the audit lens sees at a public-facing scope.
- Backend route: `GET /api/northena/trace/{trace_id}` (route #13, from G5a).
- Response contract: `TraceLensEnvelope@v0` (§1.9).
- Frontend obligation: attach a `trace-receipt` URL to every intelligence response rendered on the surface.
- Not a new artifact — same record, two scopes. (Interface Spec §16 invariant #9.)

### §5.2 Design Anchor 2 — Outer-gate receipt inline in Consumer Terminal

- Glance-view render of: transform version, mint window ID, key fingerprint (never key material), applied transformations, input identifier categories.
- Backend contract: `OuterGateReceipt@v0` (§1.11).
- Explicit rendering constraint: **fact and fingerprint of the transform only; nothing about the mint or pre-image that could aid reversal.** This is the surface expression of §21.2 "anonymised, not de-identified."

### §5.3 Load-Bearing Gate 1 — Class inseparable on the surface

- No route or component state may render claim text without its defensibility class.
- Structural, testable as: "is there any path in the React app that shows a claim without its class?" → must be NO.
- The frontend testing pass will include a static analysis / component-tree traversal invariant asserting this.
- Backend prerequisite: every payload that carries claim text also carries its defensibility class in the same envelope. These payloads carry the class; Gate 1's build-time test enforces completeness (contract snapshot invariants defend the shape at each freeze — §1.6 `LedgerRow`, §1.7 `MtafitiRegistryRecord.defensibility_class`, §1.9 `TraceLensEnvelope.solva_traces.computed_class`, §1.14 `Service1Refusal.supported_class`).

### §5.4 Load-Bearing Gate 2 — Refusal as a first-class state

- A below-floor objective (or any refusal) renders the structured refusal view: asked / supported class / what would raise it.
- Never an empty result. Never a generic error.
- Every refusal envelope contract (§4 above) must have a corresponding first-class render surface.
- **For Service 1 refusals, this is now directly backed by `Service1Refusal@v0` (§1.14).** The envelope carries the three semantic fields (`asked`, `supported_class`, `what_would_raise_it`) verbatim as top-level keys, plus `outcome="refused"` as the discriminator. HTTP status is 422; frontend distinguishes governed refusal from validation-422 by the presence of `outcome`, not by the status code.

---

## §6. Substrate handoff manifest

The frontend specialist reads these directly for design intent beyond the contract shapes documented here. All at `/app/docs/mandates/` with SHA-256s from `MANIFEST.md`:

| Spec | Filename | SHA-256 (over .docx source) |
|---|---|---|
| Solva | `RMS_Solva_Specification.md` | `f375b5acfe949682122c7a2f5954512acd262a25bb9c8db124d2995c2fa297db` |
| Targeta | `RMS_Targeta_Specification.md` | `aae06440c6af3b72d870151faa79932f873ad3fa214403363d33e75500889fad` |
| Mtafiti | `RMS_Mtafiti_Specification.md` | `8e4a7ece76bd5fcc3f0a9a0e1b019bc19a12bd5b69c46560a424350ff463a7db` |
| Northena | `northena.md` | `74c4a5ccb74de5ca26f05b5269153846af72f6b60cad2903486b80a57fa1f355` |
| RMS Product & Engineering | `RMS_Product_Engineering_Spec_v2.1.md` | `9f956e470c9f06e36581f3d12413d5cfffc3ecd54dedecbfdb431a36cf2751f7` |
| RMS Interface | `RMS_Interface_Specification.md` | `25653e46a815ddd7cd0b0a3454fbe543eb635eaf960695b2a2ffe206148d30ac` |
| RMS UX Architecture | `RMS_UX_Architecture_Specification.md` | `88c487a51fce687e11697d384a04b092b70b80f05bd7e5e0ed0f9bce89bfa41d` |

Substrate-drop gate `backend/tests/invariants/test_substrate_drop_gate.py` re-computes these SHA-256s at every CI run; drift → CI red.

---

## §7. Hazard-stop framing for the frontend specialist

The 4 backend hazard-stops apply verbatim to the frontend layer:

- **(a) Contract mutation demand.** A frontend need requiring a change to any contract in §1 or any route in §2 is a HAZARD-STOP. Do not extend contracts to accommodate frontend convenience. Surface the demand: which contract, which field, which spec §-anchor forces the change. If no §-anchor forces it → the frontend accommodates the backend, not the reverse.
- **(b) Governance decision needed.** A closed-seam threshold (Owner/DPO-owned) must be configured, not invented. Four seams at G6: Mtafiti V3 overlay (Owner thresholds); Targeta yield (Owner); Northena Ledger retention (DPO); V2 cumulative-disclosure arm (DPO env vars). Frontend surfaces the closed state; does not fabricate thresholds.
- **(c) Substrate absent.** A spec §-anchor referenced by an existing route or contract is missing from `/app/docs/mandates/`. Surface as HAZARD-STOP; substrate-drop gate CI would already have caught it, but a live discovery during frontend work is a valid trigger.
- **(d) Rule 2 v2 trips.** Under strict counting standard (post-§0), the frontend phase G5b's discretionary LoC will be scrutinised the same way G6's was. Stop-and-judge if net-new discretionary exceeds lifted-verifiable; ratify-with-documentation if the mandate forces the structure.
- **(e) G6-specific holdover.** If a closed-seam requires a threshold to be expressed on the surface (e.g. rendering "V2 cumulative-disclosure arm: closed, awaiting DPO thresholds"), surface the state truthfully — don't invent a threshold to render.

---

## §8. Handoff certification

- **Frozen at:** 2026-07-02T01:00Z; **A2 refusal-envelope amendment:** 2026-07-02T02:15Z
- **CI at freeze:** 340/340 (green); **CI at A2:** 355/355 (green)
- **Frozen contracts:** 14 (Service1Refusal@v0 added as 14th at A2)
- **Routes enumerated:** 20 registered `/api/*` (excluding FastAPI-managed docs surfaces)
- **HAZARD-STOPs open at freeze:** NONE; **HAZARD-STOPs raised during A2:** NONE (§204/§247 wording check confirmed content-categories-only, HAZARD-STOP (f) did not fire)
- **Counting standard:** post-§0-strict from G6 forward; pre-§0 for phases G3/G4/G5a annotated in place, no retroactive recount
- **Signature:** `backend-contract-surface-v1.1-a2-e1_dev-20260702T021500Z` (supersedes `-v1-freeze-e1_dev-20260702T010000Z`; the v1 signature remains valid for the pre-A2 sub-surface)

**FROZEN. READ-ONLY. Any consumer needing a change surfaces HAZARD-STOP (a), not a negotiation.**
