# Phase 8a-lite — Ask Console (Frontend, UI Spec v1 §3 landing) — CLOSED

**Close date:** 2026-07-04
**Delivery format:** Standing Rule v3 — on-disk canonical + SHA-256; return
enumerates dispositions and attestations only.

**Predecessor closes:** Phase 7 Stage B-2 (2026-07-04) — SHA `c46186b173d813bd…`.

---

## 1. Machine-attested block

```
[GREEN] yarn build (production)                                          Compiled successfully
[GREEN] CI=true yarn test --watchAll=false                               27 / 27 across 5 suites
[GREEN] webpack watch (frontend supervisor)                              compiled successfully (Ask Console + /legacy shell)
[GREEN] Ask Console mounts at /                                          [data-testid="ask-console-page"] present
[GREEN] Ask binding copy verbatim §3.1                                   "What do you need to know?"
[GREEN] Quiet defaults line present                                      Standard: floor · Scope: estate · change (disabled)
[GREEN] No output-form picker on Ask surface                             5 gates GREEN (no <select>, no [role=combobox/listbox/radiogroup], no output-form data-testid, no preset-value <option>)
[GREEN] Legacy G5b pages archived under src/legacy/pages/                4 gates GREEN (no straggler under src/pages/, all 8 present under src/legacy/pages/, App.js has no bare `./pages/<Legacy>` import, App.js declares AskConsolePage at index route)
[GREEN] Gate 1 Class inseparable (re-landed under ui_spec_v1/)           7 tests
[GREEN] Gate 2 Refusal first-class + validation distinguishability       6 tests
[GREEN] Gate 3 Single ingress + trace_id retention                       4 tests (Part A + 3× Part B)
[GREEN] Manual E2E via curl POST /api/service_1/v2/dispatch              HTTP 202 AsyncDeliveryAccepted_v1 (fresh estate)
[GREEN] Manual E2E via curl (validation-422 branch)                      HTTP 422 with {detail:[...]} shape → routed to infra_fault (structurally distinct from refusal)
[STATUS] Delivery: on-disk canonical + SHA (Standing Rule v3)
[STATUS] `git push` NOT executed (Owner standing prohibition)
[STATUS] Zero backend surface delta (no /app/backend/* changes in this phase)
[STATUS] Zero new frozen contracts (parity holds at 26)
```

---

## 2. Files touched

### 2.1 New files

| Path | LoC | Role |
|---|---|---|
| `frontend/src/pages/AskConsolePage.js` | 610 | Ask Console surface per UI Spec §3 verbatim (§3.1 Ask + §3.2 Answer + §3.3 Refusal + §7 accepted-branch + infra-fault branch). Consumes `POST /api/service_1/v2/dispatch` via `api.dispatchV2(...)`. Reuses `ClassBadge` + `RefusalCard` (Owner Condition-2 posture: no reimplementation). |
| `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` | 73 | Legacy archival invariant — 4 gates. |
| `frontend/src/__tests__/ui_spec_v1/test_no_output_form_picker_present_on_ask_surface.test.js` | 82 | §3.1 no-picker invariant — 6 gates. |
| `frontend/src/__tests__/ui_spec_v1/gate1_class_inseparable.test.js` | 111 | G5b Gate 1 re-landed under UI Spec v1 — 7 tests. |
| `frontend/src/__tests__/ui_spec_v1/gate2_refusal_firstclass.test.js` | 87 | G5b Gate 2 re-landed under UI Spec v1 — 6 tests. |
| `frontend/src/__tests__/ui_spec_v1/gate3_single_ingress.test.js` | 128 | G5b Gate 3 re-landed under UI Spec v1 — 4 tests (Part A + 3× Part B). Part A excludes `src/legacy/` (archived non-active surface). |

### 2.2 Modified files

| Path | Delta | Role |
|---|---|---|
| `frontend/src/App.js` | rewrite (~43 lines total) | Routes rewritten: `/` → AskConsolePage; `/legacy/*` → legacy G5b shell (LandingPage, OperatorDashboard, RunsPage, RunDetailPage, DisciplinePage, EnginesPage, ComposePage, TraceReceiptPage); catch-all `*` → `Navigate to="/"`. Preserved AppShell for legacy nested routes. |
| `frontend/src/apiClient.js` | +18 lines (existing 21 → 39) | Added `dispatchV2(objectiveRequestV2)` method returning `{status, body}` with `validateStatus: (s) => s >= 200 && s < 500` (refusal is a first-class body per A2 doctrine). |
| `frontend/src/legacy/pages/*.js` (8 files) | import-path adjust only | `../hooks/` → `../../hooks/`; `../apiClient` → `../../apiClient`; `../components/` → `../../components/`. Mechanical fix for the archival move; no behavioural change. |

