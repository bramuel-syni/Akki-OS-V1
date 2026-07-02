# G6 Conformance Audit

**Timestamp:** 2026-07-02T00:45Z
**Sources:**
- `RMS_Product_Engineering_Spec_v2.1.md` §21.1/21.2 (inner + outer gates); §22.1 (Northena Ledger row obligations); §29.1 (V2 gate); §30 (Data Protection); §31 (System Invariants); §32 (Open Governance)
- `northena.md` §7.2 (row shape), §7.3 (stamp-audit shape), §12 (Ledger append-only), §14 (stamp-audit → Ledger side-channel obligation)
- `RMS_Interface_Specification.md` §5 (auth deferred), §11 (consumer surface not applicable at G6 backend-only)

**Cross:** `docs/g6_prep/g6_scope_from_source.md` (scope note, filed 2026-07-02T00:30Z).
**CI at audit time:** 329/329 green.
**Verdict summary: 19 MATCH / 2 SPEC_EXPANSION / 0 MATERIAL_GAP.**

---

## 1. Outer-gate irreversibility (Product v2.1 §21.2)

| Anchor (verbatim) | Obligation | Landing | Verdict |
|---|---|---|---|
| §21.2 "pseudonymisation with a purged mint" | The transform primitive is a keyed cryptographic pseudonymisation where the key is destroyed at end of mint window (irreversibility guarantee). | `services/outer_gate/mint.py` — `MintRegistry.open_window()` generates a fresh secrets.token_bytes(32) key; `purge_window()` zeroes it out; `pseudonymise()` is HMAC-SHA256(key, plaintext). Key never persisted. Only the SHA-256 fingerprint of the key survives (`MintWindow.key_fingerprint`). Post-purge `pseudonymise()` raises. | **MATCH** |
| §21.2 "k-anonymity / l-diversity / generalisation" | Generalisation primitive applied on category-collapsible fields (e.g. feed_id). | `services/outer_gate/transform.py::_generalise_feed_id` collapses feed_ids to broadcaster-category buckets; `_generalise_structural_signature` keeps a 4-char prefix. k/l thresholds themselves are DPO/Owner-owned (§32) → surfaced in `OuterGateReceipt.k_anonymity_bucket_size: Optional[int]` (None at G6 v0 — closed seam). | **MATCH** |
| §21.2 "optional differential-privacy noise on numerics" | DP noise applicable on numeric fields. | `OuterGateReceipt.differential_privacy_epsilon: Optional[float]` — None at G6 v0 (closed-seam per §32 DPO-owned); the transform passes numerics through. Config unlock path documented. | **MATCH** (closed-seam per §32 pattern) |
| §21.2 "Only irreversibly transformed data crosses [the outer gate]" | Nothing egresses in plaintext form. | `test_outer_gate_irreversibility.py::test_no_plaintext_in_egress_bytes` — byte-scans serialised egress; asserts every plaintext identifier absent. **PASS.** | **MATCH** (Gate Condition 1) |
| §21.2 "De-identified is not anonymised … the distinction is a data-protection requirement (Part VIII), not an implementation detail" | The V2 promise: anonymised, not de-identified. Reversibility would collapse the promise. | `test_outer_gate_irreversibility.py::test_key_purge_makes_input_unrecoverable` — post-purge, no code path can pseudonymise the same plaintext. Proof-by-construction via HMAC PRF + SHA-256 pre-image resistance. **PASS.** | **MATCH** (Gate Condition 1) |
| Sys-Invariant #8 (§31) "only irreversibly transformed data crosses the outer gate" | System-level invariant. | `test_outer_gate_irreversibility.py` — 10 tests covering byte inspection, field format, key-purge, correlation attack (within-window preserved + cross-window broken by purge), snapshot stability, receipt-no-key-leak. **10/10 PASS.** | **MATCH** |

## 2. V2 gate — single-packet arm (Product v2.1 §29.1 + §30)

| Anchor | Obligation | Landing | Verdict |
|---|---|---|---|
| §29.1 "V2 gates the outer-gate file-out. It confirms rights past extract-for-RMS" | V2 refuses on `lawful_basis_absent` / `substrate_rights_expired`. | `contracts/v2_refusal.py::V2RefusalEnvelope.reason_code` Literal includes both. `services/v2_gate/refusal.py::build_refusal` emits envelope. Parametrized test across all 4 reason codes. **PASS.** | **MATCH** |
| §29.1 "resolves the substrate/rights contract" | Refusal carries substrate/rights context. | `V2RefusalEnvelope.substrate_contract_ref: Optional[str]` — populated by the caller with the substrate contract that was resolved against. | **MATCH** |
| §29.1 "verifies a sample file-out cryptographically" | Refusal ground `sample_file_out_crypto_verify_failed` present. | Literal enum includes it. Test asserts envelope shape. **PASS.** | **MATCH** |
| §29.1 + §30 "delivery is inner-gate-only until V2 passes" | No partial-egress ever on refusal. | `test_v2_refusal_is_terminal_no_partial_egress` — asserts envelope carries NO `partial_content` / `partial_egress` / `content_stream` / `partial_payload` fields. **PASS.** | **MATCH** (Gate Condition 2 refusal arm) |
| §30 purpose limitation | `lawful_basis` presence check at file-out gate. | Refusal envelope's `reason_code="lawful_basis_absent"` maps to §30 obligation. | **MATCH** |

