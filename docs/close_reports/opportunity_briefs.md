# §3.15 Opportunity Briefs — Close Report

**Close:** 2026-07-10 · atomic execution commit per Owner rulings OB-E1 α + OB-E2 α × 3 seams + OB-E3 α · band `[1,300, 1,900]` RATIFIED.
**Basis:** Stage A `/app/docs/stage_a_proposals/opportunity_briefs.md` · SHA `39061210811943e21a5d1f68da99d356430e0a3bd7d52dc4829ba5fc373d8ab6`.
**Rulings:** `/app/docs/rulings/opportunity_briefs_ob_e1_to_e3.md` · SHA `91532c04cae050ea85e6b25f3d56d0b0db1c611b3c39450529b69fbe53e35bf2`.
**Governance:** 3-tier ruling model · §9 metric-verdict-in-raw-LoC · §12 close-ratification-on-own-text · §12.1 remaining-gates enumeration.
**Standing Rule v3:** on-disk canonical.

---

## §1. Ratification posture (§12 self-ratifying · Owner 2026-07-10)

Per governance §12 (Owner verbatim 2026-07-10): *"A close whose named gates are green and whose rulings are attested as applied ratifies on its own text. Post-close evidence questions are permitted only where a specific Tier-1 gate is alleged defective, with the allegation named. Conditions attach at ruling time, never at close time. No conditional ratifications on meta-evidence."*

Three criteria evaluated at close-landing:

- **(a) Named gates green:** YES — OB-G1..G5 + Seam-1/2/3 sub-gates + auxiliary gates all pass. See §3.
- **(b) Rulings attested as applied:** YES — OB-E1 α + OB-E2 α × 3 seams + OB-E3 α all encoded in source + tests. See §2.
- **(c) No new Tier-1 escalation surfaced during execution:** YES — execution stayed within Stage A escalation matrix (OB-E1..E3). No new Tier-1 surface emerged mid-execution.

**Close ratifies on its own text.**

---

## §2. Rulings applied — attest

### §2.1 OB-E1 α · byte-verbatim structured-anchor grounding

Owner verbatim: *"Structured anchor + byte-verbatim substring check, whole-brief reject on any failure, gate never patches — the AF-E1 β grammar ported intact, including its conditions (mechanical check, no semantic scoring)."*

- Shield-side LLM boundary at `backend/services/synisense/shield/brief_synthesizer.py` emits structured JSON `{brief_text, quantitative_anchors: [{value, registry_read_ref}]}` — hard-schema validated by `_validate_structured_output(...)`.
- Grounding gate at `backend/services/opportunity_briefs/brief_grounding.py::verify_brief_grounding(...)` runs (A) byte-verbatim value check + (B) numeric-coverage check.
- Whole-brief REJECT: any failure → `generator.generate_one_brief(...)` returns `(None, telemetry_with_status='grounding_reject')` · brief NOT written to registry.
- Gate NEVER patches prose (attested at OB-G-Grounding-Fail).
- Mechanical byte-substring only · **no semantic scoring** (attested at OB-G-E3-No-Synth-Compute AST cell).

Attested at:
- `test_ob_g1_brief_numbers_are_registry_reads_verbatim` (green)
- `test_ob_g_grounding_fail_prevents_brief_write` (green)
- `test_ob_g_e3_no_synthesis_compute_ast` (green · §6.10 AST attest)

### §2.2 OB-E2 α × 3 seams · class honesty

Owner verbatim: *"α across all three seams. Write-time attach + render reflection walk (Seam-1), route-level 404 with distinct `brief_id` namespace (Seam-2), grep-negative import boundary on the governed-response path (Seam-3). All three are the established §6.10 mechanism class (AS-G6/TF-G9/FR-G4 lineage) — mechanism enforced by structure, proven by gate, no new precedent minted."*

**Seam-1 · Advisory marker on every render path — α applied:**
- Write-time attach at `backend/services/opportunity_briefs/advisory_marker.py::attach(brief)` invoked by `brief_registry.BriefRegistry.write(...)`. Every registry row carries `_advisory_marker` populated.
- Frontend render-surface reads the marker from the sidecar payload via `frontend/src/pages/opportunity_briefs/OpportunityBriefCard.jsx` and renders under `data-testid="opportunity-brief-advisory-marker"`.
- §6.10 no-strip reflection walk `test_ob_g2_seam1_no_strip_ast` attests no code path deletes/pops/clears `ADVISORY_MARKER_KEY` in the OB package.
- Seam-1 β (contract-embed marker in frozen `OpportunityBrief_v0` field) NOT selected — parity 31 preserved.

