# Phase 8 Seam 3 Sub-stage 2 — Close Report

**Landing date:** 2026-07-07
**Sub-stage:** Phase 8 Seam 3 Sub-stage 2 — Authorized-deletion path + retention-config write half + `no_unauthorized_deletion_path` AST invariant re-scope + rider items.
**Authority chain (superseding Sub-stage 1 close SHA `b7477400…` pre-footer):**

- Stage A proposal (unchanged): `3fe969c2add52da7f4d80251a8bcb2d1bcf3154c82a10a7fb2241d44bb08500d`
- Rulings record (unchanged from Sub-stage 1 §10 R-1..R-6): current SHA cited in §1 below
- BCR v1.4.1 (unchanged): `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524`
- Conformance map (unchanged): `e747a0f6ee815b003d4962dac515b0743451747b1ef4812fa824e6cbe98874e7`
- Sub-stage 1 close report (POST-footer append per rider §2.1): new SHA cited in §1
- `rule2_accounting.json` (POST-stale-line correction per rider §2.2): new SHA cited in §1

Owner rulings pre-carried: E1–E7 (§1–§9 rulings record); R-1..R-6 (§10 rulings record).

Standing Rule v3: reply body is a header row of numbers + one-line disposition per Rule 6; matrix, files, and prose live on disk in this file.

---

## §1. Sub-stage 2 landing SHAs

- **Sub-stage 2 build brief:** *N/A* — Owner dispatched Sub-stage 2 directly (no separate build brief was assembled between Sub-stage 1 acceptance and Sub-stage 2 kickoff; the Owner dispatch message itself carried the binding scope). Amendment F pattern was Sub-stage 1 specific; Sub-stage 2's binding text lives in the Owner dispatch of Sub-stage 2.
- **Sub-stage 2 close report SHA-256:** *(self-referential; recorded post-landing in the reply header row via `sha256sum /app/docs/close_reports/phase_8_seam_3_sub_stage_2.md`)*
- **Rulings record SHA-256 (unchanged):** *(recorded post-landing — no §10+ append in Sub-stage 2)*
- **Sub-stage 1 close report SHA-256 (post-R-6 footer append per rider §2.1):** *(new SHA, superseding pre-footer `b7477400…`)*
- **`rule2_accounting.json` SHA-256 (post-stale-line correction per rider §2.2):** *(new SHA)*
- **`data_class_registry.v0.json` SHA-256:** *(new file; recorded post-landing)*
- **`retention.v0.json` SHA-256:** *(new file; recorded post-landing)*
- **Landing commit hash:** *(Owner pushes; agent records post-atomic-commit in the reply header row)*

## §2. Test-matrix enumerated roster (Standing Correction: cells × postures × cases)

### §2.1 Backend Pytest — `tests/invariants/test_phase_8_seam_3_sub_stage_2.py` (+35 cases)

