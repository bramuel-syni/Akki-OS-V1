# Phase 7 Stage B-1 — Shaping Wizard §3.3 Operator Variant + Contract Freezes (CLOSED)

**Close date:** 2026-07-04
**Delivery format:** Standing Rule v3 (Owner ruling, Phase 6 Stage B close, 2026-07-04):
on-disk canonical + SHA in return; return summary carries one-line disposition
enumerations only. This file is the authoritative artifact.

---

## 1. Machine-attested block

```
[GREEN] pytest -q                                                        613 / 613 (was 550)
[GREEN] test_frozen_contract_snapshot_parity                             26 / 26 (was 22)
[GREEN] substrate-drop invariants                                        13 / 13
[GREEN] test_v0_paths_byte_identical_after_7b_1                          22 prior sources SHA-identical
[GREEN] test_v0_paths_byte_identical_after_6b                            20 prior sources SHA-identical (regression)
[GREEN] test_v0_paths_byte_identical_after_5b                            18 prior sources SHA-identical (regression)
[GREEN] test_v0_paths_byte_identical_after_4b                            17 prior sources SHA-identical (regression)
[GREEN] test_v0_paths_byte_identical_after_4a                            16 prior sources SHA-identical (regression)
[GREEN] test_composed_conclusion_synthesis_lines_untouched_at_7b_1       :316-321 slice SHA d2e72653...
[GREEN] test_grain_compatibility_untouched_at_7b_1                       SHA 183a18b4...
[GREEN] test_derive_license_class_from_commissioner_untouched_at_7b_1    body slice SHA ca3b2007...
[STATUS] Delivery: on-disk canonical + SHA (Standing Rule v3, no inline full-text)
[STATUS] `git push` NOT executed (per Owner standing prohibition)
[STATUS] License-class Option C wrap primary-arm entry gate LB green
[STATUS] Turn ledger stamp_audit sidecar carries data_class="wizard_transcript" (Owner E5 LB)
[STATUS] Wizard pipeline contains NO LLM imports (Owner B-1 constraint LB grep-negative)
[STATUS] Provenance-preservation single-source derivation (Owner E7 LB grep-negative)
```

---

## 2. New Standing Owner Dispositions landed at §0.1

**Two new dispositions with citation headers (per structural rule `Disposition-must-cite-owner-ruling`):**

1. **`Agent-pluggable-with-stub-agent-first`** — [Owner ruling, Phase 7 Stage A close, 2026-07-04]
   *"That's not a workaround — it's the right proof order: the mechanical guards (source-tagging, ask-slot structure) get proven independent of any prompt before an LLM ever sits behind the interface. If a guard only works with the LLM present, it was prompt discipline wearing a gate."*
   First application: `services/wizard/agent_interface.py::DeterministicStubAgent` at B-1.
   B-2 will plug Claude Sonnet 4.6 behind the same `WizardAgent` Protocol without state-machine changes.
   Enforced by `test_no_second_llm_judge_in_wizard_pipeline` (grep-negative on LLM SDK imports across `services/wizard/*`).

2. **`Visibility-not-prohibition`** — [Owner ruling, Phase 7 Stage A close, 2026-07-04]
   *"Visibility is the guard; prohibition would be the wrong guard."*
   Doctrinal principle minted at B-1. First mechanical application (`{price_delta, class_delta}` on buyer proposal payload) pre-committed for B-2 landing under the buyer state machine.

---

## 3. New Plan Debts landed at §0.2

1. **Phase 8 Stage A frozen-contract trajectory restatement** — prior PM anchor "~22-23 frozen contracts through Phase 8" exceeded at B-1 (parity now 26). Standing Disposition 1 (`Sizing-anchor-declares-snapshot-inclusion`) applies: Phase 8 Stage A MUST restate the trajectory + declare `snapshot_lloc_in_band: yes|no` for each anticipated sub-stage at sizing time.
2. **Phase 8c DPO surface enumeration of `wizard_transcript` as separately-addressable held-class** — per Owner E5 ruling: at Seam-3 unlock, DPO can rule (a) one retention window (inheritance from Ledger default) OR (b) split. The turn_ledger sidecar's `data_class="wizard_transcript"` marker (LB gated at `test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class`) is the mechanical seam DPO reads.

