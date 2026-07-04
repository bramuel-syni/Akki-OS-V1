# Phase 6 Stage A — Economics config surface §8 (DESIGN-ONLY)

**Delivered:** 2026-07-04 (Emergent E1 e1_dev)
**Scope:** Design-only proposals. No code writes. Parity stays 20. CI stays 504/504.
**Format:** Seven Returns per Owner dispatch (design-only).
**Delivery:** On-disk canonical + SHA quoted + inline-per-amended-standing-rule (Ruling-conditioned artifacts + new Standing Disposition text inline; everything else referenced by SHA).

---

## §0. Ruled constraints in force

| # | Ruling | Source | Binding at Phase 6 |
|---|---|---|---|
| R5 | `pricing_tier` MUST NOT be a Literal | PM review, 2026-07-04 | Applies to any tier-like Literal — pricing_tier goes constrained-str + registry. |
| R4-SD2 | Pricing values → Phase 6 mechanism + `price-model@v0-exploratory` config swap; fleet arbitration beyond apportionment → simple apportionment holds | Substrate-Drop v2, 2026-07-03 | Stage A ships MECHANISM. Real numbers post-G2b. |
| R3-SD2 | Config-as-versioned-not-frozen; shape freezes, values version | Substrate-Drop v2, 2026-07-03 | `price-model@vN.json`, `fleet-policy@vN.json`, `pricing_tiers.vN.json` — versioned config, byte-frozen shape only. |
| Infra-not-refusal | Capacity-unavailable = 503; fleet-policy-driven governance refusal = 422 with AdmissionRefusal_v0 | Phase 5 Stage A close, 2026-07-04 | Distinction Design-time clean (Return 6.5). |
| Frozen-field-changes-as-new-versions | Any frozen-field re-typing lands as v1 version file | Phase 5 Stage A close, 2026-07-04 | Applies to `AsyncDeliveryAccepted@v0.quote` seam (Return 1.4). |
| Loose-as-frozen | Where §8 does not narrow a scalar type, freeze permissively per v0-precedent default | Substrate-Drop v2, 2026-07-03 | Applies to `delivery_estimate: str`, `figure: str`, etc. Owner rules on narrowing via new contract addition. |

---

## §1. Return 1 — QuoteEnvelope@v0 shape design + D4b argument

### 1.1 Proposed field roster

Anchored to v3 §8 bullets 2, 3, 4 + §12 invariant #9 + UI Spec v1 §5.1 buyer-surface bindings.

```python
# contracts/quote_envelope.py (PROPOSAL — DESIGN-ONLY; do not implement at Stage A)
from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, constr


class QuoteEnvelope_v0(BaseModel):
    """v3 §8: every quote stamps its price-model version + carries the
    shape/model_version/outcome/stall/first-lever instrumentation surface.

    Freeze posture: FROZEN if D4b returns YES (see §1.2); UNFROZEN by named
    wire-shape gate if D4b returns NO (Ruling 3 config-as-versioned-not-frozen
    is about the CONFIG file; this is the ENVELOPE contract — different axis).
    """
    model_config = ConfigDict(extra="forbid", frozen=True)

    # ── Identity + provenance (governance-carrying) ──
    quote_id: str = Field(..., min_length=1, description="uuid-like — one quote, one id.")
    trace_id: str = Field(..., min_length=1, description="Northena/Solva trace correlator.")
    quoted_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")

    # ── Model-version stamp (§8 bullet 2 + §12 invariant #9) ──
    price_model_version: constr(min_length=1, max_length=64, pattern=r"^price-model@v[0-9]+(-[a-z0-9_-]+)?$") = Field(
        ..., description="Refs price-model@vN.json version. Pattern price-model@v<N>[-<tag>].",
    )

    # ── Pricing tier (Ruling 5 explicit: constrained-str + registry) ──
    pricing_tier: constr(min_length=1, max_length=32, pattern=r"^[a-z][a-z0-9_]{0,31}$") = Field(
        ..., description="Refs pricing_tiers.vN.json registry. constrained-str, NOT Literal (Ruling 5).",
    )

    # ── Buyer-surface payload (UI Spec v1 §5.1) ──
    figure: str = Field(..., min_length=1, description="Free-form price figure. Loose-as-frozen.")
    qualifying_volume: str = Field(..., min_length=1, description="Free-form volume. Loose-as-frozen.")
    delivery_estimate: str = Field(..., min_length=1, description="ISO-8601 duration or human string.")
    delivery_class: Literal["served_from_qualified", "requires_fresh_extraction"] = Field(
        ..., description="§8 bullet 4 two-cost-class discriminator.",
    )
    feasible_and_offerable: bool = Field(..., description="UI Spec §5.1 'feasible-and-offerable line' as bool.")

    # ── Instrumentation carry-through (§8 bullet 3) ──
    instrumentation_seed: "QuoteInstrumentationSeed_v0" = Field(
        ..., description="Inner frozen 5-key shape per §8 bullet 3.",
    )


class QuoteInstrumentationSeed_v0(BaseModel):
    """Inner frozen shape — five keys per §8 bullet 3."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    shape_ref: str = Field(..., min_length=1, description="ref to shape signature — reach + output + envelope.")
    price_model_version: str = Field(..., min_length=1, description="Belt-and-suspenders with outer envelope.")
    outcome: Literal["accepted", "rejected", "negotiated_to", "pending"] = Field(default="pending")
    stall_dimension: Optional[str] = Field(default=None, description="Which shape axis stalled.")
    first_lever_pulled: Optional[str] = Field(default=None, description="First axis buyer moved.")
```

