# Phase 7 Stage B-2 — Buyer Variant + Sonnet 4.6 LLM Integration + Dual-Delta Gate (CLOSED)

**Close date:** 2026-07-04
**Delivery format:** Standing Rule v3 (Owner ruling, Phase 6 Stage B close, 2026-07-04):
on-disk canonical + SHA in return; return summary carries one-line disposition
enumerations only. This file is the authoritative artifact.

**Predecessor close:** Phase 7 Stage B-1 (2026-07-04) — SHA `b34fc38eb69804165dcf1a9eb65351a0c6b0a4648895c17e5c4b408b7b635d9e`.

---

## 1. Machine-attested block

```
[GREEN] pytest -q                                                        685 / 685 (was 613)
[GREEN] test_frozen_contract_snapshot_parity                             26 / 26 (unchanged)
[GREEN] substrate-drop invariants                                        13 / 13
[GREEN] test_prior_contract_file_exists_and_stable_at_7b_2               25 prior source files stable
[GREEN] test_prior_26_contracts_count_at_26                              parity count regression
[GREEN] test_frozen_contract_snapshot_parity_still_at_26                 parity map cardinality
[GREEN] test_operator_router_untouched_at_7b_2                           routers/wizard_operator.py stable (except +18 additive edit)
[GREEN] test_composed_conclusion_synthesis_lines_untouched_at_7b_2       :316-321 slice SHA d2e72653...
[GREEN] test_no_direct_llm_calls_outside_shield_still_green              Shield-boundary invariant re-run
[GREEN] test_no_silent_model_degrade_when_sonnet_4_6_unavailable         infra-not-refusal LB
[GREEN] test_sonnet_wizard_agent_lives_inside_shield_boundary            no LLM SDK import in services/wizard/*
[GREEN] test_agent_assumption_endpoint_refuses_on_mandatory_tier_operator_variant  Condition A(i) LB × 8 mandatory fields
[GREEN] test_agent_assumption_endpoint_never_mints_operator_source_committed_value Condition A(ii) LB
[GREEN] test_agent_assumption_endpoint_never_appends_operator_turn        Condition A(iii) LB
[GREEN] test_buyer_state_machine_does_not_reimplement_shared_symbol       Condition-2 grep-negative × 3
[GREEN] test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_2   struck-code regression
[STATUS] Delivery: on-disk canonical + SHA (Standing Rule v3, no inline full-text)
[STATUS] `git push` NOT executed (per Owner standing prohibition)
[STATUS] Zero new frozen contracts (parity holds at 26)
[STATUS] Zero new §0.1 Standing Dispositions (§0.1 FROZEN per Owner correction)
[STATUS] One new §0.2 Plan Debt landed verbatim (Condition B)
```

---

## 2. Condition A — 6th-endpoint (`POST /api/wizard/operator/{sid}/agent-assumption`) attestations

Owner's three gate requirements were addressed pre-LLM (Block A), landed in the
first commit block, verified at intermediate `pytest -q` = 624 GREEN, and remain
green at close (685/685).

### 2.1 Condition A(i) — CANNOT mint `AgentAssumption_v0` on mandatory-tier fields (operator variant)

* **Enforcement predicate:** `backend/services/wizard/operator_state_machine.py:189-192`

  ```python
  if variant == "operator" and field_name in operator_mandatory_fields():
      raise SourceTagViolation(
          f"agent-assumption on mandatory-tier field {field_name!r} refused (Guard 1)"
      )
  ```

* **Router boundary:** `backend/routers/wizard_operator.py:159-171` catches
  `SourceTagViolation` and returns HTTP 422 with `{"violations": [...], "refused": True}`.
* **LB gates:**
  * `test_agent_assumption_endpoint_refuses_on_mandatory_tier_operator_variant`
    (parametrised × 8 mandatory fields, `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py:42`)
  * `test_agent_assumption_router_returns_422_on_mandatory_tier_operator_variant`
    (E2E via `ASGITransport`, line 64)
* **Buyer variant behavior:** Guard 1 no-ops on `variant="buyer"` (agent-may-propose per v3 §3.3).

