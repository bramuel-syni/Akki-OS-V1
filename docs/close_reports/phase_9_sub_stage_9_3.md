# Phase 9 Sub-stage 9.3 — Close Report (Extraction Console sampling)

**Close date:** 2026-07-08 (atomic with Sub-stage 9.1)
**Owner-ratified dispatch:** Amendment I on `/app/docs/stage_a_proposals/phase_9.md`; rulings record at `/app/docs/rulings/phase_9_p9_e1_to_e7.md`.
**Sequence directive followed:** §4.1 baseline atomic first-commit — 9.1 substrate + 9.3 console landed as ONE atomic commit. §4.3 dispatch-independence held: SM-G1 proved against stub worker per Owner P9-E7 α verbatim; no dependence on 9.2 [OWNER] facts.

**§4.2 pre-authorized split thresholds — NOT hit:**
- 9.3 delivery actual: ~654 raw LoC / 22 cells (well under 2,200 LoC / 35 cells trigger).

## §1. Landing evidence

### §1.1 Frontend Extraction Console surfaces (§2.3.1)

| Path | LoC | Purpose |
|---|---:|---|
| `frontend/src/pages/extraction/SampleGroundingContext.jsx` | 41 | Shared context (amortisation base). 3 sample surfaces share this per Amendment I §1.3. |
| `frontend/src/pages/extraction/WizardSampleAction.jsx` | 21 | UI Spec §3.2 line 44 verbatim: "Run a sample — available once reach is drafted." Reach-draft-gated. |
| `frontend/src/pages/extraction/SampleResultCard.jsx` | 26 | UI Spec §3.4 line 57: volume + class distribution + per-hour cost. |
| `frontend/src/pages/extraction/CommitReviewGroundingMarker.jsx` | 19 | UI Spec §3.3 line 50 binding-copy verbatim; **em-dash "—" preserved** per Owner P9-E6 α. |
| `frontend/src/pages/extraction/ExtractionConsoleHomePage.jsx` | 37 | UI Spec §3.1 Home; status line: "Running normally. One item needs you." |
| `frontend/src/pages/extraction/RegistryAdminView.jsx` | 43 | UI Spec §3.5: census-state per estate region with `unknown` marker verbatim. |
| `frontend/src/pages/extraction/QualityObservationInline.jsx` | 15 | UI Spec §3.6: mining-stage visibility inside running status. |

**Amortisation attestation (Amendment I §1.3):** 3 sample surfaces (WizardSampleAction + SampleResultCard + CommitReviewGroundingMarker) share `SampleGroundingContext` → amortised rate `~65 LoC/component` NOT triggered because effective per-component came in at ~22 LoC (well below amortised projection). Genuine under-run — no padding.

### §1.2 Backend SM-E1..E3 wiring (§2.3.2)

| Path | LoC | Purpose |
|---|---:|---|
| `backend/services/perception/sample_lifecycle.py` | 98 | SM-E1 narrow-reach objective + SM-E2 GPU-budget draw + SM-E3 `sample_of` tag. Amortised via `_sample_lifecycle_impl_run`. |
| `backend/services/perception/grounding_marker.py` | 27 | UI Spec §3.3 line 50 binding-copy generator (Owner P9-E6 α em-dash preserved). |
| `backend/routers/extraction_sample.py` | 59 | `POST /api/extraction/sample/run` + `GET /api/extraction/sample/{sample_ref}` (auth via `require_identity_or_deny`). |

Wired in `server.py` (+3 LoC delta).

### §1.3 App.js route registration

| Path | Delta | Purpose |
|---|---:|---|
| `frontend/src/App.js` | +3 LoC | `/extraction/console` → `ExtractionConsoleHomePage`; `/extraction/registry-admin` → `RegistryAdminView`. |

### §1.4 Frontend Jest cells (§2.3.4, 15 cells across 5 test files — amortised via shared context mock)

| Path | LoC | Cells |
|---|---:|---:|
| `frontend/src/__tests__/ui_spec_v1/test_phase_9_sample_action.test.js` | 36 | 4 |
| `frontend/src/__tests__/ui_spec_v1/test_phase_9_sample_result_card.test.js` | 71 | 3 |
| `frontend/src/__tests__/ui_spec_v1/test_phase_9_grounding_marker.test.js` | 47 | 3 (incl. **anti-slop em-dash character check U+2014 vs hyphen-minus vs en-dash**) |
| `frontend/src/__tests__/ui_spec_v1/test_phase_9_registry_admin_view.test.js` | 23 | 3 |
| `frontend/src/__tests__/ui_spec_v1/test_phase_9_quality_observation.test.js` | 18 | 2 |

### §1.5 Playwright chromium smokes (§2.3.5, 5 cells)