Fields: 10 outer + 5 inner. `pricing_tier` constrained-str per Ruling 5. `price_model_version` constrained-str per Ruling 5 principle applied to versioning strings.

### 1.2 D4b argument — does QuoteEnvelope FREEZE at v0?

**Argument for FROZEN:**
- QuoteEnvelope is an external-integrator-versioned shape. UI Spec §5.1 renders `Estimated price` + `delivery estimate` + `feasible-and-offerable line` — every field is discriminated on by integrators.
- `pricing_tier` and `price_model_version` are governance-carrying strings integrators pin runtime behaviour to.
- `delivery_class` is a Literal discriminator that late-refused-first-class must carry across the accepted→delivered/refused arc unchanged.
- Precedent: `AsyncDeliveryAccepted_v0` is FROZEN for identical reasons (Owner ruling at Stage A close, 2026-07-04).

**Argument for UNFROZEN + wire-shape gate:**
- `figure`, `qualifying_volume`, `delivery_estimate` are loose-as-frozen strings whose semantics come from the model, not from schema.
- Phase 6 economics is intentionally exploratory; freezing an envelope around exploratory content risks locking a shape that fails to survive real numbers.

**Recommendation: FROZEN.** Same reasoning that FROZE `AsyncDeliveryAccepted_v0`. Loose-as-frozen scalars are fine as strings under FROZEN — Ruling loose-as-frozen explicitly authorises this. Real-number narrowing post-G2b lands as `QuoteEnvelope_v1` per frozen-field-changes-as-new-versions.

**Owner ruling required at Stage B open:** FROZEN vs UNFROZEN + wire-shape gate. Default recommendation: FROZEN. 21st + 22nd frozen contracts at Stage B (Envelope + InstrumentationSeed).

### 1.3 Sub-issue A — `pricing_tier` registry initial set

Registry file: `/app/backend/services/economics/pricing_tiers.v0.json`.

**Enumerated by v3 §8 (no speculative future tiers per Ruling 5):**

```json
{
    "version": "v0",
    "sha_hint": "computed at seal-time",
    "valid_tiers": [
        {
            "tier": "exploratory",
            "structurally_non_precedent": true,
            "time_boxed": true,
            "default_expiry_iso_duration": "P90D",
            "spec_ref": "v3 §8 bullet 2: 'Learning-phase quotes are structurally non-precedent; price-model@v0-exploratory; time-boxed'"
        }
    ]
}
```

**Rationale:** §8 bullet 2 explicitly names ONLY `exploratory`. Additional tiers (`published`, `committed`, `benchmark`) would be speculative-future violating Ruling 5 discipline. Extend via registry bump per `admission_refusal_reasons.vN.json` precedent.

**Owner ruling required at Stage B open:** initial set stays at `exploratory` (recommended) OR pre-declare a second tier.

### 1.4 Sub-issue B — AsyncDeliveryAccepted@v0.quote seam closure

