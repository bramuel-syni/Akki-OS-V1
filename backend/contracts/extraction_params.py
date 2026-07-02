"""extraction_params@v0 — frozen catalogue for the Re-extraction Handle ring.

Spec authority: RMS Spec §5.5 (`extraction_params` field declared but key
set NOT enumerated). G0 BUILD_JOURNAL "Contract ambiguities held back
from freeze" flagged this for pre-G2 hardening. Freeze pattern mirrors
`signal_ring_dimensions@v0` exactly: catalogue dict + invariant snapshot
+ bump-by-new-file (`v1.json`, never v0 mutation).

The Re-extraction Handle ring's *schema* (Pydantic model in
`contracts/five_rings.py::ReextractionHandleRing`) is BYTE-IDENTICAL to
G0 and stays that way. This module pins the *content* of the
`extraction_params` dict the schema already accepts: which keys are
mandatory per modality, which keys are reproducibility anchors, and
when a comparison is non-reproducible-by-construction.

STAKEHOLDER CORRECTION #1 — `extracted_at` is mandatory-yes,
reproducibility-anchor-NO.

  A timestamp records *when* a run happened; it does not *determine the
  output*. Two runs identical on everything but `extracted_at` should
  reproduce byte-identically. Keep `extracted_at` on the unit (useful
  provenance) but DO NOT key the V1 two-run comparison on it — that
  would chase phantom diffs. Use `reproducibility_keys(modality)` for
  the comparison, never the full mandatory set.

STAKEHOLDER CORRECTION #2 — temperature determinism stance.

  Recording `temperature` isn't enough. If temperature > 0, the
  extraction is stochastic and cannot reproduce byte-identically
  regardless of what else is pinned, which breaks the Re-extraction
  Handle's core promise. For the reproducibility path, the V1 harness
  must REQUIRE `temperature = 0` (or an equivalent future seed pin) on
  the runs it compares. A non-zero run is flagged
  `non_reproducible_by_construction=True` with the failing keys listed,
  and the harness REFUSES to assert "outputs differ → bug" — sampling
  noise is not a bug.

Implementation lives in two functions, both must be wired into the V1
harness `compare_runs()` code path:
  * `reproducibility_keys(modality)`         → subset for comparison
  * `is_deterministically_reproducible(params)` → gate before comparing

Forward note: TRANSCRIPT and COMPOSITE are catalogued for forward-shape
stability. The current `Modality` enum (frozen at G0) covers TEXT /
AUDIO / VIDEO / IMAGE / COMPOSITE; TRANSCRIPT-sourced units are
modality=TEXT today. If/when TRANSCRIPT enters the enum, this catalogue
is already shaped.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Set, Tuple


EXTRACTION_PARAMS_REV = "v0"


# ---------------------------------------------------------------------------
# Catalogue. Each leaf carries a `reproducibility_anchor` flag.
# Nested objects are declared with a `nested` schema listing their own keys.
# ---------------------------------------------------------------------------
BASE: Dict[str, Dict[str, Any]] = {
    "provider_id":       {"type": "string",    "reproducibility_anchor": True},
    "provider_version":  {"type": "string",    "reproducibility_anchor": True},
    "extraction_run_id": {"type": "string",    "reproducibility_anchor": True},
    "extracted_at":      {"type": "string",    "reproducibility_anchor": False},
}

_AUDIO_DECODING = {
    "language_hint":  {"type": "string?",  "reproducibility_anchor": True},
    "beam_size":      {"type": "integer",  "reproducibility_anchor": True},
    "temperature":    {"type": "number",   "reproducibility_anchor": True, "determinism_pin": 0},
    "vad_threshold":  {"type": "number",   "reproducibility_anchor": True},
}

_VISION_DECODING = {
    "prompt_template_id": {"type": "string",  "reproducibility_anchor": True},
    "max_tokens":         {"type": "integer", "reproducibility_anchor": True},
    "temperature":        {"type": "number",  "reproducibility_anchor": True, "determinism_pin": 0},
}

AUDIO: Dict[str, Dict[str, Any]] = {
    "sample_rate_hz":         {"type": "integer", "reproducibility_anchor": True},
    "chunk_ms":               {"type": "integer", "reproducibility_anchor": True},
    "model_decoding_params":  {"type": "object",  "reproducibility_anchor": True, "nested": _AUDIO_DECODING},
}

VIDEO: Dict[str, Dict[str, Any]] = {
    "keyframe_strategy":      {"type": "enum",    "reproducibility_anchor": True,
                               "enum": ["every_n_seconds", "scene_change", "uniform_n"]},
    "keyframe_interval_ms":   {"type": "integer?", "reproducibility_anchor": True,
                               "required_when_strategy": "every_n_seconds"},
    "keyframe_count":         {"type": "integer?", "reproducibility_anchor": True,
                               "required_when_strategy": "uniform_n"},
    "audio":                  {"type": "object?", "reproducibility_anchor": True, "nested": AUDIO},
    "vision_decoding_params": {"type": "object",  "reproducibility_anchor": True, "nested": _VISION_DECODING},
}

IMAGE: Dict[str, Dict[str, Any]] = {
    "target_resolution":      {"type": "tuple_int_int", "reproducibility_anchor": True},
    "ocr_engine":             {"type": "string?",       "reproducibility_anchor": True},
    "vision_decoding_params": {"type": "object",        "reproducibility_anchor": True, "nested": _VISION_DECODING},
}

TEXT: Dict[str, Dict[str, Any]] = {
    "source_format": {"type": "enum",    "reproducibility_anchor": True,
                      "enum": ["pdf", "docx", "pptx", "txt", "md", "rtf", "csv", "xlsx"]},
    "max_chars":     {"type": "integer", "reproducibility_anchor": True},
    "encoding":      {"type": "string",  "reproducibility_anchor": True},
    "ocr_engine":    {"type": "string?", "reproducibility_anchor": True},
}

TRANSCRIPT: Dict[str, Dict[str, Any]] = {
    "source_format":        {"type": "enum",   "reproducibility_anchor": True,
                             "enum": ["vtt", "srt", "json"]},
    "gold_transcript_hash": {"type": "string", "reproducibility_anchor": True},
}

COMPOSITE: Dict[str, Dict[str, Any]] = {
    "source_artifact_refs": {"type": "list_of_string", "reproducibility_anchor": True},
    "aggregation_strategy": {"type": "enum",           "reproducibility_anchor": True,
                             "enum": ["union", "weighted_merge", "summary"]},
}

EXTRACTION_PARAMS_V0: Dict[str, Any] = {
    "rev": EXTRACTION_PARAMS_REV,
    "base": BASE,
    "modality": {
        "audio":      AUDIO,
        "video":      VIDEO,
        "image":      IMAGE,
        "text":       TEXT,
        "transcript": TRANSCRIPT,
        "composite":  COMPOSITE,
    },
    "provider_extras_key": "provider_extras",
}


# ---------------------------------------------------------------------------
# Errors + helpers.
# ---------------------------------------------------------------------------
class ExtractionParamsViolation(ValueError):
    """Raised on validation failure of an extraction_params block."""


def _modality_catalogue(modality: str) -> Dict[str, Dict[str, Any]]:
    cat = EXTRACTION_PARAMS_V0["modality"].get(modality.lower())
    if cat is None:
        raise ExtractionParamsViolation(
            f"unknown modality {modality!r}; known: {sorted(EXTRACTION_PARAMS_V0['modality'])}"
        )
    return cat


def mandatory_keys(modality: str) -> Set[str]:
    """All TOP-LEVEL keys that must be present for this modality.

    Includes BASE keys + per-modality mandatory keys (skipping the
    `_when_strategy`-conditional ones; those are validated by
    `validate_extraction_params`, not by mere key presence).
    """
    cat = _modality_catalogue(modality)
    keys: Set[str] = set(BASE.keys())
    for k, spec in cat.items():
        t = spec.get("type", "")
        # `?` suffix marks optional-by-shape (e.g. ocr_engine, audio
        # sub-block on video). These are validated per-spec, not by
        # presence requirement on the top-level mandatory set.
        if t.endswith("?"):
            continue
        keys.add(k)
    return keys


def reproducibility_keys(modality: str) -> Set[str]:
    """Subset of `mandatory_keys(modality)` flagged as anchors.

    USE THIS for the V1 two-run comparison. Excludes `extracted_at`
    per stakeholder correction #1.
    """
    cat = _modality_catalogue(modality)
    keys: Set[str] = {k for k, s in BASE.items() if s.get("reproducibility_anchor")}
    for k, spec in cat.items():
        if spec.get("type", "").endswith("?"):
            continue
        if spec.get("reproducibility_anchor"):
            keys.add(k)
    return keys


def _collect_temperature_failures(params: Dict[str, Any], path: str = "") -> List[str]:
    """Walk nested params, return list of dotted-key paths where
    `temperature` is present and != 0. Per stakeholder correction #2,
    deterministic re-extraction requires `temperature == 0`."""
    failing: List[str] = []
    if not isinstance(params, dict):
        return failing
    for k, v in params.items():
        sub_path = f"{path}.{k}" if path else k
        if k == "temperature":
            if v != 0 and v != 0.0:
                failing.append(sub_path)
        elif isinstance(v, dict):
            failing.extend(_collect_temperature_failures(v, sub_path))
    return failing


def is_deterministically_reproducible(params: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Stakeholder correction #2 gate.

    Returns (True, []) iff every nested `temperature` field in `params`
    is exactly 0 (and any future seed pin is set — none defined at v0).
    Returns (False, [failing_dotted_keys]) otherwise. The V1 harness
    must call this before `reproducibility_keys(...)` comparison; if
    this returns False, the harness flags
    `non_reproducible_by_construction=True` and refuses to assert
    "outputs differ → bug".
    """
    failing = _collect_temperature_failures(params)
    return (len(failing) == 0, failing)


