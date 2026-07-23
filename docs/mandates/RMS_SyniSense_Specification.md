**SyniSense**

The Shield — Engine Specification

The complete specification of the boundary governor: the outbound LLM chokepoint, the policy-enforcement custody chain, the de-identification pipeline, the purpose-validation contract, the key-custody trust receipts, and the module structure, typed contracts, algorithms, and test obligations that implement them.

Engine Specification · Version 1.0 · elaborates the Product & Engineering Specification v3 (§18), which prevails on conflict.

*Prepared by Syni.ai · July 2026 · Confidential · Fifth engine mandate (parity with Solva · Targeta · Mtafiti · Northena) · assembly from on-disk audited surfaces; zero new design; OD-1/OD-2/OD-3 dispositions per FLAG 1 ruling 2026-07-15.*

This document is binding on ratification. Part I states what SyniSense must do and why; Part II specifies how it is built — modules, typed contracts, the chokepoint algorithm, the custody chain, the de-identification pipeline, the purpose-validation contract, key custody, and test obligations; Part III states governance and invariants. It is a forward specification: it defines what must be true of any correct implementation.

# Part I — Shield: role, promise, and boundary

## §1.1 Role

**SyniSense (Shield) is the boundary governor for the platform's outbound LLM surface and its adjacent custody chain.** It is the single reconnected chokepoint through which every LLM call transits (`services/synisense/shield/llm_router.py:1-232` — 232 LoC · `docs/audits/engine_conformance_v1.md:82,98`), the de-identify → LLM → re-identify custody chain enforcement point (`docs/audits/engine_conformance_v1.md:101`), the class-honesty guard for governed-response boundaries (`docs/audits/engine_conformance_v1.md:92`), and the refusal-taxonomy closer for the 10 refusal modules across `services/{service_1, v2_gate, compliance, northena}` (`docs/audits/engine_conformance_v1.md:97`).

## §1.2 Promise

- **P1 · Single outbound LLM surface.** No LLM call may originate outside the Shield chokepoint. Enforced by `test_no_direct_llm_calls_outside_shield.py` (`docs/audits/engine_conformance_v1.md:82`).
- **P2 · Custody chain is reachable.** De-identifier and re-identifier are RECONNECTED at the chokepoint post-IF-1 ruling (`docs/audits/engine_conformance_v1.md:101`); pre-IF-1 client.py orchestrator superseded (`docs/audits/engine_conformance_v1.md:102`).
- **P3 · Grounding is not asserted, it is proven.** Grounding gates run at `services/service_1/answer_grounding.py` and `services/opportunity_briefs/brief_grounding.py`, protected by 13 CI cells (AF-G2a..d, AF-G3a..c, AF-G-Grounding-Fail) and OB-G1 + OB-G-Grounding-Fail + OB-G-E3-No-Synth-Compute respectively (`docs/audits/engine_conformance_v1.md:86-87`).
- **P4 · Data-blind prompts.** Prompt templates carry no data; `grep`-negative enforcement on `services/synisense/shield/fluency_prompt.v0.txt` and `brief_prompt.v0.txt` (`docs/audits/engine_conformance_v1.md:89`).
- **P5 · Advisory markers at write-time and render-time.** Advisory-class outputs carry markers stamped at write-time (`services/opportunity_briefs/advisory_marker.py`) and enforced visible at render-time (`frontend/src/pages/opportunity_briefs/OpportunityBriefCard.jsx`) (`docs/audits/engine_conformance_v1.md:90-91`).
- **P6 · Refusal taxonomy is closed.** 10 refusal modules span the layered governance surface; no ad-hoc refusal path (`docs/audits/engine_conformance_v1.md:97`).
- **P7 · Fluency telemetry sidecar.** Every LLM invocation emits a sidecar record — fluency_mode_telemetry for S1 fluency, brief_telemetry for briefs (`docs/audits/engine_conformance_v1.md:93-94`).
- **P8 · Mechanical composer is the fallback arm.** Byte-identical pre-3.8 baseline preserved at `services/service_1/mechanical_composer.py` per AF-E4 α (`docs/audits/engine_conformance_v1.md:95`); rung-4 always carries a rung-1/2 fallback per Registry Doctrine §5.1 Rung-4 rule.
- **P9 · Class-honesty governed-response boundary.** AST negative-scan over `services/service_1/**` enforces no class-honesty violation (`docs/audits/engine_conformance_v1.md:92`).
- **P10 · Brief-id namespace boundary.** Brief IDs land inside `services/opportunity_briefs/brief_registry.new_brief_id` (`docs/audits/engine_conformance_v1.md:96`).