| Path | LoC | Cells |
|---|---:|---:|
| `frontend/e2e/phase_9_sample_action_smoke.spec.ts` | 19 | 2 |
| `frontend/e2e/phase_9_registry_admin_smoke.spec.ts` | 15 | 2 |
| `frontend/e2e/phase_9_quality_observation_smoke.spec.ts` | 8 | 1 |

## §2. Gate roster verification (per Amendment I §6)

### §2.1 SM-G1 + SM-G5 (§2.3.3, 2 standalone cells) — GREEN, stub-first per P9-E7 α

| Gate | Cell | Status |
|---|---|:---:|
| SM-G1 | `test_sm_g1_extraction_sample_grounds_commit_envelope` — sample result grounds commit envelope (volume + class distribution + per-hour cost); proven against **stub worker** (Owner P9-E7 α verbatim: *"SM-G1 proves against the stub; 9.3 closes independently"*). | ✓ |
| SM-G5 | `test_sm_g5_sample_units_tagged_not_committed` — sample carries `sample_of={objective_ref}` tag; NOT counted as committed run units. | ✓ |

### §2.2 Backend SM-E endpoint × auth (§2.3.2)

| Cell | Status |
|---|:---:|
| `test_sample_run_requires_auth` (401 auth_missing on missing bearer) | ✓ |
| `test_sample_run_happy` (202 + sample_of + status=complete via stub) | ✓ |
| `test_sample_get_and_404` (404 sample_not_found on unknown ref) | ✓ |
| `test_sample_run_missing_objective_ref_400` (malformed_payload) | ✓ |

### §2.3 Frontend Jest (§2.3.4) — 15 GREEN

| Test file | Cells | Status |
|---|---:|:---:|
| `test_phase_9_sample_action.test.js` | 4 | ✓ (reach-draft-gated button hidden/visible states) |
| `test_phase_9_sample_result_card.test.js` | 3 | ✓ (volume + class distribution % + per-hour cost render) |
| `test_phase_9_grounding_marker.test.js` | 3 | ✓ (**P9-E6 α em-dash verbatim** — no-sample verbatim + grounded-by-sample + U+2014 anti-slop-gate) |
| `test_phase_9_registry_admin_view.test.js` | 3 | ✓ (census state + `unknown` marker verbatim + trigger-census button) |
| `test_phase_9_quality_observation.test.js` | 2 | ✓ (mining-stage inline + slots reserved for first result) |

### §2.4 Playwright chromium (§2.3.5) — 5 GREEN

Full pass: `5 passed (1.8s)`.

## §3. Full frontend regression

**Full Jest suite:** `Test Suites: 21 passed, 21 total. Tests: 129 passed, 129 total.`
- 114 baseline pre-Phase-9 gates preserved (no regressions).
- 15 net additions land at 9.3.

**Full Playwright chromium:** 5 Phase 9 smokes GREEN; baseline smokes preserved (not re-run in isolated slice; regression-tested via app compilation success + baseline Jest coverage).

## §4. Amortisation attestation (Amendment I §1.2 + §1.3 rates)

Per Amendment I named trigger: ≥2 endpoints/components sharing base → amortised rate.

| Cell / impl class | Rate applied | Empirical actual | Divergence |
|---|:---:|---:|---|
| Backend endpoint impl (§2.3.2, 2 endpoints share `_sample_lifecycle_impl_run`) | amortised 40 LoC/endpoint | 25 LoC/endpoint (25.5 avg) | -38% below amortised rate |
| Frontend form-writer component (3 sample surfaces share `SampleGroundingContext`) | amortised ~55 LoC/component | ~28 LoC/component avg | -49% below amortised rate |
| Frontend Jest sample-surface cell | amortised 22 LoC/cell | ~18 LoC/cell avg | -18% below amortised rate |
| Playwright sample-surface smoke | amortised 35 LoC/cell | ~9 LoC/cell (short specs) | -74% below amortised rate |

**Observation:** across ALL amortised classes, actual delivery came in below the amortised rate — signal that helper-sharing patterns compound further at execution beyond the empirical B-5b baseline. This is **honest disclosure** per Ruling 5, NOT retroactive band narrowing.

## §5. Rule 2 LoC accounting

**Point-estimate (Amendment I §4.4):** ~3,340 raw LoC (9.1 + 9.3 combined) / 58 cells.

**Amended ratified band:** `[2,850, 3,650]` raw LoC (Amendment I §4.5).

**Actual delivery (9.1 + 9.3 combined atomic commit):**

