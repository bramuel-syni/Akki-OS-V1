"""Synisense Shield — governance layer.

Sub-package layout (post-IF-1 chokepoint reconnection · 2026-07-14):
- `deidentifier`  : regex → tenant dict → spaCy NER (local only). LIVE via chokepoint.
- `reidentifier`  : token → original re-substitution. LIVE via chokepoint.
- `llm_router`    : outbound LLM provider call. Chokepoint carries de-id → LLM → re-id.
- `tenant_entities` : S2.onboard-era stub (empty catalogue; regex + spaCy carry).
- `trust_receipt` : HMAC-SHA256 with HKDF per-tenant key. Live via `perception_router`.
- `perception_router` : Shield-mediated perception ingress.
- `fluency_synthesizer` / `brief_synthesizer` : structured-output synthesis via chokepoint.

Shaved at IF-1 close 2026-07-14 (superseding citation:
`docs/audits/deviation_audit_v1.md` rows 1/3/4/5): `client.py`, `audit_log.py`,
`canonical.py`, `purpose_validator.py`.
"""
