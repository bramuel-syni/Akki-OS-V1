# Phase 9 Sub-stage 9.2a · Owner Rulings 9.2a-E1..E4

**Dispatch:** Owner post-Stage-A relay (2026-07-10).
**Applies to:** Stage A proposal `docs/stage_a_proposals/9_2a.md` (post-rename to `9.2a-E*` naming per Owner Ancillary 1).
**Governance model:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`.
**Standing Rule v3:** on-disk canonical.

---

## §1. Owner rulings — VERBATIM

### §1.1 9.2a-E1 — α, one correction: seed with the CI fixture model's entry

> **9.2a-E1 — α, one correction: the registry does NOT seed empty — it seeds with the CI fixture model's entry.** "Empty per data-blind" misapplies the posture: data-blind governs assumptions about the *estate's content*, not tool provenance — a model registry entry is tooling attestation, and an empty registry plus a provenance gate is the CD-E3 deadlock again (nothing can pass). Seed `models_registry.v0.json` with `whisper-tiny` pinned (SHA + license + origin URL) as the CI fixture model; production models land additively at 9.2b via the registry bump, selected then. "Whisper-class" resolves as: CI = whisper-tiny pinned now; production model = 9.2b decision.

**Applied at execution:**
- `backend/services/perception/models_registry.v0.json` seeded with whisper-tiny (SHA `dcb76c65…` + MIT license + HF origin URL `https://huggingface.co/Systran/faster-whisper-tiny`).
- `backend/services/perception/model_registry.py::attest_model(model_id)` — runtime enforce; hard-fails on unregistered model.
- `register_model(...)` — additive v(N)→v(N+1) bump for 9.2b production-model registration; matches CD-E3 α + TF-E3 α versioning pattern.
- Gate 9.2a-G1 attests the seeded entry + attest_model behaviour + provenance-superset over worker `MODEL_ID` references.

### §1.2 9.2a-E2 — α, two conditions

> **9.2a-E2 — α, two conditions.** (1) **No silent default at deployment:** env var unset → explicit import-time failure, never a silent fallback to CPU — a GPU deployment quietly running CPU is the silent-swap risk in the other direction. CI sets `cpu` explicitly. (2) **`execution_mode` lands in result telemetry** — attribution of GPU-hours and yield to a mode the record doesn't carry is the same fabricated-attribution gap E1 closes for models. One field, honest attribution.

**Applied at execution:**
- **Condition 1:** `backend/services/perception/gpu_execution/cuda_runtime.py` reads `PERCEPTION_EXECUTION_MODE` at module-import time. UNSET → `raise ImportError("...no silent fallback...")`. Invalid value → `raise ImportError("...invalid...")`. Valid values are the closed 2-set `{cpu, gpu}`. CI sets `cpu` via `backend/.env` + `tests/conftest.py` `os.environ.setdefault("PERCEPTION_EXECUTION_MODE", "cpu")` (before any perception import at collection time).
- **Condition 2:** `backend/services/perception/execution_mode_telemetry.py::annotate_result(job_id, telemetry_dict)` returns a NEW dict (non-mutating) with `execution_mode` + `_execution_mode_attribution_job_id` fields. Both ASR worker and diarization worker paths invoke `annotate_result` before serialising telemetry to the V1-B4 sidecar. Stub-worker telemetry is ALSO annotatable via the same helper (symmetry attested at 9.2a-G3).
- `PerceptionResult_v0` frozen contract is NOT mutated — `execution_mode` ships as a sidecar/observability payload, preserving parity 31.
- Gates 9.2a-G2 (env-var gate) and 9.2a-G3 (telemetry attribution gate) attest both conditions.

### §1.3 9.2a-E3 — α, with the discriminator verified before it's trusted

> **9.2a-E3 — α, with the discriminator verified before it's trusted.** Non-empty-units discriminates only if the stub genuinely emits zero units on this path — the proposal asserts it; the test must not assume it. If the stub emits canned units here, the discriminator becomes **input-sensitivity**: two different audio fixtures → different unit sets (the stub is input-independent by construction; a real model cannot be). Land whichever discriminator the stub's actual behavior supports, state which in the close. β stays rejected per P9-E7's own text — quality is BM-V's.

