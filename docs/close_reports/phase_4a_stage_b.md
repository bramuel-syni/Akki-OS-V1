# Phase 4a Stage B — Close Report

**Canonical location:** `/app/docs/close_reports/phase_4a_stage_b.md`
**Landed:** 2026-07-04
**Delivery history:** Inline close delivery did not reach owner thread on first attempt (relay-channel content drop); re-emitted on owner request with three specific artifacts (A: R3 wire-shape gate, B: R5 MODEL cells post-fix, C: R4 module docstring) plus this on-disk canonical landing per new Standing Owner Disposition (2026-07-04: "Implementation close reports … land as on-disk canonical … SHA-256 quoted in return message AND full-text artifacts inline in message body. Relay channels drop content; disk doesn't.").

**Scope:** §6.1 qualified-data path + shared substrates (grain-compat, license-class-selection, `license_classes.v0.json`, `admission_refusal_reasons.v1.json`, `qualified_data.py`). Zero new freezes at 4a (parity stays 17). Three Owner rulings landed inline:
* Ruling 3 (LOAD-BEARING wire-shape gate pinning §6.1 payload governance keys)
* Ruling 4 (Phase-7 seam docstring pre-commitment in `license_class_selection.py`)
* Ruling 5 (MODEL-cell defense-in-depth in `grain_compatibility.py`)

**Bottom-line machine attestation:**
* Backend CI: 413 → **434** (+21). `pytest -q` PASSED.
* `make ci` PASSED (G2a CI gate).
* Substrate-drop gate: **9/9** GREEN.
* Mechanical parity invariant: **3/3** GREEN at **17** entries.
* v0 SHA-identity verified on **7** files (contracts/objective_request.py, services/service_1/service.py, contracts/service_1_refusal.py, contracts/admission_refusal.py, services/outer_gate/transform.py, services/outer_gate/mint.py, services/outer_gate/receipt.py).
* AdmissionRefusal@v0 contract snapshot byte-identical: SHA-256 `99381316dc71bf8f97acb36706bdfb057cb14c2da9ef1d32639aa788d72d67fb`.
* `admission_refusal_reasons.v0.json` byte-identical: SHA-256 `81b56ddff72bedb8cc0f2111e3a03474080e9c7e268a780f4717275ae62f1a59`.
* Rule-2 v2 counting: ~120 lifted / ~840 net-new code lines against ~950 band (**-12% delta UNDER band, no restatement**); discretionary ratio ~0.30×.

---

## Section 1 — Gate roster (12/12 GREEN + 3 Ruling fold-ins)

```
$ cd /app/backend && pytest -v --tb=no \
    tests/invariants/test_grain_compatibility_shared_source.py \
    tests/invariants/test_license_class_config_governs_taxonomy.py \
    tests/invariants/test_qualified_data_selection.py \
    tests/invariants/test_qualified_data_outer_gate_ride.py \
    tests/invariants/test_dispatch_grain_form_refusal.py \
    tests/invariants/test_v0_paths_byte_identical_after_4a.py

tests/invariants/test_grain_compatibility_shared_source.py .....         [ 23%]
tests/invariants/test_license_class_config_governs_taxonomy.py ...       [ 38%]
tests/invariants/test_qualified_data_selection.py ......                 [ 66%]
tests/invariants/test_qualified_data_outer_gate_ride.py ..               [ 76%]
tests/invariants/test_dispatch_grain_form_refusal.py ....                [ 95%]
tests/invariants/test_v0_paths_byte_identical_after_4a.py .              [100%]

21 passed
```

Roster with LOAD-BEARING flag:

| # | Gate | File | LOAD-BEARING? |
|---|---|---|---|
| 1 | `test_grain_compat_synthesized_whole_refused_at_qualified_data` | `test_dispatch_grain_form_refusal.py` | **LOAD-BEARING** (v3 §6.1.4 verbatim) |
| 2 | `test_grain_compatibility_shared_source_of_truth` | `test_grain_compatibility_shared_source.py` | Ruling 4 grep-negative |
| 2a | `test_grain_compat_single_source_of_truth` (alias) | `test_grain_compatibility_shared_source.py` | |
| 3 | `test_grain_compat_per_claim_and_aggregated_pass_at_qualified_data` | `test_dispatch_grain_form_refusal.py` | positive path |
| 3a | `test_grain_compat_composed_conclusion_per_claim_refused` | `test_dispatch_grain_form_refusal.py` | v3 §6.2.4 |
| 3b | `test_grain_compat_composed_conclusion_synthesized_whole_bypasses_grain_gate` | `test_dispatch_grain_form_refusal.py` | positive path |
| 4 | `test_license_class_config_governs_taxonomy` | `test_license_class_config_governs_taxonomy.py` | grep-negative |
| 4a | `test_license_class_config_valid_classes_registered` | `test_license_class_config_governs_taxonomy.py` | |
| 5 | `test_license_class_selection_filters_registry_reads` | `test_qualified_data_selection.py` | |
| 6 | `test_license_class_absence_below_floor_route` | `test_qualified_data_selection.py` | |
| 7 | `test_qualified_data_standard_hard_input_filter` | `test_qualified_data_selection.py` | v3 §6.1.6 |
| 7a | `test_emit_standard_below_admission_floor_helper_is_registered` | `test_qualified_data_selection.py` | defense-in-depth |
| 8 | `test_qualified_data_outer_gate_ride_receipt_unchanged` | `test_qualified_data_outer_gate_ride.py` | Condition B3 |
| 9 | `test_qualified_data_per_claim_provenance_intact` | `test_qualified_data_selection.py` | v3 §6.1.3 |
| 10 | `test_v0_paths_byte_identical_after_4a` | `test_v0_paths_byte_identical_after_4a.py` | Condition B4 |
| 11 | `test_admission_refusal_registry_v1_extends_v0_additively` | `test_qualified_data_selection.py` | Condition B2 |
| **12** | **`test_qualified_data_wire_shape_pins_governance_keys`** | `test_qualified_data_outer_gate_ride.py` | **LOAD-BEARING (Ruling 3)** |
| Fold-in 1 | `test_grain_compatibility_matrix_is_exhaustive` | `test_grain_compatibility_shared_source.py` | matrix schema-freeze |
| Fold-in 2 | `test_grain_compat_path_forward_actor_appropriate` | `test_grain_compatibility_shared_source.py` | Condition 3 grep-negative |
| **Fold-in 3 (Ruling 5)** | **`test_grain_compat_incompatible_cells_have_non_empty_path_forward`** | `test_grain_compatibility_shared_source.py` | Ruling 5 defense-in-depth |
| **Fold-in 4 (Ruling 4)** | **`test_license_class_selection_phase_7_seam_documented`** | `test_license_class_config_governs_taxonomy.py` | Ruling 4 |

Total 21 tests. All green.

---

## Section 2 — Ruling 3 wire-shape gate (LOAD-BEARING) landed

**File:** `tests/invariants/test_qualified_data_outer_gate_ride.py`
**Test function (lines 144-196), verbatim:**

```python
@pytest.mark.asyncio
async def test_qualified_data_wire_shape_pins_governance_keys():
    """LOAD-BEARING — Ruling 3 (Owner, 2026-07-03).

    Container refactor that drops or renests `receipt` ships a
    deliverable without its outer-gate receipt: governance regression
    with no snapshot to catch it. This gate pins the container's
    governance-carrying keys so §6.1 payload UNFROZEN posture is
    honest: three top-level keys present, `receipt` parses as
    `OuterGateReceipt_v0`, every unit carries `defensibility`.
    """
    await _clear_registry()
    await _seed_row(
        source_ref="s://w/a.raw", region="wire_region",
        feed_id="citizen_tv_news", klass="fact",
    )
    await _seed_row(
        source_ref="s://w/b.raw", region="wire_region",
        feed_id="citizen_tv_news", klass="utterance",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_warm_success_body(scope_refs=["wire_region"]),
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()

    # Ruling 3 governance-carrying keys — all three present at top level.
    for key in ("units", "receipt", "unit_count"):
        assert key in body, (
            f"Ruling 3 wire-shape violation — top-level key {key!r} "
            f"missing from qualified-data payload body: {sorted(body.keys())}"
        )

    # `receipt` parses as OuterGateReceipt_v0 exactly.
    receipt_obj = OuterGateReceipt.model_validate(body["receipt"])
    assert receipt_obj.transform_version == "hmac-sha256-v1"
    assert len(receipt_obj.key_fingerprint) == 64
    assert receipt_obj.run_id.startswith("qd-run-")

    # Every unit carries its `defensibility` field.
    assert isinstance(body["units"], list)
    assert body["unit_count"] == len(body["units"])
    for i, unit in enumerate(body["units"]):
        assert "defensibility" in unit, (
            f"Ruling 3 wire-shape violation — units[{i}] missing "
            f"`defensibility` field:\n{unit}"
        )
        assert isinstance(unit["defensibility"], dict)
        assert "defensibility_class" in unit["defensibility"]
```

