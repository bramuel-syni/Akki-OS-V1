# Engine Conformance Audit v1 · 2026-07-12

**Authority:** Owner-ratified via IF-1 close (STEP A rider). **Source:** Combined-audit reply (2026-07-12 · this session, Part A). **Discipline:** capability-based matching per July-1 precedent; on-disk canon reads only (D-11).

## A.0 Canonical engine documents on-disk

| engine | path | sha256 | size | mtime |
|---|---|---|---:|---|
| Northena | `/app/docs/mandates/northena.md` | `ab0beeddf23c9530cc54c6ddd4255b4b3d0435df0d4c156d05de478e65af8345` | 26,303 | 2026-07-02 17:04:12 |
| Targeta | `/app/docs/mandates/RMS_Targeta_Specification.md` | `7e0ca7a373684cf30ca39d6a9c98f3a59e57c29f8ce1179eac0cbef9e4086990` | 25,689 | 2026-07-02 17:04:12 |
| Mtafiti | `/app/docs/mandates/RMS_Mtafiti_Specification.md` | `664fb76680cd8b9e62cfeac084a9d7d9410122a26d692f873c0242b59c78a1da` | 27,783 | 2026-07-02 17:04:12 |
| Solva | `/app/docs/mandates/RMS_Solva_Specification.md` | `e38b0370eed0b065468072a0ab393a66d39760f87c4d12a64f7560b5f0e260b5` | 24,564 | 2026-07-01 15:40:10 |
| Product & Engineering Spec v3 (in-force) | `/app/docs/mandates/RMS_Product_Engineering_Spec_v3.md` | `af2e3cb2fccfd92278dedec725732ae1b5b48dff614fd6f7c8fbc805160d915a` | 19,599 | 2026-07-04 12:55:16 |
| Product & Engineering Spec v2.1 (archived carrier) | `/app/docs/mandates/archive/RMS_Product_Engineering_Spec_v2.1.md` | `510cc1a9f58138cf4753e907fdb68a1b0334b5336eff05db32a3c40071cf484b` | 68,604 | 2026-07-03 21:05:17 |

Companion audits (cited for SUPERSEDED verdicts): `/app/docs/audits/g3_solva_conformance_v1.md`, `/app/docs/audits/g4_targeta_conformance_v1.md`, `/app/docs/audits/g4_mtafiti_conformance_v1.md`, `/app/docs/audits/northena_conformance_v1.md`.

## A.1 Solva

| spec item | verdict | evidence | notes |
|---|---|---|---|
| `services/solva_depth/` layout | BUILT | `/app/backend/services/solva_depth/` — `__init__.py`, `admit_assist.py`, `assertion.py`, `enforce.py`, `interfaces.py`, `load_bearing.py`, `pipeline.py`, `reasoning/`, `stamp.py`, `trace.py` | Matches mandate §7 verbatim. |
| Frame stage | BUILT | `services/solva_depth/reasoning/frame.py:14-21` — `def frame(question, tier_slice)` | Source: mandate §8. |
| Candidate stage | BUILT | `services/solva_depth/reasoning/candidate.py:14-22` — `def candidate(frame_artifact, units)` | Source: mandate §8. |
| Tension stage | BUILT | `services/solva_depth/reasoning/tension.py:14-37` — Ring 3 edges consumed verbatim, "does not average tensions away" | Source: mandate §8. |
| Probability-Bayesian stage | PARTIAL | `services/solva_depth/reasoning/probability.py:14-32` — G3 v0 honest default: equal-weight candidates; LLM binding under `extraction_params@v0 temperature=0` discipline is G3+ implementation seat | Weighting-method seat carried under mandate §18. |
| Reflection stage | BUILT | `services/solva_depth/reasoning/reflection.py:1-34` — returns conclusion + load-bearing units | Source: mandate §8, §9. |
| `load_bearing.py` | BUILT | `services/solva_depth/load_bearing.py:1-27` — returns unit refs only; NO class decision carried | Source: mandate §9. |
| `assertion.py` floor computation | BUILT | `services/solva_depth/assertion.py:1-24` — `conclusion_class` = floor over load-bearing classes; "signature IS the guard" | Source: mandate §10. Attested: `tests/invariants/test_solva_assertion_boundary.py`. |
| `enforce.py` below-floor refusal | BUILT | `services/solva_depth/enforce.py:1-27` — compares against `defensibility_floor`; returns `Assertion` OR structured `Refusal` | Source: mandate §11. |
| SolvaTrace per-stage records | BUILT | `services/solva_depth/trace.py:1-28` — `@dataclass(frozen=True) SolvaTrace` w/ `to_dict()` for Ledger `stamp_audit` | Source: mandate §13. Verified: `tests/invariants/test_solva_trace_ledger_integration.py`. |
| Ring 5 stamp path | BUILT | `services/solva_depth/stamp.py:1-12` — G3 v0 pass-through: preserves Layer C-emitted Ring 5 verbatim | Source: mandate §12. Zero-caller today; post-G3 seat (see deviation row 19). |
| Pipeline seam | BUILT | `services/solva_depth/pipeline.py:1-27` — `run_solva(...)`; imported by `routers/solva.py`, `tests/invariants/test_solva_trace_ledger_integration.py:34` | Source: mandate §7, §15. |
| Router | BUILT | `routers/solva.py` mounted · `services.solva_depth.pipeline.run_solva` invoked | |