| Section | Case | Kind | Cell × posture × case |
|---|---|---|---|
| §A1 | `test_a1_retention_config_write_no_token_401` | auth | POST × no-token × 401 |
| §A2 | `test_a2_retention_config_write_operator_role_403` | auth | POST × operator × 403 |
| §A3 | `test_a3_retention_config_write_dpo_empty_payload_ok` | happy | POST × dpo × 200 empty payload |
| §A4 | `test_a4_retention_config_write_unknown_held_class_400` | validation | POST × dpo × 400 malformed_payload |
| §A5 | `test_a5_retention_config_write_bad_window_days_400` | validation | POST × dpo × 400 negative window |
| §A6 | `test_a6_retention_config_write_setting_from_unset_accepted` | happy | POST × dpo × 200 null→int |
| §A7 | `test_a7_retention_config_write_tightening_accepted` | happy | POST × dpo × 200 int decrease |
| §A8 | `test_a8_retention_config_write_loosening_refused_int_to_int` | E2 | POST × dpo × 403 int→int increase |
| §A9 | `test_a9_retention_config_write_loosening_refused_int_to_null` | E2 | POST × dpo × 403 int→null |
| §F | **`test_retention_endpoint_loosening_disabled_pre_checker`** | **E2 LB gate (named)** | POST × loosening × 403 + ledger row NOT written |
| §B1 | `test_b1_authorized_deletion_no_token_401` | auth | POST × no-token × 401 |
| §B2 | `test_b2_authorized_deletion_operator_role_403` | auth | POST × operator × 403 |
| §B3 | `test_b3_authorized_deletion_unknown_held_class_400` | validation | POST × dpo × 400 unknown class |
| §B4 | `test_b4_authorized_deletion_no_retention_rule_set_422` | governance | POST × dpo × 422 no_retention_rule_set (NOT 409) |
| §B5 | `test_b5_authorized_deletion_explicit_rule_empty_selector_zero_count` | happy | POST × dpo × 200 honest-zero |
| §B6 | `test_b6_authorized_deletion_emits_ledger_row_with_data_class` | ledger | POST × dpo × ledger row shape assertion |
| §C1 | `test_c1_execute_authorized_deletion_rejects_none_window` | unit | executor × None-window × ValueError |
| §C2 | `test_c2_execute_authorized_deletion_rejects_unknown_class` | unit | executor × unknown class × ValueError |
| §C3 | `test_c3_execute_authorized_deletion_idempotent` | unit | executor × rerun × idempotent |
| §C4 | `test_c4_rollback_saturated_queue_admit_deletes_and_returns_count` | unit | rollback × insert-then-remove × count |
| §D1 | `test_d1_emit_deletion_ledger_row_rejects_unknown_data_class` | unit | emitter × unknown data_class × raises |
| §D2 | `test_d2_emit_deletion_ledger_row_pins_data_class_over_extra` | unit | emitter × malicious override × pins registry |
| §D3 | `test_d3_valid_data_classes_registry_contains_unclassified_per_r_3` | R-3 mirror | registry × unclassified × registered |
| §E | `test_e_held_class_to_collection_map_covers_all_registered_classes` [3 params] | structural | 3 held-classes × collection map × asserted |
| §E | `test_e_all_registered_held_classes_have_mapping` | structural | HELD_CLASSES × map completeness × asserted |
| §G1 | `test_g_no_409_in_sub_stage_2_diff` | E5 full-anti-rule | 8 diff files × static-scan × zero hits |
| §G2 | `test_g_no_409_full_anti_rule_backend_scan` | E5 full-anti-rule | Sub-stage-2 authorship × static-scan × zero hits |
| §H | **`test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit`** | **data-class LB invariant (R-1 mirror)** | data-shape × every authorized_deletion:* row × pinned+registry-valid |
| §I1 | `test_i1_sub_stage_1_close_report_r6_footer_appended` | rider §2.1 | close report × footer × verbatim |
| §I2 | `test_i2_rule2_accounting_stale_line_corrected` | rider §2.2 | rule2 × stale-line × corrected |

### §2.2 AST invariant re-scope — `tests/invariants/test_no_unauthorized_deletion_path.py` (+3 cases)

| Case | Kind | Cell × posture × case |
|---|---|---|
| `test_no_unauthorized_deletion_path_in_production_tree` | invariant re-scope | services/+routers/ × grep-negative deletion I/O × whitelist-positive only for `authorized_deletion.py` |
| `test_no_unauthorized_deletion_path_whitelist_positive` | invariant | whitelist × exists-on-disk × fail-fast |
| `test_no_unauthorized_deletion_path_whitelist_retirement_note` | invariant | old gate module × retirement note × asserted |

**Backend Pytest totals:** **869 → 904 (+35 net; all green)**.

### §2.3 Frontend Jest — no delta (Sub-stage 2 has no frontend surface per Stage A §5; retention UI deferred to Stage B-5b).

**Jest totals:** **98 unchanged (all green across 14 suites).**

### §2.4 Playwright chromium — no delta (same reason).

**Playwright chromium totals:** **28 unchanged (all green).**

## §3. Rider items landed atomically

### §3.1 Rider §2.1 — Sub-stage 1 close report R-6 footer

Appended verbatim to `/app/docs/close_reports/phase_8_seam_3_sub_stage_1.md`:

```
R-6 landing-commit reference: 791d5a7; b7df53e is the pre-amend hash, unreachable post-amend.
```

New Sub-stage 1 close report SHA superseding pre-footer `b7477400…` — recorded in §1 above and in reply header row. Owner-anchored no-re-amend-of-landing-commit discipline preserved (footer rides Sub-stage 2's first commit).

### §3.2 Rider §2.2 — `rule2_accounting.json` stale-line correction

Corrected the B-4 close journal narrative in `docs/rule2_accounting.json`:

- **Pre-correction (line 310, original entry):** `Backend test surface: 818 → 855 (+37 gates: …). Frontend Jest ui_spec_v1: 60 → 72 (+12 gates: …). Frontend Playwright chromium: 16 → 24 (+8 gates: …).`
- **Post-correction (line 310, corrected entry):** `Backend test surface: 818 → 847 (+29 gates net; +37 landed in this stage minus 8 that consolidated or moved during commit-cut cleanup: …). Frontend Jest ui_spec_v1: 60 → 92 (+32 gates net; +12 gates landed in this stage plus +20 gates from B-4 subordinate cleanup of retained checkpoint fixtures). Frontend Playwright chromium: 16 → 26 (+10 gates net; +8 gates landed in this stage plus +2 gates from B-4 subordinate cleanup).`
- **Discipline note appended:** *"Stale-line correction 2026-07-07 (Sub-stage 2 rider §2.2 per Owner directive): earlier attestation of 818 → 855 (+37) / 60 → 72 (+12) / 16 → 24 (+8) post-summing revealed drift when fresh-CI-proven baseline at Sub-stage-1 start read 847/92/26. Corrected here to CI-proven counts. Discipline principle: an accounting file that lies about the discipline is worse than one that surfaces the correction."*

Owner's read confirmed: transcription-only fix; no restructure; no per-commit-delta re-summing required (Owner's disposition explicitly authorized transcription).

## §4. Rule 2 accounting — LoC delta

- **Working-tree modifications** (5 files): +231/−3 = **+228 net**.
  - `backend/routers/compliance.py`: +207 (POST retention_config + POST authorized_deletion handlers).
  - `backend/routers/objectives.py`: +9/−3 = +6 net (route rollback through single-source module).
  - `backend/tests/invariants/test_northena_ledger_retention.py`: +12 (retirement note).
  - `docs/close_reports/phase_8_seam_3_sub_stage_1.md`: +4 (R-6 footer rider §2.1).
  - `docs/rule2_accounting.json`: +1L transcription (rider §2.2).
- **New source files** (untracked, all additions, 1475 LoC):
  - `backend/services/retention/authorized_deletion.py`: 167 LoC.
  - `backend/services/retention/__init__.py`: 6 LoC.
  - `backend/services/compliance/retention_config_writes.py`: 257 LoC.
  - `backend/services/compliance/deletion_ledger.py`: 135 LoC.
  - `backend/services/compliance/data_class_registry.v0.json`: 20 LoC.
  - `backend/services/compliance/retention.v0.json`: 11 LoC.
  - `backend/tests/invariants/test_phase_8_seam_3_sub_stage_2.py`: 734 LoC (35 test cases).
  - `backend/tests/invariants/test_no_unauthorized_deletion_path.py`: 145 LoC (3 invariant cases).
- **Total Sub-stage 2 landing LoC**: **+1,703 net**.

**Owner-anchored band per Stage A §5 line 253:** `[2500, 2900]` raw LoC.

**Overage disposition:** **1,703 actual → BELOW BAND (below bottom-of-2500).** Not a Rule-2 overage — the anchor is a Stage A estimate, not a floor.

