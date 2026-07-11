"""Brief synthesizer — Shield-side LLM boundary for Opportunity Briefs §3.15.

Owner ruling OB-E1 α (2026-07-10): AF-E1 β grammar ported intact —
per-sentence structured anchor mapping, mechanical byte-verbatim
substring check via `services/opportunity_briefs/brief_grounding.py`,
whole-brief REJECT on any failure.

Boundary behaviour mirrors AF-E2 amended precedent (§0.1 disposition
AF-scope-only; briefs run under §12.1 remaining-gates posture):
  * Emergent LLM key missing/invalid → EmergentKeyMissingError (503 upstream).
  * Runtime transients (provider down · timeout · parse failure) →
    specific exceptions surfaced to the generator, which routes to
    `_generation_status ∈ {llm_unavailable, llm_timeout, llm_parse_failure}`
    and marks the brief `stale=True` (never a refusal envelope).
  * Grounding-gate REJECT (upstream) → generator routes to
    `_generation_status="grounding_reject"`; brief NOT written to
    the registry.

Structured-output schema (LLM MUST emit exactly):

    {
      "brief_text": <str>,
      "quantitative_anchors": [
        {"value": <str>, "registry_read_ref": <str>},
        ...
      ]
    }

Timeout: 30s (matches AF-E2 amended Owner Tier-3 default).
Chokepoint discipline: this module is the ONLY entry to the LLM for
brief synthesis; the pre-existing `test_no_direct_llm_calls_outside_shield`
covers upstream.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from services.synisense.exceptions import ServiceUnavailable


log = logging.getLogger("synisense.shield.brief_synthesizer")


class EmergentKeyMissingError(Exception):
    """Emergent LLM key missing/invalid — config defect → 503 fail loud."""


class LLMUnavailableError(Exception):
    """Provider down / rate-limited at runtime — degrades to stale brief."""


class LLMTimeoutError(Exception):
    """Shield boundary timeout — degrades to stale brief."""


class LLMParseFailureError(Exception):
    """Structured-output parse failure — degrades to stale brief."""


_PROMPT_TEMPLATE_PATH = Path(__file__).parent / "brief_prompt.v0.txt"


def _load_prompt_template() -> str:
    return _PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")


def _build_registry_reads_block(registry_read_texts: Dict[str, str]) -> str:
    return "\n".join(
        f"- {ref}: {text}"
        for ref, text in registry_read_texts.items()
    )


def _validate_structured_output(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise LLMParseFailureError(
            f"top-level payload is {type(payload).__name__}, not dict"
        )
    if "brief_text" not in payload or not isinstance(payload["brief_text"], str):
        raise LLMParseFailureError("payload.brief_text missing or not str")
    if "quantitative_anchors" not in payload or not isinstance(
        payload["quantitative_anchors"], list
    ):
        raise LLMParseFailureError(
            "payload.quantitative_anchors missing or not list"
        )
    for i, anchor in enumerate(payload["quantitative_anchors"]):
        if not isinstance(anchor, dict):
            raise LLMParseFailureError(
                f"quantitative_anchors[{i}] is not a dict"
            )
        v = anchor.get("value")
        r = anchor.get("registry_read_ref")
        if not isinstance(v, str) or not isinstance(r, str):
            raise LLMParseFailureError(
                f"quantitative_anchors[{i}] missing value/registry_read_ref str"
            )
    return payload


async def _invoke_llm_raw(prompt: str, *, timeout_seconds: float) -> str:
    llm_mode = os.environ.get("SYNISENSE_LLM_MODE", "").lower()
    emergent_key = os.environ.get("EMERGENT_LLM_KEY", "").strip()
    if not emergent_key and llm_mode != "mock":
        raise EmergentKeyMissingError(
            "EMERGENT_LLM_KEY missing or empty; brief synthesis "
            "requires a configured key OR SYNISENSE_LLM_MODE=mock."
        )
    from services.synisense.shield import llm_router
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


async def synthesise_brief(
    *,
    scope: str,
    contributing_slices: List[str],
    registry_read_texts: Dict[str, str],
    timeout_seconds: float = 30.0,
) -> Dict[str, Any]:
    """Produce a validated `{brief_text, quantitative_anchors}` payload.

    Raises:
      EmergentKeyMissingError — config defect (503 upstream).
      LLMUnavailableError / LLMTimeoutError / LLMParseFailureError —
      runtime transient (caller routes to stale-brief marking).
    """
    template = _load_prompt_template()
    prompt = (
        template
        .replace("{scope}", scope)
        .replace("{contributing_slices}", ", ".join(contributing_slices))
        .replace("{registry_reads_block}", _build_registry_reads_block(registry_read_texts))
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