## A.2 Targeta

| spec item | verdict | evidence | notes |
|---|---|---|---|
| `services/targeta/` layout | BUILT | `services/targeta/` — `__init__.py`, `core.py`, `gate.py`, `interface.py`, `plan.py`, `yield_layer.py` | |
| `core.py` (deterministic eligibility) | BUILT | `services/targeta/core.py:1-15` — "core.py imports NO ML library"; enforced by `test_core_has_no_ml_import` | Source: mandate §9. |
| `interface.py` (set-preserving boundary) | BUILT | `services/targeta/interface.py:1-12` — `YieldCandidate` excludes `defensibility_floor`/`registry_defensibility` by construction | Source: mandate §10 verbatim. |
| `gate.py` (two-arm gate) | BUILT | `services/targeta/gate.py:1-19` — Arm 1 Helps + Arm 2 Coverage Veto; CLOSED SEAM `admitted=False` unconditional until thresholds configured | Source: mandate §12. |
| `plan.py` (MiningPlan assembly + version stamping) | BUILT | `services/targeta/plan.py:1-14` — reproducible: same Registry + governing artifact + yield-layer version → byte-identical plan_id | Source: mandate §17 #8. |
| `modes.py` (portfolio / per_run orchestration) | SUPERSEDED | `/app/docs/audits/g4_targeta_conformance_v1.md:23` — SPEC_EXPANSION: inlined into `plan.build_plan(mode=…)` | Not ABSENT — see also targeta/__init__.py:9 stale comment (deviation row 20). |
| deterministic eligibility (never imports yield) | BUILT | `tests/invariants/test_targeta_invariants.py::test_core_has_no_ml_import` GREEN | |
| yield-layer seat | BUILT | `services/targeta/yield_layer.py:1-13` — full learned-reorderer path built; CLOSED SEAM at G4 | mandate §17. |
| validation gate (yield admission) | BUILT | `services/targeta/gate.py` — CLOSED SEAM until threshold configured | mandate §11. |
| portfolio mode | BUILT | Per SPEC_EXPANSION — `plan.build_plan(mode="portfolio", ...)`; governing artifact = Portfolio Mandate | |
| per-run mode | BUILT | Per SPEC_EXPANSION — `plan.build_plan(mode="per_run", ...)`; governing artifact = ObjectiveRequest w/ `defensibility_floor` | |
| Contract `targeta_mining_plan@v0` | BUILT/FROZEN | `contracts/targeta_plan.py`; snapshot `targeta_mining_plan.contract_snapshot.json` · parity 31 | |

## A.3 Mtafiti

