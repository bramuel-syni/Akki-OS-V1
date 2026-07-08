# Artifact Store · Close Report (BCR §3.2 V3 last mile)

**Close date:** 2026-07-08
**Sequence position:** BCR §5.1 line 314 — *"3. Artifact store (3.2) — the only gap that is purely a decision plus a small phase; unblocks V3's done-condition and is a dependency of 3.7."*
**Dispatch discipline:** §4.1 baseline atomic first-commit per Owner post-8-EXT-ratification dispatch (execute directive baked into rulings message).
**Governance model:** 3-tier ruling model (`docs/governance/tiered_ruling_model.md`) — first phase executed under the new model.

**Standing Rule v3:** on-disk canonical. Reply body carries SHA + tier tags only.

---

## §1. Artefact map (SHA-256 anchored)

### §1.1 New files landed at Artifact Store

| Path | SHA-256 | LoC | Purpose |
|---|---|---:|---|
| `backend/contracts/outer_gate_receipt_v1.py` | `dc0ad43da72f3c22fd17f64b862d08ff9aa8ed3f1a79f6037706461c9255a379` | 103 | AS-E1 α: NEW frozen contract `OuterGateReceiptV1` = v0 shape + `artifact_sha256` + `artifact_key` (both `Optional[str]`). |
| `backend/tests/invariants/outer_gate_receipt_v1.contract_snapshot.json` | `94a982815439ff7f6602e9adc3ab936fb481ab529e0613a0e4bbb3890f93d075` | 155 | AS-E1 α: snapshot of v1 schema (parity 29 assertion). |
| `backend/services/artifact_store/__init__.py` | `b41f42f9018f08b7943556ffe9603416cbf8c0502be93135e43780a54a730bc7` | 29 | Package barrel. |
| `backend/services/artifact_store/adapter.py` | `b63fb1eed9b27b7c3be73cc0812720455482d8b0bad58cb0305a7ae3361e012c` | 202 | AS-I1 three-op adapter · `put_once` / `get` / `head` · AS-E4 γ split (`_get_raw` private + `get(key, caller_scope)` public REQUIRED-scope) · dev-tier local FS at `RMS_ARTIFACT_STORE_ROOT` (default `/tmp/rms_artifact_store`) · ext whitelist `{json,csv,parquet,bin,txt}`. |
| `backend/services/artifact_store/atomic_write.py` | `252c1fc11db7f47951e344f93ca8cbc3f7905056c7b1623cc491f9b335b5a062` | 252 | AS-E2 γ six-step atomic write coordinator + `reconcile_incomplete_write()` recovery rule (tmp threshold `RMS_ARTIFACT_STORE_TMP_THRESHOLD_SECONDS`, dev default 300s). |
| `backend/services/artifact_store/orphan_scan.py` | `a32b04611eae2bc7d9a63711071c6cbf6ea0c3eae50219a23ffb17fac5b7c49f` | 94 | AS-E3 α READ-ONLY orphan scanner + AS-E2 interplay (in-flight tmp classification). |
| `backend/routers/artifact_store.py` | `480d9f8252a0753d4f9b914f344b47557b7a7664a270309f0edda16d15ea2b72` | 125 | AS-U1 + AS-B3 · GET + HEAD download endpoints · `ScopeInsufficientError` → `auth_refusal.emit('auth_scope_insufficient', ...)` (4-code closure) · NO DELETE handler (AS-H1). |
| `backend/tests/invariants/test_artifact_store.py` | `4fb16a3ab387802496d4cf13c1df3ccf8b4bc5370f98addff4022b3f5f8677e9` | 579 | 22 cells: AS-G1..G6 + V1-G7@29 + v0 preservation + 4-code closure + E5 no-409 + AS-H1 no-DELETE + fixtures. |
| `docs/rulings/artifact_store_as_e1_to_e4.md` | `62e0aa732671c76fea68b6dc4d2d398163289f912d02bc6c3efaa0a4396a7c8e` | 105 | Owner AS-E1..E4 verbatim rulings on-disk. |
| `docs/close_reports/artifact_store.md` | *(SHA at commit-time)* | — | This report. |

### §1.2 Modified files at Artifact Store

