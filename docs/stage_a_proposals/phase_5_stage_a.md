# Phase 5 Stage A — Async Delivery Contract §7 (Design-Only Proposals)

**Canonical location:** `/app/docs/stage_a_proposals/phase_5_stage_a.md`
**Landed:** 2026-07-04
**Scope:** design proposals only. No code writes. No contract mutations. Parity stays 18. CI stays 450/450. Substrate-drop stays 13/13.

**Bottom-line status:** two HAZARD-STOP candidates surfaced (Return 6 — `LedgerRow.decision` Literal has no `terminate_cancelled`; Return 7 — 202-accepted body posture argued as UNFROZEN-by-wire-shape-gate but requires Owner ruling); one PROVISIONAL Ruling-4 verdict pending Owner acceptance (Return 1 — VERDICT A — GOVERNANCE-HONEST SCAFFOLD); five ADDITIVE registry-bump reason codes proposed (Returns 5 + 6) preserving Ruling 2 and Phase 3 Standing Disposition.

---

## Return 1 — `answer_text` composition function verbatim + Ruling-4 discriminating-property verdict

### 1.1 Composition function pasted verbatim from disk

**Source:** `/app/backend/services/service_1/composed_conclusion.py`

**Function `package_composed_conclusion` — success-path `answer_text` construction, lines 282–321 (verbatim):**

```python
    # 7. Success path — persist ONE Northena Ledger row for
    # trace_id → load_bearing correlation (v3 §6.2.3).
    load_bearing_unit_ids = [v.unit_id for v in unit_views]
    objective_ref = f"objreq-{trace_id}"
    run_id = f"cc-run-{uuid.uuid4().hex[:12]}"

    # Ledger's `reason` field carries the retrievable payload — same
    # pattern as service.py's `service_1_converged:units=N:plan=X`.
    # `stage=converge / decision=terminate_success` per the frozen
    # LedgerRow stage/decision enum table.
    ledger_reason = (
        f"composed_conclusion:class={computed_class.value}"
        f":load_bearing={','.join(load_bearing_unit_ids)}"
    )
    await northena_ledger.record(LedgerRow(
        run_id=run_id,
        trace_id=trace_id,
        stage="converge",
        decision="terminate_success",
        reason=ledger_reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id=objective_ref,
            version="v2",
        ),
        lawful_basis_ref=request.envelope.lawful_basis,
        stamp_audit=None,
        at=datetime.now(timezone.utc),
    ))

    # 8. Build the ComposedConclusion_v0 envelope — Solva-threaded class
    # UNCHANGED. Answer_text is a governance-honest scaffold stub for
    # Phase 4b (real synthesis is downstream; this phase lands the
    # frozen envelope + governance path, not the LLM composition).
    answer_text = (
        f"Composed conclusion over {len(load_bearing_unit_ids)} "
        f"load-bearing unit(s) at defensibility class "
        f"'{computed_class.value}'. Load-bearing set retrievable "
        f"via Northena Ledger by trace_id."
    )
    return ComposedConclusion_v0(
        conclusion_class=computed_class,
        answer_text=answer_text,
        trace_id=trace_id,
        load_bearing_unit_ids=load_bearing_unit_ids,
        objective_ref=objective_ref,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
```

**Contributing callees (lines 149–204):** `_rows_to_unit_views(rows)` reads `row["defensibility_class"]` per Registry row; `_max_supported_class(unit_views)` and `_plain_language_asked(request)` do not contribute to `answer_text` (they contribute to the sibling `Service1Refusal(composition_below_floor)` path). The Solva boundary call `_solva_conclusion_class(unit_views)` at line 265 produces `computed_class`, which is `answer_text`'s only class-carrying substrate.

### 1.2 Ruling-4 discriminating-property verdict — LINE-BY-LINE

The `answer_text` is constructed by a single f-string at lines 316–321 (four format spans). Enumerate each format span and trace its source:

| Format span | Static/dynamic | Source | Traceable? |
|---|---|---|---|
| `"Composed conclusion over "` | STATIC literal | Template prefix | N/A (structural) |
| `f"{len(load_bearing_unit_ids)}"` | DYNAMIC | `load_bearing_unit_ids` = `[v.unit_id for v in unit_views]` (line 284); each `unit_id` derived from Registry row's `source_ref` (line 167–170). Count is deterministic over the class-filtered survivor rows. | ✓ Mechanically derived from load-bearing unit set |
| `" load-bearing unit(s) at defensibility class "` | STATIC literal | Template continuation | N/A (structural) |
| `f"'{computed_class.value}'"` | DYNAMIC | `computed_class` = `_solva_conclusion_class(unit_views)` at line 265 — the ONE Solva boundary call, floor-reducing over per-unit Ring-5-governed `defensibility_class` values. | ✓ Mechanically derived from Solva-computed conclusion class |
| `". Load-bearing set retrievable via Northena Ledger by trace_id."` | STATIC literal | Template suffix — states a mechanical fact (the load-bearing set IS retrievable by trace_id via the ledger row persisted at lines 296–310, whose `reason` field carries `load_bearing=<ids>`). | Structural claim provably true from the immediately-preceding ledger write — verifiable, not fabricated |

**Every dynamic span in `answer_text` is a deterministic template fill from unit fields or the Solva-computed class.** No connective content is introduced. No claim is stated about the content of any unit's underlying material (no natural-language summary of what units say; no synthesis of positions across units). The `answer_text` states three mechanical facts about the deliverable: (a) how many load-bearing units contributed, (b) at what defensibility class the conclusion sits, (c) where the load-bearing set can be retrieved.

Cross-check against Owner's discriminating property:
- **"Every sentence in `answer_text` mechanically derived from the load-bearing units?"** — YES. All dynamic content in the answer is either a count of load-bearing units, the Solva-computed conclusion class over those units, or a structural retrieval reference to the persisted ledger row (which itself only names the load-bearing unit_ids and the computed class).
- **"Contains any invented connective content not sourced from units?"** — NO. There is no claim about what the units say, no aggregation of unit content into a natural-language proposition, no LLM-synthesised connective tissue between per-unit positions.

### 1.3 Verdict

**VERDICT A — GOVERNANCE-HONEST SCAFFOLD.**

Provisional per Owner Ruling 4: the 4b close's "governance-honest" claim is accepted PROVISIONALLY on exactly this test, subject to Owner ratification of the trace above. @200 stands. Phase 5 wraps `ComposedConclusion_v0` as-is via the async terminal-state envelope. LLM fluency upgrade lands later behind the same frozen envelope — the six-field `ComposedConclusion_v0` schema does not change when `answer_text` gains fluency; only the string it carries becomes richer while remaining bounded by the same "every sentence traces to a load-bearing unit" property.

**Ratification handoff to Owner:** this verdict is a Phase 5 gating condition per the dispatch. Owner rules VERDICT A stands or is overturned to VERDICT B (fabrication → remediate to 501 pattern before Phase 5 wraps).

**Fluency-upgrade posture (for the record, not for immediate action):** when LLM synthesis lands (post-Phase-5), the discriminating property becomes a LOAD-BEARING gate: `test_answer_text_every_sentence_traces_to_load_bearing_unit`. Sentence-level provenance retention becomes an invariant of the fluency-upgrade phase.

---

## Return 2 — Envelope inventory per Ruling 2

### 2.1 Terminal-refused classes Phase 5 must handle