# Part II — Engineering: how Shield is built

## §2.1 Module structure

Assembly from on-disk tree at `backend/services/synisense/` (as of 2026-07-15):

- `shield/llm_router.py` (232 LoC) — the outbound chokepoint · module-level `emergentintegrations.llm.chat.LlmChat` import · `_EMERGENT_AVAILABLE` probe · per-call `invoke_with_metering` (`docs/audits/engine_conformance_v1.md:98`).
- `shield/deidentifier.py` (686 LoC) — pre-LLM PII stripping and mapping (`docs/audits/engine_conformance_v1.md:101`).
- `shield/reidentifier.py` (332 LoC) — post-LLM re-attach against the mapping (`docs/audits/engine_conformance_v1.md:101`).
- `shield/perception_router.py` (147 LoC) — Shield-mediated perception routing; consumed by `services/layer_b/asr/whisper_provider.py:24` and `services/layer_b/vision/frame_perception_provider.py:22` (`docs/audits/engine_conformance_v1.md:100`).
- `shield/trust_receipt.py` — key custody envelope; imported by `perception_router.py:31,59` and tests (`docs/audits/engine_conformance_v1.md:99`).
- `shield/fluency_synthesizer.py:180` — rung-4 fluency composition; invokes `llm_router.invoke_with_metering(...)` (`docs/audits/engine_conformance_v1.md:84,88`).
- `shield/brief_synthesizer.py:114` — rung-4 brief composition (`docs/audits/engine_conformance_v1.md:85`).
- `shield/tenant_entities.py` — tenant-scoped entity resolution for de-identification.
- `shield/fluency_prompt.v0.txt` · `shield/brief_prompt.v0.txt` — data-blind prompt templates (`docs/audits/engine_conformance_v1.md:89`).
- `shield/exceptions.py` — Shield-scoped exception taxonomy.
- `synisense/webhook_registration.py` — webhook custody registration.
- `synisense/config.py` · `synisense/exceptions.py` — envelope config and exceptions.
- Peer gates (Shield-invoked, reside in sibling services): `services/service_1/answer_grounding.py` · `services/opportunity_briefs/brief_grounding.py` · `services/service_1/mechanical_composer.py` · `services/service_1/fluency_mode_telemetry.py` · `services/opportunity_briefs/brief_telemetry.py` · `services/opportunity_briefs/advisory_marker.py` (`docs/audits/engine_conformance_v1.md:86-95`).

## §2.2 Typed contracts (frozen · anchored in Parity 31)

Shield behavior is anchored by frozen Pydantic contracts under `backend/contracts/` (31 contracts held byte-identical per Parity 31/31):

- `admission_refusal.py` — refusal admission envelope produced at Shield-boundary rejection.
- `outer_gate_receipt.py` / `outer_gate_receipt_v1.py` — outer-gate stamp emitted at Shield ingress; consumed by Northena ledger.
- `quote_envelope.py` — quote envelope Shield stamps for verbatim-fidelity claims.
- `signal_ring.py` — signal ring Shield reads to compose refusal or admission.
- `service_1_refusal.py` — S1-scoped refusal composition (governed-response boundary · `docs/audits/engine_conformance_v1.md:92`).
- `v2_refusal.py` — v2-scoped refusal composition.
- `agent_assumption.py` — assumption-tracking contract for governed answers.
- `trace_lens.py` — trace-lens envelope for outbound custody.

Anchor rule (per Registry Doctrine §3.2 · byte-identity lock enforcement class): any change to these 8 contracts is a Parity seal event and requires Owner ruling (EAB-2 is the ratified seal event for Service1Refusal@v1 per phase-ledger §5 sequence position 2).

## §2.3 The chokepoint algorithm (llm_router.invoke_with_metering)

Per `docs/audits/engine_conformance_v1.md:98`, the chokepoint's runtime signature is:

1. **Provider selection** — `_provider_for(<provider_name>)` reads `EMERGENT_LLM_KEY` from env; falls back to echo if absent (`docs/audits/engine_conformance_v1.md:98`).
2. **De-identify** — inbound payload transits `shield/deidentifier.py` before LLM invocation (`docs/audits/engine_conformance_v1.md:101` post-IF-1 reconnection).
3. **Invoke with metering** — `emergentintegrations.llm.chat.LlmChat` is invoked; per-call metering emitted to fluency/brief telemetry sidecars (`docs/audits/engine_conformance_v1.md:93-94`).
4. **Re-identify** — outbound LLM output transits `shield/reidentifier.py` against the de-identify mapping (`docs/audits/engine_conformance_v1.md:101`).
5. **Grounding gate** — for S1 fluency composition, `services/service_1/answer_grounding.py` enforces per-sentence anchor map (`docs/audits/engine_conformance_v1.md:86,88`). For briefs, `services/opportunity_briefs/brief_grounding.py` enforces the brief grounding cell suite (`docs/audits/engine_conformance_v1.md:87`).
6. **Class-honesty check** — AST negative-scan bounds prevent governed-response boundary violations (`docs/audits/engine_conformance_v1.md:92`).
7. **Trust receipt** — every invocation writes a trust receipt via `shield/trust_receipt.py` (`docs/audits/engine_conformance_v1.md:99`).