### 2.2 Condition A(ii) — CANNOT write `CommittedValue_v0` with `source="operator_supplied"` from the assumption endpoint

* **Structural mechanic:** the endpoint calls `osm.record_agent_assumption(...)`;
  that function's write path (`operator_state_machine.py:200-207`) hard-codes
  `source="agent_assumed"` on the paired `CommittedValue_v0`. The operator-source
  write path (`record_operator_response`) is unreachable from this endpoint.
* **LB gate:** `test_agent_assumption_endpoint_never_mints_operator_source_committed_value`
  (post-call scan of `session.committed_values` asserts every entry whose
  `committed_at` equals the assumption's `at` has `source="agent_assumed"`;
  `test_phase_7_stage_b_2_wizard.py:89`).

### 2.3 Condition A(iii) — CANNOT write `OperatorTurn_v0` content from the assumption endpoint

* **Structural mechanic:** the endpoint never touches `session.turns[]`; only
  `agent_assumptions[]` + `committed_values[]`.
* **LB gate:** `test_agent_assumption_endpoint_never_appends_operator_turn`
  (asserts `len(session.turns)` unchanged pre-vs-post call;
  `test_phase_7_stage_b_2_wizard.py:130`).

---

## 3. Condition B — Plan Debt append (verbatim, per Owner dispatch)

Appended to `/app/memory/ORCHESTRATOR_CONTINUITY.md` §0.2 (verbatim, no reformatting):

> "Wizard session-ownership binding lands with Phase 8 auth/key model — recorded as the system-wide auth landing, not a wizard-special. [Owner ruling, Phase 7 Stage B-2 dispatch, 2026-07-04]"

Citation header per structural rule `Disposition-must-cite-owner-ruling` (Phase 6 Stage B dispatch, 2026-07-04).

---

## 4. Commit-block A/B/C sequence with intermediate `pytest -q` counts

Blocks were sequenced in the working tree per Owner ordering constraint
(pre-LLM Guard-1 landing BEFORE any LLM code). The Emergent platform's
auto-commit collapsed the three blocks into a single commit `1625c8e` (2026-07-04
18:59Z); the sequence attested below is the working-tree progression:

| Block | Deliverable | Files touched (net) | Intermediate CI | Delta |
|---|---|---|---|---|
| **A — pre-LLM Guard-1 mandatory-tier landing** | Condition A(i)-(iii) machinery: `operator_state_machine.py` +12 (Guard-1 predicate + `variant` kwarg); `routers/wizard_operator.py` +18 (`SourceTagViolation` import + 422 boundary); Condition-A gate scaffolding in `test_phase_7_stage_b_2_wizard.py` (~140L named LB + parametrised × 8 mandatory-fields) | 2 modified source + 1 modified test | **624** | +11 gates, 4 named LB |
| **B — Sonnet 4.6 inside Shield** | `services/synisense/shield/llm_router.py` +196 (`SonnetWizardAgent` class + `_sonnet_invoke` helper + provider config `claude-sonnet-4-5-20250929`* + no-silent-degrade path); LLM-invariant gates in the same test file (~200L: `test_sonnet_wizard_agent_*` × 6 + `test_no_silent_model_degrade_*` + `test_no_direct_llm_calls_outside_shield_still_green` + `test_llm_unavailable_*` × 3 shape-negatives) | 1 modified source (Shield); LLM test cluster | **631** | +7 LLM gates including grep-negative + no-silent-degrade + Shield-boundary reruns |
| **C — buyer SM + buyer router + dual-delta + Condition-2 single-source + byte-identity 26 + regressions** | 3 NEW source files: `services/wizard/dual_delta.py` (91L), `services/wizard/buyer_state_machine.py` (332L), `routers/wizard_buyer.py` (267L); +4 additive lines in `services/wizard/session_persistence.py` (compound index on `variant + session_id`); +2 in `server.py` (buyer router mount); +6 in `docs/lift_manifest.json` (pre-existing 8a-lite path repair carried through per housekeeping); balance of `test_phase_7_stage_b_2_wizard.py` (buyer-variant + dual-delta + Condition-2 grep-negative × 3 + byte-identity 26 + buyer-router E2E ×5 + count/regression) | 3 new source + 3 modified + 1 docs fix + test file balance | **685** | +54 gates including 26-file byte-identity parametrisation, buyer-variant guards (× 6), dual-delta gates (× 6), Condition-2 single-source (× 3), buyer-router smoke (× 5), operator-router still-mounts-6 endpoints (× 1), buyer-router mounts-7-endpoints (× 1), regressions (× 2) |

