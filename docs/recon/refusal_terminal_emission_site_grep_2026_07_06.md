# Refusal-terminal ledger-row emission site grep — 2026-07-06

**Trigger:** Owner ruling (3) — verification gate before LB gate parametrisation and before Amendment F brief correction. Read-only pass. Ruling language governs; census gets verified against it.

**Definition applied (from E1.γ.1 + `contracts/northena_ledger_v1.py`):**

> A **refusal-terminal ledger-row emission** is any production code site (excluding `/app/backend/tests/`) that constructs or persists a `LedgerRow` / `NorthenaLedgerRow_v1` whose `decision` field equals `"refused"`. The frozen contract's `_ALLOWED_V1` map admits `"refused"` only under `stage ∈ {"admit", "gate"}`. `terminate_cancelled` is cancellation-family per Standing Disposition cancellation-is-a-state-not-a-refusal and is **excluded** from refusal-terminal.

## §1. Grep patterns executed

1. Direct `LedgerRow(` / `NorthenaLedgerRow_v1(` constructor + `decision="refused"` (or single-quoted) — line-adjacent grep in `/app/backend/` excluding `tests/` and `__pycache__/`.
2. Every writer of `NORTHENA_LEDGER_COLLECTION` (both `ledger_record(row)` funnel + direct `db[NORTHENA_LEDGER_COLLECTION].insert_one(...)`) — verified each writer's `decision=` context.
3. Reachability chase — every construct-site's containing function, then callers of that function, then callers of those callers, terminating at either a live HTTP router or a dead-code apex.
4. Cross-check `except`/`isinstance` branches for `Service1Refusal`, `ComposedService1Refusal`, `AdmissionRefusal_v0` — surface raise/handle sites that would need instrumentation (distinct from current construct sites).

## §2. Ground-truth: refusal-terminal ledger-row CONSTRUCTOR sites (grep result)

Grep patterns collapsed to **six** production code sites that construct a `LedgerRow` with `decision="refused"`. All six enumerated below with reachability + family classification.

| # | File : line | Function | `stage` | `reason` (verbatim / templated) | Family under `refusal_family_classifier.classify_family()` | Currently reachable from a live HTTP route? | Notes |
|---|---|---|---|---|---|---|---|
| C1 | `services/northena/converge.py:139-147` | `absorb_v2_refusal` | `gate` | `f"v2_refused:{reason_code}"` | `outer_gate_refusals` (prefix match) | **NO** — only importers are `system_state.py` (docstring), `refusal_family_classifier.py` (docstring), self. Zero call-sites. | Plan item 8. Currently constructs `stamp_audit={"v2_refusal": refusal_dict}` — augmentation would add the pinned key. |
| C2 | `services/northena/gate.py:31-36` | `route()` refusal branch | `gate` | `"out_of_scope"` | `unclassified` (no registry match) | **NO** — only caller is `state_machine.run_service1_linear` which has zero production callers. | **Site the plan MISSED.** Reason `out_of_scope` is not in `admission_refusal_reasons.v3.json`, not in `service_1_refusal_reasons.v0.json`, no `v2_refused:` prefix. Under current classifier it falls to `unclassified`. |
| C3 | `services/northena/admit.py:155-165` | `_refuse` | `admit` | caller-supplied (`val.refusal_reason()` from validation, `"scope_unresolved"` from unresolved scope) | Depends on `reason`. `scope_unresolved` → `unclassified`. Validation reasons may or may not be in `admission_refusal_reasons.v3.json` — depends on `_validate_completeness`. Grep of that helper is out of scope of this pass. | **NO** — only caller is `compile_and_freeze` whose only caller is `state_machine.run_service1_linear` (zero production callers). | Plan item 7. Currently `stamp_audit=None`. |
| C4 | `services/service_1/async_state.py:245-253` | `emit_ledger_terminate_refused` | `admit` | caller-supplied | Depends on caller. Zero production callers. | **NO** — dead stub. Build brief §3 E4 ruling: docstring migration only, body byte-identical (BC preserved). | This is the site the E4 ruling explicitly names as dead-stub. Not in plan's 8-item list because it's the pre-Sub-stage-1 baseline. Currently `stamp_audit=None`. |
| C5 | `services/compliance/refusal_ledger.py:118-128` | `emit_refusal_ledger_row` (Sub-stage-1 canonical writer) | `admit` **or** `gate` (caller-supplied; runtime-checked; rejects `converge`) | caller-supplied | Depends on caller; constructor requires `family ∈ VALID_REFUSAL_FAMILIES` (`refusal_families.v0.json`). | **Not yet.** Zero callers today; will be invoked from wire-up sites after Sub-stage 1 execution. | The single canonical writer being landed at Sub-stage 1. Pins `stamp_audit["refusal_family"] = family` at line 110-116. |
| C6 | `services/northena/ledger.py:95-109` | `absorb_stamp_audit` (refuse branch: `entry_decision == "refuse"` → `ledger_decision = "refused"`) | `admit` or `gate` (caller-supplied) | caller-supplied `reason` (default `"stamp_audit_absorbed"`) | Depends on caller-supplied reason. Under default reason `"stamp_audit_absorbed"` → `unclassified`. | **NO** — grep of non-self, non-docstring, non-test callers returned zero. Only `routers/northena.py:4` mentions the name in a docstring header. Dead helper. | **Site the plan MISSED.** G2 swap-in helper described in `services/northena/ledger.py:78-84`. Its refusal-branch construct would produce a `decision="refused"` row today if any caller invoked it. |