## §2.4 The de-identification pipeline

Per `docs/audits/engine_conformance_v1.md:101`:

- **Pre-IF-1 state:** custody chain was PARTIAL — deidentifier and reidentifier existed but the custody chain was unreachable through `services/synisense/shield/client.py` (superseded orchestrator).
- **Post-IF-1 state (current):** deidentifier and reidentifier RECONNECTED at the `llm_router.invoke_with_metering` chokepoint. The pattern is chokepoint-at-llm_router, not custody-at-orchestrator (`docs/audits/engine_conformance_v1.md:102` supersession record).
- **Deidentifier (`shield/deidentifier.py`, 686 LoC):** strips PII to placeholder tokens, records the mapping in a per-request custody envelope.
- **Reidentifier (`shield/reidentifier.py`, 332 LoC):** re-attaches identifiers to the LLM output using the same custody envelope; unmatched tokens raise Shield-exception.
- **Tenant entities (`shield/tenant_entities.py`):** tenant-scoped entity resolution shape.

## §2.5 Purpose validation

**As-built at the seam (OD-1 disposition · 2026-07-15 Owner ruling):** Purpose validation is documented as-built at the `llm_router` custody-chain seam, per the IF-1 supersession of the pre-IF-1 `client.py` orchestrator (`docs/audits/engine_conformance_v1.md:101,102`). No standalone `purpose_validator.py` module is resurrected; the mandate records the distributed enforcement that exists on-disk today:

- **Data-blind prompt boundary** — `fluency_prompt.v0.txt` and `brief_prompt.v0.txt` (`docs/audits/engine_conformance_v1.md:89`) — prompts by construction cannot leak purpose-scoped data.
- **Grounding gate posture** — grounding is proof-of-purpose-alignment: a claim ungrounded is a refusal (`docs/audits/engine_conformance_v1.md:86-87`).
- **Refusal taxonomy** — 10 modules across `services/{service_1, v2_gate, compliance, northena}` (`docs/audits/engine_conformance_v1.md:97`) exhaustively enumerate governed-purpose refusal paths.
- **Advisory marker discipline** — non-fact classes carry markers at write and render (`docs/audits/engine_conformance_v1.md:90-91`).

**IF-1 citation:** the custody chain reconnection ruling (`docs/audits/engine_conformance_v1.md:101` post-IF-1 state · `:102` supersession record) establishes that purpose enforcement is a chokepoint property at `llm_router.invoke_with_metering`, not a standalone module. This mandate records the reality; no new file is proposed.

## §2.6 Key custody

- **`shield/trust_receipt.py`** — key custody envelope emitted per invocation (`docs/audits/engine_conformance_v1.md:99`).
- **Consumption sites:** `perception_router.py:31,59` and Shield tests (`docs/audits/engine_conformance_v1.md:99`).
- **Env key handling:** `EMERGENT_LLM_KEY` read at `llm_router.py` module load; echo fallback if absent — key is never logged; presence surfaces as a boolean `_EMERGENT_AVAILABLE` probe (`docs/audits/engine_conformance_v1.md:98`).
- **Reconnected pathway (post-IF-1):** custody flows through `perception_router.py` for perception-side calls; through `llm_router.invoke_with_metering` for synthesis-side calls.
- **Perception router — as-built routing seat (OD-2 disposition · 2026-07-15 Owner ruling):** `services/synisense/shield/perception_router.py` (147 LoC) is documented in its live as-built role: the Shield-mediated routing seat for rung-3 perception calls, consumed by `services/layer_b/asr/whisper_provider.py:24` and `services/layer_b/vision/frame_perception_provider.py:22`. The mandate records this routing seat as it operates today; zero new design.

## §2.7 Test obligations

Assembly of on-disk conformance evidence (verbatim carrier of the 19 audit rows at `docs/audits/engine_conformance_v1.md:82-100`):