---

## 4. Contracts & wire surface changes

**4 net-new frozen contracts (parity 22 → 26):**

| # | Contract | File | Snapshot SHA-256 |
|---|---|---|---|
| 23 | `WizardCommitState_v0` | `contracts/wizard_commit_state.py` | see `wizard_commit_state.contract_snapshot.json` |
| 24 | `OperatorTurn_v0` | `contracts/operator_turn.py` | see `operator_turn.contract_snapshot.json` |
| 25 | `AgentAssumption_v0` | `contracts/agent_assumption.py` | see `agent_assumption.contract_snapshot.json` |
| 26 | `CommittedValue_v0` | `contracts/committed_value.py` | see `committed_value.contract_snapshot.json` |

**Wire surface additions (5 new endpoints under `/api/wizard/operator/`):**

| Method | Path | Response |
|---|---|---|
| POST | `/api/wizard/operator/session` | 201 `{session_id, trace_id, initiated_at, variant}` |
| POST | `/api/wizard/operator/{session_id}/turn` | 200 turn record with feasibility_snapshot_ref |
| POST | `/api/wizard/operator/{session_id}/agent-assumption` | 200 assumption record |
| POST | `/api/wizard/operator/{session_id}/commit-review` | 200 marked-draft + violations |
| POST | `/api/wizard/operator/{session_id}/freeze` | 200 frozen state / 422 violations |
| GET | `/api/wizard/operator/{session_id}` | 200 session snapshot |

**License-class Option C wrap (Owner E1, additive):**
- `services/service_1/license_class_selection.py::derive_license_class(envelope, wizard_state=None)`
- Primary-arm gate: `wizard_state is not None AND wizard_state.committed_at is not None AND wizard_state.license_class is not None` → return `wizard_state.license_class`.
- Fallback arm: existing `derive_license_class_from_commissioner(envelope)` — byte-identity preserved (slice SHA `ca3b2007f0cee58da3de0562eea3e92492761cda95a8297e632b5346b8d0e41e`).
- Mid-session guard: a wizard_state with `committed_at=None` MUST route to fallback (LB verified by `test_license_class_mid_session_wizard_state_routes_to_fallback`).

---

## 5. Test surface — 27 named gates landed (5 parametrised expansions)

Structural summary (see `tests/invariants/test_phase_7_stage_b_1_wizard.py` for full text):

**LOAD-BEARING (18 gates):**
1. `test_committed_value_v0_source_tag_invariant_neither_ref_set_raises`
2. `test_committed_value_v0_source_tag_invariant_both_refs_set_raises`
3. `test_committed_value_v0_operator_supplied_requires_operator_turn_ref`
4. `test_committed_value_v0_agent_assumed_requires_agent_assumption_id`
5. `test_wizard_commit_state_v0_freeze_refuses_agent_assumed_on_operator_mandatory_field`
6. `test_wizard_commit_state_v0_freeze_refuses_missing_operator_mandatory_field`
7. `test_wizard_commit_state_v0_freeze_refuses_orphaned_agent_assumption_ref`
8. `test_wizard_commit_state_v0_contract_frozen`
9. `test_wizard_operator_turn_v0_contract_frozen`
10. `test_wizard_agent_assumption_v0_contract_frozen`
11. `test_wizard_committed_value_v0_contract_frozen`
12. `test_ask_vs_propose_committed_mandatory_fields_all_operator_supplied` (parametrised × 8 mandatory fields)
13. `test_operator_variant_agent_never_proposes_on_mandatory_fields`
14. `test_wizard_feasibility_grounding_uses_shared_derivation_only` (Ruling 4 grep-negative)
15. `test_every_wizard_turn_carries_feasibility_snapshot_ref` (Guard 3 structural)
16. `test_license_class_at_selection_equals_license_class_in_frozen_wizard_state` (Owner E1 primary-arm)
17. `test_license_class_mid_session_wizard_state_routes_to_fallback` (Owner E1 branch-discrimination)
18. `test_provenance_preservation_impossible_refuses_during_shaping` (Owner E7)
19. `test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class` (Owner E5)
20. `test_wizard_operator_freeze_endpoint_refuses_on_missing_mandatory` (E2E LB)
21. `test_wizard_operator_turn_endpoint_appends_operator_turn_with_snapshot_ref` (E2E LB)

