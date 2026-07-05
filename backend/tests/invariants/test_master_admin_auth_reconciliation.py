"""Phase 8 Stage B-4 — Master Admin auth reconciliation (Owner-ratified).

Owner ratification verbatim (2026-07-05):
    "RETIRE `RMS_MASTER_ADMIN_TOKEN` env-gating on the pricing + fleet
     routers — replace with JWT role-based auth requiring `master_admin`
     in `identity.roles`. Two parallel auth mechanisms on the highest-
     privilege surface is a standing confusion. Retiring closes the
     confusion."

Parametrised gate over five write endpoints × three auth postures:
  * Endpoints:
      - POST /api/pricing/tier_lock (Path A)
      - POST /api/pricing/model_version (Path B → 501)
      - POST /api/fleet/policy (Path B → 501)
      - GET  /api/master_admin/pending_seams (read)
      - GET  /api/master_admin/audit_trail (read)
  * Auth postures:
      - no-auth → 401 auth_missing with {reason, detail} body
      - authenticated non-master → 403 auth_scope_insufficient with body
      - authenticated master_admin → success path (200/501 as declared;
        NOT 401/403)

Owner Condition (Standing E2):
  * Denial body shape is EXACTLY {reason, detail} — NO `outcome` key.
  * `reason` must be one of the 4-code registry closed set. NO NEW
    codes at B-4.
  * Grep-negative gate: `X-RMS-Master-Admin` header sent alongside
    a no-JWT request MUST NOT permit access — the retired token has
    zero runtime effect.
"""
from __future__ import annotations

import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from core import db
from server import app
from services.auth import auth_refusal
from services.economics import quote_service as _quote_service


ADMIN_EMAIL = "admin@rms.example.com"
ADMIN_PASSWORD = "admin-b1-test-pw"

VALID_REGISTRY_CODES = set(auth_refusal.load_registry()["reasons"].keys())


@pytest.fixture(autouse=True)
def _reset_tier_lock_after_each_test():
    yield
    _quote_service.set_tier_lock(False, None)


# ---------- Endpoint list under audit ----------

MASTER_ADMIN_WRITE_ENDPOINTS = [
    ("POST", "/api/pricing/tier_lock",
     {"locked": True, "reason_note": "auth taxonomy test", "idempotency_key": "irrelevant"},
     200),
    ("POST", "/api/pricing/model_version", None, 501),
    ("POST", "/api/fleet/policy", None, 501),
]

MASTER_ADMIN_READ_ENDPOINTS = [
    ("GET", "/api/master_admin/pending_seams", None, 200),
    ("GET", "/api/master_admin/audit_trail", None, 200),
]

ALL_MASTER_ADMIN_ENDPOINTS = MASTER_ADMIN_WRITE_ENDPOINTS + MASTER_ADMIN_READ_ENDPOINTS


