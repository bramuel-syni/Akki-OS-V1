"""Phase 8 Stage B-4 — Path B honest-501 gates.

Owner ratification 2026-07-05: `POST /api/pricing/model_version` and
`POST /api/fleet/policy` are Path B endpoints — they respond 501 with a
plain-language `detail` message. The UI surface renders `detail`
verbatim in the "What changes" info box; the reason code
`requires_versioned_file_change_by_owner` is the only recognised code.

Gates:
  * Both endpoints return 501 to authenticated master_admin callers.
  * Body shape is {reason, detail}.
  * `reason` == "requires_versioned_file_change_by_owner".
  * `detail` is plain language — no `vN.json`, no `bump`, no `.py`,
    no JSON blob, no YAML fragment.
  * `outcome` key MUST NOT appear (infra-not-refusal doctrine + not a
    governance refusal).
  * NO auth-refusal registry code (bounded set) appears in `reason` — this
    is not an auth denial.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from server import app
from services.auth import auth_refusal


ADMIN_EMAIL = "admin@rms.example.com"
ADMIN_PASSWORD = "admin-b1-test-pw"

VALID_AUTH_CODES = set(auth_refusal.load_registry()["reasons"].keys())

PATH_B_ENDPOINTS = [
    ("/api/pricing/model_version", "price model"),
    ("/api/fleet/policy", "GPU capacity apportionment"),
]


async def _login_admin(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.mark.asyncio
@pytest.mark.parametrize("url,phrase_seed", PATH_B_ENDPOINTS)
async def test_path_b_endpoint_returns_501_with_reason_key(url, phrase_seed):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        resp = await client.post(url, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 501, resp.text
    body = resp.json()
    assert body["reason"] == "requires_versioned_file_change_by_owner"


@pytest.mark.asyncio
@pytest.mark.parametrize("url,phrase_seed", PATH_B_ENDPOINTS)
async def test_path_b_endpoint_detail_is_plain_language(url, phrase_seed):
    """Detail sentence is plain language — no config syntax."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        resp = await client.post(url, headers={"Authorization": f"Bearer {token}"})
    body = resp.json()
    detail = body["detail"]
    assert isinstance(detail, str) and len(detail) > 0
    # NO config syntax / no version strings.
    for forbidden in (".vN.json", ".v0.json", ".py", ".yaml", "bump", "{ ", "= "):
        assert forbidden not in detail, (
            f"{url} detail contains forbidden config syntax {forbidden!r}: {detail!r}"
        )
    # Plain-language cue words present.
    assert "Contact Owner" in detail
    assert "No change applied" in detail


@pytest.mark.asyncio
@pytest.mark.parametrize("url,phrase_seed", PATH_B_ENDPOINTS)
async def test_path_b_endpoint_body_carries_no_outcome_key(url, phrase_seed):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        resp = await client.post(url, headers={"Authorization": f"Bearer {token}"})
    body = resp.json()
    assert "outcome" not in body, (
        f"{url}: `outcome` key MUST NOT appear on Path B 501 body."
    )
    # `reason` on this endpoint is NOT an auth-refusal registry code.
    assert body["reason"] not in VALID_AUTH_CODES, (
        f"{url}: reason {body['reason']!r} must NOT be in the auth-refusal registry."
    )
    # Body keys are exactly {reason, detail}.
    assert set(body.keys()) == {"reason", "detail"}, (
        f"{url}: body keys must be {{reason, detail}}, got {set(body.keys())!r}"
    )
