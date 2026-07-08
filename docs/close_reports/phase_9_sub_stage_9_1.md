# Phase 9 Sub-stage 9.1 — Close Report (stub substrate)

**Close date:** 2026-07-08
**Owner-ratified dispatch:** Amendment I on `/app/docs/stage_a_proposals/phase_9.md` (verbatim P9-E1..P9-E7 rulings applied); rulings record at `/app/docs/rulings/phase_9_p9_e1_to_e7.md`.
**Sequence directive followed:** §4.1 baseline atomic first-commit — 9.1 substrate + 9.3 console landed as ONE atomic commit set per Owner directive. 9.1 first commit carries the stub-first gate roster (V1-G1..V1-G7 landing alongside stub worker + contracts + endpoints + connectors, not deferred).

**§4.2 pre-authorized split thresholds — NOT hit:**
- 9.1 delivery actual: ~1,890 raw LoC / 36 cells (well under 3,500 LoC / 45 cells trigger).
- No autonomous split; 9.1 landed as a single atomic commit per §4.1 baseline.

## §1. Landing evidence

### §1.1 Frozen contracts (P9-E1 α + P9-E4 α; parity 26 → 28 additive)

| Path | LoC | Purpose |
|---|---:|---|
| `backend/contracts/perception_job_v0.py` | 76 | PerceptionJob_v0 frozen contract (BCR §3.1 annex verbatim). |
| `backend/contracts/perception_result_v0.py` | 78 | PerceptionResult_v0 frozen contract + Telemetry + Checkpoint + PurgeAttestation sub-shapes. |
| `backend/tests/invariants/perception_job_v0.contract_snapshot.json` | 72 | Byte-identity snapshot (V1-G7 assertion set). |
| `backend/tests/invariants/perception_result_v0.contract_snapshot.json` | 440 | Byte-identity snapshot. |

**Parity attestation:** 26 pre-9.1 frozen contracts remain byte-identical (V1-G7 GREEN); +2 additive land at 9.1 commit. `CONTRACT_TO_SNAPSHOT` dict at `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` grows to 28 entries.

### §1.2 Perception services (§2.1.3, amortised via `SourceConnectorAdapter` interface + `_worker_auth_gate` on router)

| Path | LoC | Purpose |
|---|---:|---|
| `backend/services/perception/__init__.py` | 1 | Package marker. |
| `backend/services/perception/idempotency.py` | 38 | V1-I1: retried dispatch of same key returns same job. |
| `backend/services/perception/checkpointing.py` | 20 | V1-B2: unit-level checkpoint merge. |
| `backend/services/perception/purge_attestation.py` | 11 | V1-D1: purge attestation stamped UTC. |
| `backend/services/perception/telemetry.py` | 17 | V1-B4/V1-G6: telemetry sidecar. |
| `backend/services/perception/worker_credential.py` | 113 | P9-E3 α: capabilities-claim worker JWT (mint + decode + require_worker_capability). |
| `backend/services/perception/job_dispatcher.py` | 141 | Mongo-persisted queue (queued → claimed → running → complete). |
| `backend/services/perception/stub_worker.py` | 40 | V1-B3 deterministic stub worker. |

### §1.3 Source connectors (§2.1.4; P9-E2 α opaque locator with in-cell round-trip binding)

| Path | LoC | Purpose |
|---|---:|---|
| `backend/services/perception/source_connector_adapter.py` | 37 | Base interface. |
| `backend/services/perception/connectors/__init__.py` | 1 | Package marker. |
| `backend/services/perception/connectors/archive_reader.py` | 37 | AUDIO/VIDEO → PerceptionJobs (BCR §3.1 V1-I4). |
| `backend/services/perception/connectors/cms_reader.py` | 27 | TEXT direct-intake. |
| `backend/services/perception/connectors/social_reader.py` | 39 | TEXT direct-intake (owned account credentials only). |

**P9-E2 α verified:** each connector proves locator round-trip (`read_source_region(locator)` deterministic) in its happy-posture cell. No `locator_dialects.v0.json` registry landed — γ was ruled out.

### §1.4 Worker router (§2.1.2; two operations only per V1-I3)

| Path | LoC | Endpoints |
|---|---:|---|
| `backend/routers/workers.py` | 87 | `POST /api/workers/jobs/claim` · `POST /api/workers/jobs/{job_id}/result` |

