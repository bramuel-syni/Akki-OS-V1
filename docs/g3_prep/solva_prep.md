# Solva G3 prep — read-only sketch

**Source:** `/app/docs/mandates/RMS_Solva_Specification.md` (SHA-256 in `/app/docs/mandates/MANIFEST.md`). **Read now, act at G3.** No G3 code written this pass.
**Parent cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §23.
**Reconciliation:** `/app/docs/audits/substrate_drop_v1/solva_reconciliation.md` (Substrate-Drop v1, 2026-07-01).

## 1. Purpose (G3 role)

Solva is the **depth governor** — the "genuine judgment" layer that
walls **powerful, free reasoning** from **governed, mechanical assertion**
so claim laundering (strength-of-argument raising a class) is
unrepresentable-by-construction, not runtime-policed.

## 2. Two-faculty split (load-bearing G3 architecture)

### Reasoning faculty (FREE — five stages)

Judges the **quality of reasoning**; no governed artifact dictates its
output. Spec §8:

| # | Stage | One-line intent |
|---|---|---|
| 1 | **Frame** | Establishes the question + relevant slice of the Normalized tier |
| 2 | **Candidate** | Proposes units + compositions that could answer it |
| 3 | **Tension** | Surfaces contradiction / corroboration / retraction among candidates — never averages them away |
| 4 | **Probability** | Weighs candidates toward the best-supported conclusion |
| 5 | **Reflection** | Judges soundness + sufficiency; identifies load-bearing units; composes the conclusion |

### Assertion boundary (BOUND — one function)

Spec §10:

```python
conclusion_class(load_bearing_units) -> str
```

- **Accepts**: only the set of load-bearing units.
- **Does NOT accept**: reasoning confidence · evidence weight · strength-of-argument. Not-a-parameter is the guard.
- **Computation**: mechanical floor over the units' classes (`min` over `defensibility_class` enum: `non_factual < utterance < fact`).
- **Laundering**: unrepresentable-by-construction — the function's signature has no confidence input, so no technical path exists for reasoning strength to influence the output class.

**Build order at G3 (construction-as-guard property; spec §15.1):**
1. FIRST land the boundary `conclusion_class` at `services/solva_depth/assertion.py` with its narrow signature + `UnitRef` shape + snapshot invariant.
2. THEN reshape the five stages against it. Stages CAN produce whatever reasoning artifacts they need; the boundary rejects any attempt to pass confidence via signature — that path doesn't exist.

## 3. Read-only governed values (confirm-integration-points)

Every value Solva reads is confirmed against the actually-frozen contract in `/app`. Product Spec 2.1 §31 invariant #4 requires "the violation is unrepresentable, not merely disallowed" — read-only handles satisfy this.

| Integration point | Confirmation | Verdict |
|---|---|---|
| `defensibility_floor` from `ObjectiveRequest` | `contracts/objective_request.py` L81: `defensibility_floor: DefensibilityFloor = Field(default_factory=DefensibilityFloor)` — present and frozen (@v0) | **CONFIRMED** |
| `defensibility_class` enum | `contracts/five_rings.py` L62: `class DefensibilityClass(str, Enum)` — three values (`non_factual`, `utterance`, `fact`) frozen at G0 | **CONFIRMED** |
| Unit shape (`UnitRef`) | `contracts/five_rings.py::NormalizedUnit` carries `unit_id: str`; `UnitRef` will most naturally be `unit_id` (a str) or a Pydantic wrapper around it | **CONFIRMED as `unit_id: str`** |
| `QualificationMatrix` verdict (Matrix rule lookup) | `contracts/qualification_matrix/*` frozen; `matrix_rule_ref` field on `DefensibilityRing` already threads through | **CONFIRMED** |
| Stage record shape | `Sequence[StageRecord]` — new G3 contract, no in-pod ancestor | **PENDING G3** (new frozen contract at G3) |
| Trace shape `SolvaTrace` | New G3 contract; joinable via `trace_id` into the Northena Ledger's `stamp_audit` field (already present on `LedgerRow`) | **PENDING G3** — Northena side already has the seam |

## 4. Trace-from-first-commit (spec §13)

Every extraction-time judgment MUST record:

- `trace_id` — joined to unit-level intelligence + three trace-lens surfaces at G5. Shape: `str` (matches `LedgerRow.trace_id`).
- `stages: Sequence[StageRecord]` — full sequence, including refusal paths.
- `load_bearing: list[UnitRef]` — units the conclusion rests upon (populated at Reflection).
- `computed_class: str` — the floor-computation result.
- `conclusion: Assertion` — final `Assertion(claim + class)` OR `Refusal(reason)`.

**Ledger absorption at G3**: the Northena `LedgerRow.stamp_audit` field is `Optional[Dict]` and already accepts a free-form audit blob. Solva's `SolvaTrace` serializes into that field via a small `services/northena/ledger.py::absorb_solva_trace` helper — mirrors the existing `absorb_stamp_audit` swap-in. **No Northena contract change required** — the seam exists.

## 5. G3 module layout (spec §7 — canonical, per Substrate-Drop v1)

**Substrate state as of 2026-07-01**: `/reference/akki-legacy/` unreachable (settled directive norm #8). G3 Solva reshape is spec-forced; transitive lifts via in-pod intermediates where structurally honest.

Spec §7 canonical layout:

```
services/solva_depth/
  reasoning.py       # the 5 stages: frame/candidate/tension/probability/reflection
  load_bearing.py    # identifies load-bearing units (a reasoning judgment)
  assertion.py       # computes defensibility class = floor over load-bearing
  enforce.py         # applies the floor from the Objective Request; refuses
  stamp.py           # Ring 5 emission at convergence
  trace.py           # records path + load-bearing + class + conclusion
  interfaces.py      # opaque handles (MatrixHandle, FloorSpec) — read-only
contracts/
  solva_trace.py     # frozen: SolvaTrace + StageRecord + Assertion + Refusal
routers/
  solva.py           # enforcement + trace read surfaces
```

Lift manifest expectation per module:

| Module | Expected `lift_kind` | Cousin / chain candidate |
|---|---|---|
| `services/solva_depth/assertion.py` | `mandate-forced-net-new` | Spec §10 — signature discipline is spec's construction-as-guard property |
| `services/solva_depth/reasoning.py` | `mandate-forced-net-new` | Spec §8 — free reasoning stages, no in-pod ancestor |
| `services/solva_depth/load_bearing.py` | `mandate-forced-net-new` | Spec §9 — reasoning judgment, no cousin |
| `services/solva_depth/enforce.py` | `mandate-forced-net-new` | Spec §11 — floor + Matrix read-only, refuse-below-floor |
| `services/solva_depth/stamp.py` | `transitive` | via `services/g1_defensibility/ring5_stamper.py` (Ring 5 emission already present at G1) |
| `services/solva_depth/trace.py` | `mandate-forced-net-new` | Spec §13 — trace-from-first-commit forced |
| `services/solva_depth/interfaces.py` | `transitive` | via `contracts/objective_request.py` (FloorSpec read shape) + `contracts/qualification_matrix/loader.py` (opaque handle pattern) |
| `contracts/solva_trace.py` (`SolvaTrace` + `StageRecord` + `Assertion` + `Refusal`) | `mandate-forced-net-new` | Spec §7 + §13 force contract shape; freeze-discipline reused from `northena_ledger.py` |
| `services/northena/ledger.py::absorb_solva_trace` (append to existing file) | `transitive` | via existing `absorb_stamp_audit` swap-in (same shape) |
| `routers/solva.py` (`/api/solva/trace/{trace_id}`, enforcement status) | `transitive` | via `routers/northena.py` + `routers/contracts.py` |

**Note on existing `services/solva_depth/admit_assist.py`**: G2a placed this file as the Northena-side Solva admit-assist shim. Spec §7 does NOT list it in Solva's canonical layout — the shim's Protocol formalism (currently `SolvaAdmitAssistProtocol`) folds into `services/solva_depth/interfaces.py` at G3 restructure. Not a contradiction; a scheduled reshape.

**Rule 2 expectation for G3**: heaviest reshape of the build (five stages net-new + boundary + trace contract + Ledger absorption helper). Overall net-new will likely > lifted; **discretionary-only** target stays ≤ 2× lifted after Rule-2 STOP-and-shrink discipline (same pattern as G2a).

## 6. Nine binding invariants (spec §17)

Spec §17 lists **9 binding invariants** (the substrate-drop canonical count, corrected from the pre-drop "12" figure which conflated stages with invariants).

| # | Invariant | G3 landing shape |
|---|---|---|
| 1 | Solva reasons; never extracts; issues operations + interprets results | Stages 1–4 call operator primitives; Reflection interprets. Import assertion: no Akki-primitive execution inside Solva modules. |
| 2 | Two faculties (free reasoning + bound assertion) with one-way seam | Boundary at `assertion.py`; reasoning at `reasoning.py`. Dependency rule enforced by import assertion: `assertion.py` does not import from `reasoning.py`; `reasoning.py` does not import from `assertion.py`. |
| 3 | Class = floor over load-bearing units' classes; reasoning strength not an input | `conclusion_class(load_bearing_units) -> str` — signature has no confidence param. `test_class_takes_no_confidence` asserts via signature-inspection. |
| 4 | Utterance-class asserted as "was stated", never as fact | `Assertion` shape distinguishes claim + class; utterance path stamped as `'X was stated'`. |
| 5 | Solva identifies load-bearing units; does not choose their class | Stage 5 (Reflection) identifies load_bearing; boundary computes class from their pre-existing classes. |
| 6 | Floor + Matrix verdict read-only to Solva | `FloorSpec` + `MatrixHandle` in `interfaces.py` — read-only. No mutation. |
| 7 | Below-floor conclusion refused with structured reason | `enforce.py::enforce(...)` returns `Refusal(reason='below_defensibility_floor', computed_class, floor)`. |
| 8 | Every extraction-time judgment produces a trace | `SolvaTrace` frozen contract at G3. Absorbed into Northena Ledger via `absorb_solva_trace`. |
| 9 | Solva governs depth only; three axes never collapsed | Import assertion for cross-governor boundaries; extends N-INV-11 orthogonality grep. |

## 7. Test obligations (spec §14 — 7 tests)

At G3 dispatch, land all 7 spec-named tests:

1. `test_class_is_floor_over_load_bearing` — `conclusion_class` returns min class among load-bearing units.
2. `test_class_takes_no_confidence` — signature-inspection: no confidence/strength parameter.
3. `test_utterance_never_asserted_as_fact` — utterance-class conclusion phrased 'was stated', never fact, regardless of evidence weight.
4. `test_refuse_below_floor` — below-floor conclusion refused with structured reason.
5. `test_solva_reads_governed_values_readonly` — enforce/assertion never mutate the floor or Matrix (read-only handle assertion).
6. `test_solva_never_extracts` — Solva issues operations to Akki, never runs operator primitive itself.
7. `test_trace_records_load_bearing_and_class` — every extraction-time judgment produces trace carrying load-bearing + computed class.

## 8. Governance — no items pending (spec §18)

Spec §18: *"No design decision in this mandate is left open."* Reasoning method is a build-time choice bounded by the invariants; no owner or DPO decision blocks Solva.

`OPEN_GOVERNANCE.md` records Solva has NO owner/DPO decisions pending.

## 9. G3 dispatch acceptance sketch (for stakeholder to shape when G3 opens)

- Assertion boundary `assertion.py::conclusion_class` lands FIRST (construction-as-guard property held — spec §15.1).
- Five stages reshape at `reasoning.py` against the boundary; each emits `StageRecord` entries.
- `load_bearing.py` extracts the reasoning-judgment portion of Reflection.
- `enforce.py` applies floor read-only; refuses below floor.
- `stamp.py` emits Ring 5 at convergence.
- `trace.py` writes `SolvaTrace` (frozen contract snapshot + invariant test).
- `interfaces.py` gates opaque `MatrixHandle` + `FloorSpec`.
- `absorb_solva_trace` helper appended to `services/northena/ledger.py`.
- 9/9 Solva invariants covered; 7 spec-named tests land.
- Rule 2 STOP-and-shrink if net-new > lifted overall; discretionary target ≤ 2×.
- Lift manifest gains ~9-10 new entries; every one grep-verifiable per Conditions 1 & 2.
- Substrate-drop-gate check step 0 (Substrate-Drop v1 institutionalisation) — REQUIRED specs present + SHA-256 match in `MANIFEST.md`.
- No governance surface (per §18).