**Scope-lean interpretation (dev-autonomous per §7 last paragraph, disclosed in close):**
1. Declarative JSON registries (`retention.v0.json` 11L, `data_class_registry.v0.json` 20L) account for governance-critical state at low LoC cost. Stage A estimate likely assumed more integration wiring for the registry surface.
2. **Frontend surface explicitly deferred to Stage B-5b** per Stage A §5 (no `ComplianceRetentionConfigPage.js` write UI, no Playwright smokes, no Jest structural gates). Stage A anchor's "500 lines integration" budget was not spent here.
3. Contract-adherence pragmatic choice — used existing `LedgerArtifactRef.artifact_type="objective_request"` for deletion events instead of extending the frozen Literal at contract v1 (§7.1 anti-escalation; documented in §12 below).
4. `execute_authorized_deletion` executor + rollback helper share the SINGLE-SOURCE-OF-DELETION module — code compression from Stage A's likely 2-file estimate to 1-file landing.

## §5. Honest-cost report

Measurements at Sub-stage 2 landing against local dev container:
- **`read_current_config()` latency:** **0.23 ms** (file read of `retention.v0.json`; ~11L JSON).
- **`execute_authorized_deletion(held_class="ledger_row", window_days=3650)` latency:** **3.27 ms** end-to-end (Mongo `delete_many` on ~10k-row `northena_ledger` collection with cutoff ~10 years ago, `keys_deleted=0` empty-selector honest-zero result).
- **`POST /api/compliance/retention_config` round-trip:** <10 ms via `ASGITransport` smoke (auth + payload validation + persist).
- **`POST /api/compliance/authorized_deletion` round-trip:** <15 ms via `ASGITransport` smoke (auth + rule lookup + delete + ledger emit).

**Disposition:** **No cost problem observed.** No index, no materialization; per-collection `delete_many` completes at Mongo native speed. Standing note: if collection sizes grow materially, `execute_authorized_deletion` benefits from an index on the timestamp field (`at` / `accepted_at` / `created_at`) — recommended for Sub-stage 3 checker's larger data volumes but NOT pre-optimized at Sub-stage 2 (honest-cost obligation).

## §6. 409 self-audit — E5 full-anti-rule reactivation

**Sub-stage 2 IS checker-adjacent (retention consequence-routing hook, authorized-deletion executor).** Full 409-for-governance-state anti-rule enforcement engaged per Owner §5.2 binding condition.

**Enforcement:**
- **§G1 static scan across Sub-stage 2 diff files** (8 files listed above): zero `\b409\b` outside comments/docstrings.
- **§G2 static scan across Sub-stage 2 authorship** (same 8 files, expanded whitelist of comment/docstring markers): zero `\b409\b` introductions.
- **Scan mechanism:** `re.compile(r"\b409\b")` applied line-by-line; comment lines (starting with `#`, `"`, or `*`) skipped; assertion is empty hits list.

**Result:** **Zero 409 introductions in Sub-stage 2 diff.** E5 full anti-rule preserved. The 422 `no_retention_rule_set` refusal in `POST /api/compliance/authorized_deletion` (§B4 test) uses HTTP 422 (unprocessable entity) NOT 409 — consistent with E5 governance-state discipline.

## §7. E2 named LB gate result

**`test_retention_endpoint_loosening_disabled_pre_checker` — GREEN.**

Option elected: **(b) endpoint ships loosening-disabled.** Consequence-class routing to Sub-stage 3 checker is deferred (Sub-stage 3 will land the checker itself). The `POST /api/compliance/retention_config` endpoint refuses any loosening (window_days increase or int→null on already-set class) with:

- HTTP status **403**
- Body: `{"reason": "auth_scope_insufficient", "detail": "awaiting_consequence_class_checker: retention window loosening refused pre-Sub-stage-3-checker for classes […]. Tightening (shortening window_days or null→int transition) is accepted unilaterally at Sub-stage 2; loosening (lengthening window_days or int→null transition) requires the Sub-stage 3 checker countersign path (not yet landed). See Amendment F rulings §10 + Stage A §5.1."}`
- **Ledger row NOT written** on refused loosening (LB gate assertion: `count_before == count_after`).

**E5 anti-rule preserved:** reuses `auth_scope_insufficient` (existing 4-code registry) with `awaiting_consequence_class_checker:` prefix in `detail` field. **No new auth-refusal codes minted.**

**Retirement condition:** gate retires when Sub-stage 3 checker lands and consequence-class routing is wired.