| # | Function | State | Evidence | Class / notes |
|---:|---|---|---|---|
| 1 | Shield chokepoint (single outbound LLM surface) | BUILT | `services/synisense/shield/llm_router.py` (232 LoC) · `test_no_direct_llm_calls_outside_shield.py` | PES v3 §18 · doctrine §5.1 · IF-1 chokepoint reconnection lands here |
| 2 | `synisense.shield.llm_single_source_boundary` | BUILT | `docs/registry/function_promise_registry_v0.md:99` + AST gate | Rung 1 (Deterministic AST walk) |
| 3 | `synisense.shield.fluency_synthesizer` | BUILT | `services/synisense/shield/fluency_synthesizer.py:180` → `llm_router.invoke_with_metering(...)` · Registry row `:102` | Rung 4 |
| 4 | `synisense.shield.brief_synthesizer` | BUILT | `services/synisense/shield/brief_synthesizer.py:114` · Registry row `:103` | Rung 4 |
| 5 | `synisense.shield.grounding_gate_answer_fluency` | BUILT | `services/service_1/answer_grounding.py` · Registry row `:100` · 13 CI cells (AF-G2a..d, AF-G3a..c, AF-G-Grounding-Fail) | — |
| 6 | `synisense.shield.grounding_gate_opportunity_briefs` | BUILT | `services/opportunity_briefs/brief_grounding.py` · Registry row `:101` · OB-G1 + OB-G-Grounding-Fail + OB-G-E3-No-Synth-Compute | — |
| 7 | `synisense.shield.per_sentence_anchor_map` | BUILT | `services/synisense/shield/fluency_synthesizer.py` · Registry row `:104` | — |
| 8 | `synisense.shield.data_blind_prompt_template` | BUILT | Grep-negative on `services/synisense/shield/{fluency_prompt.v0,brief_prompt.v0}.txt` · Registry row `:105` | — |
| 9 | `synisense.shield.advisory_marker_write_time_attach` | BUILT | `services/opportunity_briefs/advisory_marker.py` · Registry row `:106` | — |
| 10 | `synisense.shield.advisory_marker_render_time_visible` | BUILT | `frontend/src/pages/opportunity_briefs/OpportunityBriefCard.jsx` · Registry row `:107` | — |
| 11 | `synisense.shield.class_honesty_governed_response_boundary` | BUILT | AST negative-scan over `services/service_1/**` · Registry row `:108` | — |
| 12 | `synisense.shield.fluency_mode_telemetry_sidecar` | BUILT | `services/service_1/fluency_mode_telemetry.py` · Registry row `:109` | — |
| 13 | `synisense.shield.brief_telemetry_sidecar` | BUILT | `services/opportunity_briefs/brief_telemetry.py` · Registry row `:110` | — |
| 14 | `synisense.shield.mechanical_composer_baseline` | BUILT | `services/service_1/mechanical_composer.py` (byte-identical pre-3.8 per AF-E4 α) · Registry row `:111` | — |
| 15 | `synisense.shield.brief_id_namespace_boundary` | BUILT | `services/opportunity_briefs/brief_registry.new_brief_id` · Registry row `:112` | — |
| 16 | `synisense.shield.refusal_taxonomy_closed` | BUILT | 10 refusal modules across `services/{service_1, v2_gate, compliance, northena}` · Registry row `:113` | — |
| 17 | llm_router internals | BUILT | `services/synisense/shield/llm_router.py` (232 LoC) · `emergentintegrations.llm.chat.LlmChat` · `_EMERGENT_AVAILABLE` probe · `invoke_with_metering` | Key custody via `EMERGENT_LLM_KEY`; echo fallback if absent |
| 18 | Key custody (trust receipt) | BUILT | `services/synisense/shield/trust_receipt.py` — imported by `services/synisense/shield/perception_router.py:31,59` + tests | Reconnected pathway lives via perception_router |
| 19 | Perception router (Shield-mediated) | BUILT | `services/synisense/shield/perception_router.py` (147 LoC) · consumed by `services/layer_b/asr/whisper_provider.py:24` + `services/layer_b/vision/frame_perception_provider.py:22` | — |
| — | De-identifier / re-identifier | BUILT (post-IF-1) | `services/synisense/shield/deidentifier.py` (686 LoC) + `reidentifier.py` (332 LoC) — RECONNECTED at `llm_router.invoke_with_metering` chokepoint | Pre-IF-1 was PARTIAL (custody chain unreachable); IF-1 close reconnects deidentify → LLM → reidentify at chokepoint |
| — | Custody chain (client.py orchestrator) | SUPERSEDED | Pre-IF-1 orchestrator at `services/synisense/shield/client.py` shaved; superseded by chokepoint-at-llm_router pattern | IF-1 ruling |