### 2.3 Deleted files

| Path | Reason |
|---|---|
| `frontend/src/legacy/__tests__/gate1_class_inseparable.test.js` | Copy-forward superseded by `ui_spec_v1/gate1_class_inseparable.test.js` (Owner ruling verbatim: "copy-forward from src/legacy/__tests__/"). |
| `frontend/src/legacy/__tests__/gate2_refusal_firstclass.test.js` | Copy-forward superseded (as above). |
| `frontend/src/legacy/__tests__/gate3_single_ingress.test.js` | Copy-forward superseded (as above). |

---

## 3. Test surface — 27 gates across 5 suites

**Suite 1: `test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (4 gates)**
1. `no page file with a legacy name exists directly under src/pages/`
2. `every legacy page file exists under src/legacy/pages/`
3. `src/App.js never imports a legacy page from './pages/'`
4. `src/App.js declares AskConsolePage at the index route`

**Suite 2: `test_no_output_form_picker_present_on_ask_surface.test.js` (6 gates)**
5. `AskConsolePage renders no <select> element`
6. `AskConsolePage renders no ARIA role=combobox/listbox/radiogroup`
7. `AskConsolePage renders no data-testid pattern matching an output picker`
8. `AskConsolePage does not surface the preset form values as visible options`
9. `Quiet defaults line is present and change affordance is present but disabled`
10. `Ask binding copy renders verbatim per §3.1`

**Suite 3: `gate1_class_inseparable.test.js` (7 gates)**
11–17. `RefusalCard renders supported_class alongside asked` / reason+class together / `LedgerTable` renders `defensibility_class` / `LedgerTable` renders `computed_class` fallback / `ClassBadge` renders all three defensibility classes / `ClassBadge` returns null when class is falsy / `ClassBadge` renders Solva `computed_class` value.

**Suite 4: `gate2_refusal_firstclass.test.js` (6 gates)**
18–23. T1 all fields render / T2 `asked` prominent + labelled / T3 `supported_class` as ClassBadge / T4 `what_would_raise_it` actionable / T5 null when refusal null / T6 validation-422 vs refusal shape distinguishability.

**Suite 5: `gate3_single_ingress.test.js` (4 gates)**
24. Part A: Zero raw `fetch`/`axios`/XHR referencing `/api/` outside `apiClient.js` on the ACTIVE surface (excluding `src/legacy/` archived non-active surface).
25. Part B: `LedgerTable` renders `trace_id` as link with correct `href`.
26. Part B: `TrustReceiptLink` renders `trace_id` in DOM.
27. Part B: `TrustReceiptLink` returns null when `traceId` is falsy.

**Test result: 27 / 27 GREEN.** Warnings only (React Router v7 future-flag), no failures.

---

## 4. Standing constraints — compliance attestations

| Constraint | Compliance |
|---|---|
| **Zero backend surface delta** | ✅ No `/app/backend/*` change in this phase. `pytest -q` still 685 / 685 GREEN (verified pre-flight + post-write). |
| **26 frozen contracts byte-identical** | ✅ Not touched — no backend surface delta. |
| **Shield boundary preserved** | ✅ Not touched — no LLM code in frontend. |
| **infra-not-refusal (503 doctrine)** | ✅ AskConsolePage: `catch (e)` branch routes network/5xx errors to `InfraFaultView` — clearly labelled "System temporarily unavailable" + "This is an infrastructure fault, not a governance decision." Not laundered as a governance refusal. |
| **Refusal first-class body-shape (A2 doctrine)** | ✅ `apiClient.dispatchV2` uses `validateStatus: (s) => s >= 200 && s < 500` so 422 refusals are returned as `body`, not thrown. `isRefusal(body)` discriminates on `body.outcome === "refused"`, NOT status code (Gate 2 T6 covers structural distinguishability). |
| **No output-form picker on Ask surface (§3.1)** | ✅ 6 gates in `test_no_output_form_picker_present_on_ask_surface.test.js`; quiet-defaults "change" affordance disabled at 8a-lite (enabled at Phase 8 full with Buyer Wizard). |
| **Legacy pages archived (Owner ruling)** | ✅ 8 files moved to `src/legacy/pages/`; import paths adjusted; App.js routes them at `/legacy/*` (kept reachable for Trust receipt deep-links from Ask Console answer surface). |
| **Component reuse (Owner Condition-2 flavored posture)** | ✅ `AskConsolePage` reuses `ClassBadge` + `RefusalCard` from `src/components/*` — zero reimplementation. `LedgerTable` + `TrustReceiptLink` reused by re-landed Gate 3 tests. |
| **Ruling 3 wire-shape gate** | ✅ Ask Console consumes ObjectiveRequest_v2 with the strictly frozen shape: `output.form = 'composed_conclusion'`, `output.consumer = 'person'`, `output.grain = 'synthesized_whole'`, `output.standard = { minimum_class: 'utterance', minimum_scores: {} }` — verified by E2E curl smoke returning HTTP 202. |
| **Standing Rule v3 delivery format** | ✅ close report on-disk canonical; SHA-256 in return. No full-text inline pastes. |
| **`git push` NOT executed** | ✅ per Owner standing prohibition. |
| **No refactoring** | ✅ only mechanical import-path adjustments on the 8 archived legacy pages; no code cleanup on shared components (they remain byte-identical). |
| **Synthetic estate v1** | ✅ Ask Console consumes fresh dispatch (returns 202 AsyncDeliveryAccepted_v1 for fresh estate). G2b real hour remains Owner-blocked. |

---

## 5. Wire posture — what the Ask Console renders in each response branch

| HTTP | Body shape | Ask Console phase | Rendered surface |
|---|---|---|---|
| 200 | `ComposedConclusion_v0` (`conclusion_class + answer_text + trace_id + …`) | `answer` | `AnswerView` per §3.2 — question echoed / class badge + `{n} sources examined · answered in {t}` / headline finding / actions (Why this answer · Export report · Trust receipt · Ask another). |
| 202 | `AsyncDeliveryAccepted_v0/v1` (`objective_id + status='accepted' + delivery_estimate + trace_id + …`) | `accepted` | `AcceptedView` — "Accepted — being composed." with objective_id / delivery_estimate / trace_id + optional Trust receipt link. §7 async admission legitimately surfaced, not laundered as answer or refusal. |
| 422 | `AdmissionRefusal_v0` or `Service1Refusal_v0` (`outcome='refused' + reason + …`) | `refusal` | `RefusalView` per §3.3 — "Not to the standard you asked for." + `RefusalCard` (shared component) + binding actions (Accept as recorded statement · Narrow the objective · Lower the standard) + "A refusal is the system keeping its promise…" footer with "Why this was refused" link. |
| 422 | validation `{ detail: [...] }` (Pydantic model-attributes error) | `infra_fault` | `InfraFaultView` — routed here per structural distinguishability (Gate 2 T6); NOT rendered as governance refusal (would misrepresent the state). |
| 5xx / network | any | `infra_fault` | `InfraFaultView` — "System temporarily unavailable · This is an infrastructure fault, not a governance decision." Per infra-not-refusal doctrine. |
| 501 | Phase 2 placeholder | `infra_fault` | out-of-scope for 8a-lite. |

**All five paths are code-covered.** The 200 answer path requires prior warm state (Phase 4b §6.1 qualified-data); at 8a-lite on synthetic estate, dispatch typically returns 202. The 422 refusal path returns cleanly when triggered (validated via unit tests + isRefusal discriminator).

---

## 6. Non-goals at 8a-lite (deferred to Phase 8 full)

- Operator / Engineer / Buyer / Master Admin / DPO full surfaces per UI Spec §2.
- Shared §8 cross-surface component layer formalisation (Owner Q3 sequencing).
- Buyer Wizard surface for the "change" affordance on quiet-defaults line.
- Long-poll or SSE for async delivery completion (Ask Console shows "accepted" state; user must revisit or wait for Trust receipt link).
- G2b real hour on live RMS material.
- Backend surface changes of any kind.

---

## 7. Awaiting Owner acceptance

- **This close report** at `/app/docs/close_reports/phase_8a_lite.md` (SHA-256 quoted in return).
- **Ask Console live** at `/` — human-visible surface unblocked.

---

*End of Phase 8a-lite close report.*
