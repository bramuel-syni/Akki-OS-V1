# RMS Intelligence — Test Credentials

**Warning:** dev-only test credentials. Rotate before ship.

## Phase 8 Stage B-1 (2026-07-05) — auth landing

Seeded via `services/auth/user_store.seed_admin_if_absent(...)` at backend startup, reading ADMIN_EMAIL + ADMIN_PASSWORD from `/app/backend/.env`.

| Field | Value |
|---|---|
| Email | `admin@rms.example.com` |
| Password | `admin-b1-test-pw` |
| Roles | admin, operator, engineer, buyer, master_admin, dpo |
| Key grants | 1 (external / live_query / floor=utterance / scope=estate) |

**Auth flow for testing:**

```
# Login
curl -X POST "$REACT_APP_BACKEND_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@rms.example.com","password":"admin-b1-test-pw"}'
# → {"access_token":"...","refresh_token":"...","identity":{...}}

# Introspect
curl -H "Authorization: Bearer <access_token>" "$REACT_APP_BACKEND_URL/api/auth/me"
# → Identity JSON

# Refresh
curl -X POST -H "Authorization: Bearer <refresh_token>" "$REACT_APP_BACKEND_URL/api/auth/refresh"
# → new {access_token, refresh_token, identity}
```

**Registration:**

```
curl -X POST "$REACT_APP_BACKEND_URL/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"someone@example.com","password":"testpass123","name":"Someone"}'
# → 201 + tokens; default role `ask_console_user`, no key_grants
```

**Auth-denial shape (Owner E2 non-negotiable):**

- 401 / 403 body: `{"reason": <code>, "detail": <string>}`
- 4-code bounded set: `auth_missing`, `auth_expired`, `auth_scope_insufficient`, `auth_identity_mismatch_for_wizard_session`
- NEVER contains `outcome` key
- NEVER routed via RefusalCard