Currently `quote: Optional[Any]`. Phase 6 lands `QuoteEnvelope_v0`. Three options:

**Option α — v1 version of AsyncDeliveryAccepted.** New `contracts/async_delivery_accepted_v1.py` with `quote: Optional[QuoteEnvelope_v0]`. Superset-validating (every v0 body validates under v1). Parity 20 → 22 at Stage B (or 23 with InstrumentationSeed).
- **Pro:** Consistent with NorthenaLedgerRow_v1 pattern; type-safety at schema; integrators binding v1 get narrow type.
- **Con:** +1 contract file; two response shapes at `POST /api/objectives`.

**Option β — Leave AsyncDeliveryAccepted@v0 with `Optional[Any]`.** Integrators coerce `quote` at read-time. Loose-as-frozen authorises this.
- **Pro:** Zero contract-file churn.
- **Con:** Type-safety client-side; wire-shape gate needed for pinning.

**Option γ — QuoteEnvelope IS the .quote content, envelope stays `Optional[Any]` indefinitely.**
- **Pro:** Deferred decision, zero cost.
- **Con:** Silent shape-drift risk without wire-shape gate.

**Recommendation: Option α (v1 version file).** Reasons:
1. Standing Disposition frozen-field-changes-as-new-versions gives the pattern for free — second application after 5b cements precedent.
2. Buyer surface renders live quote fields; contract-schema guarantee valuable.
3. Superset-validating means zero breaking change.

**Owner ruling required at Stage B open:** α (recommended) vs β vs γ.

---

## §2. Return 2 — price-model@v0-exploratory.json config schema + illustrative values

### 2.1 Proposed config schema

Shape freezes; values version per Ruling R3-SD2. File: `/app/backend/services/economics/price_model.v0-exploratory.json`.

**Levers consumed:** `reach` (cardinality + depth) · `output.form` · `output.grain` · `output.standard.minimum_class` · `envelope.license_class` · `warm_vs_fresh` (Phase 5) · `delivery_class`.

**OUT of scope for mechanism (BLOCKED on G2b):** Real GPU-hour costs, per-modality throughput, real unit-yield.

**OUT of scope per Ruling R4-SD2:** Fleet-arbitration-under-contention.

```json
{
    "version": "price-model@v0-exploratory",
    "tier": "exploratory",
    "expires_at": "2026-10-04T00:00:00+00:00",
    "sha_hint": "computed at seal-time",
    "levers": {
        "reach_cardinality_bands": [
            {"band": "narrow", "max_scope_refs": 3, "multiplier": 1.0},
            {"band": "moderate", "max_scope_refs": 20, "multiplier": 1.5},
            {"band": "broad", "max_scope_refs": 100, "multiplier": 2.5},
            {"band": "unbounded", "max_scope_refs": null, "multiplier": 4.0}
        ],
        "output_form_multipliers": {
            "qualified_data": 1.0,
            "composed_conclusion": 1.4,
            "callable_skill": null,
            "knowledge_artifact": null
        },
        "output_grain_multipliers": {
            "per_claim": 1.0,
            "aggregated": 0.9,
            "synthesized_whole": 1.2
        },
        "standard_multipliers": {
            "utterance": 1.0,
            "non_factual": 1.1,
            "fact": 1.4,
            "qualified_utterance": 1.6
        },
        "warm_fresh_multipliers": {"warm": 1.0, "fresh": 2.2},
        "delivery_class_multipliers": {
            "served_from_qualified": 1.0,
            "requires_fresh_extraction": 1.8
        },
        "base_figure_currency": "USD",
        "base_figure_illustrative": "10.00"
    },
    "compute_signature": "figure = base * reach * form * grain * standard * warm_fresh * delivery_class",
    "delivery_estimate_bands": {
        "warm_qualified": "PT0S — PT30S",
        "fresh_short": "PT5M — PT15M",
        "fresh_medium": "PT15M — PT2H",
        "fresh_long": "PT2H — PT24H"
    },
    "hazard_stop_notes": [
        "All multipliers ILLUSTRATIVE. Real values BLOCKED on G2b per §12 invariant #9.",
        "callable_skill and knowledge_artifact multipliers null — model refuses to quote until §6.3/§6.4 lands.",
        "Delivery estimate bands ILLUSTRATIVE. Real math BLOCKED on G2b."
    ]
}
```

