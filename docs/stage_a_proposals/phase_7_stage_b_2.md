# Phase 7 Stage B-2 — Stage A Proposal (Buyer Variant + Sonnet 4.6 LLM Integration)

**Delivery date:** 2026-07-04
**Delivery format:** Standing Rule v3 — on-disk canonical + SHA quoted at return.
**Ordering:** Stage A landed to disk; Owner confirmation required before Stage B execution.

---

## 0. Owner Condition A — 6th-endpoint gate confirmation (verbatim answer)

Endpoint: `POST /api/wizard/operator/{session_id}/agent-assumption`. Owner's three gate requirements:

| Requirement | Current disk state | B-2 action |
|---|---|---|
| (i) **CANNOT mint AgentAssumption_v0 on mandatory-tier fields** | **Not enforced** — `services/wizard/operator_state_machine.py:170-196` `record_agent_assumption` mints for ANY `field_name`; Guard 1 only fires at freeze via `_validate_freeze_time_invariants` on the frozen model_validator. | **LAND at B-2 (test-first):** raise `SourceTagViolation` inside `record_agent_assumption` when `variant == "operator"` AND `field_name in operator_mandatory_fields()`. Endpoint boundary returns 422 with the violation as text. Buyer variant permits assumptions on any axis (agent-may-propose per v3 §3.3 buyer semantics). |
| (ii) **CANNOT write CommittedValue_v0 with `source="operator_supplied"`** | Structurally enforced but **no explicit gate** — endpoint at `routers/wizard_operator.py:141-166` only calls `osm.record_agent_assumption(...)` which at `operator_state_machine.py:189-195` writes `source="agent_assumed"` verbatim; the operator-source write path `record_operator_response` (line 127) is never reachable from this endpoint. | **LAND at B-2:** explicit gate `test_agent_assumption_endpoint_never_mints_operator_source_committed_value` — post-call scan of `session.committed_values` asserts EVERY entry whose `committed_at` equals the assumption's `at` has `source="agent_assumed"`. |
| (iii) **CANNOT write OperatorTurn_v0 content** | Structurally enforced but **no explicit gate** — endpoint never touches `session.turns[]`; only `agent_assumptions[]` + `committed_values[]`. | **LAND at B-2:** explicit gate `test_agent_assumption_endpoint_never_appends_operator_turn` — assert `len(session.turns)` unchanged pre-vs-post call. |

**Enforcement predicate for (i) (planned, one line):**
```python
if variant == "operator" and field_name in operator_mandatory_fields():
    raise SourceTagViolation(f"agent-assumption on mandatory-tier field {field_name!r} refused (Guard 1)")
```

**One-line summary for close-report Condition A:**
> All three gates land at B-2 close as `test_agent_assumption_endpoint_*` in `tests/invariants/test_phase_7_stage_b_2_wizard.py`; enforcement predicate for (i) lives at `services/wizard/operator_state_machine.py::record_agent_assumption` — line-anchor recorded at close.

---

## 0.1 Owner Condition B — Plan Debt append (verbatim)

Append to `/app/memory/ORCHESTRATOR_CONTINUITY.md` §0.2 Plan Debts (verbatim, no reformatting):

> "Wizard session-ownership binding lands with Phase 8 auth/key model — recorded as the system-wide auth landing, not a wizard-special. [Owner ruling, Phase 7 Stage B-2 dispatch, 2026-07-04]"

Lands at B-2 close alongside the Phase Ledger row.

---

## 1. Scope reprise (no new questions; Owner dispatch verbatim absorbed)

Five deliverables, all backend, zero frontend touches (8a-lite in flight):

1. **Buyer state machine** — new `services/wizard/buyer_state_machine.py`.
2. **Buyer router** — new `routers/wizard_buyer.py` (**decision justified in §2**).
3. **Sonnet 4.6 LLM integration** — new `SonnetWizardAgent` class inside `services/synisense/shield/llm_router.py` (Shield boundary preserved).
4. **Dual-delta gate** — new shared helper `services/wizard/dual_delta.py` (declarative-table pattern mirroring `provenance_preservation.py` from B-1).
5. **Session persistence extension** — additive index on `variant + session_id` in `services/wizard/session_persistence.py`.