def _validate_nested(name: str, spec: Dict[str, Any], value: Any) -> None:
    """Validate a nested object against its declared sub-schema."""
    if not isinstance(value, dict):
        raise ExtractionParamsViolation(
            f"{name!r} must be an object; got {type(value).__name__}"
        )
    sub_schema = spec.get("nested", {})
    for sk, ss in sub_schema.items():
        if ss.get("type", "").endswith("?"):
            continue
        if sk not in value:
            raise ExtractionParamsViolation(
                f"{name!r}: missing required sub-key {sk!r} per v0 catalogue"
            )


def validate_extraction_params(modality: str, params: Dict[str, Any]) -> None:
    """Validate a Re-extraction Handle `extraction_params` block.

    Rules:
      * All BASE keys must be present.
      * All modality-mandatory keys must be present
        (modality is `Modality.value` — lowercase string).
      * Conditional video keys: `keyframe_interval_ms` required when
        `keyframe_strategy=="every_n_seconds"`; `keyframe_count`
        required when `keyframe_strategy=="uniform_n"`.
      * Top-level keys outside (BASE ∪ modality_keys ∪ {"provider_extras"})
        are rejected. `provider_extras` is the explicit escape hatch.
      * `provider_extras` content is free-form and NOT inspected.
    """
    if not isinstance(params, dict):
        raise ExtractionParamsViolation(
            f"extraction_params must be a dict; got {type(params).__name__}"
        )

    cat = _modality_catalogue(modality)
    allowed: Set[str] = set(BASE.keys()) | set(cat.keys()) | {"provider_extras"}
    unknown = [k for k in params.keys() if k not in allowed]
    if unknown:
        raise ExtractionParamsViolation(
            f"unknown extraction_params key(s) for modality {modality!r}: {unknown!r}. "
            f"Put provider-specific exotica under `provider_extras`."
        )

    for k in BASE:
        if k not in params:
            raise ExtractionParamsViolation(
                f"missing required BASE key {k!r} in extraction_params"
            )

    for k, spec in cat.items():
        t = spec.get("type", "")
        if t.endswith("?"):
            if k in params and t == "object?":
                _validate_nested(k, spec, params[k])
            continue
        if k not in params:
            raise ExtractionParamsViolation(
                f"missing required modality-{modality!r} key {k!r} in extraction_params"
            )
        if t == "object":
            _validate_nested(k, spec, params[k])
        if t == "enum":
            allowed_enum = spec.get("enum", [])
            if params[k] not in allowed_enum:
                raise ExtractionParamsViolation(
                    f"{k!r} must be one of {allowed_enum!r}; got {params[k]!r}"
                )

    # Conditional video keyframe gating.
    if modality.lower() == "video":
        strat = params.get("keyframe_strategy")
        if strat == "every_n_seconds" and params.get("keyframe_interval_ms") is None:
            raise ExtractionParamsViolation(
                "VIDEO: keyframe_strategy='every_n_seconds' requires keyframe_interval_ms"
            )
        if strat == "uniform_n" and params.get("keyframe_count") is None:
            raise ExtractionParamsViolation(
                "VIDEO: keyframe_strategy='uniform_n' requires keyframe_count"
            )


def known_modalities() -> List[str]:
    return sorted(EXTRACTION_PARAMS_V0["modality"].keys())