**Grep-confirmed exhaustive count of refusal-terminal LEDGER-ROW CONSTRUCTOR sites: N = 6** (C1–C6 above).

Of these six: **1 is the canonical Sub-stage-1 writer (C5)**. **2 are documented in the plan (C1 absorb_v2_refusal, C3 admit._refuse)**. **1 is documented in the brief as the dead-stub migration target (C4 emit_ledger_terminate_refused)**. **2 are grep-surfaced sites the plan and brief did NOT enumerate (C2 gate.route refusal branch, C6 absorb_stamp_audit refuse branch)**.

Of these six: **0 are reachable from a live HTTP route today.** All six construct sites are inside functions whose call graphs terminate at dead-code apexes (`state_machine.run_service1_linear` — zero non-test callers; standalone helpers — zero non-self, non-docstring callers).

## §3. Refusal-terminal INSTRUMENTATION sites the plan enumerates as needing wire-up (raise/handle-line granular)

These are distinct from §2 construct sites — they are `raise`/`except`/`isinstance` branches where refusal is currently surfaced to the API caller **without** a ledger-row write today. Wire-up = adding a call to `emit_refusal_ledger_row` (C5) at each site.

| # | File : line | Kind | Reason literal | Family under `refusal_family_classifier.classify_family()` | Currently reachable from a live HTTP route? |
|---|---|---|---|---|---|
| I1 | `services/service_1/service.py:127` | `raise Service1Refusal("no_defensibility_floor", ...)` | `"no_defensibility_floor"` | `composition_below_floor` (in `SERVICE_1_REASONS`) | **YES** — via `POST /api/service_1/run` at `routers/service_1.py:116`. |
| I2 | `services/service_1/service.py:135` | `raise Service1Refusal("no_lawful_basis", ...)` | `"no_lawful_basis"` | `composition_below_floor` (in `SERVICE_1_REASONS`) | **YES** — same router entry point as I1. |
| I3 | `services/service_1/service.py:188` | `raise Service1Refusal("composition_below_floor", ...)` | `"composition_below_floor"` | `composition_below_floor` (in `SERVICE_1_REASONS`) | **YES** — same router entry point. |
| I4 | `services/service_1/composed_conclusion.py:273` | `raise Service1Refusal("composition_below_floor", ...)` | `"composition_below_floor"` | `composition_below_floor` | **YES** — via `POST /api/service_1/v2/dispatch` at `routers/service_1.py:269` (async composition path also reaches this via `async_worker._dispatch_objective → package_composed_conclusion`). |
| I5 | `services/service_1/async_worker.py:97-113` | `except ComposedService1Refusal as e:` — currently emits envelope + calls `async_state.transition_to_refused` + fires webhook; does NOT write to `NORTHENA_LEDGER_COLLECTION`. | `e.reason` (dynamic; `"composition_below_floor"` given upstream) | `composition_below_floor` | **YES** — via async worker consuming `POST /api/objectives` queue. |
| I6 | `services/service_1/async_worker.py:129-137` | `if isinstance(result, AdmissionRefusal_v0):` — currently emits envelope + calls `async_state.transition_to_refused` + fires webhook; does NOT write to `NORTHENA_LEDGER_COLLECTION`. | `result.reason` (dynamic; one of `admission_refusal_reasons.v3.json`) | `admission_refusals` | **YES** — same async worker path. |

