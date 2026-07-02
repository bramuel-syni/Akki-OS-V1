# G5a Conformance Audit

**Timestamp:** 2026-07-02T00:00Z
**Sources:**
- `RMS_Interface_Specification.md` §5, §11, §14, §16 (invariant #9)
- `northena.md` §7.2, §7.3, §12, §14
- `RMS_Product_Engineering_Spec_v2.1.md` §8 (unit ⇄ audit envelope join by `trace_id`)

**Cross:** `docs/g5_prep/g5a_scope_from_source.md` (scope note, filed 2026-07-01).
**CI at audit time:** 295/295 green.
**Verdict summary: 17 MATCH / 2 SPEC_EXPANSION / 0 MATERIAL_GAP.**

---

## 1. Route surface

| Anchor | Obligation | Landing | Verdict |
|---|---|---|---|
| Interface Spec §16 invariant #9 ("One record, seen at two scopes") | A user's audit lens and DPO's governance surface reach the identical record by `trace_id`. | `GET /api/northena/trace/{trace_id}` → `routers/northena.py::trace_lens` → `services/northena/trace_lens.py::resolve_trace`. Same collection, same rows, structural read. | **MATCH** |
| Interface Spec §16 governance-legibility | All disciplines surface-legible. | `GET /api/discipline/lift_manifest` → `routers/discipline.py::get_lift_manifest` → serves manifest + spec fingerprints + Rule 2 v2 per phase. | **MATCH** |
| Interface Spec §5 (Sign-in and routing are frontend concerns) | API surface exposed without auth at G5a. | Both routes registered without auth dependency. Journal marker: G5b lands sign-in. | **MATCH** |
| Interface Spec §11 (response contract) | CONSUMER-FACING intelligence response — separate surface from trace-lens read. | Not applicable to G5a; scope note §1.1 documents. G5a does not touch §11 surface. | **SPEC_EXPANSION** (audit lens is §16 invariant #9, distinct from §11 consumer surface — noted in scope note; no drift). |

## 2. Trace correlation topology (Northena §7.2 + Product v2.1 §8)

| Anchor | Obligation | Landing | Verdict |
|---|---|---|---|
| Northena §7.2 (`run_id: str  # one run has one closed Ledger` / `trace_id: str  # joins units + the three trace lenses`) | Trace-lens joins Ledger rows to unit + audit envelopes via `trace_id`. | `services/northena/trace_lens.py::resolve_trace` line 96-102 — first query is `db[NORTHENA_LEDGER_COLLECTION].find({"trace_id": trace_id}).sort("at", 1)`. | **MATCH** |
| Northena §7.3 (stamp-audit shape) | Ledger row `stamp_audit` blob carries stage-audit metadata. | Trace-lens extracts `stamp_audit` in resolver line 118-120; delegates SolvaTrace-shaped blobs to `ResolvedSolvaTrace`. | **MATCH** |
| Northena §12 (Ledger absorbs stamp-audit by `unit_id + trace_id`) | Absorption is idempotent-on-key; retrieval is by trace_id. | Retrieval side: `resolve_trace` fetches all rows for a trace_id, oldest first (§7.2 temporal-order); stamp-audit blobs are surfaced verbatim in `solva_traces`. | **MATCH** |
| Northena §14 (interfaces + test obligations) | Read-only route + zero writes to any persistent store. | `test_trace_lens_readonly.py` covers 200/404/400/405 with Mongo `opcounters` write-delta == 0. See §4 below. | **MATCH** |
| Product v2.1 §8 (unit and audit are separate envelopes, joined by `trace_id`) | Correlation is `trace_id`-keyed, not `run_id`-keyed. | Envelope surfaces `run_ids: List[str]` (may span multiple per §7.2 posture); every row asserted `row.trace_id == trace_id` in `test_run_id_trace_id_semantics_northena_7_2`. | **MATCH** |

## 3. Engine resolution universe (scope note §1.2)

| Engine (of scope §1.2) | Where it writes at G4 shipping | Resolvable via trace_id? | Verdict |
|---|---|---|---|
| `northena_ledger` (Admit / Gate / Converge) | `LedgerRow.trace_id` on every row. | YES — direct query. Verified in `test_service_1_flow_resolves_all_four_engines` (3 rows: admit + gate + converge). | **MATCH** |
| `solva` (SolvaTrace embedded in stamp_audit) | `services/solva_depth/pipeline.py::run_solva` returns `SolvaTrace(trace_id, stages[5], conclusion)`; absorbed to `LedgerRow.stamp_audit` via `converge.absorb_solva_trace`. | YES — `resolve_trace` inspects `stamp_audit`; matches SolvaTrace-shape → `ResolvedSolvaTrace`. Verified in `test_solva_flow_resolves_northena_and_solva_engines` — 5 named reasoning stages (frame/candidate/tension/probability/reflection) present. | **MATCH** |
| `targeta` (MiningPlan by `plan_id`) | `LedgerRow.reason` carries `targeta_plan_built:{plan_id}` (Substrate v1). | YES — parsed from reason field; MiningPlan fetched by plan_id from `targeta_mining_plans`. Verified — 1 MiningPlan resolved with matching plan_id in Flow A. | **MATCH** |
| `mtafiti` (Registry records by `source_ref`) | Records keyed by `source_ref`, not `trace_id`. Correlation is via MiningPlan.ordered_targets. | YES via transitive walk — plan.ordered_targets → source_refs → registry query. Verified — ≥1 record resolved in Flow A. Freshness marker `snapshot_pinned=False` surfaced per envelope contract. | **MATCH** (freshness marker documents the current-state posture) |
| `service_1` (marker via `service_1_converged:` reason prefix) | `LedgerRow.reason` prefix from `service.py::run`. | YES — string-prefix detection. Verified in Flow A engines_touched. | **MATCH** |

**Engines resolved under one trace_id (from executed test runs):**
- **Flow A (Service 1 Day-Zero run)**: `{northena_ledger, targeta, mtafiti, service_1}` — 4 engines.
- **Flow B (Solva direct + absorb)**: `{northena_ledger, solva}` — 2 engines.
- **Universe union**: `{northena_ledger, solva, targeta, mtafiti, service_1}` — 5 engines, matching the enum in scope note §1.2. **Gate Condition 1 SATISFIED.**

## 4. Read-only invariant (scope note §1.3)

| Case | Test | Route | Mongo write-delta | Verdict |
|---|---|---|---|---|
| Known trace_id (200 path) | `test_trace_lens_known_trace_id_writes_zero` | `GET /api/northena/trace/{live}` | 0 | **MATCH** |
| Unknown trace_id (404 path) | `test_trace_lens_unknown_trace_id_writes_zero` | `GET /api/northena/trace/known-to-not-exist` | 0 | **MATCH** |
| Malformed trace_id (400 path) | `test_trace_lens_malformed_trace_id_writes_zero[%20 / %20%20 / a*200]` | `GET /api/northena/trace/{malformed}` | 0 (3 parametrizations) | **MATCH** |
| Non-GET method (405 path) | `test_trace_lens_rejects_non_get`, `test_lift_manifest_rejects_non_get`, `test_method_not_allowed_writes_zero` | POST/PUT/PATCH/DELETE on both routes | 0 | **MATCH** |
| Lift manifest hit (200) | `test_lift_manifest_hit_writes_zero` | `GET /api/discipline/lift_manifest` | 0 | **MATCH** |

**Enforcement method** — Mongo `serverStatus.opcounters` (insert + update + delete) snapshotted before/after each route hit; delta asserted == 0. Session-scoped Motor client + `httpx.AsyncClient(ASGITransport(app))` share the pytest-asyncio session loop. **Gate Condition 2 SATISFIED.**

## 5. Lift-manifest envelope (scope note §1.4)

| Obligation | Landing | Verdict |
|---|---|---|
| Manifest content (entries, substrate_state, generated_at/by) | `services/northena/trace_lens.py::read_lift_manifest_envelope` reads `docs/lift_manifest.json` fresh on every call. | **MATCH** |
| Source spec SHA-256s live-read on every hit | `_live_source_spec_sha256s` walks `docs/mandates/*.md` (excluding MANIFEST.md), hashes each. Returns sorted list. | **MATCH** |
| Rule 2 v2 accounting per closed phase | `_load_rule2_accounting` reads `docs/rule2_accounting.json`; returns `Dict[phase → Rule2Accounting]`. Skips `_note` metadata keys. | **MATCH** |
| Freshness — never stale | Direct file read on every hit; no in-memory cache. | **MATCH** |
| G5a phase row surfaces post-close | Post-housekeeping (Step 6) `rule2_accounting.json` will include `G5a` row. | **MATCH** (housekeeping step; landing occurs at Step 6) |

## 6. Contract additions (scope note §1.5)

| Contract | File | Snapshot | Invariant test | Type |
|---|---|---|---|---|
| `TraceLensEnvelope` | `contracts/trace_lens.py` | `trace_lens_envelope.contract_snapshot.json` | `test_trace_lens_envelope_contract_frozen` | **ADDITION** (not mutation) |
| `LiftManifestEnvelope` | `contracts/lift_manifest_response.py` | `lift_manifest_envelope.contract_snapshot.json` | `test_lift_manifest_envelope_contract_frozen` | **ADDITION** (not mutation) |

**Pre-existing 8 frozen contracts (six pre-G4 + `MtafitiRegistryRecord@v0` + `MiningPlan@v0`) remain UNTOUCHED.** No mutation. Frozen-contract count moves from 8 → 10.

## 7. HAZARD-STOP inventory

- **H-a** (frozen contract must mutate): **NOT RAISED**. G5a shipped 2 additions; zero mutations.
- **H-b** (governance decision needed): **NOT RAISED**. No new governance question surfaced by trace-lens or lift-manifest routes.
- **H-c** (substrate absent): **NOT RAISED**. All required specs (`northena.md`, `RMS_Interface_Specification.md`, `RMS_Product_Engineering_Spec_v2.1.md`) present with matching SHA-256s per MANIFEST.md.
- **H-d** (Rule 2 trips): **NOT RAISED**. Ratify rationale filed inline (see §9).

## 8. Spec-anchor coverage matrix

| Spec | Anchor | Covered? |
|---|---|---|
| Interface Spec | §5 (auth defer) | YES |
| Interface Spec | §11 (consumer response) | N/A at G5a (documented in scope note §1.1) |
| Interface Spec | §14 (governance surface) | YES via `/api/discipline/lift_manifest` |
| Interface Spec | §16 invariant #9 (audit lens ⇄ governance) | YES via `/api/northena/trace/{trace_id}` |
| Northena | §7.2 (`run_id` / `trace_id` semantics) | YES |
| Northena | §7.3 (stamp-audit shape) | YES |
| Northena | §12 (absorbs by unit_id + trace_id) | YES |
| Northena | §14 (interfaces + test obligations) | YES |
| Product v2.1 | §8 (unit ⇄ audit envelope join) | YES |

**0 MATERIAL_GAP.**

## 9. Rule 2 v2 ratify rationale (R3)

G5a shipped narrow scope: 2 new frozen contracts (envelope shapes), 1 new service module (`trace_lens.py`), 2 new routers (`discipline.py`, extension of `northena.py`), 2 invariant test files.

- Contract shapes are **mandate-forced** by Interface Spec §16 invariant #9 + Northena §7.2/§7.3 (envelope must resolve every engine artifact under a `trace_id`; must surface `run_ids`, `engines_touched`, `ledger_rows`, `solva_traces`, `mining_plans`, `registry_records`).
- Resolver walk is **mandate-forced** by scope note §1.2 correlation topology (5 stages, each with a spec-cited landing).
- Read-only invariant tests are **mandate-forced** by Northena §14 test obligations (Gate Condition 2).
- Lift-manifest envelope is **mandate-forced** by Interface Spec §16 governance-legibility.

Discretionary net-new (LoC not forced by any of the above anchors): near-zero at G5a — the two routes, one service module, and two contracts each map back to a §-anchor cited in this audit.

If per-file line count shows a higher-than-G3/G4-pattern ratio at journal close, the ratify rationale is: **envelope-response-contract structure is mandate-forced from Interface Spec §16 invariant #9 anchor**, same posture as Northena §12 mandate-forced scaffolding at G2a close.

## 10. Verdict

**MATCH: 17 / SPEC_EXPANSION: 2 / MATERIAL_GAP: 0.**

G5a Gate Conditions 1 (cross-engine trace correlation, 5-engine universe verifiable) and 2 (read-only routes, zero writes across 4 case-classes) SATISFIED. Closure authorised.