**Seam-2 · Brief exclusion from trace/receipt resolution — α applied:**
- `services/opportunity_briefs/__init__.py::BRIEF_ID_PREFIX = "brief_"` — distinct namespace.
- `brief_registry.new_brief_id()` mints IDs in the `brief_` namespace.
- `backend/routers/solva.py::get_trace(trace_id)` explicitly rejects `brief_`-prefixed IDs with HTTP 404 (namespace boundary enforcement).
- Namespace distinctness attest: `test_ob_g3_seam2_namespace_distinct` (green).

**Seam-3 · Brief content excluded from governed response — α applied:**
- §6.10 AST/reflection gate `test_ob_g_seam3_governed_response_import_boundary` walks `backend/services/service_1/**` and rejects any AST `Import`/`ImportFrom` node referencing `opportunity_briefs`.
- `services/opportunity_briefs/README.md` documents the governed-response boundary carrier.
- No `ComposedConclusion_v0.answer_text` synthesis path can consume brief content.

Attested at:
- `test_ob_g2_advisory_marker_present_on_every_brief_render`
- `test_ob_g2_seam1_no_strip_ast`
- `test_ob_g3_brief_excluded_from_trace_resolution` (E2E via ASGITransport)
- `test_ob_g3_seam2_namespace_distinct`
- `test_ob_g_seam3_governed_response_import_boundary`

### §2.3 OB-E3 α · Registry-computable aggregate = Registry-exposed native

Owner verbatim: *"A Registry-computable aggregate is one the Registry read API itself exposes and the brief quotes byte-verbatim; synthesis-time computation forbidden. This is the mandate's own sentence made mechanical — the Registry computes, the brief quotes."*

- Grounding gate treats `registry_read_ref` as opaque; the anchor's `value` MUST appear byte-verbatim in the referenced Registry-read text.
- Synthesis-time computation FORBIDDEN — enforced by §6.10 AST walk over `backend/services/opportunity_briefs/generator.py` + `backend/services/synisense/shield/brief_synthesizer.py`. Any `sum/avg/min/max/count/mean/statistics` Name-call rejected.
- OB-G5 attests a well-formed Combined brief (multi-slice anchors) + a Registry-computable native aggregate ("count_of_units_in_combined(slice_a,slice_b) = 69").

Attested at:
- `test_ob_g5_combined_brief_numbers_trace_to_each_contributing_slice`
- `test_ob_g_e3_no_synthesis_compute_ast`

### §2.4 Band `[1,300, 1,900]` — RATIFIED · verdict below

See §4.

---

## §3. Gate roster (full attestation)

**Backend Pytest cells — all green (16 cells):**

| Gate | Tier | Status | Location |
|---|---|---|---|
| **OB-G1** `test_brief_numbers_are_registry_reads_verbatim` | Tier-1 (OB-R2) | GREEN | `backend/tests/invariants/test_opportunity_briefs_ob_g1_to_g5.py` |
| **OB-G2** `test_advisory_marker_present_on_every_brief_render` | Tier-1 (OB-R3 Seam-1) | GREEN | same |
| **OB-G2 sub** `test_ob_g2_seam1_no_strip_ast` | Tier-1 (§6.10) | GREEN | same |
| **OB-G3** `test_brief_excluded_from_trace_resolution` | Tier-1 (OB-R3 Seam-2) | GREEN | same |
| **OB-G3 sub** `test_ob_g3_seam2_namespace_distinct` | Tier-1 | GREEN | same |
| **OB-G4** `test_shape_as_objective_prefills_reach_only` | Tier-3 (OB-R4) | GREEN | same |
| **OB-G5** `test_combined_brief_numbers_trace_to_each_contributing_slice` | Tier-1 (OB-R6) | GREEN | same |
| **OB-G-Seam3** `test_ob_g_seam3_governed_response_import_boundary` | Tier-1 (§6.10) | GREEN | same |
| **OB-G-DB** `test_brief_prompt_template_data_blind_no_residues` | Tier-1 (§8) | GREEN | same |
| **OB-G-Parity** `test_parity_31_preserved_at_ob_landing` | Tier-1 (frozen contracts) | GREEN | same |
| **OB-G-Refresh** `test_stale_marking_on_census_change` | Tier-3 (OB-R5) | GREEN | same |
| **OB-G-Grounding-Fail** `test_grounding_fail_prevents_brief_write` | Tier-1 (OB-R2 fail path) | GREEN | same |
| **OB-G-E3-No-Synth-Compute** `test_ob_g_e3_no_synthesis_compute_ast` | Tier-1 (OB-E3 · §6.10) | GREEN | same |
| **OB-G-Selector** `test_ob_g_selector_three_scope_enumeration` | Tier-3 | GREEN | same |
| **OB-G-Telemetry** `test_ob_g_telemetry_sidecar_shape` | Tier-3 | GREEN | same |
| **OB-G-Runtime-Transient** `test_ob_g_runtime_transient_never_refusal_envelope` | Tier-1 (AF-E2-precedent-shape) | GREEN | same |