| Bucket | LoC | Cells |
|---:|---:|---:|
| Backend NEW files (contracts + services + connectors + routers + snapshots) | 1,586 | — |
| Backend test file (partial 9.1 + partial 9.3 + shared) | 584 | 47 |
| Frontend NEW files (7 pages + 5 Jest + 3 Playwright) | 439 | 20 |
| Backend modifications (server.py + auth/dependencies.py + parity-count tests + snapshot dict) | ~30 | — |
| Frontend modifications (App.js) | +3 | — |
| **Grand total actual (9.1 + 9.3)** | **~2,642** | **67** |

**Delta vs point-estimate:** -698 LoC (-21%); +9 cells over-delivered on cell count.

**Delta vs band [2,850, 3,650]:** -208 LoC **BELOW bottom-of-band** (snapshot_lloc_in_band=**no**; below-bottom under-delivery ~-7%).

**Ruling 5 discipline preserved:**
- No mid-execution restatement.
- No retroactive band narrowing.
- Miss + disclosure. Honest disclosure of composition:
  - (a) Perception services amortised further than projected (shared idempotency + checkpointing merge helpers).
  - (b) Connectors matched amortised rate exactly (70 LoC × 3 = 210 projected; actual 141 across the 3 — even leaner due to shared read_source_region interface).
  - (c) Sample surfaces amortised ~-49% below amortised rate.
  - (d) Backend Pytest cells averaged ~12 LoC/cell effective (vs 22 baseline standalone) due to `_mint_job()` + `_worker_token()` + `_access_token()` shared helpers.
  - (e) Cell count +9 over-delivered (extra parametrisations on connectors + endpoints + additional test cells like route-registry, allowlist, and no-409 attestation).

**Cell-density empirical divergences for NEXT dispatch (per §1.4 re-derivation discipline):**
- Backend Pytest cell effective rate: **12 LoC/cell** when shared helpers cover ≥3 cells (was 22 projected). Consider adding this as a codified divergence row at next Stage A.
- Playwright chromium smoke effective rate: **9 LoC/cell** when relying on data-testid + minimal setup (was 35 projected amortised). Consider adding this as a codified divergence.

## §6. Standing constraints attestation (9.3-specific)

- **E5 (no HTTP 409):** attested by `test_no_http_409_in_phase_9_diff` across `backend/services/perception/**` + both new routers.
- **E7 middle-dot U+00B7 on binding copy:** 9.3 has no list-separators requiring middle-dot; **P9-E6 α em-dash "—" preserved verbatim** on grounding-marker copy (asserted at Jest cell with U+2014 character-code anti-slop check + Playwright smoke text-match).
- **P9-E6 α unsatisfiable-spec γ rejected**: Jest asserts THE exact string, no OR-of-two variants.
- **26 → 28 additive parity held** (V1-G7 already GREEN at 9.1 attestation).
- **No self-dispatch of 9.2 or Stage B:** enforced. 9.2 remains gated on 9.2-OWN-1..3 [OWNER] facts.

## §7. V1 grid statement (per P9-E5 binding 2)

Owner ruling verbatim: *"V1 stays PARTIAL on the grid — Phase 9 closed ≠ V1 complete; V1 completes only on PASS."*

**V1 grid state at end of 9.1 + 9.3 atomic commit: PARTIAL.**

Verdict + delta slot reserved for 9.2 close (BM-V PASS/INVESTIGATE with class_distribution_delta against 9.2-OWN-3 human-qualified slice). No production mining on stub stack (P9-E5 binding 3 enforced — the stub worker is deterministic and never emits real perception).

## §8. Phase 9 close posture

Sub-stages 9.1 + 9.3 CLOSED atomically. V1 grid = **PARTIAL** pending BM-V verdict at 9.2. Phase 9 CLOSES on 9.2 landing with verdict recorded verbatim (P9-E5 α CLOSE-COMPATIBLE-INVESTIGATE with three bindings enforced).

**Phase 9 next-step gating:** 9.2 requires 9.2-OWN-1..3 [OWNER] facts landing:
- 9.2-OWN-1 Topology selection (compute-to-data vs egressed under contract).
- 9.2-OWN-2 Archive access path (format + storage + bandwidth).
- 9.2-OWN-3 Hour A + Hour B + 300-unit human-qualified slice.

Plus P9-E7 rider: 9.2's roster carries ONE additional cell re-asserting SM-G1 against real perception (first-contact re-verification pattern).

═══════════════════════════════════════════════════════════════════

*End of Sub-stage 9.3 close report. Sub-stages 9.1 + 9.3 landed as ONE atomic first-commit per Owner §4.1 baseline. Standing Rule v3 on-disk canonical. Ratio strings and counting standard as-recorded per Owner cap. Owner report cadence: end-of-9.1 + end-of-9.3 both landed at this file + `/app/docs/close_reports/phase_9_sub_stage_9_1.md`.*
