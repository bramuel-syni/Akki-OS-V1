# Transform Forms · Stage A Proposal (BCR §3.7)

**Dispatch:** Owner post-Artifact-Store-ratification message, 2026-07-08.
**Sequence position:** BCR §5.1 line 315 — *"6. Transform forms (3.7) and fluency (3.8) — post-B-5b; both ride existing envelopes and gates."* Active lane per Owner update; unblocked by Artifact Store close (`ea9957e`).
**Governance model:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Escalations pre-tiered per §4.4.
**Standing Rule v3:** on-disk canonical. Reply body carries file SHA + line-range map + tier tags only.

---

## §1. Cell-density assumption (rates carried forward from governance §6)

Rates cited from the on-disk codified rate ledger; no restatement.

### §1.1 Empirical baseline (all prior codifications carried forward)

| Class | Rate | Basis |
|---|---:|---|
| Backend Pytest shared-helper amortised | 12 LoC/cell | §6.1 |
| Backend endpoint impl 3-share | 40 LoC/endpoint | §6.2 |
| Backend service module standalone | 100 LoC/module | §6.3 |
| Frontend Jest structural fallback | 16 LoC/cell | §6.4 |
| Playwright chromium data-testid | 9 LoC/cell | §6.5 |
| Frozen Pydantic contract class | 60 LoC/class | §6.6 |
| **Frozen contract snapshot JSON standalone** | **~155 LoC/snapshot** | **§6.7 (codified at AS close, mandatory line-item for any new frozen contract)** |

### §1.2 Amortisation Divergence Class

All prior triggers unchanged (Amendment I; shared-helper 12 LoC/cell class remains the classic amortised rate).

### §1.3 Snapshot JSON rate — LINE-ITEM AT §3 BAND DERIVATION

Per governance §6.7 named trigger: *"Any Stage A adding a new frozen contract MUST price its snapshot at ~155 LoC/snapshot standalone."*

Transform Forms adds **2 frozen contracts** (KA + Callable Skill provisioning; per §2.1 below) → **2 × 155 = 310 LoC in snapshots**, entered explicitly at §3.

### §1.4 Watched rate classes (per governance §6.8; NOT codified until second observation)

Transform Forms will observe (or not observe) these rate classes in execution:
- **Async httpx backend Pytest cells** — ~25 LoC/cell empirical at AS. TF has ≤ 3 async client cells expected (KA-produce E2E + skill provision E2E + skill query E2E). If they land at ~25 LoC/cell → **codification trigger**.
- **AST/reflection gate cells** — ~40 LoC/cell empirical at AS-G6. TF has 1 candidate: TF-G6 "Literal-widening negative" (see §2.6). If it lands at ~40 LoC/cell → **codification trigger**.

Neither is priced in the band; both are watched and disclosed at close if observed.

### §1.5 Transform-Forms-specific cell classes

None emerge. The KA claim-graph assembly + Callable Skill provisioning + per-call inner gate all decompose into standard shapes (endpoint impl, service module, Pydantic contract, Pytest cell). No new rate class.

### §1.6 Re-derivation rule

If execution observes a class not present in the rate ledger (unlikely at TF given all shapes are pre-classified), disclose at close with cell count + LoC actuals; codify only if a second observation confirms the class.

---

## §2. Matrix enumeration

### §2.1 Frozen contracts to add

**Two new frozen contracts land at Transform Forms** (per BCR §3.7 annex line 219-233). Both priced at §6.6 (60 LoC/class) + §6.7 (155 LoC/snapshot) per governance.

#### §2.1.1 Knowledge Artifact export (`ka.v0`) — TF-R1

**Authority-source (BCR §3.7 annex line 220-226 verbatim):**

```
Knowledge artifact export (ka.v0)
  { schema_version: ka.v0,
    nodes: [ { claim_id, claim_text,
               defensibility: {class, contested: bool},
               trace_id, provenance: {source_ref} } ],
    edges: [ { from_claim_id, to_claim_id,
               relation: corroborates | contradicts | retracts } ] }
```

