"""Synisense Shield — outbound LLM router (post-de-id).

Phase A:
- Single provider abstraction. The route selects a provider/model based
  on the request's `model_preference` ("analytical" | "generative" |
  "balanced"). Routing logic stays simple — Phase B will expand.
- Uses the universal LLM key via `emergentintegrations`. If
  the key is missing OR the SDK is unavailable, we fall back to a
  deterministic echo response so smoke tests are hermetic in CI.
- **No cloud LLM-NER calls.** The course correction explicitly removed
  this path. NER is now local-only (spaCy) in `deidentifier.py`.

Returns: `(response_text, llm_provider, llm_model)`. The Shield route
records all three in the audit log and trust receipt.

Chunk 18 (Track 4 item 1, 2026-05-21) — `emergentintegrations.LlmChat`
moved to module-level import (was inline inside `invoke()` for the
fallback-availability check pattern). Module-level import pays the
~500ms-1s cost ONCE at process startup instead of on every first
request post-deploy. The `_EMERGENT_AVAILABLE` flag preserves the
graceful-degradation semantics — if the package isn't importable we
still fall back to the echo path on call.
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any, Dict, Literal, Optional, Tuple

from services.synisense.exceptions import ServiceUnavailable

# Chunk 18 cold-start fix — module-level import + availability probe.
# This replaces the previous inline `try: from emergentintegrations.llm.chat
# import LlmChat, UserMessage` inside invoke(). The probe runs ONCE at
# import time; subsequent invocations skip the try/except cost.
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage  # noqa: WPS433
    _EMERGENT_AVAILABLE = True
except Exception as _exc:  # noqa: BLE001
    LlmChat = None  # type: ignore[assignment]
    UserMessage = None  # type: ignore[assignment]
    _EMERGENT_AVAILABLE = False
    _EMERGENT_IMPORT_ERROR = f"{type(_exc).__name__}: {str(_exc)[:200]}"
else:
    _EMERGENT_IMPORT_ERROR = None

# Chunk 18.5 cold-start fix — lift `litellm` + `get_integration_proxy_url`
# from per-call lazy imports to module-level. The previous code paid the
# import-cache lookup + module init on every cold path even though both
# are pure-python wrappers with no side-effects worth deferring.
# Module-level matches the LlmChat probe style above + uses the same
# `_EMERGENT_AVAILABLE` flag to short-circuit on missing deps.
try:
    import litellm  # noqa: WPS433
    from emergentintegrations.llm.utils import get_integration_proxy_url  # noqa: WPS433
    _LITELLM_AVAILABLE = True
except Exception as _lite_exc:  # noqa: BLE001
    litellm = None  # type: ignore[assignment]
    get_integration_proxy_url = None  # type: ignore[assignment]
    _LITELLM_AVAILABLE = False
    _LITELLM_IMPORT_ERROR = f"{type(_lite_exc).__name__}: {str(_lite_exc)[:200]}"
else:
    _LITELLM_IMPORT_ERROR = None

log = logging.getLogger("synisense.shield.llm_router")

ModelPreference = Literal["analytical", "generative", "balanced"]

# Provider/model selection table — locked for Phase A.
_PROVIDER_TABLE: dict = {
    "analytical": ("anthropic", "claude-sonnet-4-5-20250929"),
    "generative": ("openai", "gpt-4o"),
    "balanced":   ("gemini", "gemini-2.5-flash"),
}


def _provider_for(preference: ModelPreference) -> Tuple[str, str]:
    return _PROVIDER_TABLE.get(preference, _PROVIDER_TABLE["balanced"])


# ─────────────────────────────────────────────────────────────────────
# Deterministic echo fallback. Used when EMERGENT_LLM_KEY is missing OR
# when SYNISENSE_LLM_MODE=mock. Smoke tests opt into this so they don't
# burn LLM budget. The fallback intentionally echoes the de-identified
# content verbatim so `reidentify()` has tokens to swap back, exercising
# the full pipeline.
# ─────────────────────────────────────────────────────────────────────
def _mock_invoke(de_id_content: str) -> str:
    return de_id_content


async def invoke(
    de_id_content: str,
    *,
    model_preference: ModelPreference = "balanced",
    timeout_seconds: float = 20.0,
) -> Tuple[str, str, str]:
    """Call the consumer LLM with de-identified content.

    Returns `(response_text, provider, model)`. Raises
    `ServiceUnavailable` on hard failure (timeout / SDK exception /
    network) so the Shield can fail-closed and emit a 503.

    Backwards-compatible wrapper around `invoke_with_metering`. Existing
    callers that don't need token metering keep the 3-tuple shape. The
    Shield client + the legacy `/api/synisense/shield/invoke` route both
    use `invoke_with_metering` to capture exact provider usage.
    """
    text, provider, model, _usage = await invoke_with_metering(
        de_id_content,
        model_preference=model_preference,
        timeout_seconds=timeout_seconds,
    )
    return (text, provider, model)


async def invoke_with_metering(
    de_id_content: str,
    *,
    model_preference: ModelPreference = "balanced",
    timeout_seconds: float = 20.0,
    system_msg: Optional[str] = None,
) -> Tuple[str, str, str, Dict[str, Any]]:
    """Same contract as `invoke()` but additionally returns a usage dict.

    Chunk 18 (Track 4 item 2, 2026-05-21) — token-accurate metering.

    `usage` shape:
      - Live SDK call: `{"input_tokens": int, "output_tokens": int, "method": "exact"}`
      - Mock / fallback: `{}` (caller must fall back to estimation).

    Phase 14 (2026-06-05) — `system_msg` kwarg. When provided, REPLACES
    the built-in privacy-governed system prompt for this call. When
    None (default for the 90+ existing call sites), the built-in
    prompt is preserved. This is how `routers/chat.py` injects the
    AKKI editorial persona + token-shape fluency guard rails without
    rippling into every other shield_invoke consumer.
    """
    provider, model = _provider_for(model_preference)

    # Mock mode — explicit opt-in OR no key configured.
    llm_mode = os.environ.get("SYNISENSE_LLM_MODE", "").lower()
    emergent_key = os.environ.get("EMERGENT_LLM_KEY", "").strip()
    if llm_mode == "mock" or not emergent_key:
        if not emergent_key and llm_mode != "mock":
            log.info("synisense.shield.llm_router: EMERGENT_LLM_KEY absent — using echo fallback")
        return (_mock_invoke(de_id_content), provider + ":mock", model + ":mock", {})

    # Live mode — call litellm directly so we can keep the ModelResponse
    # and pull `usage.prompt_tokens` / `usage.completion_tokens`. Module-
    # level import probe (Chunk 18 cold-start) covers the integrations SDK;
    # `_LITELLM_AVAILABLE` (Chunk 18.5) covers litellm + the proxy URL
    # helper. Both probes run ONCE at import time.
    if not _EMERGENT_AVAILABLE or not _LITELLM_AVAILABLE:
        log.warning(
            "synisense.shield.llm_router: SDK unavailable (emergent=%s litellm=%s)",
            _EMERGENT_IMPORT_ERROR or "ok",
            _LITELLM_IMPORT_ERROR or "ok",
        )
        return (_mock_invoke(de_id_content), provider + ":mock", model + ":mock", {})

    try:
        proxy_url = get_integration_proxy_url()
        if provider == "gemini":
            litellm_model = f"gemini/{model}"
        else:
            litellm_model = model  # openai, anthropic via the universal LLM proxy
        params = {
            "model": litellm_model,
            "messages": [
                {
                    "role": "system",
                    "content": system_msg if system_msg else (
                        "You are a privacy-governed assistant. The user message contains "
                        "opaque tokens of the shape [[ENT_XXX_NNN]] — preserve them "
                        "verbatim. Do not invent meanings for them. Respond concisely."
                    ),
                },
                {"role": "user", "content": de_id_content},
            ],
            "api_key": emergent_key,
            "api_base": proxy_url + "/llm",
            "custom_llm_provider": "openai",
        }
        response = await asyncio.wait_for(
            litellm.acompletion(**params),
            timeout=timeout_seconds,
        )
        # Extract text from the OpenAI-compatible response envelope.
        text = ""
        try:
            text = response.choices[0].message.content or ""
        except Exception:  # noqa: BLE001
            text = str(response)
        usage: Dict[str, Any] = {}
        try:
            u = getattr(response, "usage", None)
            prompt = int(getattr(u, "prompt_tokens", 0) or 0)
            completion = int(getattr(u, "completion_tokens", 0) or 0)
            if prompt > 0 or completion > 0:
                usage = {
                    "input_tokens": prompt,
                    "output_tokens": completion,
                    "method": "exact",
                }
        except Exception:  # noqa: BLE001 — usage is best-effort; estimation path absorbs gaps
            usage = {}
        # Suppress unused-import warnings when emergentintegrations imports
        # have already been done at module load.
        _ = (LlmChat, UserMessage)
        return (text, provider, model, usage)
    except asyncio.TimeoutError as exc:
        raise ServiceUnavailable(
            f"LLM provider timeout after {timeout_seconds}s"
        ) from exc
    except Exception as exc:  # noqa: BLE001
        log.warning("synisense.shield.llm_router: invoke failed (%s)", type(exc).__name__)
        raise ServiceUnavailable(
            f"LLM provider call failed: {type(exc).__name__}: {str(exc)[:200]}"
        ) from exc


# ─────────────────────────────────────────────────────────────────────
# Phase 7 Stage B-2 — SonnetWizardAgent (Owner ruling, 2026-07-04).
# ─────────────────────────────────────────────────────────────────────
# Owner dispatch: "Sonnet 4.6 = Emergent LLM Key. Use the standard
# Emergent LLM key path via Shield's config. Do NOT prompt for API keys."
#
# This class implements the `WizardAgent` Protocol declared at
# `services/wizard/agent_interface.py`. It stays INSIDE Shield's
# boundary so the top-level gate `test_no_direct_llm_calls_outside_shield.py`
# remains green: wizard modules import ONLY the Protocol; the LLM SDK
# calls all live here.
#
# Standing Owner Disposition #2 (`Infra-not-refusal`, [Owner ruling,
# Phase 5 Stage A close, 2026-07-04]) — any Sonnet error class
# (rate-limit, 5xx, auth, timeout, SDK exception, network fault)
# surfaces as `ServiceUnavailable` from this module; the router
# boundary translates to HTTP 503. NEVER an AdmissionRefusal_v0 /
# Service1Refusal_v0 governance envelope.
#
# No silent fallback. If Sonnet 4.6 is unavailable, we raise 503 — no
# swap to a smaller model, no fall-back to the DeterministicStubAgent,
# no re-prompt. Silent model swap on a governed surface changes shaping
# quality invisibly. Enforced by
# `test_no_silent_model_degrade_when_sonnet_4_6_unavailable`.
#
# Temperature discipline (Owner dispatch):
#   * live sessions: temperature=0.2 (default constructor arg)
#   * deterministic-replay tests: temperature=0.0 (hermetic fixture)
#
# Sync `next_turn` / `commit_review` — matches the WizardAgent Protocol
# shape at B-1. Uses `litellm.completion` (sync) so no event-loop
# bridge is needed inside FastAPI's async request context. B-1
# interface unchanged.

_SONNET_MODEL = "claude-sonnet-4-6"
_SONNET_PROVIDER = "anthropic"


def _sonnet_invoke(
    *,
    system_msg: str,
    user_msg: str,
    temperature: float = 0.2,
    timeout_seconds: float = 20.0,
) -> str:
    """Sync-callable Sonnet 4.6 invoke — Shield-boundary LLM call.

    Returns the response text OR raises `ServiceUnavailable` on any
    fault (Standing Owner Disposition `Infra-not-refusal`). No silent
    model swap; no fallback shape.
    """
    emergent_key = os.environ.get("EMERGENT_LLM_KEY", "").strip()
    if not emergent_key:
        raise ServiceUnavailable(
            "SonnetWizardAgent: EMERGENT_LLM_KEY absent — infra-not-refusal"
        )
    if not _LITELLM_AVAILABLE:
        raise ServiceUnavailable(
            f"SonnetWizardAgent: litellm SDK unavailable "
            f"({_LITELLM_IMPORT_ERROR})"
        )
    try:
        proxy_url = get_integration_proxy_url()
        response = litellm.completion(
            model=_SONNET_MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=temperature,
            api_key=emergent_key,
            api_base=proxy_url + "/llm",
            custom_llm_provider="openai",
            timeout=timeout_seconds,
        )
        try:
            text = response.choices[0].message.content or ""
        except Exception:  # noqa: BLE001
            text = str(response)
        return text
    except Exception as exc:  # noqa: BLE001
        # No silent degrade — any fault becomes ServiceUnavailable → 503.
        log.warning(
            "synisense.shield.llm_router.SonnetWizardAgent: invoke failed (%s)",
            type(exc).__name__,
        )
        raise ServiceUnavailable(
            f"SonnetWizardAgent call failed: {type(exc).__name__}: {str(exc)[:200]}"
        ) from exc


class SonnetWizardAgent:
    """Claude Sonnet 4.6 implementation of the `WizardAgent` Protocol.

    Lives inside Shield's LLM router so
    `test_no_direct_llm_calls_outside_shield.py` stays green: no LLM
    SDK import fires from `services/wizard/*`.

    Wire the constructor's `temperature` at 0.2 for live sessions,
    0.0 for hermetic replay tests. The `_invoke` seam is exposed for
    test-time monkeypatch (fixture-driven deterministic replay).
    """

    def __init__(
        self,
        *,
        temperature: float = 0.2,
        timeout_seconds: float = 20.0,
    ):
        self._temperature = float(temperature)
        self._timeout_seconds = float(timeout_seconds)

    # Test seam — hermetic replay overrides this with a fixture caller.
    def _invoke(self, system_msg: str, user_msg: str) -> str:
        return _sonnet_invoke(
            system_msg=system_msg,
            user_msg=user_msg,
            temperature=self._temperature,
            timeout_seconds=self._timeout_seconds,
        )

    def next_turn(self, state):  # -> AgentTurnResponse
        # Imported here to avoid a wizard→shield→wizard import cycle.
        from services.wizard.agent_interface import AgentTurnResponse
        from contracts.wizard_commit_state import operator_mandatory_fields

        variant = state.variant
        supplied = {
            name for name, cv in state.committed_values.items()
            if cv.source == "operator_supplied"
        }
        if variant == "operator":
            # Ask the next unmet mandatory field.
            for field_name in sorted(operator_mandatory_fields()):
                if field_name in supplied:
                    continue
                sys_msg = (
                    "You are a shaping-wizard operator agent. Ask ONE clear "
                    "question about the field named in the user turn. Do not "
                    "propose a value; ask the operator to supply it. Keep the "
                    "question one sentence, plain-language."
                )
                user_msg = (
                    f"Field to ask about: {field_name!r}. "
                    f"Session has {len(supplied)} of "
                    f"{len(operator_mandatory_fields())} mandatory fields supplied."
                )
                content = self._invoke(sys_msg, user_msg)
                return AgentTurnResponse(
                    field_asked=field_name,
                    content=content or f"Please supply a value for {field_name!r}.",
                    is_ask=True,
                )
            return AgentTurnResponse(
                field_asked=None,
                content="All mandatory fields supplied. Ready for commit review.",
                is_ask=False,
            )
        # Buyer variant: agent may propose across axes within offerability.
        # Buyer proposal emission is exercised via the buyer-router
        # /propose endpoint (Phase 7 Stage B-2 §3). For `next_turn` we
        # produce a plain conversational turn.
        sys_msg = (
            "You are a shaping-wizard buyer agent. Guide the buyer toward a "
            "feasible, offerable shape within the estate. If a proposal is "
            "warranted, mark it clearly; otherwise ask a clarifying question. "
            "Never invent lawful basis; the buyer's use_purpose drives license class."
        )
        user_msg = f"Buyer session snapshot: variant={variant}, supplied={sorted(supplied)}"
        content = self._invoke(sys_msg, user_msg)
        return AgentTurnResponse(
            field_asked=None,
            content=content or "How would you like to shape your request?",
            is_ask=True,
        )

    def commit_review(self, state):  # -> CommitReviewPayload
        # Imported here to avoid the cycle.
        from services.wizard.agent_interface import CommitReviewPayload

        payload = CommitReviewPayload()
        for name in sorted(state.committed_values):
            cv = state.committed_values[name]
            entry = {"field": name, "value": str(cv.value)}
            if cv.source == "operator_supplied":
                payload.you_supplied.append(entry)
            else:
                payload.agent_assumed_items.append(entry)
        # Commit-review render uses temperature=0.0 for determinism — a
        # governed-surface constraint (Owner dispatch). Marked-draft
        # painting is structural; we invoke Sonnet ONLY when the caller
        # wants a rendered summary blurb (deferred to B-3 UI). At B-2
        # the commit-review payload is data-only; no LLM call fires.
        return payload