**Plan's raise/handle-line-granular instrumentation count: I = 6** (I1–I6).

## §4. Comparison — plan's 8-item list vs. grep's construct + instrumentation ground truth

The plan enumerates 8 items (labelled 1–8 in the ask_human question). Mapping:

| Plan item | Corresponds to | Grep concordance |
|---|---|---|
| 1. `service_1/service.py:127` | I1 (instrumentation) | Confirmed — un-ledgered raise site. |
| 2. `service_1/service.py:135` | I2 (instrumentation) | Confirmed. |
| 3. `service_1/service.py:188` | I3 (instrumentation) | Confirmed. |
| 4. `composed_conclusion.py:273` | I4 (instrumentation) | Confirmed. |
| 5. `async_worker.py:97-108` | I5 (instrumentation) | Confirmed. Exact range is 97-113 (through the `return` after webhook fire), but semantically one instrumentation point. |
| 6. `async_worker.py:129-131` | I6 (instrumentation) | Confirmed. Exact range is 129-137. |
| 7. `northena/admit.py::_refuse` | C3 (construct) | Confirmed — but grep flags it as unreachable from live routes today (only caller chain terminates at dead `run_service1_linear`). |
| 8. `northena/converge.py::absorb_v2_refusal` | C1 (construct) | Confirmed — same dead-code observation as item 7. |

**Not present in plan's 8-item list (grep-surfaced):**

- **C2 — `services/northena/gate.py:31-36` refusal branch** (`out_of_scope`). Constructs a `decision="refused"` row. Unreachable from live routes today (dead via `state_machine.run_service1_linear`). Under current `refusal_family_classifier.classify_family("out_of_scope")` this would map to `unclassified` — no registry family covers `out_of_scope` as a reason string.
- **C4 — `services/service_1/async_state.py:245-253` `emit_ledger_terminate_refused`** stub. Documented in the build brief §3 E4 ruling as the dead-stub migration target (docstring migration only, body byte-identical). Not in the plan's 8-item list because the brief scopes it separately.
- **C6 — `services/northena/ledger.py:95-109` `absorb_stamp_audit` refuse branch**. Zero live callers. Would produce a `decision="refused"` row if invoked with an `entry.decision == "refuse"` stamp. Under default `reason="stamp_audit_absorbed"` this classifies as `unclassified`.

## §5. Relation of plan's 8-item to grep's 6 constructors

The plan's 8 items and grep's 6 constructors are **complementary sets, not competing counts**:

- The **grep result** is a count of code sites that currently construct `LedgerRow(decision="refused")`. That count is **6** (C1–C6).
- The **plan's 8 items** enumerate the union of {*construct sites needing augmentation*} ∪ {*raise/handle sites needing instrumentation*}. That count is **8** (I1–I6 + C1 + C3).

They intersect at **C1 = plan item 8** and **C3 = plan item 7**. They differ because:

- **Plan is missing C2 (`gate.py::route`) and C6 (`ledger.py::absorb_stamp_audit`)** as constructor sites.
- **Plan is missing C4 (`emit_ledger_terminate_refused`)** as a distinct entry, but the build brief §3 E4 ruling names it as the dead-stub migration target (docstring only). If C4 is treated as "covered by E4," this omission is intentional; the LB gate must still not permit family-less rows from C4 if any future caller resurrects it.
- **Plan lists I1–I6** which are not in the grep-constructor set because they do not construct ledger rows today — they raise/handle exceptions.

**Neither "6" nor "8" as a total-emission-point count is exhaustive without qualification:**

- Total distinct code sites that CONSTRUCT a `decision="refused"` row today: **6** (C1–C6).
- Total distinct code sites that RAISE/HANDLE a refusal exception whose emission should land a `decision="refused"` row after Sub-stage-1 wire-up: **6** (I1–I6).
- Total distinct "refusal-terminal emission points" if BOTH kinds of sites are counted: **12** (C1 + C2 + C3 + C4 + C6 + I1..I6). C5 excluded because it is the canonical writer being landed, not an emission point that carries the LB gate obligation independently.
- Reachable from live HTTP routes today: **6** (I1–I6 only). C1, C2, C3, C4, C6 are all dead-code paths under current router surface wiring.

## §6. Ambiguity flags

