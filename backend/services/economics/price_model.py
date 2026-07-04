"""Price-model compute + versioned-config loader — Phase 6 Stage B.

Spec authority: v3 §8 bullets 1, 2, 3, 4 + §12 invariant #9.

HAZARD-STOP-NOTES (v3 §8 bullet 1 + §12 invariant #9):
  * All multipliers ILLUSTRATIVE. Real values BLOCKED on G2b.
  * `callable_skill` and `knowledge_artifact` multipliers = null;
    quote issuance refuses these forms until §6.3/§6.4 lands.
  * Buyer surface NEVER sees GPU numbers per §8 bullet 4.

Standing Owner Dispositions applied:
  * Ruling 3 config-as-versioned-not-frozen — shape freezes, values
    version. Master Admin bumps to a fresh `price-model@vN.json`;
    never in-place edit.
  * Ruling 5 — `pricing_tier` + `price_model_version` are constrained-
    str (registry-governed), not Literal.
"""
from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Dict, Optional, Tuple

from contracts.objective_request_v2 import ObjectiveRequest_v2


# Config path — Master Admin bumps by ADDING a fresh vN file and
# bumping this pointer; never in-place edit of an existing bless.
_CONFIG_PATH = Path(__file__).parent / "price_model.v0-exploratory.json"


def load_config() -> Dict:
    """Read the current-bless price-model config."""
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


def current_model_version(cfg: Dict = None) -> str:
    """Return the config's `version` field — this is the string stamped
    on every quote per §8 bullet 2 + §12 invariant #9."""
    cfg = cfg or load_config()
    return cfg["version"]


def current_tier(cfg: Dict = None) -> str:
    """Return the config's `tier` field (registry-governed name)."""
    cfg = cfg or load_config()
    return cfg["tier"]


def _reach_multiplier(request: ObjectiveRequest_v2, cfg: Dict) -> Optional[float]:
    """Pick the reach-cardinality-band multiplier from scope_refs count.

    Bands are ordered; first band whose `max_scope_refs` is either None
    (unbounded) or >= scope_refs count applies.
    """
    n_scope = len(request.reach.scope_refs) if request.reach.scope_refs else 0
    for band in cfg["levers"]["reach_cardinality_bands"]:
        cap = band.get("max_scope_refs")
        if cap is None or n_scope <= cap:
            return band.get("multiplier")
    return None


def _form_multiplier(request: ObjectiveRequest_v2, cfg: Dict) -> Optional[float]:
    """Pick form multiplier; `None` here means the form is NOT quotable
    at this config (callable_skill/knowledge_artifact until §6.3/§6.4)."""
    form_value = request.output.form.value
    return cfg["levers"]["output_form_multipliers"].get(form_value)


def _grain_multiplier(request: ObjectiveRequest_v2, cfg: Dict) -> Optional[float]:
    return cfg["levers"]["output_grain_multipliers"].get(request.output.grain.value)


def _standard_multiplier(request: ObjectiveRequest_v2, cfg: Dict) -> Optional[float]:
    return cfg["levers"]["standard_multipliers"].get(
        request.output.standard.minimum_class.value
    )


def _warm_fresh_multiplier(warm_vs_fresh: str, cfg: Dict) -> float:
    return cfg["levers"]["warm_fresh_multipliers"].get(warm_vs_fresh, 1.0)


def _delivery_class_multiplier(delivery_class: str, cfg: Dict) -> float:
    return cfg["levers"]["delivery_class_multipliers"].get(delivery_class, 1.0)


class UnquotableFormError(RuntimeError):
    """Raised when a request's form is not quotable at the current config
    (multiplier is null → §6.3/§6.4 not yet landed, or callable/knowledge)."""


def compute_figure(
    request: ObjectiveRequest_v2,
    warm_vs_fresh: str,
    delivery_class: str,
    cfg: Optional[Dict] = None,
) -> Tuple[str, str]:
    """Pure function — compute the illustrative figure + qualifying_volume.

    Returns `(figure_str, qualifying_volume_str)`.

    HAZARD-STOP-NOTE binding: all illustrative until G2b (per §8 bullet 1).
    """
    cfg = cfg or load_config()
    base = Decimal(str(cfg["levers"]["base_figure_illustrative"]))
    currency = cfg["levers"]["base_figure_currency"]

    multipliers = [
        _reach_multiplier(request, cfg),
        _form_multiplier(request, cfg),
        _grain_multiplier(request, cfg),
        _standard_multiplier(request, cfg),
        _warm_fresh_multiplier(warm_vs_fresh, cfg),
        _delivery_class_multiplier(delivery_class, cfg),
    ]
    if any(m is None for m in multipliers):
        # Some lever is off-menu at this config version. Callers should
        # NOT have reached this function; upstream (quote_service) checks
        # form quotability first.
        raise UnquotableFormError(
            f"One or more lever multipliers is null at the current "
            f"config bless. Form quotability MUST be checked upstream."
        )

    figure = base
    for m in multipliers:
        figure = figure * Decimal(str(m))
    figure = figure.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    figure_str = f"{currency} {figure}"
    scope_count = len(request.reach.scope_refs) if request.reach.scope_refs else 0
    qualifying_volume_str = (
        f"~{scope_count} scope reference(s), "
        f"{request.output.grain.value} grain, "
        f"{request.output.standard.minimum_class.value} minimum standard"
    )
    return figure_str, qualifying_volume_str


def is_form_quotable(request: ObjectiveRequest_v2, cfg: Optional[Dict] = None) -> bool:
    """Return True iff every lever multiplier is non-null for the request
    at the current config bless."""
    cfg = cfg or load_config()
    return _form_multiplier(request, cfg) is not None