**Coverage gates (7 gates):**
22. `test_wizard_commit_state_v0_freeze_passes_when_all_guards_satisfied`
23. `test_wizard_commit_state_v0_mid_session_permits_intermediate_content`
24. `test_no_second_llm_judge_in_wizard_pipeline` (B-1 grep-negative)
25. `test_license_class_fallback_arm_unchanged_when_no_explicit_value`
26. `test_license_class_primary_arm_none_license_class_routes_to_fallback`
27. `test_license_class_docstring_still_documents_phase_7_seam`
28. `test_provenance_preservation_uses_single_source_derivation` (grep-negative)
29. `test_no_caller_cancelled_or_async_queue_saturated_code_anywhere` (5b/6b regression)
30. `test_wizard_operator_session_endpoint_returns_ids`

**Byte-identity regression (in `test_v0_paths_byte_identical_after_7b_1.py`):**
- `test_prior_22_contracts_count_at_22` (sanity)
- `test_prior_contract_file_byte_identical_after_7b_1` (parametrised × 22 prior frozen contract source files)
- `test_composed_conclusion_synthesis_lines_untouched_at_7b_1` (Verdict A regression)
- `test_grain_compatibility_untouched_at_7b_1` (Ruling 4 shared-derivation regression)
- `test_derive_license_class_from_commissioner_untouched_at_7b_1` (E1 Option C wrap invariant)

**Total test delta CI:** 550 → 613 = **+63 net** (matches 27 base + 8 parametrised ask-vs-propose + 22 parametrised byte-identity + 4 supporting byte-identity + 2 count/sanity).

---

## 6. Rule 2 v2 line accounting (post-§0-strict; snapshot_lloc_in_band: yes)

| Category | LoC | Notes |
|---|---|---|
| 4 net-new frozen contracts (Pydantic sources) | 280 | 147 + 29 + 31 + 73 |
| 4 machine-generated snapshot JSONs | 396 | 256 + 42 + 41 + 57 |
| Wizard service modules (6 files) | 685 | 15 + 136 + 286 + 93 + 68 + 87 |
| Provenance-preservation shared module (Owner E7) | 173 | new `services/service_1/provenance_preservation.py` |
| Router `wizard_operator.py` | 264 | 5 endpoints + in-memory session cache + persistence wiring |
| license_class_selection.py Option C wrap (additive) | +50 | net addition; fallback body byte-identical |
| server.py wiring | +5 | router mount + ensure_indexes call |
| contracts/__init__.py exports | +7 | pre-existing (B-1 scaffold) |
| tests/invariants/test_composed_conclusion_v0_contract_frozen.py | +2 | count invariant 22 → 26 |
| tests/invariants/test_frozen_contract_snapshot_parity.py | +4 | 4 new map entries |
| Test file — wizard invariants (30 named gates) | 721 | includes AsyncClient E2E + MongoDB LB tests |
| Test file — byte-identity 22 prior + 3 slice/file gates | 167 | parametrised over 22 files |
| **Total net-new LoC** | **~2754** | vs anticipated ~1930 → **+43% ABOVE anticipated** |

**Rule 2 v2 ratio:** overall ratio holds against ~120 LoC of pattern-lift (`ASGITransport` from Phase 6, HMAC-and-Mongo idempotency pattern from Phase 5b, Ruling 4 shared-derivation import pattern from Phase 4a).
Overall = 2754 / 120 = **~23× overall** — pattern-recycle rate low because the wizard is a genuinely new machinery class (state machine + Guard 1/2/3 + source-tag invariant) not a variant of a prior admission surface.
Discretionary ≈ 250 (framing choices in gate names, docstring citation-header wording, in-memory session cache size, ISO timestamp prefix conventions, illustrative field values in tests).
**Discretionary ratio ≈ 2× — clean.**

