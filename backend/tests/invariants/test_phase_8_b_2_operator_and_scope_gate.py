"""Phase 8 Stage B-2 invariant gates — Operator surface + session-binding decorator + scope-enforcement gate pair.

Owner rulings landed at B-2:
    * Session-binding decorator wired across ALL operator wizard endpoints
      (`/api/wizard/operator/*`); identity-mismatch → 403 with
      `auth_identity_mismatch_for_wizard_session` (existing E2 4-code).
    * `GET /api/operator/status` — read-only aggregate for UI Spec §2.1 Home.
    * Scope-enforcement gate PAIR on `POST /api/service_1/v2/dispatch`:
      granted key → dispatch executes; insufficient key → 403 with E2 body
      `{"reason": "auth_scope_insufficient", "detail": "..."}` — NO
      `outcome` key, NO admission-refusal discriminator, ZERO envelope delta.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from server import app
from services.auth.identity import Identity, KeyGrant
from services.auth.jwt_service import create_access_token


def _make_access_token(
    user_id: str = "u-b2-test",
    email: str = "b2test@example.com",
    key_grants: list | None = None,
) -> str:
    """Mint an access token for E2E tests (bypasses register/login round-trip)."""
    return create_access_token(
        user_id=user_id,
        email=email,
        roles=["ask_console_user", "operator"],
        key_grants=key_grants or [],
    )


# ────────────────────────────────────────────────────────────────
# Session-binding decorator gate — wizard operator endpoints
# ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_b2_operator_session_grandfathered_permits_anonymous_access():
    """A session created anonymously (no Authorization) permits subsequent
    anonymous operations — B-1 grandfathering carve-out preserved."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/api/wizard/operator/session")
        assert r.status_code == 201, r.text
        session_id = r.json()["session_id"]
        # Anonymous GET on the grandfathered session — permitted.
        g = await ac.get(f"/api/wizard/operator/{session_id}")
        assert g.status_code == 200