**Landing:** `backend/contracts/knowledge_artifact_v0.py` NEW — `KnowledgeArtifactV0` (top-level) + `KnowledgeArtifactNode` (nested per-node with `defensibility`, `trace_id`, `provenance`) + `KnowledgeArtifactEdge` (per-edge with `relation` literal `corroborates|contradicts|retracts`). Snapshot `knowledge_artifact_v0.contract_snapshot.json`.

**Parity delta:** 29 → 30 (or higher — see TF-E1 [Tier 1]).

**LoC estimate:** 60 class + 155 snapshot = **215 LoC**.

#### §2.1.2 Callable Skill provisioning record — TF-R2

**Authority-source (BCR §3.7 annex line 228-233 verbatim):**

```
Callable-skill provisioning record
  { skill_id, corpus_slice_ref: artifact-store key,
    key_grant_id, floor, scope, endpoint_path,
    provisioned_at, revoked_at?: str }
  Governance: per-call inner gate; every response carries class inline;
  slice bound at freeze and immutable thereafter (new slice = new skill).
```

**Landing:** `backend/contracts/callable_skill_provisioning_v0.py` NEW — `CallableSkillProvisioningV0` (7 fields + Optional revoked_at). Snapshot `callable_skill_provisioning_v0.contract_snapshot.json`.

**Parity delta:** 30 → 31 (or service-layer per TF-E2 [Tier 1]).

**LoC estimate:** 60 class + 155 snapshot = **215 LoC** (if frozen); ~40 LoC (if service-layer dataclass per TF-E2 β).

### §2.2 Backend transform pipeline

- `backend/services/transform_forms/knowledge_artifact.py` NEW — claim-graph assembly. Inputs: reach + standard filter; output: `KnowledgeArtifactV0`. **~120 LoC** (module + assembly logic).
- `backend/services/transform_forms/callable_skill.py` NEW — provisioning + per-call inner gate wrapper. Slice-freeze mechanism (see TF-E4 [Tier 1] for the how). **~140 LoC**.
- `backend/services/transform_forms/__init__.py` NEW — barrel export. ~10 LoC.

**LoC estimate for services:** ~270 LoC.

### §2.3 Provenance preservation mechanism (TF-R1 + Owner Tier-1 line "every claim carries class + trace_id inline")

**Owner Tier-1 line verbatim:** *"provenance preservation through the transform (every claim in a KA carries class + trace_id inline)"*

**Landing shape:** structural — the KA contract at §2.1.1 has `defensibility.class` + `trace_id` DIRECTLY on each `KnowledgeArtifactNode` (not sidecar, not join-table). Mechanism-not-convention.

**Attestation at close:** TF-G3 provenance gate — every `KnowledgeArtifactNode` has non-None `defensibility.class` AND non-None `trace_id`. Grep-negative or Pydantic `min_length=1` validator; both enforce structurally.

### §2.4 Callable Skill per-call inner gate + slice bound at freeze

**Owner Tier-1 line verbatim:** *"the governance line on Callable Skills — per-call inner gate, slice bound at freeze"*

**Two sub-surfaces open here** — see TF-E4 [Tier 1] for the ruling menu.

#### §2.4.1 Per-call inner gate location

- **Option α (recommended pending ruling):** inner gate is a decorator/wrapper on the skill query endpoint that checks scope + standard-floor + emits per-response class inline. Reuses the existing scope check via `services.auth.key_grants.check_scope` (P8E-E2 α pattern; single-source-of-truth for scope).
- **Option β:** inner gate is a middleware at the router level. Rejected inline — middleware applies to all routes; skill-specific governance would violate single-source-of-truth for scope.

#### §2.4.2 Slice bound at freeze mechanism

- Freeze primitive: on provisioning, the skill's `corpus_slice_ref` (an artifact-store key) is written into the `CallableSkillProvisioning` record. The record is **write-once** in a `callable_skills` collection (`find_one_and_update` with upsert=True, no update path).
- Immutability enforced structurally: the endpoint `POST /api/callable_skill/{skill_id}/query` reads `corpus_slice_ref` from the provisioning record and passes it to the inner gate; a "new slice = new skill" invariant means any change requires a new `skill_id` (attested by TF-G5).

### §2.5 Frontend forms

**Zero frontend work at Transform Forms Stage A.** Per BCR §3.7 TF-R3 verbatim:

> *"The grain-compatibility matrix already encodes both forms' cells (verified); wizard offerability for these forms opens when they land — a config change, not a wizard rebuild."*

Landing: the config file `grain_compatibility_matrix.json` (existing) is patched to mark `knowledge_artifact` + `callable_skill` cells as `offerable=true` at TF close. **~5 LoC config diff.** Zero Jest cells. Zero Playwright cells.

`[Tier 3 default]` (§5.6): no new frontend surface; existing wizard picks up the two forms as offerable via config toggle only.

### §2.6 Named gate roster (TF-G* + Tier-1 attestations)

BCR §3.7 does NOT enumerate named TF-G* gates in the annex (unlike EE-G1..G4 or AS-G1..G4). Standing pattern: derive gate names from the promise structure + Owner Tier-1 line.

| Gate | Purpose | Test cell |
|---|---|---|
| **TF-G1** KA contract shape frozen + snapshot at parity 30 | attest v1-g7 at 30 for KA + byte-identity of nodes/edges/relation Literal | `test_transform_forms.py::test_tf_g1_ka_v0_frozen_and_snapshot_at_30` |
| **TF-G2** Callable Skill contract shape frozen + parity 31 (if TF-E2 α) OR service-layer if β | attest v1-g7 at ruling-dependent parity | `test_tf_g2_callable_skill_provisioning_shape` |
| **TF-G3** Every KA node carries class + trace_id inline (provenance preservation) | Pydantic validator + structural attest cell | `test_tf_g3_every_ka_node_has_class_and_trace_id_inline` |
| **TF-G4** Below-floor query returns refusal envelope (BCR §3.7 line 117 spec) | inner gate refuses below floor | `test_tf_g4_below_floor_query_returns_refusal` |
| **TF-G5** Slice bound at freeze — new slice = new skill (immutability) | attempt to mutate `corpus_slice_ref` after provisioning fails | `test_tf_g5_slice_bound_at_freeze_no_mutation` |
| **TF-G6** Relation Literal closed at 3 values `{corroborates,contradicts,retracts}` — no widening | grep-negative on Literal expansion outside `contracts/` | `test_tf_g6_relation_literal_closed` |
| **TF-G7** Per-response class inline on Callable Skill query output | every skill query response has non-None `defensibility.class` | `test_tf_g7_skill_query_response_has_class_inline` |
| **V1-G7** parity attestation at 30 or 31 (ruling-dependent) | snapshot bijection at new parity | `test_v1_g7_attestation_parity_N_at_transform_forms_close` |
| E5 no HTTP 409 in TF new files | grep-negative | `test_no_http_409_in_transform_forms_new_files` |
| 4-code registry closure re-attest | registry unchanged | `test_auth_refusal_registry_still_closed_at_four_codes` |

**Backend cell count total: 12** (TF-G1..G7 + V1-G7 + 2 anti-rule + 2 attestations = 12).

### §2.7 Backend routers

- `backend/routers/transform_forms.py` NEW — `POST /api/transform/knowledge_artifact/produce` + `POST /api/transform/callable_skill/provision` + `POST /api/callable_skill/{skill_id}/query`. **~150 LoC** (3 endpoints × 40 LoC + 30 LoC router scaffolding).

---

## §3. Band derivation

### §3.1 Point-estimate (matrix × rates)

| Bucket | LoC |
|---|---:|
| §2.1.1 KA contract class + snapshot | 60 + 155 = 215 |
| §2.1.2 Callable Skill contract class + snapshot | 60 + 155 = 215 |
| §2.2 Backend service modules (KA assembly + skill wrapper + __init__) | 270 |
| §2.5 Frontend config toggle | 5 |
| §2.7 Router (3 endpoints amortised) | 150 |
| §2.6 Backend tests (12 cells × 12 LoC/cell + fixtures 40) | 184 |
| Docs (close report + rulings record) | *(excluded per §4.1 baseline)* |
| **Point-estimate total** | **~1,039 LoC** |

**Cell count total: 12 backend Pytest cells. Zero frontend Jest cells. Zero Playwright cells.**

### §3.2 Owner-anchored band

**Anchored band:** `[880, 1,240]` LoC (point-estimate ± ~15% shave/cushion; matches 8-EXT proportion `[900, 1,180]` ≈ ±14%).

