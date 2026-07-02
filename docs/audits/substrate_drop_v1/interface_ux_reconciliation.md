# Interface + UX Reconciliation — Substrate-Drop v1

**Canonical sources:**
- `/app/docs/mandates/RMS_Interface_Specification.md` (SHA-256 in `MANIFEST.md`).
- `/app/docs/mandates/RMS_UX_Architecture_Specification.md` (SHA-256 in `MANIFEST.md`).

**Cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` (parent on conflict per both specs' front-matter).

**Reconciliation scope:**
- Currently-shipped `/api/*` routes against Interface Spec §11 response contract + §14 governance-record semantics.
- Planned G5a/G5b routes and surfaces against Interface + UX specs.
- No G5 prep sketches exist yet — mismatches are NOT sketch-corrections; they're recorded as TODOs for future G5-prep dispatches.

## Legend: as per Northena reconciliation.

## 1. Currently-shipped API routes vs Interface Spec

Full audit of shipped `/api/*` surface, cross-referenced against Interface Spec §10 (Developer Surface) + §11 (Response Contract) + §14 (Governance Surface).

### 1.1 `GET /api/system/state` (shipped)

**Interface Spec binding:** none (this is an internal/admin state endpoint, not part of the six declared user surfaces). Interface Spec §5–§15 enumerate user-facing surfaces; there is no Interface-Spec-declared shape for a system-state route. Route is admin-only.

**Verdict: NON-BINDING.** Not covered by Interface Spec. Retained for orchestrator + operator use.

### 1.2 `GET /api/contracts/{five_rings,objective_request,qualification_matrix,extraction_params}` (shipped)

**Interface Spec binding:** none. These are meta/self-descriptive endpoints returning the frozen JSON-Schema of the six contracts. Interface Spec §7–§14 describe user-facing intelligence surfaces; contract-schema endpoints are not user-facing under any of the six.

**Verdict: NON-BINDING.** Retained for engineering/DPO reference.

### 1.3 `GET /api/northena/status` (shipped)

**Interface Spec binding:** none directly. Approximate mapping to Operator Surface §13 "Governance: gate result changes / floor refused at rate" (planned for G5b, not shipped as a user-facing surface).

**Verdict: NON-BINDING.** Shipped as internal orchestrator status.

### 1.4 `GET /api/northena/ledger/by_run/{run_id}` (shipped)

**Interface Spec binding:** partial. Interface Spec §14 (Governance Surface) says: *"Any run is reachable by its trace_id, and the record shown is the same one the decision-maker's audit lens reaches; there is one record, seen at two scopes."*

- Shipped uses `run_id` as the URL parameter.
- Interface Spec § names `trace_id` as the addressing key.
- Frozen `LedgerRow` has BOTH fields (`run_id: str, trace_id: str` — see `contracts/northena_ledger.py`), and a single run may span multiple trace_ids in the Service-2 loop.

**Verdict: MATCH (dual-key coexistence).** The `by_run/{run_id}` endpoint remains valid for run-scope queries (open-runs bookkeeping, audit-trail-by-run). The Interface-Spec-declared `trace_id`-keyed endpoint is scheduled as **G5a-backlog** per BUILD_JOURNAL 2026-07-01T08:30Z: `GET /api/northena/trace/{trace_id}`. Both endpoints will coexist. **Not CODE_IMPACT.**

### 1.5 `GET /api/northena/ledger/open_runs` (shipped)

**Interface Spec binding:** none (bookkeeping surface). Approximate mapping to Operator Surface §13 exceptions ("open runs beyond retention window" would surface as a governance exception).

**Verdict: NON-BINDING.**

### 1.6 Planned G5a routes

Per BUILD_JOURNAL + ORCHESTRATOR_CONTINUITY §2, G5a is "backend routes: `/api/discipline/lift_manifest`, `/api/northena/trace/{trace_id}`, trace-lens correlation."

Interface Spec §11 (Response Contract) specifies the **integration surface's per-query response shape**:
```
{
  'trace_id': '…',
  'claim': '…',
  'defensibility': { 'class', 'claim_genre', 'source_standing', 'matrix_rule_ref' },
  'provenance': { … },
  'floor_met': true
}
```

**Note:** this shape describes the **intelligence-query response** (a live productization or extract call), NOT the ledger read-side. The intelligence-query endpoint itself is a G5a+ obligation (there is no shipped `/api/query` or equivalent). The response shape is not currently violated because the endpoint doesn't exist yet.

**Verdict: NON-BINDING (yet).** G5a prep must land Interface Spec §11 response contract when the intelligence-query endpoint is drawn.

### 1.7 Interface Spec §16 invariants — currently-shipped-code check

| # | Invariant | Shipped exposure | Verdict |
|---|---|---|---|
| 1 | One entry, deterministic routing on role | Frontend `App.js` has minimal router but no role-differentiated surfaces yet | **G5b obligation** — no violation because no multi-role UI shipped |
| 2 | Surfaces open calm; depth on reach | N/A — no rich UI shipped | **G5b obligation** |
| 3 | Class present with every unit; plain-language, never bare score | `NormalizedUnit.defensibility.defensibility_class` is required + frozen; downstream UI must render it — no shipped UI hides it | **MATCH** (backend obligation met via frozen contract) |
| 4 | Three lenses join via `trace_id`; user reaches deeper on same surface | `LedgerRow.trace_id` frozen field exists; lens rendering is G5b | **G5b obligation** |
| 5 | Refusal-below-floor occupies answer position | Northena `refuse_open_run` path exists + returns `LedgerRow(stage='admit', decision='refused')`; UI treatment is G5b | **MATCH** (backend) + **G5b obligation** (UI) |
| 6 | Response contract returns claim + class as one object; no separable shape | No `/api/query` endpoint shipped yet — nothing to violate | **G5a obligation** |
| 7 | Key scope enforced server-side; outer gate for data-buying | No key management shipped yet | **G5a obligation** (P2 backlog) |
| 8 | Operator surface exception-first | No operator UI shipped | **G5b obligation** |
| 9 | One record, two scopes (governance surface + audit lens reach identical record) | Backend seam exists (`by_run` + planned `by_trace`); UI ensures identical rendering is G5b | **MATCH** (backend seam) + **G5b obligation** (UI) |
| 10 | Every control-surface action versioned, diffed, logged | No control-surface UI shipped | **G5b obligation** (P2 backlog) |

**Cumulative shipped-code contradiction count: 0.**

## 2. UX Architecture Spec vs shipped state

UX Spec is the parent that Interface Spec realises. UX Spec sections §1–§9 (trust model, surface map, trace model) are **experience-architecture-level**, not code-level. They bind G5b (frontend) primarily and G5a (integration response shape) secondarily.

### 2.1 Trust model (UX §3)

Three layers: **the answer** (with class), **the reasoning** (on reach), **the record** (on reach). Shipped backend supports this via:
- `NormalizedUnit.defensibility.defensibility_class` (the answer's class)
- `SolvaTrace` (G3-frozen contract; the reasoning) — NOT YET SHIPPED
- `LedgerRow` (the record) — SHIPPED

**Verdict: MATCH (partial, expected).** G3 delivers reasoning trace; G5b delivers UI rendering of all three.

### 2.2 Surface map (UX §4)

Six surfaces: Decisions console, Product surface, Integration surface, Operator surface, Governance surface, Control surface. **None shipped as user-facing UI.** Frontend has a placeholder `App.js`.

**Verdict: G5b obligation** (all six surfaces build sequentially post-G5a).

### 2.3 Trace model (UX §9)

Three lenses (unit / reasoning / audit) joined by `trace_id`. Backend seams for lens 1 (unit) exist via `NormalizedUnit`; lens 3 (audit) via `LedgerRow`. Lens 2 (reasoning) needs G3's `SolvaTrace`.

**Verdict: MATCH (backend seams)** + **G3 + G5b obligation** (contract + rendering).

## 3. Cross-reference: Interface / UX ↔ Product Spec 2.1

Both new specs cite Product Spec v2.1 as the parent-that-prevails-on-conflict. Cross-reference check:

- Product Spec §27 (User Surfaces) enumerates the same six surfaces as UX Spec §4 + Interface Spec §3 — **MATCH**.
- Product Spec §28 (Integration Contract) declares the same response-contract shape as Interface Spec §11 — **MATCH**.
- Product Spec §30 (Governance and Control) declares taxonomy/thresholds/access/tenancy control classes matching Interface Spec §15 + UX Spec §8 — **MATCH**.
- Product Spec §31 invariants #1–#14 subsume Interface Spec §16 invariants (Interface Spec invariants are ALL derivable from Product Spec invariants + surface descriptions) — **MATCH**.

**No cross-spec contradictions.**

## 4. G5-prep TODO items (journal for future G5-prep dispatches — do NOT write prep docs in this phase)

The following are surfaced for later G5-prep phases; **not** in Substrate-Drop v1 scope:

- **G5a prep TODO** (`docs/g5a_prep/*.md`, to be written when G5a is opened):
  - `/api/discipline/lift_manifest` — read-only manifest exposure route.
  - `/api/northena/trace/{trace_id}` — trace-lens correlation route (Interface Spec §14 + UX Spec §9 both bind this).
  - `/api/query/*` — intelligence-query endpoint(s) per Interface Spec §11 response contract.
  - Key management + scope enforcement (Interface Spec §10 keys-and-scope) — likely deferred to a later slice.
- **G5b prep TODO** (`docs/g5b_prep/*.md`, to be written when G5b is opened):
  - Decisions console (UX §5 + Interface §6–§8).
  - Product surface (UX §5 + Interface §9).
  - Integration surface UI landing (Interface §10 keys-generation UI).
  - Operator surface (UX §7 + Interface §13, exception-first pattern).
  - Governance surface (UX §8 + Interface §14, DPO's audit lens at system scope).
  - Control surface (UX §8 + Interface §15, taxonomy + thresholds + access + tenancy).
  - Landing + sign-in routing (Interface §4 + §5, the entry).

## 5. Phase source-requirements assignment

Interface Spec + UX Spec are **primarily G5 substrate**. Both specs' front-matter says "It is a forward specification: it defines what must be true of any correct experience/interface, and does not assume one has been built."

- Interface Spec §11 response contract binds G5a **and** touches G6 (outer-gate data-buying path).
- Interface Spec §14 (Governance Surface, trace_id-keyed record retrieval) binds G5a (backend trace route) **and** G5b (governance surface UI).
- Interface Spec §11 references Northena Ledger fields (`trace_id`, `matrix_rule_ref`, `provenance`) — informational for G5a; not build-time material for G3/G4 (Solva/Targeta/Mtafiti do not need the interface response contract to build their contracts; they produce the fields the interface consumes).
- UX Spec §3 (trust model / three-lens architecture) binds G5b for the lens rendering, and touches Northena `stamp_audit` semantics — but the backend absorption seam is already frozen.

**Final phase_source_requirements.yaml mapping (applied):**

```yaml
G3:
  - RMS_Solva_Specification.md
  - RMS_Product_Engineering_Spec_v2.1.md
G4:
  - RMS_Targeta_Specification.md
  - RMS_Mtafiti_Specification.md
  - RMS_Product_Engineering_Spec_v2.1.md
G5a:
  - RMS_Interface_Specification.md
  - RMS_Product_Engineering_Spec_v2.1.md
  - northena.md
G5b:
  - RMS_UX_Architecture_Specification.md
  - RMS_Interface_Specification.md
  - RMS_Product_Engineering_Spec_v2.1.md
G6:
  - RMS_Product_Engineering_Spec_v2.1.md
  - RMS_Interface_Specification.md
  - northena.md
```

Rationale for G6 addition of Interface Spec: Interface §12 (Data-Buying Path) declares the outer-gate integration surface — an obligation on G6 for the outer-gate + data-buying shape.

---

## CODE_IMPACT items

**Currently-shipped API route contradictions: none.**

The `/api/northena/ledger/by_run/{run_id}` route uses `run_id`, not `trace_id`, but this is dual-key coexistence, not contradiction. `LedgerRow` carries both fields; the run-scope query stays valid, the trace-scope query lands at G5a.

All other Interface-Spec-declared surfaces + endpoints are G5-obligations — no shipped code contradicts them because they aren't shipped yet.

## Corrections applied

**None** to shipped code. **None** to prep sketches (G5 prep docs do not yet exist and are explicitly out-of-scope for Substrate-Drop v1).

- `phase_source_requirements.yaml` **extended** with Interface + UX mappings per §5 above.
- `MANIFEST.md` **extended** with Interface + UX SHA-256 entries.
- `test_substrate_drop_gate.py` auto-picks up new phase entries via parametrization; no test-code change needed.

## Summary

- **MATCH: 6** (contract-schema route non-binding, ledger.by_run dual-key, invariant #3 backend-obligation-met, invariant #5 backend refusal path, invariant #9 backend one-record seam, cross-spec parent alignment).
- **SKETCH_CORRECTION: 0** (no G5 prep sketches yet).
- **CODE_IMPACT: 0.**
- **G5-prep TODO: 12 items** (7 G5b UI surfaces + 5 G5a route/prep items), journaled for future G5-prep dispatches.
- **HAZARD-STOP (a) raised for shipped API routes: NO.**

**Verdict:** Interface + UX specs cleanly slot into G5a + G5b substrate. Shipped code (G0..G2a) does not contradict either spec. G3/G4 build against their own specs; Interface + UX bind G5 onward.