**Frontend Jest cells — all green (8 cells across 4 describes):**

| Cell | Attests |
|---|---|
| `OB-R3 Seam-1 α · advisory marker renders verbatim from sidecar` | Seam-1 render-time surface |
| `OB-R3 Seam-1 α · brief_text renders verbatim` | grounding-render integrity |
| `OB-R6 scope chip · scope=slice → "Slice"` | scope-chip render |
| `OB-R6 scope chip · scope=combined → "Combined"` | scope-chip render |
| `OB-R6 scope chip · scope=estate → "Estate"` | scope-chip render |
| `OB-R5 · stale=true surfaces stale indicator` | stale visibility |
| `OB-R5 · stale=false does NOT surface stale indicator` | stale absence |
| `OB-R4 · button click invokes onShapeAsObjective callback with brief payload` | handoff surface |

Location: `frontend/src/__tests__/ui_spec_v1/test_opportunity_brief_card.test.js`.

**Frontend Playwright chromium smokes — all green (4 cells):**

| Cell | Attests |
|---|---|
| `opportunity briefs page renders three fixture briefs with advisory markers` | UI Spec v2.2 §3.7 + OB-R3 Seam-1 α render-time |
| `scope chips render for slice / combined / estate` | OB-R6 three-scope enumeration render |
| `stale indicator renders on the stale estate fixture brief` | OB-R5 render |
| `shape-as-objective click stashes reach prefill + navigates off briefs page` | OB-R4 handoff wiring |

Location: `frontend/e2e/opportunity_brief_smoke.spec.ts`.

---

## §4. Rule 2 accounting — §9 metric-verdict-in-raw-LoC

### §4.1 Actual raw LoC (from `wc -l`)

| Bucket | LoC |
|---|---:|
| `services/opportunity_briefs/__init__.py` | 8 |
| `services/opportunity_briefs/advisory_marker.py` | 45 |
| `services/opportunity_briefs/brief_grounding.py` | 103 |
| `services/opportunity_briefs/brief_registry.py` | 116 |
| `services/opportunity_briefs/brief_selector.py` | 69 |
| `services/opportunity_briefs/brief_telemetry.py` | 81 |
| `services/opportunity_briefs/generator.py` | 148 |
| `services/opportunity_briefs/shape_as_objective_prefill.py` | 31 |
| **Backend OB package subtotal** | **601** |
| `services/synisense/shield/brief_synthesizer.py` | 164 |
| `services/synisense/shield/brief_prompt.v0.txt` | 36 |
| **Backend Shield subtotal** | **200** |
| `backend/routers/solva.py` (OB Seam-2 patch delta) | ~15 |
| **Backend source subtotal** | **816** |
| `backend/tests/invariants/test_opportunity_briefs_ob_g1_to_g5.py` | 456 |
| **Backend tests subtotal** | **456** |
| `frontend/src/pages/opportunity_briefs/OpportunityBriefCard.jsx` | 73 |
| `frontend/src/pages/opportunity_briefs/OpportunityBriefsPage.jsx` | 110 |
| `frontend/src/App.js` (OB route + import delta) | ~4 |
| **Frontend source subtotal** | **187** |
| `frontend/src/__tests__/ui_spec_v1/test_opportunity_brief_card.test.js` | 100 |
| `frontend/e2e/opportunity_brief_smoke.spec.ts` | 63 |
| **Frontend tests subtotal** | **163** |
| **GRAND TOTAL (code + tests · raw LoC per §9)** | **1,622** |

### §4.2 Band verdict (§9 band-relative trichotomy)

- **Ratified band:** `[1,300, 1,900]` (per rulings §1.4).
- **Actual:** **1,622 raw LoC**.
- **Position in band:** at 54% of range · WITHIN BAND · **`snapshot_raw_in_band=yes`**.
- **Trichotomy verdict:** in-band. No driver disclosure required beyond snapshot line.

### §4.3 §4.2 threshold disclosure (Tier-2 · never blocking per §12.1)