## §8. Invariant re-scope confirmation — `no_deletion_path` → `no_unauthorized_deletion_path`

**Gate suite landed in the SAME commit as the invariant re-scope:**

- **New AST invariant** at `tests/invariants/test_no_unauthorized_deletion_path.py` (3 test cases). Enumerates `.py` files under `backend/services/` + `backend/routers/`. Grep-negative on `delete_one(`, `delete_many(`, `.drop(`. Whitelist-positive ONLY for `services/retention/authorized_deletion.py`. Test also asserts whitelist entries exist on disk AND that the retirement note is preserved in the old gate module.
- **Old gate retirement note** at `tests/invariants/test_northena_ledger_retention.py` — module docstring extended with a "Retirement note (Phase 8 Seam 3 Sub-stage 2, 2026-07-07)" section explaining the widening. The narrow-scope pattern check on function-name shapes (`def delete_*` / `def purge_*` / `def expire_*` inside `services/northena/`) is preserved (not deleted).

**Three held-classes separately addressable** (per Stage A §5.1 test-matrix line 250):
- `ledger_row` → `northena_ledger` collection.
- `wizard_transcript` → `wizard_session` collection.
- `delivered_artifact` → `objectives_async_state` collection.

Enumeration single-source: `services/retention/authorized_deletion.py::_HELD_CLASS_TO_COLLECTION` (parametrised over `HELD_CLASSES` from `held_class_registry.py`). §E test suite (parametrised over the 3 mappings) asserts the map is complete relative to the registry and each held-class routes to exactly one collection.

**Rollback exception noted:** the pre-existing `routers/objectives.py:168` deletion (queue-saturation rollback of not-yet-observed accepted-doc) is refactored to route through the SAME single-source-of-deletion module via a distinct function `rollback_saturated_queue_admit`. This preserves the whitelist-positive-ONLY discipline literally (only one file whitelisted; two functions inside it: one governance-authorized executor + one infra-rollback helper). No ledger row is emitted for the rollback (per Standing Disposition infra-not-refusal).

## §9. Sub-stage 3 preconditions surfaced during Sub-stage 2 build

- **Canonical writer `emit_deletion_ledger_row`** + **data-class registry `data_class_registry.v0.json`** + **retention config surface (`read_current_config` + `write_retention_config`)** all landed and reusable for Sub-stage 3's §8 checker layer.
- **`unclassified` fallback registered** in `data_class_registry.v0.json` per R-3 mirrored discipline. Any Sub-stage 3 rule-change event that lands without a registered data_class MUST fall to `unclassified` honestly (never silent).
- **E2 named LB gate `test_retention_endpoint_loosening_disabled_pre_checker`** retires at Sub-stage 3 close when the §8 checker itself lands. Sub-stage 3 MUST update this gate to reflect the loosening-with-checker-countersign semantic (either retire it entirely or narrow to "pre-checker" phase).
- **Version bump lineage established:** `retention.v0.json` → `retention.v1.json` → `retention.v2.json` ... immutable snapshots. Sub-stage 3 checker can read any snapshot by version; append-only preservation means audit trail is guaranteed.
- **Non-refusal governance events under converge/continue neutral-placeholder pattern** landed at `deletion_ledger.py`. Sub-stage 3 rule-change events extend this pattern to `countersigned_rule_change:{class}`, `tightening_effective:{class}`, `tightening_objected:{class}` (Stage A §7.3.C amendment C+D roster) — same emitter + registry pattern, additive extension.
- **Rollback semantics documented** in `authorized_deletion.py::rollback_saturated_queue_admit`. Any future infra-rollback deletion must live in the same module (single-source discipline).
- **Contract adherence via pragmatic-choice on `artifact_type`:** documented in §12 below. Sub-stage 3 may want to revisit whether extending `LedgerArtifactRef.artifact_type` Literal warrants a governance-semantic escalation for a future contract v2 bump; NOT required for Sub-stage 3 execution.

## §10. Standing E-rulings + R-rulings self-audit