| Path | Δ LoC | Purpose |
|---|---:|---|
| `backend/server.py` | +7 | Mount `artifact_store_router` on `/api/artifacts`. |
| `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` | +1 | Add `outer_gate_receipt_v1.py → outer_gate_receipt_v1.contract_snapshot.json` mapping. |
| `backend/tests/invariants/test_8_ext.py` | +10 −6 | V1-G7 parity assertion 28 → 29 (semantic-drift note in docstring: post-Artifact-Store total). |
| `backend/tests/invariants/test_composed_conclusion_v0_contract_frozen.py` | +6 −3 | Parity assertion 28 → 29 (running-total invariant; snapshot preserved bijection). |
| `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` | +2 −2 | Parity assertion 28 → 29. |
| `backend/tests/invariants/test_phase_7_stage_b_3_wizard.py` | +2 −2 | Parity assertion 28 → 29. |
| `backend/tests/invariants/test_phase_9_sub_stage_9_1_and_9_3.py` | +3 −3 | Parity assertion 28 → 29. |

### §1.3 v0 byte-identity attestation (AS-E1 α condition)

| Path | Pre-Artifact-Store SHA (STEP 1) | Post-Artifact-Store SHA (this close) | Verdict |
|---|---|---|---|
| `backend/contracts/outer_gate_receipt.py` | `11cd8544332aa2602cca32b55f75bc0dcb69d5a816deb7546fdb580bd338524c` | `11cd8544332aa2602cca32b55f75bc0dcb69d5a816deb7546fdb580bd338524c` | **BYTE-IDENTICAL** ✓ |
| `backend/tests/invariants/outer_gate_receipt.contract_snapshot.json` | `3de2a919e39c77837ed6879cab0cd9829a4ee3422146074144e8726777fd030c` | `3de2a919e39c77837ed6879cab0cd9829a4ee3422146074144e8726777fd030c` | **BYTE-IDENTICAL** ✓ |

Attested by `test_artifact_store.py::test_outer_gate_receipt_v0_byte_identical_at_artifact_store_close` GREEN.

---

## §2. AS-H1 non-trip attestation (verbatim carrier for the AS-E2 rollback clarification)

Owner ruling AS-E2 clarification (2026-07-08 verbatim):

> *"Clarification so AS-H1 isn't tripped: rollback of an incomplete write is transaction mechanics, not data deletion — the artifact never existed in the governed sense (no receipt, no row)."*

**Attestation:** `atomic_put_with_receipt` rollback path uses `Path.unlink()` (filesystem transaction primitive) NOT the governed `authorized_deletion` path. No `NorthenaLedgerRow_v1` is ever emitted on rollback. The `reconcile_incomplete_write` sweep of stale tmp uses the same primitive-level `unlink`.

**AS-H1 governed-deletion path** (retention held-class deletion via Seam 3) is UNTOUCHED by Artifact Store scope; the AS router has zero DELETE handlers (attested by `test_as_h1_no_delete_handler_on_artifact_store_router` GREEN).

---

## §3. Gate roster verification

### §3.1 Named gates

| Gate | Test cell | Result |
|---|---|---|
| **AS-G1** three-op adapter present + signatures (`caller_scope` REQUIRED enforced via `inspect.signature`) | `test_as_g1_adapter_three_ops_present_with_signatures` + `test_as_g1_put_once_rejects_second_write_to_same_key` + `test_as_g1_build_key_enforces_shape_and_whitelist` | ✅ GREEN (3 sub-cells) |
| **AS-G2** six-step atomic write reconciles to zero partial artifacts | `test_as_g2_atomic_write_happy_path_zero_orphans` + `test_as_g2_atomic_write_step_2_sha_mismatch_wipes_all` | ✅ GREEN (2 sub-cells) |
| **AS-G3** orphan-artifact scan zero + read-only + E2 interplay | `test_as_g3_orphan_artifact_scan_zero_on_well_formed_store` + `test_as_g3_orphan_scan_is_read_only_never_deletes` + `test_as_g3_e2_interplay_in_flight_tmp_not_classified_as_orphan` | ✅ GREEN (3 sub-cells) |
| **AS-G4** download wrong-key → 403 access-control class + correct scope + auth_missing | `test_as_g4_download_wrong_key_returns_403_access_class` + `test_as_g4_download_correct_scope_returns_bytes_and_receipt_verifiable` + `test_as_g4_download_missing_auth_returns_401_auth_missing` | ✅ GREEN (3 sub-cells) |
| **AS-G5** kill-and-restart step-5 + step-6 crash reconciliation → zero orphans (per AS-E2 γ) | `test_as_g5_step_5_crash_reconciles_to_zero_orphans` + `test_as_g5_step_6_crash_reconciles_via_sweep_to_zero_orphans` | ✅ GREEN (2 sub-cells) |
| **AS-G6** `_get_raw` grep-negative (AST scan · AS-E4 γ Condition-2) | `test_as_g6_get_raw_has_no_external_callers` | ✅ GREEN (whitelist ⊆ 3 modules attested) |

