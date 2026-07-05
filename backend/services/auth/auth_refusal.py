"""Phase 8 Stage B-1 — auth-denial 401/403 emitter (Owner E2 ratified).

Body shape: {"reason": <code>, "detail": <string>}.
NO `outcome` key. NO `outcome=refused` value. NO `AdmissionRefusal_v0`
discriminator. Auth denial is a FOURTH class OUTSIDE the three
governance render paths (composed_conclusion / admission_refusal /
infra-not-refusal). The three do not gain a fourth wearing the first's
clothes.

The bounded 4-code set lives in `auth_refusal_reasons.v0.json`
(versioned config per Ruling 3, NOT frozen contract). Every auth
denial cites one of these four codes verbatim.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from fastapi.responses import JSONResponse

AuthRefusalCode = Literal[
    "auth_missing",
    "auth_expired",
    "auth_scope_insufficient",
    "auth_identity_mismatch_for_wizard_session",
]

_REGISTRY_PATH = Path(__file__).parent / "auth_refusal_reasons.v0.json"
_registry_cache: dict | None = None


def load_registry() -> dict:
    """Load the versioned auth-refusal reason registry."""
    global _registry_cache
    if _registry_cache is None:
        with _REGISTRY_PATH.open() as f:
            _registry_cache = json.load(f)
    return _registry_cache


def emit(reason: AuthRefusalCode, detail: str | None = None) -> JSONResponse:
    """Emit an auth-denial response. Body: {reason, detail}. NO outcome key.

    HTTP status is looked up from the versioned registry:
      * auth_missing → 401
      * auth_expired → 401
      * auth_scope_insufficient → 403
      * auth_identity_mismatch_for_wizard_session → 403
    """
    reg = load_registry()
    entry = reg["reasons"].get(reason)
    if entry is None:
        # Should be impossible under Literal type constraint. Fail-fast.
        raise ValueError(
            f"auth_refusal.emit called with unknown code {reason!r} "
            "(not in auth_refusal_reasons.v0.json)."
        )
    body_detail = detail if detail else entry["detail_template"]
    return JSONResponse(
        status_code=entry["http_status"],
        content={"reason": reason, "detail": body_detail},
    )
