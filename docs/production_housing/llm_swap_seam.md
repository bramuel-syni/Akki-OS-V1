# LLM swap seam (PH-R1 · PH-E4 α + Owner addition)

**Landing:** 2026-07-10 · Owner ruling PH-E4 α + documentation-addition clause.
**Standing Rule v3:** on-disk canonical.

---

## §1. Owner ruling (verbatim)

> **PH-E4 — α, one addition inside the same ruling:** document the seam, defer the rename — correct, "contained + documented" is the PH-R1 clause and β is a mid-flight refactor with no honesty gain. **Addition:** the seam doc records the BCR annex shape as the binding migration target with its call-site inventory (the two post-cut call sites named), so the PH-R4 swap executes against a written target rather than rediscovering the seam. Documentation content, zero code, no cell change.

**BCR v1.5 §3.4 annex verbatim (target shape):**

> LLM swap seam (single module)
>   llm_router.complete(messages, temperature, model) -> text
>   provider selection reads LLM_PROVIDER; call sites never change

---

## §2. Current shape (PH-R1 landing)

**Module:** `/app/backend/services/synisense/shield/llm_router.py`

**Public function surface:**

```python
async def invoke_with_metering(
    prompt: str,
    model_preference: ModelPreference,          # str: "analytical" | "creative" | ...
    timeout_seconds: float,
    system_msg: str | None = None,
) -> tuple[str, str, str, dict]:
    """Returns (text, provider, model, usage_dict)."""
```

**Private dispatch:** `_provider_for(preference: ModelPreference) -> tuple[str, str]` maps preference → `(provider_id, model_id)`. Providers currently supported: **emergent** (Emergent LLM key routing to Anthropic Sonnet 4.6 via `emergentintegrations` SDK).

---

## §3. Single-source discipline attest

The single-router discipline is **mechanically enforced** via `backend/tests/invariants/test_no_direct_llm_calls_outside_shield.py` — an AST/grep-negative gate that rejects any non-Shield import of an LLM SDK.

**Attested at:** PH-G4 (test_llm_swap_seam_doc_exists_and_records_target_shape).

---

## §4. Call-site inventory (Owner addition · post-cut)

Per Owner PH-E4 documentation addition — the two post-cut call sites that consume `invoke_with_metering(...)` and will migrate to the BCR annex `complete(...)` shape at PH-R4 owner-side swap:

### §4.1 Answer Fluency post-Shield synthesis

- **File:** `/app/backend/services/synisense/shield/fluency_synthesizer.py`
- **Line:** L182
- **Current call:**
  ```python
  text, _prov, _model, _usage = await llm_router.invoke_with_metering(
      prompt=composed_prompt,
      model_preference="analytical",
      timeout_seconds=FLUENCY_TIMEOUT_SECONDS,
      system_msg=FLUENCY_SYSTEM_MSG,
  )
  ```
- **Post-swap target:**
  ```python
  text = await llm_router.complete(
      messages=[{"role": "system", "content": FLUENCY_SYSTEM_MSG},
                {"role": "user",   "content": composed_prompt}],
      temperature=FLUENCY_TEMPERATURE,   # Tier-3 default value locked here
      model=FLUENCY_MODEL,
  )
  ```
- **Metering:** current `invoke_with_metering` returns `usage_dict`; the `complete(...)` target does not. Metering moves to a Shield-side wrapper decorator OR to a separate `record_usage(...)` helper. Owner-side PH-R4 ruling required before landing.

### §4.2 Opportunity Briefs post-Shield synthesis

- **File:** `/app/backend/services/synisense/shield/brief_synthesizer.py`
- **Line:** L116
- **Current call:**
  ```python
  text, _prov, _model, _usage = await llm_router.invoke_with_metering(
      prompt=composed_prompt,
      model_preference="analytical",
      timeout_seconds=BRIEF_TIMEOUT_SECONDS,
      system_msg=BRIEF_SYSTEM_MSG,
  )
  ```
- **Post-swap target:**
  ```python
  text = await llm_router.complete(
      messages=[{"role": "system", "content": BRIEF_SYSTEM_MSG},
                {"role": "user",   "content": composed_prompt}],
      temperature=BRIEF_TEMPERATURE,
      model=BRIEF_MODEL,
  )
  ```

---

## §5. Migration target (binding for PH-R4)

**Target function signature (BCR annex verbatim):**

```python
async def complete(
    messages: list[dict[str, str]],   # OpenAI-style [{"role", "content"}]
    temperature: float,
    model: str,                        # provider-agnostic model ID
) -> str:
    """Provider dispatch via LLM_PROVIDER env var; call sites never change."""
```

**Provider selection contract:**
- `LLM_PROVIDER=emergent` (current default) → Emergent LLM key → underlying Sonnet 4.6 dispatch (unchanged).
- `LLM_PROVIDER=anthropic` (post-PH-R4 owner-side swap) → off-platform `LLM_API_KEY` → direct Anthropic API.

**Invariants preserved at PH-R4 swap:**
- Zero call-site change beyond migrating to the new signature.
- `test_no_direct_llm_calls_outside_shield` gate remains green (single-source discipline).
- Refusal taxonomy unchanged (config defects fail-loud 503; runtime transients → mechanical arm per AF-E2 amended).
- Model selection stays inside the shield (no call site passes provider details).

---

## §6. Non-invocation at PH-R1

**Zero code change to `llm_router.py` at PH-R1.** The rename lands post-PH-R4 [OWNER] LLM account swap. This doc is the written target for that swap — no rediscovery of the seam required.

**Attested at:** PH-G4 (test_llm_swap_seam_doc_exists_and_records_target_shape + test_llm_swap_seam_call_site_inventory_matches_repo).

═══════════════════════════════════════════════════════════════════

*End of LLM swap seam documentation. On-disk canonical per Standing Rule v3. Migration target recorded verbatim to BCR v1.5 §3.4 annex. Call-site inventory: 2 post-cut (fluency_synthesizer L182 + brief_synthesizer L116). Zero code change at PH-R1.*