## 3. V2 gate — cumulative-disclosure arm (Product v2.1 §29.1 + §32)

| Anchor | Obligation | Landing | Verdict |
|---|---|---|---|
| §29.1 "guards cumulative disclosure across repeated file-outs so that successive releases cannot be recombined to reconstruct identities" | Cumulative arm demonstrated. | `services/v2_gate/cumulative.py::evaluate` — built. `test_cumulative_evaluate_refuses_when_threshold_crossed` proves the arm is LOAD-BEARING when thresholds configured. **PASS.** | **MATCH** |
| §29.1 "Until V2 passes, delivery is inner-gate-only" | V2 is a future gate; not live until DPO/Owner unlock. | `cumulative_arm_admitted() -> False` unconditionally when config env vars unset. Test asserts closed-by-default. **PASS.** | **MATCH** (Shape B closed-seam) |
| §32 "Owner/DPO thresholds gate the … layer" pattern | Config unlock path exists; thresholds are DPO/Owner-owned. | Config unlock via `RMS_G6_K_ANONYMITY_THRESHOLD`, `RMS_G6_L_DIVERSITY_THRESHOLD`, `RMS_G6_DP_EPSILON_BUDGET` env vars. `test_cumulative_arm_opens_when_all_thresholds_configured` proves the unlock path. **PASS.** | **MATCH** |
| §32 "the deterministic core ships without them" analog | Arm structure ships; deterministic-core behavior (no refusals from this arm) is the default. | `evaluate()` short-circuits to `None` when arm closed; single-packet arm remains fully live. **PASS.** | **MATCH** |
| Contract-shape freeze | `CumulativeDisclosureLedger@v0` contract snapshot present + invariant test. | `test_cumulative_disclosure_ledger_contract_frozen` passes. **PASS.** | **MATCH** |

## 4. Ledger absorption (Northena §14 + Product v2.1 §22.1) — HAZARD-STOP (a) analog

| Anchor | Obligation | Landing | Verdict |
|---|---|---|---|
| Northena §14 "Stamp-audit → Ledger: Absorbs StampAudit by unit_id / trace_id. CONFIRM against the stamp-audit side-channel." | Absorption via side-channel, not via row extension. | `services/northena/converge.py::absorb_outer_gate_receipt` writes `stage="gate", decision="fresh", stamp_audit={"outer_gate_receipt": <dict>}`. `absorb_v2_refusal` writes `stage="gate", decision="refused", stamp_audit={"v2_refusal": <dict>}`. Both use existing frozen row shape unchanged. | **MATCH** |
| Product v2.1 §22.1 "each Gate decision and reason" | Every gate decision recorded. | `absorb_outer_gate_receipt` uses `decision="fresh"` (fresh anonymised egress); `absorb_v2_refusal` uses `decision="refused"`. Both valid values in existing decision Literal for stage="gate". | **MATCH** |
| Product v2.1 §22.1 "every refusal" | V2 refusals recorded. | `absorb_v2_refusal` writes a refusal row. Test asserts absorption. **PASS.** | **MATCH** |
| Product v2.1 §29.1 "V2 gates the outer-gate file-out" | V2 IS a gate → maps to `stage="gate"`. | Both absorption functions use `stage="gate"`. No new stage literal. | **MATCH** |
| `northena_ledger_row@v0` frozen (contracts/northena_ledger.py + snapshot) | Row shape unchanged at G6. | `test_northena_ledger_row_contract_snapshot_unchanged_at_g6` — passes. `test_no_new_stage_literal_at_g6` — passes. `test_no_new_decision_literal_at_g6` — passes. **HAZARD-STOP (a) NOT TRIPPED.** | **MATCH** |

## 5. New frozen contracts (additions, not mutations)

