# Fixture Substrate Diff — Substrate-Drop v1

**Fetched:** 2026-07-01T15:54Z
**Discipline:** on-disk fixture NOT overwritten. Incoming staged at `/app/backend/services/data_source/synthetic_assets/rms_adversarial_v1/incoming/`. Adoption blocked pending user judgment.

## 1. SHA-256 comparison

| File | On-disk (shipped) | Incoming (staged) | Match? |
|---|---|---|---|
| `generate_fixture.py` | `50be96a29d96a0f83baa43c34ef8edf29bcfd7b7f8e3e687327ea1fa1df2a50c` | `7c85a8c771fb6d91e766be45099fb44dec1e230a3ab86a13935d16a9e81b7460` | ❌ **DIFFERENT** |
| `fixture.json` | `f137c6ed8d013892cb413cf3f06c86301d0217d08615e61f4cb1c09f91bca423` | `e3df6920b8213bcc0b9f94bb777e46eac285f84356224f05a6a32d47b32cf03e` | ❌ **DIFFERENT** |

## 2. `generate_fixture.py` — unified diff

Full unified diff at `/tmp/gen_fixture.diff` (568 lines). Character of change: full rewrite. Highlights:

- On-disk generator emits `NormalizedUnit`-conformant JSON directly (post-HAZARD-STOP #1 contract-shaped emit, journaled 2026-07-01T12:35Z).
- Incoming generator emits a **different top-level shape** with per-ring prefixed fields (`ring1_provenance / ring2_signal / ring3_relational / ring4_reextraction / ring5_defensibility`), a new top-level `content: str` field, and a new `unit_type: str` field. Also adds a `_fixture` per-unit metadata blob.
- Incoming generator's `_manifest.shape` note claims: `"five_rings@v0 (corrected: modality-enum-only, edge evidence_ref, signal Dict[str,float] no per-dim confidence, extraction_params Optional[dict], defensibility ring integrated, one hazard-stop unit, one CONTRACT-conformant fixture)"` — this is a **different interpretation** of `five_rings@v0` than the frozen contract's shape.

## 3. `fixture.json` — structural / semantic diff

### 3.1 Top-level shape

| Field | On-disk | Incoming |
|---|---|---|
| `_manifest` | present | present |
| `units` | present | present |
| unit count | 19 | 19 |

### 3.2 Unit-level shape

Per-unit top-level keys:

| Key | On-disk | Incoming |
|---|---|---|
| `unit_id` | ✅ | ✅ |
| `provenance` | ✅ (matches frozen `NormalizedUnit.provenance: ProvenanceRing`) | ❌ absent — renamed `ring1_provenance` |
| `signal` | ✅ (matches frozen `NormalizedUnit.signal: SignalRing`) | ❌ absent — renamed `ring2_signal` |
| `relational` | ✅ (matches frozen `NormalizedUnit.relational: RelationalRing`) | ❌ absent — renamed `ring3_relational` |
| `reextraction_handle` | ✅ (matches frozen `NormalizedUnit.reextraction_handle: ReextractionHandleRing`) | ❌ absent — renamed `ring4_reextraction` |
| `defensibility` | ✅ (matches frozen `NormalizedUnit.defensibility: DefensibilityRing`) | ❌ absent — renamed `ring5_defensibility` |
| `ring1_provenance` | absent | present |
| `ring2_signal` | absent | present |
| `ring3_relational` | absent | present |
| `ring4_reextraction` | absent | present |
| `ring5_defensibility` | absent | present |
| `content` | absent | present (new top-level string field) |
| `unit_type` | absent | present (new top-level string field) |
| `freshness_stamp` | absent | present (moved out of a nested ring) |
| `_fixture` | absent | present (per-unit metadata blob) |

### 3.3 Adversarial coverage

Both fixtures declare 19 units. Adversarial coverage classes (from the `_fixture` / `_manifest.tags` field where present) appear to overlap by intent — refusal, corroboration, retraction, contested — but the incoming fixture reshuffles unit ids and adds coverage tags. Full mapping deferred pending shape-conformance resolution (moot until frozen contract is either (a) mutated OR (b) not-mutated with fixture rejected/transformed).

## 4. Contract conformance check

Executed: parse each incoming unit against frozen `contracts.five_rings.NormalizedUnit` (Pydantic v2 strict).

| Fixture | Units parsed | Parse errors |
|---|---|---|
| On-disk `fixture.json` | **19/19** | 0 |
| Incoming `fixture.incoming.json` | **0/19** | 19 |

First-error example (representative of all 19 incoming units):
```
11 validation errors for NormalizedUnit
  provenance             Field required (input has ring1_provenance instead)
  reextraction_handle    Field required (input has ring4_reextraction instead)
  defensibility          Field required (input has ring5_defensibility instead)
  unit_type              Extra inputs are not permitted  (top-level field absent from contract)
  content                Extra inputs are not permitted  (top-level field absent from contract)
  ring1_provenance       Extra inputs are not permitted
  ring2_signal           Extra inputs are not permitted
  ring3_relational       Extra inputs are not permitted
  ring4_reextraction     Extra inputs are not permitted
  ring5_defensibility    Extra inputs are not permitted
  freshness_stamp        Extra inputs are not permitted  (frozen contract nests this inside ProvenanceRing)
```

**Verdict: FAILS contract conformance.** Adopting the incoming fixture as-is would require **mutating** the frozen `NormalizedUnit` contract (rename 5 fields + add 3 new top-level fields + move `freshness_stamp` out of `ProvenanceRing`) — which is a **HAZARD-STOP (a)** trigger.

## 5. Tests-would-break assessment

The 23 `test_rms_adversarial_v1_roundtrip.py` tests load `fixture.json` and parse each unit against `NormalizedUnit`. Adopting the incoming fixture as-is (naïve overwrite) would break **all 23 roundtrip tests** immediately (Pydantic validation failure on load). The 149→158 shipped CI green count would drop to **135/158** (23 failures) if the incoming fixture replaced the on-disk one without a corresponding contract mutation.

## 6. Adoption paths (user judgment required)

1. **Reject** — incoming fixture uses a shape incompatible with the frozen contract; on-disk fixture stays canonical. No action needed. **Recommended default.** Rationale: incoming fixture appears to be a design-time draft of a hypothetical alternative field-naming (ring-prefixed) that would require mutating the frozen contract shipped at G0 and snapshot-tested by all invariant tests. Contract mutation is HAZARD-STOP (a) territory; not warranted unless the ring-prefixed shape is stakeholder-authoritative.

2. **Transform on load** — write a `services/data_source/rms_adversarial_v1/loader.py` mapper that translates the incoming shape (`ring1_provenance → provenance`, etc.) into `NormalizedUnit`-compliant units at parse time. Keeps frozen contract intact; adopts incoming fixture's content (adversarial coverage tags, hazard-stop unit, `content` + `unit_type` fields dropped or stored as sidecar). Rule 2 cost: ~30-50 LoC net-new (`transitive` lift from existing `data_source/parser.py` pattern). Requires user sign-off because dropping fields is a substrate-content decision.

3. **Mutate frozen contract** — rename the 5 ring fields + add 3 new top-level fields + relocate `freshness_stamp`. **HAZARD-STOP (a).** Requires stakeholder re-bless of `NormalizedUnit` snapshot + regeneration of all invariant snapshots + likely cascade through Northena `LedgerRow.artifact_ref` shape + Layer C stamp emission + V1/V3 harnesses. Highest cost. Only justified if the ring-prefixed shape is stakeholder-authoritative (i.e., "the frozen contract shipped at G0 was wrong; we're fixing it").

## 7. HAZARD-STOP declaration

**HAZARD-STOP (a) raised** against **fixture-adoption**, scoped:

- **Blocker for:** adopting `incoming/fixture.incoming.json` into `fixture.json` (or any path that swaps it into the live test set).
- **Not a blocker for:** the Substrate-Drop v1 phase itself. On-disk fixture is untouched; 158/158 CI green; no shipped code contradiction. The phase closes green with the HAZARD-STOP surfaced as a **pending user decision**, not a phase-halt.
- **Escalation to user:** which adoption path? (Reject / Transform / Mutate.) Reject is recommended default; a decision from stakeholder is required before any adoption step is taken.

## 8. On-disk state (post-phase, verifiable)

- `/app/backend/services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` — **UNCHANGED** (SHA `50be...c2333`).
- `/app/backend/services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json` — **UNCHANGED** (SHA `f137...ca423`).
- `/app/backend/services/data_source/synthetic_assets/rms_adversarial_v1/incoming/generate_fixture.incoming.py` — **STAGED** (SHA `7c85...b7460`).
- `/app/backend/services/data_source/synthetic_assets/rms_adversarial_v1/incoming/fixture.incoming.json` — **STAGED** (SHA `e3df...cf03e`).
- `/tmp/gen_fixture.diff` — full 568-line unified diff (ephemeral).