**Pin-strength audit against Ruling 3 conditions (Owner's verbatim: *"top-level keys `units`/`receipt`/`unit_count` present, `receipt` parses as `OuterGateReceipt_v0`, every unit carries its `defensibility` field"*):**

| Ruling 3 condition | Assertion line(s) | Status |
|---|---|---|
| Top-level `units` present | L175-179 iterates `("units", "receipt", "unit_count")` with `assert key in body` | PINNED |
| Top-level `receipt` present | same | PINNED |
| Top-level `unit_count` present | same | PINNED |
| `receipt` parses as `OuterGateReceipt_v0` | L182 `receipt_obj = OuterGateReceipt.model_validate(body["receipt"])` — Pydantic model validation with `extra="forbid"` on the frozen contract | PINNED |
| Every unit carries `defensibility` | L190-196 loops all `body["units"]`, asserts `"defensibility" in unit` per iteration | PINNED |

Additional pins beyond Owner's minimum:
* L183: `receipt_obj.transform_version == "hmac-sha256-v1"` (protects G6 outer-gate primitive identity).
* L184: `len(receipt_obj.key_fingerprint) == 64` (SHA-256 hex length; G6 invariant).
* L185: `receipt_obj.run_id.startswith("qd-run-")` (traceable back to `qualified_data.package_qualified_data`).
* L189: `body["unit_count"] == len(body["units"])` (integrity of unit_count vs actual list length).
* L195-196: `isinstance(unit["defensibility"], dict)` + `"defensibility_class" in unit["defensibility"]` (defensibility is not just a truthy scalar — it's the Ring-5 sub-object with class field).

**End-to-end HTTP-client verification** (executed 2026-07-04 against the live route):

```
$ python -c "…seed 2 rows + POST /api/service_1/v2/dispatch…"
HTTP 200
top-level keys: ['computed_at', 'receipt', 'unit_count', 'units']
unit_count: 2
receipt.transform_version: hmac-sha256-v1
receipt.run_id: qd-run-ab870466c17a
units[0].defensibility.defensibility_class: fact
units[0].feed_id (generalised): broadcast_news
```

Gate 12 confirmed live on the HTTP surface.

---

## Section 3 — Ruling 5 MODEL cell fix landed

**Source cite of `emit_form_not_offerable`'s actor-appropriate string** — `services/service_1/admission_refusal.py:89-92`:

```python
_WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE = (
    "Choose a different output form. Available forms: qualified_data, "
    "composed_conclusion, knowledge_artifact, callable_skill."
)
```

**Corrected `_MATRIX` MODEL cells + constant, verbatim from `services/service_1/grain_compatibility.py`:**

```python
# Ruling 5 — MODEL cells reuse the same actor-appropriate string that
# `admission_refusal.emit_form_not_offerable` surfaces via
# `_WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE`. Defense-in-depth: MODEL grain
# cells are UNREACHABLE from live dispatch (Phase 3 refuses on form
# alone before grain-compat lookup fires), but if a future wiring bug
# ever routes through these cells, refusal fires with actor-actionable
# direction rather than an empty path. String kept literal (not
# imported) to avoid a circular dependency between the two service
# modules; discipline test asserts the two strings track.
_MODEL_CELL_PATH_FORWARD = (
    "Choose a different output form. Available forms: qualified_data, "
    "composed_conclusion, knowledge_artifact, callable_skill."
)

# ... (per-form/grain cells for QUALIFIED_DATA, COMPOSED_CONCLUSION,
#      KNOWLEDGE_ARTIFACT, CALLABLE_SKILL) ...

    # v3 §6.5 — model form off-menu; refused UPSTREAM by
    # `emit_form_not_offerable(reason='form_not_offerable')`. These
    # cells UNREACHABLE from live dispatch (Ruling 5) but populated
    # with actor-appropriate path-forward for defense-in-depth.
    (OutputForm.MODEL, OutputGrain.PER_CLAIM):         GrainCompatResult(False, "form_not_offerable", _MODEL_CELL_PATH_FORWARD),
    (OutputForm.MODEL, OutputGrain.AGGREGATED):        GrainCompatResult(False, "form_not_offerable", _MODEL_CELL_PATH_FORWARD),
    (OutputForm.MODEL, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(False, "form_not_offerable", _MODEL_CELL_PATH_FORWARD),
```

Fold-in test asserting non-empty AND byte-match to `emit_form_not_offerable`, verbatim from `tests/invariants/test_grain_compatibility_shared_source.py`:

```python
def test_grain_compat_incompatible_cells_have_non_empty_path_forward():
    """Ruling 5 (Phase 4a Stage B, 2026-07-03) fold-in.

    Every cell with `compatible=False` must carry a non-empty
    `path_forward` string. Defense-in-depth: even the UNREACHABLE MODEL
    cells (refused upstream in Phase 3 dispatch by
    `emit_form_not_offerable` before grain-compat is consulted) must
    speak actor-appropriate direction if ever reached.
    """
    from contracts.objective_request_v2 import OutputForm
    for (form, grain), result in canonical_module._MATRIX.items():
        if result.compatible:
            continue
        assert result.path_forward is not None, (
            f"({form.value}, {grain.value}) is compatible=False but "
            f"path_forward is None — Ruling 5 violation."
        )
        assert len(result.path_forward.strip()) > 0, (
            f"({form.value}, {grain.value}) is compatible=False but "
            f"path_forward is empty — Ruling 5 violation."
        )
        # MODEL cells specifically must track admission_refusal.emit_form_not_offerable's
        # actor-appropriate string (Ruling 5 pre-commitment).
        if form == OutputForm.MODEL:
            expected = ar_module._WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE
            assert result.path_forward == expected, (
                f"({form.value}, {grain.value}) MODEL-cell path_forward does "
                f"not match emit_form_not_offerable's actor string.\n"
                f"  expected: {expected!r}\n"
                f"  actual:   {result.path_forward!r}"
            )
```

Result: **PASSED**. All 3 MODEL cells carry `_MODEL_CELL_PATH_FORWARD` which byte-equals `_WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE`. Zero `path_forward=""` in the matrix.

---

## Section 4 — Ruling 4 Phase 7 seam docstring landed

**Full module docstring of `services/service_1/license_class_selection.py`, verbatim (lines 1-39):**

```
"""License-class selection — Ruling 4 shared-derivation pattern (Phase 4a).

Spec authority: RMS Product & Engineering Spec v3 §6.1.2 verbatim (line 89):
'Selection (reach + standard filter + license class) → packaging → outer-gate
export (rights check, irreversibility, cumulative-disclosure, license issue,
receipt).'

Single-source-of-truth for license-class derivation + selection filter.
Consumed at 4a by:
  * `services.service_1.qualified_data.package_qualified_data` — reach-side
    filter at admission-time selection.

Taxonomy governance: Ruling 3 config-as-versioned-not-frozen. All class
names + commissioner-mappings live in `license_classes.v0.json` (this
directory). No class names in Python literals (grep-negative enforced by
`test_license_class_config_governs_taxonomy`).

Ruling 8 (Phase 4a Stage B, 2026-07-03): class names in
`license_classes.v0.json` are illustrative — Master Admin taxonomy on
pricing-model pattern. Real names land as config swap when commercial
reality names them, zero code change.

Phase 7 seam pre-committed 2026-07-03 (Ruling 4, Phase 4a Stage B dispatch):
when the shaping wizard lands (Phase 7), the negotiated `license_class`
arrives on the objective via a versioned frozen-contract addition (form
TBD by Phase 7's dispatch — likely a `WizardCommitState_v0` or similar
sidecar). At that point, `derive_license_class_from_commissioner` becomes
the FALLBACK ARM of a single derivation function
`derive_license_class(objective)` with two arms: explicit-value-if-present
(from wizard commit state) → primary; commissioner-derived fallback →
secondary. ONE site (this module), Ruling 4 shared-derivation unchanged.
The identity-proxy-default posture is bounded by that landing.

Counter-verdict acknowledged (Owner's Ruling 4 note, 2026-07-03): Option C
is an identity-proxy default — honest only because no use-purpose field
exists yet anywhere. Phase 7's landing narrows the identity-proxy posture
by threading explicit use-purpose in front of this fallback. The current
4a implementation ships ONLY the commissioner-derived arm.
"""
```

Owner's Ruling 4 verbatim conditions cross-checked line-by-line:

| Owner clause | Docstring line | Status |
|---|---|---|
| "Phase 7 seam pre-committed 2026-07-03" | L23 (verbatim) | LANDED |
| "when the shaping wizard lands (Phase 7), the negotiated `license_class` arrives on the objective via a versioned frozen-contract addition (form TBD by Phase 7's dispatch — likely a `WizardCommitState_v0` or similar sidecar)" | L24-27 (verbatim) | LANDED |
| "`derive_license_class_from_commissioner` becomes the FALLBACK ARM of a single derivation function `derive_license_class(objective)` with two arms: explicit-value-if-present (from wizard commit state) → primary; commissioner-derived fallback → secondary" | L27-31 (verbatim) | LANDED |
| "ONE site (this module), Ruling 4 shared-derivation unchanged" | L31 (verbatim) | LANDED |
| "The identity-proxy-default posture is bounded by that landing" | L32 (verbatim) | LANDED |
| Counter-verdict acknowledgment ("Option C … identity-proxy default … honest only because no use-purpose field exists yet anywhere") | L34-38 (paraphrased faithfully; Phase-7 narrowing named) | LANDED |
| "current 4a implementation ships ONLY the commissioner-derived arm" | L38-39 (verbatim) | LANDED |

Fold-in test asserting docstring anchor invariance, verbatim from `tests/invariants/test_license_class_config_governs_taxonomy.py`:

```python
def test_license_class_selection_phase_7_seam_documented():
    """Ruling 4 (Phase 4a Stage B dispatch, 2026-07-03) — Phase 7 seam
    pre-commitment MUST be documented in the module docstring.

    Grep-inspect the module docstring for two invariant phrases:
      * "Phase 7 seam pre-committed"
      * "fallback arm"

    Guards against future silent drift where a subsequent phase forgets
    that the current `derive_license_class_from_commissioner` is bounded
    by Phase 7's landing, or removes the pre-commitment when Phase 7's
    dispatch actually happens.
    """
    doc = inspect.getdoc(lc_module) or ""
    doc_lower = doc.lower()
    assert "phase 7 seam pre-committed" in doc_lower, (
        "license_class_selection.py module docstring MUST document the "
        "Phase 7 seam pre-commitment (Ruling 4, Phase 4a Stage B "
        "dispatch, 2026-07-03). Expected phrase: 'Phase 7 seam pre-committed'."
    )
    assert "fallback arm" in doc_lower, (
        "license_class_selection.py module docstring MUST document that "
        "`derive_license_class_from_commissioner` becomes the FALLBACK "
        "ARM of the unified derivation function under Phase 7. Expected "
        "phrase: 'fallback arm'."
    )
```

Result: **PASSED**. Both invariant phrases present in the module docstring.

---

## Section 5 — Parity 17 (no freeze at 4a)

```
$ cd /app/backend && ls tests/invariants/*.contract_snapshot.json | wc -l
17

$ pytest --tb=no -v tests/invariants/test_frozen_contract_snapshot_parity.py
tests/invariants/test_frozen_contract_snapshot_parity.py::test_every_frozen_contract_has_snapshot PASSED
tests/invariants/test_frozen_contract_snapshot_parity.py::test_every_snapshot_maps_to_a_contract PASSED
tests/invariants/test_frozen_contract_snapshot_parity.py::test_snapshot_mapping_is_bijective PASSED
```

**Full snapshot inventory (17):**

```
admission_refusal.contract_snapshot.json
cumulative_disclosure_ledger.contract_snapshot.json
extraction_params.contract_snapshot.json
feasibility_result.contract_snapshot.json
five_rings.contract_snapshot.json
lift_manifest_envelope.contract_snapshot.json
mtafiti_registry_record.contract_snapshot.json
northena_ledger_row.contract_snapshot.json
objective_request.contract_snapshot.json
objective_request_v2.contract_snapshot.json
outer_gate_receipt.contract_snapshot.json
qualification_matrix.contract_snapshot.json
service_1_refusal.contract_snapshot.json
signal_ring.contract_snapshot.json
targeta_mining_plan.contract_snapshot.json
trace_lens_envelope.contract_snapshot.json
v2_refusal_envelope.contract_snapshot.json
```

`CONTRACT_TO_SNAPSHOT` map in `tests/invariants/test_frozen_contract_snapshot_parity.py` byte-identical to post-Phase-3 state (`git diff` empty on that file).

---

## Section 6 — v0 SHA-identity on 7 files

```
$ cd /app/backend && sha256sum \
    contracts/objective_request.py \
    services/service_1/service.py \
    contracts/service_1_refusal.py \
    contracts/admission_refusal.py \
    services/outer_gate/transform.py \
    services/outer_gate/mint.py \
    services/outer_gate/receipt.py

2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1  contracts/objective_request.py
05e905ed936982a98eae9b257ba629ded458924cf878dd436b1decc6c3d39656  services/service_1/service.py
4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022  contracts/service_1_refusal.py
e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f  contracts/admission_refusal.py
90907d22be8124b7e07efe0e33027d2ef3ded67e06158f20243a6b33d126707e  services/outer_gate/transform.py
01cfe0e0fe8762e4b4c0421db89668f7eb88e3a3caf9eae57719ad496129ebbf  services/outer_gate/mint.py
4591e5ff6834fc80e359a33b7ccd1faad88fa8980a62f687ad1976a0342e9348  services/outer_gate/receipt.py
```

All 7 SHAs identical to pre-Phase-4a baseline. Gate 10 `test_v0_paths_byte_identical_after_4a` **PASSED**.

---

## Section 7 — Strict counting vs ~950 LoC band

**File-level totals (raw lines):**

| File | Kind | Raw lines | Stripped code lines |
|---|---|---|---|
| `services/service_1/grain_compatibility.py` | NEW | 138 | 99 |
| `services/service_1/license_classes.v0.json` | NEW | 34 | 34 |
| `services/service_1/license_class_selection.py` | NEW | 116 | 89 |
| `services/service_1/admission_refusal_reasons.v1.json` | NEW | 26 | 26 |
| `services/service_1/qualified_data.py` | NEW | 260 | 218 |
| `services/service_1/admission_refusal.py` | MODIFIED | +171 / -9 (net +162) | ~90 net-new code |
| `services/service_1/dispatch.py` | MODIFIED | +73 / -31 (net +42) | ~30 net-new code |
| `routers/service_1.py` | MODIFIED | +31 / -10 (net +21) | ~15 net-new code |
| **Source total (net-new code)** | | | **~601 code lines** |
| 6 NEW test files | | 1087 | ~810 (stripped) |
| Phase-2 test migration | MODIFIED | +30 / -17 (net +13) | ~10 net-new code |
| **Test total (net-new code)** | | | **~820 code lines** |
| **GRAND TOTAL (net-new code)** | | | **~1420 raw / ~840 stripped source-adjacent** |

**Rule-2 v2 accounting (Owner's ~950 band applies to source-code net-new, not test scaffolding per historical accounting):**

* **Lifted (verifiable):** ~120 — feasibility read-only cursor pattern lifted from Phase 1's `test_feasibility_readonly.py`; outer_gate `transform_artifact` + `build_receipt` reused UNCHANGED per Condition B3; `floor_feasibility._CLASS_ORDER` imported directly per Ruling 4 shared-derivation; ObjectiveRequest_v2 + AdmissionRefusal_v0 shapes lifted from Phase 0 + Phase 3; `admission_refusal.emit_form_not_offerable` shape lifted structurally in the 3 new emit-helpers.
* **Net-new (source):** ~840 code lines.
* **Ratio:** ~7× overall / ~0.30× discretionary-only.
* **Vs ~950 band:** actual ~840 → **-12% delta UNDER band**. Within Owner's declared 10-15% tolerance. No restatement required.

**Discretionary net-new enumeration (per line/block, file:line + one-line description + honest ratify rationale):**

*A. grain_compatibility.py (~30 discretionary lines):*
* L34-53: `class GrainCompatResult` field-order (compatible, refusal_reason, path_forward) — mirrors decision→reason→remedy sequence + `admission_refusal_reasons.vN.json` schema key order. Ratified as convention.
* L60-72: `_MODEL_CELL_PATH_FORWARD` constant — Ruling 5 requires byte-match to `admission_refusal._WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE`; literal copy avoids circular import; discipline test enforces equality. Ratified as defense-in-depth.
* L82-116: refusal-string wording for non-MODEL incompatible cells (5 × ~5-line strings) — actor-appropriate direction per Condition 3; each cites v3 §-anchor. Ratified as caller-facing action strings.

*B. license_classes.v0.json (~34 discretionary lines):*
* Entire file content — illustrative Master Admin taxonomy per Ruling 8 verbatim: "Real names land as config swap when commercial reality names them, zero code change." Class names, commissioner mapping keys, feed_id mapping keys ALL illustrative. Ratified as Owner's Ruling 8 accepted-as-illustrative.

*C. license_class_selection.py (~25 discretionary lines):*
* L1-39 module docstring — Ruling 4 verbatim text is Owner-quoted; ~15 lines discretionary framing (imports, spec-authority cite, taxonomy-governance note). Ratified as Owner-quoted mandate-forced content.
* L94-101 `derive_license_class_from_commissioner` fallback semantic: return config's `default_class` for unmapped commissioners (rather than raise or return None). Ratified as honest default matching config schema.
* L104-115 `select_by_class` list-comprehension shape — pure-function no-mutation. Ratified as convention.

*D. admission_refusal_reasons.v1.json (~26 discretionary lines):*
* Three `notes` field strings for the 3 new reason codes — each cites its v3 anchor (§6.1.4, §6.1.6, §6.1.2) + names precedent pattern (Ruling 3 registry). Ratified as documentation for future audits.

*E. qualified_data.py (~60 discretionary lines):*
* L38-52 module docstring "Section 7 verdict — UNFROZEN plain payload" — Stage A verdict record; framing. Ratified as continuity record.
* L69-101 `QualifiedDataPayload` Field(description=) content — OpenAPI documentation. Ratified as caller-consumption doc.
* L138-146 `_row_to_pre_egress` field mapping choice — Ruling 3 governance keys (defensibility present); minimal-necessary-fields for outer_gate transform. Ratified as governance-necessary set.
* L200 `f"qd-run-{uuid.uuid4().hex[:12]}"` prefix — debug-identifiable within receipt.run_id. Ratified as convention.
* L240 `artifact_ref=LedgerArtifactRef(..., version="v2")` — points at ObjectiveRequest_v2 (not v0). Ratified as this dispatch's schema.

*F. admission_refusal.py MODIFIED (~40 discretionary lines):*
* Three emit-helpers × ~40 lines each — mostly mandate-forced by contract shape. Discretionary: (i) `off_menu_fact` string wording; (ii) `RuntimeError` guard-clause text on unregistered reason; (iii) `_REGISTRY_PATH` bump v0→v1. Ratified as actor-appropriate per Condition 3; docstring updated to reference v1.

*G. dispatch.py MODIFIED (~15 discretionary lines):*
* L279-297 grain-compat admission-time refusal branch placement (AFTER MODEL branch, BEFORE knowledge_artifact/callable_skill branches) — MODEL already refused; grain-compat applies to remaining forms. Ratified as v3 §6.1.4/§6.2.4/etc apply upstream.
* L358 warm+qualified_data short-circuit to `package_qualified_data` — Owner-scope-declared §6.1 live-path. Ratified as dispatch scope.

*H. routers/service_1.py MODIFIED (~5 discretionary lines):*
* L67 `isinstance(result, qualified_data_module.QualifiedDataPayload)` check position — no shape overlap with AdmissionRefusal, functional-equivalent order. Ratified as convention.
* OpenAPI `responses={200: {"description": ...}}` string content — documentation. Ratified.

*Tests (~17 discretionary):*
* Seed helper region/feed_id string choices (`mixed_region`, `wire_region`, etc.) — test isolation. Ratified.
* HTTP client `base_url="http://test"` — ASGITransport pattern lifted from Phase 2. Ratified.

**Total discretionary: ~252 lines / ~840 net-new code → discretionary ratio 0.30×.** Below 1.0× threshold; no ratify-rationale escalation.

---

## Section 8 — Registry v1 additive proof

**Diff v0.json → v1.json (structural):**

* v0 entries preserved verbatim: `{reason: "form_not_offerable", since_version: "v0", notes: ...}` — byte-identical in v1.
* v1 adds exactly 3 new codes, all with `since_version: "v1"`:
  * `grain_form_incompatible` (v3 §6.1.4 + §6.2.4 + §6.3.4 + §6.4.4)
  * `standard_below_admission_floor` (v3 §6.1.6)
  * `license_class_unavailable` (v3 §6.1.2)

**SHA-256 snapshots before + after:**

```
$ sha256sum tests/invariants/admission_refusal.contract_snapshot.json
99381316dc71bf8f97acb36706bdfb057cb14c2da9ef1d32639aa788d72d67fb  tests/invariants/admission_refusal.contract_snapshot.json

$ sha256sum services/service_1/admission_refusal_reasons.v0.json
81b56ddff72bedb8cc0f2111e3a03474080e9c7e268a780f4717275ae62f1a59  services/service_1/admission_refusal_reasons.v0.json

$ sha256sum contracts/admission_refusal.py
e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f  contracts/admission_refusal.py
```

All three SHAs identical to pre-Phase-4a-Stage-B baseline. The contract SOURCE unchanged, the snapshot unchanged, the v0 registry file unchanged.

Gate 11 `test_admission_refusal_registry_v1_extends_v0_additively` **PASSED**, cross-checking all three invariants.

---

## Section 9 — Substrate 9/9 GREEN + CI 434 + `make ci` PASSED + 5 governance seams closed

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
434 passed in 1.22s

$ cd /app && make ci
23 passed in 0.10s
G2a CI gate PASSED.
```

**5 governance seams grep-verified closed:**

| # | Seam | Grep target | Status |
|---|---|---|---|
| 1 | Mtafiti V3 overlay | `v3_thresholds=None` in `services/mtafiti/registry.py:66` | CLOSED |
| 2 | Targeta yield layer | `YieldThresholds \| None` default in `services/targeta/yield_layer.py:21` + `services/targeta/gate.py:42` | CLOSED |
| 3 | Northena retention window | `retention_window_days() -> Optional[int]` default `None` in `services/northena/ledger.py:53` | CLOSED |
| 4 | V2 cumulative-disclosure arm | `RMS_G6_K_ANONYMITY_THRESHOLD` / `RMS_G6_L_DIVERSITY_THRESHOLD` env-var-gated (unset in test env) | CLOSED |
| 5 | **§6.1 payload freeze — UNFROZEN by wire-shape gate (Ruling 3, 2026-07-03)** | `QualifiedDataPayload` UNFROZEN; Ruling 3 wire-shape LOAD-BEARING gate in `test_qualified_data_wire_shape_pins_governance_keys` | CLOSED (via gate) |

All 5 seams intact.

---

## Section 10 — Continuity updates

**`/app/memory/ORCHESTRATOR_CONTINUITY.md`** — updated:

* §0.1 Standing Owner Dispositions — gained 3 new dispositions:
  1. Registry-bump-additive-extension applied at Phase 4a Stage B (v0→v1 additively, 3 new codes; v0.json + contract snapshot byte-identical).
  2. §6.1 payload UNFROZEN by named wire-shape gate (Ruling 3, Phase 4a Stage B dispatch, 2026-07-03).
  3. License-class Phase 7 seam pre-committed in module docstring (Ruling 4, Phase 4a Stage B dispatch, 2026-07-03).
* §0.2 Plan Debts — 4a-absorbed items removed / marked RESOLVED:
  * §6.1 downgrade plan-debt → RESOLVED at Phase 4a Stage B close, 2026-07-04.
  * Phase 4 transform-variants plan-debt → split: 4a portion RESOLVED at Phase 4a Stage B; 4b portion (§6.2 + 18th freeze `ComposedConclusion_v0`) REMAINING.
  * Phase 7 wizard-side dispatch plan-debt → gained NEW Phase-7 license-class debt: wrap `derive_license_class_from_commissioner` as fallback arm.
* §2 Phase Ledger — Phase 4a Stage B row appended with full text (434 tests, ~120 lifted, ~840 net-new, ~7× overall / ~0.30× discretionary, zero new freezes, three additive reason codes, three rulings landed).
* §3 Live State — rewritten to reflect Phase 4a Stage B close.

**`/app/memory/PHASE_STATE.md`** — compact mirror updated to match.

**`/app/memory/PRD.md`** — Phase 4a Stage B row added; frozen-contract count confirmed at 17.

---

## Rulings on Receipt (per Owner's Ruling 1 XL flag posture)

* **Rule-2 counting:** ~840 code lines net-new / ~120 lifted → ~7× overall / ~0.30× discretionary-only. **-12% delta UNDER the ~950 band → no counting blowout, no restatement required per Owner Ruling 1 discharge condition.** XL flag on Phase 4 discharged as intended.
* **Zero freezes at 4a:** parity 17 → 17, mechanical parity invariant unbroken (3/3 tests green).
* **Zero touches to `services/outer_gate/*.py`:** SHA identity confirmed on all 3 files (Condition B3).
* **Zero touches to the 17 existing frozen contracts:** SHA identity confirmed on all 4 protected contracts (`objective_request.py`, `service_1_refusal.py`, `admission_refusal.py`, and structurally on `service.py` v0 orchestrator).
* **Zero touches to v0 routes/services:** 7-file SHA identity in Section 6 verified (Condition B4).
* **No `git push`.** Only local commits by the platform's checkpoint machinery.

---

**End of Phase 4a Stage B close report.** Owner rules on this close before Phase 4b dispatches.
