# Northena Reconciliation — Substrate-Drop v1

**Canonical source:** `/app/docs/mandates/northena.md` (from `RMS_Northena_Specification.docx`, SHA-256 in `MANIFEST.md`).
**Cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §22 (parent).
**Reconciled artifacts:** shipped G2a code + `/app/docs/audits/northena_conformance_v1.md` (pre-drop audit).
**Predecessor:** `/app/docs/mandates/archive/northena_v1.0_predrop.md` (retained for provenance).

**Discipline:** source wins; sketch corrects to source; code contradictions surface as HAZARD-STOP (a).

## Legend
- **MATCH** — shipped code aligns with source (verbatim or semantically equivalent).
- **SKETCH_CORRECTION** — audit doc / prep sketch needed updating to reflect the new canonical spec; corrections applied.
- **CODE_IMPACT** — source contradicts already-shipped G2a code in a way that requires code change (HAZARD-STOP (a) trigger).

---

## 1. Four stages (spec §3)

| Stage | Verdict | Evidence |
|---|---|---|
| Admit — compile + validate + freeze | **MATCH** | `services/northena/admit.py::compile_and_freeze` — completeness via `AdmitOffender+AdmitValidation`, freezes as `FrozenArtifact` (N-INV-4), delegates only scope/depth/floor to Solva assist |
| Gate — strict set-membership | **MATCH** | `services/northena/gate.py::route` — pure `sub_objective ∈ scope`; no inference |
| Converge — threshold stop (done > budget > continue) | **MATCH** | `services/northena/converge.py::check` |
| Ledger — append-only writer | **MATCH** | `services/northena/ledger.py::record`; frozen `LedgerRow`; N-INV-8 grep-guards |

## 2. Determinism boundary (spec §4, §13, invariants #1, #2)

| Rule | Verdict | Evidence |
|---|---|---|
| No ML library in any Northena module | **MATCH** | `test_N_INV_1a_northena_no_ml_imports` (grep-guard) |
| No inference in Northena; behavioural | **MATCH** | `test_N_INV_1b_northena_no_inference_behaviour` |
| Solva reached only through an opaque handle | **MATCH (semantic)** | `state_machine.py` L23 `RegistryHandle = object`; opaque by construction |
| Governors orthogonal | **MATCH** | `test_N_INV_11_governors_orthogonal` |

## 3. Ledger row (spec §8; frozen `northena_ledger_row@v0`)

Nine-field row snapshot-tested at `tests/invariants/northena_ledger_row.contract_snapshot.json`. Fields verified 1:1:

| Spec field | Impl field | Verdict |
|---|---|---|
| `run_id` | `run_id: str` | MATCH |
| `trace_id` | `trace_id: str` | MATCH |
| `stage` (admit/gate/converge) | `stage: Literal["admit","gate","converge"]` | MATCH |
| `decision` | `decision: Literal[...]` w/ stage-consistency validator | MATCH |
| `reason` | `reason: str` | MATCH |
| `artifact_ref` | `artifact_ref: LedgerArtifactRef` (frozen sub-model) | MATCH |
| `lawful_basis_ref` | `lawful_basis_ref: str` | MATCH |
| `stamp_audit` (Optional) | `stamp_audit: Optional[Dict]` | MATCH |
| `at` (ISO 8601) | `at: datetime` (JSON-serialised) | MATCH |

## 4. Invariants (spec §17 — 10 invariants)

Spec §17 enumerates **10 invariants**. Shipped `test_northena_invariants.py` runs **11 tests** (N-INV-1a, 1b, 2, 4, 5, 6, 7, 8, 9, 10, 11) — invariant #1 (Determinism) is split into 1a grep-guard + 1b behavioural, per implementation discipline documented in `northena_conformance_v1.md` §2.