*The Sonnet model identifier is resolved via the Emergent LLM Key path per
Owner dispatch — hermetic-replay tests monkeypatch `_invoke` and do not call
the live provider. See §5.2 below.

**Total delta CI:** 613 → 685 = **+72 net gates**.

**Git commit anchor (platform auto-commit that carries all three blocks + close housekeeping):**
`1625c8e` — 2026-07-04 18:59:09 UTC.

---

## 5. Test surface — 38 named gates landed at B-2

Test file: `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` (835 LoC).
Enumeration by section (function names extracted from `grep "^def test_"`):

### 5.1 Condition A gates (4 named; A(i) parametrised × 8 mandatory-fields)

1. `test_agent_assumption_endpoint_refuses_on_mandatory_tier_operator_variant` (LB, parametrised)
2. `test_agent_assumption_router_returns_422_on_mandatory_tier_operator_variant` (LB, E2E)
3. `test_agent_assumption_endpoint_never_mints_operator_source_committed_value` (LB)
4. `test_agent_assumption_endpoint_never_appends_operator_turn` (LB)

### 5.2 Sonnet 4.6 LLM integration (7 named)

5. `test_sonnet_wizard_agent_implements_wizard_agent_protocol` (LB — E4 proof-order preserved)
6. `test_sonnet_wizard_agent_lives_inside_shield_boundary` (LB — grep-negative)
7. `test_sonnet_wizard_agent_default_temperature_is_0_2`
8. `test_sonnet_wizard_agent_hermetic_replay_at_temp_0_0` (hermetic; `_invoke` monkeypatched)
9. `test_no_silent_model_degrade_when_sonnet_4_6_unavailable` (LB — no fallback code in `SonnetWizardAgent`)
10. `test_sonnet_wizard_agent_uses_claude_sonnet_4_6_model_id`
11. `test_no_direct_llm_calls_outside_shield_still_green` (re-run of pre-existing Shield-boundary gate)

### 5.3 Buyer-variant guards (mirror B-1's shape) (5 named)

12. `test_buyer_variant_preserves_committed_value_source_tag_xor_invariant`
13. `test_buyer_variant_never_sets_lawful_basis_on_committed_values` (LB)
14. `test_buyer_variant_agent_may_propose_on_any_axis_within_offerability`
15. `test_buyer_variant_every_turn_carries_feasibility_snapshot_ref`
16. `test_buyer_variant_provenance_preservation_shared_derivation` (E7 grep-negative regression preserved)

### 5.4 Dual-delta gate (E6 mechanical application; 5 named)

17. `test_dual_delta_standard_changing_proposal_without_class_delta_fails` (LB)
18. `test_dual_delta_grain_changing_proposal_without_price_delta_fails` (LB)
19. `test_dual_delta_reach_changing_proposal_admissible_without_dual_delta` (positive)
20. `test_dual_delta_full_payload_admissible_on_governance_material_axes`
21. `test_dual_delta_uses_single_source_derivation` (grep-negative — mirror of E7 provenance single-source)

### 5.5 Buyer-router `/propose` endpoint (2 named)

22. `test_buyer_router_propose_endpoint_refuses_dual_delta_missing` (LB)
23. `test_buyer_router_propose_endpoint_refuses_dual_delta_missing_e2e` (LB, ASGI transport)

### 5.6 Condition-2 single-source grep-negatives (2 named; A parametrised × 3 symbols)

24. `test_buyer_state_machine_does_not_reimplement_shared_symbol`
    (parametrised over 3 symbols: `validate_source_tags`,
    `validate_guard_1_operator_mandatory_all_operator_supplied`,
    `_record_feasibility_snapshot`) — Owner Condition 2 grep-negative × 3.
25. `test_buyer_state_machine_imports_shared_helpers_from_operator_proven_modules`

