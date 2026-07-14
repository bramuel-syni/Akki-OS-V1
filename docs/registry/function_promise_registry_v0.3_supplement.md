# Function & Promise Registry — v0.3 Supplement (IF-1 custody gates)

**Purpose:** carries this phase's (IF-1 execution · Shield custody reconnection + dead-code shave · doctrine §14 additive-supplement pattern) own R4 reflexive Registry rows, landed per Owner ruling **IF-1** (see `/app/docs/rulings/outstanding_register_v1_amendment_2026-07-12.md`) and **governance §14** (additive-supplement discipline).

**Source lock:** primary source-of-truth `/app/docs/registry/function_promise_registry_v0.md` remains byte-identical at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`. Prior supplements `/app/docs/registry/function_promise_registry_v0.1_supplement.md` byte-identical at SHA `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092`, `/app/docs/registry/function_promise_registry_v0.2_supplement.md` byte-identical at SHA `25c5dd5ac515b34a41584dd2b4ba4eab20eb0ae5d40d9022320761056555b79a`.

**Combined source per §14:** `(v0.md + v0.1_supplement + v0.2_supplement + v0.3_supplement)` ↔ `registry.yaml` — one set. MRR-G3 round-trip attests transparent extension to N supplements (path-list drives the check).

**Doctrine reference:** Registry Doctrine v1.0 §3.2 schema (11 mandatory fields) · §3.3 R4 · §14 additive-supplement pattern.

**Landed:** 2026-07-14 (atomic IF-1 commit with Shield chokepoint reconnection + shave + STEP A riders).

---

## §S1. R4 reflexive rows — IF-1 custody gates (3 rows · §3.2 schema)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `synisense.shield.custody_chain_wired` (IF1-G1) | Named surfaces (Shield chokepoint · reflexive) | Built to attest outbound text passes through `deidentifier.deidentify → llm_router.invoke_with_metering (litellm) → reidentifier.reidentify` in that exact order; a token in the outbound prompt is de-identified before reaching the LLM boundary; the reidentified response semantics match the pre-de-id token's contextual class per `reidentifier._VISIBLE_STRATEGY`. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shield_custody_chain.py::test_if1_g1_custody_chain_wired` | runtime check | 1 cell · ms class | shielded=True default + deidentifier + reidentifier module presence | 1 · Deterministic | Owner |
| `synisense.shield.fail_closed_deidentify_blocks_llm` (IF1-G2) | Named surfaces (Shield chokepoint · reflexive) | Built to attest that if `deidentifier.deidentify` raises `ServiceUnavailable` (spaCy-unloadable, tenant-lookup failure, or any other unrecoverable de-id failure), the LLM invocation does NOT occur AND the caller receives the ServiceUnavailable exception verbatim (fluency/brief synthesizers catch and route to mechanical arm per AF-E2 amended boundary; never a refusal envelope). | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_shield_custody_chain.py::test_if1_g2_fail_closed_deidentify_raise_blocks_llm` | runtime fail-closed cell | 1 cell · µs class | ServiceUnavailable → mechanical arm | 1 · Deterministic | Owner |
| `synisense.shield.fail_closed_reidentify_blocks_response` (IF1-G3) | Named surfaces (Shield chokepoint · reflexive) | Built to attest that if `reidentifier.reidentify` raises during the outbound seam (defence-in-depth; would be a bug given reidentify is pure regex), the LLM response is NOT returned to the caller — the exception surfaces via ServiceUnavailable at the chokepoint, preserving the never-return-raw-response guarantee. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_shield_custody_chain.py::test_if1_g3_fail_closed_reidentify_raise_blocks_response` | runtime fail-closed cell | 1 cell · µs class | reidentifier presence + exception propagation | 1 · Deterministic | Owner |

**Row count:** 3 IF1-G# reflexive rows for the custody chain.

---

## §S2. R4 reflexive rows — Shave attestations (10 rows · §3.2 schema)