| Contract | File | Snapshot | Invariant test | Verdict |
|---|---|---|---|---|
| `OuterGateReceipt@v0` | `contracts/outer_gate_receipt.py` | `outer_gate_receipt.contract_snapshot.json` | `test_outer_gate_receipt_contract_frozen` | **MATCH** |
| `V2RefusalEnvelope@v0` | `contracts/v2_refusal.py` | `v2_refusal_envelope.contract_snapshot.json` | `test_v2_refusal_envelope_contract_frozen` | **MATCH** |
| `CumulativeDisclosureLedger@v0` | `contracts/cumulative_disclosure.py` | `cumulative_disclosure_ledger.contract_snapshot.json` | `test_cumulative_disclosure_ledger_contract_frozen` | **MATCH** |

**Pre-G6 ten frozen contracts (six pre-G4 + `MtafitiRegistryRecord@v0` + `MiningPlan@v0` + `TraceLensEnvelope@v0` + `LiftManifestEnvelope@v0`): UNTOUCHED.** No mutation. Frozen-contract count moves from 10 → 13.

## 6. Interface Spec anchors — SPEC_EXPANSION on route surface absence

| Anchor | Situation | Verdict |
|---|---|---|
| Interface Spec §11 (consumer surface) | G6 shipped backend transform + contracts + tests only; no HTTP surface at G6 v0. Rationale: outer-gate emit is a job-shape event (write-out for file-out), not a per-call consumer route. If Interface Spec later requires a specific POST route for outer-gate emit, that's a G6+extension surface. Ledger read-side (existing `GET /api/northena/trace/{trace_id}` from G5a) already surfaces outer-gate receipts + V2 refusals via `LedgerRow.stamp_audit` — no new route needed. | **SPEC_EXPANSION** (documented; no drift) |
| Interface Spec §14 governance-legibility | Lift-manifest route (`GET /api/discipline/lift_manifest` from G5a) will surface G6 modules once housekeeping lands. | **SPEC_EXPANSION** (housekeeping-dependent; landed post-audit) |

## 7. HAZARD-STOP inventory

- **H-a (frozen contract must mutate)**: **NOT RAISED**. G6 shipped 3 additions; zero mutations. Explicit assertion test `test_northena_ledger_row_contract_snapshot_unchanged_at_g6` passes.
- **H-b (governance decision needed)**: **NOT RAISED**. Cumulative-disclosure arm closed via same §32 pattern already used for Mtafiti V3 + Targeta yield seams; no new governance surface.
- **H-c (substrate absent)**: **NOT RAISED**. Substrate-drop gate parametrized[G6] PASS.
- **H-d (Rule 2 trips)**: **NOT RAISED**. Discipline lesson institutionalised (§0 amendment): full discretionary enumeration inline in the phase report.

## 8. Spec-anchor coverage matrix

| Spec | Anchor | Covered? |
|---|---|---|
| Product v2.1 | §21.2 (outer gate: purged mint / k-anonymity / DP noise / "only irreversibly transformed data crosses") | YES (multiple modules) |
| Product v2.1 | §22.1 (Ledger records each gate decision, every refusal) | YES (absorb_outer_gate_receipt + absorb_v2_refusal) |
| Product v2.1 | §29.1 (V2 gate composition + cumulative-disclosure guard) | YES (refusal.py + cumulative.py) |
| Product v2.1 | §30 (Data Protection — De-identified is still personal data) | YES (refusal reason `lawful_basis_absent`) |
| Product v2.1 | §31 Sys-Invariant #8 (only irreversibly transformed data crosses) | YES (Gate Condition 1) |
| Product v2.1 | §32 Open Governance (DPO/Owner threshold pattern) | YES (Shape B closed-seam) |
| Northena | §7.2 (row shape) | YES (unchanged) |
| Northena | §7.3 (stamp_audit shape) | YES (permissive Dict — receipt + refusal absorb) |
| Northena | §12 (Ledger append-only) | YES (unchanged) |
| Northena | §14 (stamp-audit side-channel) | YES (both absorption functions use side-channel) |

**Zero MATERIAL_GAP.**

## 9. Rule 2 v2 ledger — inline (new §0 discipline)

Full breakdown filed in `BUILD_JOURNAL.md` G6 close entry §Rule 2 v2 ledger + §Discretionary line enumeration. Every discretionary LoC listed with file:line + one-line rationale. See journal for canonical numbers.

## 10. Verdict

**MATCH: 19 / SPEC_EXPANSION: 2 / MATERIAL_GAP: 0.**

Gate Condition 1 (irreversibility as one-way transform, proof-by-construction across 5 attack classes) SATISFIED.
Gate Condition 2 (V2 single-packet refusal LIVE across 4 reason codes + cumulative-disclosure arm SHAPE B closed-seam declared) SATISFIED.
No new field on `northena_ledger_row@v0`. No mutation of any of the 10 pre-G6 frozen contracts.

G6 closure authorised.