**Applied at execution:**
- **Discriminator verification cell** landed at `test_9_2a_g4_discriminator_verification_stub_emits_zero_units_on_fixture_audio`. This cell runs `stub_worker.process_job_deterministically` against `fixture_a_silence.wav` and `fixture_b_tone.wav` and asserts `len(result.units) == 0` in both cases. Passes GREEN → stub confirmed zero-emitting on the fixture-audio path.
- **Chosen discriminator: (a) non-empty units.** Rationale: stub verified to emit 0 units unconditionally on fixture-audio; real ASR + real diarization workers emit ≥1 unit per handle (verified at execution).
- **9.2a-G4 P9-E7 rider cells** (`test_9_2a_g4_p9_e7_rider_sm_g1_against_real_perception_asr` + `test_9_2a_g4_p9_e7_rider_diarization_symmetry`) assert:
  1. Real perception module ≠ stub module (identity check).
  2. Wire-shape identity: `PerceptionResult_v0` validates.
  3. `grounding_marker` renders — P9-E6 α em-dash verbatim.
  4. Discriminator (a): real ≥1 unit AND stub = 0 units on the same fixture-audio.
- β is not landed (Owner: "β stays rejected per P9-E7's own text — quality is BM-V's").

### §1.4 9.2a-E4 — α as specified

> **9.2a-E4 — α as specified.** V1-H2 mandates mechanical; the grep-negative + scope-walker + whitelist is the established §6.10 pattern (AS-G6/TF-G9/CD-G3 lineage). No conditions.

**Applied at execution:**
- `backend/tests/invariants/test_9_2a_purge_ast_gate.py` lands the §6.10 reflection-gate class.
- **Cell 1** — grep-negative on `self.raw_audio =`, `self._audio_bytes = `, `self._audio_cache = `, `self.audio_bytes_cache = `, `self.raw_pcm = ` patterns across `asr_worker.py` + `diarization_worker.py` + `gpu_execution/*.py`. Docstring-mention whitelist via `_is_only_inside_docstring` heuristic.
- **Cell 2** — AST module-level scan for forbidden ALL-CAPS audio-buffer names (`AUDIO_BYTES`, `RAW_AUDIO`, `AUDIO_CACHE`, `RAW_PCM_BUFFER`, `GLOBAL_AUDIO`).
- **Cell 3** — AST walker: `asr_worker.process_job` + `diarization_worker.process_job` MUST construct `PurgeAttestation` in their scope; asserts purge-attestation call before return.
- **Cell 4** — AST caller scan: `_read_handle_bytes` return values MUST be assigned to function-local `ast.Name` targets; class-attribute `ast.Attribute` targets are violation.
- Named 9.2a-G5.

---

## §2. Ancillary rulings applied at this commit's STEP A (Owner, 2026-07-10)

### §2.1 Ancillary 1 — Escalation ID naming correction

> correct to 9.2a-E1..E4 at the next commit's STEP A. Not cosmetics: the 'CD-' prefix files these under census-dimensions in every future grep and rulings-record lookup — phase-scoped IDs are how five phases of rulings have stayed retrievable. One-line fix.

**Applied inline at this commit's STEP A:** `docs/stage_a_proposals/9_2a.md` renamed `CD-9.2a-E*` → `9.2a-E*` (all headings + cross-references). This rulings record file (`9_2a_e1_to_e4.md`) written fresh under correct naming.

### §2.2 Ancillary 2 — Fixture-refresh queued as post-9.2a mini-phase

> correctly escalated, and the answer is a scoped mini-phase after 9.2a close, not a ride-along. The builder's instinct to stop was right — a HAZARD-STOP-protected fixture plus a v0→v1 registry bump plus a ~10-file cascade is a coordinated change, and coordinated changes don't ride housekeeping commits. It queues as a named mini-phase post-9.2a: one Stage A (small), the HAZARD-STOP posture question surfaced there as its Tier-1 item, license_class_map v0→v1 additive per standing pattern. Until then it stays deferred-and-disclosed, which is its current honest state.

**Applied at this commit's STEP A backlog update:** `memory/PHASE_STATE.md` + `memory/PRD.md` queue "Fixture Refresh mini-phase" as next post-9.2a active lane (see §5 sequenced work).

---

## §3. Ruling recorder

- **Owner text on disk (this file):** all rulings verbatim, no paraphrase, no trimming.
- **Applied-at-execution notes** are the builder's disclosure of how each ruling landed in code + tests.
- **Anti-regression discipline:** any future dispatch modifying `CensusContentDimension`-adjacent OR PerceptionWorker-adjacent contracts MUST reference this rulings record.

═══════════════════════════════════════════════════════════════════

*End of 9.2a Owner rulings record. Standing Rule v3: on-disk canonical.*