---

## 2. Router-file choice — Owner said "your call, but justify"

**Decision: TWO files. `routers/wizard_operator.py` (existing, untouched) + `routers/wizard_buyer.py` (new).**

**Rejected alternative:** single-file variant-parameterised path `/api/wizard/{variant}/session`. Reasons:

| Axis | Two-file (chosen) | Single-file (rejected) |
|---|---|---|
| Semantic divergence | Operator has Guard 1 mandatory-tier + no proposal semantics; buyer has no mandatory tier + agent-may-propose + dual-delta gate. Two files carry the semantic split honestly. | Single file forces `if variant == "operator": ... else: ...` branching at every endpoint — hides the semantic split under a path parameter. |
| Test surface | Each router file gets its own set of gate tests scoped to that variant's shape. | Gate tests must parametrise over variant and re-run each assertion twice — noise. |
| Endpoint asymmetry | Buyer has ONE endpoint operator doesn't need: `POST /api/wizard/buyer/{sid}/propose` (agent proposal emission with dual-delta payload). Operator router has no proposal path. | Would need a variant-scoped conditional 404 on `/propose` — path claims to exist but rejects — worse than absence. |
| Router LoC | ~250 each; sum ~500. Operator router UNTOUCHED. | ~300-350 single file; changes to operator paths (add branch). Not additive-only. |
| Owner ordering constraint | "26 contracts stay byte-identical." Path-level additivity easier to prove with a NEW router file mounted alongside. | Modifying `wizard_operator.py` on disk violates additive-only posture on Phase 7 Stage B-1's landed router. |
| Rule 2 v2 lifted ratio | Buyer router lifts endpoint shape + persistence-wire idioms from operator router (~150 LoC lifted, ~100 net-new). | Single-file lift ratio is lower because the branching logic is genuinely net-new. |

**Wire surface (new):** `POST /api/wizard/buyer/session`, `POST /api/wizard/buyer/{sid}/turn`, `POST /api/wizard/buyer/{sid}/propose`, `POST /api/wizard/buyer/{sid}/agent-assumption`, `POST /api/wizard/buyer/{sid}/commit-review`, `POST /api/wizard/buyer/{sid}/freeze`, `GET /api/wizard/buyer/{sid}` — **7 endpoints**.

The extra endpoint (`/propose`) is buyer-specific per §3.3 buyer semantics. `/agent-assumption` is retained on buyer router for consistency with operator's B-1 landing and Owner's Condition A acceptance — **on the buyer router, the mandatory-tier restriction of Condition A(i) does NOT apply because buyer has no operator-mandatory tier**; Condition A(ii) and A(iii) still apply (no operator-source CommittedValue, no OperatorTurn writes).

---

## 3. Buyer state machine — `services/wizard/buyer_state_machine.py`

Mirrors operator's shape (`BuyerSession` dataclass; `new_buyer_session`, `next_agent_turn`, `record_buyer_response`, `record_agent_assumption`, `record_proposal`, `preflight_freeze`, `freeze`). Divergences from operator:

| Aspect | Operator (B-1) | Buyer (B-2) |
|---|---|---|
| Mandatory tier | 8 operator-mandatory fields (Guard 1 at freeze) | **None** — agent may propose across all axes within offerability |
| `variant` field on frozen state | `"operator"` | `"buyer"` |
| Lawful basis | Operator supplies | **Buyer NEVER supplies** — `lawful_basis` field on committed_values MUST be null for buyer variant; use_purpose drives `license_class` at commit-review (primary arm of E1 Option C wrap) |
| Agent proposal emission | Not applicable (Guard 1 forbids propose on mandatory) | **First-class** — agent may propose standard/grain/reach shifts; each proposal MUST carry `{price_delta, class_delta}` via dual-delta gate |
| Guard 2 (agent-assumed marking) | Applies | **Applies** — same source-tag XOR invariant on CommittedValue_v0 |
| Guard 3 (per-turn feasibility) | Applies | **Applies** — every turn appends non-empty `feasibility_snapshot_ref` |
| Provenance-preservation shaping-time refuse | Applies via shared `provenance_preservation.py` from B-1 (E7 shared-derivation) | **Applies** — same shared module import; refuse-during-shape identical predicate |
| Freeze pathway | `preflight_freeze` + `freeze()` mint frozen `WizardCommitState_v0` | **Deferred to B-3** — B-2 lands the machinery + tests but freeze admission handoff is Phase 7 Stage B-3 scope |

**Guard 1 semantic on buyer:** N/A. Buyer's `preflight_freeze` skips the mandatory-tier check. Enforced by `validate_guard_1_operator_mandatory_all_operator_supplied(committed_values, variant="buyer")` — the source-tagging function ALREADY takes a variant parameter (see `services/wizard/source_tagging.py`); on `"buyer"` the function no-ops.

---

## 4. LLM integration — `SonnetWizardAgent` inside Shield's LLM router

Owner mandate: `test_no_direct_llm_calls_outside_shield.py` MUST stay green. All LLM calls stay inside `services/synisense/shield/*`.

**Landing location:** `services/synisense/shield/llm_router.py` (existing 221 LoC; extends to ~330 LoC). Adds:

- New class `SonnetWizardAgent` implementing the `WizardAgent` Protocol declared at `services/wizard/agent_interface.py:1-136` — same shape as `DeterministicStubAgent`, different `next_turn` / `commit_review` bodies.
- Sonnet 4.6 via Emergent LLM Key using the existing `emergentintegrations.LlmChat + UserMessage` pattern (see current `llm_router.py:31-40` — `_EMERGENT_AVAILABLE` probe already scaffolded).
- Provider/model configuration: `provider="anthropic"`, `model="claude-sonnet-4.6"` (exact SDK identifier resolved at Stage B via `integration_playbook_expert_v2` per §7 handling below).

**Temperatures (per Owner dispatch):**
- Live sessions (buyer AND operator variants): `temperature=0.2`.
- Deterministic-replay tests using recorded fixtures: `temperature=0.0`.
- Temperature switching via `SonnetWizardAgent(temperature: float)` constructor arg.