| # | Refusal class | Firing site | Existing envelope on disk | Envelope source path | Contract # (of 18) | Sync HTTP status | Async wrapper `refusal_envelope` field carries |
|---|---|---|---|---|---|---|---|
| 1 | `form_not_offerable` (v3 §6.5 model form off-menu) | Admission | `AdmissionRefusal_v0` | `contracts/admission_refusal.py:82-158`; snapshot `tests/invariants/admission_refusal.contract_snapshot.json` | 17 | 422 | `AdmissionRefusal_v0` body verbatim |
| 2 | `grain_form_incompatible` (v3 §6.1.4 / §6.2.4 grain × form matrix) | Admission | `AdmissionRefusal_v0` | (same) | 17 | 422 | `AdmissionRefusal_v0` body verbatim |
| 3 | `standard_below_admission_floor` (v3 §6.1.6 hard input filter empty) | Admission | `AdmissionRefusal_v0` | (same) | 17 | 422 | `AdmissionRefusal_v0` body verbatim |
| 4 | `license_class_unavailable` (v3 §6.1.2 license-class axis empty) | Admission | `AdmissionRefusal_v0` | (same) | 17 | 422 | `AdmissionRefusal_v0` body verbatim |
| 5 | `composition_below_floor` (v3 §6.2.6 conclusion-class < requested floor) | Execution (Service 1 §6.2 packaging) | `Service1Refusal_v0` | `contracts/service_1_refusal.py:50-98`; snapshot `tests/invariants/service_1_refusal.contract_snapshot.json` | 14 | 422 | `Service1Refusal_v0` body verbatim |
| 6 | `lawful_basis_absent` (V2 gate — §29.1) | Egress (V2 gate) | `V2RefusalEnvelope` | `contracts/v2_refusal.py:22-59`; snapshot `tests/invariants/v2_refusal_envelope.contract_snapshot.json` | 12 | 422 (existing V2 gate route) | `V2RefusalEnvelope` body verbatim |
| 7 | `substrate_rights_expired` (V2 gate — §29.1 rights past extract-for-RMS) | Egress (V2 gate) | `V2RefusalEnvelope` | (same) | 12 | 422 | `V2RefusalEnvelope` body verbatim |
| 8 | `sample_file_out_crypto_verify_failed` (V2 gate — §29.1 sample verification) | Egress (V2 gate) | `V2RefusalEnvelope` | (same) | 12 | 422 | `V2RefusalEnvelope` body verbatim |
| 9 | `cumulative_disclosure_risk` (V2 arm — §29.1 / §30, seam-gated dark until DPO env-var unlock — Closed Seam 5) | Egress (V2 gate) | `V2RefusalEnvelope` | (same) | 12 | 422 | `V2RefusalEnvelope` body verbatim (only fires when Seam 5 unlocked) |
| 10 | `idempotency_key_reused_with_different_body` (Phase 5 admission-time — see Return 5) | Admission | `AdmissionRefusal_v0` via **v1→v2 registry bump** (additive; new reason code; Phase 3 Standing Disposition pattern) | `contracts/admission_refusal.py:82-158` (unchanged); `services/service_1/admission_refusal_reasons.v2.json` (new file, additive over v1) | 17 (contract unchanged; registry bump) | 422 | `AdmissionRefusal_v0` body with reason code from registry v2 |
| 11 | `caller_cancelled` (Phase 5 — see Return 6, Argument A only) | Admission-time OR Execution-time, depending on cancel arrival phase | `AdmissionRefusal_v0` OR `Service1Refusal_v0` via **v1→v2 registry bump** (additive) — see Return 6 for the arm-selection argument | (envelope files unchanged); `services/service_1/admission_refusal_reasons.v2.json` OR sibling registry for Service 1 reasons | 17 or 14 | 422 | Whichever existing envelope matches the cancel-arrival phase |

**Envelope-invention check** (per Ruling 2): none of classes 1–9 requires a new envelope. Classes 10–11 use registry-bump-additive-extension (Phase 3 Standing Disposition) which preserves `AdmissionRefusal_v0`'s snapshot byte-identical; NO new envelope, NO Literal-widening (reason is constrained `str` not `Literal` per `admission_refusal.py:102-113`).

### 2.2 Ledger row for cancellation — HAZARD-STOP CANDIDATE

**Refusal-envelope inventory above resolves cleanly.** However v3 §7 bullet 5 requires: *"No partial egress, including on caller cancellation; a cancelled run is still ledgered."* This surfaces a distinct HAZARD-STOP at the LEDGER surface (not the refusal-envelope surface):

- `contracts/northena_ledger.py:42-46` — `_ALLOWED = {"converge": {"terminate_success", "terminate_budget", "continue"}, ...}` (verbatim); `contracts/northena_ledger.py:57-61` — `decision: Literal["admitted", "refused", "warm", "fresh", "terminate_success", "terminate_budget", "continue"]` — this Literal has NO `terminate_cancelled` code.
- Cancellation arriving mid-`running` requires a converge-stage ledger row (the run reached converge before terminating). No existing `converge/decision` value semantically fits cancellation without semantic distortion:
  - `terminate_success` — false (cancel is not success).
  - `terminate_budget` — false (cancel is not budget exhaustion).
  - `continue` — false (this is a terminal transition, not a continuation).
- Cancellation arriving before `running` transition can ledger as `admit/refused` cleanly — that decision code exists and is semantically correct for cancel-at-accepted-state (caller withdrew before dispatch).

**Full HAZARD-STOP argument and options-space is in Return 6.** Cross-referenced here so the envelope inventory surface is complete.

### 2.3 Uncovered classes check

No refusal class Phase 5 must handle is left without a governance envelope, PROVIDED Owner accepts the cancellation-ledger HAZARD-STOP resolution in Return 6 (whichever option). If Owner rejects all Return-6 options and refuses to widen `LedgerRow.decision`, that is a distinct HAZARD-STOP outcome — cancel-with-ledger becomes unreachable and v3 §7 bullet 5 cannot be honoured. Escalated to Owner in Return 6.

---

## Return 3 — Queue substrate design per Ruling 1

### 3.1 Persistence model

**Mongo collection proposal:** `objectives_async_state` (following the `northena_ledger_rows` / `mtafiti_registry_records` singular-scoped-plural naming precedent).

**Document shape:**

| Field | Type | Semantic |
|---|---|---|
| `objective_id` | `str` (uuid) | Primary key; assigned at accept-time; returned to caller in the 202. |
| `status` | `Literal["accepted", "running", "delivered", "refused"]` | State-machine current state. Source of truth (never derived from task set). |
| `state_transitions` | `List[{state: str, at: datetime, worker_generation_id: Optional[str], reason: Optional[str]}]` | Append-only history. Every transition atomic-writes here + `status` field simultaneously via `findOneAndUpdate`. |
| `enqueue_time` | `datetime` | Wall-clock at accept. Used for recovery-sweep ordering. |
| `last_worker_touch` | `Optional[datetime]` | Set by the worker on each `running`-stage progression. Idle-detection for stuck-worker sweep (future). |
| `worker_generation_id` | `Optional[str]` | Unique per worker-boot generation; set atomically on `accepted → running`. Fencing against duplicate work. |
| `idempotency_key` | `str` (min_length ≥ 1) | Copied from `ObjectiveRequest_v2.idempotency_key` (line 234 of `contracts/objective_request_v2.py`). Unique index (see 3.2). |
| `request_body_hash` | `str` (sha256 hex, 64 chars) | Canonicalised hash of the request body — see Return 5 for canonicalisation rule. |
| `trace_id` | `str` (uuid) | Northena/Solva trace correlator. Same lifetime as `objective_id`; different key. |
| `webhook_url` | `Optional[str]` | Registered at SyniSense app registration; nullable (polling-only apps have no webhook). |
| `sandbox_mode` | `bool` | Key-mode flag from registration (§7 bullet 8). If true, served from fixture estate. |
| `terminal_envelope` | `Optional[Dict[str, Any]]` | Populated on `delivered` or `refused` transition — the ENVELOPE body that a subsequent `GET /api/objectives/{id}` returns. For `delivered`: the `ComposedConclusion_v0` / `QualifiedDataPayload` body. For `refused`: the `AdmissionRefusal_v0` / `Service1Refusal_v0` / `V2RefusalEnvelope` body per Return 2. |

**Mongo indexes:**

| Index | Type | Rationale |
|---|---|---|
| `{idempotency_key: 1}` | UNIQUE | Ruling 1's persistence substrate for retry-detection. Enforced at Mongo layer — race-safe. |
| `{status: 1, enqueue_time: 1}` | non-unique | Recovery sweep query: `find({status: {$in: ["accepted", "running"]}}).sort({enqueue_time: 1})`. |
| `{objective_id: 1}` | UNIQUE | Primary key lookup for `GET /api/objectives/{id}` and cancel. |
| `{trace_id: 1}` | UNIQUE | Cross-engine correlation (existing pattern in `northena_ledger_rows`). |

### 3.2 Enqueue path (POST `/api/objectives`)

