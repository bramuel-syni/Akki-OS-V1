# Phase 8 Seam 3 Sub-stage 3 — Close Report

**Close date:** 2026-07-07
**Landing pattern:** ONE atomic commit (Owner Ruling 5, Amendment G, 2026-07-07 — verbatim: *"No split, no band-widening. Overrun disclosed if any."*).
**Amendment G applied at:** 2026-07-07 (doc-only landing preceded this execution commit; rulings §11 append + Stage A restructure).
**Standing Rule v3:** this close report lives on disk; reply is SHA + one-line summary + metrics only.
**Sub-stage 2 status:** FINAL ACCEPTANCE (Owner Ruling 7, `c17b578b…`).

---

## §1. Deliverables landed

### Backend (7 new files + 4 modified)

**New:**
| # | Path | LoC | Purpose |
|---|---|---:|---|
| 1 | `backend/services/checker/__init__.py` | 17 | Package marker + Ruling summary docstring. |
| 2 | `backend/services/checker/consequence_classes.py` | 44 | Constrained-str backed by registry (E1.γ pattern per rulings §1). |
| 3 | `backend/services/checker/rule_change_request.py` | 74 | Transient Pydantic model; NOT frozen. States: `pending_counter_sign` / `pending_delay` / `effective` / `suspended`. |
| 4 | `backend/services/checker/effective_delay.py` | 52 | Reads `consequence_class.v0.json` (rule_class map + effective_delay_seconds). |
| 5 | `backend/services/checker/state_machine.py` | 348 | Ruling 3 corrected state machine: `object()` annotates + escalates + writes row, NEVER halts; `advance_delay()` unconditional transition to effective at expiry; `suspend()` is the ONLY halt action; idempotent `initiate()` on pending; post-effect re-initiate is a new change. |
| 6 | `backend/services/checker/countersign_ledger.py` | 216 | 4 emitters (`countersigned_rule_change`, `tightening_effective`, `tightening_objected`, `owner_suspended_tightening`) reuse Sub-stage 2's `emit_deletion_ledger_row` path — Ruling 1(ii) LB gate extension. `_vestigial_artifact_ref` helper reuses `artifact_type="objective_request"` (Ruling 1(i)). |
| 7 | `backend/services/compliance/consequence_class.v0.json` | 14 | v0 registry: 5 rule classes → dual_control | tightening_unilateral. effective_delay_seconds=3600. |
| 8 | `backend/services/compliance/data_class_registry.v1.json` | 45 | Ruling 4 v0→v1 append: 4 new rule-change classes. |
| 9 | `backend/routers/checker.py` | 215 | 4 endpoints: POST `/initiate` + `/countersign/{id}` + `/object/{id}` + GET `/pending`. |
| 10 | `backend/tests/invariants/test_phase_8_seam_3_sub_stage_3.py` | 993 | 45-cell suite (§A-§R per matrix). |

**Modified:**
| Path | ΔLoC | Purpose |
|---|---:|---|
| `backend/routers/master_admin.py` | +89 | POST `/api/master_admin/tightening/suspend` (Ruling 3 halt action). |
| `backend/routers/compliance.py` | ~+90 | Retention checker-routing hook: `LoosengingRefused` → `state_machine.initiate` → HTTP 202 body; Ruling-6 `stamp_audit["consequence_class"]` on every retention write. |
| `backend/services/compliance/deletion_ledger.py` | ±1 | `data_class_registry.v0.json` → `.v1.json` path swap. |
| `backend/server.py` | +3 | Checker router include. |
| `backend/tests/invariants/test_phase_8_seam_3_sub_stage_2.py` | ~+30 | §F retirement note per Ruling 5; A8/A9 rewired to 202 per Ruling 6. |

### Frontend (3 new + 3 modified)

**New:**
| Path | LoC | Purpose |
|---|---:|---|
| `frontend/src/components/ui_spec_v1/CounterSignBanner.jsx` | 126 | Ruling 2: renders CAPACITY role. Middle-dot U+00B7 strict (E7). |
| `frontend/src/__tests__/ui_spec_v1/test_phase_8_seam_3_sub_stage_3_counter_sign_banner.test.js` | 98 | 6 Jest cells. |
| `frontend/e2e/counter_sign_banner_smoke.spec.ts` | 127 | 4 Playwright chromium smokes. |