### 2.2 Time-boxing (§8 bullet 2)

Two levels:
- Registry-level `tier_expires_at` (in `pricing_tiers.v0.json`) — TIER sunset.
- Config-level `expires_at` (in `price-model.v0-exploratory.json`) — THIS config sunset.

**Recommendation:** config-level `expires_at` — allows multiple exploratory-model versions with independent expiries; tier lifecycle is longer-arc.

### 2.3 Model-version stamp

`QuoteEnvelope.price_model_version` stamped at mint-time from ACTIVE config's `version` field. §8 bullet 2 requires per-quote; §12 invariant #9 makes it a Named Invariant enforced at gate.

### 2.4 Compute function seam

```python
# services/economics/price_model.py (PROPOSAL — DESIGN-ONLY)
def compute_figure(
    request: ObjectiveRequest_v2,
    warm_vs_fresh: Literal["warm", "fresh"],
    delivery_class: Literal["served_from_qualified", "requires_fresh_extraction"],
    config: PriceModelConfig,
) -> Tuple[str, str, str]:  # (figure, qualifying_volume, delivery_estimate)
    """Pure function. All illustrative until G2b. HAZARD-STOP-NOTE binding."""
```

---

## §3. Return 3 — fleet-policy@v0.json config schema + illustrative apportionment

### 3.1 Proposed schema

`/app/backend/services/economics/fleet_policy.v0.json`:

```json
{
    "version": "fleet-policy@v0",
    "sha_hint": "computed at seal-time",
    "apportionment": {
        "mining": 0.40,
        "transforms": 0.35,
        "live_path": 0.25
    },
    "constraint": "sum(apportionment.*) == 1.0 ± 0.001",
    "governance": {
        "control_surface": "master_admin_only",
        "change_recording": "ledger_row_per_change",
        "reversible": true,
        "audit_trail_ref": "v3 §6.1 Master Admin UI Spec + §11 build doctrine"
    },
    "arbitration_beyond_apportionment": {
        "status": "OPEN — Owner Ruling R4-SD2 (Substrate-Drop v2, 2026-07-03)",
        "spec_ref": "v3 §8 bullet 5 + §10 open decisions row 4",
        "hazard_stop_notes": [
            "SIMPLE APPORTIONMENT holds until concurrency bites.",
            "Under-contention arbitration DEFERRED.",
            "This module MUST refuse arbitration decisions beyond ratios."
        ]
    }
}
```

### 3.2 Apportionment discipline

- Fractions sum to 1.0 (±0.001 rounding tolerance).
- Every apportionment change writes a Northena Ledger row (stage: `converge`, decision: `terminate_success`, reason: `fleet_policy_change:from=<prior>:to=<new>`).
- Reversible per §11 — rollback writes another ledger row reason: `fleet_policy_rollback:from=<current>:to=<prior_hash>`.

### 3.3 Arbitration deferral

Per Owner Ruling R4-SD2, simple apportionment holds. Schema has NO arbitration fields beyond apportionment; `arbitration_beyond_apportionment` block IS explicit HAZARD-STOP-NOTES documentation.

Module docstring MUST carry deferral note at Stage B:
```python
"""
Fleet policy — apportionment across mining/transforms/live_path (§8 bullet 5).

HAZARD-STOP-NOTES (Owner Ruling R4-SD2, 2026-07-03):
  * Simple apportionment ONLY at Phase 6.
  * Arbitration-under-contention DEFERRED.
  * When concurrency bites (measurable threshold TBD), escalate to Owner.
"""
```

---

## §4. Return 4 — Quote instrumentation hooks

### 4.1 Instrumentation write surface

**Proposal:** Instrumentation writes to Northena Ledger via `stamp_audit` sidecar pattern — NOT a new collection.

Rationale:
- Existing pattern; no new substrate.
- §7.3 stamp_audit sidecar precedent absorbs artifacts NEVER contradicts primary field (Frozen-field-changes ruling).
- Ledger's frozen shape v0 unchanged; instrumentation rides as sidecar.
- Audit path single-surface (Master Admin queries Ledger, not two collections).

### 4.2 Ledger row shape for instrumentation

Instrumentation writes ONE ledger row per quote-outcome-event:

```python
LedgerRow(
    run_id="quote-run-<uuid>",
    trace_id=<request trace_id>,
    stage="converge",
    decision="terminate_success",
    reason=f"quote_minted:model_version={mv}:tier={tier}:delivery_class={dc}",
    artifact_ref=LedgerArtifactRef(
        artifact_type="quote_envelope",
        artifact_id=<quote_id>,
        version="v0",
    ),
    lawful_basis_ref=<from request>,
    stamp_audit={
        "quote_instrumentation_event": {
            "event": "minted" | "accepted" | "rejected" | "negotiated_to" | "refused_after_acceptance",
            "shape_ref": <shape signature>,
            "price_model_version": <mv>,
            "outcome": "accepted" | "rejected" | "negotiated_to" | "pending",
            "stall_dimension": <axis> | null,
            "first_lever_pulled": <axis> | null,
            "at": <ISO-8601 UTC>,
            "note_on_never_contradicting_primary": "stamp_audit ABSORBS the mint/outcome event; LedgerRow.reason carries primary decision. Sidecar NEVER overrides."
        }
    },
    at=<now>,
)
```

### 4.3 Service module

`services/economics/instrumentation.py`. Function `record_quote_event(quote_envelope, event, ...)` writes the ledger row.

**No new frozen contract** — ledger row shape (v0 or v1 for cancel) carries instrumentation via `stamp_audit` sidecar per §7.3.

### 4.4 Read path (Phase 8 seam)

Master Admin (§6.1 UI Spec) needs `GET /api/admin/quote_instrumentation?window=P30D&group_by=stall_dimension`. **Not landed at Phase 6.** Phase 8 seam.

### 4.5 stamp_audit-never-contradicts regression

**Named regression gate** (Stage B roster):
```
test_quote_instrumentation_never_contradicts_primary_field
    — asserts LedgerRow.stamp_audit.quote_instrumentation_event.outcome
      is CONSISTENT with LedgerRow.decision.
```

---

## §5. Return 5 — Delivery-time computation seam

### 5.1 Consumption of Phase 5 warm/fresh

Phase 5's dispatch fork emits `warm_vs_fresh`. Phase 6's `compute_delivery_estimate` CONSUMES — does NOT re-derive.

### 5.2 Pure function seam

```python
# services/economics/delivery_time.py (PROPOSAL — DESIGN-ONLY)
def compute_delivery_estimate(
    request: ObjectiveRequest_v2,
    warm_vs_fresh: Literal["warm", "fresh"],
    fleet_state: FleetStateSnapshot,
    config: PriceModelConfig,
) -> Tuple[str, Literal["served_from_qualified", "requires_fresh_extraction"]]:
    """
    Returns (delivery_estimate_str, delivery_class).

    Rules (§8 bullet 4):
      * NEVER expose GPU numbers on buyer surface.
      * served_from_qualified (warm): "instant-to-seconds" band from config.
      * requires_fresh_extraction (fresh): queue-depth + throughput + Layer costs.
        HAZARD-STOP-NOTE: real numbers BLOCKED on G2b. Illustrative bands only.
    """
```

### 5.3 fleet_state input

`FleetStateSnapshot` (runtime data class, not frozen contract):
- `queue_depth: int` — from `async_worker.get_queue().qsize()`.
- `apportionment: Dict[str, float]` — from `fleet_policy.v0.json`.
- `active_workers: int` — from `async_worker._WORKER_COUNT`.
- `estimated_throughput_units_per_hour: Optional[float]` — `None` until G2b.

### 5.4 Buyer-surface never sees GPU numbers

**Named regression gate** (Stage B roster):
```
test_delivery_time_never_reports_gpu_numbers_on_buyer_surface
    — grep-negative on QuoteEnvelope_v0 + buyer-facing response bodies for:
      "gpu", "GPU", "gpu_hours", "gpu_hrs", "cuda", "vram", "throughput_units_per_hour".
```

### 5.5 HAZARD-STOP-NOTES

Every economics module docstring carries:
```python
"""
HAZARD-STOP-NOTES (v3 §8 bullet 4 + §12 invariant #9):
  * Fresh-extraction delivery-time ships MECHANISM only.
  * Real queue-depth × throughput × Layer costs BLOCKED on G2b.
  * Buyer surface NEVER sees GPU numbers per §8 bullet 4.
"""
```

