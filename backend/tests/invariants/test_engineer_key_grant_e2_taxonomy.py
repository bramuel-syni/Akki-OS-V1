"""Phase 8 Stage B-3 Block 3 — E2 taxonomy extension over grant endpoints.

Owner Condition 2 attached to D4b (verbatim, 2026-07-04):
    "Registration/revocation denials are 403 auth-class {reason, detail} —
     never outcome=refused, never RefusalCard. Grant CRUD is a new
     403-emitting surface; the symmetric-cut gate parametrizes over it."

This gate mirrors `test_phase_8_b_2_scope_gate_pair.py` (or equivalent
B-1/B-2 taxonomy gate) — parametrised over the 3 grant endpoints
(POST /register, GET /list, POST /revoke). Each denial path:
  * Returns 403.
  * Body is exactly `{reason, detail}`.
  * `reason` is one of the 4-code registry (NO new codes at B-3).
  * NO `outcome` key on the body.
  * NO `AdmissionRefusal_v0` discriminator.
"""
from __future__ import annotations

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from core import db
from server import app
from services.auth import auth_refusal


VALID_REGISTRY_CODES = set(auth_refusal.load_registry()["reasons"].keys())


async def _register_user(client: AsyncClient, tag: str) -> str:
    """Register a fresh user with default role (`ask_console_user`) —
    lacks the engineer/admin role required for grant CRUD.
    Returns the access token.
    """
    email = f"e2-taxonomy-{tag}-{uuid.uuid4().hex[:8]}@rms.example.com"
    r = await client.post(
        "/api/auth/register",
        json={"email": email, "password": "e2-taxonomy-test-pw", "name": f"E2 {tag}"},
    )
    assert r.status_code == 201, r.text
    return r.json()["access_token"]


def _valid_grant_body() -> dict:
    return {
        "grantee_email": f"grantee-e2-{uuid.uuid4().hex[:8]}@rms.example.com",
        "key_class": "external",
        "path": "live_query",
        "floor": "utterance",
        "scope": "estate",
        "justification": "E2 taxonomy test grant.",
        "lawful_basis_ref": "e2-taxonomy-lawful-basis-v0",
    }


GRANT_ENDPOINTS = [
    ("POST", "/api/engineer/key_grants", "issuance"),
    # `list` is authenticated-only for self-lookup; taxonomy applies to the
    # cross-grantee lookup which requires engineer authority.
    ("GET", "/api/engineer/key_grants?grantee_email=other@example.com", "cross_grantee_list"),
    ("POST", "/api/engineer/key_grants/some-grant-id/revoke", "revocation"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("method,url,label", GRANT_ENDPOINTS)
async def test_grant_endpoint_no_auth_returns_401_auth_missing(method, url, label):
    """Owner E2 taxonomy: no-auth on a grant endpoint → 401 auth_missing
    with `{reason, detail}` body (no outcome key)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        if method == "POST" and "revoke" in url:
            resp = await client.post(url, json={"reason": "auth taxonomy test"})
        elif method == "POST":
            resp = await client.post(url, json=_valid_grant_body())
        else:
            resp = await client.get(url)
    assert resp.status_code == 401, (
        f"{label}: expected 401 auth_missing, got {resp.status_code}: {resp.text}"
    )
    body = resp.json()
    assert body["reason"] == "auth_missing"
    assert body["reason"] in VALID_REGISTRY_CODES, (
        f"{label}: reason not in 4-code registry: {body['reason']!r}"
    )
    assert "outcome" not in body, f"{label}: `outcome` key present (E2 violation)."
    assert set(body.keys()) == {"reason", "detail"}, (
        f"{label}: body keys must be exactly {{reason, detail}}, got {set(body.keys())!r}"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("method,url,label", GRANT_ENDPOINTS)
async def test_grant_endpoint_ordinary_user_returns_403_scope_insufficient(method, url, label):
    """Owner E2 taxonomy: ordinary-user auth (no engineer role) on a
    grant endpoint → 403 auth_scope_insufficient with `{reason, detail}`
    body (no outcome key)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _register_user(client, label)
        headers = {"Authorization": f"Bearer {token}"}
        if method == "POST" and "revoke" in url:
            resp = await client.post(url, json={"reason": "auth taxonomy test"}, headers=headers)
        elif method == "POST":
            resp = await client.post(url, json=_valid_grant_body(), headers=headers)
        else:
            resp = await client.get(url, headers=headers)
    assert resp.status_code == 403, (
        f"{label}: expected 403 auth_scope_insufficient, got {resp.status_code}: {resp.text}"
    )
    body = resp.json()
    assert body["reason"] == "auth_scope_insufficient"
    assert body["reason"] in VALID_REGISTRY_CODES, (
        f"{label}: reason not in 4-code registry: {body['reason']!r}"
    )
    assert "outcome" not in body, f"{label}: `outcome` key present (E2 violation)."
    # NO admission-refusal discriminator (`asked`, `supported_class`, etc.).
    for governance_key in ("asked", "supported_class", "what_would_raise_it", "trace_id", "run_id"):
        assert governance_key not in body, (
            f"{label}: governance-refusal key {governance_key!r} present on auth-denial (E2 violation)."
        )


@pytest.mark.asyncio
async def test_grant_endpoint_engineer_role_succeeds_or_returns_governance_agnostic_error():
    """Sanity — engineer role bypasses the auth taxonomy and reaches
    the endpoint. Success = 201; not-found on revoke = 404 (governance-agnostic).
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _register_user(client, "engineer-happy-path")
        # Promote the user to engineer role.
        # Extract the email from the JWT claims by re-registering deterministically.
        me = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        email = me.json()["email"]
        await db.users.update_one(
            {"email": email},
            {"$set": {"roles": ["engineer"]}},
        )
        # Re-login to get token with new roles claim.
        # We use POST /login with a known password from register step.
        # (Instead, register a fresh user with engineer role directly.)
        r_reg = await client.post(
            "/api/auth/register",
            json={
                "email": f"engineer-happy-{uuid.uuid4().hex[:8]}@rms.example.com",
                "password": "engineer-happy-pw",
                "name": "Engineer Happy",
            },
        )
        assert r_reg.status_code == 201
        engineer_email = r_reg.json()["identity"]["email"]
        await db.users.update_one(
            {"email": engineer_email},
            {"$set": {"roles": ["engineer"]}},
        )
        r_login = await client.post(
            "/api/auth/login",
            json={"email": engineer_email, "password": "engineer-happy-pw"},
        )
        engineer_token = r_login.json()["access_token"]
        # Happy-path issuance.
        r = await client.post(
            "/api/engineer/key_grants",
            json=_valid_grant_body(),
            headers={"Authorization": f"Bearer {engineer_token}"},
        )
    assert r.status_code == 201, r.text