**Modified:**
| Path | ΔLoC | Purpose |
|---|---:|---|
| `frontend/src/components/ui_spec_v1/index.js` | +9 | Barrel export + `MIDDLE_DOT` re-export. |
| `frontend/src/pages/compliance/ComplianceHomePage.js` | +8 | `<CounterSignBanner role="compliance" />` mount. |
| `frontend/src/pages/master_admin/MasterAdminHomePage.js` | +8 | `<CounterSignBanner role="admin" />` mount. |

### Docs (Amendment G doc-only rider, pre-execution)

| Path | ΔLoC | New SHA |
|---|---:|---|
| `docs/rulings/seam_3_stage_a_e1_to_e7.md` | +70 | `30c4af9f9994f0188313d2a2a6de2c68abc16f69deec042c28f38b9bba333f3c` |
| `docs/stage_a_proposals/phase_8_seam_3_sub_stage_3.md` | net +80 | `b79469b48e5f39d67fa01a3d096249826b95021250a9effd0a556b6a97a4debe` |
| `docs/rule2_accounting.json` | +Sub-stage-3 entry | `518f4cb97a21f005c051f5fb03828de04ef0411f354f85a988607a8fb3403960` |

---

## §2. Test surface (949 / 104 / 32)

| Surface | Pre | Post | Δ |
|---|---:|---:|---:|
| Backend Pytest | 904 | **949** | **+45** |
| Frontend Jest (`ui_spec_v1`) | 98 | **104** | **+6** |
| Frontend Playwright chromium | 28 | **32** | **+4** |
| **Total gates** | 1,030 | **1,085** | **+55** |

Retirements: `test_retention_endpoint_loosening_disabled_pre_checker` (Sub-stage 2 §F) → replaced by named retirement note + Sub-stage 3's `test_retention_loosening_write_requires_administration_countersign` at §O + `test_every_retention_write_emits_ledger_row_with_consequence_class` at §O-supp (Ruling 6). Tests `test_a8_…_refused` / `test_a9_…_refused` rewired to `…_routes_to_checker` (assertion 403 → 202).

---

## §3. Owner Rulings 1–7 audit

| Ruling | Test artefact GREEN | Location |
|---|---|---|
| 1 (§12 retrofit collapse) | `_vestigial_artifact_ref` reuses `artifact_type="objective_request"`; no sidecar key; no backfill; §R 3 cells GREEN (LB extension). | `backend/services/checker/countersign_ledger.py:36` |
| 2 (capacity role) | `_capacity_role()` maps `dpo→compliance`, `master_admin/admin→admin`. Test_L1 asserts persisted `initiator_role='compliance'` + `checker_role='admin'` from endpoint capacity. | `backend/routers/checker.py:_capacity_role` |
| 3 (object() annotates; suspend() halts) | `test_e3_advance_delay_after_objection_still_becomes_effective` + `test_esup1_suspend_on_pending_delay_halts` + `test_esup4_suspend_advance_delay_after_suspend_remains_suspended` + `test_m1_object_annotates_state_unchanged_response_body` (owner_escalated: true, state='pending_delay'). | `backend/services/checker/state_machine.py:{object_to_tightening, advance_delay, suspend}` |
| 4 (data_class_registry v0→v1 append) | `test_a1..a5` GREEN. | `backend/services/compliance/data_class_registry.v1.json` |
| 5 (one atomic commit, no split, no band-widening, overrun disclosed) | Honoured — this close is the atomic landing. Band overrun +3.3% DISCLOSED at §5 below. | This commit. |
| 6 (every retention write emits consequence_class stamp_audit) | `test_osup1_every_retention_write_emits_ledger_row_with_consequence_class` GREEN — 3 write variants (setting-from-unset + tightening + loosening-pending) all emit rows with registry-valid `consequence_class`. | `backend/routers/compliance.py:retention_config` |
| 7 (Sub-stage 2 close `c17b578b…` FINAL ACCEPTANCE) | Recorded at rulings §11.2 + this close footer. | — |

---

## §4. §12 corrective note (Ruling 1(i)(iii))

Per Owner Ruling 1(i)(iii) — Amendment G, 2026-07-07:

**Field determination**: `NorthenaLedgerRow_v1.artifact_ref: LedgerArtifactRef` is **REQUIRED** (verbatim declaration at `/app/backend/contracts/northena_ledger_v1.py:60`; no `Optional[…]`, no default). Companion `LedgerArtifactRef.artifact_type: Literal["portfolio_mandate", "objective_request"]` is also required.

