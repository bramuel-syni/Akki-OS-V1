"""Phase 8 Stage B-3 Block 3 — Buyer-variant session-binding gates.

Owner mandate (verbatim, attached to D4b Block 3):
    "Wire `services/auth/session_binding.py` decorator across all buyer
     wizard endpoints (`/api/wizard/buyer/{sid}/*` — 8 endpoints per B-3
     close). Mirror the operator-variant wiring from B-2. Mismatch →
     403 `auth_identity_mismatch_for_wizard_session`."

The buyer-variant gate mirrors `test_wizard_operator_session_binding.py`
in shape. It parametrises over all buyer POST /{sid}/* endpoints + GET
/{sid}, asserting that each returns 403 with the 4-code registry code
`auth_identity_mismatch_for_wizard_session` when the caller identity
does not match the bound session.
"""
from __future__ import annotations

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from server import app


async def _register_and_login(client: AsyncClient, tag: str) -> tuple[str, str]:
    email = f"buyer-binding-{tag}-{uuid.uuid4().hex[:8]}@rms.example.com"
    password = "buyer-binding-test-pw"
    r = await client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "name": f"Buyer {tag}"},
    )
    assert r.status_code == 201, r.text
    tok = r.json()["access_token"]
    return email, tok


async def _open_bound_buyer_session(client: AsyncClient, token: str) -> str:
    r = await client.post(
        "/api/wizard/buyer/session",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 201, r.text
    return r.json()["session_id"]


BUYER_MISMATCH_ENDPOINTS = [
    # (method, path_suffix, body)
    ("POST", "/turn", {}),
    ("POST", "/propose", {"axes_changed": [], "proposal_content": "test"}),
    ("POST", "/agent-assumption", {"field": "reach", "inferred_value": "test", "evidence_ref": "test"}),
    ("POST", "/commit-review", None),
    ("POST", "/freeze", {}),
    ("POST", "/handoff", {}),
    ("GET", "", None),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("method,suffix,body", BUYER_MISMATCH_ENDPOINTS)
async def test_buyer_session_endpoint_denies_wrong_identity_with_4code_registry(
    method: str, suffix: str, body,
):
    """Owner Block 3 mandate: buyer-variant session-binding denies
    cross-identity access with the 4-code registry code
    `auth_identity_mismatch_for_wizard_session`.

    Parametrised across all 7 non-creation endpoints (POST /turn,
    /propose, /agent-assumption, /commit-review, /freeze, /handoff +
    GET /{sid}).

    Note: POST /session is NOT in this parametrisation — it's the
    creation surface, always permitted for any authenticated caller.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        _, tok_creator = await _register_and_login(client, "creator")
        _, tok_intruder = await _register_and_login(client, "intruder")
        sid = await _open_bound_buyer_session(client, tok_creator)
        url = f"/api/wizard/buyer/{sid}{suffix}"
        headers = {"Authorization": f"Bearer {tok_intruder}"}
        if method == "POST":
            resp = await client.post(url, json=(body or {}), headers=headers)
        else:
            resp = await client.get(url, headers=headers)
    assert resp.status_code == 403, (
        f"{method} {suffix}: expected 403, got {resp.status_code}: {resp.text}"
    )
    body_json = resp.json()
    assert body_json.get("reason") == "auth_identity_mismatch_for_wizard_session", (
        f"{method} {suffix}: wrong reason. Full body: {body_json!r}. "
        "The 4-code registry MUST close at B-3 without new codes."
    )
    # No `outcome` key on auth-denial (E2 symmetric cut).
    assert "outcome" not in body_json, (
        f"{method} {suffix}: `outcome` key present on auth-denial body "
        f"({body_json!r}). E2 taxonomy: NO outcome key on 4-code denials."
    )


@pytest.mark.asyncio
async def test_buyer_session_creation_binds_identity_to_session():
    """Session created under Bearer token → binding recorded.
    Subsequent same-identity access permitted."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        _, tok = await _register_and_login(client, "self")
        sid = await _open_bound_buyer_session(client, tok)
        # Same-identity read is permitted.
        r = await client.get(
            f"/api/wizard/buyer/{sid}",
            headers={"Authorization": f"Bearer {tok}"},
        )
    assert r.status_code == 200, r.text
    assert r.json()["session_id"] == sid


@pytest.mark.asyncio
async def test_buyer_grandfathered_session_permits_anonymous_operations():
    """Session created WITHOUT a Bearer token (grandfathered) → no
    binding recorded → anonymous operations permitted (mirrors operator
    B-2 semantic)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/api/wizard/buyer/session")
        assert r.status_code == 201
        sid = r.json()["session_id"]
        # Anonymous GET works.
        r2 = await client.get(f"/api/wizard/buyer/{sid}")
    assert r2.status_code == 200, r2.text