**Snapshot line-item transparency (per governance §6.7 named trigger):** 2 × 155 LoC = 310 LoC of the point-estimate is snapshot JSON, priced standalone. Any deviation (>±30%) disclosed at close.

**Ruling-dependent band drift:**
- If TF-E1 α (KA additive): 60 + 155 = 215 LoC (in-band).
- If TF-E2 α (Callable Skill frozen): 60 + 155 = 215 LoC (in-band). If TF-E2 β (service-layer): only ~40 LoC → **band drops ~175 LoC** at the low end. Disclose at close.
- If TF-E4 α (inner gate = decorator + reuse `check_scope`): ~40 LoC. If TF-E4 β/γ (middleware/other): higher.

### §3.3 Symmetric miss-disclosure discipline

Per new governance §2.2 (Tier 2): a band miss is a line in the close report, not a halt.

### §3.4 §4.2 pre-authorized split thresholds — not expected to trigger

**Thresholds:** ≥1,500 LoC **OR** ≥60 cells → autonomous split.

**Actuals (point-estimate):** 1,039 LoC (69% of LoC threshold) · 12 cells (20% of cell threshold).

**Trigger status:** NOT expected. If actual creeps into threshold (as AS did), disclose at close per Tier-2; split remains pre-authorized.

---

## §4. Dispatch discipline

### §4.1 Baseline atomic first-commit

Single atomic commit bundling: 2 frozen contracts + 2 snapshots + service modules + router + all tests + rulings record + close report + PRD/PHASE_STATE updates. Pattern-matches 8-EXT / 9.1+9.3 / Artifact Store.

### §4.2 Pre-authorized split thresholds

Threshold ≥1,500 LoC OR ≥60 cells → autonomous split. If triggered during execution, split by natural boundary: **commit A** lands KA (contract + assembly + endpoint + provenance gate); **commit B** lands Callable Skill (contract + inner-gate wrapper + provisioning + query endpoint + slice-freeze gate). Both surfaces independently coherent.

### §4.3 Dispatch-independence + [OWNER] gates

