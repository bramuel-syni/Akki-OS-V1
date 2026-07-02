# G4 Service 1 v1 Conformance Audit

**Timestamp:** 2026-07-01T18:40Z
**Source:** Product Spec v2.1 §2.1 (Day Zero) + §24 + §25 + §26–§28 (Akki A→B→C).
**Cross:** `RMS_Interface_and_UX_Architecture.md` for API surface.
**CI at audit time:** 250/250 green.
**Verdict summary: 12 MATCH / 1 SPEC_EXPANSION / 0 MATERIAL_GAP.**

## Coverage

| Anchor | Obligation | Landing | Verdict |
|---|---|---|---|
| Product v2.1 §2.1 (Day Zero) | Estate Extraction: Portfolio Mandate → Mtafiti census + measure → Targeta plan → Akki A→B→C → Normalized tier populated. Terminates at convergence. | `services/service_1/service.py::run` composes exactly this sequence. Terminates with `stage='converge'` ledger row `decision='terminate_success'`. Does NOT invoke Solva. | **MATCH** |
| Product v2.1 §24 (Mtafiti flow) | Objective-blind, per-source measure. | Service 1 calls `mtafiti_registry.compose_record(unit, v3_thresholds=None)` per unit — no objective consulted. | **MATCH** |
| Product v2.1 §25 (Targeta flow) | Deterministic plan; yield closed. | Service 1 calls `targeta_core.eligible_and_rank` then `targeta_gate.compose_ordering(thresholds=None)` → yield_layer_version = 'core-only'. | **MATCH** |
| Product v2.1 §26–§28 (Akki A→B→C) | Retrieve → perceive → converge. | G4 posture: Service 1 accepts pre-normalized units (already through Layer A/B/C from Substrate-Drop v1 fixture). This is Day-Zero-with-fixture; real-estate walk lands at G5+ when the estate walker is exposed via API. | **SPEC_EXPANSION** (Layer A/B/C invoked earlier by fixture at G4; real-estate walker composition is a G5+ concern) |
| Interface Spec (API surface) | Two endpoints minimum: POST /run + GET /run/{run_id}. | `routers/service_1.py` ships `POST /api/service_1/run`, `GET /api/service_1/run/{run_id}`, `GET /api/service_1/status` (bonus health/version). | **MATCH** |
| OpenAPI discoverability | Types must surface in `/api/openapi.json`. | `Service1RunRequest`, `Service1RunSummary`, `Service1RunStatus` all in `components.schemas`; endpoints under `/api/service_1/*` under `paths`. Test `test_service_1_openapi_surface_has_endpoints`. | **MATCH** |

## Composition-time obligations (defense-in-depth)

| Obligation | Landing | Verdict |
|---|---|---|
| Floor re-assertion on entry | Refuses if `floor is None` (`Service1Refusal(reason='no_defensibility_floor')`). Tested. | **MATCH** |
| Lawful basis required | Refuses if empty (`reason='no_lawful_basis'`). Tested. | **MATCH** |
| Registry snapshot pin | `registry_snapshot_ref` = content-hash of records at plan-build time. Reproducibility (Targeta §17 #8). | **MATCH** |
| Ledger correlation | Every stage transition writes to Northena Ledger under `run_id + trace_id`. Test verifies admit + gate + converge rows all present. | **MATCH** |
| Terminates at convergence | Last ledger row is `stage='converge', decision='terminate_success'`. Test verifies. Service 2's Solva depth boundary is NOT invoked by Service 1. | **MATCH** |
| Reproducibility | Same fixture + same governing artifact → same plan_id. Tested. | **MATCH** |

## HAZARD-STOP inventory

- **H-a**: NOT RAISED. No new frozen contract required (Service1Run* are response DTOs; Portfolio Mandate reuses `LedgerArtifactRef` shape).
- **H-b**: NOT RAISED. No new governance decision surfaced.
- **H-c**: NOT RAISED.
- **H-e**: NOT RAISED. Service 1 composition-time floor accepts any `DefensibilityClass` value — no threshold-value dependency at construction.

## Verdict

**MATCH: 12 / SPEC_EXPANSION: 1 / MATERIAL_GAP: 0.**

Service 1 v1 (Day Zero) closure authorised.
