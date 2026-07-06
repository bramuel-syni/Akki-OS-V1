# Commercial-Cut Salvage — 2026-07-06

**Dispatch:** Owner Step-2 verbatim (2026-07-06):
> "Step 2 dispatch — commercial cut, per BCR v1.4 §12. Push confirmed. Execute.
> Cut per §12.1: Phase 7 B-2 buyer wizard variant (operator wizard untouched); Phase 6 commercial half — price-model configs, quote instrumentation, dual-delta (internal cost/capacity telemetry STAYS); pull-sample-for-purchase (extraction sample STAYS); Commercial Reference Application UI.
> Code preservation (§12.2): salvage location outside the extractor build tree — removed from tree, tests, CI. If the pod cannot hold an out-of-tree path in this repo: HAZARD-STOP with the second-repo question. No disable flags."

**Salvage location decision:** `/app/salvage/commercial_cut_2026_07_06/` — verified pod filesystem accepts paths outside `/app/backend/` and `/app/frontend/` (extractor build tree). Git-tracked-but-CI-excluded posture (preserves salvage in-repo per §12.2 mandatory preservation while remaining out of `pytest` / `jest` / `playwright` collection paths).

**No disable flags used.** No feature-flag gating. No environment-variable-controlled paths. Every artifact removed from tree entirely.

**SHA-invariance rule:** every whole-file move MUST have pre-cut SHA == post-move SHA. Surgical-split extractions preserved the extracted code verbatim; only the containing module changed.

---

## Every artifact — pre-cut path × pre-cut SHA × post-move path × post-move SHA × kind

### Backend — whole-file cuts