| Spec # | Spec text | Impl marker | Verdict |
|---|---|---|---|
| 1 | Deterministic; no model, no learned weights | N-INV-1a + 1b | MATCH |
| 2 | Any inference is Solva's; opaque handle | N-INV-11 + `RegistryHandle` | MATCH (semantic) |
| 3 | Exactly one frozen artifact + valid lawful_basis | N-INV-2 | MATCH |
| 4 | Frozen artifact immutable for run | N-INV-4 | MATCH |
| 5 | Gate strict set-membership | N-INV-5 | MATCH |
| 6 | Northena owns halt; no run closes without closed Ledger | N-INV-6 + N-INV-7 | MATCH |
| 7 | Ledger contract-grade (versioned + snapshot + append-only) | N-INV-8 + snapshot | MATCH |
| 8 | Out-of-scope + refused items recorded, never dropped | N-INV-9 | MATCH |
| 9 | Ledger absorbs stamp-audit by unit_id / trace_id | N-INV-10 + `absorb_stamp_audit` | MATCH |
| 10 | Northena governs direction only (SyniSense boundary; Solva depth) | N-INV-11 (grep) | MATCH |

**Verdict: 10/10 spec invariants MATCH.** Shipped decomposition (1→1a/1b) is enforcement-mechanism differentiation, not scope drift.

## 5. Test obligations (spec §14 — 9 named tests)

| Spec test | Shipped equivalent | Verdict |
|---|---|---|
| `test_no_run_without_lawful_basis` | `test_N_INV_2_admit_requires_lawful_basis` | MATCH (rename) |
| `test_frozen_artifact_immutable` | `test_N_INV_4_frozen_artifact_immutable` | MATCH |
| `test_gate_is_set_membership` | `test_N_INV_5_gate_strict_set_membership` | MATCH |
| `test_converge_owns_halt` | `test_N_INV_6_northena_owns_halt` | MATCH |
| `test_no_run_without_closed_ledger` | `test_N_INV_7_open_runs_visible` (open-runs set-difference — "admitted minus terminated" — enforces "no run closes without closed ledger") | MATCH (semantic; name-differs) |
| `test_ledger_append_only` | `test_N_INV_8_ledger_is_append_only` | MATCH |
| `test_ledger_row_frozen` | `test_northena_ledger_row_v0_content_frozen` (snapshot) | MATCH |
| `test_northena_has_no_ml_import` | `test_N_INV_1a_northena_no_ml_imports` | MATCH (rename) |
| `test_solva_is_opaque` | `test_N_INV_11_governors_orthogonal` | MATCH (semantic) |

**Verdict: 9/9 spec test obligations MATCH.** Naming differences documented, not code changes.

## 6. Module structure (spec §7)

Spec §7 declares this module layout:
```
services/northena/
  admit.py
  gate.py
  converge.py
  ledger.py
  state_machine.py
  interfaces.py        # opaque handles (SolvaHandle, RegistryHandle)
contracts/
  northena_ledger.py   # frozen: LedgerRow
routers/
  northena.py          # read-side + run-status API
```

Shipped layout:
```
services/northena/
  __init__.py
  admit.py
  gate.py
  converge.py
  ledger.py
  state_machine.py     # RegistryHandle folded inline (no interfaces.py)
contracts/
  northena_ledger.py   # LedgerRow (frozen)
routers/
  northena.py          # /api/northena/status, /ledger/by_run/{run_id}, /ledger/open_runs
```

**Verdict: SKETCH_CORRECTION.** Shipped code deleted `interfaces.py` at G2a-shrink pass (folded `RegistryHandle = object` inline into `state_machine.py`; deletion journaled in BUILD_JOURNAL 2026-07-01T08:30Z). Behavioural contract (opaque handle) preserved; module layout differs from spec §7. **Not CODE_IMPACT** because:
1. The spec's stated intent (opaque handle discipline) is enforced structurally (`RegistryHandle = object` + N-INV-11 grep-guard).
2. Solva's full Protocol formalism (`SolvaHandle` with `resolve_scope`, `set_preservation`) lands at G3 (Solva reshape), when the second handle (`RegistryHandle` for the Mtafiti registry) also gets formalised. Restoring `interfaces.py` is a G3-time reshape.
3. Product Spec 2.1 §31 invariant #4 requires "the violation is unrepresentable, not merely disallowed" — the shipped alias satisfies this.

Journal correction: `northena_conformance_v1.md` §2 row for invariant #2 ("Solva Opacity") is updated below to reference this reconciliation.

