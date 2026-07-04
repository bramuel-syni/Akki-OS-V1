"""Economics service — Phase 6 Stage B (v3 §8).

Modules in this package land the pricing / delivery-estimate / fleet-
policy MECHANISM. Real numbers (throughput, GPU-hours, unit yield)
are BLOCKED on G2b per v3 §12 invariant #9.

Standing Owner Dispositions binding this package:
  * Ruling 5 (`pricing_tier` MUST NOT be a Literal) — pricing_tier is a
    constrained-str governed by `pricing_tiers.vN.json` registry.
  * Ruling R4-SD2 — simple apportionment holds; arbitration-under-
    contention DEFERRED (module docstring HAZARD-STOP-NOTES).
  * Ruling R3-SD2 — config-as-versioned-not-frozen; shape freezes,
    values version.
  * infra-not-refusal — capacity-unavailable = 503; fleet-policy-driven
    governance refusal = 422 AdmissionRefusal_v0 (registry v3 codes).
  * Loose-as-frozen — `figure`, `qualifying_volume`, `delivery_estimate`
    stay free-form strings until measured cut-points define narrowing.
"""