- **AS-OWN-1** (production object-store choice) — still open, NOT gating Transform Forms; KA hand-over uses the adapter seam (`atomic_put_with_receipt`); production swap is a config change (§AS Tier-3 default #1).
- **9.2-OWN-1..3** (Topology · Archive access · 300-unit slice) — in-motion Owner-side per Owner update (2026-07-08). NOT gating Transform Forms; Transform Forms is independent of Phase 9 Stage B.
- **New [OWNER] gates from TF:** NONE anticipated. TF is not gated on any Owner-side fact; Owner-Tier-1 rulings on TF-E1..E4 are sufficient.

---

## §5. Escalations — PRE-TIERED per governance §4.4

### §5.1 TF-E1 [Tier 1] · Knowledge Artifact contract shape (additive parity 29→30)

**Class:** frozen wire contract (governance §1.1 last bullet).
**Question:** does `KnowledgeArtifactV0` land as a single top-level frozen contract with nested per-node/per-edge sub-models (per BCR §3.7 annex line 220-226 shape), OR split into three separate frozen contracts (`KnowledgeArtifactV0` + `KnowledgeArtifactNode` + `KnowledgeArtifactEdge` — three parity bumps: 29 → 32), OR use an aliased-list shape?

**Authority-source language (BCR §3.7 annex line 220-226 verbatim):**

```
Knowledge artifact export (ka.v0)
  { schema_version: ka.v0,
    nodes: [ { claim_id, claim_text,
               defensibility: {class, contested: bool},
               trace_id, provenance: {source_ref} } ],
    edges: [ { from_claim_id, to_claim_id,
               relation: corroborates | contradicts | retracts } ] }
```

**Promise-protected (governance §4.3):** frozen wire contract — external parties consume the KA JSON export; a stable schema over time is the client-promise. Sub-model choice affects `$defs` shape in the auto-generated JSON schema but not the wire.

**Options:**

- **α** — Single top-level `KnowledgeArtifactV0` with `KnowledgeArtifactNode` + `KnowledgeArtifactEdge` as nested Pydantic sub-models in the SAME file. Parity 29 → 30 (one new snapshot; sub-models emit under `$defs`).
- **β** — Three separate frozen contracts (top-level KA + Node + Edge each as own file + snapshot). Parity 29 → 32 (three new snapshots). Wire-identical to α.
- **γ** — Untyped nested `dict` for nodes + edges under a single top-level `KnowledgeArtifactV0`. Rejects Pydantic-frozen-contract discipline for the inner shape. NOT recommended.

**Recommended:** **α**. Rationale: (1) single wire-facing contract (client-visible shape at `ka.v0`) matches BCR's `schema_version: ka.v0` framing; (2) nested Pydantic sub-models emit their shapes under `$defs` in the JSON schema — same wire semantics as β with a smaller parity bump; (3) additive-by-one-new-contract mirrors AS-E1 α pattern.

**Escalation surface:** frozen contract + parity assertion set. Full-rigor Tier-1 treatment. Owner ruling required BEFORE execution.

### §5.2 TF-E2 [Tier 1] · Callable Skill provisioning record shape (frozen contract vs service-layer)

**Class:** frozen wire contract (governance §1.1 last bullet) OR service-layer artefact (§1.1 opt-out condition).
**Question:** does the `CallableSkillProvisioning` record land as a NEW frozen Pydantic contract with snapshot (parity 30 → 31 assuming TF-E1 α), OR as a service-layer dataclass with a Pydantic-validated JSON persistence adapter (no snapshot, no parity bump)?

**Authority-source language (BCR §3.7 annex line 228-233 verbatim):**

```
Callable-skill provisioning record
  { skill_id, corpus_slice_ref: artifact-store key,
    key_grant_id, floor, scope, endpoint_path,
    provisioned_at, revoked_at?: str }
  Governance: per-call inner gate; every response carries class inline;
  slice bound at freeze and immutable thereafter (new slice = new skill).
```

**Promise-protected:** the provisioning record is INTERNAL — it drives per-call scope enforcement + slice-freeze but is not an external wire contract on the query surface (query responses ride the existing `qualified_data` / `composed_conclusion` envelopes per BCR §6.4 line 114-115). Therefore the frozen-contract discipline is optional here; the trade-off is honesty grammar vs parity honesty.

**Options:**

- **α** — Frozen contract `CallableSkillProvisioningV0` + snapshot. Parity 30 → 31. Honesty grammar: "provisioning is a stable wire" (even though the wire is internal). Simpler audit story.
- **β** — Service-layer dataclass in `services/transform_forms/callable_skill.py` (no snapshot, no parity bump). Parity stays at 30. LoC saving ~175. Reserves frozen-contract discipline for external-consumer surfaces.
- **γ** — MongoDB collection schema (no Pydantic contract). Rejects Pydantic-BaseModel discipline entirely for this record. NOT recommended.

**Recommended:** **α**. Rationale: (1) governance §1.1 line "frozen wire contracts" — the provisioning record IS load-bearing on the per-call inner gate (a corrupt or mutated provisioning record breaks the slice-freeze promise); (2) parity 31 is the honest count when a load-bearing shape lands as a Pydantic contract; (3) LoC saving from β (~175 LoC) is not the material trade-off — audit clarity is.

**Escalation surface:** frozen contract + parity assertion set. Owner ruling required BEFORE execution.

### §5.3 TF-E3 [Tier 1] · Provenance preservation — `defensibility.class` field type (constrained-str vs Literal)

**Class:** honesty grammar (governance §1.1 · "class-with-claim" · "no fabricated values") + frozen wire contract.
**Question:** on `KnowledgeArtifactNode.defensibility.class`, is the field a Python `Literal[...]` enumeration (e.g. `Literal["load_bearing", "contested", "unsupported", ...]`) OR a `constrained-str` (str with `min_length=1` + optional regex) validated against a versioned registry (`defensibility_classes.v0.json`)?

**Authority-source language (BCR §3.7 line 216 verbatim):** *"nodes are claims carrying class, contested status, and trace_id"*

**Product v2.1 §21 policy (verbatim from RMS_Product_Engineering_Spec_v3.md):** *"class-with-claim: every disposition/refusal carries a class label."* (governance §1.1 second sub-bullet)

**Promise-protected:** class-with-claim invariant. If `class` widens over time (as new defensibility categories emerge from Compliance rulings), a Literal freeze forces a contract mutation. A versioned registry (`disclosure_types.v0.json` pattern from B-5b) accommodates additive widening without touching the frozen contract.

**Options:**

- **α** — `constrained-str` + versioned registry `defensibility_classes.v0.json`. Matches B-5b Ruling E3 γ + P8E-E7 α precedent (Term-2 config versioning). Additive widening without contract mutation.
- **β** — `Literal[...]` with a small closed set (e.g. 4 initial classes). Any new class requires a contract bump. Frozen-Literal-widening risk (Owner's explicit anti-pattern: *"never a Literal that will widen"* per BCR §3.11 CK-I1).
- **γ** — `str` (unbounded). Rejects class-with-claim discipline entirely. NOT recommended.

**Recommended:** **α**. Rationale: (1) Owner explicit anti-pattern rules against widening Literals at CK-I1; (2) B-5b + AS precedent (`disclosure_types.v0` + `data_class_registry.v2/v3`) — versioned registry is the established shape; (3) Compliance rulebook writes (B-5b `RuleClassWriter`) already produce `defensibility_classes` additively over time.

**Escalation surface:** frozen wire contract + honesty grammar surface. Full-rigor Tier-1. Owner ruling required BEFORE execution.

### §5.4 TF-E4 [Tier 1] · Callable Skill per-call inner gate location + slice-freeze mechanism

**Class:** security boundary + honesty grammar (governance §1.1 · "auth scope" + "class-with-claim per response").
**Question:** two sub-questions on the mechanism:

**(a) Inner gate location.** Does the per-call inner gate live as:
- **α** — a decorator on the skill query endpoint (per-endpoint, module-scoped) that composes: (i) scope check via `services.auth.key_grants.check_scope` (P8E-E2 α single-source), (ii) standard-floor check against the provisioning record's `floor`, (iii) response mutation to include `defensibility.class` inline. Failure at any step → refusal envelope (below-floor) or 403 (scope mismatch).
- **β** — a FastAPI middleware that intercepts every `/api/callable_skill/*` request. Broad; may leak to non-skill routes as router paths shift.
- **γ** — an in-service function `governed_skill_query(...)` that endpoint calls first thing. Simplest but "call-site convention" (violates mechanism-not-convention).

**(b) Slice-freeze mechanism.** Is `corpus_slice_ref` freeze enforced by:
- **α** — write-once at provisioning (Mongo `insert_one` only; no `update_one` on the field; grep-negative gate over the codebase for `update_one({..., "corpus_slice_ref": ...})`).
- **β** — immutable field via Pydantic `ConfigDict(frozen=True)` at contract-load time (post-hydration mutation raises TypeError).
- **γ** — Owner ruling as convention "new slice = new skill_id" but no structural enforcement.

**Authority-source language (BCR §3.7 line 232-233 verbatim):** *"Governance: per-call inner gate; every response carries class inline; slice bound at freeze and immutable thereafter (new slice = new skill)."* + BCR §6.4 line 116 verbatim: *"Stay-running via the inner gate: governance enforced per call, key scope server-side — the existing live-path enforcement mode, applied to a standing service."*

**Promise-protected:** two surfaces:
- **security boundary** — per-call scope check + response class-inline enforcement.
- **immutability** — slice-freeze is the client-promise: "the corpus you provisioned is the corpus you're querying" (buyer verification). If mutable, a compromised admin could re-point a skill mid-flight.

**Options + Recommended:**

- **(a) α + (b) α** — decorator on endpoint + write-once at provisioning + grep-negative gate. RECOMMENDED. Mirrors AS-E4 γ Condition-2 pattern: mechanism enforced by structure, proven by gate.
- Alternative combinations disclosed above.

**Escalation surface:** two Tier-1 sub-surfaces (governance mechanism + slice-freeze). Owner ruling required BEFORE execution on both (a) and (b).

### §5.5 TF-E5 [Tier 2] · Adapter surface split threshold (disclosure-only, no ruling required)

**Class:** cost/rework · split threshold (governance §2.1).

**Statement:** if execution LoC exceeds 1,500 OR cell count exceeds 60, split by natural boundary: **commit A** lands KA (contract + assembly + `POST /produce` + TF-G1/G3/G6); **commit B** lands Callable Skill (contract + inner-gate wrapper + provisioning + query + slice-freeze + TF-G2/G4/G5/G7). Both independently coherent — KA has no dependency on Callable Skill and vice versa.

**Disclosure-only:** no Owner ruling required.

**Expected trigger:** NO (point-estimate 1,039 LoC / 12 cells — 69% / 20% of thresholds). If AS-close overshoot pattern repeats (snapshot JSON + test-file rate composition), actual may hit 1,300-1,500 LoC. Disclosed at close.

### §5.6 Tier-3 defaults (silent, disclosed at close, no escalation)

Per governance §3.2: builder defaults + one disclosure line per item. Format: `[Tier 3 default] {item} → {chosen default} — {one-line rationale}.`

Expected Tier-3 defaults at Transform Forms execution:

1. **`[Tier 3 default]` Module layout** → `backend/services/transform_forms/` (singular directory, plural noun for scope) — matches `services/artifact_store/` + `services/compliance/` conventions.
2. **`[Tier 3 default]` Form naming** → `ka.v0` for Knowledge Artifact + `callable_skill_v0` for Callable Skill provisioning — matches Owner-verbatim BCR §3.7 annex text.
3. **`[Tier 3 default]` Rendering mechanics (frontend)** → NONE (no new UI at this phase per TF-R3 verbatim; existing wizard picks up two new forms as offerable via `grain_compatibility_matrix.json` config toggle).
4. **`[Tier 3 default]` Storage collection for Callable Skill provisioning** → MongoDB collection `callable_skills` with unique index on `skill_id`; write-once via `insert_one` (no `update_one` for `corpus_slice_ref`).
5. **`[Tier 3 default]` Router path** → `POST /api/transform/knowledge_artifact/produce` + `POST /api/transform/callable_skill/provision` (writes) + `POST /api/callable_skill/{skill_id}/query` (per-call).
6. **`[Tier 3 default]` KA delivery hand-over** → via existing Artifact Store adapter (`atomic_put_with_receipt` from AS phase) with key `artifacts/{trace_id}/{ka_id}.json`; ext=`json` in the whitelist per AS Tier-3.
7. **`[Tier 3 default]` `skill_id` generation** → `uuid.uuid4().hex` at provisioning time (caller does not supply; the provisioning endpoint mints).
8. **`[Tier 3 default]` Grain matrix toggle** → in-file edit at existing `grain_compatibility_matrix.json` config; mark `knowledge_artifact` + `callable_skill` cells as `offerable=true`.
9. **`[Tier 3 default]` Docs skeleton** → `stage_a_proposals/transform_forms.md` (this file) + `close_reports/transform_forms.md` (at close) + `rulings/transform_forms_tf_e1_to_e4.md` (Tier-1 rulings only).

---

## §6. Standing constraints preserved

| Constraint | Attestation at close |
|---|---|
| 29 → N frozen contracts + N snapshots byte-identical (V1-G7 at ruling-dependent parity) | `test_v1_g7_attestation_parity_N_at_transform_forms_close`. |
| 4-code auth-refusal registry closed (P9-E3 / P8E-E4 α pre-carry) | `test_auth_refusal_registry_still_closed_at_four_codes` re-run. |
| E5 no HTTP 409 in TF new files | grep-negative on new files. |
| E7 middle-dot / P9-E6 α em-dash | No UI copy at TF Stage A (§2.5). No enforcement cell. |
| Standing Rule v3 (on-disk canonical) | Proposal + close + rulings on disk. |
| AS-H1 retention held-class (no direct DELETE) | TF adds no DELETE handlers. Grep-negative attest. |
| Governance §4.3 promise-naming rule | Each TF-E1..E4 landing carries the promise it protects. |

---

## §7. §0.2 Plan-debts status expected at close

- **No new debt anticipated.**
- **AS-OWN-1** still open (production object-store choice) — dispatch-independent.
- **9.2-OWN-1..3** in-motion Owner-side per Owner update — dispatch-independent of Transform Forms.

═══════════════════════════════════════════════════════════════════

*End of Transform Forms Stage A proposal. Standing Rule v3: on-disk canonical. Reply body carries file SHA + line-range map + tier-tagged escalation IDs.*
