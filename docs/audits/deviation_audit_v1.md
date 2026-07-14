# Deviation Audit v1 · 2026-07-12

**Authority:** Owner-ratified via IF-1 close (STEP A rider). **Source:** Combined-audit reply (2026-07-12 · this session, Part B). **Discipline:** read-only findings; baseline = 64,762 LoC (backend 55,312 + frontend 9,450, excluding salvage/node_modules/pycache).

**Post-IF-1 revision note (2026-07-14):** rows 10/11/12/13/17/18 reclassified to LIVE (evidence surfaced during IF-1 execution: cancellation via `routers/objectives.py`; expiry + delivery_time + fleet_policy via `economics/quote_service.py` + `routers/pricing.py`; audio_batching + shape_as_objective_prefill are spec-gated AST/CI cells). Shave envelope narrowed accordingly.

| # | item | classification | evidence | raw LoC | removal risk |
|---|---|---|---|---:|---|
| 1 | `services/synisense/shield/client.py` | dead | 249 LoC. Only occurrence at `test_no_direct_llm_calls_outside_shield.py:117` is a docstring reference, not an import. Live call path is `fluency_synthesizer.py:180` / `brief_synthesizer.py:114` → direct `from services.synisense.shield import llm_router`. Superseded by chokepoint-at-llm_router (IF-1). | 249 | isolated |
| 2 | `services/synisense/shield/reidentifier.py` | RECONNECTED (IF-1) | 332 LoC. Called at the `llm_router.invoke_with_metering` chokepoint post-IF-1. Exits shave list. | 332 | live |
| 3 | `services/synisense/shield/audit_log.py` | dead (chain-dead behind #1) | 191 LoC. Only in-tree callers were within `client.py:93-101`. Chokepoint reconnection does not carry audit_log (no `user_id`/`consumer_id`/`purpose` context at the seam). Shave with superseding citation. | 191 | isolated |
| 4 | `services/synisense/shield/canonical.py` | dead | 191 LoC. Zero importers. Observability tool per module docstring. | 191 | isolated |
| 5 | `services/synisense/shield/purpose_validator.py` | dead (chain-dead behind #1) | 60 LoC. Only runtime caller was `client.py:31,63,188`. Chokepoint reconnection does not carry purpose_validator (per IF-1 conditional). Shave with superseding citation; ALLOWED_PURPOSES + INTERNAL_ONLY_PURPOSE_PREFIXES in `services/synisense/config.py:73-193` shave with. | 60 | isolated |
| 6 | `services/synisense/shield/deidentifier.py` | RECONNECTED (IF-1) | 686 LoC. Reconnected at chokepoint post-IF-1; spaCy-unloadable → `ServiceUnavailable` propagates → fluency_synthesizer's `LLMUnavailableError` → mechanical arm (AF-E2 amended). Exits shave list. | 686 | live |
| 7 | `services/storage_service.py` | dead | 256 LoC. Zero in-tree importers. | 256 | isolated |
| 8 | `services/data_source/synthetic_assets/rms_adversarial_v1/rejected/generate_fixture.incoming.py` | dead | 347 LoC. `.incoming.py` suffix + `rejected/` sub-dir + docstring "SYNTHETIC - PLUMBING ONLY. NOT V1/V3 VALID." Zero importers. | 347 | isolated |
| 9 | `services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` | dead | 341 LoC. Zero in-tree importers; CLI-only tool with no entry-point wiring. | 341 | isolated |
| 10 | `services/service_1/cancellation.py` | **LIVE (revised 2026-07-14)** | 59 LoC. Imported at `routers/objectives.py:13,40,224` as `cancellation_service` + `tests/invariants/test_phase_5_stage_b_async_delivery.py:39`. Standing Disposition cancellation-is-a-state-not-a-refusal (5th state). | 59 | live |
| 11 | `services/economics/expiry.py` | **LIVE (revised 2026-07-14)** | 40 LoC. Imported at `services/economics/quote_service.py:7` (`expiry.is_expired`) + `tests/invariants/test_phase_6_stage_b_economics.py:41`. Gate 11 config-expiry → governance refusal. | 40 | live |
| 12 | `services/economics/fleet_policy.py` | **LIVE (revised 2026-07-14)** | 86 LoC. Imported at `routers/pricing.py:39` as `_fleet_policy` + served via `GET /api/pricing/fleet_policy` (`:223-228`). Frontend combines this per `routers/operator.py:6` capacity view. | 86 | live |
| 13 | `services/economics/delivery_time.py` | **LIVE (revised 2026-07-14)** | 81 LoC. Imported at `services/economics/quote_service.py:38,153` (`compute_delivery_estimate`). TWO-band delivery per test invariant. | 81 | live |
| 14 | `services/v1_harness/metrics.py` | dead | 34 LoC. `v1_harness/__init__.py` re-exports from `harness.py` + `types.py` only, not from `metrics.py`. Zero importers. | 34 | isolated |
| 15 | `services/perception/purge_attestation.py` | dead | 11 LoC. Zero callers of `attest_purge()`. Test-side references to `.purge_attestation` are field access on `PerceptionResult` (via `contracts/perception_result_v0.py:PurgeAttestation`), NOT module imports. | 11 | isolated |
| 16 | `services/perception/telemetry.py` | dead | 17 LoC. Zero callers of `build_telemetry`. Field references in tests are attribute access on `PerceptionResult.telemetry` (via `contracts/perception_result_v0.py:Telemetry`). | 17 | isolated |
| 17 | `services/perception/gpu_execution/audio_batching.py` | **LIVE (revised 2026-07-14)** | 32 LoC. Required-existence per 9.2a-G5b AST gate (`tests/invariants/test_9_2a_purge_ast_gate.py:34`, `test_9_2a_real_perception.py:378,444` — E5-anti-rule + V1-G5b file inventory). Deletion breaks CI. | 32 | live |
| 18 | `services/opportunity_briefs/shape_as_objective_prefill.py` | **LIVE (revised 2026-07-14)** | 31 LoC. Imported by `tests/invariants/test_opportunity_briefs_ob_g1_to_g5.py:33` as OB-G4 gate cell (`test_ob_g4_shape_as_objective_prefills_reach_only`). | 31 | live |
| 19 | `services/solva_depth/stamp.py` | superseded-alive | 45 LoC. Zero importers. Docstring: G3 v0 pass-through; post-G3 seat. **EXEMPT** per Owner (spec-named). | 45 | entangled — future-binding spec surface |
| 20 | `services/targeta/__init__.py:9` stale comment | superseded-alive | 1 LoC comment. `modes.py` file does not exist; inlined per `docs/audits/g4_targeta_conformance_v1.md:23`. Line replaced in IF-1 close per E4. | 1 | isolated |
| 21 | contract v0/v1 pairs (`async_delivery_accepted`, `outer_gate_receipt`, `northena_ledger`, `objective_request`) | superseded-alive (**EXEMPT**) | v0: 297 LoC total. v1/v2: 485 LoC total. Both consumed across routers/services. **EXEMPT** per Registry Doctrine v1.0 §14 additive-supplement discipline + Parity 31 additive freeze. | 782 | EXEMPT |
| 22 | Frontend `/legacy/*` pages (`src/legacy/pages/`) | superseded-alive | 1,118 LoC across 7 files. `App.js:5-12,88` mounts under `/legacy/*`. Comment: "Legacy G5b operator pages remain nested under `/legacy/*` for continuity." G-7 note: `/legacy/trace/:traceId` is the SOLE rendering of the three-lens commitment. | 1,118 | entangled — Owner-held for G-10 decision |
| 23 | Redundant gates (Registry Q1 lens · same-promise/same-surface duplicates) | none | Deterministic scan of `docs/registry/machine/registry.yaml` — 96 function_ids × (promise × cell) pairs; **0 duplicate keys**. | 0 | — |
| 24 | Salvage boundary (`/app/salvage/`) | isolated (no leak) | `/app/salvage/commercial_cut_2026_07_06/` — 18 files, 276 KB. `grep -RIn 'from salvage\|import salvage' /app/backend /app/frontend` returns **zero import hits** (docstring/comment references only). Boundary intact. | 0 | — |

**Total shaveable LoC (post-IF-1 revised · clear-dead only):** rows 1,3,4,5,7,8,9,14,15,16 = **1,697 LoC** · **2.62%** of live baseline (64,762 LoC).

**Exemptions honored:** row 19 stamp.py (spec-named) · row 20 comment-fix (1 LoC replaced in-place) · row 21 v0/v1 contract pairs · rows 10/11/12/13/17/18 (LIVE evidence surfaced during IF-1 execution) · `/app/salvage` · Standing-Rule-v3 records.

**Reconnected (exits shave):** rows 2 + 6 = 1,018 LoC restored to live-service status.

See also: /app/docs/briefs/outstanding_work_and_gap_register_v1.1.md §4
