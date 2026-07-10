# Transform Forms · Owner Rulings TF-E1 through TF-E4 (2026-07-08)

**Dispatch context:** Owner rulings message post-Stage-A relay of the 4 Tier-1 escalations (governance §4.4). Rulings arrived in a single Owner message with the execute directive baked in ("pre-flight → atomic first-commit → close").

**Governance model:** 3-tier ruling model per `docs/governance/tiered_ruling_model.md` (adopted 2026-07-08; §6.7 snapshot rate codified post-AS; §8 data-blind posture landed at TF close 2026-07-09).

**Standing Rule v3:** verbatim rulings on-disk. Reply carries SHA + one-line quotes only.

---

## TF-E1 — Knowledge Artifact contract shape (additive parity 29→30)

**Ruling:** α — single top-level `KnowledgeArtifactV0` with nested Node/Edge sub-models.

**Owner verbatim:** *"α. Single top-level KnowledgeArtifactV0, Node/Edge as nested sub-models, parity 29→30. The wire is one document (ka.v0); one contract is the honest count. β is wire-identical at triple the snapshots — ~310 LoC of ceremony for zero external difference. γ abandons the discipline on the exact surface external parties consume."*

**Landing:**
- `backend/contracts/knowledge_artifact_v0.py` — `KnowledgeArtifactV0` + `KnowledgeArtifactNode` + `KnowledgeArtifactNodeDefensibility` + `KnowledgeArtifactNodeProvenance` + `KnowledgeArtifactEdge` in one file. Sub-models emit under `$defs` in the auto-generated JSON schema (attested by `test_tf_g1_ka_v0_frozen_and_snapshot_present` GREEN).
- Parity 29 → 30 (+1 additive; 29 pre-existing byte-identical).

---

## TF-E2 — Callable Skill provisioning record shape (parity 30→31)

**Ruling:** α — frozen contract; parity 31 honest.

**Owner verbatim:** *"α. Internal-vs-external is not the test; promise-load-bearing is. The provisioning record carries slice-freeze — 'the corpus you provisioned is the corpus you're querying' is a buyer-facing promise, and the record enforcing it gets the same shape-drift protection as any external wire. Parity 31 honest. The ~175 LoC saving is Tier-2; the promise is Tier-1."*

**Landing:**
- `backend/contracts/callable_skill_provisioning_v0.py` — `CallableSkillProvisioningV0` frozen contract with `ConfigDict(extra="forbid", frozen=True)`.
- Parity 30 → 31 (+1 additive; total 31).

---

## TF-E3 — `defensibility.class` field type + registry seed condition

**Ruling:** α + one condition — constrained-str + versioned registry, single-source vocabulary.

**Owner verbatim:** *"α, one condition: single-source the class vocabulary. Settled doctrine (CK-I1 never-a-widening-Literal; registry precedents at B-5b/8-EXT/AS). Condition: defensibility_classes.v0.json is seeded verbatim from the class vocabulary the production composition path emits today and becomes the canonical registry going forward — existing frozen contracts stay byte-identical; no second vocabulary may diverge from this one. Gate added: registry ⊇ every class the live composition path can emit. ~+1 cell, disclosed at close."*

**Landing:**
- `backend/services/transform_forms/defensibility_classes.v0.json` seeded VERBATIM from `contracts/five_rings.py::DefensibilityClass` = `{"fact", "utterance", "non_factual"}`.
- `backend/services/transform_forms/defensibility_loader.py` — `ALLOWED_DEFENSIBILITY_CLASSES` frozenset + `validate_defensibility_class()`.
- `KnowledgeArtifactNode.defensibility.class_` (aliased to `class`) is `constrained-str, min_length=1`, validated through the loader at KA assembly time.
- Existing frozen contracts (`five_rings.DefensibilityClass` Enum + `mtafiti_registry.MtafitiRegistryRecord.defensibility_class` Literal) preserved byte-identical.

**TF-G8 registry-superset gate landed:** `test_tf_g8_defensibility_registry_superset_live_composition_path` GREEN (asserts `live_classes ⊆ ALLOWED_DEFENSIBILITY_CLASSES`) + `test_tf_g8_no_second_vocabulary_diverges_from_registry` GREEN (asserts `mtafiti_registry` Literal args equal `ALLOWED_DEFENSIBILITY_CLASSES`).

---

## TF-E4 — Callable Skill per-call inner gate + slice-freeze mechanism

**Ruling:** (a) α + (b) α AND β together — belt-and-suspenders.

**Owner verbatim:** *"(a) α; (b) α and β together, not either. (a) decorator composing the P8E-E2 single-source scope check + floor check + class-inline mutation — mechanism-not-convention; middleware rejected (route-drift leak); γ rejected (call-site convention). (b) α is the load-bearing enforcement — write-once at provisioning, no update_one on corpus_slice_ref, grep-negative gate over the codebase (Condition-2 pattern) — the persisted record is the actual attack surface. β rides along: ConfigDict(frozen=True) on the new contract at creation — in-memory hardening, one line, part of the initial snapshotted shape. Enforced by structure, proven by gate, hardened in memory."*

**Landing:**

### (a) α · Inner gate = decorator (mechanism-not-convention)

- `backend/services/transform_forms/callable_skill_gate.py::require_governed_skill_query(request, skill_id, db)` — FastAPI dep composing:
  1. `require_identity_or_deny(request)` → 401 auth_missing/auth_expired.
  2. `check_scope(identity, ...)` via P8E-E2 α single-source → 403 `auth_scope_insufficient` on mismatch.
  3. Returns provisioning record on success.
- `ensure_response_carries_class(response, class_label, floor)` — validates class against registry (TF-E3 α) + floor rank check + mutates response to carry `defensibility.class` inline. Raises `BelowFloorError` on class < floor.
- `below_floor_refusal_envelope(...)` — refusal shape `{outcome: refused, reason: defensibility_below_floor, detail: {class, floor}}`.
- Router endpoint `POST /api/callable_skill/{skill_id}/query` calls `require_governed_skill_query` FIRST, then mutates response via `ensure_response_carries_class`.

### (b) α + β · Slice-freeze belt-and-suspenders

- **(β) In-memory hardening:** `ConfigDict(frozen=True)` on `CallableSkillProvisioningV0`. Post-load mutation raises `pydantic.ValidationError`. Attested by `test_tf_g5_slice_bound_at_freeze_no_mutation` GREEN.
- **(α) Persistence write-once:** `services/transform_forms/callable_skill_persistence.py::provision_skill` uses `insert_one` only. `revoke_skill` uses `update_one` scoped to `{"$set": {"revoked_at": ...}}` — the update-set touches `revoked_at` ONLY; `corpus_slice_ref` is never in the update-set.
- **TF-G9 grep-negative gate landed:** `test_tf_g9_no_update_one_touches_corpus_slice_ref` — AST walk over `backend/**/*.py`, checks every `.update_one(...)` call's source segment for the literal string `corpus_slice_ref`. Any hit = fail. GREEN post-execution.

═══════════════════════════════════════════════════════════════════

*End of Transform Forms rulings record. Standing Rule v3: verbatim on-disk. Reply body carries SHA + tier tags only.*
