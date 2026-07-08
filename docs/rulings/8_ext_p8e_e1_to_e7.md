# 8-EXT Owner Rulings — P8E-E1 through P8E-E7 (2026-07-08)

**Dispatch context:** Owner GREEN-LIGHT on 8-EXT execution (Message 340, 2026-07-08).
**Authority-source:** Owner rulings on the 7 escalations enumerated in `/app/docs/stage_a_proposals/8_ext.md` §5.

**Standing Rule v3:** verbatim rulings landed here on disk. Reply body carries SHA + one-line quotes only.

---

## P8E-E1 — `external_engineer` role addition to Identity RoleName Literal

**Ruling:** α — additive Literal expansion.

**Owner verbatim:** *"α, no bump. Identity is service-layer and unfrozen by explicit ruling; expanding a service-layer Literal from 7 to 8 role names is the definition of additive. V1-G7 assertion set stays at 28 — the frozen contract snapshot bijection is untouched. Bumping Identity to `Identity_v2` here would confuse two disciplines: frozen-contract versioning (which we reserve for envelope-wire schemas) and role-registry growth (which is a service-layer additive concern). The 4-code auth registry is also unchanged — role identity is not a refusal code."*

**Discipline attestation carried:** V1-G7 assertion set unchanged at 28.

---

## P8E-E2 — Server-side own-scope gate placement (dedicated helper)

**Ruling:** α + one condition — dedicated helper is the single source.

**Owner verbatim:** *"α, one condition. The dedicated helper is not a 'parallel mechanism' — EE-R4's prohibition protects B-1's scope-tuple primitive from duplication; own-scope is a different check (caller identity vs resource owner) and gets its own single source. Condition: the helper is provably the single source — grep-negative gate over inline owner-comparison patterns in the engineer router."*

**Condition attested:** `test_engineer_router_has_no_inline_owner_comparisons` (grep-negative on 5 inline-comparison patterns) GREEN.

---

## P8E-E3 — Onboarding invite-token shape (DB-persisted invite row)

**Ruling:** α + condition — DB-persisted invite row; JWT minted at approval time; NO new JWT class.

**Owner verbatim:** *"α. DB-persisted invite row, external_engineer JWT minted at approval time, no new JWT class — 'JWT mechanics unchanged' honored literally. Invite-row mechanics (expiry, single-use) are dev defaults stated at close."*

**Dev defaults stated at close (per condition):**
- `expiry_duration_hours: 168` (7 days).
- `single_use: True` — approval endpoint uses atomic `find_one_and_update` with `state=pending_invite` filter; second approve on the same invite_id returns 404 `invite_not_approvable` (idempotent-single-use).
- JWT minted at approval uses standard `create_access_token()` path (attested by `test_approval_mints_standard_access_jwt_no_new_class` — `claims.type == "access"`).

---

## P8E-E4 — EE-G3 admin/fleet 403 code reuses existing 4-code registry

**Ruling:** α — all external-scope denials use `auth_scope_insufficient`. 4-code registry stays closed.

**Owner verbatim:** *"α. Matches EE-R1 verbatim and P9-E3 α condition 1 pre-carry. Every external-scope denial in 8-EXT — foreign-resource, admin-fleet-route, or foreign-invite-write — uses auth_scope_insufficient. Zero new codes."*

**Attestation:** `test_auth_refusal_registry_still_closed_at_four_codes` GREEN — registry keys are exactly {`auth_missing`, `auth_expired`, `auth_scope_insufficient`, `auth_identity_mismatch_for_wizard_session`}.

---

## P8E-E5 — `internal_engineer` role naming — retain `engineer` as internal identifier

**Ruling:** α — retain `engineer` as the internal-engineer identifier; add `external_engineer` only.

**Owner verbatim:** *"α. Retain `engineer` as internal; add `external_engineer` only. `engineer` ≡ the matrix's internal_engineer column — descriptive label, not a role to mint. Nobody creates the synonym later."*

**Attestation:** `test_ee_g1_external_engineer_role_present_in_literal` GREEN — assertions:
- `"external_engineer" in RoleName.__args__` ✓
- `"engineer" in RoleName.__args__` ✓ (retained)
- `"internal_engineer" not in RoleName.__args__` ✓ (no synonym minted)

---

## P8E-E6 — UI Spec §5.4 binding copy em-dash preservation

**Ruling:** α — preserve em-dash "—" (U+2014) verbatim on §5.4 binding copy.

**Owner verbatim:** *"α. P9-E6 pattern applies. Em-dash on syntactic pauses is not a list separator; middle-dot substitution is a mis-application of E7. Jest anti-slop-gate on U+2014 character code is the enforcement."*

**Attestation:** `test_page_mounts_with_binding_copy_verbatim_including_em_dash_U_2014` GREEN — spec-line text contains `\u2014`, `charCodeAt` == `0x2014`, ≠ `0x002D` (hyphen), ≠ `0x2013` (en-dash).

---

## P8E-E7 — Ledger emission on onboarding approval (new `stamp_audit.data_class` variant)

**Ruling:** α + condition — additive new `data_class` variant `engineer_onboarding_approved` in `data_class_registry.v3.json`. No frozen contract touched.

**Owner verbatim:** *"α. Ratifies the pattern from B5b-E4 verbatim: registry v2→v3 is additive-only, existing classes preserved byte-identical, new class landing brings its consumers with it (deletion_ledger loader re-point). NorthenaLedgerRow_v1 shape untouched — `stamp_audit.data_class` is a sidecar-string slot from the start. Condition: v2 file must remain byte-identical on disk (never mutated in place); deletion_ledger.py re-pointer is a single-line change validated by test."*

**Attestations:**
- `test_data_class_registry_v3_landed_additive_from_v2` GREEN — v2 preserved on disk; v3 is superset of v2 by exactly one new entry (`engineer_onboarding_approved`).
- `test_deletion_ledger_loader_repointed_to_v3` GREEN — `deletion_ledger.py` contains string `data_class_registry.v3.json`.
- v2 SHA-256 (byte-identical, unchanged): `ad413644cfbf7c44260ad26f3dc0b9392a7e8b0015c425ce381650d379168e2c`.
- v3 SHA-256 (new, additive): `5c36a1ccab4b9fb6b1571f04aa950ef27b718ad0383c8bcdb750c8068ab421a7`.

═══════════════════════════════════════════════════════════════════

*End of 8-EXT rulings record. Standing Rule v3: verbatim on-disk. Reply body carries SHA + one-line quotes only.*