---

## §6. Return 6 — HAZARD-STOP surface enumeration

### 6.1 (a) frozen-contract mutation

- **None anticipated.** New contracts at Stage B: `QuoteEnvelope_v0`, `QuoteInstrumentationSeed_v0`, optionally `AsyncDeliveryAccepted_v1` (Option α). ADDITIONS, not mutations.
- Prior 20 contracts byte-identical (Stage B `test_prior_contracts_byte_identical_after_phase_6_stage_b`).
- **NO HAZARD-STOP raised.**

### 6.2 (b) governance decisions needed

Requires Owner ruling at Stage B open:

1. **QuoteEnvelope@v0 freeze posture** (Return 1.2). Recommendation: FROZEN.
2. **pricing_tier registry initial set** (Return 1.3). Recommendation: only `exploratory`.
3. **AsyncDeliveryAccepted@v0.quote seam** (Return 1.4). Recommendation: Option α.
4. **Delivery-estimate bands granularity** (Return 2.1, 5.4). Recommendation: 4 bands.
5. **Instrumentation write surface** (Return 4.1). Recommendation: Ledger + stamp_audit sidecar.
6. **Time-box axis** (Return 2.2). Recommendation: config-level `expires_at`.

### 6.3 (c) substrate absent

- **Real cost / throughput / yield BLOCKED on G2b** per §12 invariant #9. Phase 6 mechanism ships without them (Owner-ratified R4-SD2). Explicit HAZARD-STOP-NOTES in `price_model.py`, `delivery_time.py`, `fleet_policy.py` module docstrings at Stage B.
- **NO Stage A HAZARD-STOP raised** — known gap, ratified.

### 6.4 (d) Rule 2 trips

- **Not a Stage A concern.** Sizing anticipation surfaced in Return 7.

### 6.5 Governance vs infra distinction (Ruling infra-not-refusal)

| Condition | Class | HTTP | Body |
|---|---|---|---|
| Queue saturated (async capacity exhausted) | INFRA | 503 | `{detail: "..."}` (no refusal envelope) |
| Fleet apportionment reserved zero capacity for modality | GOVERNANCE | 422 | `AdmissionRefusal_v0(reason=fleet_policy_reserved_zero_capacity)` |
| Master Admin froze exploratory tier mid-mint | GOVERNANCE | 422 | `AdmissionRefusal_v0(reason=pricing_tier_frozen_by_control_surface)` |
| Config file corruption / unreadable | INFRA | 503 | `{detail: "..."}` |
| Config expired (`expires_at` past) mid-mint | GOVERNANCE | 422 | `AdmissionRefusal_v0(reason=exploratory_tier_expired)` |

**Registry additions** (Stage B, registry-bump v2 → v3):
- `fleet_policy_reserved_zero_capacity`
- `pricing_tier_frozen_by_control_surface`
- `exploratory_tier_expired`

ADD, not mutate. Registry-bump discipline.

**Named regression gates:**
```
test_fleet_capacity_governance_refusal_uses_admission_refusal_v0
    — fleet-policy-driven refusal is 422 with AdmissionRefusal_v0, NOT 503.
test_queue_saturation_returns_503_not_refusal
    — regression from Phase 5 Stage B, still GREEN.
```

---

## §7. Return 7 — Sizing + gates roster + §8 clause-by-clause accounting

### 7.1 Sizing anticipation (Rule 2 v2 for Stage B)

**Lifted candidates (~250L):** Versioned-config pattern (feasibility_config, admission_refusal_reasons, license_classes) ~50L; Ledger writer pattern from `async_state.py::emit_ledger_*` ~40L; stamp_audit sidecar pattern §7.3 ~30L; Wire-shape gate pattern (if UNFROZEN) ~40L; Pydantic contract scaffolding ~50L; constrained-str + registry (Ruling 5) ~40L.