- **Raw LoC threshold (1,500):** **CROSSED** — 1,622 vs 1,500 → +8.1%. Per governance §12.1 (Owner 2026-07-10 verbatim): *"§4.2 thresholds and band disclosures — Tier-2, disclosure-only, never blocking."*
- **Driver rationale:** OB-E1 α whole-brief-reject + OB-E2 α × 3 seams (Seam-1 write-time + render walk · Seam-2 route-level 404 · Seam-3 grep-negative AST walk) + OB-E3 α synthesis-time-compute-forbidden AST walk + OB-R5/R6 auxiliary gates + OB-G-Refresh + OB-G-Grounding-Fail + Shield-boundary brief_synthesizer (200 LoC · §6.9 verbatim carrier on top of AF pattern) + 16 backend Pytest cells + 8 Jest cells + 4 Playwright smokes → dense mandate + dense gate roster + full frontend surface per Stage A §3.3. Comparable magnitude to AF close (1,140 code+tests at Rule-2 miss +20%); OB comes in **WITHIN BAND at +8.1% of §4.2 raw threshold**, honoring the split-fallback threshold without needing to split.
- **Cell count threshold (60):** NOT crossed. 16 backend Pytest + 12 frontend (8 Jest + 4 Playwright) = **28 cells**.
- **Disposition:** atomic single commit per §4.1 baseline · dev's judgment per Owner delegation (governance §2.2 "no round-trip"). Split-fallback NOT triggered.

### §4.4 CI outcomes

- **Pytest:** 1,178 passed + 1 skipped (baseline 1,162 + 1 → **+16 new OB cells**).
- **Jest:** 145/145 (baseline 137/137 → **+8 new OB frontend cells**).
- **Playwright chromium:** 48/48 (baseline 44/44 → **+4 new OB frontend smokes**).
- **Parity:** **31/31 byte-identical** (attested at OB-G-Parity).

---

## §5. §12.1 remaining-gates enumeration (Owner 2026-07-10)

Per governance §12.1 · Tier-1 surfaces named in the mandate covered by execution:

- **OB-R2 grounding integrity** → OB-E1 α · OB-G1 + OB-G-Grounding-Fail (green) · Registry-anchored numerals with mechanical byte-verbatim substring check + whole-brief reject. **Ratified in effect.**
- **OB-R3 class honesty** → OB-E2 α × 3 seams · OB-G2 + OB-G2-Seam1-No-Strip + OB-G3 + OB-G3-Seam2-Namespace + OB-G-Seam3 (green) · advisory marker mandatory-visible + trace-resolution 404 + governed-response import boundary. **Ratified in effect.**
- **OB-R6 grounding clause (Combined)** → OB-E3 α · OB-G5 + OB-G-E3-No-Synth-Compute (green) · Registry-computable aggregate = Registry-exposed native · synthesis-time compute forbidden. **Ratified in effect.**

No remaining Tier-1 gates open. No new Tier-1 escalation mid-execution.

---

## §6. Standing constraints preserved

| Constraint | Attest |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | OB-G-Parity (green) · no contract touched |
| 4-code auth-refusal registry closed | GREEN — briefs not an auth surface |
| No HTTP 409 in OB new/modified files (E5) | GREEN — no 409 boundary in OB source |
| Standing Rule v3 (on-disk canonical) | GREEN — Stage A + rulings + close all on-disk |
| AS-H1 retention held-class (no direct DELETE) | GREEN — OB-R5 preserves stale briefs; no DELETE handlers |
| Governance §8 data-blind posture | OB-G-DB (green) |
| Governance §9 metric-verdict-in-raw-LoC | GREEN — verdict rendered in raw LoC · WITHIN BAND |
| Governance §10 9.2 split ruling | GREEN — OB dispatch-independent from 9.2a/9.2b |
| Governance §11 9.2-OWN resolution | N/A (OB is control-plane) |
| Governance §12 close-ratification-on-own-text | GREEN — three criteria met (see §1) |
| Governance §12.1 remaining-gates enumeration | GREEN — see §5 |
| AF-E2 amended boundary set (Standing Disposition 2026-07-10 · AF-scope-only) | GREEN — briefs run under §12.1 posture; brief runtime transients → sidecar telemetry, never a refusal envelope (`test_ob_g_runtime_transient_never_refusal_envelope`) |
| AF-E3 α sidecar telemetry precedent | REUSED — `brief_telemetry.py` mirrors `fluency_mode_telemetry.py` shape |
| AS-U2 sample rules (fixture-census demo permitted) | APPLIED — fixture-notice card rendered at `data-testid="opportunity-briefs-fixture-notice"` |
| OB-R1 salvage-lifted-not-imported | ATTESTED via `services/opportunity_briefs/README.md` salvage carrier · zero Akki imports |

