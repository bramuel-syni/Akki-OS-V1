# Northena Conformance Audit — G2a-retrospective

**Reference:** consolidated Northena Mandate & Engineering Spec
(https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/aegtpka0_RMS_Northena_Mandate_and_Engineering_Spec.docx).

**Implementation-bound-to:** Northena Mandate v1.0
(`/app/docs/mandates/northena_v1.0.md`), G2a build 2026-07-01.

**Discipline (stakeholder framing):** *"This is the consolidated conformance
reference. G2a stays closed. Verify against it at leisure; a material gap is
journaled as a finding, not reworked without a gate."*

**Legend:** `MATCH` = implementation honours the spec. `MATERIAL_GAP` = spec
says X, implementation does Y that differs materially. `SPEC_EXPANSION` =
consolidated spec adds detail v1.0 mandate didn't have; implementation
predates the expansion, may or may not honour it.

## 1. Four stages (Admit / Gate / Converge / Ledger)

| Stage | Verdict | Evidence |
|---|---|---|
| Admit — compile raw intent → frozen immutable artifact; deterministic completeness/lawful-basis check; Solva invoked ONLY for resolution | **MATCH** | `services/northena/admit.py::compile_and_freeze` — validates completeness via `AdmitOffender+AdmitValidation`, freezes as `FrozenArtifact` (N-INV-4), delegates only scope/depth/floor to `SolvaAdmitAssistProtocol` |
| Gate — strict set-membership; ambiguity = fatal | **MATCH** | `services/northena/gate.py::gate_check` — pure `sub_objective ∈ scope` set-check; no inference; warm/fresh/refused triage |
| Converge — fixed thresholds only (done > budget > continue) | **MATCH** | `services/northena/converge.py` — threshold ladder; no learned stopping (N-INV-6) |
| Ledger — append-only, contract-grade, closes-before-run-complete | **MATCH** | `services/northena/ledger.py::record` — append-only insert; `contracts/northena_ledger.py` `LedgerRow` is contract-grade (frozen); N-INV-8 grep-guards against `update`/`delete` |

## 2. Binding invariants (spec: 11)

Spec renumbers as 1–11. Implementation renumbers as 1a/1b/2/4/5/6/7/8/9/10/11
(N-INV-3 covered by the frozen snapshot test). Semantic mapping:

| Spec # | Spec name | Impl marker | Verdict | Evidence |
|---|---|---|---|---|
| 1 | Determinism (no ML, behaviour from frozen artifacts) | N-INV-1a (grep-guard) + N-INV-1b (behavioural) | **MATCH** | `test_N_INV_1a_northena_no_ml_imports`, `test_N_INV_1b_northena_no_inference_behaviour` |
| 2 | Solva Opacity (opaque handles; never inspect internals) | Impl via `RegistryHandle = object` + `SolvaAdmitAssistProtocol`; only `admit.py` reaches into `services.solva_depth` (N-INV-11) | **MATCH** | `services/northena/state_machine.py` L23 `RegistryHandle = object`; `test_N_INV_11_governors_orthogonal` grep-guards. **Substrate-Drop v1 annotation (2026-07-01):** the new canonical `docs/mandates/northena.md` §7 declares a dedicated `interfaces.py` module for opaque handles; shipped code deleted that file at G2a-shrink and folded `RegistryHandle = object` into `state_machine.py`. Behavioural conformance preserved (opaque by construction); module layout differs. Restoration of `interfaces.py` is a G3-time reshape (see `docs/audits/substrate_drop_v1/northena_reconciliation.md` §6). Not CODE_IMPACT. |
| 3 | Mandatory Admission (exactly one frozen artifact + valid lawful_basis) | N-INV-2 | **MATCH** | `test_N_INV_2_admit_requires_lawful_basis` |
| 4 | Immutability (frozen artifacts don't change during run) | N-INV-4 + snapshot | **MATCH** | `test_N_INV_4_frozen_artifact_immutable` + `test_northena_ledger_row_v0` |
| 5 | Gate Strictness (pure set-check, no inference at runtime) | N-INV-5 | **MATCH** | `test_N_INV_5_gate_strict_set_membership` |
| 6 | Converge Sovereignty (fixed thresholds only) | N-INV-6 | **MATCH** | `test_N_INV_6_northena_owns_halt` |
| 7 | Ledger Completion (closed audit-grade entry per run) | N-INV-7 (via router `_open_runs`) | **MATCH** | `test_N_INV_7_open_runs_visible` — enforces "no run closes without closed ledger" |
| 8 | Contract Integrity (versioned, immutable, snapshot-guarded) | N-INV-8 + frozen snapshot | **MATCH** | `test_N_INV_8_ledger_is_append_only` + `northena_ledger_row.contract_snapshot.json` |
| 9 | Transparency (refusals logged, never dropped) | N-INV-9 | **MATCH** | `test_N_INV_9_refusals_written` |
| 10 | Defensibility Linkage (G2+ absorb stamp-audit by unit_id/trace_id) | N-INV-10 + `absorb_stamp_audit` | **MATCH** | `test_N_INV_10_stamp_audit_absorbed` + `services/northena/ledger.py::absorb_stamp_audit` |
| 11 | Separation of Axes (Northena direction only; boundaries to SyniSense/Solva) | N-INV-11 grep-guard | **MATCH** | `test_N_INV_11_governors_orthogonal` |

**Invariant count verdict: 11/11 MATCH.** Impl's 1a/1b decomposition is
enforcement-mechanism differentiation (grep vs behaviour) of spec invariant
#1; not a scope change.

## 3. Ledger row shape (`northena_ledger_row@v0`)

| Spec field | Impl field | Verdict |
|---|---|---|
| `run_id` (str) | `run_id: str` | MATCH |
| `trace_id` (str) | `trace_id: str` | MATCH |
| `stage` (Enum) | `stage: Literal["admit","gate","converge"]` | MATCH |
| `decision` (str) | `decision: Literal[...]` with stage-consistency validator | MATCH |
| `reason` (str) | `reason: str` | MATCH |
| `artifact_ref` (ArtifactRef) | `artifact_ref: LedgerArtifactRef` (frozen sub-model) | MATCH |
| `lawful_basis_ref` (str) | `lawful_basis_ref: str` | MATCH |
| `stamp_audit` (Optional[StampAudit]) | `stamp_audit: Optional[Dict]` | MATCH |
| `at` (ISO 8601) | `at: datetime` (serialised ISO) | MATCH |

**Rules verdict**: append-only + snapshot-guarded + closed-per-run: **MATCH**.

## 4. Solva assist-at-admit interface

| Spec — Solva decides | Impl | Verdict |
|---|---|---|
| Resolves ambiguous scopes | `SolvaAdmitAssistProtocol.resolve_scope(declared, registry) → List[str]` | MATCH |
| Sets preservation depth | `preservation_depth(hint) → str` | MATCH |
| Defines defensibility floor | `defensibility_floor(hint) → str` | MATCH |

| Spec — Northena freezes | Impl | Verdict |
|---|---|---|
| Presence/completeness checks | `_validate_completeness` in `admit.py` | MATCH |
| Final freeze (immutable for run) | `FrozenArtifact` (`__setitem__` raises `TypeError`) | MATCH |

## 5. Stamp-audit absorption path (§7.3-equivalent)

| Spec | Impl | Verdict |
|---|---|---|
| Occurs at Ledger stage, introduced at G2 | `services/northena/ledger.py::absorb_stamp_audit` — active | MATCH |
| Consumed via `unit_id` + `trace_id` | Function reads `entry["unit_id"]` + accepts `trace_id` parameter; row records both | MATCH |
| Separate envelopes for unit and audit | LedgerRow carries `stamp_audit` field as Optional[Dict]; unit envelope is the ring buffer at `services/g1_defensibility/stamp_audit.py`; wiring point is `absorb_stamp_audit` (G2 swap-in complete, real-material substitution parks on G2b) | MATCH |

## 6. Explicit spec-expansions (vs v1.0 mandate)

| Expansion | Impl status | Verdict |
|---|---|---|
| G2 build requirement: explicit stamp_audit absorption in Ledger | Implemented at G2a | **MATCH** (impl leads spec) |
| Import assertions: CI-level assertions no ML imports | Implemented as N-INV-1a grep-guard | **MATCH** |
| Protocol handles: `SolvaHandle` formalised as Python `Protocol` | Implemented as `SolvaAdmitAssistProtocol` + `RegistryHandle = object` opaque alias | **SPEC_EXPANSION — SATISFIED**. Spec names one shape `SolvaHandle`; impl uses `SolvaAdmitAssistProtocol` for the assist-interface + `RegistryHandle = object` for the registry pass-through. Semantics identical. Naming difference is documentation-level only; no code rework needed. **Substrate-Drop v1 annotation (2026-07-01):** the new canonical Solva spec §7 places `SolvaHandle` in Solva's own `interfaces.py` module (with `MatrixHandle`, `FloorSpec` alongside). The rename `SolvaAdmitAssistProtocol → SolvaHandle` + relocation lands at G3 restructure of `services/solva_depth/`. Not G2a rework; reaffirmed as G3-time obligation (see `docs/audits/substrate_drop_v1/solva_reconciliation.md` §7). |

## 7. Pending decisions (governance)

| Item | Owner | Impl status |
|---|---|---|
| Ledger retention duration + end-of-window logic | DPO | **PENDING** — `retention_mode()` reads env `RMS_NORTHENA_LEDGER_RETENTION_MODE` (default `indefinite`). Not a build-blocker. Logged in `/app/docs/g4_prep/OPEN_GOVERNANCE.md`. |

## Summary

- **MATCH: 20** (all 4 stages + 11 invariants + ledger row shape + solva-assist + stamp-audit path + 2 of 3 spec-expansions honour cleanly)
- **SPEC_EXPANSION honoured: 3** (all 3 consolidated-spec additions already implemented at G2a build)
- **MATERIAL_GAP: 0**
- **Pending governance: 1** (Ledger retention → DPO)

**Verdict**: G2a implementation conforms to the consolidated spec. No
rework required. Findings are journaled; retention decision remains
DPO-pending (unchanged since G2a build). **G2a stays formally closed.**