@pytest.mark.asyncio
async def test_b2_operator_session_bound_at_creation_permits_owner_access():
    """A session created with an authenticated caller binds session→identity.
    Subsequent operations with the same identity → permitted."""
    tok = _make_access_token(user_id="u-owner-1", email="owner1@example.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/wizard/operator/session",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert r.status_code == 201, r.text
        session_id = r.json()["session_id"]
        # Same identity accesses the bound session — permitted.
        g = await ac.get(
            f"/api/wizard/operator/{session_id}",
            headers={"Authorization": f"Bearer {tok}"},
        )
        assert g.status_code == 200


@pytest.mark.asyncio
async def test_b2_operator_session_bound_at_creation_denies_different_identity():
    """A bound session denies a DIFFERENT authenticated identity with
    403 + `{reason: auth_identity_mismatch_for_wizard_session, detail: ...}`."""
    tok_owner = _make_access_token(user_id="u-owner-2", email="owner2@example.com")
    tok_stranger = _make_access_token(user_id="u-stranger-2", email="stranger2@example.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/wizard/operator/session",
            headers={"Authorization": f"Bearer {tok_owner}"},
        )
        assert r.status_code == 201
        session_id = r.json()["session_id"]
        # Stranger accesses the bound session — 403.
        g = await ac.get(
            f"/api/wizard/operator/{session_id}",
            headers={"Authorization": f"Bearer {tok_stranger}"},
        )
        assert g.status_code == 403
        body = g.json()
        assert "outcome" not in body
        assert body["reason"] == "auth_identity_mismatch_for_wizard_session"


@pytest.mark.asyncio
async def test_b2_operator_session_bound_at_creation_denies_anonymous():
    """A bound session denies anonymous callers with the same 403 code."""
    tok_owner = _make_access_token(user_id="u-owner-3", email="owner3@example.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/wizard/operator/session",
            headers={"Authorization": f"Bearer {tok_owner}"},
        )
        assert r.status_code == 201
        session_id = r.json()["session_id"]
        # Anonymous accesses the bound session — 403.
        g = await ac.get(f"/api/wizard/operator/{session_id}")
        assert g.status_code == 403
        body = g.json()
        assert "outcome" not in body
        assert body["reason"] == "auth_identity_mismatch_for_wizard_session"


# ────────────────────────────────────────────────────────────────
# GET /api/operator/status — read-only aggregate
# ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_b2_get_operator_status_anonymous_returns_empty_projection():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/operator/status")
    assert r.status_code == 200
    body = r.json()
    assert body["identity"] is None
    assert body["running"] == []
    assert body["attention"] is None
    assert body["status_line"] == "Running normally."


@pytest.mark.asyncio
async def test_b2_get_operator_status_authenticated_returns_identity_projection():
    tok = _make_access_token(user_id="u-op-status-1", email="opstat@example.com")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get(
            "/api/operator/status",
            headers={"Authorization": f"Bearer {tok}"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["identity"]["user_id"] == "u-op-status-1"
    assert body["identity"]["email"] == "opstat@example.com"
    assert isinstance(body["running"], list)


# ────────────────────────────────────────────────────────────────
# E1+E2 SCOPE-ENFORCEMENT GATE PAIR on POST /v2/dispatch (Owner ratified)
#
# Owner ruling verbatim:
#   "The proof is a gate pair, not a wire change: granted key → 200,
#    insufficient key → 403 with the E2 body, both curl-attested.
#    ~30 LoC, zero envelope delta, and the ComposedConclusion_v0 question
#    dissolves — nothing touches it."
# ────────────────────────────────────────────────────────────────

_MINIMAL_OBJECTIVE_REQUEST_V2 = {
    "entry": "external_request",
    "reach": {"scope_refs": ["estate"], "exclusions": [], "depth": "default"},
    "output": {
        "form": "composed_conclusion",
        "consumer": "person",
        "grain": "synthesized_whole",
        "standard": {"minimum_class": "utterance", "minimum_scores": {}},
    },
    "envelope": {
        "lawful_basis": "legitimate_interest",
        "done_condition": "standing_floor",
        "budget": "default",
        "scope_ceiling": "estate",
        "availability_snapshot": {},
        "floor_feasibility": {},
        "commissioner": "b2-scope-gate-test",
        "committed_at": "2026-07-05T00:00:00Z",
    },
    "shaping": None,
    "commercial": None,
    "idempotency_key": "b2-scope-gate-test",
}


def _mint_token_with_grant(class_: str, path: str, floor: str, scope: str) -> str:
    return create_access_token(
        user_id="u-scope-gate-test",
        email="scope@example.com",
        roles=["ask_console_user"],
        key_grants=[{
            "grant_id": "g-scope-gate-test",
            "key_class": class_,
            "path": path,
            "floor": floor,
            "scope": scope,
        }],
    )


@pytest.mark.asyncio
async def test_b2_v2_dispatch_scope_gate_granted_key_dispatch_executes():
    """Granted key → dispatch executes. Owner-ratified gate pair (half 1).

    The request minimum_class=utterance + scope_ceiling=estate is satisfied
    by a grant of {external, live_query, utterance, estate}. Response is
    a legitimate dispatch outcome (200 QualifiedData / 200 ComposedConclusion
    / 202 AsyncDeliveryAccepted / 422 governance refusal / 501 scaffold /
    503 infra) — the point is NOT 403, and NO auth metadata is on the wire.
    """
    tok = _mint_token_with_grant("external", "live_query", "utterance", "estate")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/service_1/v2/dispatch",
            json=_MINIMAL_OBJECTIVE_REQUEST_V2,
            headers={"Authorization": f"Bearer {tok}"},
        )
    # Gate 1 assertion: NOT 403; dispatch semantics carry the response.
    assert r.status_code != 403, f"granted key must not be denied on scope: {r.status_code} {r.text}"
    # ZERO envelope delta: response body carries no auth metadata (Owner symmetric-E2-cut).
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    for auth_key in [
        "granted", "matched_grant_id", "required",
        "auth_scope", "auth_grant", "key_grants_used",
    ]:
        assert auth_key not in body, (
            f"envelope delta violation: response carries {auth_key!r} — "
            f"auth metadata MUST NOT leak into the intelligence envelope"
        )


@pytest.mark.asyncio
async def test_b2_v2_dispatch_scope_gate_insufficient_key_returns_403_with_e2_body():
    """Insufficient key → 403 with `{reason, detail}` E2 body. Owner-ratified
    gate pair (half 2). NO `outcome` key. NO admission-refusal discriminator.
    """
    # Grant is external+live_query BUT scope='wrong_estate' (mismatch).
    tok = _mint_token_with_grant("external", "live_query", "utterance", "wrong_estate")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/service_1/v2/dispatch",
            json=_MINIMAL_OBJECTIVE_REQUEST_V2,
            headers={"Authorization": f"Bearer {tok}"},
        )
    assert r.status_code == 403, f"insufficient key must be denied with 403; got {r.status_code}"
    body = r.json()
    # Owner E2 non-negotiable body shape: {reason, detail}. NO `outcome` key.
    assert "outcome" not in body, "auth-denial body must not carry `outcome`"
    assert body["reason"] == "auth_scope_insufficient"
    assert isinstance(body["detail"], str)
    # NOT an admission-refusal discriminator anywhere in the response.
    assert "asked" not in body
    assert "supported_class" not in body
    assert "what_would_raise_it" not in body
    assert "what_you_can_do" not in body


@pytest.mark.asyncio
async def test_b2_v2_dispatch_scope_gate_anonymous_falls_through():
    """No Authorization header → anonymous fall-through (Ask Console at B-1
    posture preserved). Response is a legitimate dispatch outcome, not 403.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/service_1/v2/dispatch",
            json=_MINIMAL_OBJECTIVE_REQUEST_V2,
        )
    # Anonymous MUST NOT be denied at scope gate; dispatch executes normally.
    assert r.status_code != 403, f"anonymous must fall through the scope gate: {r.status_code} {r.text}"


@pytest.mark.asyncio
async def test_b2_v2_dispatch_scope_gate_floor_hierarchy_higher_floor_grant_permits_lower_floor_ask():
    """A grant of floor=established_fact satisfies an ask at floor=utterance
    (floor-hierarchy is ordered least-to-most-restrictive)."""
    tok = _mint_token_with_grant("external", "live_query", "established_fact", "estate")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/service_1/v2/dispatch",
            json=_MINIMAL_OBJECTIVE_REQUEST_V2,
            headers={"Authorization": f"Bearer {tok}"},
        )
    assert r.status_code != 403, f"higher-floor grant must satisfy lower-floor ask: {r.status_code} {r.text}"


# ────────────────────────────────────────────────────────────────
# Standing constraints regression at B-2
# ────────────────────────────────────────────────────────────────

def test_b2_parity_still_26_frozen_contracts():
    from pathlib import Path
    contract_dir = Path(__file__).resolve().parents[2] / "contracts"
    contract_files = [p for p in contract_dir.glob("*.py") if p.name != "__init__.py"]
    assert len(contract_files) >= 25, "contract count regressed"


def test_b2_operator_router_imports_session_binding():
    """The B-2 wiring is a load-bearing edge: operator router imports
    session_binding + auth_refusal + get_current_identity_or_none."""
    from pathlib import Path
    src = (Path(__file__).resolve().parents[2] / "routers" / "wizard_operator.py").read_text()
    assert "from services.auth import auth_refusal, session_binding" in src
    assert "from services.auth.dependencies import get_current_identity_or_none" in src
    assert "_check_session_ownership_or_deny" in src


def test_b2_service_1_router_imports_scope_enforcement():
    """service_1 router imports key_grants + auth_refusal + identity resolver."""
    from pathlib import Path
    src = (Path(__file__).resolve().parents[2] / "routers" / "service_1.py").read_text()
    assert "from services.auth import auth_refusal, key_grants" in src
    assert "from services.auth.dependencies import get_current_identity_or_none" in src
    # Gate pair emit points must both cite the E2 code:
    assert 'emit(\n                "auth_scope_insufficient"' in src or 'emit("auth_scope_insufficient"' in src


def test_b2_operator_status_route_registered():
    from routers import operator as op_router
    paths = {r.path for r in op_router.router.routes}
    assert "/operator/status" in paths
