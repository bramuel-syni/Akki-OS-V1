"""Commercial-cut salvage — SonnetWizardAgent + _sonnet_invoke (2026-07-06).

Extracted verbatim from `backend/services/synisense/shield/llm_router.py`
lines 224-418 at commercial cut per BCR v1.4 §12. This module implements
the `WizardAgent` Protocol via Claude Sonnet 4.6 (Emergent LLM Key).

Landed at Phase 7 Stage B-2 for the BUYER wizard variant introduction
(agent-may-propose posture per v3 §3.3 buyer semantics). Post-cut no
live consumer remains: routers/wizard_buyer.py was cut whole; the
operator wizard uses `DeterministicStubAgent` from
`services/wizard/agent_interface.py` (unchanged).

The class supports both operator and buyer variants; kept verbatim per
§12.2 preservation for possible future restoration.

Preserved dependencies (which stay in the extractor build tree):
  * `services.synisense.shield.llm_router.ServiceUnavailable`
  * `services.synisense.shield.llm_router.get_integration_proxy_url`
  * `services.synisense.shield.llm_router._LITELLM_AVAILABLE`
  * `services.synisense.shield.llm_router._LITELLM_IMPORT_ERROR`
  * `services.synisense.shield.llm_router.litellm` (import symbol)
  * `services.synisense.shield.llm_router.log` (module logger)
  * `services.wizard.agent_interface.AgentTurnResponse`
  * `services.wizard.agent_interface.CommitReviewPayload`
  * `contracts.wizard_commit_state.operator_mandatory_fields`
"""
from __future__ import annotations

import os

# The following imports are for verbatim preservation. Post-cut this
# module is NOT imported by any live consumer inside the extractor build
# tree.
try:
    import litellm  # type: ignore[import]
    _LITELLM_AVAILABLE = True
    _LITELLM_IMPORT_ERROR = None
except ImportError as exc:
    _LITELLM_AVAILABLE = False
    _LITELLM_IMPORT_ERROR = str(exc)

import logging
log = logging.getLogger(__name__)


class ServiceUnavailable(Exception):
    """Infra-not-refusal signal (Owner Standing Disposition #2)."""


def get_integration_proxy_url() -> str:
    """Stub — resurrect from Shield when restoring."""
    return os.environ.get("EMERGENT_INTEGRATION_PROXY_URL", "http://localhost:8000")


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