- **C2 (`gate.py::route` refusal branch)** — reason `out_of_scope` has no home in any registered refusal family. Wire-up requires either (a) adding `out_of_scope` as a reason under an existing family (likely `admission_refusals` since gate is stage-gate but "out of frozen scope" is admission-adjacent), (b) creating a new family (`outer_gate_refusals` might absorb it, but the family's docstring anchors it to V2 gate refusals with `v2_refused:` prefix), or (c) accepting `unclassified` classification with the honesty banner. **Owner ruling needed** on which route.
- **C3 (`admit.py::_refuse`) reason `"scope_unresolved"`** — not in `admission_refusal_reasons.v3.json` and not in `service_1_refusal_reasons.v0.json`. Under current classifier → `unclassified`. Owner ruling needed on whether to extend the registry (bump v3 → v4 additive) or accept `unclassified` for the dead-code path.
- **C3 reason via `val.refusal_reason()`** — not verified in this grep pass; depends on the `_validate_completeness` helper. If it emits any reason not in the two reason registries, same `unclassified` outcome. **Ambiguity flag** to lift in a follow-on grep pass, or accepted-as-latent since the entire code path is unreachable.
- **Registry JSON governance-note mismatch** — `refusal_families.v0.json:8-10` says `admission_refusals` covers "services/service_1/service.py sync raises for no_defensibility_floor / no_lawful_basis". But those reasons live in `service_1_refusal_reasons.v0.json`, and the classifier maps them to `composition_below_floor` (line 107-108). The registry JSON's family-attribution note and the classifier's deterministic mapping **conflict** for those two reasons. Owner ruling needed on which authority governs — the registry attribution note or the classifier's reason-set membership.
- **I5/I6 emission timing** — wire-up in `async_worker._process_one` needs to occur BEFORE `async_state.transition_to_refused` (so the ledger row lands even if state-transition fails) or AFTER (so the row corresponds to a state that actually flipped)? Owner ruling likely already anchored somewhere in the doctrine; not lifted in this pass.

## §7. Recommended LB gate parametrisation

Owner's binding language: *"the gate covers what grep finds, not what the plan listed."*

Under a strict reading, the LB gate `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit` should assert the invariant on **every row in `NORTHENA_LEDGER_COLLECTION` where `decision="refused"`** — data-shape invariant, not static enumeration. This is the honest correctness gate.

**Two candidate parametrisation strategies:**

**Strategy A — data-shape invariant (recommended):**
- One test that scans the entire ledger post-run and asserts every `decision="refused"` row has `stamp_audit` shaped `{"refusal_family": <str>, ...}` with the family value in `refusal_families.v0.json::valid_families`.
- Parametrised over **exercise fixtures** that generate rows through each I1–I6 wire-up path (6 fixtures). Plus one aggregate-regression fixture that runs the coverage-marker query and asserts the resulting `RefusalsCoverageResponse` sees the expected families.
- Total: **6 exercise + 1 aggregate = 7 cases**.
- Rationale: matches the Owner's "gate covers what grep finds" language because the gate itself is the invariant, and grep governs the fixture roster.
- Does **not** exercise C1, C2, C3, C4, C6 in fixtures because those paths are dead code — no live HTTP entry point reaches them under Sub-stage 1 scope. If a future phase resurrects any of them, the same data-shape invariant will fire on the resurrected path's ledger row.

**Strategy B — per-construct-site + per-instrumentation-site parametrisation:**
- 6 fixtures for I1–I6 (instrumentation sites) + 5 fixtures for C1–C4, C6 (construct sites; C5 excluded as canonical writer). = **11 exercise cases + 1 aggregate = 12 total**.
- Rationale: strict enumeration of every code path that could ever produce a `decision="refused"` row.
- Cost: C1, C2, C3, C4, C6 have no live entry points, so fixtures for those must construct rows in-place via unit-test scaffolding — the fixture body reaches into the private helper directly, which is coupling the test to internal shape.

**Recommended: Strategy A.** The gate's honesty comes from data-shape invariance, not from enumeration completeness. Enumeration governs the fixture roster; the gate itself is a query over `NORTHENA_LEDGER_COLLECTION`.

If Owner prefers Strategy B, add explicit test cases for C1, C2, C3, C4, C6 — each constructs a row via the module's function (or directly if the function is not straightforwardly callable) and asserts the LB invariant.

**Owner ruling required** on:
- Strategy A vs Strategy B for LB gate parametrisation.
- Whether the plan's 8-item list should be amended to include C2 (`gate.py::route` refusal branch, reason `out_of_scope`) and C6 (`absorb_stamp_audit` refuse branch) as augmentation targets, or whether their dead-code status defers them to a future phase.
- Family attribution for `out_of_scope` (C2) and `scope_unresolved` (C3) reasons — extend registry, or accept `unclassified`?
- Registry-JSON governance-note vs. classifier-code conflict on `no_defensibility_floor` / `no_lawful_basis` family attribution (§6 above).

## §8. Honest self-audit of grep methodology

- **Coverage:** all `.py` files under `/app/backend/` excluding `tests/` and `__pycache__/`. Both `contracts/`-side model definitions and every `services/`, `routers/` writer.
- **Patterns used:** direct `decision="refused"` (and single-quoted variant), all `LedgerRow(` / `NorthenaLedgerRow_v1(` constructor invocations with 15-line lookahead, all `NORTHENA_LEDGER_COLLECTION` references, all callers of `absorb_v2_refusal` / `_refuse` / `emit_ledger_terminate_refused` / `absorb_stamp_audit`.
- **What a stricter methodology would catch that this pass may have missed:**
  1. **Dynamic decision-value assignment** — e.g. `LedgerRow(decision=some_var, ...)` where `some_var` could be `"refused"` at runtime but the string literal never appears adjacent to the constructor. Grep for `LedgerRow(...decision=<identifier>...)` returned only `services/economics/instrumentation.py:156` and `services/northena/gate.py:46` — both verified: economics uses `_EVENT_DECISION_MAP` (no "refused" value); gate.py uses `decision, reason = "warm", ...` / `"fresh", ...` (never `"refused"`).
  2. **Refusal rows written by test fixtures or seed scripts** — deliberately out-of-scope per §1 definition (test emission is not production emission), but if any dev-only seed script writes refusal rows into a shared dev DB, the LB gate would fire on them. Not verified this pass.
  3. **Rows written via alternative collection names** — grep constrained to `NORTHENA_LEDGER_COLLECTION`. Any dev-only alt-collection writer would be missed. Not expected to exist per the frozen collection-name discipline in `contracts/northena_ledger.py:37-39`.
  4. **`refusal_row` variable-name pattern** — not grepped explicitly; sample check: `grep -rn "refusal_row\|refused_row" /app/backend/*.py services/ routers/` (would surface any variable-name-based writer). Recommended to verify before LB gate lands.
- **What was NOT grepped:** the `_validate_completeness` helper in `services/northena/admit.py` (its return-value branches govern C3's reason strings). Deliberately deferred — the entire C3 code path is unreachable, so its reason-set need not be enumerated for Sub-stage 1 LB gate scope.

## §9. Summary — reply-format numbers per Owner §4

- **Total refusal-terminal ledger-row CONSTRUCTOR sites (grep-exhaustive):** N = **6** (C1–C6).
- **Total refusal-terminal RAISE/HANDLE instrumentation sites needing wire-up under Sub-stage 1 scope (grep-exhaustive):** I = **6** (I1–I6).
- **Total distinct refusal-terminal emission points (constructor ∪ instrumentation, C5 canonical writer excluded):** 6 + 6 − 0 overlap = **12**. Of these, **6 are reachable from live HTTP routes today** (all I1–I6); the other 6 are dead-code paths (all C1–C6 except C5).
- **Plan's 8-item list vs. grep:** neither subset nor exact match. Plan covers 6 instrumentation sites (I1–I6) + 2 construct sites (C1, C3). Grep additionally surfaces **C2** (`gate.py::route` refusal branch) and **C6** (`absorb_stamp_audit` refuse branch) — both are dead code, both would produce family-less refusal rows if resurrected.
- **Recommended LB gate parametrisation:** Strategy A — data-shape invariant with 6 exercise fixtures (one per I1–I6) + 1 aggregate regression = **7 cases**. Ruling deferred to Owner if Strategy B (per-construct-site + per-instrumentation-site) is preferred — 11 exercise + 1 aggregate = 12 cases.
- **Surprises:** C2 (`gate.py::route` refusal branch) with reason `out_of_scope` — first-visible from this grep; no home in current registry families; would classify as `unclassified` today. C6 (`absorb_stamp_audit` refuse branch) — declared as G2 swap-in but has zero production callers; the refuse branch would produce a `decision="refused"` row under default reason `"stamp_audit_absorbed"` which is also `unclassified`.
- **Honest methodology caveats:** did not verify dynamic decision-var branches for `"refused"` (spot-checked negative in 2 candidate sites); did not enumerate `_validate_completeness` reason-set (C3's dead-code path); did not audit seed/dev-only scripts (out-of-scope per §1).