**Net-new source (~1350L):**
- `contracts/quote_envelope.py` (QuoteEnvelope_v0 + InstrumentationSeed_v0) ~120L
- `contracts/async_delivery_accepted_v1.py` (Option α) ~60L
- Snapshot JSONs (3 files) ~150L
- `services/economics/pricing_tiers.v0.json` ~15L
- `services/economics/price_model.v0-exploratory.json` ~60L
- `services/economics/fleet_policy.v0.json` ~40L
- `services/economics/quote_service.py` ~180L
- `services/economics/price_model.py` ~140L
- `services/economics/fleet_policy.py` ~100L
- `services/economics/instrumentation.py` ~120L
- `services/economics/delivery_time.py` ~80L
- `routers/pricing.py` ~120L
- Modifications to `routers/objectives.py` ~30L
- Modifications to `services/service_1/dispatch.py` ~20L
- Modifications to `services/service_1/admission_refusal.py` (3 new emit helpers) ~90L
- Modifications to `services/service_1/admission_refusal_reasons.v3.json` (registry bump) ~20L
- Modifications to `test_frozen_contract_snapshot_parity.py` ~5L

**Test files (~880L):**
- `test_phase_6_stage_b_economics.py` ~700L
- `test_prior_contracts_byte_identical_after_phase_6_stage_b.py` ~130L
- Pre-Phase-6 migrations (Condition-5 pattern) ~50L delta

**Combined net-new: ~2230L.**

**PM review estimated 800–1200 LoC.** Stage A refines to **~1350L source + ~880L test = ~2230L combined** — larger because PM anchor did not fully account for Option α (v1 file + snapshot) NOR full instrumentation + fleet_policy service layer.

**Anticipated band for Stage B: 1800–2400 LoC combined.** Confidence: MEDIUM-HIGH.

### 7.2 Gates roster (Stage B target — 18 named + 5 coverage + 4 migration = ~27 tests)

**LB = LOAD-BEARING:**

| # | Gate name | Enforces | LB |
|---|---|---|---|
| 1 | `test_quote_envelope_frozen_at_v0` | Contract schema matches snapshot (if FROZEN) | LB |
| 2 | `test_price_model_version_stamps_every_quote` | §12 invariant #9 | LB |
| 3 | `test_pricing_tier_not_a_literal` | Ruling 5 AST-inspection | LB |
| 4 | `test_pricing_tier_registry_extension_via_bump_not_literal_widening` | Registry-bump discipline | LB |
| 5 | `test_fleet_policy_apportionment_sums_to_one` | Config validation | |
| 6 | `test_exploratory_tier_is_time_boxed` | §8 bullet 2 | |
| 7 | `test_quote_instrumentation_never_contradicts_primary_field` | Frozen-field ruling | LB |
| 8 | `test_delivery_time_never_reports_gpu_numbers_on_buyer_surface` | §8 bullet 4 grep-negative | LB |
| 9 | `test_queue_saturation_returns_503_not_refusal` | Phase 5 regression | |
| 10 | `test_fleet_capacity_governance_refusal_uses_admission_refusal_v0` | Governance-vs-infra | LB |
| 11 | `test_config_expiry_governance_refusal` | Time-boxing regression | |
| 12 | `test_async_delivery_accepted_v1_supersets_v0` | Frozen-field ruling (Option α) | LB |
| 13 | `test_quote_envelope_v0_wire_shape_pins_governance_keys` | Wire-shape (if UNFROZEN chosen) | conditional |
| 14 | `test_prior_contracts_byte_identical_after_phase_6_stage_b` | Byte-identity regression | LB |
| 15 | `test_admission_refusal_v3_extends_v2_additively` | Registry-bump | |
| 16 | `test_master_admin_only_writes_fleet_policy` | §6.1 UI Spec + governance | |
| 17 | `test_no_arbitration_beyond_apportionment_in_fleet_policy_json` | Ruling R4-SD2 deferral | |
| 18 | `test_hazard_stop_notes_in_all_economics_modules` | Doctrine | |

### 7.3 §8 clause-by-clause scope-bullet accounting

**Bullet 1 (v3 line 135):** *"Cost is measured; price is shaped. Throughput (GPU-hours per broadcast-hour, per modality), unit yield, and cost per qualified unit come from instrumented real-material runs. All figures are illustrative until measured."*
- Covered: Return 4 + 2 + 5. Gates: 8, 18. G2b: MECHANISM ships; REAL FIGURES blocked.

