# Service 1 v1 scope from source — G4 pre-code note

**Source:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §2.1 (Day Zero) + §24 (Mtafiti flow) + §25 (Targeta flow) + §26–§28 (Akki A→B→C).
**Cross-source:** `RMS_Interface_and_UX_Architecture.md` for API surface.

## 1. What Service 1 does (Product v2.1 §2.1)

**Day Zero: Estate Extraction.** Standing-up pass under a Portfolio Mandate. Sequence:

```
Portfolio Mandate  →  Mtafiti (census + defensibility measure)
                  →  Targeta (prioritise where to mine)
                  →  Akki A → B → Layer C (retrieve, perceive, converge)
                  →  Normalized tier populated
```

**Terminates at convergence.** Service 1 populates the Normalized tier; does NOT answer objectives (that's Service 2). Re-run when Mtafiti Registry materially changes (freshness).

## 2. End-to-end flow

At G4, the entities involved:

| Stage | Component | Owned by | Landing at G4 |
|---|---|---|---|
| Intake | Portfolio Mandate (an ArtifactRef) | governance | consumed from `ObjectiveRequest.governing_artifact_ref` or new `PortfolioMandate` contract |
| Census | Mtafiti `census.py` | Mtafiti | LIVE (G4 §2) |
| Defensibility measure | Mtafiti `measure.py` + `verdict.py` | Mtafiti | LIVE with baseline; V3 overlay DARK |
| Prioritise | Targeta `core.py` + `plan.py` | Targeta | LIVE with core arm; yield DARK |
| Retrieve | Layer A handlers | Akki | LIVE (G0) |
| Perceive | Layer B providers | Akki | LIVE (G0) |
| Converge | Layer C `aggregator.py` + G3 `convergence.py` | Akki | LIVE (G0.5, G3) |
| Ring 5 stamp | `services/g1_defensibility/ring5_stamper.py` | G1 | LIVE (G1); consults Mtafiti Registry at G4 |
| Trace | Northena Ledger | Northena | LIVE (G2a); G4 Service 1 writes stage='converge' rows via existing seams |

**Governing artifact for Service 1**: a Portfolio Mandate. Spec doesn't fully enumerate; frozen `objective_request@v0` is close (has defensibility_floor + scope). For G4, treat Service 1 as accepting an `ObjectiveRequest` (existing frozen contract) with mode='service_1_day_zero'. This avoids proliferating contracts. If a distinct `PortfolioMandate` contract lands post-G4, it's an addition.

## 3. API surface (Interface Spec cross-reference)

Two endpoints at minimum:

- `POST /api/service_1/run` — accepts `ObjectiveRequest` (Day-Zero framed), returns `Service1RunStarted { run_id, trace_id, mining_plan_id }`.
- `GET /api/service_1/run/{run_id}` — returns `Service1RunStatus { run_id, stage, mining_plan_id, registry_snapshot_ref, converged_unit_count, ledger_correlation_ref, defensibility_class }`.

Both must appear in `/api/openapi.json` per G2a discipline.

## 4. Composition-time obligations

Service 1's composition boundary re-asserts (defense-in-depth) — this mirrors Solva's `enforce()` at the depth boundary and Northena's `admit` at the run boundary.

1. **Defensibility floor re-assertion**: on run entry, verify `ObjectiveRequest.defensibility_floor` is set. If not, refuse (structured refusal, `reason='no_defensibility_floor'`).
2. **Registry snapshot pin**: on run entry, capture the current Mtafiti Registry snapshot id. All Targeta plans + Akki runs correlate to this snapshot. Reproducibility (Targeta §17 #8).
3. **Ledger correlation**: every stage transition writes a Ledger row keyed to the run_id + trace_id.
4. **Terminate at convergence**: the run halts at Layer C convergence. Does NOT invoke Solva reasoning (Solva is Service 2's boundary at Objective-Extraction time). Service 1 stamps Ring 5 at declaration baseline via G1 stamper + Mtafiti Registry.

## 5. Northena Ledger integration

Existing Northena Ledger row shape (`northena_ledger_row@v0`) supports `stage ∈ {admit, gate, converge}`. Service 1 writes:
- One `admit` row on run intake (governing artifact accepted; floor validated).
- One `gate` row on Targeta plan accepted (or refused).
- N `converge` rows for each Layer C convergence event.

No frozen-contract mutation.

## 6. New frozen contracts implied for Service 1

- **`Service1RunSummary`** — not a frozen contract (a response DTO shape). Lives at `contracts/service_1.py` as a Pydantic model, but does NOT need snapshot+invariant since it's a response envelope, not a governed artifact. (Same pattern as `NorthenaAdmitRequest` at G2a.)
- **Portfolio Mandate**: G4 reuses `ObjectiveRequest` framing; no new contract.

## 7. Invariants for Service 1

| # | Invariant | Test |
|---|---|---|
| 1 | Run refuses on missing defensibility_floor | `test_service_1_refuses_no_floor` |
| 2 | Run correlates all writes to run_id + trace_id | `test_service_1_ledger_correlation` |
| 3 | Run terminates at convergence (no Solva/Service-2 invocation) | `test_service_1_terminates_at_convergence` |
| 4 | Mining plan consulted (Targeta core arm invoked) | `test_service_1_calls_targeta_core` |
| 5 | Registry consulted (Mtafiti census/declaration invoked) | `test_service_1_calls_mtafiti` |
| 6 | Reproducible: same fixture + artifact → byte-identical plan_id + trace | `test_service_1_reproducible` |
| 7 | OpenAPI surface complete | `test_service_1_openapi_surface` |

## Ready-to-code checklist

- [x] Product v2.1 §-anchors mapped
- [x] End-to-end sequence enumerated
- [x] API routes defined (2 endpoints)
- [x] Composition-time floor re-assertion identified (mirrors Solva depth boundary)
- [x] Northena Ledger integration uses existing frozen row shape (no mutation)
- [x] Zero new frozen contracts required (Service1RunSummary is a response DTO)
- [x] 7 invariants mapped to tests
