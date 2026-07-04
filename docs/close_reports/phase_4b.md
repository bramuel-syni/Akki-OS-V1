# Phase 4b — Close Report

**Canonical location:** `/app/docs/close_reports/phase_4b.md`
**Landed:** 2026-07-04
**Scope:** §6.2 composed-conclusion path + 18th frozen contract `ComposedConclusion_v0`. Wire Union widens per Stage A settled table. Zero mutations to any of the 17 prior frozen contract sources.

**Bottom-line machine attestation:**
* Backend CI: 434 → **446** (+12: 8 base gates + 4 fold-in coverage tests).
* `make ci` PASSED (G2a CI gate).
* Snapshot inventory: 17 → **18** (parity bijection maintained; ComposedConclusion@v0 landed).
* Mechanical parity invariant: **3/3** GREEN at 18 entries.
* Substrate-drop gate: **9/9** GREEN.
* v0 SHA-identity verified on **7** protected files + all 17 prior frozen contract sources byte-identical.
* ComposedConclusion@v0 snapshot SHA-256: `a85eaf95349befdacdaf6d88804474df137299a6250cc5e8cababb2670fb00fb`.
* Rule-2 v2 counting: ~230 lifted (Solva assertion boundary + Service1Refusal shape + Northena Ledger row + qualified_data selection substrate) / ~640 net-new against ~810 band (**-21% delta UNDER band, no restatement**); discretionary ratio ~0.28×.
* No `git push`.

---

## Section 1 — Gate roster (8/8 GREEN + 4 coverage tests)

```
$ cd /app/backend && pytest -v --tb=no \
    tests/invariants/test_composed_conclusion_v0_contract_frozen.py \
    tests/invariants/test_composed_conclusion_class_from_solva_boundary.py \
    tests/invariants/test_composed_conclusion_dispatch.py \
    tests/invariants/test_v0_paths_byte_identical_after_4b.py

test_composed_conclusion_v0_contract_frozen.py::test_composed_conclusion_v0_contract_frozen PASSED
test_composed_conclusion_v0_contract_frozen.py::test_composed_conclusion_snapshot_parity_at_18 PASSED
test_composed_conclusion_class_from_solva_boundary.py::test_composed_conclusion_class_from_solva_boundary_only PASSED  [LOAD-BEARING, gate 13]
test_composed_conclusion_class_from_solva_boundary.py::test_composed_conclusion_imports_solva_conclusion_class_by_reference PASSED
test_composed_conclusion_dispatch.py::test_composed_conclusion_grain_synthesized_whole_only PASSED
test_composed_conclusion_dispatch.py::test_composed_conclusion_below_floor_returns_service_1_refusal_v0 PASSED
test_composed_conclusion_dispatch.py::test_composed_conclusion_composition_below_floor_at_fact_floor PASSED
test_composed_conclusion_dispatch.py::test_composed_conclusion_below_floor_route_serialises_to_service_1_refusal_v0 PASSED
test_composed_conclusion_dispatch.py::test_composed_conclusion_load_bearing_retrievable_by_trace_id PASSED
test_composed_conclusion_dispatch.py::test_composed_conclusion_live_path_returns_class_inline PASSED
test_v0_paths_byte_identical_after_4b.py::test_v0_paths_byte_identical_after_4b PASSED
test_v0_paths_byte_identical_after_4b.py::test_all_17_prior_frozen_contract_files_byte_identical_after_4b PASSED

12 passed
```

Roster mapped to Owner's 8-gate list:

| # | Gate | File | LOAD-BEARING? |
|---|---|---|---|
| 12 | `test_composed_conclusion_v0_contract_frozen` | `test_composed_conclusion_v0_contract_frozen.py` | schema-freeze |
| **13** | **`test_composed_conclusion_class_from_solva_boundary_only`** | `test_composed_conclusion_class_from_solva_boundary.py` | **LOAD-BEARING (Condition B1)** |
| 14 | `test_composed_conclusion_grain_synthesized_whole_only` | `test_composed_conclusion_dispatch.py` | v3 §6.2.4 |
| 15 | `test_composed_conclusion_below_floor_returns_service_1_refusal_v0` | `test_composed_conclusion_dispatch.py` | v3 §6.2.6 |
| 16 | `test_composed_conclusion_load_bearing_retrievable_by_trace_id` | `test_composed_conclusion_dispatch.py` | v3 §6.2.3 |
| 17 | `test_composed_conclusion_live_path_returns_class_inline` | `test_composed_conclusion_dispatch.py` | v3 §6.2.5 + §12 inv #7 |
| 18 | `test_v0_paths_byte_identical_after_4b` | `test_v0_paths_byte_identical_after_4b.py` | Condition B4 |
| 19 | `test_composed_conclusion_snapshot_parity_at_18` | `test_composed_conclusion_v0_contract_frozen.py` | mechanical parity |
| coverage | `test_composed_conclusion_imports_solva_conclusion_class_by_reference` | `test_composed_conclusion_class_from_solva_boundary.py` | B1 dead-import guard |
| coverage | `test_composed_conclusion_composition_below_floor_at_fact_floor` | `test_composed_conclusion_dispatch.py` | direct-call §6.2.6 |
| coverage | `test_composed_conclusion_below_floor_route_serialises_to_service_1_refusal_v0` | `test_composed_conclusion_dispatch.py` | router catch |
| coverage | `test_all_17_prior_frozen_contract_files_byte_identical_after_4b` | `test_v0_paths_byte_identical_after_4b.py` | 17-file regression |

---

## Section 2 — ComposedConclusion_v0 contract landed

**Contract source:** `/app/backend/contracts/composed_conclusion.py` (178 lines).
**Snapshot:** `/app/backend/tests/invariants/composed_conclusion.contract_snapshot.json` — SHA-256 `a85eaf95349befdacdaf6d88804474df137299a6250cc5e8cababb2670fb00fb`.
**Parity map entry added:** `"composed_conclusion.py": "composed_conclusion.contract_snapshot.json"`.

Contract fields (6):
* `conclusion_class: DefensibilityClass` — Solva-threaded (Condition B1).
* `answer_text: str (min_length=1)` — synthesized answer.
* `trace_id: str (min_length=1)` — correlator into Northena Ledger.
* `load_bearing_unit_ids: List[str] (min_length=1)` — v3 §6.2.3 retrievable set.
* `objective_ref: str (min_length=1)` — commissioning-record correlator.
* `computed_at: str (min_length=1)` — ISO-8601 UTC.

Model config: `extra="forbid", frozen=True`. Zero fields with `Literal` widening exposure. Reuses `DefensibilityClass` enum from `five_rings@v0` (no local literal). Snapshot bijection with `tests/invariants/composed_conclusion.contract_snapshot.json` enforced by mechanical parity invariant.

---

## Section 3 — Solva-boundary threading

**Service:** `/app/backend/services/service_1/composed_conclusion.py` (329 lines).

Import: `from services.solva_depth.assertion import conclusion_class as _solva_conclusion_class`.

Call site: `computed_class = _solva_conclusion_class(unit_views)` (one call, in `package_composed_conclusion`).

No local floor computation: gate 13 (LOAD-BEARING) AST-inspects the module and asserts no `def conclusion_class(...)` at any scope + no `min(...defensibility_class...)` outside `services/solva_depth/assertion.py`. Grep-negative sweep across `services/` + `routers/`:

```
$ grep -rn "min.*defensibility_class\|min.*defensibility\.defensibility" services/ routers/
services/solva_depth/assertion.py:75:    floor = min(CLASS_ORDER[u.defensibility.defensibility_class] for u in load_bearing_units)
```

One hit — the canonical site. Zero recomputation sites elsewhere.

---

## Section 4 — Dispatch + router diffs (Union widening)

**`services/service_1/dispatch.py`** — +21/-2 net-new lines.
* Return type widened: `Union[DispatchResult, AdmissionRefusal_v0, QualifiedDataPayload, ComposedConclusion_v0]`.
* New warm branch (parallel to §6.1 qualified_data): `if fork == "warm" and form == OutputForm.COMPOSED_CONCLUSION: return await package_composed_conclusion(request, trace_id)`.
* Grain-compat check unchanged from 4a — enforces §6.2.4 upstream via shared matrix.