**Bullet 2 (v3 line 136):** *"Price is config: `price-model@vN`, versioned, swapped by the Master Admin control surface; every quote stamps its model version. Learning-phase quotes are structurally non-precedent: `price-model@v0-exploratory`, time-boxed."*
- Covered: Return 2.1, 2.2, 1.1, 6.5. Gates: 2 LB, 6, 11. G2b: SHAPE + MECHANISM ship.

**Bullet 3 (v3 line 137):** *"Quote instrumentation (the goal is understanding pricing dynamics, not scoring quotes): per quote — shape, model version, outcome (accepted / rejected / negotiated-to), the dimension negotiation stalled on, the first lever the buyer pulled."*
- Covered: Return 4, 1.1. Gates: 7 LB. G2b: MECHANISM ships. Phase 8 aggregation view is UI-side.

**Bullet 4 (v3 line 138):** *"Delivery time is the capacity signal users see — never GPU numbers. Two cost classes: served-from-qualified (fast) vs requires-fresh-extraction (queued, longer, priced higher)."*
- Covered: Return 5, 1.1 (`delivery_class` Literal), 2.1 (bands). Gates: 8 LB. G2b: MECHANISM ships; real math blocked.

**Bullet 5 (v3 line 139):** *"Fleet allocation is config: `fleet-policy@vN` apportioning capacity across mining / transforms / live path, set at the control surface; the operator manages it live. Arbitration logic beyond apportionment is open (§10)."*
- Covered: Return 3, 6.5, 3.3. Gates: 5, 10 LB, 16, 17. G2b: MECHANISM ships; contention arbitration DEFERRED per R4-SD2.

### 7.4 Cross-references

| Cross-ref | Phase 6 posture |
|---|---|
| §5.1 buyer surface | Phase 6 mints QuoteEnvelope; Phase 8 renders. |
| §6.1 Master Admin | Phase 6 lands service layer; Phase 8 exposes UI. |
| §12 invariant #9 | Gates 2 LB + 18 + HAZARD-STOP-NOTES in every module. |
| §10 row 3 (pricing values) | Config swap `price-model.v1.json` post-G2b. |
| §10 row 4 (fleet arbitration) | Simple apportionment; deferral in module docstring. |

---

## §8. Amended standing rule for inline delivery (Owner ruling, 2026-07-04)

Landing at `/app/memory/ORCHESTRATOR_CONTINUITY.md §0.1` as part of Phase 6 Stage A close. **Verbatim:**

> **Ruling — Inline delivery scope amended (Owner ruling, 2026-07-04):** *"On-disk canonical + SHA quoted in the return message is the authoritative close record. Inline full-text is mandatory only for two content classes: (a) ruling-conditioned artifacts (the items acceptance was explicitly conditioned on) and (b) any new Standing Disposition text. Everything else is referenced by SHA. This matches the failure evidence: four recurrences of full-report inline drops through the summarising finish wrapper; zero recurrences on bounded artifact pastes. Standing rule from Phase 5 Stage B close onwards, superseding the Phase 4a Stage B inline-all requirement to this narrower scope. The Phase 4a Stage B rule (on-disk + SHA + inline) remains historically anchored for phases 4a/4b/5-Stage-A/5-Stage-B; the amendment applies from Phase 6 onwards."*

---

## §9. Stage A close attest

- CI: 504/504 (no code writes; docs-only Stage A close).
- Parity: 20 (no new contracts at Stage A — proposals only).
- Substrate-drop: 13/13 (Phase_6 GREEN — substrate present).
- HAZARD-STOPS raised at Stage A: 0.
- `git push`: NONE.
- On-disk canonical: `/app/docs/stage_a_proposals/phase_6_stage_a.md`.
- SHA-256 (this file): quoted in return message body post-write.

---

## §10. Sign-off

**Phase 6 Stage A DESIGN COMPLETE.** Owner rules on:
1. QuoteEnvelope@v0 freeze posture (rec: FROZEN).
2. pricing_tier registry v0 initial set (rec: only `exploratory`).
3. AsyncDeliveryAccepted@v0.quote seam option (rec: α).
4. Delivery-estimate bands granularity (rec: 4 bands).
5. Instrumentation write surface (rec: Ledger + stamp_audit sidecar).
6. Time-box axis (rec: config-level `expires_at`).
7. Ratification of amended-inline-delivery Standing Disposition (§8 above).

Hold before Phase 6 Stage B dispatch.