async def _login_admin(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


async def _register_ordinary_user(client: AsyncClient, tag: str) -> str:
    email = f"ma-taxonomy-{tag}-{uuid.uuid4().hex[:8]}@rms.example.com"
    resp = await client.post(
        "/api/auth/register",
        json={"email": email, "password": "ma-taxonomy-test-pw", "name": f"MA {tag}"},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["access_token"]


# ---------- Post 1: no-auth → 401 ----------


@pytest.mark.asyncio
@pytest.mark.parametrize("method,url,body,_expected", ALL_MASTER_ADMIN_ENDPOINTS)
async def test_master_admin_endpoint_no_auth_returns_401(method, url, body, _expected):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        if method == "POST":
            resp = await client.post(url, json=body or {})
        else:
            resp = await client.get(url)
    assert resp.status_code == 401, (
        f"{method} {url}: expected 401 auth_missing, got {resp.status_code}: {resp.text}"
    )
    payload = resp.json()
    assert payload["reason"] == "auth_missing"
    assert payload["reason"] in VALID_REGISTRY_CODES, (
        f"{method} {url}: reason {payload['reason']!r} not in 4-code registry."
    )
    assert "outcome" not in payload, f"{method} {url}: `outcome` key present (E2 violation)."
    assert set(payload.keys()) == {"reason", "detail"}, (
        f"{method} {url}: body keys must be exactly {{reason, detail}}, got {set(payload.keys())!r}"
    )


# ---------- Post 2: ordinary-user → 403 ----------


@pytest.mark.asyncio
@pytest.mark.parametrize("method,url,body,_expected", ALL_MASTER_ADMIN_ENDPOINTS)
async def test_master_admin_endpoint_ordinary_user_returns_403(method, url, body, _expected):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tok = await _register_ordinary_user(client, "ordinary")
        headers = {"Authorization": f"Bearer {tok}"}
        if method == "POST":
            resp = await client.post(url, json=body or {}, headers=headers)
        else:
            resp = await client.get(url, headers=headers)
    assert resp.status_code == 403, (
        f"{method} {url}: expected 403 auth_scope_insufficient, got {resp.status_code}: {resp.text}"
    )
    payload = resp.json()
    assert payload["reason"] == "auth_scope_insufficient"
    assert payload["reason"] in VALID_REGISTRY_CODES, (
        f"{method} {url}: reason {payload['reason']!r} not in 4-code registry."
    )
    assert "outcome" not in payload, f"{method} {url}: `outcome` key present (E2 violation)."
    for governance_key in ("asked", "supported_class", "what_would_raise_it", "run_id"):
        assert governance_key not in payload, (
            f"{method} {url}: governance-refusal key {governance_key!r} present on auth-denial."
        )


# ---------- Post 3: master_admin → declared success/501 ----------


@pytest.mark.asyncio
@pytest.mark.parametrize("method,url,body,expected", ALL_MASTER_ADMIN_ENDPOINTS)
async def test_master_admin_endpoint_master_admin_role_permits(method, url, body, expected):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tok = await _login_admin(client)
        headers = {"Authorization": f"Bearer {tok}"}
        # Give the tier_lock body a unique idempotency_key per test invocation
        # so it does not collide with an earlier commit in the same test session.
        if url.endswith("/pricing/tier_lock"):
            body = {
                "locked": True,
                "reason_note": "auth taxonomy master pass",
                "idempotency_key": f"ma-auth-{uuid.uuid4().hex[:10]}",
            }
        if method == "POST":
            resp = await client.post(url, json=body or {}, headers=headers)
        else:
            resp = await client.get(url, headers=headers)
    assert resp.status_code == expected, (
        f"{method} {url}: expected {expected} with master_admin role, "
        f"got {resp.status_code}: {resp.text}"
    )


# ---------- Post 4: retired header has zero effect ----------


@pytest.mark.asyncio
async def test_retired_master_admin_header_has_zero_runtime_effect():
    """Sending the retired `X-RMS-Master-Admin` header alongside a
    no-JWT request MUST still be denied — the header is not a valid
    auth vector post-B-4. Zero permit paths outside JWT."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # No Authorization header; retired header injected.
        resp = await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "retired-header",
                  "idempotency_key": "retired-header-test"},
            headers={"X-RMS-Master-Admin": "test-master-token"},
        )
    assert resp.status_code == 401, (
        f"Retired header must have zero effect. Got {resp.status_code}: {resp.text}"
    )
    payload = resp.json()
    assert payload["reason"] == "auth_missing"


# ---------- Post 5: seeded admin carries master_admin role ----------


@pytest.mark.asyncio
async def test_seeded_admin_carries_master_admin_role():
    """Baseline sanity — the seeded admin (ADMIN_EMAIL) carries the
    `master_admin` role. Without this, all subsequent gates fail
    for reasons unrelated to reconciliation."""
    doc = await db.users.find_one({"email": ADMIN_EMAIL})
    assert doc is not None, f"Seeded admin user {ADMIN_EMAIL!r} missing."
    roles = set(doc.get("roles") or [])
    assert "master_admin" in roles, (
        f"Seeded admin roles must include `master_admin`. Got: {sorted(roles)}."
    )