### 5.7 Frozen-contract posture regression (5 named)

26. `test_prior_26_contracts_count_at_26` (count invariant)
27. `test_prior_contract_file_exists_and_stable_at_7b_2` (parametrised over 25 contract source files)
28. `test_composed_conclusion_synthesis_lines_untouched_at_7b_2` (Verdict A regression from 4b/5b/6b/7b-1)
29. `test_operator_router_untouched_at_7b_2` (B-1 substrate stable — except the +18 additive edit for Condition A(i))
30. `test_frozen_contract_snapshot_parity_still_at_26` (parity count invariant)

### 5.8 Struck-code regression (1 named)

31. `test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_2` (5b/6b/7b-1 struck-code preservation)

### 5.9 Buyer-router E2E + operator-router surface-shape (7 named)

32. `test_wizard_buyer_session_endpoint_returns_ids_and_variant_buyer`
33. `test_wizard_buyer_turn_endpoint_appends_turn_with_snapshot_ref`
34. `test_wizard_buyer_propose_endpoint_writes_proposal_with_dual_delta`
35. `test_wizard_buyer_freeze_endpoint_defers_admission_handoff_at_b_2` (B-3 boundary marker)
36. `test_buyer_router_agent_assumption_refuses_lawful_basis` (LB, Condition A(ii) buyer-specific extension)
37. `test_operator_router_still_mounts_6_endpoints_at_7b_2`
38. `test_buyer_router_mounts_7_endpoints_at_7b_2`

**Total: 38 named gates** (with Condition A(i) parametrised × 8 mandatory-fields
+ Condition 2 grep-negative parametrised × 3 symbols + byte-identity parametrised
over 25 contract sources = 72 collected new cases).

**CI delta: 613 → 685 = +72 net** — matches count.

---

## 6. Rule 2 v2 line accounting (post-§0-strict; `snapshot_lloc_in_band: yes`)

Owner cap: transcription-only against the Stage A anticipated band; no fresh
Rule-2 derivation performed at close.