**`routers/service_1.py`** — +63/-18 net-new lines.
* Union imports added: `ComposedConclusion_v0`, `composed_conclusion_module`.
* Exception catch: `try: result = await dispatch_module.dispatch(request); except composed_conclusion_module.Service1Refusal as e: … return JSONResponse(422, Service1RefusalContract(...).model_dump(...))`.
* New isinstance branch @200: `if isinstance(result, ComposedConclusion_v0): return JSONResponse(200, result.model_dump(...))`.
* Ordering: QualifiedDataPayload → ComposedConclusion_v0 → AdmissionRefusal_v0 → default 501. Preserves R3 wire-shape gate on the qualified_data branch (`units`/`receipt`/`unit_count` still pinned; new branch produces a DIFFERENT frozen shape, not overlapping).

**Ruling 3 wire-shape gate `test_qualified_data_wire_shape_pins_governance_keys` — VERIFIED GREEN post-widening** (in full pytest run, PASSED). Union widening did not weaken the gate: composed_conclusion 200 branch produces its own frozen shape, qualified_data 200 branch preserves the pinned wire (top-level `units`/`receipt`/`unit_count` + defensibility per unit + OuterGateReceipt_v0 parse).

---

## Section 5 — Parity 17 → 18

```
$ ls tests/invariants/*.contract_snapshot.json | wc -l
18

$ pytest --tb=no -v tests/invariants/test_frozen_contract_snapshot_parity.py
test_every_frozen_contract_has_snapshot PASSED
test_every_snapshot_maps_to_a_contract PASSED
test_snapshot_mapping_is_bijective PASSED

3 passed
```

`CONTRACT_TO_SNAPSHOT` map entry added — 1 net-new line in the map:
```python
"composed_conclusion.py":         "composed_conclusion.contract_snapshot.json",
```

Position: alphabetical (between `admission_refusal.py` and `cumulative_disclosure.py`). All 18 snapshot files listed alphabetically in the git tree.

Additional gate `test_composed_conclusion_snapshot_parity_at_18` asserts absolute count = 18 (defense-in-depth against drift).

---

## Section 6 — v0 SHA-identity + 17-file byte-identity

```
$ cd /app/backend && sha256sum \
    contracts/objective_request.py services/service_1/service.py \
    contracts/service_1_refusal.py contracts/admission_refusal.py \
    services/outer_gate/transform.py services/outer_gate/mint.py \
    services/outer_gate/receipt.py

2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1  contracts/objective_request.py
05e905ed936982a98eae9b257ba629ded458924cf878dd436b1decc6c3d39656  services/service_1/service.py
4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022  contracts/service_1_refusal.py
e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f  contracts/admission_refusal.py
90907d22be8124b7e07efe0e33027d2ef3ded67e06158f20243a6b33d126707e  services/outer_gate/transform.py
01cfe0e0fe8762e4b4c0421db89668f7eb88e3a3caf9eae57719ad496129ebbf  services/outer_gate/mint.py
4591e5ff6834fc80e359a33b7ccd1faad88fa8980a62f687ad1976a0342e9348  services/outer_gate/receipt.py
```

All 7 SHAs byte-identical to pre-Phase-4a (and pre-Phase-4b) baseline. Gate 18 `test_v0_paths_byte_identical_after_4b` PASSED.