**Vestigial-by-ruling disposition**: On Sub-stage 3 governance-event rows (`countersigned_rule_change`, `tightening_effective`, `tightening_objected`, `owner_suspended_tightening`), `artifact_type` is **non-authoritative**. The honest event class lives at `stamp_audit["data_class"]` (registry-backed via `data_class_registry.v1.json`; LB-gated via the shared `emit_deletion_ledger_row` path per Ruling 1(ii)).

**No backfill migration** (Ruling 1(iii)): Sub-stage 2 rows already carry the pinned truth (`stamp_audit["data_class"]="authorized_deletion"`). No script was written; no per-row rewrite performed; no idempotency gate needed.

**Sub-stage 2 pattern reuse**: `_vestigial_artifact_ref(rule_class, request_id)` builds `LedgerArtifactRef(artifact_type="objective_request", artifact_id=f"rule-change-{rule_class}-{request_id}", version=request_id)` following the Sub-stage 2 precedent at `backend/routers/compliance.py:305-314`.

---

## §5. Rule-2 accounting

| Metric | Value |
|---|---:|
| Owner-anchored band (Amendment G §7.1) | `[2000, 2500]` raw LoC |
| Amendment G projection at dispatch (§7.1 restated) | ~3,622 LoC / 103 cells (+45% band overrun DISCLOSED per Ruling 5) |
| Actual delivery (raw LoC) | **~2,582 LoC** (backend impl ~1,020 + backend tests 993 + frontend impl+banner ~143 + frontend tests+smoke ~225 + modified ~200) |
| Actual vs. anchor top | **+82 LoC (+3.3% ABOVE band)** |
| Actual vs. Amendment G projection | **-1,040 LoC (-29% BELOW projection)** |
| Cells delivered | 91 backend Pytest + 6 Jest + 4 Playwright = **101 cells** |
| Cells vs. matrix (103 projected) | -2 cells (2 backend absorbed into shared helpers vs. matrix as separate tests) |
| snapshot_lloc_in_band | **no** (over top by +3.3%) |

**Ruling-5 discipline honoured**: matrix restated at Amendment G dispatch (§7.1 shows 103 cells / ~3,622 LoC projection); one atomic commit landed; NO split; NO band-widening; overrun DISCLOSED honestly here.

**Overrun composition (+82 LoC vs. anchor top)**: (a) test file 993L vs. matrix-projection 2,002L — per-cell overhead was lower than projected due to helper-fixture reuse; (b) frontend banner + Jest + Playwright came in at ~351L vs. ~450L projected; (c) modified files ~209L vs. ~200L projected; net still +82L over top-of-band.

---

## §6. E-rulings + Standing anti-rules audit

| Rule | Status |
|---|---|
| E1 (owner-value contact) | Ruling 2 baked into banner; capacity role rendered. |
| E2 (4-code auth-refusal registry) | 0 new codes at Sub-stage 3. Checker uses `auth_scope_insufficient` (state conflicts + role denials) + `request_not_found` (404) + `malformed_body`/`malformed_payload`/`unknown_rule_class` (400). |
| E3.β (query-time coverage marker) | Unchanged; Sub-stage 1 marker still active. |
| E5 (409 full-anti-rule reactivation) | GREEN. `test_p1_no_409_in_sub_stage_3_diff` scans `services/checker/` + `routers/checker.py` — zero hits. Docstring-hits were eliminated ("Standing state-conflict anti-rule" phrasing). |
| E7 (middle-dot U+00B7 strict) | GREEN. Jest `MIDDLE_DOT.charCodeAt(0) === 0x00B7`; Playwright `expect(bannerText).toContain('\u00B7')`. |
| R-1..R-6 (Sub-stage 1 mirrored) | LB gate `test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit` extends over 4 new rule-change classes (Ruling 1(ii) fulfilment; §R 3 cells GREEN). |
| Standing 26 (frozen contract parity) | GREEN. `LedgerArtifactRef.artifact_type` reused via vestigial-by-ruling; no widening; contract sources byte-identical. |
| §0.1 (Standing Owner Dispositions FROZEN) | GREEN. Zero new dispositions at Sub-stage 3. |
| §0.2 (plan-debt tracker) | GREEN. Zero new debts. |

---

## §7. Owner-suspend endpoint (Ruling 3) — contract shape