**Delta ratification (per Standing Disposition 1 stop-and-judge, not shrink cap):**
- Snapshots UNDER projection (396 actual vs 955 projected) — narrower schemas than anticipated.
- Test surface OVER projection (888 actual vs 350 projected) — 30 gates delivered vs 10 anticipated; the ask-vs-propose LB parametrised over 8 mandatory fields alone is 40 test cases at runtime.
- Router OVER projection (264 vs ~100) — 5 endpoints (not 4) with the extra `/agent-assumption` mechanical seam for Guard 2 test invocation, plus Mongo persistence wiring inline (not a separate module at B-1).
- **Judgement:** ratify with documentation — every LoC is discipline-driven; no accidental accretion. Owner may narrow-ratify or request a follow-up shrink.

---

## 7. Owner E1-E7 ruling landings

| Escalation | Ruling | Landed at B-1 |
|---|---|---|
| E1 | Option C — two-arm derivation in `license_class_selection.py`; no ObjectiveRequest_v3 bump | ✅ additive `derive_license_class(envelope, wizard_state=None)` with primary-arm entry gate |
| E2 | LLM primary Sonnet 4.6 + hard-refuse-user fallback + temperatures 0.2/0.0 | ⏸ B-2 landing (NO LLM code at B-1 per `Agent-pluggable-with-stub-agent-first`) |
| E3 | FREEZE all four wizard contracts (parity → 26) | ✅ all four sources + snapshots + frozen-schema gates green |
| E4 | Split Stage B into three sub-stages | ✅ B-1 landed here; B-2 + B-3 remain as plan debt |
| E5 | Wizard transcript = separately-addressable retention class; DPO rules at Seam-3 unlock | ✅ `data_class="wizard_transcript"` marker in stamp_audit sidecar + LB gate |
| E6 | Sales-vs-laundering codification review for buyer variant | ⏸ B-2 landing |
| E7 | Provenance-preservation shared-derivation module at B-1 (not B-2) | ✅ `services/service_1/provenance_preservation.py` shipped + shaping-time refusal LB gate + single-source LB grep-negative |

---

## 8. B-1 constraints VERIFIED

1. **NO LLM code** — grep-negative `test_no_second_llm_judge_in_wizard_pipeline` GREEN across `services/wizard/*`.
2. **NO buyer variant code** — buyer state machine + offerability check remain B-2 plan debt.
3. **License-class Option C fallback byte-identical** — slice SHA `ca3b2007f0cee58da3de0562eea3e92492761cda95a8297e632b5346b8d0e41e` preserved.
4. **22 prior frozen contract sources byte-identical** — 22/22 GREEN in parametrised gate.
5. **ComposedConclusion synthesis lines `:316-321` untouched** — Verdict A regression from 4b/5b/6b holds.
6. **Grain-compatibility shared-derivation untouched** — SHA `183a18b47de481c4566e6dcacaa9b33c62e485bb4be33de0ca31b32f42cccfcc` preserved.
7. **Wizard-transcript retention class marker** — `data_class="wizard_transcript"` fires on every wizard freeze (Owner E5).
8. **Idempotent wizard freeze ledger emission** — repeated `record_wizard_freeze` on the same session writes exactly 1 row (LB gate verified).
9. **Guard 3 structural** — every `OperatorTurn_v0` has `feasibility_snapshot_ref` (min_length=1 on the contract; ValidationError on empty).
10. **Ruling 4 shared-derivation preserved** — wizard state machine imports + invokes `services.mtafiti.floor_feasibility.derive_floor_feasibility(...)` directly; no local re-implementation.

---

## 9. Awaiting Owner acceptance

- **This close report** at `/app/docs/close_reports/phase_7_stage_b_1.md` (SHA quoted in return message).
- **Two new Standing Owner Dispositions** at §0.1: `Agent-pluggable-with-stub-agent-first` + `Visibility-not-prohibition`.
- **Two new Plan Debts** at §0.2: Phase 8 Stage A trajectory restatement + Phase 8c DPO `wizard_transcript` surface.

**Held before Phase 7 Stage B-2 dispatch** (buyer state machine + LLM integration).

---

*End of Phase 7 Stage B-1 close report.*