| spec item | verdict | evidence | notes |
|---|---|---|---|
| `services/mtafiti/` layout | BUILT | `services/mtafiti/` — `census.py`, `declaration.py`, `feasibility.py`, `feasibility_config.v0.json`, `floor_feasibility.py`, `inference.py`, `measure.py`, `registry.py`, `source_standing.py`, `v3_overlay.py`, `verdict.py` | Nine modules per Mtafiti Spec §7. |
| Qualification Matrix computation | BUILT | `services/mtafiti/verdict.py:11` — maps onto frozen `qualification_matrix@v0` axes `(genre, source_standing)`; loader `contracts/qualification_matrix/loader.py:85` | Source: Spec §5. |
| Ring 3 edge detection | BUILT | Consumed at `services/solva_depth/reasoning/tension.py:23-32` from `u.relational.edges` (frozen `NormalizedUnit`) | |
| Ring 3 population | BUILT | Population via `NormalizedUnit.relational.edges` on frozen `five_rings@v0`; consumed in tension stage | mandate §4. |
| registry surface | BUILT | `services/mtafiti/registry.py` (166 LoC) + contract `contracts/mtafiti_registry.py`; snapshot in parity 31 | |
| detection surface | BUILT | 9-module verdict-computation surface — reads Registry state, emits per-unit Ring 5 stamps | Source: mandate §7. |
| Contract `mtafiti_registry_record@v0` | BUILT/FROZEN | `contracts/mtafiti_registry.py`; snapshot in parity 31 | |
| Contract `qualification_matrix@v0` | BUILT/FROZEN | `contracts/qualification_matrix/loader.py`; snapshots + content snapshot in parity 31 | |

## A.4 Northena

| spec item | verdict | evidence | notes |
|---|---|---|---|
| `services/northena/` layout | BUILT | `services/northena/` — `admit.py`, `converge.py`, `gate.py`, `ledger.py`, `state_machine.py`, `trace_lens.py` | 6-module structure. |
| Admit stage | BUILT | `services/northena/admit.py` + `routers/northena.py`; `test_admission_refusal_dispatch.py` + `test_northena_invariants.py` | Source: `docs/mandates/northena.md`. |
| Gate stage | BUILT | `services/northena/gate.py` | |
| Converge stage | BUILT | `services/northena/converge.py` — refusal absorb `converge.absorb_v2_refusal`; verified live at `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py` | |
| Ledger stage | BUILT | `services/northena/ledger.py` — append-only writes + `write_audit` piggyback; contracts v0/v1 both frozen (parity 31); retention config live per Phase 8 B-5b | |
| State machine | BUILT | `services/northena/state_machine.py` | |
| Trace lens | BUILT | `services/northena/trace_lens.py` + endpoint at `routers/northena.py`; `TraceLensEnvelope_v0` frozen contract | Phase 8 B-5a compliance console. |

## A.5 SyniSense (evidence base: `bundle_index` in `frontend/public/downloads/shield_engine_specs.tar.gz`)