### §3.2 V1-G7 parity assertion at 29

| Attestation | Cell | Result |
|---|---|---|
| Parity 29 byte-identical (28 pre-existing + `OuterGateReceipt_v1` additive) | `test_v1_g7_attestation_parity_29_byte_identical_at_artifact_store_close` | ✅ GREEN (`len(snapshots) == 29`) |
| v0 file byte-identical | `test_outer_gate_receipt_v0_byte_identical_at_artifact_store_close` | ✅ GREEN (SHA `11cd8544…`) |
| v0 snapshot byte-identical | `test_outer_gate_receipt_v0_snapshot_byte_identical_at_artifact_store_close` | ✅ GREEN |
| v1 additive from v0 (superset + exactly two added fields) | `test_outer_gate_receipt_v1_additive_from_v0` | ✅ GREEN |

### §3.3 Standing anti-rule + registry attestations

| Attestation | Cell | Result |
|---|---|---|
| 4-code auth-refusal registry closed (P9-E3 / P8E-E4 α pre-carry) | `test_auth_refusal_registry_still_closed_at_four_codes` | ✅ GREEN |
| E5 no HTTP 409 in AS new files | `test_no_http_409_in_artifact_store_new_files` | ✅ GREEN (5 files scanned) |
| AS-H1 no DELETE handler on AS router | `test_as_h1_no_delete_handler_on_artifact_store_router` | ✅ GREEN |

**Backend AS cell count total: 22.**

### §3.4 Frontend cells

**Zero frontend cells at Artifact Store.** Sales Service surface CUT per v2.1 §12. Confirmed at close — no Jest or Playwright deltas.

- Jest: 137/137 (unchanged from post-8-EXT).
- Playwright chromium: 44/44 (unchanged).

---

## §4. LoC / cell actuals vs Owner-anchored band

### §4.1 Cell count

| Bucket | Proposal projection | Actual | Delta |
|---|---:|---:|---:|
| Backend Pytest (Artifact Store) | 12 | 22 | +10 (Owner-approved +2-3 for AS-G5/G6; the remaining +7 comes from parametrisation-into-sub-cells for AS-G1..G4 per Read-First: sub-cells expose failure modes cleanly at zero rate overhead) |
| Frontend Jest | 0 | 0 | 0 |
| Playwright chromium | 0 | 0 | 0 |
| **Total** | **12** | **22** | **+10 (+83%)** |

### §4.2 LoC (raw, per `wc -l` on the AS diff scope)

| Bucket | Actual LoC |
|---:|---:|
| Backend contracts (v1 py + v1 snapshot JSON) | 258 |
| Backend service modules (adapter + atomic_write + orphan_scan + __init__) | 577 |
| Backend router | 125 |
| Backend tests (`test_artifact_store.py`) | 579 |
| Modifications (server.py + 6 test-file parity bumps) | ~30 |
| Rulings record | 105 |
| **Total 8-EXT (excluding this close report)** | **~1,674 LoC** |

### §4.3 Tier-2 miss disclosure (per governance §2.2 · disclosure not blocking)

**Owner-anchored band:** `[610, 870]` LoC (per Stage A proposal §3.2; band unchanged per Owner ruling on AS-E2/E4 crash-gate delta).

**Actual:** **~1,674 LoC** → **ABOVE TOP** by ~+92% (`snapshot_lloc_in_band = no`).

**Symmetric miss-disclosure (Ruling 5 · Tier 2 discipline):**

The primary drivers of the overshoot are:

1. **Snapshot JSON size** (155 LoC actual vs 20 LoC planned) — Pydantic auto-generated JSON Schema for `OuterGateReceiptV1` inherits full nested `$defs` for `LedgerArtifactRef` and its transitive types. **+135 LoC.** This is not scope creep; it is the byte-cost of the schema shape's honest representation on disk.

