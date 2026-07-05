"""Phase 8 Stage B-1 — auth/key model (custom JWT + bcrypt).

Owner ruling (Phase 8 Stage B-1 dispatch, E1 ratified):
  * Standard libraries only — no hand-rolled crypto (PyJWT + bcrypt).
  * B-1's auth is not just login — it is the UI Spec §4 key-scope
    enforcement point (class + path + floor + scope, server-side per
    call), and lands as such.
  * Federation is additive-later posture — the session layer must be
    shaped so OAuth can front the same session layer without breaking
    the JWT single-source. Design for federation-forward; do NOT
    implement it.

Module surface:
  * `identity.py` — Identity Pydantic model + JWT-claim shape.
  * `password_hash.py` — bcrypt password hashing (vetted library only).
  * `jwt_service.py` — PyJWT wrapping (access + refresh tokens).
  * `key_grants.py` — Per-call scope enforcement primitives ({class,
    path, floor, scope}).
  * `user_store.py` — Motor async Mongo store for users collection.
  * `session_binding.py` — Wizard session→identity binding (satisfies
    the Phase 7 B-2 §0.2 wizard session-ownership plan-debt).
  * `auth_refusal.py` — 401/403 helper emitting {reason, detail}. Owner
    E2 ratification: NO `outcome` key; NO `outcome=refused` value; NO
    `AdmissionRefusal_v0` discriminator. The three governance render
    paths do not gain a fourth member wearing the first's clothes.
  * `auth_refusal_reasons.v0.json` — versioned config for the 4-code
    bounded set (Ruling 3 pattern).
"""