| spec item | verdict | evidence | notes |
|---|---|---|---|
| Shield chokepoint (single outbound LLM surface) | BUILT | `services/synisense/shield/llm_router.py` (232 LoC). Enforced by `test_no_direct_llm_calls_outside_shield.py` | Source: PES v3 §18, doctrine §5.1. IF-1 chokepoint reconnection lands here. |
| `synisense.shield.llm_single_source_boundary` | BUILT | `docs/registry/function_promise_registry_v0.md:99` + AST gate | Rung 1 (Deterministic AST walk). |
| `synisense.shield.fluency_synthesizer` | BUILT | `services/synisense/shield/fluency_synthesizer.py:180` → `llm_router.invoke_with_metering(...)`. Registry row `:102`. Rung 4. | |
| `synisense.shield.brief_synthesizer` | BUILT | `services/synisense/shield/brief_synthesizer.py:114`. Registry row `:103`. Rung 4. | |
| `synisense.shield.grounding_gate_answer_fluency` | BUILT | `services/service_1/answer_grounding.py`. Registry row `:100`. 13 CI cells (AF-G2a..d, AF-G3a..c, AF-G-Grounding-Fail). | |
| `synisense.shield.grounding_gate_opportunity_briefs` | BUILT | `services/opportunity_briefs/brief_grounding.py`. Registry row `:101`. OB-G1 + OB-G-Grounding-Fail + OB-G-E3-No-Synth-Compute. | |
| `synisense.shield.per_sentence_anchor_map` | BUILT | `services/synisense/shield/fluency_synthesizer.py`. Registry row `:104`. | |
| `synisense.shield.data_blind_prompt_template` | BUILT | Grep-negative on `services/synisense/shield/{fluency_prompt.v0,brief_prompt.v0}.txt`. Registry row `:105`. | |
| `synisense.shield.advisory_marker_write_time_attach` | BUILT | `services/opportunity_briefs/advisory_marker.py`. Registry row `:106`. | |
| `synisense.shield.advisory_marker_render_time_visible` | BUILT | `frontend/src/pages/opportunity_briefs/OpportunityBriefCard.jsx`. Registry row `:107`. | |
| `synisense.shield.class_honesty_governed_response_boundary` | BUILT | AST negative-scan over `services/service_1/**`. Registry row `:108`. | |
| `synisense.shield.fluency_mode_telemetry_sidecar` | BUILT | `services/service_1/fluency_mode_telemetry.py`. Registry row `:109`. | |
| `synisense.shield.brief_telemetry_sidecar` | BUILT | `services/opportunity_briefs/brief_telemetry.py`. Registry row `:110`. | |
| `synisense.shield.mechanical_composer_baseline` | BUILT | `services/service_1/mechanical_composer.py` (byte-identical pre-3.8 per AF-E4 α). Registry row `:111`. | |
| `synisense.shield.brief_id_namespace_boundary` | BUILT | `services/opportunity_briefs/brief_registry.new_brief_id`. Registry row `:112`. | |
| `synisense.shield.refusal_taxonomy_closed` | BUILT | 10 refusal modules across `services/{service_1,v2_gate,compliance,northena}`. Registry row `:113`. | |
| llm_router internals (EMERGENT_LLM_KEY, `_provider_for`, `invoke_with_metering`) | BUILT | `services/synisense/shield/llm_router.py` (232 LoC) · module-level `emergentintegrations.llm.chat.LlmChat` import · `_EMERGENT_AVAILABLE` probe · per-call `invoke_with_metering` | Key custody via `EMERGENT_LLM_KEY` env; echo fallback if absent. |
| Key custody (trust receipt) | BUILT | `services/synisense/shield/trust_receipt.py` — imported by `services/synisense/shield/perception_router.py:31,59` + tests. | Reconnected pathway lives via perception_router. |
| Perception router (Shield-mediated) | BUILT | `services/synisense/shield/perception_router.py` (147 LoC). Consumed by `services/layer_b/asr/whisper_provider.py:24` + `services/layer_b/vision/frame_perception_provider.py:22`. | |
| De-identifier / re-identifier | BUILT (post-IF-1) | `services/synisense/shield/deidentifier.py` (686 LoC) + `reidentifier.py` (332 LoC) — RECONNECTED at `llm_router.invoke_with_metering` chokepoint. | Pre-IF-1 was PARTIAL (custody chain unreachable); IF-1 close reconnects deidentify → LLM → reidentify at chokepoint. |
| Custody chain (client.py orchestrator) | SUPERSEDED | Pre-IF-1 orchestrator at `services/synisense/shield/client.py` shaved; superseded by chokepoint-at-llm_router pattern | IF-1 ruling. |

## A.6 Contracts

| contract | frozen? | consumed? | by whom? |
|---|---|---|---|
| `signal_ring_dimensions@v0` | Y — `contracts/signal_ring.py` + snapshot `signal_ring.contract_snapshot.json` + content snapshot `signal_ring_dimensions.v0.content_snapshot.json` (parity 31) | Y (19 in-tree refs) | `services/layer_c/convergence.py:9-35`, `services/layer_c/aggregator.py:75`, `services/mtafiti/verdict.py`, `contracts/mtafiti_registry.py:5`, `contracts/extraction_params.py:6`, `services/system_state.py:143`, `tests/invariants/test_layer_c_signal_ring_conformance.py`, `tests/invariants/test_signal_ring_dimensions_v0.py`. |
| `qualification_matrix@v0` | Y — `contracts/qualification_matrix/loader.py` + `__init__.py`; snapshots + schema/content (parity 31) | Y (66 in-tree refs) | `routers/contracts.py:41-115` (`GET /api/contracts/qualification_matrix`), `contracts/mtafiti_registry.py:4`, `contracts/admission_refusal.py:35`, `contracts/five_rings.py:137,251,265`, `services/mtafiti/verdict.py:11`, `services/system_state.py:142`. |
| `objective_request@v0` | Y — `contracts/objective_request.py` + snapshot; additive v2 also frozen (`objective_request_v2.contract_snapshot.json`) — both in parity 31 | Y (145 in-tree refs) | v0: `routers/contracts.py:35`, `contracts/objective_request_v2.py:72`. v2 (primary): `routers/service_1.py:32`, `routers/objectives.py:33`, `routers/wizard_operator.py:283`, `routers/mtafiti.py:14`. Additive per Substrate-Drop v2. |

See also: /app/docs/briefs/outstanding_work_and_gap_register_v1.1.md §4
