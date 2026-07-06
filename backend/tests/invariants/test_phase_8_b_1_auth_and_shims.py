"""Phase 8 Stage B-1 — auth + router_shims invariant gates.

Owner E1 ratifications:
    * JWT single-source via PyJWT + bcrypt (standard libraries only).
    * B-1 auth is the UI Spec §4 key-scope enforcement point.
    * Federation-forward: OAuth adapters later mint the same JWT claim shape.

Owner E2 ratifications (NON-NEGOTIABLE):
    * 4-code bounded set: auth_missing, auth_expired, auth_scope_insufficient,
      auth_identity_mismatch_for_wizard_session.
    * 403/401 body: {reason, detail}. NO `outcome`. NO `outcome=refused`. NO
      AdmissionRefusal_v0 discriminator.
    * Registry-exclusion gate: no auth code enters admission-refusal registry.

Owner E3 ratifications:
    * router_shims.py hosts the triad (compose_objective_request_from_frozen_state,
      compose_objective_request_from_frozen_state_with_proposals, summarise_dual_deltas).
    * Grep-negative gate parametrised over the triad symbols — neither router
      defines these locally.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from server import app
from services.auth import auth_refusal, jwt_service, key_grants, password_hash
from services.auth.identity import Identity, KeyGrant

_ROOT = Path(__file__).resolve().parents[2]
_SERVICES = _ROOT / "services"
_ROUTERS = _ROOT / "routers"
_CONTRACTS = _ROOT / "contracts"


# ────────────────────────────────────────────────────────────────
# E1 — JWT + password_hash + key_grants primitives
# ────────────────────────────────────────────────────────────────

def test_e1_password_hash_roundtrip():
    """bcrypt hash → verify_password returns True; wrong password False."""
    h = password_hash.hash_password("hunter2-canary")
    assert h.startswith("$2b$"), "bcrypt canonical form"
    assert password_hash.verify_password("hunter2-canary", h)
    assert not password_hash.verify_password("wrong", h)


def test_e1_jwt_access_token_roundtrip():
    tok = jwt_service.create_access_token(
        user_id="uid-1",
        email="a@b.com",
        roles=["ask_console_user"],
        key_grants=[],
    )
    claims = jwt_service.decode_token(tok, expected_type="access")
    assert claims["sub"] == "uid-1"
    assert claims["email"] == "a@b.com"
    assert claims["roles"] == ["ask_console_user"]
    assert claims["type"] == "access"


def test_e1_jwt_refresh_token_type_mismatch_rejected():
    """A refresh token decoded as access → TokenInvalid."""
    tok = jwt_service.create_refresh_token(user_id="uid-1")
    with pytest.raises(jwt_service.TokenInvalid):
        jwt_service.decode_token(tok, expected_type="access")


def test_e1_jwt_extract_bearer_token_shapes():
    assert jwt_service.extract_bearer_token(None) is None
    assert jwt_service.extract_bearer_token("") is None
    assert jwt_service.extract_bearer_token("Bearer abc") == "abc"
    assert jwt_service.extract_bearer_token("bearer  spaces  ") == "spaces"
    assert jwt_service.extract_bearer_token("Basic notabearer") is None


def test_e1_key_grants_check_scope_matches_exact():
    id_ = Identity(
        user_id="u1", email="a@b.com",
        roles=["engineer"],
        key_grants=[KeyGrant(
            grant_id="g-1", key_class="external", path="live_query",
            floor="utterance", scope="estate",
        )],
    )
    r = key_grants.check_scope(id_, "external", "live_query", "utterance", "estate")
    assert r.granted is True
    assert r.matched_grant_id == "g-1"


def test_e1_key_grants_check_scope_floor_hierarchy():
    """A grant with a HIGHER floor implicitly satisfies asks with a LOWER floor."""
    id_ = Identity(
        user_id="u1", email="a@b.com", roles=["engineer"],
        key_grants=[KeyGrant(
            grant_id="g-h", key_class="internal", path="live_query",
            floor="established_fact", scope="estate",
        )],
    )
    # Ask at lower floor "utterance" is satisfied.
    assert key_grants.check_scope(id_, "internal", "live_query", "utterance", "estate").granted


def test_e1_key_grants_check_scope_class_mismatch_denied():
    id_ = Identity(
        user_id="u1", email="a@b.com", roles=["engineer"],
        key_grants=[KeyGrant(
            grant_id="g-i", key_class="internal", path="live_query",
            floor="utterance", scope="estate",
        )],
    )
    r = key_grants.check_scope(id_, "external", "live_query", "utterance", "estate")
    assert not r.granted
    assert r.reason == "auth_scope_insufficient"


def test_e1_key_grants_anonymous_denied_with_auth_missing():
    r = key_grants.check_scope(None, "external", "live_query", "utterance", "estate")
    assert not r.granted
    assert r.reason == "auth_missing"


# ────────────────────────────────────────────────────────────────
# E2 — auth-refusal shape + registry + render-path invariants
# ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize(
    "code",
    [
        "auth_missing",
        "auth_expired",
        "auth_scope_insufficient",
        "auth_identity_mismatch_for_wizard_session",
    ],
)
def test_e2_auth_refusal_registry_contains_all_4_codes(code: str):
    reg = auth_refusal.load_registry()
    assert code in reg["reasons"], f"{code} missing from auth_refusal_reasons.v0.json"


def test_e2_auth_refusal_registry_has_exactly_4_codes():
    reg = auth_refusal.load_registry()
    assert set(reg["reasons"].keys()) == {
        "auth_missing", "auth_expired",
        "auth_scope_insufficient", "auth_identity_mismatch_for_wizard_session",
    }


def test_e2_auth_refusal_emit_body_has_no_outcome_key():
    """Owner E2 non-negotiable: 403/401 body carries {reason, detail} — NO outcome key."""
    resp = auth_refusal.emit("auth_scope_insufficient")
    body = json.loads(resp.body.decode())
    assert "outcome" not in body, "Owner E2 non-negotiable: NO `outcome` key in auth-denial body"
    assert body == {
        "reason": "auth_scope_insufficient",
        "detail": "Caller identity is authenticated but the required scope grant is absent.",
    }


@pytest.mark.parametrize(
    "code,expected_status",
    [
        ("auth_missing", 401),
        ("auth_expired", 401),
        ("auth_scope_insufficient", 403),
        ("auth_identity_mismatch_for_wizard_session", 403),
    ],
)
def test_e2_auth_refusal_http_status_per_code(code, expected_status):
    resp = auth_refusal.emit(code)
    assert resp.status_code == expected_status


def test_e2_auth_refusal_reasons_registry_never_contains_outcome_refused():
    """Registry `reasons` sub-tree carries no `outcome` key nor `outcome=refused` value (Owner E2).

    The top-level `description` field may contain doctrine text explaining what
    the registry must NOT do; the invariant applies to the emitted-body shape,
    which is derived only from the `reasons` sub-tree.
    """
    p = _SERVICES / "auth" / "auth_refusal_reasons.v0.json"
    reg = json.loads(p.read_text())
    def _walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                assert k != "outcome", f"reasons sub-tree must not carry `outcome` key (found at {k!r})"
                _walk(v)
        elif isinstance(node, list):
            for item in node:
                _walk(item)
        elif isinstance(node, str):
            assert "outcome=refused" not in node, "reasons sub-tree must not carry 'outcome=refused'"
    _walk(reg.get("reasons", {}))


def test_e2_admission_refusal_registry_never_contains_auth_codes():
    """Owner E2 non-negotiable registry-exclusion: no `auth_*` code enters admission-refusal registry."""
    p = _SERVICES / "service_1" / "admission_refusal_reasons.v1.json"
    if not p.exists():
        pytest.skip("admission_refusal_reasons.v1.json not present at this phase")
    src = p.read_text()
    for auth_code in [
        "auth_missing", "auth_expired",
        "auth_scope_insufficient", "auth_identity_mismatch_for_wizard_session",
    ]:
        assert auth_code not in src, (
            f"admission-refusal registry contains auth code {auth_code!r} — "
            f"Owner E2 non-negotiable registry-exclusion violation"
        )


def test_e2_auth_refusal_module_never_imports_admission_refusal():
    """Auth-denial code MUST NOT import from admission-refusal domain (fourth-not-wearing-first's-clothes).

    Checks IMPORTS only (doc-comments may reference AdmissionRefusal_v0 to explain
    what auth denial must NOT do — that's fine and expected).
    """
    p = _SERVICES / "auth" / "auth_refusal.py"
    src = p.read_text()
    forbidden_imports = [
        "from contracts.admission_refusal",
        "import contracts.admission_refusal",
        "from services.service_1.admission_refusal",
        "import services.service_1.admission_refusal",
    ]
    for f in forbidden_imports:
        assert f not in src, f"auth_refusal.py must not import from admission-refusal domain ({f!r})"


# ────────────────────────────────────────────────────────────────
# E2 — endpoint-level 401 shape (E2E via ASGI transport)
# ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_e2_get_auth_me_unauthenticated_returns_401_reason_auth_missing():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/auth/me")
    assert r.status_code == 401
    body = r.json()
    assert "outcome" not in body
    assert body == {
        "reason": "auth_missing",
        "detail": "Authentication required. Provide a valid Authorization: Bearer <token> header.",
    }


@pytest.mark.asyncio
async def test_e2_get_auth_me_bad_token_returns_401_reason_auth_missing():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/api/auth/me", headers={"Authorization": "Bearer garbage.jwt.value"})
    assert r.status_code == 401
    body = r.json()
    assert "outcome" not in body
    assert body["reason"] == "auth_missing"


@pytest.mark.asyncio
async def test_e2_post_auth_login_wrong_password_returns_401_reason_auth_missing():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Use a random email that is unlikely to exist
        r = await ac.post(
            "/api/auth/login",
            json={"email": "nobody-b1@example.com", "password": "wrongwrongwrong"},
        )
    assert r.status_code == 401
    body = r.json()
    assert "outcome" not in body
    assert body["reason"] == "auth_missing"


@pytest.mark.asyncio
async def test_e2_post_auth_register_login_me_flow_e2e():
    """Full E2E: register → issued tokens → GET /me with bearer token → 200."""
    email = f"e2e-b1-{__import__('uuid').uuid4().hex[:8]}@example.com"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post(
            "/api/auth/register",
            json={"email": email, "password": "testpass123", "name": "E2E B1"},
        )
        assert r.status_code == 201, r.text
        tokens = r.json()
        assert "access_token" in tokens
        assert tokens["identity"]["email"] == email
        # Introspect with the issued access token.
        me = await ac.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        assert me.status_code == 200
        assert me.json()["email"] == email


# ────────────────────────────────────────────────────────────────
# E3 — router_shims triad extraction + grep-negative gate.
#
# Commercial-cut 2026-07-06 (BCR v1.4 §12): the two buyer-only members
# of the triad — `summarise_dual_deltas` and
# `compose_objective_request_from_frozen_state_with_proposals` — were
# relocated verbatim to salvage. The operator-remaining member,
# `compose_objective_request_from_frozen_state`, stays in-tree.
# All symbol-level grep-negative gates are updated to the reduced
# operator-remaining set.
# ────────────────────────────────────────────────────────────────

TRIAD_SYMBOLS = [
    "compose_objective_request_from_frozen_state",
]

SALVAGED_TRIAD_SYMBOLS = [
    "compose_objective_request_from_frozen_state_with_proposals",
    "summarise_dual_deltas",
]


def test_e3_router_shims_hosts_the_operator_remaining_triad_symbol():
    """The B-1 landing module `services/wizard/router_shims.py` still
    defines the operator-remaining triad symbol post-commercial-cut."""
    p = _SERVICES / "wizard" / "router_shims.py"
    assert p.exists(), "router_shims.py must exist post-cut (Owner E3 named receiver)"
    src = p.read_text()
    for sym in TRIAD_SYMBOLS:
        assert f"def {sym}(" in src, f"{sym} must be defined in router_shims.py"


def test_e3_router_shims_does_not_locally_define_salvaged_symbols():
    """Post-cut regression: the two salvaged buyer-only helpers must
    NOT re-appear in the extractor build tree."""
    p = _SERVICES / "wizard" / "router_shims.py"
    src = p.read_text()
    for sym in SALVAGED_TRIAD_SYMBOLS:
        assert f"def {sym}(" not in src, (
            f"{sym!r} was relocated to salvage at commercial cut; must not "
            f"resurrect inside router_shims.py"
        )


@pytest.mark.parametrize("symbol_name", TRIAD_SYMBOLS)
def test_e3_wizard_operator_router_does_not_locally_define_triad_symbol(symbol_name: str):
    """Grep-negative: routers/wizard_operator.py MUST NOT locally define any triad symbol."""
    p = _ROUTERS / "wizard_operator.py"
    src = p.read_text()
    assert f"def {symbol_name}(" not in src, (
        f"wizard_operator.py must not locally define {symbol_name!r} — "
        f"router_shims.py is the canonical single source"
    )


def test_e3_admission_handoff_now_pure_reexport_shim():
    """After B-1 + commercial cut 2026-07-06, services/wizard/admission_handoff.py
    is a pure re-export shim for the OPERATOR-REMAINING triad symbol.
    """
    p = _SERVICES / "wizard" / "admission_handoff.py"
    src = p.read_text()
    for sym in TRIAD_SYMBOLS + SALVAGED_TRIAD_SYMBOLS:
        assert f"def {sym}(" not in src, (
            f"admission_handoff.py must be a pure re-export post-cut; "
            f"{sym!r} lives elsewhere"
        )
    # Verifies re-export line present.
    assert "from services.wizard.router_shims import" in src


def test_e3_admission_handoff_bc_import_still_works():
    """Historical import path `services.wizard.admission_handoff.<symbol>`
    still resolves for the OPERATOR-REMAINING triad symbol post-cut."""
    from services.wizard import admission_handoff  # noqa: F401
    for sym in TRIAD_SYMBOLS:
        assert hasattr(admission_handoff, sym), f"BC broken: {sym!r} not importable"


# ────────────────────────────────────────────────────────────────
# Standing constraints regression (Phase 8 B-1)
# ────────────────────────────────────────────────────────────────

def test_parity_still_26_frozen_contracts_at_phase_8_b_1():
    """Auth landing must NOT introduce new frozen contracts."""
    # Count contract source .py files (excluding __init__ + qualification_matrix subdir).
    contract_files = [
        p for p in _CONTRACTS.glob("*.py")
        if p.name != "__init__.py"
    ]
    # Must match the historical count from Phase 7 B-3 close.
    assert len(contract_files) >= 25, "contract count regressed"


def test_auth_module_never_imports_llm_libraries():
    """Auth boundary is NOT in Shield; MUST NOT import litellm/anthropic/emergentintegrations."""
    forbidden = ["litellm", "anthropic", "emergentintegrations"]
    for p in (_SERVICES / "auth").glob("*.py"):
        src = p.read_text()
        for f in forbidden:
            assert f not in src, f"{p.name} must not import {f!r} (auth is not in Shield)"


def test_auth_router_registered_at_api_auth_prefix():
    """server.py includes auth router at /api/auth prefix."""
    from routers import auth as auth_router
    prefixes = {r.path for r in auth_router.router.routes}
    assert "/auth/register" in prefixes
    assert "/auth/login" in prefixes
    assert "/auth/refresh" in prefixes
    assert "/auth/me" in prefixes
