"""Quote service — Phase 6 Stage B orchestrator.

Composes:
  * `price_model.compute_figure` for the illustrative figure.
  * `delivery_time.compute_delivery_estimate` for TWO-band delivery.
  * `fleet_policy.capacity_reserved_zero` for governance refusal check.
  * `expiry.is_expired` for time-boxed tier refusal check.
  * `instrumentation.record_quote_event(event='minted')` on mint.

Returns:
  * `QuoteEnvelope_v0` on successful mint.
  * `AdmissionRefusal_v0` on governance refusal (fleet zero / tier
    frozen / config expired / form not quotable).

HAZARD-STOP-NOTES (v3 §8 bullet 1 + §12 invariant #9):
  * All ILLUSTRATIVE until G2b.
  * Buyer surface NEVER sees GPU numbers per §8 bullet 4.

Standing Owner Dispositions binding this module:
  * Frozen-field-changes-as-new-versions — populated `quote` field on
    AsyncDeliveryAccepted_v0 body is a QuoteEnvelope_v0 dict; v1 file
    (AsyncDeliveryAccepted_v1) narrows the type at contract layer.
  * infra-not-refusal — module NEVER raises infra errors as governance
    refusals; fleet-zero apportionment IS a governance decision.
  * Disposition-must-cite-owner-ruling — three governance-refusal
    codes ship with citation notes in the emit helpers.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, Union

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.objective_request_v2 import ObjectiveRequest_v2, OutputForm
from contracts.quote_envelope import QuoteEnvelope_v0, QuoteInstrumentationSeed_v0
from services.economics import (
    delivery_time as _delivery_time,
    expiry as _expiry,
    fleet_policy as _fleet_policy,
    instrumentation as _instrumentation,
    price_model as _price_model,
)
from services.service_1.admission_refusal import (
    emit_exploratory_tier_expired,
    emit_fleet_policy_reserved_zero_capacity,
    emit_pricing_tier_frozen_by_control_surface,
    emit_form_not_offerable,
)


# Master Admin lock on the current-bless tier. When set truthy, quote
# issuance refuses via `pricing_tier_frozen_by_control_surface`.
# Loose-as-frozen: managed via `services.economics.tier_lock` module
# below (in-memory state — Master Admin operates the surface at
# runtime; persistent registry-bump is via config file change).
_TIER_LOCK_STATE = {"locked": False, "reason_note": None}


def set_tier_lock(locked: bool, reason_note: Optional[str] = None) -> None:
    """Master-Admin-only surface — routers/pricing.py gates access.

    Locking is a GOVERNANCE decision; unlocking is another. Both write
    a Northena Ledger row via router path (governance change recording).
    """
    _TIER_LOCK_STATE["locked"] = bool(locked)
    _TIER_LOCK_STATE["reason_note"] = reason_note


def is_tier_locked() -> bool:
    return bool(_TIER_LOCK_STATE["locked"])


def _capacity_class_for(request: ObjectiveRequest_v2) -> str:
    """Map an objective's request to the fleet capacity class it consumes.

    v3 §8 bullet 5 vocabulary (three classes: mining / transforms /
    live_path). Mapping heuristic — deliberately simple until G2b:
      * qualified_data + composed_conclusion → transforms
      * knowledge_artifact + callable_skill → mining (learning-loop)
      * (MODEL is refused upstream; not reachable here)
    """
    form = request.output.form
    if form in (OutputForm.QUALIFIED_DATA, OutputForm.COMPOSED_CONCLUSION):
        return "transforms"
    return "mining"


def _shape_ref(request: ObjectiveRequest_v2) -> str:
    """Reach + output + envelope hash — instrumentation shape identifier.

    Not a security hash — a governance shape identifier for the
    §8 bullet 3 instrumentation surface.
    """
    scope_n = len(request.reach.scope_refs) if request.reach.scope_refs else 0
    return (
        f"shape:form={request.output.form.value}"
        f":grain={request.output.grain.value}"
        f":standard={request.output.standard.minimum_class.value}"
        f":scope_refs={scope_n}"
    )


async def issue_quote(
    request: ObjectiveRequest_v2,
    trace_id: str,
    warm_vs_fresh: str,
) -> Union[QuoteEnvelope_v0, AdmissionRefusal_v0]:
    """Mint one QuoteEnvelope_v0 for the given request.

    Precedence of refusal checks (per v3 §8 + Owner Ruling axes):
      1. FORM not quotable at this config bless (callable_skill / knowledge_artifact
         until §6.3/§6.4) → `form_not_offerable`.
      2. Config expired (`expires_at` past) → `exploratory_tier_expired`.
      3. Master Admin locked the current-bless tier → `pricing_tier_frozen_by_control_surface`.
      4. Fleet apportioned zero to the capacity class → `fleet_policy_reserved_zero_capacity`.

    On mint success:
      * Compute figure + qualifying_volume via price_model.
      * Compute delivery estimate + delivery_class via delivery_time (TWO bands).
      * Build QuoteEnvelope_v0 with instrumentation_seed populated.
      * Record `minted` event via instrumentation sidecar on Northena Ledger.

    HAZARD-STOP-NOTES apply per §8 bullet 1 — all figures illustrative.
    """
    price_cfg = _price_model.load_config()
    fleet_cfg = _fleet_policy.load_config()

    # 1. Form-not-quotable check.
    if not _price_model.is_form_quotable(request, price_cfg):
        return emit_form_not_offerable(request, trace_id)

    # 2. Config-expired check.
    if _expiry.is_expired(price_cfg):
        return emit_exploratory_tier_expired(request, trace_id)

    # 3. Tier-lock check.
    if is_tier_locked():
        return emit_pricing_tier_frozen_by_control_surface(request, trace_id)

    # 4. Fleet zero-capacity check for the capacity class this request consumes.
    capacity_class = _capacity_class_for(request)
    if _fleet_policy.capacity_reserved_zero(capacity_class, fleet_cfg):
        return emit_fleet_policy_reserved_zero_capacity(
            request, trace_id, capacity_class=capacity_class,
        )

    # Mint path.
    figure_str, qualifying_volume_str = _price_model.compute_figure(
        request, warm_vs_fresh, "warm_qualified" if warm_vs_fresh == "warm" else "fresh_extraction",
        cfg=price_cfg,
    )
    delivery_estimate_str, delivery_class = _delivery_time.compute_delivery_estimate(
        warm_vs_fresh, price_cfg,
    )

    price_model_version = _price_model.current_model_version(price_cfg)
    pricing_tier = _price_model.current_tier(price_cfg)

    instrumentation_seed = QuoteInstrumentationSeed_v0(
        shape_ref=_shape_ref(request),
        price_model_version=price_model_version,
        outcome="pending",
        stall_dimension=None,
        first_lever_pulled=None,
    )
    quote = QuoteEnvelope_v0(
        quote_id=f"quote-{uuid.uuid4().hex[:12]}",
        trace_id=trace_id,
        quoted_at=datetime.now(timezone.utc).isoformat(),
        price_model_version=price_model_version,
        pricing_tier=pricing_tier,
        figure=figure_str,
        qualifying_volume=qualifying_volume_str,
        delivery_estimate=delivery_estimate_str,
        delivery_class=delivery_class,
        feasible_and_offerable=True,
        instrumentation_seed=instrumentation_seed,
    )
    # Instrumentation ledger row for the `minted` event.
    await _instrumentation.record_quote_event(
        quote_envelope=quote,
        event="minted",
        objective_ref=f"objreq-{trace_id}",
        lawful_basis_ref=request.envelope.lawful_basis,
    )
    return quote