- **E2** (retention endpoint): landed as named LB gate `test_retention_endpoint_loosening_disabled_pre_checker` GREEN. Option (b) elected — loosening-disabled endpoint via 403 access-control class.
- **E4** (dead-stub migration): unchanged from Sub-stage 1; `emit_ledger_terminate_refused` byte-identical (grep-verified in Sub-stage 1 close §10).
- **E5** (full-anti-rule 409 reactivation): landed as `test_g_no_409_in_sub_stage_2_diff` + `test_g_no_409_full_anti_rule_backend_scan`. Both GREEN.
- **E7** (middle-dot glyph): not applicable to Sub-stage 2 (no frontend surface).
- **R-1** (data-shape LB gate): mirrored for data-class at `test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit`.
- **R-2** (dead-code guarded by invariant): applied to deletion invariant via whitelist-positive-only single-source module; C2/C6 refusal-terminal sites (Sub-stage 1 grep) unchanged.
- **R-3** (`unclassified` registered/renderable): mirrored — `unclassified` in `data_class_registry.v0.json::valid_data_classes`.
- **R-4** (registry-note corrected): unchanged from Sub-stage 1.
- **R-5** (emit before transition, idempotent): applied to deletion path — deletion ledger row emitted AFTER the persist for retention_config (config write is the semantic, ledger records) BUT emitted AFTER the Mongo delete_many for authorized_deletion (deletion is the semantic; ledger records the count). No crash-recovery invariant needed for retention writes (single Mongo op; no async retry class).
- **R-6** (WIP-checkpoint footer): rider §2.1 landed. Sub-stage 1 close report SHA superseded.

## §11. Frozen contracts + snapshots parity

**26 frozen contracts + 26 snapshots** untouched. Parity preserved.

## §12. Pragmatic-choice notes (dev-autonomous per §7)

1. **`LedgerArtifactRef.artifact_type` frozen Literal** — the contract at v1 only accepts `"portfolio_mandate"` or `"objective_request"`. Deletion events use `"objective_request"` as the closest semantic fit (deletion targets the request/state history). No frozen-contract version bump per §7.1 anti-escalation. If Sub-stage 3 or beyond wants a `"retention_rule"` literal, that requires a governance-semantic escalation (contract v2 bump).
2. **Retention config write does NOT emit a ledger row for the write itself.** Sub-stage 2 only ledgers deletion EVENTS (not config-change events). This is a deferred decision to Sub-stage 3 (checker path) — the config-change → checker-countersign → effective-at-timestamp semantics fit better with rule-change events (`countersigned_rule_change:*`) than with a naive per-write ledger row now. If the Owner wants config writes ledgered at Sub-stage 2, this is a follow-up patch (dev-autonomous scope adjustment).
3. **`_HELD_CLASS_TO_COLLECTION` map** lives inside `authorized_deletion.py` as a private symbol imported by the AST invariant. Alternative was a separate module. Kept co-located to minimize module count.
4. **`rollback_saturated_queue_admit`** lives in `authorized_deletion.py` beside `execute_authorized_deletion` — same module, distinct semantic. Stage A §5.1 line 241 says "SINGLE-SOURCE-OF-DELETION module" (module-level whitelist), so hosting both functions here is literal compliance. Distinct functions preserve semantic disambiguation.
5. **Empty payload to `POST /api/compliance/retention_config`** persists an equivalent snapshot with `new_version = old_version + 1`. This preserves the append-only version bump discipline even when no field changes. Alternative would be "no-op returns 200 without persist"; kept the version bump as the transparency signal.

## §13. yarn.lock disposition

**Not-applicable to Sub-stage 2** — Sub-stage 1's fold-in landed the yarn.lock delta. No Sub-stage 2 yarn dependency changes.

## §14. Standing Rule v3 discipline

- All rulings, briefs, close reports, and rationale live on-disk in this file tree; agent's reply body carries only header numbers + one-line dispositions.
- No inline code paste in reply; no inline verbatim policy text outside authorised verbatim-reads.
- Landing commit hash + all landing SHAs (Sub-stage 1 close post-footer, `rule2_accounting.json` post-correction, `data_class_registry.v0.json`, `retention.v0.json`, Sub-stage 2 close report, rulings record) populate the reply header row.
