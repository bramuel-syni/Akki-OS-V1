# G5a scope from source — pre-code note

**Sources:**
- `/app/docs/mandates/RMS_Interface_Specification.md` (§11 response contract; §14 governance surface; §16 invariant #9)
- `/app/docs/mandates/northena.md` (§7.2 LedgerRow shape with `run_id + trace_id`; §12 Ledger absorbs stamp-audit by `unit_id + trace_id`; §14 interfaces + test obligations)
- `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` (§8 unit and audit are separate envelopes with different lifecycles, joined by `trace_id`)

**Spec-filename disambiguation**: the brief references `RMS_Northena_Specification.md`; on-disk (per `MANIFEST.md` + `phase_source_requirements.yaml`) the Northena spec is filed as `northena.md`. Same content; the substrate-drop gate for G5a passes against the on-disk name.

**CI baseline at G5a opening**: 271/271 green.

---

## 1.1 Route specifications

Neither route has a verbatim path in Interface Spec §11 (which describes the CONSUMER-FACING intelligence response, not the trace-lens read surface). The trace-lens is implied by:
- Interface Spec §16 invariant #9: "One record, seen at two scopes: the DPO's governance surface and a user's audit lens reach the identical record by trace_id."
- Northena §12: Ledger absorbs stamp-audit entries by `unit_id + trace_id`.
- Product v2.1 §8: unit and audit are separate envelopes, joined by `trace_id`.

**Route 1 — trace-lens read surface**:
```
GET /api/northena/trace/{trace_id}
```
- **Method**: GET only. Other methods → 405.
- **Response**: `TraceLensEnvelope` (new frozen contract at G5a) resolving every engine artifact under `trace_id`.
- **Errors**: 404 (unknown trace_id, no ledger rows); 400 (malformed trace_id — empty/whitespace/too-long); 500 (internal).
- **Auth**: G5a defers auth to G5b per Interface Spec §5 (sign-in and routing are frontend concerns; API surface is exposed without auth at G5a). Journaled — G5b lands sign-in.

**Route 2 — lift-manifest read surface**:
```
GET /api/discipline/lift_manifest
```
- **Method**: GET only. Other → 405.
- **Response**: `LiftManifestEnvelope` (new frozen contract) — full manifest + MANIFEST.md SHA-256s + Rule 2 v2 accounting per closed phase + substrate-state markers.
- **Errors**: 500 only (manifest read must succeed for a healthy backend).

## 1.2 Trace correlation topology

Engines that emit records under a `trace_id` in the shipped codebase (G4 close):

| Engine | Where it writes | trace_id-tagged field | file:line |
|---|---|---|---|
| Northena Admit | `services/northena/admit.py::admit` → `LedgerRow(stage='admit')` | `LedgerRow.trace_id` | admit.py:~90 (via `_write_admit_row`) |
| Northena Gate | `services/northena/gate.py::gate` → `LedgerRow(stage='gate')` | `LedgerRow.trace_id` | gate.py:~40 |
| Northena Converge (§13 threshold check) | `services/northena/converge.py::check` | `LedgerRow.trace_id` | converge.py:~40 |
| Northena Converge (§13 Solva absorption) | `services/northena/converge.py::absorb_solva_trace` | `LedgerRow.trace_id`, `stamp_audit={SolvaTrace}` | converge.py:~55 |
| Northena Ledger (§7.3 stamp-audit) | `services/northena/ledger.py::absorb_stamp_audit` | `LedgerRow.trace_id`, `stamp_audit={unit_id, decision, ...}` | ledger.py:~40 |
| Solva SolvaTrace (5 reasoning stages + assertion + refusal) | `services/solva_depth/pipeline.py::run_solva` → returns `SolvaTrace(trace_id, stages[], conclusion)` | `SolvaTrace.trace_id` (embedded in `stamp_audit`) | pipeline.py:~40, trace.py:~30 |
| Solva assertion boundary | `services/solva_depth/assertion.py::conclusion_class` → included in SolvaTrace.conclusion | (indirect via SolvaTrace) | assertion.py:~50 |
| Service 1 v1 (admit + gate + converge sequence) | `services/service_1/service.py::run` writes 3 rows | `LedgerRow.trace_id` (shared across the 3 rows) | service.py:~55, 100, 115 |
| Mtafiti Registry (indirect; keyed by source_ref, NOT trace_id) | `services/mtafiti/registry.py::upsert` | via correlation: MiningPlan carries `registry_snapshot_ref` → resolvable | registry.py:~110 |
| Targeta MiningPlan (indirect; keyed by plan_id, NOT trace_id) | `services/targeta/plan.py::persist` | via correlation: `LedgerRow(stage='gate').reason='targeta_plan_built:{plan_id}'` | plan.py:~70; service.py:~110 |
| Layer A / B / C | NOT trace_id-tagged at G4 shipping state | — | (no writes to ledger at G4; deferred to G5b/G6 when consumer terminal drives the pipeline end-to-end) |

**Correlation resolution walk** (read-only):
1. Read all `LedgerRow`s with `trace_id == X` — Northena engine artifacts.
2. Extract `stamp_audit` blobs from those rows — Solva engine artifacts (when present).
3. Parse `reason` fields for `targeta_plan_built:{plan_id}` — resolve Targeta MiningPlans by plan_id.
4. For each resolved MiningPlan, extract `registry_snapshot_ref` — resolve Mtafiti Registry records at that snapshot (content-hash) via a run-scoped index. **NB**: current shipping state does NOT persist snapshot-ref → records mapping; the Registry is a rolling store. G5a addresses this by reading the CURRENT Registry state at resolution-time, filtering by `source_ref`s referenced in the plan's `ordered_targets`. Fail-toward-caution: if a Registry record has changed since plan build, the resolved record is the CURRENT one (fresh); the lens surfaces this via a `registry_freshness: current_vs_snapshot` marker.
5. Parse `reason` fields for `service_1_converged:` — mark Service 1 as engines-touched.

**engines_touched** enum in envelope: `{northena_ledger, solva, targeta, mtafiti, service_1}`.

## 1.3 Read-only invariant scope

Persistent stores touched by trace-lens route:
- `db["northena_ledger_rows"]` (Northena Ledger)
- `db["mtafiti_registry_records"]` (Mtafiti Registry)
- `db["targeta_mining_plans"]` (Targeta plans)

Read-only enforcement: `test_trace_lens_readonly.py` captures Mongo command counts (via `command_started` listener or a lightweight before/after `db.command('serverStatus')['opcounters']` snapshot) across ALL collections before + after route hits, and asserts:
- Total `insert + update + delete + findAndModify` count on `db` is identical before + after.
- No `bulkWrite` variants either.
- Applied to: unknown trace_id (404 case), malformed trace_id (400 case), known trace_id (200 case), method-not-allowed cases (405).

## 1.4 Lift-manifest route specifics

Response includes:
- `manifest_version`, `manifest_semantics`, `generated_at`, `generated_by` (from `docs/lift_manifest.json`).
- `entries: List[LiftEntry]` — full manifest entries (84 at G4 close).
- `substrate_state`, `substrate_settled_at` — from the manifest.
- `source_specs: List[{filename, sha256}]` — computed live from `docs/mandates/MANIFEST.md` (re-read on each request; freshness test asserts this).
- `phase_accounting: Dict[phase_name, Rule2Accounting]` — Rule 2 v2 numbers per closed phase (`{lifted_verifiable, net_new_discretionary, mandate_forced_net_new, overall_ratio, discretionary_only_ratio, journal_ref}`). Read from a small dedicated file `/app/docs/rule2_accounting.json` (authored at G5a from BUILD_JOURNAL data — a machine-readable mirror of the journal narrative).

Response invariants:
- MANIFEST.md SHA-256s for all 7 filed specs surface in `source_specs`.
- Rule 2 v2 rows for G0.5 / G1 / Pre-G2 / G2a / G3 / G4 surface in `phase_accounting` (UNKNOWN acceptable for early phases; phase entries MUST exist).
- Route re-reads `docs/lift_manifest.json` on every hit (or serves a fresh-checked cache). Never serves stale.

## 1.5 Cross-spec contract hazard check

Reviewed all 8 existing frozen contracts + G3/G4-authored dataclasses. G5a route surface consumes existing shapes; no mutation demanded.

**New frozen contracts implied (additions, not mutations)**:
1. `TraceLensEnvelope` at `contracts/trace_lens.py`.
2. `LiftManifestEnvelope` at `contracts/lift_manifest_response.py`.

Both authored + snapshot + invariant. **HAZARD-STOP (a) NOT RAISED.**

## Ready-to-code checklist

- [x] Interface Spec §11 + §16 anchors mapped
- [x] Northena §7.2 + §12 + §14 anchors mapped
- [x] Product v2.1 §8 correlation semantics mapped
- [x] 2 new frozen contracts identified as ADDITIONS
- [x] Correlation walk defined (5 engines resolvable at G4 shipping state)
- [x] Read-only invariant scope defined (3 Mongo collections)
- [x] HAZARD-STOP inventory: none raised at scope-note stage
