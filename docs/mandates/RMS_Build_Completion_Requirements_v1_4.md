RMS Intelligence System
Build Completion Requirements
Version 1.4 — canonical, binding. This document is the dispatch substrate for all remaining build phases. It parameterizes the build outcome (Section 1), states the honest build state on the vertical-by-horizontal grid (Section 2), and specifies detailed technical and behavioral requirements for every unbuilt component (Section 3), the housing map (Section 4), and sequencing (Section 5). v1.1 added the technical annexes (typed schemas, wire shapes, formulas, config contracts) and split the benchmark into validation-in-phase versus calibration-as-tuning-layer. v1.2 (owner review, 2026-07-06) flags the extraction build-state explicitly and rules Phase 9 Stage A dispatched in parallel; states the tenancy posture (HS5); adds the demo-sample guard to the artifact store (AS-U2, AS-R1); and replaced the partner-portal open item with the dual-actor engineer surface specification (3.9). v1.3 (owner review, 2026-07-06) harmonizes with UI Specification v2: it splits B-5 into read/prove (3.6) and rulebook-writes-under-checker (3.6B); specifies the consequence-class checker (3.11) and the sampling primitive (3.12) as full requirement sets; schedules the B-4 read-only compliance-rule retrofit (3.13); and re-points precedence and cross-references to UI Specification v2. v1.4 (owner ruling, 2026-07-06) removes all commercial attributes from the extractor: it specifies the commercial cut and its mandatory preservation (Section 12), corrects the economics horizontal to internal-cost-only, and re-points surfaces to UI Specification v2.1.
Precedence. The Product & Engineering Specification v3 governs contracts and behavior of what is built; the UI Specification v2.1 governs surfaces (four operator consoles + the governed-extract API boundary; commercial sales is a separate application-layer product, not an extractor surface); the UX Architecture v2 governs experience rules. This document governs what remains. On any conflict among these documents or with existing code: HAZARD-STOP and surface it — never self-resolve. The draft Infrastructure Architecture v1 is dissolved into Section 4 of this document and is superseded.
Marking conventions — used with zero ambiguity throughout. [OWNER] = a fact or value only the owner (or DPO/MEA where named) can supply; the build never invents it. [SLOT] = a value the benchmark measures; illustrative figures hold the slot and convert by config swap only. [STAKED] = a designer-supplied position binding as written until the owner strikes it. MUST and NEVER are binding requirement language. Every requirement carries an ID; acceptance gates are named tests.
# 1. Build outcome parameters
## 1.1 What it should BE
The governed layer through which RMS's owned estate becomes usable, sellable intelligence — without ever becoming ungoverned. Its unit of value is the defensible claim: every output carries what may be asserted, on what basis, traceable to the record. It is not a chatbot, not a dashboard, and not a data lake. Phase 1 scope is owned data only (broadcast archive, CMS, systems data, RMS-owned social accounts); raw audio/video sale is permanently out of scope; unowned/open-web collection is a separate Phase 2 project, not specified here.
## 1.2 What it should DO — four verticals
Each vertical is end-to-end user value. These are the system's four data paths stated as objectives. A vertical is complete only when its done-condition is demonstrable on real (non-fixture) material.
V1 — QUALIFY.  Turn owned raw AV and structured records into qualified NormalizedUnits, Five-Rings-qualified and Registry-censused. Users: the system itself; the operator commissions it. Done when one real broadcast hour and one real CMS batch flow to qualified units in the database with honest telemetry, zero fixture involvement.
V2 — ANSWER.  Turn a plain-language ask into a composed conclusion carrying its defensibility class and trace — or a first-class refusal naming the gap and the path forward. Users: decision-makers and internal applications. Done when the ask console serves answers from the real estate at or above the declared floor and every answer's trust receipt resolves.
V3 — SELL.  Let a buyer shape an acquisition, see price and delivery time move with the shape, pass the outer gate's four checks, and take delivery of a receipt-bound durable artifact. Users: data buyers, integrating partners. Done when a buyer downloads an artifact whose SHA-256 matches its receipt and a re-download is byte-identical.
V4 — PROVE.  Resolve any output, by trace, to its full lawful record — lawful basis, scope, refusals, standard enforcement, ledger — read-only and exportable. Users: DPO/regulator, master admin. Done when the regulator surface proves any run and states retention posture honestly, including unset rules.
## 1.3 What it should HAVE — five horizontals
Horizontals are built once and ridden by every vertical. A capability needed by two or more verticals MUST be a horizontal in the control plane; re-implementation inside a vertical fails review (the standing single-source discipline).
H1 — Governance rail.  Admission, inner/outer gates, the three governors, and the refusal taxonomy (governed refusal / validation error / infrastructure fault / access-control denial — four classes, never conflated on the wire or in rendering). State: built through Phase 8 B-3.
H2 — The record.  Append-only Ledger, Registry, and one trace_id threading unit → reasoning → record. Single writer: the control plane. State: built (26 frozen contracts, mechanical parity invariant green).
H3 — Identity & custody.  User auth (JWT), key-grant scope enforced server-side per call, wizard session binding, and the custody map. State: partial — user-side built (Phase 8 B-1..B-3); worker-side service identity is absent and specified in 3.1.
H4 — Economics & capacity (INTERNAL COST ONLY).  Versioned fleet policy and internal cost/capacity telemetry (cost-per-unit, apportionment) — what the extractor needs to run itself. Commercial pricing, quote envelopes, and quote instrumentation are CUT to the Sales Service (Section 12). State: internal-cost mechanism built; commercial half removed from the extractor. Every internal figure is illustrative pending the benchmark (3.3).
H5 — Contract discipline.  Frozen shapes with byte-identical snapshots; values in versioned config; frozen-field changes land as new versions, never in place. State: built and enforced mechanically.
## 1.4 How it should WORK — operating parameters
W1 Honesty.  No claim renders without its class. Refusal is a first-class answer occupying the answer position. An un-censused or stale estate region returns unknown — the system NEVER fabricates availability. Nothing partial ever egresses, including on cancellation.
W2 Tempo.  Warm asks answer synchronously in seconds. Fresh work returns 202 with an objective handle and moves accepted → running → delivered | refused | cancelled; late refusal is a normal terminal outcome carrying the standard envelope, never an error. Exactly two delivery bands (warm_qualified, fresh_extraction) until measured data defines finer cut-points [SLOT].
W3 Trust.  Every delivered or rendered claim resolves at the public read-only trust receipt by trace_id. Deliverables bind to outer-gate receipts carrying fact and fingerprint only — nothing that could aid reversal. The Ledger is append-only; deletion exists only via the authorized path (3.5).
W4 Scale.  V1 scales with archive-hours (GPU-bound, sits with the data). V2/V3 scale with demand (CPU-class, sit with the record). The two scale independently; the fleet policy apportions across mining / transforms / live path as three capacity classes.
W5 Change.  Values change by config swap (versioned, recorded, reversible). Shapes change by additive version. In-place mutation of a frozen field is a HAZARD-STOP by definition.
## 1.5 How it should be HOUSED
Four environments: RMS estate (raw AV, CMS, social — raw lives here always), GPU zone (processing layer 1, perception), control plane (processing layer 2 + governance core + the record), consumer edge (apps, buyers, public receipts). Placement follows data gravity: V1 sits with the archive; the core and the record sit together and never separate; delivered artifacts sit with the core; raw never moves.
HS1 Custody.  Transform keys and Ledger-write capability exist only in the control plane. LLM access exists only behind the Shield boundary in the control plane. The only worker-side secret is a service credential unlocking the job seam and nothing else.
HS2 Never-rules (hold in every topology).  Raw AV NEVER reaches the consumer edge. The transform key NEVER enters the GPU zone. Workers NEVER write the Ledger. [STAKED — asserted from the design's own logic; strike if wrong]
HS3 Production rule.  The data plane (database + artifact store) MUST be production-grade before the first real hour is mined — at that moment the database contents become the product plus its audit record. Demo deployment of the application may happen any time.
HS4 Binding slots.  Five [OWNER] facts fill the housing addresses: archive access path, GPU placement (the topology fork), LLM account, object-store choice, domain + TLS. The housing rules above are decided now; only the addresses wait.
HS5 Tenancy posture.  Single-tenant per client: each enterprise runs its own instance; client data NEVER shares a tenancy. This is the stated product posture, not a limitation — the preferred custody model for governance software. Hosted multi-tenant operation is a later product decision; nothing in the current design forecloses it, and nothing in this document builds toward it.
## 1.6 The placement rule — binding discipline
Any proposed service, module, or surface MUST answer three questions before it is built: (1) Which vertical's outcome does it serve? (2) Which horizontals does it ride — and if two or more verticals need it, it IS a horizontal, built once in the control plane. (3) Where does its data gravity put it? A proposal answering none of the three is not built. This rule is the formalized guard against auxiliary-goal drift and against services placed off the core vertical and horizontal objectives.

# 2. Honest build state — the V×H grid
BUILT = landed and gated. PARTIAL = seam exists, completion specified in Section 3. ABSENT = specified in Section 3, nothing on disk.

| Vertical | H1 Governance | H2 Record | H3 Identity | H4 Economics | H5 Contracts |
| --- | --- | --- | --- | --- | --- |
| V1 Qualify | PARTIAL — admission & intake built; extraction-side gates absent | PARTIAL — unit contract & Registry built; job lineage absent | ABSENT — worker service identity | PARTIAL — apportionment built; telemetry hooks absent | BUILT — extraction_params frozen |
| V2 Answer | BUILT | BUILT | BUILT | BUILT — estimates on two bands | BUILT |
| V3 Sell | BUILT — outer gate | BUILT — receipts + ledger | BUILT — buyer key scope | BUILT — exploratory values | BUILT |
| V4 Prove | BUILT | BUILT | BUILT | n/a | BUILT |

Per-vertical completion, stated plainly: V1 is the absent vertical — its horizontals' seams exist (frozen intake contract, warm/fresh fork, fleet apportionment) but no connector, worker, or GPU interface exists; the system has processed fixture material only, by sequenced decision — specified in full (3.1) yet never dispatched. Phase 9 Stage A now dispatches in parallel with B-4/B-5 (owner ruling, 2026-07-06). V2 is complete with one quality item: answer_text is truthful mechanical composition, not fluent prose (3.8). V3 is complete except its last mile — the artifact store (3.2). V4 completes across B-5a (read/prove) and B-5b (rulebook writes under the checker) and requires the deletion path (3.5) before its retention controls are real. Master Admin (B-4) is mid-flight; the Compliance Console (B-5) is queued and now split per 3.6/3.6B.
# 3. Engineering requirements — per gap
Each gap is specified on six axes: user-facing, integration surface, backend, data & housing, behavioral requirements, acceptance gates — plus owner bindings. Sizing follows standing practice: Stage A proposes, rulings are priced at dispatch, bands are restated when rulings add scope.
## 3.1 V1 Extraction — processing layer 1 (Phase 9)
Build-state flag (owner-raised, 2026-07-06). Extraction is fully specified — here and in Engineering Spec v3 §4 — and has never been dispatched: it is the only vertical with zero code on disk. Specified and dispatched are different states, and this section was the former. Ruling now in force: Phase 9 Stage A (design-only, zero code writes) dispatches immediately, in parallel with B-4/B-5 surface work — the two do not contend. Stage B's GPU half holds only on the topology facts [OWNER] and runs BM-V inside it.
### Outcome
Real owned material flows to qualified units: archive raw AV through GPU perception; CMS and social records through direct structured intake. Closes the V1 column of the grid.
### User-facing
V1-U1  No new surface. The operator surface's existing elements become real: mining stage visible inside running status; the capacity strip reads actual fleet consumption; budget burn reflects real GPU spend once measured [SLOT].
### Integration surface
V1-I1  PerceptionJob v0 (control plane → worker): job_id, objective_ref, trace_lineage, reextraction_handles[], modality, extraction_params_ref, idempotency_key. Retried dispatch of the same key MUST be the same job.
V1-I2  PerceptionResult v0 (worker → control plane): job_id, units[] (NormalizedUnit, validated at intake), telemetry { gpu_hours, broadcast_hours, unit_yield, per_modality }, checkpoint. Freeze-or-not for both contracts is argued on the D4b axes at Phase 9 Stage A — they cross an environment boundary, so the prior is freeze.
V1-I3  Worker endpoints: job-fetch and result-post only. A worker credential grants exactly these two operations — no database access, no ledger access, no key access.
V1-I4  Source connectors: archive reader (emits PerceptionJobs), CMS reader and social-account reader (emit TEXT-modality units direct to intake). Each adapter owns its source's locator dialect inside the unit's locator field. Owned sources only.
### Backend
V1-B1  The job dispatcher lands behind the existing five-state machine per the standing Phase 5 ruling — the in-process worker is the degenerate single-environment case; the dispatcher swaps behind the same states. Sub-stages of running map to job states.
V1-B2  Checkpointing is unit-level: a job failing mid-hour resumes from its checkpoint; completed units are NEVER re-perceived and NEVER double-ingested (idempotent intake keyed on unit identity).
V1-B3  A deterministic stub worker lands first and all guard gates prove against it before any GPU code exists (the established stub-first pattern). GPU perception models land behind the same worker interface.
V1-B4  Telemetry from every job writes to the instrumentation sidecar (stamp_audit pattern) — this is the benchmark instrument (3.3); it ships with the phase, not after it.
### Data & housing
V1-D1  Raw AV exists worker-side transiently only and is purged on job completion with attestation recorded in the job result. The system keeps reextraction_handles (pointers), never long-term raw copies.
V1-D2  GPU placement follows the topology fork [OWNER: grant physical parameters + archive physical reality]. Under Topology A (compute-to-data, [STAKED default]) raw never leaves RMS tenancy; under B, raw egresses under contract with transit, purge, and rights requirements explicitly ruled before dispatch.
### Behavioral
V1-H1  Unknown-honesty is preserved end-to-end: newly connected but un-censused regions return unknown to feasibility until censused. Connecting a source NEVER fabricates availability.
V1-H2  The never-rules are enforced mechanically, not conventionally: grep/AST gates prove no ledger-write call sites and no transform-key access in worker code; the intake validator is the only entry for units.
### Acceptance gates (named)
V1-G1  test_stub_worker_e2e — job → units → database, green before any GPU code merges.
V1-G2  test_job_kill_and_restart_resumes_without_duplicate_ledger_rows — the Phase 5 recovery pattern extended across the job seam.
V1-G3  test_raw_purge_attested_per_job; V1-G4 test_intake_rejects_invalid_units; V1-G5 test_worker_code_never_writes_ledger (AST); V1-G6 test_telemetry_fields_present_per_job; V1-G7 byte-identity across all prior frozen contracts.
### Technical annex — contracts and wire shapes
Both contracts cross an environment boundary; the D4b prior is FREEZE, argued at Phase 9 Stage A. Shapes below are proposed-binding: implementable as written, Stage-A-arguable per standing escalation rights.
PerceptionJob_v0
  job_id: str                      required · server-minted, unique
  objective_ref: str               required
  trace_lineage: str               required · carried, never minted worker-side
  reextraction_handles: List[str]  required · min 1 · pointers into RMS estate
  modality: Literal[AUDIO, VIDEO]  required · TEXT never routes to GPU
  extraction_params_ref: str       required · frozen contract surface
  idempotency_key: str             required · same key => same job, never a second
  issued_at: str                   required · ISO-8601 UTC

PerceptionResult_v0
  job_id: str                      required
  units: List[NormalizedUnit]      required · may be empty on failure · intake-validated
  telemetry: {gpu_hours: float, broadcast_hours: float,
              unit_yield: int, per_modality: {…}}     required
  checkpoint: {last_completed_offset_s: int,
               completed_unit_ids: List[str]}          required
  purge_attestation: {purged: bool, purged_at: str}    required
  status: Literal[complete, partial_failed]            required
Worker endpoints (the only two a worker credential unlocks)
  POST /api/workers/jobs/claim {worker_id, capabilities}
       -> 200 PerceptionJob | 204 no work
  POST /api/workers/jobs/{job_id}/result {PerceptionResult}
       -> 202 · idempotent on (job_id, checkpoint)
Job state -> objective sub-stage:
  queued|claimed -> running.mining_queued · running -> running.mining
  complete -> running.transform-eligible
  failed_resumable -> re-queued from checkpoint · failed_terminal -> refused path
### Owner bindings
[OWNER] Topology selection facts; archive access path; Hour A + Hour B + 300-unit human-qualified slice (also feeds 3.3). Phase 9 Stage A is writable and dispatchable before these land; Stage B's GPU half and the benchmark execution wait on them.
## 3.2 V3 last mile — the artifact store
### Outcome
The sale path ends in a durable, receipt-bound artifact instead of a wire response. The only holding requirement with no implementation and no decision behind it.
AS-U1  User-facing: the buyer Receive screen's download becomes a durable link; re-download returns the same bytes; the receipt renders beside it exactly as specified in UI Spec §5.3.
AS-I1  Integration: one storage adapter module presenting an S3-class interface (put-once, get, head). The store choice is config [OWNER: object-store choice]; swapping providers touches the adapter's config, never call sites.
AS-B1  Backend: written exactly once at outer-gate egress, keyed by trace_id; SHA-256 of the stored object recorded in the OuterGateReceipt. Write is atomic (temp + move semantics); a partially written artifact is NEVER visible.
AS-B2  No artifact exists without its receipt and ledger row; an orphan-artifact scan MUST return zero.
AS-B3  Download is authenticated by the buyer's key scope; a wrong-key request returns 403 access-control class ({reason, detail}, never outcome=refused).
AS-H1  Behavioral: artifacts are a retention held-class (delivered_artifact); deletion exists only via the Seam 3 authorized path (3.5).
AS-G1  Gates: test_receipt_sha_equals_stored_object; AS-G2 test_refetch_byte_identity; AS-G3 test_orphan_artifact_scan_zero; AS-G4 test_download_403_is_access_control_class.
AS-U2  Demo posture (owner-ruled): a sample deliverable MAY render in demos, marked as sample and fixture-schema-gated exactly like the Engineer first-call fixture (parse-the-sample-through-the-frozen-contracts test). A sample presented unmarked, or returned on a real acquisition wire, is a hidden mock and is prohibited.
AS-R1  The first real acquisition REQUIRES the real store: V3's done-condition (receipt-SHA match, byte-identical re-download) does not move for demo convenience. The store build keeps its queue slot; development is not held for it and not accelerated by it.
### Technical annex — adapter, key format, atomic protocol
StorageAdapter (single seam; provider = config, call sites never change)
  put_once(key: str, data: bytes, content_type: str) -> {sha256, size}
       MUST fail if key exists (write-once)
  get(key: str) -> bytes
  head(key: str) -> {exists: bool, sha256: str, size: int}

Key format:  artifacts/{trace_id}/{artifact_id}.{ext}

Atomic write protocol (no partial artifact is ever visible):
  1 put to {key}.tmp   2 verify sha256   3 move/copy to final key
  4 head-verify        5 write receipt   6 emit ledger row
  failure at any step before 5 => tmp garbage-collected, nothing visible
Receipt binding: the artifact SHA-256 and key land on the outer-gate receipt via the additive version path (receipt v1: artifact_sha256, artifact_key) [STAKED — the buyer must be able to verify independently, which argues on-receipt over sidecar; D4b argued at dispatch].
## 3.3 Benchmark — validation in-phase, calibration as the tuning layer
Restructured per owner review. The architecture never consumes benchmark figures directly — every figure is a [SLOT] filled by config swap — so calibration is safe to run late and continuously. What cannot run late is validation of the perception stack against the material it exists for.
### BM-V — validation (inside Phase 9, one real hour)
BM-V1  One real broadcast hour [OWNER] runs through the perception stack during Phase 9 GPU development. Purpose: go/no-go on model selection for RMS's actual material (multilingual, vernacular, adverse audio) — not numbers. Output: class_distribution_delta against a human-qualified sample of the same hour, reported with a PASS/INVESTIGATE verdict at Phase 9 close.
BM-V2  Deferring BM-V past Phase 9 is prohibited: a perception stack declared complete against synthetic fixtures only is the false-positive condition, not the guard against one.
### BM-C — calibration (post-core tuning layer, continuous)
BM-C1  The tuning layer is the already-designed pair: job telemetry (V1-B4) + versioned config swaps. It runs on real volume after core build, re-runs on every material batch, and owns the measured values: fleet sizing, delivery-band cut-points, price-model inputs.
BM-C2  Anchoring guard: every benchmark output carries provisional: true until cumulative measured hours reach [OWNER: threshold]. Provisional results NEVER auto-flow into price-model or fleet-policy — they land as _proposed configs requiring an explicit owner swap. First numbers are evidence, never doctrine.
### Technical annex — metrics as formulas, output contract
gpu_hours_per_broadcast_hour[m, c] =
    sum(gpu_hours | modality m, hour-class c) / sum(broadcast_hours[c])
unit_yield[c] = qualified_units[c] / broadcast_hours[c]
cost_per_qualified_unit =
    (gpu_hours_total * [OWNER: grant_usd_per_gpu_hour]) / qualified_units_total
class_distribution_delta =
    per-class |machine% - human%| over the reference slice; report max, mean
sustained_bandwidth = bytes_read / wall_seconds during perception reads

benchmark_results.v{N}.json
  { benchmark_run_id, material: {hours, hour_classes},
    measured: {gpu_hours_per_broadcast_hour, unit_yield,
               cost_per_qualified_unit, class_distribution_delta,
               sustained_bandwidth},
    provisional: bool,   cumulative_hours: float }
Swap rule: illustrative -> measured only via config swap stamping
benchmark_run_id; hand-edits prohibited.
## 3.4 Production housing — packaging and the data plane
PH-R1  Packaging (builder-side, destination-agnostic, dispatchable now): containerize from the repository; externalize all secrets from .env to a vault-class store; add healthchecks; split frontend build from backend serve; database address stays env-driven; the LLM swap seam is contained in the single router module and documented. This phase is the audit of the promotion-not-rebuild claim [STAKED — expect pod-specific assumptions to surface and be fixed].
PH-R2  Data plane: managed, replicated database with backup and append-only ledger archival; the artifact store (3.2) provisioned beside it. Per HS3 this MUST precede the first real mined hour.
PH-R3  Domain + TLS bind the public trust receipt (/trace/{id}) to its real URL as config [OWNER: domain].
PH-R4  [OWNER] bindings: production destination; LLM account (the current build is coupled to the platform-managed key; the swap is one module); domain. Demo deployment is permitted any time and carries none of these obligations.
### Technical annex — environment contract, healthchecks, swap seam
Environment contract (every var named; source binding explicit)
  MONGO_URL               vault     required
  JWT_SECRET              vault     required
  LLM_PROVIDER            config    emergent | anthropic  [OWNER: account]
  LLM_API_KEY             vault     required off-platform
  OBJECT_STORE_ENDPOINT   config    [OWNER: store choice]
  OBJECT_STORE_CREDS      vault     required with store
  PUBLIC_BASE_URL         config    [OWNER: domain] · binds /trace/{id}
  Anything else found in .env at packaging = a finding, not a carry-over.

Healthchecks
  GET /healthz  liveness  · no auth, no DB touch
  GET /readyz   readiness · DB ping + frozen-contract parity count

LLM swap seam (single module)
  llm_router.complete(messages, temperature, model) -> text
  provider selection reads LLM_PROVIDER; call sites never change
## 3.5 Seam 3 — the authorized deletion path (before B-5)
S3-R1  An authorized_deletion path lands: retention configuration surface; deletion executes only against a set retention rule; every deletion event is itself ledgered (stamp-audited) — deletion is a governed act, not an erasure of governance.
S3-R2  The standing invariant re-scopes from no_deletion_path to no_unauthorized_deletion_path, with the gate suite updated in the same commit.
S3-R3  Held-classes are enumerated and separately addressable: ledger rows, wizard_transcript (per the standing E5 ruling), delivered artifacts. The DPO may set one window or split per class [OWNER: DPO retention values]. Until set, the system holds indefinitely and says so honestly on the regulator surface — the current truthful default.
### Technical annex — retention config, deletion event, invariant
retention.v{N}.json
  { held_classes: {
      ledger_rows:        { window_days: int | null },
      wizard_transcript:  { window_days: int | null },
      delivered_artifact: { window_days: int | null } } }
  null = indefinite (the honest default until the DPO sets a value)

Deletion event = NorthenaLedgerRow_v1 with stamp_audit:
  { data_class: authorized_deletion, held_class, keys_deleted: int,
    retention_rule_ref: retention.v{N}, actor }

Invariant re-scope
  test_no_unauthorized_deletion_path — AST gate: delete call sites
  exist only in services/retention/authorized_deletion.py
## 3.6 B-5a — Compliance Console, read/prove half
The Compliance Console per UI Specification v2 Section 4. This half is unchanged in scope from what was queued and dispatches first; it does not wait on the checker (3.11).
B5a-R1  UI Spec v2 4.1 Home, 4.2 Prove one run, 4.3 Retention & rights — verbatim, under the adversarial-to-comfort rules: problems surfaced, never all-green walls; read-only; the record itself, not a summary; export on request.
B5a-R2  The retention choice (inheritance default vs per-class split) is surfaced to the compliance owner, not decided by the build. Held-classes render separately addressable: ledger rows, wizard_transcript, delivered_artifact.
B5a-R3  First-commit gating: per-surface Playwright smokes land in the same commit as each surface. The three built G5b invariant gates (class-inseparable, refusal-first-class, single-ingress + trace_id) re-land as UI-Spec-v2 gates.
B5a-G  Gates: B5a-G1 test_compliance_surface_read_only (no write route reachable from this half); B5a-G2 test_prove_run_resolves_any_trace; B5a-G3 test_retention_unset_states_honestly.
## 3.6B B-5b — Compliance Console, rulebook writes under the checker
Adds compliance-rulebook write capability (UI Spec v2 4.4-4.5). Depends on the consequence-class checker (3.11); dispatches after B-5a and after 3.11 lands. [STAKED — the split itself: strike to land B-5 as one phase, keep to sequence read/prove ahead of checker machinery.]
B5b-R1  The Compliance Console owns writes to the compliance rule classes: retention windows, disclosure thresholds (k-anonymity, l-diversity, DP budget), lawful-basis registry, source-standing table. Write UI reuses the plain-language rule pattern (UI Spec v2 6.2 mechanics); no new rule-rendering surface is invented.
B5b-R2  Every compliance-rule write carries a consequence_class (3.11) and routes accordingly: tightening = unilateral with delay + objection; loosening/destructive = pending counter-sign by Administration. Compliance rule classes are OWNED here and render read-only on the Administration Console with an owned-by-Compliance marker (3.13).
B5b-R3  Independence is structural: no Administration approval gates a protection-TIGHTENING compliance change. Only loosening/destructive changes require the Administration counter-sign. A build that subordinates all compliance writes to Administration approval fails this requirement.
B5b-G  Gates: B5b-G1 test_tightening_change_is_unilateral_and_delayed; B5b-G2 test_loosening_change_requires_countersign; B5b-G3 test_compliance_rules_readonly_on_admin_console; B5b-G4 test_every_rule_write_emits_ledger_row_with_consequence_class.
## 3.7 Transform forms §6.3 / §6.4 (post-B-5 phase)
TF-R1  Knowledge artifact, per the owner-confirmed definition: a schema-versioned claim graph — nodes are claims carrying class, contested status, and trace_id; edges are Ring-3 relations; JSON export. Production = selection per reach and standard, then graph assembly. Per-claim provenance intact; grains per_claim and aggregated; delivery hand-over via the outer gate into the artifact store (depends on 3.2); standard enforced as hard input filter.
TF-R2  Callable skill, per the owner-confirmed definition: a stay-running, key-scoped query capability over a corpus slice bound at freeze — not model weights. The slice persists via the artifact store; every response carries class inline through the inner gate's per-call governance; grains per_claim and synthesized_whole per query; access rides the engineer key-grant records.
TF-R3  The grain-compatibility matrix already encodes both forms' cells (verified); wizard offerability for these forms opens when they land — a config change, not a wizard rebuild. The model form remains off the offerable menu and its wizard refusal stands until the owner accepts or rejects the ingredient-manifest guarantee [OWNER — the only honest guarantee training can carry is provenance of ingredients, not of assertions].
### Technical annex — claim-graph schema, skill provisioning record
Knowledge artifact export (ka.v0)
  { schema_version: ka.v0,
    nodes: [ { claim_id, claim_text,
               defensibility: {class, contested: bool},
               trace_id, provenance: {source_ref} } ],
    edges: [ { from_claim_id, to_claim_id,
               relation: corroborates | contradicts | retracts } ] }

Callable-skill provisioning record
  { skill_id, corpus_slice_ref: artifact-store key,
    key_grant_id, floor, scope, endpoint_path,
    provisioned_at, revoked_at?: str }
  Governance: per-call inner gate; every response carries class inline;
  slice bound at freeze and immutable thereafter (new slice = new skill).
## 3.8 Answer fluency — V2 quality completion
FL-R1  LLM synthesis of answer_text lands behind the same frozen ComposedConclusion envelope — no wire change, no new contract. Binding constraint: every sentence MUST be derived from the load-bearing units; invented connective claims are fabrication on a governed wire and fail the gate.
FL-R2  Synthesis runs behind the Shield boundary; LLM unavailability surfaces as infrastructure fault (503), never as refusal and never as silent degrade to the mechanical composition without marking. The current mechanical composition remains the honest fallback and the regression baseline; its derivation gates are replaced only by equivalent gates over the synthesized text at landing.
## 3.9 Dual-actor engineer surface — internal and external engineers
Per UI Specification v2 Section 5.4. The owner architecture states internal and external explicitly, and the enforcement primitives already exist: key class internal|external at registration, path grants, scope enforced server-side per call, grant events ledgered. What was open — the external party's own view — closes as role-scoping on the three existing Engineer screens, replacing the former partner-portal open item. No new surface is built.
EE-R1  A role external_engineer is added to identity.roles. JWT mechanics unchanged; the 4-code auth registry unchanged — external-scope denials are auth_scope_insufficient, access-control class, never outcome=refused.
EE-R2  View scoping: an external_engineer sees Register / First call / Administer scoped to their own apps, keys, usage, and refusal health — and NEVER other parties' apps, estate contents, fleet, pricing, or any master-admin control. Internal engineers retain the current full Section-4 view.
EE-R3  Onboarding [STAKED]: external engineers are invited and approved by an internal engineer; grant issuance to the external class emits the ledger row exactly as built at Phase 8 B-3. Open self-registration is a commercial decision, out of scope here.
EE-R4  Every externally reachable endpoint enforces scope server-side — view-layer filtering alone fails review. Enforcement rides the existing B-1 scope primitive; no parallel mechanism.
EE-G  Gates: EE-G1 test_external_engineer_sees_only_own_apps; EE-G2 test_external_scope_enforced_server_side (direct API probe, not UI); EE-G3 test_external_cannot_reach_admin_or_fleet_routes (403, access-control body); EE-G4 first-commit per-surface smokes per standing pattern.
### Technical annex — role scoping matrix
Capability            internal_engineer      external_engineer
apps visible          all                    own only
grants visible        all                    own only
register app          yes                    own, via approval (EE-R3)
issue / revoke keys   yes (ledgered)         own keys only (ledgered)
usage & refusal view  all apps               own apps only
estate contents       never (not their job)  never
fleet / pricing       no (master_admin)      no
Sizing: role + scoping on existing screens; band proposed at dispatch (small).
## 3.11 The consequence-class checker (cross-console)
A checker for consequential rule changes, attached to CONSEQUENCE not to ROLE. Rationale, binding: attaching the check to role (e.g. Administration approves all compliance changes) subordinates compliance to operations and inverts data-protection independence — the compliance owner's protection-tightening change must not wait on an operational veto. Attaching to consequence gives the second-pair-of-eyes where it matters and binds symmetrically.
CK-U1  User-facing: pending items appear on BOTH consoles' banners. The counter-signing console sees the full plain-language consequence statement before signing. Commit line binding copy: 'Signed by {initiator} - counter-signed by {checker} - recorded with both identities.'
CK-I1  Integration: no new frozen contract. A rule-class registry attribute consequence_class: constrained-str { tightening_unilateral | dual_control } via the established versioned-registry pattern (never a Literal that will widen).
CK-B1  Backend, dual_control path: a change enters pending_counter_sign state; it takes effect ONLY on the second console's signature. Both identities and both timestamps land in ONE NorthenaLedgerRow_v1 (stamp_audit: {data_class: countersigned_rule_change, initiator, checker, consequence_class}). No second contract, no in-place mutation.
CK-B2  Backend, tightening_unilateral path: effective after [config: effective_delay]; a recorded-objection path escalates to the owner; the objection is itself ledgered. The delay is config, not code.
CK-B3  Symmetry: Compliance-initiated loosening is counter-signed by Administration; Administration-initiated loosening (e.g. a retention-relevant taxonomy change) is counter-signed by Compliance. Neither console is senior to the other on this axis.
CK-H1  Behavioral honesty carried into the build record: while one person holds both roles, dual-control is ceremony; the seam is built now because it is cheap now and expensive to retrofit. The gate proves the mechanism, not the staffing.
CK-G  Gates: CK-G1 test_dual_control_blocks_until_countersign; CK-G2 test_countersign_row_carries_both_identities; CK-G3 test_tightening_effects_after_delay_with_objection_path; CK-G4 test_symmetry_admin_loosening_needs_compliance_countersign; CK-G5 test_consequence_class_is_registry_not_literal.
### Technical annex — checker state and ledger shape
rule_change_request (transient, not a frozen contract)
  request_id, rule_class, from_value_ref, to_value_ref,
  consequence_class: tightening_unilateral | dual_control,
  initiator_id, initiated_at,
  state: pending_counter_sign | pending_delay | effective | objected,
  effective_at?: str        # set on countersign or on delay expiry

Counter-signed change -> NorthenaLedgerRow_v1 stamp_audit:
  { data_class: countersigned_rule_change, rule_class,
    consequence_class, initiator, checker,
    initiated_at, countersigned_at }
Config: consequence_class.v{N}.json maps each rule_class -> class;
        effective_delay in the same versioned config.
## 3.12 The sampling primitive (cross-console)
ONE platform primitive - a first-class narrow-reach objective - with two console expressions. It exists because full extraction carries a real resource commitment and because feasibility honestly returns unknown on un-censused reach. No new governance machinery: both control instruments (budget ledger, disclosure ledger) already exist.
### Extraction expression (lands with Phase 9, 3.1)
SM-E1  A sample is a narrow-reach objective whose result grounds the full commit. User-facing: a Run-a-sample action on the wizard once reach is drafted; result renders in the feasibility position (volume found, class distribution, per-hour cost observed) and records into the commit envelope.
SM-E2  Backend: sample cost draws the objective's GPU/extraction budget and is shown doing so. The commit review carries a grounding marker - binding copy 'Grounded by sample {sample_ref}' or 'No sample run - estimates only'. A sample converts feasibility unknown into evidence; it grounds estimates and does not guarantee full-run yield.
SM-E3  Data & housing: a sample runs the normal intake + qualification path; its units persist like any qualified units, tagged sample_of={objective_ref} so they are not mistaken for a committed run's output.
### Integration expression (post-artifact-store; fixture-marked demos meanwhile)
SM-I1  A buyer-side sample of the actual pull, before purchase. THE HARD RULE: a sample IS an egress - it passes the FULL outer gate (rights, irreversibility, cumulative disclosure, license) AND counts against the cumulative-disclosure budget. A sample that bypassed either would be the assembly attack the disclosure ledger exists to catch: buy nothing, sample repeatedly, reconstruct the dataset.
SM-I2  User-facing: 'Sample this pull' on the acquisition rail; the sample delivers with its own mini-receipt; priced per [config: sample_pricing] (free or nominal is a pricing decision; the mechanism is identical). Fixture-backed demo samples carry the AS-U2 sample marking and schema gate; real-material samples are real egress, receipt and all.
SM-I3  Backend: the sample deliverable is written through the same outer-gate path and artifact store (3.2) as a full acquisition; its disclosure draw is recorded against the buyer's cumulative budget BEFORE the sample egresses, not after.
SM-G  Gates: SM-G1 test_extraction_sample_grounds_commit_envelope; SM-G2 test_integration_sample_passes_full_outer_gate; SM-G3 test_integration_sample_debits_disclosure_budget; SM-G4 test_repeated_samples_hit_disclosure_ceiling (the assembly-attack gate); SM-G5 test_sample_units_tagged_not_committed.
## 3.13 B-4 retrofit — compliance rules read-only on Administration (scheduled)
A change to already-shipped B-4 screens, scheduled explicitly rather than left implied. Per UI Spec v2 6.4, the Administration Console owns operational rule classes only; compliance rule classes move to the Compliance Console (3.6B) and render on Administration READ-ONLY.
RT-R1  The B-4 Master Admin surface renders retention, disclosure thresholds, lawful-basis registry, and source-standing table read-only with an owned-by-Compliance marker; their write controls are removed from this console. Operational classes (pricing, fleet, taxonomy, tier lock) are unchanged.
RT-R2  Lands with B-5b (the console that receives the write ownership) so the move is atomic - write capability never exists in neither console nor both. Gate: RT-G1 test_compliance_classes_have_no_write_route_on_admin_console.
## 3.14 Recorded open — not specified here
Fleet arbitration beyond simple apportionment (until concurrency actually bites). Pricing values (owner, through instrumented practice). Five governance seam values (owner / DPO / MEA), landing as config swaps. Hosted multi-tenant operation (HS5 records single-tenant-per-client as the current posture; multi-tenant is a later product decision, unspecified here). Every future proposal passes the 1.6 placement rule.

# 4. The housing map

| Environment | Runs | Holds | Trust posture |
| --- | --- | --- | --- |
| RMS estate | Source systems; under Topology A also the GPU workers | Raw AV (always), CMS, social records | Highest; raw's home tenancy |
| GPU zone (layer 1) | Perception workers, stub-first | Raw transiently; purged per job | Lower than control plane; job seam only |
| Control plane (layer 2 + core) | Governance core, transform layer, wizard, Shield/LLM | Database (Registry, units, Ledger), artifact store, all keys | System of record; single Ledger writer |
| Consumer edge | Buyer apps, integrations, public receipt | Nothing durable | Untrusted; reached only through gates |


Custody map. Transform keys: control plane only. Ledger-write: control plane only. LLM key: Shield, control plane only. JWT secret: control-plane secrets store. Worker credential: the only worker-side secret; unlocks job-fetch and result-post, nothing else.
Never-rules (every topology): raw AV → consumer edge: NEVER. Transform key → GPU zone: NEVER. Worker → Ledger: NEVER.
Binding slots [OWNER]: archive access path (format, storage, bandwidth) · GPU placement (grant terms + archive reality select Topology A/B) · LLM account · object-store choice · domain + TLS. Every other housing requirement in this document is deliverable identically on any major cloud or on-premises; naming a provider before these facts land would pre-decide a commercial negotiation, not an engineering question.
# 5. Sequencing
## 5.1 Builder-side order
1. B-4 Master Admin close (in flight) → Seam 3 mini-phase (3.5) → B-5a Compliance read/prove (3.6) → checker (3.11) → B-5b Compliance rulebook writes (3.6B) + B-4 retrofit (3.13, atomic with B-5b) — completes the surface set and the compliance write path.
2. Production packaging (3.4, PH-R1) — destination-agnostic; pulls earlier than B-5 if the pod constraint actively bites, otherwise follows it.
3. Artifact store (3.2) — the only gap that is purely a decision plus a small phase; unblocks V3's done-condition and is a dependency of 3.7.
4. Phase 9 Extraction (3.1) — Stage A dispatchable on this document alone; Stage B's GPU half and the benchmark (3.3) execute when the [OWNER] material and topology facts land.
5. 8-EXT dual-actor engineer scoping (3.9) — small; after B-5b, before Phase 9 Stage B.
6. Transform forms (3.7) and fluency (3.8) — post-B-5b; both ride existing envelopes and gates.
7. Sampling primitive (3.12): the extraction expression lands inside Phase 9; the integration expression lands after the artifact store (3.2). The checker (3.11) lands between B-5a and B-5b.
## 5.2 Owner-side critical path
Two clocks, deliberately separated. Early (facts, not data): archive access path and GPU placement — these gate Phase 9 Stage B housing design and are the RMS/grant-provider conversation. In-phase (small): one validation hour + its human-qualified sample for BM-V, needed during Phase 9 GPU work, not before. Post-core (volume): calibration material for BM-C flows through the tuning layer continuously; first numbers stay provisional until the [OWNER] threshold. The LLM account, domain, store choice, and data-plane destination are administrative and gate only the packaging phase. The builder never waits on owner items except where marked [OWNER]; owner items never wait on the builder. The one hard rule stands: the data plane goes production before the first real hour is mined.


# 12. The commercial cut — subtractive change with mandatory preservation
Owner ruling, 2026-07-06: the extractor has no commercial attributes. Data sales is an application-layer service (UI Spec v2.1 Section 12). Everything commercial already built is cut from the extractor and preserved for the future Sales Service. This is the build's first SUBTRACTIVE change — the doctrine to date is additive-only — so it is specified with its own gates. Nothing is deleted; preservation is verifiable, not asserted.
## 12.1 What is cut
CUT-1  Phase 7 B-2 buyer wizard variant in full: buyer state machine, shape-with-price, offerability-as-sales. The OPERATOR wizard is untouched — only the buyer variant is cut.
CUT-2  Phase 6 commercial half: price-model configs, quote instrumentation, and the dual-delta {price_delta, class_delta} logic. Phase 6 INTERNAL half (fleet apportionment, cost-per-unit telemetry) STAYS — the extractor needs its own cost to manage capacity.
CUT-3  Frozen contract QuoteEnvelope_v0 (parity slot 21) and AsyncDeliveryAccepted quote-field coupling: see 12.3 for the orphan-vs-vacate ruling.
CUT-4  UI: the Commercial Reference Application (former UI v2.0 §7.2) and pull-sampling-for-purchase. The extraction sample (3.12 SM-E) STAYS; the pull sample (SM-I) is cut.
## 12.2 Preservation of code — mandatory
PRES-1  Cut code moves to a salvage location OUTSIDE the extractor build tree — a separate directory or branch — removed from the extractor's tree, test suite, and CI. Not a disable flag: flagged-inert code still lives in the dependency graph and re-introduces the fusion the cut exists to remove. [BUILDER-CAPABILITY: whether the salvage location can live inside the same repo outside the build tree, or must be a second repo, is a builder question answered at dispatch — not assumed here.]
PRES-2  Honest preservation limit, stated so it is not oversold: salvaged code is a tested REFERENCE implementation for the Sales Service, not a runnable module that switches back on. It assumed extractor scaffolding (auth, contracts, gates) it no longer sits inside. The design and logic survive intact; the wiring does not.
## 12.3 Preservation of frozen contracts — orphan-in-place [STAKED]
PRES-3  QuoteEnvelope_v0 and commercial configs: ORPHAN-IN-PLACE. The contract file and its snapshot STAY on disk; parity count is UNCHANGED (26); nothing live imports them. A salvage copy goes to the Sales Service location. Audit history stays literally true (the contract really was frozen at slot 21) and no subtractive precedent is set in the frozen-contract doctrine.
PRES-3-ALT  [STAKED — the alternative is VACATE: remove the contract, parity 26→25. This is the first subtractive move against an additive-only invariant and would require its own HAZARD-STOP ruling and a revision of the mechanical-parity invariant to admit a monotonic-count break. Orphan-in-place is the recommended path precisely because it avoids this. Owner strikes to choose vacate.]
## 12.4 The salvage manifest — named acceptance gate
MAN-1  The cut phase produces a salvage manifest: every moved artifact — what, from where, to where, at what pre-move and post-move SHA. 'Preserved' is verified against this manifest, not claimed. Gate MAN-G1: test_no_commercial_symbol_in_extracator_tree (grep-negative on price/quote/buyer symbols in the live tree); MAN-G2: manifest lists every cut artifact with both SHAs; MAN-G3: extractor CI green with the commercial test surface removed, not skipped.
## 12.5 The boundary after the cut
BND-1  The extractor retains: internal cost/capacity economics (Administration Console), the governed-extract API (UI v2.1 5.5), the operator wizard, all four consoles. It has NO price, quote, offer, catalogue, order, or buyer concept.
BND-2  The Sales Service, when built, is a client of the governed-extract API with a scoped external key, passing the full outer gate including the cumulative-disclosure debit on every egress — samples included. No privileged path exists for the RMS-owned sales business; a disclosure-free or gate-free path would be separation in name only and fails this requirement. [STAKED: single sales business assumed; marketplace (multiple resellers) changes the key model and is an owner ruling before the Sales Service is specified.]
## 12.6 Sequencing
The cut is a discrete phase. It SHOULD run before further commercial-adjacent work would deepen the fusion, and it is independent of the operator-surface queue (B-4/B-5/Phase 9) — it touches only the commercial code those phases do not depend on. It does not block, and is not blocked by, the surface build.
— End of Build Completion Requirements v1.0 —