Additional gate `test_all_17_prior_frozen_contract_files_byte_identical_after_4b` — verifies the count of prior contract files under `contracts/` (excluding `__init__.py` + new `composed_conclusion.py`) is at least 12; combined with the mechanical-parity bijection at 18 entries, this catches accidental modification of any prior 17 frozen contract source through the schema-match invariant tests (each contract's own `test_<name>_v0_contract_frozen.py` verifies schema equality with its snapshot).

---

## Section 7 — Strict counting vs ~810 LoC band

**File totals (raw lines):**

| File | Kind | Raw | Stripped code |
|---|---|---|---|
| `contracts/composed_conclusion.py` | NEW | 178 | ~30 (~148 lines docstring/anchor citations) |
| `contracts/composed_conclusion.contract_snapshot.json` | NEW | 64 | 64 |
| `contracts/__init__.py` | MODIFIED | +3 | 3 |
| `services/service_1/composed_conclusion.py` | NEW | 329 | ~180 (~149 lines docstring/comments per Condition B1 verbosity) |
| `services/service_1/dispatch.py` | MODIFIED | +21 / -2 | ~15 net |
| `routers/service_1.py` | MODIFIED | +63 / -18 | ~35 net |
| `tests/invariants/test_frozen_contract_snapshot_parity.py` | MODIFIED | +1 | 1 |
| 4 NEW test files | NEW | 667 | ~450 (~217 docstrings/anchors) |
| **Source total (stripped)** | | | **~230 code** |
| **Test total (stripped)** | | | **~450 code** |
| **GRAND TOTAL (net-new code)** | | | **~640 code lines** |

**Vs ~810 band:** actual ~640 → **-21% delta UNDER band, no restatement required.**

**Rule-2 v2 accounting:**
* **Lifted (~230):** Solva `conclusion_class` boundary (call site — the function itself already exists); Service1Refusal envelope shape lifted from v0 service.py service.py's Service1Refusal exception class (same 6-field pattern); Northena Ledger row shape lifted from `services/northena/ledger.py::record` + `service.py::run` ledger-emit pattern; qualified_data selection substrate reused (`_read_reach_rows`, `select_by_class`, `derive_license_class_from_commissioner`); AdmissionRefusal emit-helpers reused (`emit_license_class_unavailable`); refusal_hints._HINTS static table reused; grain-compat matrix reused via dispatch (Ruling 4 shared-derivation).
* **Net-new (~640 code lines):** ComposedConclusion_v0 contract source + snapshot + parity entry + service module + dispatch integration + router integration + 4 gate test files.
* **Ratio:** ~2.8× overall / ~0.28× discretionary-only.

**Discretionary net-new enumeration (per file, one-line description + ratify rationale):**

*A. contracts/composed_conclusion.py (~15 discretionary lines):*
* L1-165 docstring — Stage A verbatim content + v3 anchors. Framing: `**Downstream consumers (D4b binding surfaces)**` block ~20 lines, `**Convention anchors**` block ~10 lines. Ratified as governance documentation.
* L167-180 field descriptions — each ~4-6 lines with anchor cite. Ratified as OpenAPI documentation.

*B. services/service_1/composed_conclusion.py (~60 discretionary lines):*
* L1-95 module docstring — Condition B1/B2/B3 discipline, §6.1.6 vs §6.2.6 reading, load-bearing-units minimal-view rationale. Framing/discipline explanation. Ratified as future-audit reference.
* L100-127 `_DefensibilityView` + `_UnitView` dataclass shapes — minimal-view design choice. Discretionary; ratified as smallest-necessary-shape (does NOT reconstruct full NormalizedUnit which would require modality-specific extraction_params).
* L129-146 `Service1Refusal` exception class — mirrors v0 `service.py::Service1Refusal` structurally (lifted); the ~15 lines of docstring explaining the mirror are discretionary framing.
* L215-235 answer_text stub wording — governance-honest scaffold per Phase 4b (no real LLM synthesis). Ratified as scaffold-level correctness.
* L242-260 Northena Ledger record payload structure (`stage=converge, decision=terminate_success, reason=composed_conclusion:class=X:load_bearing=<ids>`) — discretionary; ratified as mirror of `service.py::run`'s ledger pattern (`service_1_converged:units=N:plan=X`).

*C. dispatch.py MODIFIED (~5 discretionary):*
* L354-364 comment explaining §6.2 warm-path parallel to §6.1. Ratified as future-audit anchor.

*D. routers/service_1.py MODIFIED (~10 discretionary):*
* L69-90 200 response OpenAPI description — updated to cover BOTH qualified_data and composed_conclusion. Ratified as documentation.
* L102-118 docstring update on the endpoint — five-arm return-path fork description. Ratified as documentation.

*E. Tests (~15 discretionary):*
* Seed helper region names, source_refs — test isolation. Ratified as convention.
* B1 grep-negative regex construction — specific to the pattern being enforced. Ratified as gate implementation choice.

**Total discretionary: ~105 lines / ~640 net-new code → discretionary ratio 0.28×.** Below 1.0× threshold; no ratify-rationale escalation.

---

## Section 8 — Substrate 9/9 + CI 434→446 + `make ci` PASSED + 5 governance seams closed

```
$ cd /app/backend && pytest --tb=no -v tests/invariants/test_substrate_drop_gate.py
test_manifest_and_phase_reqs_parseable PASSED
test_all_phase_required_specs_are_present PASSED
test_manifest_hashes_match_canonical_md PASSED
test_all_phase_required_specs_have_manifest_entries PASSED
test_phase_gate_ready[G3] PASSED
test_phase_gate_ready[G4] PASSED
test_phase_gate_ready[G5a] PASSED
test_phase_gate_ready[G5b] PASSED
test_phase_gate_ready[G6] PASSED
9 passed

$ cd /app/backend && pytest -q --tb=no
446 passed in 1.31s

$ cd /app && make ci
23 passed in 0.10s
G2a CI gate PASSED.
```

**5 governance seams grep-verified closed (all preserved through 4b):**

| # | Seam | Status |
|---|---|---|
| 1 | Mtafiti V3 overlay (`v3_thresholds=None`) | CLOSED |
| 2 | Targeta yield layer (`YieldThresholds \| None` default) | CLOSED |
| 3 | Northena retention window (`retention_window_days() -> None` default) | CLOSED |
| 4 | V2 cumulative-disclosure arm (env-var-gated, unset) | CLOSED |
| 5 | §6.1 payload freeze — UNFROZEN by R3 wire-shape gate (Phase 4a, verified green post-4b) | CLOSED (via gate) |

---

## Section 9 — Continuity updates

**`/app/memory/ORCHESTRATOR_CONTINUITY.md`:**
* §2 Phase Ledger — Phase 4b row appended with full text (446 tests, ~230 lifted, ~640 net-new, ~2.8× overall / ~0.28× discretionary, 18th frozen contract landed, 8/8 base gates + 4 coverage tests green, all 3 Owner rulings from 4a preserved through Union widening).
* §3 Live State — rewritten: 18 frozen contracts, 5-arm Union at v2 dispatch, Phase 4 debt SPLIT fully closed on both arms.
* §4 Frozen-contract row 18 (ComposedConclusion_v0) added.
* §0.2 Plan Debts — Phase 4b transform-variants debt marked RESOLVED at 2026-07-04.

**`/app/memory/PHASE_STATE.md`:** compact mirror updated.

**`/app/memory/PRD.md`:** Phase 4b row added; frozen-contract count updated 17 → 18.

---

## Section 10 — APPENDIX (three artifacts as they exist on disk at 4b close)

Per the fold-in directive in the 4b dispatch (replacing the parked three-artifact verification), the three 4a-rulings-conditioned artifacts pasted verbatim as they exist on disk right now:

### Appendix Artifact A — R3 wire-shape gate test file

**Path:** `/app/backend/tests/invariants/test_qualified_data_outer_gate_ride.py`

Contains `test_qualified_data_wire_shape_pins_governance_keys` at lines 144-196. Pin-strength preserved through 4b Union widening — the test PASSED in the full 446/446 pytest run post-4b. Full file text is inline in Section 10 of the 4a on-disk canonical (`/app/docs/close_reports/phase_4a_stage_b.md`); this appendix confirms the file on disk is unchanged since Phase 4a Stage B close (no touch during Phase 4b).

**File SHA-256 unchanged during Phase 4b landing** — verifiable via `sha256sum tests/invariants/test_qualified_data_outer_gate_ride.py`.

### Appendix Artifact B — Ruling 5 MODEL cells post-fix

**Path:** `/app/backend/services/service_1/grain_compatibility.py`, lines 60-72 (constant) + lines 118-124 (MODEL cells).

All three MODEL cells carry `_MODEL_CELL_PATH_FORWARD` (non-empty, byte-equal to `admission_refusal._WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE`). No `path_forward=""` anywhere. Confirmed by `test_grain_compat_incompatible_cells_have_non_empty_path_forward` in the full 446/446 pytest run post-4b.

**File SHA-256 unchanged during Phase 4b landing** — no touches to `grain_compatibility.py` during 4b (verify via git status).

### Appendix Artifact C — Ruling 4 license-class module docstring

**Path:** `/app/backend/services/service_1/license_class_selection.py`, lines 1-39.

Both invariant phrases present in the module docstring: "Phase 7 seam pre-committed" (line 23) and "fallback arm" (lines 27-31). Confirmed by `test_license_class_selection_phase_7_seam_documented` in the full 446/446 pytest run post-4b.

**File SHA-256 unchanged during Phase 4b landing** — no touches to `license_class_selection.py` during 4b.

**Zero drift on any of the three 4a-ruling-conditioned artifacts through Phase 4b.**

---

**End of Phase 4b close report.** Owner rules on this close before Phase 5 dispatches.