# Part III — Governance and invariants

## §3.1 Invariants

- **I1 · Chokepoint invariant.** `services/synisense/shield/llm_router.invoke_with_metering` is the ONLY module invoking `emergentintegrations.llm.chat.LlmChat` in the entire codebase. Enforced by `test_no_direct_llm_calls_outside_shield.py`.
- **I2 · Parity 31 anchor.** All 8 Shield-anchoring contracts (`admission_refusal.py` · `outer_gate_receipt.py` + v1 · `quote_envelope.py` · `signal_ring.py` · `service_1_refusal.py` · `v2_refusal.py` · `agent_assumption.py` · `trace_lens.py`) are frozen; changes are Parity seal events.
- **I3 · Custody chain reachability (post-IF-1).** Every LLM invocation transits deidentify → invoke → reidentify. No client.py orchestrator path is authorized.
- **I4 · Refusal taxonomy closure.** Exactly 10 refusal modules; no ad-hoc refusal path.
- **I5 · Rung-4 always paired with lower-rung fallback.** Mechanical composer baseline preserved byte-identical (AF-E4 α).
- **I6 · Data-blind prompt boundary.** Prompt template files are grep-negative against tenant data.

## §3.2 Cross-references

- **PES v3 §18** — Product & Engineering Spec (Shield/chokepoint mandate).
- **Registry Doctrine §5.1** — model ladder Rung-4 rule (fallback arm required).
- **Registry Doctrine Part IV D-5** — NL-only enforcement is defect D2 (Shield's data-blind prompt discipline is the exemplar of the D-5 pattern).
- **Registry Doctrine Part IV D-12** — experimentation at system level only; Shield's mechanics are known and parameterized, not staged proving.
- **Critic Seam Spec v1.0** — QA-1..QA-6; Tier-1 RV cells ride EAB phases; Critic Seam Part B (production QA machinery) per TQ v1.0 §7.
- **Transformation Quality Spec v1.0 §6 MOAC** — M-a..M-f criteria bind Shield-adjacent training-output acceptance.
- **Op. Values v1.1 §6.6** — seam-value quarantine (systemic-halt threshold, 2% DEFAULT · S2.onboard-set per MC-E3 α).
- **Outer Gate Receipt v1** — Shield ingress stamp (frozen contract).
- **CIF Spec v1.0 §6 A5** — Critic Seam rubric amendment CR-7 (rides Critic-pass phase per phase ledger §5).

## §3.3 Candidates riding downstream phases

- **Class-honesty AST-scan target extension** (OD-3 disposition · 2026-07-15 Owner ruling · out of mandate scope): the current AST negative-scan operates over `services/service_1/**` per `docs/audits/engine_conformance_v1.md:92`. Extension of the scan to `services/v2_gate/**` and `services/opportunity_briefs/**` files as a named candidate riding the Critic-pass phase's cells. This mandate records the enforcement as it exists on-disk; no enforcement work lands with this mandate document.

---

*SyniSense (Shield) — Engine Specification · Version 1.0 · Landed 2026-07-15 as the fifth engine mandate (parity with Solva · Targeta · Mtafiti · Northena). Companion to: PES v3 · Registry Doctrine v1.0 · Critic Seam Spec v1.0/v1.1 · Transformation Quality Spec v1.0 · Operating Values v1.1 · CIF Spec v1.0 · Surface & Journey Map v1.0 · S1 Memory Model & Integration Wizard Spec v1.0. Owner ratification: Gap-Closure + Sequence Ratification dispatch FLAG 1 (2026-07-15) with OD-1/OD-2/OD-3 dispositions applied. Discharges Register v1.5 §4 G-12 (SyniSense mandate missing).*

**Assembly-only attest (landed form):**

- **Source-citation count:** 47 discrete citations to `docs/audits/engine_conformance_v1.md:82-102` (19 rows verbatim); 8 citations to frozen contracts under `backend/contracts/`; 14 citations to code paths under `backend/services/synisense/**` and adjacent services; 6+ citations to sibling mandates + PES v3 + Critic Seam + TQ + Op. Values + Registry Doctrine + CIF + SJM + S1 Memory. **Total: 75+ source citations across the mandate.**
- **Zero new design assertion:** every mechanic, invariant, contract, and gate cited is BUILT on-disk today per the audit. OD-1/OD-2/OD-3 dispositions record as-built reality per Owner ruling; no new gate, worker, contract, or surface is proposed.
- **Zero synthesis assertion:** the 19 conformance rows are byte-carried verbatim from the audit; the module structure is `ls`-derived from the on-disk tree; the invariants I1-I6 are re-statements of existing test contracts.