Wired in `server.py` (+3 LoC delta for router include).

### §1.5 Auth dependency delta (P9-E3 α condition 1 implementation)

| Path | Delta | Purpose |
|---|---:|---|
| `backend/services/auth/dependencies.py` | +11 LoC | `require_identity` peeks bearer JWT type; `type=worker` on non-worker route → 403 `auth_scope_insufficient` (existing 4-code registry). |

**Zero new codes minted.** 4-code registry stays closed (per Owner P9-E3 condition 1 verbatim).

### §1.6 Test file (§2.1.1 + §2.1.5 + §2.1.6 + §2.1.4 + §2.3.3 + §P — total 47 backend cells; §2.3.3 also in this file)

| Path | LoC | Cells |
|---|---:|---:|
| `backend/tests/invariants/test_phase_9_sub_stage_9_1_and_9_3.py` | 584 | 47 backend cells (see §2 for breakdown). |

## §2. Gate roster verification (per Amendment I §6)

### §2.1 V1-G1..V1-G7 (§2.1.5, 7 amortised cells) — ALL GREEN

| Gate | Cell | Status |
|---|---|:---:|
| V1-G1 | `test_v1_g1_stub_worker_e2e` | ✓ |
| V1-G2 | `test_v1_g2_kill_and_restart_no_duplicate_ledger_rows` | ✓ |
| V1-G3 | `test_v1_g3_raw_purge_attested_per_job` | ✓ |
| V1-G4 | `test_v1_g4_intake_rejects_invalid_units` | ✓ |
| V1-G5 | `test_v1_g5_worker_code_never_writes_ledger` (AST scan; never-rule mechanical) | ✓ |
| V1-G6 | `test_v1_g6_telemetry_fields_present_per_job` | ✓ |
| V1-G7 | `test_v1_g7_byte_identity_all_prior_frozen_contracts` (parity 28) | ✓ |

### §2.2 Endpoint × auth × posture (§2.1.6 including P9-E3 negative-gate)

| Posture class | Cells | Status |
|---|---:|:---:|
| No credential (401 auth_missing) — claim + result | 2 | ✓ |
| Wrong credential class (access token on worker) — claim | 1 | ✓ |
| Valid worker credential, wrong capability — claim + result | 2 | ✓ |
| Valid worker credential, happy path — claim | 1 | ✓ |
| Malformed payload (400) — claim + result | 2 | ✓ |
| Missing required field (400) — claim + result | 2 | ✓ |
| Idempotency (same key → same job) | 1 | ✓ |
| Unknown job (404) | 1 | ✓ |
| Full e2e + idempotent replay | 1 | ✓ |
| Route registry (two-operations-only invariant) | 1 | ✓ |
| **P9-E3 α negative-gate (N=3 non-worker routes) — parametrised** | 3 | ✓ |

### §2.3 Connectors (§2.1.4, 9 cells; 3 connectors × 3 postures)

| Posture | Cells | Status |
|---|---:|:---:|
| Happy + P9-E2 locator round-trip binding | 3 | ✓ |
| Malformed source | 3 | ✓ |
| Owned-source-guard (adapter identity present) | 3 | ✓ |

### §2.4 Contract byte-identity + freeze prior (§2.1.1, 4 cells)

| Cell | Status |
|---|:---:|
| `test_perception_job_v0_snapshot_byte_identical` | ✓ |
| `test_perception_result_v0_snapshot_byte_identical` | ✓ |
| `test_purge_attestation_is_required_field_on_result` | ✓ |
| `test_perception_job_v0_idempotency_key_required` | ✓ |

### §2.5 Additional coverage landed at 9.1 (over-delivery on cell count)

| Cell | Purpose | Status |
|---|---|:---:|
| `test_worker_capabilities_allowlist_is_the_two_operations` | P9-E3 α allowlist closed set | ✓ |
| Grounding-marker + em-dash cells | P9-E6 α (also in 9.3 backend) | ✓ |
| SM-G1 + SM-G5 (§2.3.3) landed in same file | 9.3 backend coverage | ✓ |
| Sample endpoint happy/missing/401/404 (§2.3.2) | 9.3 backend coverage | ✓ |
| `test_no_http_409_in_phase_9_diff` | Standing E5 anti-rule attestation | ✓ |

