# Artifact Store · Owner Rulings AS-E1 through AS-E4 (2026-07-08)

**Dispatch context:** Owner rulings message post-Stage-A relay of the 4 Tier-1 escalations (governance §4.4). Rulings arrived in a single Owner message with the execute directive baked in ("pre-flight → atomic first-commit → close").

**Governance model in effect:** `docs/governance/tiered_ruling_model.md`. Tier-1 escalations receive verbatim treatment. AS-E5 (Tier 2) + Tier-3 defaults are disclosure-only at close.

**Standing Rule v3:** verbatim rulings on-disk. Reply body carries SHA + one-line quotes only.

---

## AS-E1 — `OuterGateReceipt_v1` parity-adjacency (28 → 29)

**Ruling:** α — additive new frozen contract.

**Owner verbatim:** *"α. OuterGateReceipt_v1 lands as a new frozen contract by addition; v0 stays byte-identical; parity 29 at close, V1-G7 assertion set bumps with it. Promise basis: buyer-independent verification — β routes the buyer's proof through our API being up and truthful; on-receipt means the receipt alone suffices. Additive-new-version is the settled pattern; 29 is the honest count."*

**Landing:**
- New `backend/contracts/outer_gate_receipt_v1.py` (class `OuterGateReceiptV1`).
- New `backend/tests/invariants/outer_gate_receipt_v1.contract_snapshot.json`.
- v0 file + snapshot BYTE-IDENTICAL (SHA-256 attested at close report §1.3).
- V1-G7 assertion set BUMPED to 29 (all prior tests updated: `test_phase_7_stage_b_2_wizard.py`, `test_phase_7_stage_b_3_wizard.py`, `test_phase_9_sub_stage_9_1_and_9_3.py`, `test_composed_conclusion_v0_contract_frozen.py`, `test_8_ext.py`).
- `test_artifact_store.py::test_v1_g7_attestation_parity_29_byte_identical_at_artifact_store_close` GREEN.

---

## AS-E2 — Atomic-write step-5 crash posture (with recovery rule)

**Ruling:** γ + explicit recovery rule.

**Owner verbatim:** *"γ, with the recovery rule explicit. Copy-not-move at step 3, dual-copy retention through step 6, GC tmp only after the ledger row lands. The tmp object is the in-flight transaction marker. Recovery rule: any tmp past threshold → if receipt + ledger row complete, GC tmp; else delete the final-key object and GC tmp (transaction abort). Clarification so AS-H1 isn't tripped: rollback of an incomplete write is transaction mechanics, not data deletion — the artifact never existed in the governed sense (no receipt, no row). Gate: kill-and-restart cell proving a step-5 crash and a step-6 crash both reconcile to zero orphans."*

**Landing:**
- `backend/services/artifact_store/atomic_write.py::atomic_put_with_receipt(...)` — six-step protocol.
- Step 3 uses `shutil.copy2(tmp, final)` (COPY-not-move).
- Step 6 emits ledger row THEN `tmp.unlink()` (GC only on success).
- `reconcile_incomplete_write(...)` — recovery-rule implementation. For each tmp past threshold (env `RMS_ARTIFACT_STORE_TMP_THRESHOLD_SECONDS`, dev default 300s):
  - If `receipt_exists(key) AND ledger_row_exists(key)` → GC tmp (successful-write cleanup).
  - Else → delete final-key object AND GC tmp (transaction abort, `os.unlink()` = filesystem primitive, NOT AS-H1 authorized_deletion).
- AS-G5 gate landed as two cells (step-5 crash + step-6 crash), both proving zero orphans post-reconcile.

**AS-H1 non-trip attested at close report §2 verbatim carrier.**

---

## AS-E3 — Orphan-scan disposition on detection

**Ruling:** α — REPORT-ONLY.

**Owner verbatim:** *"α. Report-only. The scan is read-only; disposition of a real orphan is an owner-facing decision via the Seam 3 path, per AS-H1 verbatim. One interplay line with E2: the scan distinguishes in-flight writes (live tmp marker under threshold) from orphans — a transaction in progress is not a defect."*

**Landing:**
- `backend/services/artifact_store/orphan_scan.py::scan_orphans(...)` — enumerates final-key candidates + partitions into `orphans`, `in_flight`, `scanned`.
- E2 interplay: a companion tmp file under threshold classifies the candidate as `in_flight`, EXCLUDED from `orphans`.
- No destructive action. Owner disposition via Seam 3 authorized-deletion path only.
- AS-G3 GREEN — `test_as_g3_orphan_artifact_scan_zero_on_well_formed_store` + `test_as_g3_orphan_scan_is_read_only_never_deletes` + `test_as_g3_e2_interplay_in_flight_tmp_not_classified_as_orphan`.

---

## AS-E4 — Raw-never-egresses on `get` — authz boundary location

**Ruling:** γ + Condition-2 grep-negative gate.

**Owner verbatim:** *"γ, not α. Material basis: α's caller_scope=None default is convention wearing mechanism clothing — every caller can pass None and the adapter obliges. Internal callers legitimately need raw reads (step-4 head-verify, orphan scan); the split makes that honest. Conditions that make γ mechanical: (1) public get(key, caller_scope) — scope required, no default, denies before bytes; (2) grep-negative gate: _get_raw has zero callers outside the adapter module + write-protocol + scan internals (Condition-2 pattern). Raw-never-egresses enforced by structure, proven by gate."*

**Landing:**
- `backend/services/artifact_store/adapter.py::_get_raw(key)` — PRIVATE, module-level underscore prefix, no scope check.
- `backend/services/artifact_store/adapter.py::ArtifactStoreAdapter.get(key, caller_scope)` — PUBLIC, `caller_scope` REQUIRED (no default; enforced by `inspect.signature` cell).
- Domain exceptions `ScopeInsufficientError` + `ArtifactNotFoundError`; the router translates `ScopeInsufficientError` → 403 via `auth_refusal.emit('auth_scope_insufficient', ...)`. 4-code registry closure preserved.
- AS-G6 grep-negative gate: `test_as_g6_get_raw_has_no_external_callers` — AST-walks `backend/**/*.py`, asserts `_get_raw` callers ⊆ whitelist = {`adapter.py`, `atomic_write.py`, `orphan_scan.py`}. Any external caller → fail.

---

## AS-E5 — Adapter surface split threshold (Tier 2, disclosure-only)

**No Owner ruling required per governance §2.2.** Disclosed at close report §3.2.

**Trigger status:** NOT hit (actual ~840 LoC / 22 cells vs threshold 1500 LoC / 60 cells).

---

## Tier-3 defaults (disclosure-only, per governance §3.2)

Enumerated at close report §5.6 (one-line disclosure per item). Not ruled on. Owner may raise Tier-3 items to Tier-2/1 at any subsequent dispatch via named-promise argumentation.

═══════════════════════════════════════════════════════════════════

*End of Artifact Store rulings record. Standing Rule v3: verbatim on-disk. Reply body carries SHA + tier tags only.*
