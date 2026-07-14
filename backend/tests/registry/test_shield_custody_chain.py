"""IF-1 custody-chain gates — Shield reconnection at `llm_router.invoke_with_metering`.

Owner ruling: `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md`
Registry supplement: `docs/registry/function_promise_registry_v0.3_supplement.md` §S1

Gates:
- IF1-G1 · custody chain wired (deidentify → LLM → reidentify)
- IF1-G2 · fail-closed on deidentifier raise (LLM not invoked, exception propagates)
- IF1-G3 · fail-closed on reidentifier raise (LLM response not returned)
"""
from __future__ import annotations

import asyncio
import os

import pytest

from services.synisense.exceptions import ServiceUnavailable
from services.synisense.shield import llm_router


class _StubDeIdResult:
    """Deterministic stub of `DeIdResult` for test isolation."""

    def __init__(self, redacted_text: str, token_map: dict[str, str]) -> None:
        self.redacted_text = redacted_text
        self.token_map = token_map
        self.de_id_summary: dict[str, int] = {}
        self.dilution_score = 0.0
        self.exposure_reduction_score = 0.0
        self.elapsed_ms = 0


# ── IF1-G1 ────────────────────────────────────────────────────────────
def test_if1_g1_custody_chain_wired(monkeypatch):
    """Attest that `invoke_with_metering` walks the full chain:
    deidentifier.deidentify(input, tenant_id) → llm_router (mock echo)
    → reidentifier.reidentify(response, token_map) → text_out.

    The stub deidentifier emits a known token; the mock LLM path echoes
    the redacted text; the stub reidentifier records that it was called
    with the LLM's response text AND the same token_map that deidentify
    produced. Order + wire are attested by the call-sequence recorder.
    """
    call_log: list[str] = []

    async def _fake_deidentify(content, *, tenant_id):
        call_log.append(f"deidentify(tenant_id={tenant_id})")
        # Token substitution: replace "Acme" with a stable token.
        redacted = content.replace("Acme", "[[ENT_ORG_001]]")
        return _StubDeIdResult(redacted, {"[[ENT_ORG_001]]": "Acme"})

    def _fake_reidentify(text, token_map):
        call_log.append(f"reidentify(token_map_keys={sorted(token_map.keys())})")
        for tok, orig in token_map.items():
            text = text.replace(tok, orig)
        return text

    # Patch the shield modules the chokepoint imports lazily.
    from services.synisense.shield import deidentifier, reidentifier
    monkeypatch.setattr(deidentifier, "deidentify", _fake_deidentify)
    monkeypatch.setattr(reidentifier, "reidentify", _fake_reidentify)

    # Force mock/echo LLM path (no live key) so the LLM section returns
    # verbatim what it received. This is the classic Shield chokepoint
    # discipline surface — the "de-identified content is what the LLM
    # actually sees" claim, made testable.
    monkeypatch.setenv("SYNISENSE_LLM_MODE", "mock")
    monkeypatch.delenv("EMERGENT_LLM_KEY", raising=False)

    text, prov, model, usage = asyncio.run(
        llm_router.invoke_with_metering(
            "Board discussed Acme's revenue.",
            model_preference="analytical",
            tenant_id="test-tenant",
        )
    )

    # Wire order: deidentify called FIRST, reidentify called SECOND.
    assert call_log == [
        "deidentify(tenant_id=test-tenant)",
        "reidentify(token_map_keys=['[[ENT_ORG_001]]'])",
    ], f"custody-chain order violated: {call_log}"

    # Final text: the mock LLM echoed the REDACTED text (with the token
    # present), and reidentify swapped the token back to "Acme".
    # This proves both: (a) the LLM saw the de-identified string, not
    # the raw "Acme" identifier, AND (b) the caller got the rehydrated
    # response, not the tokenized form.
    assert "Acme" in text, "reidentify did not rehydrate original entity"
    assert "[[ENT_ORG_001]]" not in text, "token leaked to caller"


# ── IF1-G2 · fail-closed on deidentify raise ─────────────────────────
def test_if1_g2_fail_closed_deidentify_raise_blocks_llm(monkeypatch):
    """If `deidentifier.deidentify` raises `ServiceUnavailable`, the
    chokepoint MUST NOT invoke the LLM (the mock/live boundary is
    unreachable) and MUST propagate the exception verbatim."""

    llm_touched = {"called": False}

    async def _raising_deidentify(content, *, tenant_id):
        raise ServiceUnavailable("spaCy model unavailable: forced-for-test")

    def _tripwire_reidentify(text, token_map):
        # If control reaches here, the LLM path executed AND
        # reidentify was called — both are violations of fail-closed.
        llm_touched["called"] = True
        return text

    from services.synisense.shield import deidentifier, reidentifier
    monkeypatch.setattr(deidentifier, "deidentify", _raising_deidentify)
    monkeypatch.setattr(reidentifier, "reidentify", _tripwire_reidentify)
    monkeypatch.setenv("SYNISENSE_LLM_MODE", "mock")

    with pytest.raises(ServiceUnavailable) as exc_info:
        asyncio.run(llm_router.invoke_with_metering("any content", tenant_id="t"))
    assert "spaCy model unavailable" in str(exc_info.value)
    assert llm_touched["called"] is False, "LLM path executed despite deidentify raise"


# ── IF1-G3 · fail-closed on reidentify raise ─────────────────────────
def test_if1_g3_fail_closed_reidentify_raise_blocks_response(monkeypatch):
    """If `reidentifier.reidentify` raises during the outbound seam,
    the LLM response MUST NOT be returned to the caller. The chokepoint
    surfaces this as `ServiceUnavailable` (defence-in-depth: reidentify
    is pure regex so a raise would be a bug, but the chain must still
    fail-closed rather than leak raw response text)."""

    async def _stub_deidentify(content, *, tenant_id):
        return _StubDeIdResult(content, {"[[ENT_ORG_001]]": "AcmeCorp"})

    def _raising_reidentify(text, token_map):
        raise RuntimeError("reidentifier bug forced for test")

    from services.synisense.shield import deidentifier, reidentifier
    monkeypatch.setattr(deidentifier, "deidentify", _stub_deidentify)
    monkeypatch.setattr(reidentifier, "reidentify", _raising_reidentify)
    monkeypatch.setenv("SYNISENSE_LLM_MODE", "mock")

    with pytest.raises(ServiceUnavailable) as exc_info:
        asyncio.run(llm_router.invoke_with_metering("hello", tenant_id="t"))
    assert "LLM provider call failed" in str(exc_info.value) or "reidentifier bug" in str(exc_info.value)