**Infra-not-refusal boundary (Standing Disposition #2 verbatim):** any Sonnet error class (rate-limit, 5xx from Anthropic, auth failure, timeout, `emergentintegrations` exception, network fault) surfaces as HTTP 503 to the caller. **Never** as an `AdmissionRefusal_v0` or `Service1Refusal_v0`. Implementation: `SonnetWizardAgent.next_turn` catches all `emergentintegrations` exceptions and re-raises as `synisense.exceptions.ServiceUnavailable`; router boundary translates to 503.

**No silent fallback.** If Sonnet 4.6 is unavailable, we return 503 — we do NOT swap to a smaller Claude model, we do NOT fall back to the deterministic stub, we do NOT re-prompt. Silent-model-swap on a governed surface changes shaping quality invisibly. Enforced by grep-negative gate `test_no_silent_model_degrade_when_sonnet_4_6_unavailable`.

---

## 5. Dual-delta gate — `services/wizard/dual_delta.py`

Mirror `services/service_1/provenance_preservation.py` (173 LoC) — declarative-table pattern.

**Predicate:** any agent proposal that changes `output.standard` OR `output.grain` MUST have BOTH `price_delta` AND `class_delta` computed and present on the turn payload. Refuse the proposal at emission if either delta is absent (per Owner's `Visibility-not-prohibition` Standing Disposition #8 — visibility is the guard, prohibition would be wrong; but the visibility itself is mandatory).

**Shape:**
```python
_DUAL_DELTA_REQUIRED_AXES: FrozenSet[str] = frozenset({"output.standard", "output.grain"})

@dataclass(frozen=True)
class DualDeltaResult:
    admissible: bool
    missing_deltas: Tuple[str, ...] = ()
    refusal_reason: Optional[str] = None

def evaluate_dual_delta(
    axes_changed: FrozenSet[str],
    price_delta: Optional[str],
    class_delta: Optional[str],
) -> DualDeltaResult: ...
```

Called from BOTH state machines (operator's `record_proposal` if ever added, buyer's `record_proposal`). **Single derivation site** — grep-negative gate mirroring E7 pattern.

---

## 6. Test surface (Stage A roster; ~30-38 gates)

New file `tests/invariants/test_phase_7_stage_b_2_wizard.py`. Roster:

**Condition A (Owner's three gates):**
1. `test_agent_assumption_endpoint_refuses_on_mandatory_tier_operator_variant` (LB)
2. `test_agent_assumption_endpoint_permits_on_buyer_variant_any_axis`
3. `test_agent_assumption_endpoint_never_mints_operator_source_committed_value` (LB)
4. `test_agent_assumption_endpoint_never_appends_operator_turn` (LB)

**Buyer variant guards (mirror B-1's shape):**
5. `test_buyer_variant_preserves_committed_value_source_tag_xor_invariant`
6. `test_buyer_variant_every_turn_carries_feasibility_snapshot_ref`
7. `test_buyer_variant_agent_may_propose_on_non_mandatory_axes`
8. `test_buyer_variant_never_sets_lawful_basis_on_committed_values` (LB)
9. `test_buyer_variant_use_purpose_drives_license_class_via_primary_arm` (LB, E1 Option C reuse)
10. `test_buyer_variant_provenance_preservation_shared_derivation` (E7 grep-negative preserved)

**Sonnet 4.6 LLM integration:**
11. `test_sonnet_wizard_agent_implements_wizard_agent_protocol` (LB, E4 proof-order preserved)
12. `test_sonnet_wizard_agent_deterministic_at_temp_0_recorded_fixture` (recorded-fixture replay; hermetic)
13. `test_no_silent_model_degrade_when_sonnet_4_6_unavailable` (LB — no fallback code in `SonnetWizardAgent`)
14. `test_llm_unavailable_surfaces_as_503_not_governance_refusal` (LB, Standing Disposition #2)
15. `test_llm_unavailable_response_body_is_not_admission_refusal_shape`
16. `test_llm_unavailable_response_body_is_not_service_1_refusal_shape`
17. `test_no_direct_llm_calls_outside_shield` (existing top-level test re-run + still green — grep-negative on `anthropic`/`httpx` LLM outside `services/synisense/shield/*`)

**Dual-delta gate (Owner Visibility-not-prohibition mechanical application):**
18. `test_standard_or_grain_changing_proposal_without_class_delta_fails` (LB, E6)
19. `test_standard_or_grain_changing_proposal_without_price_delta_fails` (LB, E6)
20. `test_reach_changing_proposal_admissible_without_dual_delta` (positive; reach isn't a §6.2/§6.3 semantic axis)
21. `test_dual_delta_uses_single_source_derivation` (grep-negative — mirror of E7 provenance single-source)
22. `test_accepted_proposal_records_both_deltas_were_rendered_on_turn_payload` (LB, E6 acceptance-visibility)

**Frozen contracts posture (byte-identity regression):**
23. `test_v0_paths_byte_identical_after_7b_2` (parametrised over **26** prior frozen contract source files — all 4 wizard contracts + 22 pre-wizard)
24. `test_composed_conclusion_synthesis_lines_untouched_at_7b_2` (Verdict A regression)
25. `test_operator_variant_state_machine_untouched_at_7b_2` (B-1 substrate byte-identical)
26. `test_operator_router_untouched_at_7b_2` (`routers/wizard_operator.py` SHA-identical)
27. `test_provenance_preservation_untouched_at_7b_2`
28. `test_frozen_contract_snapshot_parity_still_at_26` (parity count invariant)

**Regressions carried forward:**
29. `test_no_caller_cancelled_or_async_queue_saturated_code_anywhere`
30. `test_kill_and_restart_recovers_without_state_loss_or_duplicate_ledger_emission` (5b/6b/7b-1 G1 preservation)
31. `test_all_standing_dispositions_cite_owner_ruling` (structural rule regression — §0.1 remains at 9 entries or however many are in force; no new dispositions at B-2)

**Buyer router smoke (E2E):**
32. `test_wizard_buyer_session_endpoint_returns_ids_and_variant_buyer`
33. `test_wizard_buyer_turn_endpoint_appends_operator_turn_with_snapshot_ref`
34. `test_wizard_buyer_propose_endpoint_writes_proposal_with_dual_delta`
35. `test_wizard_buyer_freeze_endpoint_defers_admission_handoff_at_b_2` (B-3 boundary marker)

**Total: ~35 named gates** (some parametrised for byte-identity × 26 files).

**CI target:** 613 → ≥648 (35 new named gates + byte-identity parametrised × 26 = ~68 collected new cases). Realistic CI post-B-2 collect: ~680-700.

---

## 7. Rule 2 v2 sizing anchor

| Category | Estimated LoC | Lift source |
|---|---|---|
| `services/wizard/buyer_state_machine.py` | ~250 | `operator_state_machine.py` shape (286L) — high lift; buyer-specific delta injection is net-new |
| `routers/wizard_buyer.py` | ~250 | `wizard_operator.py` (264L) — high lift on 6/7 endpoints; `/propose` endpoint is net-new |
| `services/wizard/dual_delta.py` | ~140 | `provenance_preservation.py` (173L) declarative-table pattern — high lift |
| `services/synisense/shield/llm_router.py` extension (`SonnetWizardAgent` class + Sonnet 4.6 client wiring) | +130 (net addition) | Existing `LlmChat`/`UserMessage` invocation pattern in same file (lines 93-135); `WizardAgent` Protocol lifted verbatim from `services/wizard/agent_interface.py` |
| `services/wizard/operator_state_machine.py` modification (Condition A(i) preference-tier enforcement) | +15 (additive; existing lines untouched) | — |
| `services/wizard/session_persistence.py` modification (additive compound index) | +5 | — |
| `services/wizard/source_tagging.py` modification (buyer variant skip on Guard 1) | +8 | — |
| `server.py` (router mount) | +3 | Pattern lifted from `wizard_operator` mount at 7b-1 |
| Tests — `test_phase_7_stage_b_2_wizard.py` (~35 named gates including parametrised byte-identity) | ~750 | `test_phase_7_stage_b_1_wizard.py` (721L) — high lift on gate scaffolding; Sonnet fixtures + LLM-503 gates are net-new |
| Recorded fixture for temp=0.0 replay | ~40 | JSON fixture (machine-generated from a real Sonnet call at Stage B) |
| Close report `phase_7_stage_b_2.md` | ~200 | Mirrors B-1 close (206L) |
| **Total anticipated net-new** | **~1,791 LoC** | |
| **Anticipated lift** | **~600 LoC** (operator SM shape, operator router shape, provenance_preservation declarative pattern, `LlmChat` invocation, gate scaffolding) | |
| **Anchored band** | **1,600 – 2,000 LoC** (mid ~1,800) | |
| `snapshot_lloc_in_band: yes` | 26 contracts UNCHANGED — no snapshot deltas at B-2. | |

**Anticipated ratio at B-2 close:** overall ~1,791 / ~600 = **~3.0×** (much lower than B-1's ~23× because buyer heavily reuses operator scaffolding); discretionary-only projected **~1.5×**.

**Stop-and-judge triggers I will honor at Stage B close (Rule 2 v2 doctrine, not shrink cap):**
- If actual net-new exceeds **2,300 LoC** (+15% over top-of-band): enumerate cause-narrative in close report §Rule 2 accounting; ratify with documentation.
- If discretionary-only ratio exceeds **2.5×**: same enumeration + ratify.
- No shrink target enforced — Rule 2 v2 is discipline-not-ceiling per prior Owner ratification of B-1's +43%.

---

## 8. Standing constraints VERIFIED against Stage A plan

| Constraint | Compliance |
|---|---|
| 26 frozen contracts byte-identical | ✅ zero contract-file touches; parity gate remains at 26 |
| No LLM code in `services/wizard/*` | ✅ `SonnetWizardAgent` lands in `services/synisense/shield/llm_router.py`; wizard modules import the Protocol only |
| Shield boundary preserved | ✅ `test_no_direct_llm_calls_outside_shield.py` gate rerun in B-2 test file |
| Infra-not-refusal (Standing Disposition #2) | ✅ Sonnet errors → 503; three gates (14, 15, 16) enforce non-refusal shape |
| Frozen-field-changes-as-new-versions (Standing Disposition #1) | ✅ zero in-place mutations on any of 26 frozen contract files |
| Visibility-not-prohibition (Standing Disposition #8) | ✅ dual-delta gate lands the mechanical seam; visibility on-wire is mandatory not prohibitive |
| Agent-pluggable-with-stub-agent-first (Standing Disposition #7) | ✅ E4 proof-order preserved: `WizardAgent` Protocol from B-1 unchanged; `SonnetWizardAgent` is a NEW implementation of same interface; DeterministicStubAgent still runs the B-1 gates unchanged |
| No caller_cancelled / async_queue_saturated codes anywhere | ✅ regression gate 29 |
| No frontend touches (8a-lite in flight) | ✅ backend-only; zero `/app/frontend/*` changes |
| No new §0.1 Standing Dispositions | ✅ zero new dispositions at B-2 (§0.1 frozen per Owner correction); the two dispositions from Phase 7 Stage A close (Agent-pluggable + Visibility-not-prohibition) already landed at B-1 |
| Condition A gates landed | ✅ 4 gates in test roster (rows 1-4) |
| Condition B Plan Debt appended | ✅ verbatim into `/app/memory/ORCHESTRATOR_CONTINUITY.md` §0.2 at B-2 close |

---

## 9. Emergent LLM Key path

Sonnet 4.6 via Shield's existing `emergentintegrations.LlmChat` path. Owner explicitly said: "Use the standard Emergent LLM key path via Shield's config. Do NOT prompt for API keys." **No user prompt** — Stage B lifts the key from Shield's config lookup (existing pattern at `llm_router.py:41-80` via `os.environ.get("EMERGENT_LLM_KEY")` — verify at Stage B).

Sonnet-4.6 exact model identifier + parameter-name confirmation via `integration_playbook_expert_v2` at the START of Stage B implementation (one call; before any LLM code lands). This is the single external-integration check on B-2's path — no other integrations touch the boundary.

---

## 10. Non-goals (explicit deferrals to B-3)

- Commit-review UI feedback surfaces (Phase 8 rebuild)
- Freeze semantics for buyer variant (B-3 scope: buyer freeze → admission handoff)
- Admission handoff to `POST /api/objectives` (B-3)
- Operator/buyer surface reconciliation (both routers stand independently at B-2 close)

---

## 11. Ordering & escalation posture

- **Zero open questions.** All Owner dispatches absorbed.
- **Escalation cap (Owner standing correction):** if a HAZARD-STOP fires during Stage B, present it ONCE with a single recommended path (no A/B/C/D menu). Owner rules directly.
- **Ready to proceed** to Stage B upon Owner Stage A ratification.

---

*End of Phase 7 Stage B-2 Stage A proposal.*