Per Owner IF-1 close: for each row shaved, an AST-negative test attests the module no longer exists AND no live import references it. Row numbers reference `docs/audits/deviation_audit_v1.md` §Part B table (2026-07-12).

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `deviation.shave.row_01_client_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/client.py` no longer exists AND no in-tree file imports it; superseded by chokepoint-at-`llm_router.invoke_with_metering` (IF-1). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_01_client_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 1 | 1 · Deterministic | Owner |
| `deviation.shave.row_03_audit_log_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/audit_log.py` no longer exists AND no in-tree file imports it; chain-dead behind row 1. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_03_audit_log_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 3 | 1 · Deterministic | Owner |
| `deviation.shave.row_04_canonical_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/canonical.py` no longer exists AND no in-tree file imports it; zero-caller observability tool retired. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_04_canonical_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 4 | 1 · Deterministic | Owner |
| `deviation.shave.row_05_purpose_validator_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/purpose_validator.py` no longer exists AND no in-tree file imports it; `ALLOWED_PURPOSES` + `INTERNAL_ONLY_PURPOSE_PREFIXES` also removed from `services/synisense/config.py` per the shave-with-citation branch. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_05_purpose_validator_py_shaved` | AST-negative + fs-negative + config-negative | 1 cell · µs class | audit table row 5 | 1 · Deterministic | Owner |
| `deviation.shave.row_07_storage_service_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/storage_service.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_07_storage_service_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 7 | 1 · Deterministic | Owner |
| `deviation.shave.row_08_generate_fixture_incoming_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/data_source/synthetic_assets/rms_adversarial_v1/rejected/generate_fixture.incoming.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_08_generate_fixture_incoming_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 8 | 1 · Deterministic | Owner |
| `deviation.shave.row_09_generate_fixture_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_09_generate_fixture_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 9 | 1 · Deterministic | Owner |
| `deviation.shave.row_14_v1_harness_metrics_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/v1_harness/metrics.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_14_v1_harness_metrics_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 14 | 1 · Deterministic | Owner |
| `deviation.shave.row_15_purge_attestation_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/perception/purge_attestation.py` no longer exists AND no in-tree file imports it. Field access on `PerceptionResult.purge_attestation` (contract) is unaffected. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_15_purge_attestation_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 15 | 1 · Deterministic | Owner |
| `deviation.shave.row_16_telemetry_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/perception/telemetry.py` no longer exists AND no in-tree file imports it. Field access on `PerceptionResult.telemetry` (contract) is unaffected. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_16_telemetry_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 16 | 1 · Deterministic | Owner |

**Row count:** 10 shave-attestation rows.

---

## §S3. Promise attribution notes

Zero new promises introduced (Owner-explicit conservation posture held; IF-1 close does not mint promises, it wires existing chain + shaves dead surface).

- **PROM-S1-frozen-wire-contract** (v0.md §2) — IF1-G1 (custody chain wired verifies the chokepoint wire-contract) + 10 shave rows (dead-surface AST-negatives are wire-contract integrity checks) = 11 rows.
- **PROM-S3-audit-trail-immutable** (v0.md §2) — IF1-G2 + IF1-G3 (fail-closed gates preserve audit-trail integrity of "never reach LLM raw" and "never return raw response") = 2 rows.

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

---

## §S4. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** applied to IF-1 execution: additive supplement beside locked source. v0.md byte-identical at SHA `598a7ad4…` · v0.1_supplement byte-identical at SHA `2822f99e…` · v0.2_supplement byte-identical at SHA `25c5dd5a…`. v0.3_supplement is new sibling. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement + v0.3_supplement)` ↔ machine form as one set.

═══════════════════════════════════════════════════════════════════

*End of v0.3 supplement. 3 IF1-G* custody-chain gates + 10 shave-attestation gates = 13 R4 reflexive rows. Prior source-of-truth files byte-identical. Standing Rule v3 · on-disk canonical.*