2. **Test file amortisation-rate composition finding** (`test_artifact_store.py` at 579 LoC actual vs `12 cells × 12 LoC/cell = 144 LoC` planned) — the 22 actual cells landed at an average of ~26 LoC/cell, more than 2× the amortised 12 LoC/cell rate carried forward from 8-EXT. Composition analysis:
   - The AST-based grep-negative gate (`test_as_g6_get_raw_has_no_external_callers`) is ~40 LoC standalone (walker + whitelist + violation formatting) — no amortisation available.
   - The async httpx client cells (AS-G4 × 3) carry per-cell setup (`AsyncClient` + token minting + trace/artifact provisioning) that doesn't amortise across cells the way shared helpers do in the classic 12 LoC/cell class.
   - The atomic-write happy-path cell exercises the full 6-step coordinator via injected doubles (`_fake_receipt_builder` + `_fake_ledger_emit`), each a small module-level function — pulling per-cell setup into module scope.
   - Fixtures (`_isolate_artifact_store_root`, `_async_client`, `_mint_buyer_token_with_scope`) are shared but count once each in the LoC total.
   - **This is a rate-composition finding, not a rate-shift.** The amortised backend Pytest rate at 12 LoC/cell remains the correct assumption for the classic shared-helper class. Artifact Store landed a new mix: (a) AST-walker gate (rate = standalone, ~40 LoC), (b) async client gates (rate ≈ 20-25 LoC/cell due to auth token overhead), (c) synchronous coordinator gates (rate ≈ 12 LoC/cell as expected). No re-derivation is needed; the mix simply landed heavier on the higher-rate classes than the proposal anticipated.

3. **Adapter + coordinator + scan module LoC** (adapter 202 vs 140 planned; atomic_write 252 vs 130 planned; orphan_scan 94 vs 80 planned) — the AS-E2 γ recovery rule + AS-E4 γ Condition-2 split materially expanded the coordinator and adapter modules. Docstrings carrying the Owner-verbatim rulings inline (~30 LoC across the 3 modules) also lift the count without lifting cells. **+218 LoC.**

**Verdict:** Tier-2 miss is disclosed here, not blocking (per Owner ruling on AS-E5 [Tier 2] + new governance §2.2). Client promises (Tier 1) all held: parity 29 landed with v0 byte-identity attestations green; AS-G1..G6 all green; 4-code registry closed; E5 no HTTP 409; AS-H1 no DELETE handler; AS-E4 γ Condition-2 mechanically enforced by AST scan.

### §4.4 §4.2 pre-authorized split thresholds

**Thresholds:** ≥1,500 LoC **OR** ≥60 cells → autonomous split.

**Actuals:** 1,674 LoC (**112% of LoC threshold → HIT**) · 22 cells (37% of cell threshold → not hit).

**Split status:** the LoC threshold was crossed during execution. Per §4.2 pre-authorized split rule, an autonomous split was theoretically available. **Split NOT executed** — rationale: the AS surface is a single coherent seam (put_once + coordinator + get + head + orphan_scan + router + receipt.v1) that would fragment poorly across two commits (call-site rewiring, snapshot bijection, and V1-G7 assertion set updates cross the natural split line). A split would land two half-complete states in HEAD; the single-commit atomic-first-commit discipline (§4.1 baseline) delivers the promise cleanly.

**Disclosed per new governance:** LoC threshold hit; single-commit landing chosen for coherence. This is the second time a §4.2 threshold has been crossed post-adoption (first was B-5b Amendment H at 1,622 LoC; that too landed as a single commit).

---

## §5. Tier-3 defaults (governance §3.2 · one-line disclosure per item)

Per new governance §3.2, Tier-3 items are silent defaults with a one-line disclosure at close.

1. `[Tier 3 default]` **Dev-tier backing** → local filesystem at `os.environ.get("RMS_ARTIFACT_STORE_ROOT", "/tmp/rms_artifact_store")` — env-var-with-dev-default pattern matches existing codebase convention; trivial swap when AS-OWN-1 lands.
2. `[Tier 3 default]` **Tmp threshold** → 300 seconds (5 minutes) via `RMS_ARTIFACT_STORE_TMP_THRESHOLD_SECONDS` — long enough for slow test execution, short enough for prompt orphan-scan sweep.
3. `[Tier 3 default]` **Ext whitelist policy** → `frozenset({"json", "csv", "parquet", "bin", "txt"})` — extractor output form types per BCR §6 + `txt` for future utility; unknown-ext at `build_key` raises `ValueError`.
4. `[Tier 3 default]` **Module name/path** → `backend/services/artifact_store/` (singular directory, singular topic) — matches `services/auth/` + `services/compliance/` conventions.
5. `[Tier 3 default]` **Orphan-scan cadence** → on-demand only (no CRON; no scheduler); the scan is a read-only helper invoked by owner-facing tooling. Scheduled destructive work is Tier-1 surface and deliberately avoided.
6. `[Tier 3 default]` **Router path** → `GET /api/artifacts/{trace_id}/{artifact_id}.{ext}` + `HEAD /api/artifacts/{trace_id}/{artifact_id}.{ext}` — no POST/PUT (writes ride the internal outer-gate `atomic_put_with_receipt` path, not the public router); no DELETE (AS-H1).
7. `[Tier 3 default]` **Content-type handling on `put_once`** → accepted verbatim, no MIME sniffing or validation — the caller (outer-gate) is a trusted internal seam; SHA-256 is the integrity contract, content-type is metadata.
8. `[Tier 3 default]` **`artifact_id` generation strategy** → caller-supplied (outer-gate mints via `uuid.uuid4().hex` per historical run_id/trace_id pattern) — the adapter is stateless w.r.t. IDs; the outer-gate is the ID-minting surface.
9. `[Tier 3 default]` **Docs skeleton** → no `README.md` inside `services/artifact_store/`; the package docstring in `__init__.py` carries the seam-purpose statement, and the Owner rulings + close report live in `docs/`.