```
1. Router receives POST /api/objectives with ObjectiveRequest_v2 body.
2. Compute request_body_hash from canonical serialisation (Return 5).
3. Idempotency check via Mongo upsert-if-not-exists on idempotency_key (Return 5).
   * If existing row with same hash → return original 202 (idempotent replay).
   * If existing row with different hash → return 422 idempotency mismatch (Return 5).
   * If no existing row → INSERT new document with status="accepted",
     objective_id=uuid(), trace_id=uuid(), state_transitions=[{state:"accepted", at:now}].
4. Warm/fresh determination (v3 §4): call mtafiti/feasibility.compute_feasibility on the reach.
   * Warm → this route is not the async path; the sync v2 dispatch handles it
     (existing 4a/4b behaviour). Async path handles ONLY fresh.
   * Fresh → proceed with async substrate below.
5. Enqueue: place objective_id on the in-process asyncio.Queue (bounded, e.g. maxsize=1000).
   Queue overflow → refuse with a NEW registry-bump reason `async_queue_saturated`
   (candidate reason for v1→v2 bump; Owner rules — see Return 7 sizing note).
6. Return 202 with body `AsyncDeliveryAccepted_v0` (see Return 7 for the
   frozen-vs-UNFROZEN posture argument).
```

### 3.3 Worker loop