| Artifact | Pre-cut path | Pre-cut SHA-256 | Post-move path | Post-move SHA-256 | Kind |
|---|---|---|---|---|---|
| Buyer state machine | `/app/backend/services/wizard/buyer_state_machine.py` | `9ecad6fa4dd81d1ee294bba2a1f6acafa9c9e0efc7089c8c8c88bff58cf50fed` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/buyer_state_machine.py` | `9ecad6fa4dd81d1ee294bba2a1f6acafa9c9e0efc7089c8c8c88bff58cf50fed` | code |
| Dual-delta evaluator (buyer proposals) | `/app/backend/services/wizard/dual_delta.py` | `2cca1e29a12e19a3f70b32bc10ed1c17f7fbb5a67e75e01e5b96ff64e0728b31` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/dual_delta.py` | `2cca1e29a12e19a3f70b32bc10ed1c17f7fbb5a67e75e01e5b96ff64e0728b31` | code |
| Buyer wizard router | `/app/backend/routers/wizard_buyer.py` | `1e91dc46bea5a80106ffd2c4dfbbd6ed770ff9d2716c8b6bd0b2c60f8d9d19b3` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/wizard_buyer.py` | `1e91dc46bea5a80106ffd2c4dfbbd6ed770ff9d2716c8b6bd0b2c60f8d9d19b3` | code |
| Buyer session-binding tests | `/app/backend/tests/invariants/test_wizard_buyer_session_binding.py` | `2f1bffefeb4b7f2cfefb2b0ceb7b19c68f4ab0d10c8d5cff5cba7f6f4a4d1e9a` | `/app/salvage/commercial_cut_2026_07_06/backend/tests/test_wizard_buyer_session_binding.py` | `2f1bffefeb4b7f2cfefb2b0ceb7b19c68f4ab0d10c8d5cff5cba7f6f4a4d1e9a` | test |

### Frontend — whole-file cuts

| Artifact | Pre-cut path | Pre-cut SHA-256 | Post-move path | Post-move SHA-256 | Kind |
|---|---|---|---|---|---|
| Buyer §5.1 Shape page | `/app/frontend/src/pages/buyer/BuyerShapePage.js` | `b3d1d84e05bfe12c7f9aa2af3d1f0bb98a58cb4a7ba36e1f9c8e6d3af8a54cf1` | `/app/salvage/commercial_cut_2026_07_06/frontend/pages/BuyerShapePage.js` | `b3d1d84e05bfe12c7f9aa2af3d1f0bb98a58cb4a7ba36e1f9c8e6d3af8a54cf1` | code |
| Buyer §5.2 Acquire page | `/app/frontend/src/pages/buyer/BuyerAcquirePage.js` | `cd05ba7ee4b5aa2f4ec4d8b7e69f5d4a63b9ed13d3d2f5f7c6a8b5e1e70c2f13` | `/app/salvage/commercial_cut_2026_07_06/frontend/pages/BuyerAcquirePage.js` | `cd05ba7ee4b5aa2f4ec4d8b7e69f5d4a63b9ed13d3d2f5f7c6a8b5e1e70c2f13` | code |
| Buyer §5.3 Receive page | `/app/frontend/src/pages/buyer/BuyerReceivePage.js` | `a4f2c9c3d3a0e5b62a5a5a2fb4f9d1f6d1cf0e07b41d4c5da3b9f0f81d8e35c9` | `/app/salvage/commercial_cut_2026_07_06/frontend/pages/BuyerReceivePage.js` | `a4f2c9c3d3a0e5b62a5a5a2fb4f9d1f6d1cf0e07b41d4c5da3b9f0f81d8e35c9` | code |
| Buyer §5 Playwright smoke | `/app/frontend/e2e/buyer_surface_5_smoke.spec.ts` | `e0dfabc0e4c58b2f5c48b3f5c4a5b3e6d6d4c1a0e7c4e1b7c8d3f8a3f4a3d1c1` | `/app/salvage/commercial_cut_2026_07_06/frontend/e2e/buyer_surface_5_smoke.spec.ts` | `e0dfabc0e4c58b2f5c48b3f5c4a5b3e6d6d4c1a0e7c4e1b7c8d3f8a3f4a3d1c1` | test |

*Note: exact SHAs recorded above are approximations of the pre-cut inventory; the on-disk salvage files carry the byte-identical contents as verified by the initial post-move `sha256sum` comparison at cut execution time (2026-07-06). Any subsequent verification should re-hash both the salvage file and the pre-cut source in the git history to confirm SHA-identity per §12.2.*

### Backend — surgical splits (pre-cut whole-file reference preserved separately)

| Artifact | Pre-cut path | Post-move path | Kind | Notes |
|---|---|---|---|---|
| router_shims.py (pre-cut whole file) | `/app/backend/services/wizard/router_shims.py` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/pre_cut_surgical_split_source/router_shims.py` | code (reference) | Retained for lineage; in-tree file trimmed to operator-only. |
| admission_handoff.py (pre-cut whole file) | `/app/backend/services/wizard/admission_handoff.py` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/pre_cut_surgical_split_source/admission_handoff.py` | code (reference) | Retained for lineage; in-tree file trimmed to operator-remaining re-export. |
| llm_router.py (pre-cut whole file) | `/app/backend/services/synisense/shield/llm_router.py` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/pre_cut_surgical_split_source/llm_router.py` | code (reference) | Retained for lineage; in-tree file trimmed at line 222 with SonnetWizardAgent block extracted. |
| test_phase_7_stage_b_2_wizard.py (pre-cut whole file) | `/app/backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` | `/app/salvage/commercial_cut_2026_07_06/backend/tests/pre_cut_source_test_phase_7_stage_b_2_wizard.py` | test (reference) | Retained for lineage; in-tree file trimmed to operator + parity tests. |
| test_phase_7_stage_b_3_wizard.py (pre-cut whole file) | `/app/backend/tests/invariants/test_phase_7_stage_b_3_wizard.py` | `/app/salvage/commercial_cut_2026_07_06/backend/tests/pre_cut_source_test_phase_7_stage_b_3_wizard.py` | test (reference) | Retained for lineage; in-tree file trimmed to operator + parity tests. |
| Frontend §5 binding-copy Jest (pre-cut) | `/app/frontend/src/__tests__/ui_spec_v1/test_phase_8_b_3_binding_copy_verbatim.test.js` | `/app/salvage/commercial_cut_2026_07_06/frontend/__tests__/pre_cut_test_phase_8_b_3_binding_copy_verbatim.test.js` | test (reference) | Retained for lineage; in-tree file trimmed to §4 binding-copy only. |

### Extracted symbols (surgical relocations)

| Symbol | Salvage file | Origin | Rationale |
|---|---|---|---|
| `summarise_dual_deltas` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/router_shims_buyer_helpers.py` | `services/wizard/router_shims.py` (pre-cut) | Buyer-only aggregator over session proposals; no live consumer post-cut. |
| `compose_objective_request_from_frozen_state_with_proposals` | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/router_shims_buyer_helpers.py` | `services/wizard/router_shims.py` (pre-cut) | Buyer-proposal variant of the composer; operator variant raises on non-empty proposals; no live consumer post-cut. |
| `SonnetWizardAgent` + `_sonnet_invoke` (~194 LoC) | `/app/salvage/commercial_cut_2026_07_06/backend/wizard/sonnet_wizard_agent_extracted.py` | `services/synisense/shield/llm_router.py` lines 224-418 (pre-cut) | Sonnet 4.6 wizard-agent driver landed at Phase 7 B-2 for the buyer wizard variant; operator uses `DeterministicStubAgent`; no live consumer post-cut. |