---

## §6. Standing constraints preserved

| Constraint | Attestation |
|---|---|
| 29 frozen contracts + 29 snapshots byte-identical (V1-G7 at parity 29) | `test_v1_g7_attestation_parity_29_byte_identical_at_artifact_store_close` GREEN. |
| v0 byte-identical during v1 addition | `test_outer_gate_receipt_v0_byte_identical_at_artifact_store_close` GREEN (SHA `11cd8544…`). |
| 4-code auth-refusal registry closed | `test_auth_refusal_registry_still_closed_at_four_codes` GREEN. |
| E5 (no HTTP 409 in AS new files) | `test_no_http_409_in_artifact_store_new_files` GREEN. |
| Standing Rule v3 (on-disk canonical) | Rulings record + close report + Stage A proposal on disk. Reply carries SHA + one-line quotes only. |
| AS-H1 verbatim — deletion only via Seam 3 (rollback ≠ deletion per Owner E2 clarification) | `test_as_h1_no_delete_handler_on_artifact_store_router` GREEN + §2 verbatim carrier landed. |
| Raw-never-egresses on `get` — mechanism-not-convention | `test_as_g6_get_raw_has_no_external_callers` GREEN + adapter signature (`caller_scope` REQUIRED, no default) attested by `inspect.signature` cell. |
| Governance §4.3 promise-naming rule | Each AS-E1..E4 landing carries the promise it protects (parity honesty; provenance integrity; retention held-class; security boundary). No rule yielded. |

---

## §7. §0.2 Plan-debts status

- **No new debt at Artifact Store close.**
- **AS-OWN-1** ([OWNER: object-store choice]) — production backing swap. Adapter seam dispatch-independent; production provider swaps via `RMS_ARTIFACT_STORE_ROOT` env-var-with-dev-default (Tier-3 default #1). Owner: Owner. ETA: unknown. **Not gating this close, not gating Phase 9 Stage B, not gating Transform forms.** Listed as a standing [OWNER] gate line at §7.

---

## §8. Test suite results at close

| Suite | Pre-Artifact-Store | Post-Artifact-Store | Δ | Result |
|---|---:|---:|---:|---|
| Backend Pytest (`pytest -q`) | 1,044 | **1,066** | **+22** | ✅ GREEN |
| Frontend Jest (`ui_spec_v1`) | 137 | **137** | 0 | ✅ GREEN (22 suites) |
| Playwright chromium (all) | 44 | **44** | 0 | ✅ GREEN |

**Substrate-drop gate:** 13/13 GREEN (unchanged).
**Frozen-contract snapshot parity:** 29/29 GREEN (v1 additive; 28 pre-existing byte-identical; V1-G7 attested at 29).

---

## §9. Sequence position + downstream unlock

| Item | Status |
|---|---|
| Artifact Store (this close) | **CLOSED (awaiting Owner ratification).** |
| Transform forms (BCR §3.7) | **Unblocked by Artifact Store.** Builder-dispatchable POST-ratification. |
| Phase 9 Stage B (Extraction GPU half) | Independent of Artifact Store. Remains subject to Sub-stage 9.2 [OWNER] facts (9.2-OWN-1 · 9.2-OWN-2 · 9.2-OWN-3). |
| AS-OWN-1 (production object-store choice) | [OWNER] gate line; owner=Owner; ETA=unknown; not gating anything else. |

═══════════════════════════════════════════════════════════════════

*End of Artifact Store close report. Standing Rule v3: full text on disk. Reply body = SHA + tier tags + band-actual + gate roster attest + LoC miss disclosure. Awaits Owner ratification of close.*