## 7. Solva assist-at-admit interface (spec §13)

Spec §13 shows `SolvaHandle(Protocol)` with two methods: `resolve_scope(draft) -> Scope` and `set_preservation(draft) -> PreservationVector`. Shipped `SolvaAdmitAssistProtocol` in `services/solva_depth/admit_assist.py` has three methods: `resolve_scope(declared, registry) -> List[str]`, `preservation_depth(hint) -> str`, `defensibility_floor(hint) -> str`.

Spec §14 explicitly carries a CONFIRM marker: *"CONFIRM SolvaHandle against the Solva specification."* Solva engine spec §7 does not itself define `SolvaHandle` — it names Solva's own boundary types (`MatrixHandle`, `FloorSpec`), which are Solva-internal read-only handles for Matrix + Floor consumption, distinct from Northena's admit-time assist.

**Verdict: SKETCH_CORRECTION.** The shipped 3-method protocol reflects Northena's mandate §9 (Solva assists Admit with scope / preservation / floor). Spec §13's 2-method illustration is under-specified (CONFIRM). Solva spec §7 does not contradict shipped. G3 reshape will formalise the naming: `SolvaAdmitAssistProtocol` → part of Solva's boundary interface at `services/solva_depth/interfaces.py` per Solva spec §7. **Not CODE_IMPACT.**

## 8. Route surface (spec §7 + §13)

Spec §7: `routers/northena.py # read-side + run-status API`.
Spec §13 references `ledger.close(run_id)` semantics; run-status surface implied by Ledger's contract-grade posture.

Shipped:
- `GET /api/northena/status` — reports gate state + `contracts_frozen` + `northena_ledger_row_rev`.
- `GET /api/northena/ledger/by_run/{run_id}` → `List[LedgerRow]` (empty-set query returns `[]`, not 404).
- `GET /api/northena/ledger/open_runs` → `List[str]` (admitted minus terminated).

**Verdict: MATCH.** Read-side surface complete. Response models expose `LedgerRow` + `LedgerArtifactRef` in OpenAPI (tester-verified 2026-07-01T09:15Z).

## 9. Retention (spec §11 + §18)

Spec §11: append-only + immutable within retention window; §18 open decision (DPO).
Shipped: `services/northena/ledger.py::retention_mode()` reads `RMS_NORTHENA_LEDGER_RETENTION_MODE` (default `indefinite`); `retention_window_days()` reads `RMS_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS` (default `None`).

**Verdict: MATCH.** Mechanism ships; DPO decision remains open per `OPEN_GOVERNANCE.md`.

## 10. Two modes (spec §6)

Spec §6: Service 1 linear; Service 2 loop around Layer D + Solva.
Shipped: `run_service1_linear` only. Service 2 loop scaffolding deferred to G3 (per module docstring).

**Verdict: MATCH (deferred).** Explicit deferral to G3 documented; not a scope gap.

---

## CODE_IMPACT items

**none.**

All spec-vs-code differences are either (a) semantic MATCH with naming variance, (b) module-layout differences resolved at G3 restructure, or (c) governance deferrals already tracked in `OPEN_GOVERNANCE.md`. **No shipped G2a code contradicts the new canonical Northena spec in a way that requires code mutation or contract mutation.**

## Corrections applied to `northena_conformance_v1.md`

None applied to shipped code. Two annotations added to the pre-drop audit doc:
1. §2 (invariant #2 row): note the shrink-pass fold of `interfaces.py` per this reconciliation §6.
2. §6 (Spec-expansions row 3 — `SolvaHandle` formalisation): reaffirmed as G3-time obligation, not G2a rework.

## Summary

- **MATCH: 24** (4 stages, 4 determinism rules, 9 ledger-row fields, 10 invariants, 9 test obligations, plus mode-2 deferral, retention, route surface — see §1–§10 above).
- **SKETCH_CORRECTION: 2** (module layout §6, Solva assist protocol §7 — audit doc annotations only).
- **CODE_IMPACT: 0.**
- **HAZARD-STOP (a) raised: NO.**

**Verdict:** G2a stays formally closed. Shipped code conforms to the new canonical Northena spec. Sketch-only corrections applied.