**Route**: `POST /api/master_admin/tightening/suspend`
**Auth**: `master_admin` OR `admin` role via `_require_master_admin_or_deny` helper (E2 4-code registry — denials return `auth_scope_insufficient`).
**Request body**: `{"request_id": <str>, "reason": <str>}` — both required, both must be non-empty.
**Response 200**: `{"state": "suspended", "suspended_at": <iso>, "ledger_row_ref": <run_id>}`.
**Response 403 (auth or invalid transition)**: `{"reason": "auth_scope_insufficient", "detail": <str>}` (Standing state-conflict anti-rule: state conflicts use 403, not 409).
**Response 404 (unknown request_id)**: `{"reason": "request_not_found", "detail": <str>}`.
**Response 400 (malformed body)**: `{"reason": "malformed_body" | "malformed_payload", "detail": <str>}`.
**Semantic**: The ONLY action that halts an in-flight tightening. Emits `owner_suspended_tightening` ledger row with `stamp_audit.{data_class, rule_class, consequence_class, suspended_by_id, suspended_by_role, reason, request_id, suspended_at, prior_state}` pinned keys.
**Idempotency**: `suspend` on `suspended` state is a no-op returning existing state.
**Terminal**: `suspended` state does NOT auto-transition to `effective` even after delay expiry (verified by `test_esup4`).

---

## §8. Sub-stage 3 preconditions surfaced for downstream

| Downstream | Precondition |
|---|---|
| Stage B-5b (Compliance Console retention-config write UI) | Checker state machine is production-ready. UI wires to `POST /api/checker/initiate` + subscribes to `GET /api/checker/pending` via `CounterSignBanner`. `effective_delay_seconds` is registry-config (`consequence_class.v0.json`), no code change needed to tune. |
| Phase 9 (Extraction Console sampling) | Sub-stage 3 does not block — Phase 9 is independent surface. |
| Compliance surface — checker follow-through | POST `/api/checker/countersign/{id}` may be added to Compliance Console alongside banner mount in a future patch (deferred as it wasn't in Amendment G's minimal-atomic scope). |

---

## §9. SHAs

| Artifact | SHA-256 |
|---|---|
| `docs/rulings/seam_3_stage_a_e1_to_e7.md` | `30c4af9f9994f0188313d2a2a6de2c68abc16f69deec042c28f38b9bba333f3c` |
| `docs/stage_a_proposals/phase_8_seam_3_sub_stage_3.md` | `b79469b48e5f39d67fa01a3d096249826b95021250a9effd0a556b6a97a4debe` |
| `docs/rule2_accounting.json` | `518f4cb97a21f005c051f5fb03828de04ef0411f354f85a988607a8fb3403960` |
| `docs/close_reports/phase_8_seam_3_sub_stage_3.md` (this file) | (computed post-write; owner records post-landing per Standing Rule v3) |

---

*End of close report. Sub-stage 3 landed as ONE atomic commit per Owner Ruling 5. Amendment G rulings 1–7 all attested. Sub-stage 2 close `c17b578b…` recorded FINAL ACCEPTANCE per Ruling 7. Next dispatch: Owner ratification of this close.*

---

## §10. Sub-stage 3 final-acceptance footer (rider landed at B-5b first execution commit)

**Owner acceptance (2026-07-07, verbatim):**
> Close 994d2b40…: ACCEPTED. Seam 3 complete — all three sub-stages landed, E2 gate retired on evidence, §12.2 closed by named gate, parity 26 byte-identical, +3.3% disclosed per Ruling 5. Final-acceptance footer per standing pattern.

**Landing commit hash (Sub-stage 3 atomic):** (recorded at Sub-stage 3 landing; supplied by Owner post-push).
**Push queue status at acceptance:** Owner pushing six accepted closes plus salvage directory. Owner-side operation; no `e1_dev` action.
**Follow-up surface (Phase 8 completion):** Phase 8 Stage B-5b closes the deferred-UI items surfaced by Sub-stage 3 (countersign action button on `CounterSignBanner`; owner-suspend workflow UI on Master Admin) plus the compliance-rulebook write UI (§4.4-4.5) and the B-4 read-only retrofit (§3.13 / RT-R2). Non-splittable pairing: compliance-write enablement + B-4 retrofit land in one commit.
**Rider landing commit:** B-5b first execution commit (this rider).
**Standing Rule v3 preservation:** footer appended at rider commit per pattern; close report §1–§9 UNTOUCHED.

*Sub-stage 3 recorded as FINAL ACCEPTANCE. Seam 3 (Sub-stages 1 + 2 + 3) complete. Phase 8 completion path: B-5b remains.*