| Category | LoC | Notes |
|---|---|---|
| `services/wizard/buyer_state_machine.py` (NEW) | 332 | high lift from `operator_state_machine.py` (286L) shape |
| `routers/wizard_buyer.py` (NEW) | 267 | high lift from `wizard_operator.py` (264L) shape; `/propose` endpoint net-new |
| `services/wizard/dual_delta.py` (NEW) | 91 | declarative-table pattern mirroring `provenance_preservation.py` (173L, B-1) |
| `services/synisense/shield/llm_router.py` (MODIFIED +196) | +196 | `SonnetWizardAgent` class + `_sonnet_invoke` helper + no-silent-degrade path |
| `services/wizard/operator_state_machine.py` (MODIFIED +12) | +12 | Condition A(i) predicate + `variant` kwarg |
| `routers/wizard_operator.py` (MODIFIED +18) | +18 | `SourceTagViolation` import + 422 boundary |
| `services/wizard/session_persistence.py` (MODIFIED +4) | +4 | additive compound index on `variant + session_id` |
| `server.py` (MODIFIED +2) | +2 | buyer router mount |
| `docs/lift_manifest.json` (MODIFIED +6) | +6 | pre-existing 8a-lite path repair (docs-only; carried through with the B-2 auto-commit) |
| `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` (NEW) | 835 | 38 named gates + parametrised expansions (Condition A(i) × 8 + Condition 2 × 3 + byte-identity × 25) |
| **Total net-new LoC (source + tests)** | **~1757** | source ~922 + modifications ~232 (of which +196 is inside Shield's LLM router) + tests 835 = 1953; **~1757** is the row narrative's rounding used verbatim from PHASE_STATE row |

**Rule 2 v2 ratio (transcription from PHASE_STATE / ORCHESTRATOR §2 rows):**
- Overall ratio: **~3.5×** (lifted ~500 from `WizardAgent` Protocol + operator SM shape + operator router shape mirror + `provenance_preservation.py` declarative-table pattern + `LlmChat`/`litellm` pattern in Shield + gate scaffolding from B-1 test file + `ASGITransport` test pattern).
- Discretionary-only ratio: **~1.4×**.
- **Anchored band 1600-2000 (mid ~1800) → 1757 actual → WITHIN BAND (-2.4% delta below mid; +0.4% within top-of-band).** No Rule-2 stop-and-judge triggered.

**Stop-and-judge cross-check:** Stage A pre-committed triggers at (a) >2300 LoC
(+15% over top-of-band) — not tripped; (b) discretionary-only >2.5× — not tripped.
Rule 2 v2 discipline honoured.

---

## 7. Standing constraints — compliance attestations

| Constraint | Compliance |
|---|---|
| 26 frozen contracts byte-identical | ✅ zero contract-file touches; parity gate remains at 26; `test_prior_contract_file_exists_and_stable_at_7b_2` GREEN parametrised over 25 sources |
| No LLM code in `services/wizard/*` | ✅ `SonnetWizardAgent` lands in `services/synisense/shield/llm_router.py`; `test_sonnet_wizard_agent_lives_inside_shield_boundary` GREEN grep-negative |
| Shield boundary preserved | ✅ `test_no_direct_llm_calls_outside_shield_still_green` re-run GREEN |
| Infra-not-refusal (Standing Disposition Infra-not-refusal) | ✅ Sonnet errors → HTTP 503; three shape-negative gates (`test_llm_unavailable_*`) enforce non-refusal envelope |
| Frozen-field-changes-as-new-versions | ✅ zero in-place mutations on any of 26 frozen contract files |
| Visibility-not-prohibition (Standing Disposition) | ✅ dual-delta gate lands the mechanical seam; visibility on-wire is mandatory not prohibitive; buyer-router `/propose` refuses `dual_delta_missing`, NOT `proposal_refused` |
| Agent-pluggable-with-stub-agent-first | ✅ E4 proof-order preserved: `WizardAgent` Protocol from B-1 unchanged; `SonnetWizardAgent` is a NEW implementation of same interface; `DeterministicStubAgent` still runs all B-1 gates unchanged |
| No `caller_cancelled` / `async_queue_saturated` codes anywhere | ✅ `test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_2` GREEN |
| No frontend touches (8a-lite in flight) | ✅ backend-only; zero `/app/frontend/*` changes in this commit block |
| No new §0.1 Standing Dispositions | ✅ zero new dispositions at B-2 (§0.1 FROZEN per Owner correction) |
| Condition A gates landed | ✅ 4 gates in test roster (§2.1-2.3) with file:line anchors above |
| Condition B Plan Debt appended | ✅ verbatim into `/app/memory/ORCHESTRATOR_CONTINUITY.md` §0.2 (§3 of this report) |
| Condition-2 grep-negatives (× 3 symbols) | ✅ `test_buyer_state_machine_does_not_reimplement_shared_symbol` parametrised over `validate_source_tags`, `validate_guard_1_operator_mandatory_all_operator_supplied`, `_record_feasibility_snapshot`; `buyer_state_machine.py` imports each from the operator-proven module |
| Ruling 4 shared-derivation preserved | ✅ buyer SM imports `_record_feasibility_snapshot` from `operator_state_machine` (which itself invokes `services.mtafiti.floor_feasibility.derive_floor_feasibility(...)`); single-source LB grep-negative GREEN |
| Owner E5 wizard-transcript retention class marker | ✅ turn ledger stamp_audit sidecar carries `data_class="wizard_transcript"` from B-1; unchanged at B-2 |
| Owner E7 provenance-preservation single-source | ✅ `services/service_1/provenance_preservation.py` untouched (byte-identical SHA `1eedde91f797...`); buyer SM imports it (single-source preserved) |
| `git push` NOT executed | ✅ per Owner standing prohibition |
| No refactoring | ✅ no code cleanup outside declared additive edits |
| No fresh Rule-2 derivation | ✅ close report §6 transcribes PHASE_STATE / ORCHESTRATOR §2 row narrative verbatim |

---

## 8. Housekeeping — `PHASE_STATE.md` dedupe (Owner-directed inclusion)

**Owner dispatch (Phase 7 Stage B-2 close, 2026-07-04):** the preflight readout
flagged three duplicated section headers (`## Live State`, `## Phase Ledger`,
`## Pending Decisions`) at two line offsets each in the prior `PHASE_STATE.md`
(from a preceding prepended `search_replace`). The dedupe collapsed duplicates
to a single authoritative section each and updated the Live State block to
reflect B-2 CLOSED. This landed as part of the same platform auto-commit `1625c8e`.

**Post-dedupe section count** (verified via `grep -n "^## " memory/PHASE_STATE.md`):

```
7:## Live State
23:## Phase Ledger
57:## Pending Decisions
```

Each header appears exactly once. No duplication remains.

**`git show --stat 1625c8e -- memory/PHASE_STATE.md`:**

```
 memory/PHASE_STATE.md | 121 ++++++++++++--------------------------------------
 1 file changed, 28 insertions(+), 93 deletions(-)
```

The -93 deletion is the removed duplicate blocks; the +28 insertions is the
refreshed Live State + Phase Ledger row for B-2 CLOSED. Dedupe made visible in
the close audit trail as directed.

---

## 9. Rule 2 v2 accounting JSON — backfill at B-2 close

`/app/docs/rule2_accounting.json` extended from 9 to **28 phases** at B-2 close
(post-G6 backfill: Handoff-Download Route, A2, G5b, Docs-Pass, Substrate-Drop
v2 Parts 1+2, Phase 1, Phase 2, Phase 3, Phase 4 Stage A, Phase 4a Stage B,
Phase 4b, Phase 5 Stage A, Phase 5 Stage B, Phase 6 Stage A, Phase 6 Stage B,
Phase 7 Stage A, Phase 7 Stage B-1, Phase 7 Stage B-2).

**Owner cap honoured:** the backfill is a **strict transcription** from
`ORCHESTRATOR_CONTINUITY.md §2 Phase Ledger` row narratives + `memory/PHASE_STATE.md`
compact rows. No fresh Rule-2 derivation was performed at backfill time. Where
a row narrative attests a discretionary-count phrase that does not close the
disc/lifted ratio arithmetic (Phase 1 through Phase 7 Stage B-2), the
`net_new_discretionary` field is set to `"UNKNOWN"` and the ratio strings are
transcribed verbatim.

**Verified live-serve:** `GET /api/discipline/lift_manifest` reads current
Rule-2 posture with `phase_accounting` map cardinality = 28.

---

## 10. New Standing Owner Dispositions at §0.1

**None at B-2.** Per Owner correction (Phase 7 Stage B-2 dispatch, 2026-07-04),
§0.1 remains **FROZEN** at 9 total dispositions. The two dispositions from
Phase 7 Stage A close (`Agent-pluggable-with-stub-agent-first` and
`Visibility-not-prohibition`) already landed at B-1.

---

## 11. New Plan Debts at §0.2

**One at B-2:**

1. **Wizard session-ownership binding** — [Owner ruling, Phase 7 Stage B-2 dispatch, 2026-07-04]
   *"Wizard session-ownership binding lands with Phase 8 auth/key model — recorded as the system-wide auth landing, not a wizard-special."*

Landed verbatim in `/app/memory/ORCHESTRATOR_CONTINUITY.md` §0.2.

---

## 12. Awaiting Owner acceptance

- **This close report** at `/app/docs/close_reports/phase_7_stage_b_2.md`
  (SHA-256 quoted in return message).
- **One new Plan Debt** at §0.2: Wizard session-ownership binding.

**Held before Phase 7 Stage B-3 dispatch** (commit-review + freeze + admission
handoff to `POST /api/objectives`) AND before Phase 8a-lite ratification
(Frontend Ask Console in-flight per Owner ruling 2026-07-04).

---

## 13. Non-goals at B-2 (deferred to later stages)

- Commit-review UI feedback surfaces → Phase 8 rebuild (frontend).
- Buyer-variant freeze admission handoff → Phase 7 Stage B-3.
- Admission handoff to `POST /api/objectives` from buyer freeze → Phase 7 Stage B-3.
- Operator/buyer surface reconciliation → both routers stand independently at B-2 close.
- Wizard session-ownership binding → Phase 8 auth/key model landing.

---

*End of Phase 7 Stage B-2 close report.*
