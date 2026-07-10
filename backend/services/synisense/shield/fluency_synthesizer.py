"""Fluency synthesizer — Shield-side LLM boundary for Answer Fluency §3.8.

Owner scope anchor (Answer Fluency dispatch, 2026-07-10): *"LLM
synthesis of answer_text behind the Shield; frozen ComposedConclusion
envelope untouched — any contract contact is Tier-1."*

Owner ruling AF-E2 amended boundary set (2026-07-10):

    Config defects fail loud → 503:
        - Emergent key missing/invalid.

    Runtime transients degrade gracefully → mechanical arm (raised as
    specific exceptions; the caller in service_1 catches these and
    routes to `mechanical_composer.synthesise_mechanical_answer_text`):
        - Sonnet provider down / rate-limited     → LLMUnavailableError
        - Shield boundary timeout (30s)          → LLMTimeoutError
        - Structured-output parse failure         → LLMParseFailureError

**Never a refusal envelope on any transient.** Refusal taxonomy
(`admission_refusal` + `service_1_refusal`) stays closed.

Owner rationale carrier (verbatim): *"α contradicts AF-E4's own anchor.
'Upgrade path, not a replacement' — yet α makes the LLM a single point
of failure: provider down → request 503s while a complete, correct
mechanical answer sits available. The promise the anchor protects is
refusal-taxonomy closure, and the amended set honors it fully."*

**Timeout stays at 30s** per Owner Tier-3 default. Prompt template at
`fluency_prompt.v0.txt` (co-located). Sonnet model already inside
Shield via `llm_router._provider_for("analytical")` — Phase 7 Stage
B-2 precedent (SonnetWizardAgent extraction) established the boundary.

Structured-output schema (LLM MUST emit this exact top-level shape):

    {
      "prose": <str>,
      "per_sentence": [
        {"sentence_text": <str>, "unit_ids": [<str>, ...]},
        ...
      ]
    }
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from services.synisense.exceptions import ServiceUnavailable


log = logging.getLogger("synisense.shield.fluency_synthesizer")


# ─── AF-E2 amended boundary exceptions ────────────────────────────────
class EmergentKeyMissingError(Exception):
    """Emergent LLM key missing or invalid.

    Per AF-E2 amended boundary set: this is a CONFIG DEFECT that MUST
    fail loud. Upstream router surfaces this as HTTP 503. Not a
    runtime transient; not routed to mechanical arm.
    """


class LLMUnavailableError(Exception):
    """LLM provider down, rate-limited, or otherwise unavailable at runtime.

    Per AF-E2 amended: RUNTIME TRANSIENT → mechanical arm degrades
    gracefully. Never surfaced as 503; never a refusal.
    """


class LLMTimeoutError(Exception):
    """Shield boundary timeout (default 30s) exceeded.

    Per AF-E2 amended: RUNTIME TRANSIENT → mechanical arm.
    """


class LLMParseFailureError(Exception):
    """Structured-output parse failure.

    Owner-verbatim (AF-E2 amended): *"interpreted as 'LLM didn't
    answer coherently' — infra fault, not a refusal-worthy event."*
    RUNTIME TRANSIENT → mechanical arm.
    """


_PROMPT_TEMPLATE_PATH = Path(__file__).parent / "fluency_prompt.v0.txt"


def _load_prompt_template() -> str:
    return _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")


def _build_units_block(unit_id_to_text: Dict[str, str]) -> str:
    """Render the load-bearing set as a plain unit_id → text block."""
    return "\n".join(
        f"- {uid}: {text}"
        for uid, text in unit_id_to_text.items()
    )


def _validate_structured_output(payload: Any) -> Dict[str, Any]:
    """Validate the LLM's JSON payload has the required shape.

    Raises LLMParseFailureError with a specific detail on any
    structural violation.
    """
    if not isinstance(payload, dict):
        raise LLMParseFailureError(
            f"top-level payload is {type(payload).__name__}, not dict"
        )
    if "prose" not in payload or not isinstance(payload["prose"], str):
        raise LLMParseFailureError(
            "payload.prose missing or not str"
        )
    if "per_sentence" not in payload or not isinstance(payload["per_sentence"], list):
        raise LLMParseFailureError(
            "payload.per_sentence missing or not list"
        )
    for i, entry in enumerate(payload["per_sentence"]):
        if not isinstance(entry, dict):
            raise LLMParseFailureError(
                f"per_sentence[{i}] is not a dict"
            )
        st = entry.get("sentence_text")
        uids = entry.get("unit_ids")
        if not isinstance(st, str):
            raise LLMParseFailureError(
                f"per_sentence[{i}].sentence_text is not a str"
            )
        if not isinstance(uids, list) or not all(isinstance(u, str) for u in uids):
            raise LLMParseFailureError(
                f"per_sentence[{i}].unit_ids is not a list[str]"
            )
    return payload


async def _invoke_llm_raw(
    prompt: str,
    *,
    timeout_seconds: float,
) -> str:
    """Route the prompt through the Shield's existing llm_router with
    analytical preference (Sonnet in-tree).

    Distinguishes AF-E2 boundary conditions by exception type:
      * EmergentKeyMissingError — config defect (503-fail-loud).
      * LLMTimeoutError         — Shield boundary timeout.
      * LLMUnavailableError     — any other provider-side failure.

    Chokepoint discipline: this function is Shield-internal; it is the
    ONLY entry to the LLM for fluency synthesis. Service-1 callers
    invoke `synthesise_fluent_answer` (below), which in turn calls
    this. `test_no_direct_llm_calls_outside_shield` covers the
    service-1 side; AF-G6b (§6.10 AST) covers the answer_grounding
    module.
    """
    # AF-E2 amended: distinguish MISSING key (fail loud) from MOCK
    # mode (which is a runtime opt-in for hermetic tests) — MISSING
    # is a config defect; MOCK is a runtime mode. The Shield's
    # llm_router falls back to mock silently on missing key; the
    # fluency path explicitly checks and rejects.
    llm_mode = os.environ.get("SYNISENSE_LLM_MODE", "").lower()
    emergent_key = os.environ.get("EMERGENT_LLM_KEY", "").strip()
    if not emergent_key and llm_mode != "mock":
        raise EmergentKeyMissingError(
            "EMERGENT_LLM_KEY missing or empty; fluency synthesis "
            "requires a configured key OR SYNISENSE_LLM_MODE=mock. "
            "Config defect must fail loud per AF-E2 amended."
        )

    # Route through the existing Shield llm_router for the actual
    # provider call — this preserves the chokepoint discipline
    # (there is exactly ONE outbound litellm site).
    from services.synisense.shield import llm_router  # local to avoid cycles
    try:
        text, _prov, _model, _usage = await llm_router.invoke_with_metering(
            prompt,
            model_preference="analytical",
            timeout_seconds=timeout_seconds,
            system_msg=(
                "You return strict JSON only. No prose framing, no code fences, "
                "no explanation. Follow the schema in the user message exactly."
            ),
        )
    except ServiceUnavailable as exc:
        detail = str(exc)
        if "timeout" in detail.lower():
            raise LLMTimeoutError(detail) from exc
        raise LLMUnavailableError(detail) from exc
    except asyncio.TimeoutError as exc:
        raise LLMTimeoutError(str(exc)) from exc
    return text


async def synthesise_fluent_answer(
    *,
    load_bearing_unit_ids: List[str],
    unit_id_to_text: Dict[str, str],
    defensibility_class: str,
    timeout_seconds: float = 30.0,
) -> Dict[str, Any]:
    """Produce a fluent, grounded `{prose, per_sentence}` payload.

    Callable from `services/service_1/composed_conclusion.py` only;
    Shield-side chokepoint. Raises the AF-E2 amended exception set
    for the caller to catch + route:
      * EmergentKeyMissingError → caller surfaces 503 upstream.
      * LLMUnavailableError / LLMTimeoutError / LLMParseFailureError
        → caller falls through to mechanical arm.

    Does NOT emit refusal envelopes. Does NOT call the grounding gate
    (that runs in `services/service_1/answer_grounding.py` after this
    returns).
    """
    units_block = _build_units_block(unit_id_to_text)
    template = _load_prompt_template()
    prompt = (
        template
        .replace("{defensibility_class}", defensibility_class)
        .replace("{units_block}", units_block)
    )
    raw_text = await _invoke_llm_raw(prompt, timeout_seconds=timeout_seconds)
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise LLMParseFailureError(
            f"LLM output is not valid JSON: {type(exc).__name__}: "
            f"{str(exc)[:200]}"
        ) from exc
    return _validate_structured_output(payload)