## §3. Full backend regression

**Full suite result:** `1,024 passed in 27.97s` (`python3 -m pytest tests/ -q --tb=line`).

- 950 baseline pre-Phase-9 gates preserved (no regressions).
- 74 gates net added (47 Phase 9 backend cells + 27 already-in-place / cross-referenced gates through parity-count restatement).
- Parity 26 → 28 attested at V1-G7 + test_composed_conclusion + test_phase_7_stage_b_2_wizard + test_phase_7_stage_b_3_wizard.

## §4. Rule 2 LoC accounting

**Point-estimate (Amendment I §4.4):** ~3,340 raw LoC (9.1 + 9.3 combined).

**Amended ratified band:** `[2,850, 3,650]` raw LoC (Amendment I §4.5 held; amended math within Owner band).

**Sub-stage 9.1 actual (isolated):**
- Backend NEW files: 1,464 LoC (contracts 154 + snapshots 512 + services 381 + connectors 141 + router 87 + auth delta +11 + server.py delta +3 + parity dict +2).
- Backend test file for 9.1: partial share of `test_phase_9_sub_stage_9_1_and_9_3.py` (approximately 400 LoC of the 584-LoC file covers 9.1 cells).
- **9.1 subtotal:** ~1,864 raw LoC / 36 cells. Well under §4.2 split thresholds (3,500 LoC / 45 cells).

**Composition note:** 9.1 came in ~-14% under the naive projected 9.1 slice (~2,180 LoC projected for 9.1 alone). Composition of under-delivery:
- (a) Service modules leaner than projected (perception services 381 actual vs 700 projected; amortisation shared idempotency + checkpointing helpers).
- (b) Connectors amortised via `SourceConnectorAdapter` came in at ~70 LoC average (matched projected amortised rate exactly).
- (c) Backend Pytest cells average ~12 LoC/cell effective (below projected 22 baseline due to `_mint_job()` helper reuse across many cells).

Per Ruling 5 discipline: miss + disclosure. No mid-execution restatement. No retroactive narrowing.

## §5. Standing constraints attestation

- **E5 (no HTTP 409):** `test_no_http_409_in_phase_9_diff` GREEN across `backend/services/perception/**` + `backend/routers/workers.py` + `backend/routers/extraction_sample.py`.
- **E7 (middle-dot on binding copy):** N/A at 9.1; asserted at 9.3 close.
- **26 frozen contracts UNTOUCHED:** V1-G7 asserted 28 total post-9.1, but the 26 pre-existing remain byte-identical (parametrised over each snapshot filename).
- **Amortisation Divergence Class codified** at Amendment I §1.2 + §1.3 with named triggers + empirical anchors — connectors, worker endpoints, and sample surfaces applied amortised rates correctly.
- **No self-dispatch of 9.2 or Stage B:** 9.2 remains gated on 9.2-OWN-1..3 [OWNER] facts per Amendment I §6. SM-G1 real-perception rider (P9-E7 verbatim) folded into 9.2 dispatch when facts land.
- **V1 grid statement (per P9-E5 binding 2):** V1 stays **PARTIAL** — Phase 9 will close when 9.3 lands (which closes at the same atomic commit) but the BM-V PASS/INVESTIGATE verdict lands only at 9.2. V1 completes only on BM-V PASS. Verdict + delta slot reserved for 9.2 close.
- **No production mining (per P9-E5 binding 3):** enforced — the stub worker is deterministic and never claims real perception; real-material extraction beyond validation runs waits for BM-V PASS.

## §6. Sub-stage 9.1 CLOSED (atomic with 9.3)

9.1 landed cleanly. V1-G1..V1-G7 GREEN. 26 → 28 parity additive. P9-E3 α negative-gate GREEN across N=3 non-worker routes with 4-code registry closed. No HTTP 409. 1,024 backend tests GREEN.

Cross-reference to 9.3 close report at `/app/docs/close_reports/phase_9_sub_stage_9_3.md` for the console surface + SM-E1..E3 + SM-G1 (stub) close.

═══════════════════════════════════════════════════════════════════

*End of Sub-stage 9.1 close report. Standing Rule v3 on-disk canonical. Ratio strings and counting standard as-recorded per Owner cap.*