---

## §7. Tier-3 defaults applied (silent · one-line disclosure per §6.3)

- **[Tier 3]** module names as Stage A §6.3 enumerates — `services/opportunity_briefs/{generator,brief_registry,brief_selector,brief_telemetry,brief_grounding,advisory_marker,shape_as_objective_prefill}.py` + Shield-side `brief_synthesizer.py` + `brief_prompt.v0.txt` (`brief_proposer.py` folded into `brief_selector.py` + `generator.py` per §4.1 no-round-trip discretion).
- **[Tier 3]** LLM model: Sonnet via `llm_router::_provider_for("analytical")` (Phase 7 Stage B-2 seed reused · no new integration).
- **[Tier 3]** Shield timeout: 30s (AF-E2 amended Tier-3 default).
- **[Tier 3]** structured-output field names: `{brief_text, quantitative_anchors: [{value, registry_read_ref}]}`.
- **[Tier 3]** brief-registry table shape: in-memory `BriefRegistry` singleton (sidecar · not a frozen contract).
- **[Tier 3]** advisory-marker string: `"Advisory: opportunity brief — not a governed response."` (data-blind · applied verbatim in frontend render).
- **[Tier 3]** brief id namespace prefix: `brief_` (distinct from all known id namespaces).
- **[Tier 3]** stale-marking policy: `stale=True` set on regeneration; retention preserved.
- **[Tier 3]** shape-as-objective pre-fill scope: reach only (`contributing_slices` + `brief_id`).
- **[Tier 3]** test file naming: `test_opportunity_briefs_ob_g1_to_g5.py` (folded auxiliary gates in same file per §4.1 no-round-trip discretion; single-file cohesion).
- **[Tier 3]** salvage-lift reference path: `services/opportunity_briefs/README.md` (design carrier · lifted-not-imported · no separate `docs/salvage/*` file needed).
- **[Tier 3]** frontend component naming: `OpportunityBriefCard`, `OpportunityBriefsPage` (adapted from Stage A §6.3 default; sub-components inlined per single-render-surface simplicity).
- **[Tier 3]** frontend route: `/opportunity-briefs` (single surface hosting three fixture-census cards per AS-U2).

---

## §8. §DirectionConsistency check (per Owner §12 dead-tracker · not committed as recurring)

Per Owner 2026-07-10 verbatim: *"ran once, clean pass, done; it is not a recurring per-close section."* Not run at this close per Standing Rule v3 dead-tracker discipline.

---

## §9. §0.1 dispositions + §0.2 debts

**§0.1 dispositions:**
- Zero new §0.1 Standing Owner Dispositions at this close.
- AF-E2 amended (`unavailability surfaces as 503`-superseded-for-runtime-transients, AF-scope-only) UNCHANGED — briefs run under §12.1 posture, not under AF-E2 amended.

**§0.2 debts:**
- Zero new §0.2 Plan Debts at this close.
- Registry read API population — remains gated on 9.2b (owner-side per §11). OB fixture-census demo per AS-U2 covers the surface until 9.2b lands; not a debt.

---

## §10. Provenance + sequence forward

- **Stage A proposal:** `/app/docs/stage_a_proposals/opportunity_briefs.md` · SHA `39061210811943e21a5d1f68da99d356430e0a3bd7d52dc4829ba5fc373d8ab6`.
- **Rulings record:** `/app/docs/rulings/opportunity_briefs_ob_e1_to_e3.md` · SHA `91532c04cae050ea85e6b25f3d56d0b0db1c611b3c39450529b69fbe53e35bf2`.
- **Close report (this file):** `/app/docs/close_reports/opportunity_briefs.md` (SHA emitted post-write).
- **Salvage carrier (OB-R1 lifted-not-imported):** `/app/backend/services/opportunity_briefs/README.md`.
- **Sequence forward:** §3.4 **Production Housing (PH-R1)** Stage A dispatches immediately on this close (Owner pre-cleared 2026-07-10). PH-R1 packaging = builder-side dispatchable half; PH-R2/PH-R3/PH-R4 remain scope-annotated with [OWNER] bindings blocking full production landing. Then mandate-complete gate. 9.2b remains owner-side per §11.

═══════════════════════════════════════════════════════════════════

*End of §3.15 Opportunity Briefs close report. Standing Rule v3: on-disk canonical. Per governance §12: named gates green (§3) · rulings attested as applied (§2) · no new Tier-1 escalation surfaced during execution — close ratifies on its own text.*