**Design:** in-process `asyncio.Task` spawned at ASGI-startup, reading from the bounded queue. Concurrency N (proposal: N=4 per worker process; Owner rules on N at Stage B — Ruling 5 credit anchor doesn't gate).

Per-objective loop:

```
async def worker_loop(queue):
    while True:
        objective_id = await queue.get()

        # Atomic accepted → running transition (fencing against
        # duplicate dispatch on recovery-sweep re-enqueue).
        worker_gen = f"wg-{uuid.uuid4().hex[:12]}"
        claim = await db["objectives_async_state"].find_one_and_update(
            {"objective_id": objective_id, "status": "accepted"},
            {"$set": {"status": "running", "worker_generation_id": worker_gen,
                      "last_worker_touch": datetime.now(timezone.utc)},
             "$push": {"state_transitions": {"state": "running", "at": now,
                                             "worker_generation_id": worker_gen}}},
            return_document=ReturnDocument.AFTER,
        )
        if claim is None:
            # Another worker got it. Skip.
            continue

        # Rehydrate ObjectiveRequest_v2 from the persisted request body.
        request = ObjectiveRequest_v2.model_validate(claim["request_body"])

        try:
            # Existing Layer A/B/C + service_1 machinery. Fresh-fork ONLY
            # (warm doesn't reach here per 3.2 step 4).
            result = await dispatch_module.dispatch(request, trace_id=claim["trace_id"])
        except composed_conclusion_module.Service1Refusal as e:
            terminal_envelope = Service1RefusalContract(**e.__dict__).model_dump()
            await _terminal_transition(objective_id, "refused", terminal_envelope, worker_gen)
            await _fire_webhook(objective_id, "refused")
            continue
        except Exception:
            # Infrastructure fault. Governance says: infra faults are 500,
            # NEVER refusals (UI Spec §4.2 binding copy).
            # Stage B: log; leave status="running"; recovery sweep re-enqueues.
            # Or (proposal, Owner rules): after N infra failures, mark as
            # "abandoned" (would need a 5th terminal state — argue in Return 6).
            # Stage A: leave open; DO NOT invent an "abandoned" state.
            raise

        # Success path: dispatch returned an envelope. Determine
        # delivered-vs-refused via existing isinstance checks matching
        # routers/service_1.py's 4a/4b Union arms.
        if isinstance(result, (ComposedConclusion_v0, QualifiedDataPayload)):
            terminal_envelope = result.model_dump() if hasattr(result, "model_dump") else result
            await _terminal_transition(objective_id, "delivered", terminal_envelope, worker_gen)
            await _fire_webhook(objective_id, "delivered")
        elif isinstance(result, AdmissionRefusal_v0):
            terminal_envelope = result.model_dump()
            await _terminal_transition(objective_id, "refused", terminal_envelope, worker_gen)
            await _fire_webhook(objective_id, "refused")
        # V2 gate integration: outer-gate egress produces V2RefusalEnvelope if refused.
        # Handled inside dispatch or as post-dispatch V2 gate check (Stage B decision).
```

**Load-bearing atomic-transition primitive:** `find_one_and_update({... "status": "accepted"}, {...})` returns None if another worker already claimed. This is the fencing primitive. Two workers claiming the same objective is provably impossible because the `status: "accepted"` predicate is atomic under Mongo's find-and-modify guarantees.

### 3.4 Recovery sweep

**Trigger:** ASGI-startup lifecycle (`@app.on_event("startup")` or equivalent).

```python
async def recovery_sweep():
    cursor = db["objectives_async_state"].find(
        {"status": {"$in": ["accepted", "running"]}}
    ).sort("enqueue_time", 1)
    async for doc in cursor:
        if doc["status"] == "running":
            # Was mid-execution when killed. Reset to accepted so the
            # worker loop re-claims cleanly via the accepted→running
            # atomic transition. Previous worker_generation_id remains
            # in state_transitions history for audit.
            await db["objectives_async_state"].update_one(
                {"objective_id": doc["objective_id"], "status": "running"},
                {"$set": {"status": "accepted"},
                 "$push": {"state_transitions": {
                     "state": "recovery_reset",  # SUB-STATE, ledger-side only
                     "at": datetime.now(timezone.utc),
                     "reason": "worker_generation_replaced_on_boot"}}},
            )
        # Re-enqueue.
        await queue.put(doc["objective_id"])
```

**Duplicate-work prevention** — same argument as 3.3:
- The atomic `accepted → running` transition with `worker_generation_id` fence prevents two workers from ever entering execution for the same objective.
- Recovery-sweep `running → accepted` reset is idempotent — even if the sweep is run twice (partial boot, then full boot), the second run finds `status="accepted"` and re-enqueues; the worker loop's atomic claim fence prevents second dispatch.
- The Northena Ledger row (which is what §7.2 governs) is emitted by `services/service_1/composed_conclusion.py` on `terminate_success` at line 296. That call site is inside the worker's dispatch invocation. If a worker is killed BEFORE reaching line 296, no ledger row was written; the recovery sweep re-runs the dispatch, and the ledger row emits at the natural terminal transition. If a worker is killed AFTER line 296 but BEFORE the terminal-state Mongo update, the ledger row is written but `status` remains "running" — the sweep re-enqueues, the worker restarts dispatch from scratch, and a SECOND ledger row would emit → duplicate emission.

**This is the vulnerability the LOAD-BEARING gate must catch.** Mitigation proposals:

- **Option A (proposed default):** wrap the ledger write + Mongo terminal-state update in a single transaction using Mongo's multi-document transaction API. Atomic across the two writes. On kill-between: neither happens; sweep re-runs cleanly. On kill-after: both happened; sweep skips (status already terminal).
- **Option B (alternative):** ledger row includes a `worker_generation_id` field on `stamp_audit` (Optional[Dict], already frozen at LedgerRow — this is an addition to the CONTENTS of the Dict, not a schema change). Recovery sweep queries the ledger for `run_id` and skips if a `terminate_*` row already exists for that run_id at the correct worker_generation. Requires post-scan check.
- **Option A preferred** because it uses infrastructure-level atomicity rather than post-scan reconciliation. Stage B implements Option A unless Owner rules otherwise at Stage B dispatch.

### 3.5 LOAD-BEARING gate — `test_kill_and_restart_recovers_without_state_loss_or_duplicate_ledger_emission`

**Test shape in prose:**

```
Setup:
  - Seed one objective with status="accepted", ObjectiveRequest_v2 body B, trace_id T, run_id (not yet assigned; assigned at ledger-emit time).
  - Boot worker, worker atomically claims → status="running".
  - Inject a controlled kill point immediately BEFORE line 296 (before ledger.record())
    via a test-injection hook or by wrapping the test dispatch to raise SystemExit
    at that point.
  - Confirm: Mongo state = {status: "running"}, no ledger row for this trace_id.

Kill:
  - Simulate SIGTERM / ASGI restart.
  - Worker task cancelled; queue emptied; state remains in Mongo.

Recovery:
  - Boot second worker generation.
  - Recovery sweep runs, sees status="running", flips to "accepted",
    re-enqueues.
  - Worker atomically claims (new worker_generation_id), executes dispatch cleanly.
  - Ledger row emits at natural terminate_success.

Asserts:
  - Same trace_id (T unchanged).
  - Same objective_id (unchanged).
  - Northena Ledger query {trace_id: T, stage: "converge"} returns exactly ONE row
    (no duplicate).
  - Mongo state_transitions history shows: accepted → running → recovery_reset →
    accepted → running → delivered. Six entries. First worker_generation_id ≠
    second worker_generation_id.
  - No second webhook fired (webhook fires once at terminal-state transition;
    the sweep does NOT re-fire the delivered webhook because it went
    running → accepted, not running → delivered).
```

**Additional gates for state-family completeness (family granularity — Owner rules at Stage B if too granular):**

- `test_recover_from_accepted_re_enqueues_cleanly`
- `test_recover_from_running_resets_to_accepted_then_re_enqueues`
- `test_recover_from_delivered_is_noop_no_re_delivery_webhook`
- `test_recover_from_refused_is_noop`

**Family verdict:** the four sub-gates plus the LOAD-BEARING top-level test is proposed. Stage B implements all five; Owner may collapse to fewer at Stage B dispatch if granularity is judged excessive.

---

## Return 4 — Webhook design per Ruling 3

### 4.1 Payload shape

Proposal:

```json
{
  "event": "objective.status_changed",
  "objective_id": "obj-<uuid>",
  "trace_id": "trc-<uuid>",
  "status": "delivered" | "refused",
  "timestamp": "2026-07-04T12:34:56.789Z"
}
```

Five fields; all governance-thin (no claim content, no per-unit content, no defensibility class). `event` field is a single Literal-per-emitter now (`"objective.status_changed"`); Stage B decides if we ever emit multiple event types (retry-nudge, status-progress-nudge). For now: one event kind.

**Frozen-vs-UNFROZEN posture:**

- **Proposal:** UNFROZEN webhook payload, wire-shape gated per §6.1 pattern (`test_webhook_wire_shape_pins_five_governance_keys` — asserts all five keys present + `status ∈ {delivered, refused}` + `timestamp` is ISO-8601-parseable + `objective_id` matches Mongo state).
- **Argument for UNFROZEN:** the payload is a doorbell notification; it carries no claim content by design (§7 bullet 4). A wire-shape gate is sufficient governance. Precedent: 4a's `QualifiedDataPayload` container UNFROZEN by wire-shape gate (Ruling 3, 2026-07-03). The webhook payload is even thinner (5 vs 4 keys; no inner-frozen envelope inside).
- **Argument for FROZEN:** the webhook payload is an OUTBOUND surface (unlike QualifiedDataPayload which stays within RMS). External integrators depend on its shape. A frozen contract makes this dependency explicit. But: §7 explicitly documents this payload verbatim, so external integrators already have a source of truth (v3 §7 bullet 4). Freezing it internally adds a second source that must be kept in sync with the spec.
- **Owner rules.** Stage A default: UNFROZEN + wire-shape gate. If Owner rules FROZEN, this becomes a 19th frozen contract (`AsyncWebhookPayload_v0`), and the size band in Return 7 shifts.

### 4.2 Signing

- Algorithm: HMAC-SHA256 over `{payload_body_json}.{timestamp_iso8601}` with a per-registration secret.
- Header names: `X-RMS-Signature: sha256=<hex>`; `X-RMS-Timestamp: <iso8601>`.
- Skew window: reject signatures where `abs(now - timestamp) > 300 seconds` (5 minutes) — the standard Stripe/GitHub webhook pattern; balances clock drift against replay attack surface.
- Secret provisioning: at SyniSense app registration time (see 4.5 below); secret is stored on the app's registration record; not on the per-objective document.

### 4.3 Retry policy

- Attempts: **5**.
- Backoff: exponential — 1s, 4s, 16s, 64s, 256s (base=4, exponent=0..4). Total elapsed on 5th attempt fire: ~341 seconds (~5.7 min).
- Success criteria: HTTP 2xx from the caller within a 10-second per-attempt timeout. Non-2xx or timeout = retry.
- Terminal on attempt 5 failure: mark `webhook_undelivered=true` on the objective document; ledger a note (see 4.6); STOP. No dead-letter queue per Ruling 3.
- **Non-goal:** delivery guarantee. Webhook is a doorbell. Buyer app's poll of `GET /api/objectives/{id}` is the source of truth.

### 4.4 Registration seam

**Existing surface:** `services/synisense/config.py` — currently holds `SYNISENSE_MASTER_SECRET` resolution + allow-listed purposes. App-registration flow (not yet built) will use the same config module. Two new fields per app registration:

- `webhook_url: Optional[str]` — where doorbell fires. Nullable for polling-only apps.
- `webhook_signing_secret: bytes` — per-app HMAC key. Derived from `SYNISENSE_MASTER_SECRET` via HKDF with `app_id` as info parameter (mirrors the per-tenant HMAC pattern already documented at `synisense/config.py:23-27`).

Stage B lands the registration surface (or defers to Phase 8's engineer surface — v3 §9 explicitly). Cross-reference to Phase 8 plan-debt: engineer surface (§4.1 UI Spec) hosts the registration UI; the backend surface lands at Phase 5 Stage B.

### 4.5 Named gates

| Gate | Load-bearing? | Test shape |
|---|---|---|
| `test_webhook_signature_verifiable` | LOAD-BEARING | Round-trip: emit signed payload, verify with the same secret using the standard HMAC scheme documented in 4.2; signature MUST verify. Also negative: modify one byte of payload → signature MUST fail to verify. |
| `test_webhook_retries_bounded_at_five` | LOAD-BEARING | Configure a webhook_url that always returns 500. Trigger a terminal transition. Assert exactly 5 retry attempts fire (not 4, not 6). Assert exponential backoff between attempts. Assert `webhook_undelivered=true` set on objective doc after attempt 5. |
| `test_webhook_undelivered_still_polls_status` | LOAD-BEARING per §7 bullet 4 | After `webhook_undelivered=true`, `GET /api/objectives/{id}` still returns the correct terminal envelope. Webhook drop does NOT lose state. |
| `test_webhook_payload_carries_no_claim_content` | LOAD-BEARING per §12 invariant #7 | Grep-negative over the emitted payload against forbidden keys: `answer_text`, `units`, `receipt`, `defensibility_class`, `content`, `body`. Only 5 governance-thin keys allowed. |
| `test_webhook_timestamp_skew_rejected_beyond_five_minutes` | coverage | Signed payload with timestamp 6 minutes in past → verifier rejects. |
| `test_webhook_wire_shape_pins_five_governance_keys` | LOAD-BEARING if payload UNFROZEN | Five keys present + `status ∈ {delivered, refused}` + `timestamp` ISO-8601 parseable. Fails if any key drops or renests. |

---

## Return 5 — Idempotency design

### 5.1 Key storage

**Field source:** `contracts/objective_request_v2.py:234-237` verbatim:

```python
    idempotency_key: Optional[str] = Field(
        default=None,
        description="v3 §3.2: # external_request. Also see v3 §7 async contract.",
    )
```

Required on external_request per v3 §7 bullet 6; nullable on the contract level (external_request presence-check happens at admission — proposal: if entry=external_request and idempotency_key is None → `AdmissionRefusal_v0(reason="idempotency_key_missing")` via v1→v2 registry bump — same registry pattern; Owner may choose to make this contract-level Required later via new contract version if idempotency becomes universal).

**Persistence:** on the `objectives_async_state` Mongo document (per Return 3.1). Unique index at Mongo layer enforces cross-request race safety.

### 5.2 Retry-detection semantics

**Canonicalisation rule for `request_body_hash`:**

```python
import hashlib, json

def canonical_request_hash(request: ObjectiveRequest_v2) -> str:
    # 1. Dump to dict via Pydantic (schema-driven; skips fields
    #    the contract doesn't know about).
    body = request.model_dump(mode="python", exclude_none=False)
    # 2. Remove idempotency_key from the hash input (the key itself is
    #    the retry-detection axis; hashing it in would defeat detection
    #    of same-key/different-body).
    body.pop("idempotency_key", None)
    # 3. Sort keys recursively; no whitespace; UTF-8.
    canonical_json = json.dumps(body, sort_keys=True, separators=(",", ":"),
                                default=str, ensure_ascii=False)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
```

**Three cases at POST arrival:**

| Case | Detection | Response |
|---|---|---|
| No existing row with this `idempotency_key` | Mongo upsert-if-not-exists returns "inserted" | Proceed with normal enqueue flow; return NEW 202 |
| Existing row with same `idempotency_key` AND same `request_body_hash` | Mongo unique-index conflict on insert; find_one confirms hash match | Return the ORIGINAL 202 envelope byte-identical (same `objective_id`, same `trace_id`, same `delivery_estimate` at issue-time) |
| Existing row with same `idempotency_key` AND different `request_body_hash` | Mongo unique-index conflict; hash mismatch on read | Return `AdmissionRefusal_v0(reason="idempotency_key_reused_with_different_body")` via v1→v2 registry bump |

### 5.3 Registry-bump proposal

**Additive-only extension per Phase 3 Standing Disposition** (v0→v1 already landed at Phase 4a; v1→v2 for Phase 5 additions):

New reason codes at `services/service_1/admission_refusal_reasons.v2.json` (new file, additive over v1):

- `idempotency_key_reused_with_different_body` (Return 5)
- `caller_cancelled` (Return 6, Argument A only — Owner rules)
- `idempotency_key_missing` (Return 5 — presence-check for external_request; proposed but not requested by Owner directly; flag for Owner)
- `async_queue_saturated` (Return 3.2 — queue-overflow at accept-time; proposed but not requested by Owner directly; flag for Owner)

**Contract `admission_refusal.py` untouched.** Snapshot `admission_refusal.contract_snapshot.json` byte-identical (as at Phase 4a's registry bump). Parity stays 18.

### 5.4 LOAD-BEARING gate — `test_retried_post_neither_double_commissions_nor_double_charges`

**Test shape in prose:**

```
Setup:
  - Idempotency key K = "idem-<uuid>"; body B; sync=False (fresh-fork).

Turn 1 (initial):
  - POST /api/objectives with key=K, body=B.
  - Assert 202 returned. Capture objective_id=O1, trace_id=T1.
  - Assert Mongo has ONE document with idempotency_key=K, status="accepted"
    (or "running" if worker moved fast).

Turn 2 (retry, same key + same body):
  - POST /api/objectives with key=K, body=B.
  - Assert 202 returned; body byte-identical to Turn 1 body
    (same objective_id=O1, same trace_id=T1).
  - Assert Northena Ledger has AT MOST ONE admit row for objective_id=O1
    (depending on state machine progress).
  - Assert Mongo state_transitions history has NOT been duplicated
    (still one accepted → possibly running).
  - Assert Phase 6 quote instrumentation hook (Stage A anticipates this)
    fires ONCE for O1 (verifiable when Phase 6 lands; Stage A flags the
    dependency).

Turn 3 (retry, same key + DIFFERENT body B'):
  - POST /api/objectives with key=K, body=B'.
  - Assert 422 with AdmissionRefusal_v0 body:
    * outcome="refused"
    * reason="idempotency_key_reused_with_different_body"
    * trace_id: NEW trace_id (this is a refusal on a NEW attempt, not
      a replay; refusal envelope's trace_id is fresh — flag: Owner may
      prefer echoing the original T1 instead; Stage A default: new
      trace_id for the refusal).
  - Assert Mongo state has still ONE document total for K (Turn 3
    request did NOT create a second document).
  - Assert Phase 6 quote instrumentation fires NO additional times.
```

**Note on trace_id on refusal reply for mismatch:** open Stage A question. Two candidate postures:
- (a) Refusal carries a NEW trace_id — it's a new refusal event, ledgered separately.
- (b) Refusal echoes original T1 — the caller referenced an existing objective by key; the refusal is contextualised to that objective.
- Stage A proposal: **(a) new trace_id**, with the refusal `off_menu_fact` naming the original objective_id + trace_id in prose. This preserves the invariant "one trace_id per attempted intake". Owner rules if (b) preferred.

---

## Return 6 — Cancellation semantics

### 6.1 Endpoint

**Proposal:** `POST /api/objectives/{id}/cancel`.

**Rationale for POST-on-sub-path vs DELETE:**

- DELETE `/api/objectives/{id}` implies removal of the objective from the record. That is at odds with v3 §7 bullet 5 — cancellation is ledgered; the objective remains in the record with a terminal state. DELETE semantics mislead.
- POST `/api/objectives/{id}/cancel` is an action verb — request-cancel — which the state machine applies if reachable. Idempotent (repeated POSTs after cancel-succeeded return the terminal envelope; the state machine has already terminated).
- Auth: SyniSense-enforced key scope, same as `GET /api/objectives/{id}`. Only the app that submitted the objective can cancel it.

### 6.2 State-machine disposition — LOAD-BEARING ARGUMENT

Owner's four-state ruling is `accepted → running → delivered | refused`. Sub-stages inside `running` are detail, not states apps handle.

**Argument A — cancelled rides `refused`.** Preserves the four-state ruling exactly.

Per-timing envelope selection:

| Cancel arrival | Arm | Envelope | Reason code |
|---|---|---|---|
| Before `accepted → running` (state currently accepted) | Admission | `AdmissionRefusal_v0` | `caller_cancelled` (registry bump v1→v2) |
| Mid-`running` (state currently running, before terminal transition) | Execution | `Service1Refusal_v0` | `caller_cancelled` (Service 1 refusal reasons sibling registry — see below) |
| After `delivered` or `refused` (terminal state reached) | N/A | No new envelope; return the existing terminal envelope; cancel is a no-op | N/A |

**Sub-issue A1 — Service 1 refusal reasons registry:** `contracts/service_1_refusal.py:63-69` — `reason` is `str` (not Literal); the field docstring lists three example reasons but is not registry-governed like `AdmissionRefusal_v0`. Per Phase 3 Standing Disposition (registry pattern), Phase 5 Stage B should introduce `services/service_1/service_1_refusal_reasons.v0.json` mirroring the admission-refusal reasons registry structure — reason set for `Service1Refusal_v0` gains a Ruling 3 pattern. Existing three reasons (`no_defensibility_floor`, `no_lawful_basis`, `composition_below_floor`) plus new `caller_cancelled` all land in the v0 registry. No `Service1Refusal_v0` contract mutation; snapshot byte-identical.

**Sub-issue A2 — Ledger row for mid-running cancel:** the CRUX HAZARD-STOP.

- `LedgerRow.decision` (`contracts/northena_ledger.py:56-61`) — `stage="converge"` restricts decision to `Literal["terminate_success", "terminate_budget", "continue"]`.
- Mid-running cancel reaches converge stage semantically (the run was running; it's terminating now, at a state that isn't budget-exhaustion and isn't success).
- **No existing decision code fits without semantic distortion.**

Options-space:

1. **Ledger under `admit/refused`** — treats cancel-during-run as an admission-side event. Semantically wrong (the run already reached converge).
2. **Ledger under `converge/terminate_budget`** — distorts the meaning of budget (cancel is not budget-exhaustion). Grep-negative gate `test_ledger_terminate_budget_is_budget_only` doesn't yet exist but would obviously fail under this option in future audit.
3. **Ledger under `converge/continue`** — false; the run is terminating, not continuing. Rejected.
4. **HAZARD-STOP (a) — extend `LedgerRow.decision` Literal to include `terminate_cancelled`.** Breaks byte-identical snapshot on `northena_ledger.py` (6th frozen contract). Not permitted without Owner ruling per Standing Ruling 2.
5. **Introduce a new frozen contract `AsyncTerminalLedgerAugment_v0`** as a sidecar to LedgerRow, carrying cancel-specific fields. Ruling 2 forbids envelope invention casually. Argue against unless Owner rules — the ledger row IS the record; a sidecar is a second record for the same event.
6. **Repivot LedgerRow to registry-governed decision codes** — mirror admission-refusal-reasons registry pattern for Northena decisions. Contract stays byte-identical (decision becomes `str` with pattern constraint like `AdmissionRefusal_v0.reason`); registry adds `terminate_cancelled` additively. This is a byte-mutation of LedgerRow's `decision` field type — same HAZARD-STOP class as option 4 unless Owner accepts the loose-as-frozen posture (Standing Owner Disposition — deliberate under-determination when scalar type isn't ruled). LedgerRow's decision IS scalar-typed (Literal); repivoting from Literal to constrained str IS narrowing → widening in the opposite direction. HAZARD-STOP.

**Stage A escalation:** raise **HAZARD-STOP (a) — frozen-contract-must-mutate** on `contracts/northena_ledger.py::LedgerRow.decision` for the mid-running cancel-ledger requirement. Owner rules the resolution — options 4, 5, or 6 above, OR a new option Owner supplies.

**Argument B — cancelled is a fifth terminal state.**

Explicit argument AGAINST Owner's four-state ruling:

- **Pressure:** cancelled has a DIFFERENT semantic than refused. Refused = a governance ceiling refused to admit or a floor was not met by the material. Cancelled = the caller withdrew the ask. From the buyer/operator's perspective, "refused because governance said no" and "refused because I cancelled" are different outcomes to render. A single `refused` state with `reason: caller_cancelled` conflates the two.
- **Ledger distinction:** a fifth terminal state `cancelled` would take a distinct `LedgerRow.decision` code (`terminate_cancelled`), forcing the same HAZARD-STOP as Argument A option 4 — but the escalation is honest: fifth state requires ledger extension.
- **Alternative I'd propose:** if Owner accepts B, extend `LedgerRow.decision` Literal to include `terminate_cancelled` AND add a fifth `status` field value on the async state machine. This is TWO simultaneous frozen-contract mutations. Consequences: LedgerRow snapshot changes (contract 6); potentially a new `AsyncStatus_v0` frozen contract or wire-shape gate for the status field. Owner rules.

**Stage A verdict:** propose **Argument A with HAZARD-STOP escalation on the ledger-decision Literal**. Argument B is the alternative Owner may prefer, and if Owner picks B, the escalation converges on the same LedgerRow.decision widening. Either way, Owner rules on `LedgerRow.decision` extension.

### 6.3 No-partial-egress gate

**LOAD-BEARING per §7 bullet 5.** Named: `test_cancelled_run_no_partial_egress`.

**Test shape:**

```
Setup:
  - Objective in mid-running state.
  - Instrument outer-gate transform to record every call (should be zero
    if cancel arrives before dispatch reaches outer-gate step).

Cancel:
  - POST /api/objectives/{id}/cancel arrives at time t.
  - State machine atomically flips running → refused (Argument A) or
    running → cancelled (Argument B, if Owner rules).

Asserts:
  - outer_gate.transform_artifact call count = 0 (from setup baseline);
    no artifact was produced.
  - outer_gate.build_receipt call count = 0 (no receipt minted).
  - Webhook: fires exactly ONCE with status="refused" (Argument A) or
    status="cancelled" (Argument B); payload carries no artifact body,
    no receipt body, no unit content — only the doorbell five-key shape
    (Return 4).
  - Ledger row: exactly ONE row emitted for this trace_id with the
    Owner-ruled decision code (per §6.2 HAZARD-STOP resolution).
  - Mongo terminal_envelope field: populated with AdmissionRefusal_v0 /
    Service1Refusal_v0 body (Argument A) or a cancelled-specific envelope
    (Argument B — if Owner rules that path, argue whether cancelled needs
    its own envelope shape; Stage A default: no — cancelled rides
    Service1Refusal_v0 body with reason=caller_cancelled).
```

### 6.4 Ledger emission on cancel

Per HAZARD-STOP resolution in 6.2, ledger row shape TBD Owner. Placeholder for the record:

```python
await northena_ledger.record(LedgerRow(
    run_id=run_id,
    trace_id=trace_id,
    stage="converge",  # if cancel arrives mid-running
    decision=<OWNER-RULED-DECISION-CODE>,   # HAZARD-STOP escalation
    reason=f"caller_cancelled:cancelled_at_state=running",
    artifact_ref=LedgerArtifactRef(
        artifact_type="objective_request",
        artifact_id=objective_ref,
        version="v2",
    ),
    lawful_basis_ref=request.envelope.lawful_basis,
    stamp_audit=None,
    at=datetime.now(timezone.utc),
))
```

The `reason` field (which is `str`, not Literal) carries the cancellation detail unambiguously — even without a dedicated decision code, the `reason` string differentiates cancel from budget-exhaustion in the audit trail.

**Sub-option 6.2-1 (Argument A, semantic distortion accepted):** if Owner rules "ledger under `converge/terminate_budget` for now, accept semantic distortion as a temporary posture pending future decision-registry landing," Stage B can proceed. The `reason` string ("caller_cancelled:cancelled_at_state=running") carries the actual semantic; the decision code becomes a coarse-grained categoriser only.

**Sub-option 6.2-2 (Argument A + HAZARD-STOP resolution — decision widening):** LedgerRow contract mutation (breaks snapshot on contract 6). Owner rules.

### 6.5 Race conditions

**Cancel arrives during `accepted → running` transition:**

- Order 1 — cancel wins: cancel's own atomic transition tries `{objective_id, status: "accepted"}` → sets `status="refused"`. If it wins, worker's later attempt at `{objective_id, status: "accepted"}` returns None (already refused), worker skips. Clean.
- Order 2 — worker wins: worker's atomic transition flips to `running`. Cancel's later attempt at `{objective_id, status: "accepted"}` returns None; cancel re-tries with `{objective_id, status: "running"}` → sets refused. Mid-running-cancel path fires.

The atomic transitions are the ordering primitive. No lock is needed.

**Cancel arrives during `running → delivered/refused` (terminal-write) transition:**

- Order 1 — cancel wins: cancel's transition on `{objective_id, status: "running"}` sets refused; worker's later attempt at terminal write on `{objective_id, status: "running"}` returns None; worker abandons terminal write. Result: cancelled, but the terminal-envelope is the cancel envelope, not the completed deliverable. Governance-safe: no egress happened (assume outer-gate write is post-terminal-state transition; if outer-gate transform already ran, that's a partial-egress hole — see below).
- Order 2 — worker wins: worker's terminal write succeeds; cancel's later attempt at `{objective_id, status: "running"}` returns None (already terminal); cancel is a no-op returning the current terminal envelope (delivered).

**Sub-issue on partial-egress ordering:** if outer-gate transform executes BEFORE the terminal Mongo state write, and cancel arrives BETWEEN transform and Mongo write, the transform already produced an egress artifact but the state is still "running" — cancel arrives, flips to refused, transform result is discarded. Is this partial-egress?

- **Argument:** no — the transform ran INTERNALLY to the process; nothing left the system perimeter. Outer-gate transform is not the perimeter; the response body is the perimeter. If the state flips to refused before the response body carrying the transform result is emitted, no egress happened.
- **Enforcement:** Stage B implements the terminal transition atomically WITH the response-write. Whichever wins wins. The outer-gate transform is memoisable but not emitted until state is terminal. Concrete: worker computes transform result → sets state to `delivered` atomically → if state flip fails (cancel already terminal'd), the transform result is discarded; if state flip succeeds, the response body is written and the webhook fires.

**Gate:** `test_cancel_during_outer_gate_transform_no_partial_egress` (LOAD-BEARING per §7 bullet 5).

---

## Return 7 — Sizing + gates roster + §7 scope-bullet-accounting

### 7.1 Sizing (Rule 2 v2 anticipated for Stage B)

**Lifted candidates:**

| Substrate | Source | LoC estimate |
|---|---|---|
| Northena Ledger writer (`northena_ledger.record` call site + LedgerRow construction pattern) | Existing pattern from `services/service_1/composed_conclusion.py:296-310` + `services/service_1/service.py::run` | ~30 lifted |
| Service 1 dispatch fresh-fork branch (currently 501 placeholder) | `services/service_1/dispatch.py` (existing structure) | ~15 lifted (branch shape; content is net-new) |
| Outer_gate transform / mint / receipt primitives | `services/outer_gate/*.py` unchanged (Condition B3 preserved) | ~0 lifted (used by reference, not modified) |
| SyniSense key-scope enforcement | `services/synisense/config.py` + shield modules | ~40 lifted (registration surface hooks) |
| Existing `Service1Refusal_v0` shape + catch/serialise pattern | `services/service_1/composed_conclusion.py:118-146` + `routers/service_1.py` catch/serialise | ~25 lifted |
| Existing `AdmissionRefusal_v0` emit-helper pattern + registry (v1→v2 additive bump) | `services/service_1/admission_refusal.py` + `admission_refusal_reasons.v1.json` | ~35 lifted (emit-helpers pattern; new helpers ~15 net-new each) |
| Idempotency canonical-hash pattern | New but small — Pydantic `model_dump` + `hashlib.sha256` is standard | ~10 lifted from stdlib idioms |
| ASGI startup lifecycle hooks | Existing `server.py` startup pattern | ~10 lifted |
| **Total lifted** | | **~165 LoC** |

**Net-new candidates:**

| Component | LoC estimate (net-new) | Rationale |
|---|---|---|
| `services/service_1/async_state.py` (state-machine module + terminal-transition helpers) | 200–250 | State enum + atomic transition helpers + terminal envelope writer + Mongo document accessors |
| `services/service_1/idempotency.py` (canonical hash + upsert-if-not-exists retry-detection) | 80–120 | 3 functions: canonicalise, hash, upsert-idempotent |
| `services/service_1/async_worker.py` (worker loop + recovery sweep + queue) | 250–300 | Worker loop body + recovery sweep + startup registration |
| `services/service_1/webhook.py` (signing + emit + retry loop) | 180–220 | HMAC signing + retry loop + backoff + timeout handling |
| `routers/objectives.py` (POST `/api/objectives`, GET `/api/objectives/{id}`, POST `/api/objectives/{id}/cancel`) | 150–200 | 3 routes + request validation + response serialisation |
| `services/service_1/admission_refusal_reasons.v2.json` (v1→v2 registry bump; +2 to +4 new codes) | 20–40 | JSON registry file — small |
| `services/service_1/service_1_refusal_reasons.v0.json` (new sibling registry for Service 1 refusal reasons) | 25–35 | JSON registry file (Return 6.2 sub-issue A1) |
| `services/service_1/admission_refusal.py` MODIFIED (+ 2 to 4 new emit-helpers for new reason codes) | 60–100 | Emit-helpers per new reason (~15–25 LoC each) |
| Contracts/routers touches for AsyncDeliveryAccepted body posture (either wire-shape-gated dict OR new 19th frozen contract — see 7.2) | 0 lifted; 30–80 net-new | Small; depends on frozen-vs-UNFROZEN ruling |
| Test files (per Return 3, 4, 5, 6 gates + wire-shape + fresh-fork integration + §12 invariant coverage) | 500–700 | ~15–20 test files at 30–50 LoC each |
| **Total net-new** | | **~1500–2050 LoC** |

**Total Stage B anticipated band: ~1500–2050 net-new (with ~165 lifted).** PM band was 1200–1800; Stage A narrows to ~1500–2050. Slight upward revision from PM anchor — primarily driven by (a) the two registry bumps (admission-refusal v2 + new Service 1 refusal reasons v0), (b) the atomic transaction wrapping around ledger-write + Mongo terminal-state update per Option A in Return 3.4, (c) additional gates surfaced by Returns 5 (idempotency + trace_id echo verdict) and 6 (cancel race conditions).

**Discretionary anticipated:** ~15–20% of net-new (~300 LoC) is discretionary framing (module docstrings, per-gate docstrings, canonicalisation-rule anchor comments). Well under 1.0× discretionary threshold; no ratify-rationale escalation anticipated. Ratio anticipated: ~11× overall / ~0.18× discretionary-only.

**HAZARD-STOP-adjacent sizing risk:** if Owner rules Argument B (5th terminal state), add ~50–100 LoC for the extended state-machine + potential `AsyncStatus_v0` frozen contract (contract 19th if frozen; UNFROZEN by wire-shape gate otherwise). If Owner rules `LedgerRow.decision` widening for Argument A option 4, add ~30 LoC for the contract snapshot re-bless + Rule 2 v2 ratify rationale on the mutation.

### 7.2 202-accepted envelope frozen-vs-UNFROZEN posture

**Body content per v3 §7 bullet 1:** `{ objective_id, status: accepted, delivery_estimate, quote? }`.

**Argue frozen (§6.2 pattern — ComposedConclusion_v0):**

- Pro: outbound envelope; external integrator dependency; five governance-carrying keys deserve schema-locked shape.
- Pro: `quote?` is a Phase 6 seam — freezing the OUTER envelope while leaving `quote` as a nested reference to `QuoteEnvelope_v0` (Phase 6, future) mirrors the 4b pattern of frozen envelope with reference to other envelopes.
- Con: `delivery_estimate` scalar type not ruled by v3 (string? seconds? ISO-8601 duration?). Loose-as-frozen posture (Standing Owner Disposition) says: freeze permissively via v0-precedent default; narrow later via new contract version. Not a HAZARD-STOP for freezing now.
- Con: adds a 19th frozen contract; parity 18 → 19; snapshot registration + parity map entry + `.contract_snapshot.json` file — small operational overhead but adds surface.

**Argue UNFROZEN (§6.1 pattern — QualifiedDataPayload):**

- Pro: the body is thin. Four keys total (with `quote` nullable → 3-key common path). Wire-shape gate is sufficient governance — `test_accepted_body_pins_governance_keys`: assert `objective_id`, `status`, `delivery_estimate` present + `status == "accepted"`.
- Pro: mirrors Ruling 3 posture from Phase 4a — a thin container of governance-carrying keys does NOT need its own frozen contract if a wire-shape gate pins the container.
- Pro: parity stays 18; no new frozen contract to freeze.
- Con: `delivery_estimate` shape drift risk (a wire-shape gate can be less strict than a Pydantic schema; missing type constraint).
- Con: external integrators don't have a Pydantic schema to key off (they read v3 §7 verbatim + gate assertion).

**Stage A default proposal:** **UNFROZEN + wire-shape gate**, mirroring the 4a `QualifiedDataPayload` posture (Ruling 3, 2026-07-03). Parity stays 18. Wire-shape gate: `test_accepted_body_wire_shape_pins_governance_keys` LOAD-BEARING.

**Owner rules.** If Owner rules FROZEN: Stage B adds contract 19 `AsyncDeliveryAccepted_v0`, parity 18 → 19, mechanical parity invariant needs registration for `async_delivery_accepted.py`, snapshot bijection asserted for 19 entries. Sizing shifts +30–80 LoC.

**Escalated to Owner as an explicit ruling item, per Return 7 dispatch language ("argue the position; do not decide unilaterally").**

### 7.3 Gates roster (Stage B target)

| # | Gate | Load-bearing? | Return |
|---|---|---|---|
| G1 | `test_kill_and_restart_recovers_without_state_loss_or_duplicate_ledger_emission` | **LOAD-BEARING** | 3 |
| G2 | `test_recover_from_accepted_re_enqueues_cleanly` | coverage | 3 |
| G3 | `test_recover_from_running_resets_to_accepted_then_re_enqueues` | coverage | 3 |
| G4 | `test_recover_from_delivered_is_noop_no_re_delivery_webhook` | coverage | 3 |
| G5 | `test_recover_from_refused_is_noop` | coverage | 3 |
| G6 | `test_webhook_signature_verifiable` | **LOAD-BEARING** | 4 |
| G7 | `test_webhook_retries_bounded_at_five` | **LOAD-BEARING** | 4 |
| G8 | `test_webhook_undelivered_still_polls_status` | **LOAD-BEARING** (§7 bullet 4) | 4 |
| G9 | `test_webhook_payload_carries_no_claim_content` | **LOAD-BEARING** (§12 invariant #7) | 4 |
| G10 | `test_webhook_timestamp_skew_rejected_beyond_five_minutes` | coverage | 4 |
| G11 | `test_webhook_wire_shape_pins_five_governance_keys` | **LOAD-BEARING** if payload UNFROZEN | 4 |
| G12 | `test_retried_post_neither_double_commissions_nor_double_charges` | **LOAD-BEARING** (§7 bullet 6) | 5 |
| G13 | `test_idempotency_key_missing_on_external_request_refuses` | coverage (if reason code added) | 5 |
| G14 | `test_cancelled_run_no_partial_egress` | **LOAD-BEARING** (§7 bullet 5) | 6 |
| G15 | `test_cancel_during_outer_gate_transform_no_partial_egress` | **LOAD-BEARING** (§7 bullet 5 + race resolution) | 6 |
| G16 | `test_cancelled_run_is_ledgered` | **LOAD-BEARING** (§7 bullet 5) | 6 |
| G17 | `test_cancel_after_terminal_state_is_noop_returns_terminal_envelope` | coverage | 6 |
| G18 | `test_fresh_fork_at_admission_routes_to_async_pathway` | **LOAD-BEARING** (§4 warm/fresh fork) | 3 |
| G19 | `test_warm_fork_at_admission_uses_sync_pathway_not_async` | coverage | 3 |
| G20 | `test_accepted_body_wire_shape_pins_governance_keys` | **LOAD-BEARING** if UNFROZEN posture accepted | 7 |
| G21 | `test_governance_travels_inline_on_async_response_body` | **LOAD-BEARING** (§12 invariant #7) | 3 |
| G22 | `test_late_refusal_ledgered_with_governed_reason` | **LOAD-BEARING** (§12 invariant #8) | 3 + 6 |
| G23 | `test_sandbox_mode_serves_from_fixture_estate` | **LOAD-BEARING** (§7 bullet 8) | 3 |
| G24 | `test_admission_refusal_registry_v2_extends_v1_additively` | **LOAD-BEARING** (Phase 3 Standing Disposition regression) | 5 + 6 |

**LOAD-BEARING count:** 13. **Coverage count:** 11. **Total:** 24 gates anticipated for Stage B.

### 7.4 §7 scope-bullet accounting (clause-by-clause)

**Bullet 1 (v3 §7):**
> **Fork at admission**: warm → synchronous full response (existing contract). Fresh → `202` with `{ objective_id, status: accepted, delivery_estimate, quote? }`.

- Covered by: Return 3 (async substrate + fresh-fork routing) + Return 7 (202-accepted body posture).
- Gates: G18 (fresh routes async) + G19 (warm stays sync) + G20 (202 body wire-shape).
- Residual: **202-accepted body frozen-vs-UNFROZEN posture** escalated to Owner (Return 7.2).

**Bullet 2 (v3 §7):**
> **States**: `accepted → running → delivered | refused`. Sub-stages (mining, transforming) are detail on status reads, not states apps must handle.

- Covered by: Return 3 (state machine on Mongo document) + Return 6 (cancellation disposition argues Argument A within four-state, or Argument B against).
- Gates: G2–G5 recovery-sweep family (verifies state transitions from each starting state).
- Residual: **Return 6 Argument A vs B** escalated to Owner (default: Argument A + LedgerRow HAZARD-STOP).

**Bullet 3 (v3 §7):**
> **Late refusal is first-class**: `accepted → … → refused` is a normal terminal state carrying the same refusal envelope. Integrating apps must render it as a governed refusal, never a failure.

- Covered by: Return 2 (envelope inventory — each refusal class rides its existing envelope) + Return 3 (worker loop catches Service1Refusal / AdmissionRefusal and writes terminal-state envelope).
- Gates: G22 (late refusal ledgered with governed reason) + §12 invariant #8 coverage.
- Residual: none surfaced by Stage A analysis.

**Bullet 4 (v3 §7):**
> **Thin webhook, governed fetch**: webhook payload = `{ event, objective_id, trace_id, status }` — never claim content. The result is fetched over the app's authenticated key where scope is enforced. Polling `GET /v1/objectives/{id}` is the fallback. Rationale is binding: pushing claims to app-configured URLs would be an egress path the gates do not control.

- Covered by: Return 4 (webhook design) + Return 3 (Mongo `terminal_envelope` field serves `GET /api/objectives/{id}` fetch).
- Gates: G6–G11 (webhook family) + G21 (governance travels inline). Note the endpoint path is proposed `/api/objectives/{id}` (v3 uses `/v1/objectives/{id}` — Stage A follows the `/api` prefix rule from the RMS backend routing pattern; if Owner rules a `/v1` prefix for external-facing APIs, Stage B adds a v1 alias).
- Residual: **endpoint path** minor discrepancy (v3 says `/v1/objectives/{id}`; backend routing prefix is `/api/`). Stage A default: `GET /api/objectives/{id}` with future `/v1/` alias landing at Phase 8 if Owner rules an external-facing versioned URL.

**Bullet 5 (v3 §7):**
> **No partial egress**, including on caller cancellation; a cancelled run is still ledgered.

- Covered by: Return 6 (cancellation semantics + no-partial-egress gate).
- Gates: G14, G15, G16 (LOAD-BEARING).
- Residual: **LedgerRow.decision HAZARD-STOP** for mid-running cancel ledgering. Escalated to Owner (Return 6.2).

**Bullet 6 (v3 §7):**
> **Idempotency key** required on `external_request` submission; a retried POST must not double-commission or double-charge.

- Covered by: Return 5 (idempotency design + retry-detection semantics).
- Gates: G12 (LOAD-BEARING), G13 (missing-key coverage).
- Residual: **`idempotency_key_missing` reason-code addition** to admission_refusal_reasons.v2 flagged; Owner may prefer this presence-check happens at contract-level (require idempotency_key non-null when entry=external_request; would require ObjectiveRequest_v2 contract mutation). Stage A default: registry bump; Owner rules.

**Bullet 7 (v3 §7):**
> **Versioning**: envelopes frozen and additive (the established A2 pattern); breaking change = new path version. **Sandbox** is a key mode set at registration, served from fixture estate.

- Covered by: Return 3.1 (sandbox_mode field on objectives_async_state document) + Return 4.4 (registration surface).
- Gates: G23 (sandbox mode → fixture estate).
- Residual: **fixture-estate wiring** — Stage B either (a) reuses existing `services/data_source/synthetic.py` as the fixture-estate substrate for sandbox=true, or (b) introduces a distinct fixture set. Stage A default: reuse synthetic.py (Ruling 1 permanence of synthetic v1 as standing test substrate). Owner may rule differently.

### 7.5 Cross-references

**§4 warm/fresh fork at admission (bullet 1):** determinant is `mtafiti/feasibility.compute_feasibility` result. Existing at `services/mtafiti/feasibility.py`. Stage B calls it from the async admission route + the sync v2 dispatch route.

**§9 async additions to engineer surface:** *"Async additions to the engineer surface: webhook URL + sandbox toggle at registration; the objective lifecycle in the administer view."* — spans Phase 8. Stage A notes as plan-debt into Phase 8 (`Phase_8` frontend rework adds registration UI + lifecycle rendering per UI Spec §4.3).

**§12 invariant #7 (governance travels inline; webhook payload carries no claim content):** enforced by G9 + G21 at Stage B.

**§12 invariant #8 (late refusal is a governed outcome not error, ledgered like every refusal):** enforced by G22 at Stage B.

**UI Spec §4.2 async paragraph + §4.3 lifecycle rendering:** Phase 8 plan-debt. Stage B backend surface serves the async status endpoint; Phase 8 renders it.

---

## Continuity touch (housekeeping close reporting slip)

The housekeeping close report's machine-attested block described the substrate-drop test surface as "5 top-level + 9 phase-gate-ready parametrisations." Pytest actually reports **4 top-level tests + 9 phase-gate-ready parametrisations = 13**. The 5-vs-4 discrepancy on top-level test count was a cosmetic slip in an already-SHA'd close. Not re-rendering the housekeeping close (that would break the SHA record); noted here for the record.

Actual test roster verified by inspection of `test_substrate_drop_gate.py`:
- Top-level tests: `test_manifest_and_phase_reqs_parseable`, `test_all_phase_required_specs_are_present`, `test_manifest_hashes_match_canonical_md`, `test_all_phase_required_specs_have_manifest_entries` = **4 tests**.
- Parametrised: `test_phase_gate_ready[G3|G4|G5a|G5b|G6|Phase_5|Phase_6|Phase_7|Phase_8]` = **9 parametrisations**.
- **Total: 13 passing.**

---

**End of Phase 5 Stage A close report.** Held pending Owner ruling on the four escalations:

1. **Ruling-4 verdict (Return 1):** ratify VERDICT A — GOVERNANCE-HONEST SCAFFOLD, or overturn to VERDICT B (fabrication → remediate to 501).
2. **LedgerRow.decision HAZARD-STOP (Return 6):** rule on options 1–6 for mid-running cancel-ledger; Argument A vs B on four-state ruling.
3. **202-accepted body posture (Return 7.2):** UNFROZEN + wire-shape gate (Stage A default) vs FROZEN as 19th contract.
4. **Registry-bump additive codes (Returns 5 + 6):** approve `idempotency_key_reused_with_different_body`, `caller_cancelled`, `idempotency_key_missing`, `async_queue_saturated` for v1→v2 bump; new sibling registry for Service 1 refusal reasons v0.

Phase 5 Stage B does not dispatch until Owner rules on 1–4.