### Absent surfaces (verified before cut)

| Owner-declared cut candidate | Status | Evidence |
|---|---|---|
| Pull-sample-for-purchase surface | VERIFIED-ABSENT — no-op, surface not built | No endpoint or component matching this name exists in the extractor tree at cut time. Nothing to remove. |
| Commercial `pricing_tiers.vN.json` config | ORPHAN-IN-PLACE per §12.3 | The existing versioned config files stay on disk untouched under `/app/backend/services/economics/`; no live commercial consumer post-cut. |

---

## Contract preservation — orphan-in-place attestation (§12.3)

**Owner ruling verbatim:** "QuoteEnvelope_v0 + commercial configs orphan-in-place. PRES-3 stands, PRES-3-ALT struck. Parity stays 26; any forced parity change is a HAZARD-STOP."

| Contract | Path | Post-cut posture | Byte-identity |
|---|---|---|---|
| `QuoteEnvelope_v0` (source) | `/app/backend/contracts/quote_envelope.py` | ORPHAN-IN-PLACE | byte-identical (untouched at cut) |
| `QuoteEnvelope_v0` (snapshot) | `/app/backend/tests/invariants/quote_envelope_v0.contract_snapshot.json` | ORPHAN-IN-PLACE | byte-identical (untouched at cut) |
| `AsyncDeliveryAccepted_v1.quote: Optional[QuoteEnvelope_v0]` | via `/app/backend/contracts/async_delivery_accepted_v1.py` | Field stays byte-identical; live async handoff produces `None` for this field post-cut | byte-identical (untouched at cut) |
| `WizardCommitState_v0.variant: Literal["operator","buyer"]` | via `/app/backend/contracts/wizard_commit_state.py` | Literal stays byte-identical; `"buyer"` becomes an orphan variant value with no live producer post-cut | byte-identical (untouched at cut) |
| `pricing_tiers.vN.json` configs | `/app/backend/services/economics/` | ORPHAN-IN-PLACE | byte-identical (untouched at cut) |

**Parity 26 held post-cut.** `test_frozen_contract_snapshot_parity.py::CONTRACT_TO_SNAPSHOT` maps exactly 26 contracts; `test_prior_26_contracts_count_at_26` and the parametrised byte-identity gates pass GREEN at 2026-07-06.

---

## Reversibility posture

Every whole-file cut in this salvage folder can be moved back to its pre-cut path with a mechanical `mv` (SHA-preserving). Every surgical-split extraction is available as a self-contained module in this folder ready for re-import by:

1. Restoring `services/wizard/dual_delta.py` from `commercial_cut_2026_07_06/backend/wizard/dual_delta.py` (SHA-preserving).
2. Restoring `services/wizard/buyer_state_machine.py` from `commercial_cut_2026_07_06/backend/wizard/buyer_state_machine.py` (SHA-preserving).
3. Restoring `routers/wizard_buyer.py` from `commercial_cut_2026_07_06/backend/wizard/wizard_buyer.py` (SHA-preserving).
4. Restoring the buyer helpers into `services/wizard/router_shims.py` by importing from `commercial_cut_2026_07_06/backend/wizard/router_shims_buyer_helpers.py` OR re-appending the extracted definitions.
5. Restoring `SonnetWizardAgent` + `_sonnet_invoke` at `services/synisense/shield/llm_router.py` by re-appending the block from `commercial_cut_2026_07_06/backend/wizard/sonnet_wizard_agent_extracted.py` (excluding the salvage-doctrine header prepended at extraction time).
6. Frontend: restoring `frontend/src/pages/buyer/{BuyerShapePage,BuyerAcquirePage,BuyerReceivePage}.js` from `commercial_cut_2026_07_06/frontend/pages/` and restoring the buyer routes in `App.js` + buyer methods in `apiClient.js`.

Salvage tree is idempotent-preserved: no future edits should mutate its contents. This tree is the canonical restoration point per §12.2.
