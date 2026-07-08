# Rulings Record — Phase 9 Stage A · P9-E1..P9-E7

**Companion to:** `docs/rulings/seam_3_stage_a_e1_to_e7.md`
**Ruling authority:** Owner dispatch 2026-07-08
**Applied via:** Amendment I on `/app/docs/stage_a_proposals/phase_9.md`
**Sequence directive:** Amendment I → Sub-stage 9.1 + 9.3 atomic first-commit dispatch (per §4.1 baseline)

## File header — SHA-anchored context

- Phase 9 Stage A proposal at Amendment-I landing: file `/app/docs/stage_a_proposals/phase_9.md` (SHA-256 recorded post-write via `sha256sum`; see close-report cross-reference at Sub-stage 9.1 close).
- Original Stage A pre-Amendment-I dispatch SHA: `7be3f60b5d1afb0c681804558a8c71232db9db6b53304074393d441d546642c3`.
- BCR v1.4.1 authority: `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524`.
- UI Spec v2.1 authority: `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2`.
- Conformance map: `e747a0f6ee815b003d4962dac515b0743451747b1ef4812fa824e6cbe98874e7`.
- Prior rulings record (Seam 3 Stage A E1..E7 + R-1..R-6 + Ruling 7 + B5b-E1..E5 + Amortisation Divergence Class): `c89cacc606eda955c7fbde62e1ad1f01e381ad6ab80ae6501e39112057f0a6bb`.
- rule2_accounting.json (post-Amendment-I, Phase 9 Stage A entry appended): SHA recorded post-write at Sub-stage 9.1 close.

## §1. Owner rulings on P9-E1..P9-E7 (verbatim, no paraphrase)

### P9-E1

P9-E1 — α, FREEZE. Parity 26→28 additive at 9.1 landing. The environment-boundary prior holds: two codebases must agree on this wire, and a liquid contract under a stub-first regime means the stub proves a shape that can drift before the GPU consumes it — β is the false-positive generator. γ collapses into α: frozen-field-changes-as-new-versions already reserves the v0→v1 bump right permanently; "staged" restates standing doctrine as if it were a new option. If 9.2's GPU shape reveals field gaps, v1 lands beside v0 per that disposition — priced then, not feared now.

### P9-E2

P9-E2 — α, not γ. Locator stays opaque free-form, owned per-adapter. γ is rejected as a documentation-registry with zero consumers: nothing parses foreign locators — units carry source identity and route back to their owning adapter. B5b-E3's γ precedent doesn't transfer: disclosure_type was a validated request parameter (load-bearing registry); this registry would validate nothing while implying locators are governed. Extract-on-second-use applies — if a cross-adapter locator consumer ever exists, the registry lands then. One binding condition: each connector's cells prove locator round-trip (write → re-read → same source region) — the governance need is that re-extraction works, not that dialects are cataloged. β correctly ruled out structurally.

### P9-E3

P9-E3 — α, capabilities-claim worker JWT, two conditions. The allowlist shape: the credential names its exact two operations, rather than a role implying operations via route configuration — same up-from-permitted principle as the B-5a trace ruling. Conditions: (1) worker-auth denials use the existing 4-code registry, no new codes — registry stays closed; (2) "all other routes reject worker_jwt" is proven by a parametrised negative gate (worker credential against representative non-worker routes → 403 access-class), not convention — V1-G5's AST covers the code side; this covers the credential side.

### P9-E4

P9-E4 — α. Byte-identity asserts over all contract files present at each close; the set grows additively; the quoted parity is the current count (28 post-9.1). Naming clarification, enforcement identical, no ceremony.

### P9-E5

P9-E5 — Phase 9 CLOSES on INVESTIGATE, with three bindings. BM-V2 prohibits deferring the measurement, not recording an honest negative — and a verdict that blocks closure creates pressure to shade it toward PASS, the exact corruption a two-state honest verdict must resist. INVESTIGATE is a first-class outcome, same doctrine as refusal-occupies-the-answer-position. Bindings: (1) verdict + delta numbers land verbatim in the close report — outcome, not footnote; (2) V1 stays PARTIAL on the grid — Phase 9 closed ≠ V1 complete; V1 completes only on PASS; (3) no production mining on an INVESTIGATE stack — real-material extraction beyond validation runs waits for PASS; remediation is a named owner-ruled follow-up under BM-C's provisional discipline. Close the phase; don't unlock the mine.

### P9-E6

P9-E6 — α. E7 resolved a two-document glyph conflict by making UI Spec authoritative; here no conflict exists — UI Spec §3.3 is unambiguous and the em-dash is a syntactic pause, not a list separator. Binding copy is verbatim including the em-dash; the test asserts the exact string. γ rejected: a test passing on two different strings is an unsatisfiable-spec generator.

### P9-E7

P9-E7 — SM-G1 proves against the stub; 9.3 closes independently; §4.1 baseline holds. The gate asserts pipeline mechanism — sample flows through intake, result grounds the envelope, marker renders — none of which depends on perception quality; quality is BM-V's job, and conflating them would make the console surface hostage to the RMS facts for zero mechanism-level gain. One rider: 9.2's roster includes one cell re-asserting SM-G1 against real perception — the stub-proven loop closes at the natural moment, same first-contact re-verification pattern as the conformance map.

## §2. Ratifications (verbatim)

- §1 cell-density including the amortisation rows — RATIFIED.
- §4.2 pre-authorized split thresholds — CONFIRMED, no round-trip at trigger.
- Band [2,850, 3,650] — RATIFIED subject to Amendment I: E2 removes the registry, E3 adds negative-gate cells, E7's rider is a 9.2 cell (outside this band); re-derive per §1.4 rates, restate at dispatch, execute.

## §3. Sequence directive (verbatim)

SEQUENCE: Amendment I → 9.1 + 9.3 dispatch (9.1 first commit carries the stub-first gate roster).

## §4. Directives for the code work (verbatim, Owner-binding at dispatch)

- **§4.1 baseline atomic commit** — 9.1 substrate + 9.3 console land as one atomic first commit set per phase-9 discipline. 9.1 first commit carries the stub-first gate roster (V1-G1..V1-G7 land alongside the stub worker + contracts + endpoints, not deferred).
- **Frozen contracts:** PerceptionJob_v0 + PerceptionResult_v0 land under `backend/contracts/` with JSON snapshots under `backend/tests/invariants/`. Parity bumps 26→28 at this commit. V1-G7 assertion set expands to 28. Add-not-touch on all 26 pre-existing.
- **Worker credentials:** capabilities-claim JWT with `capabilities: [worker_claim, worker_result]`. Server-side capability check on the two worker routes; parametrised negative-gate proves worker credential → 403 access-class on ≥3 non-worker routes. Denials reuse existing 4-code registry — no new codes.
- **Locator:** `locator: str` on NormalizedUnit stays byte-identical (STANDING 26 preserved on the 26 pre-existing). Each of 3 connectors proves locator round-trip (write → re-read → same source region) inside its happy-posture cell.
- **Grounding marker copy:** exact UI Spec §3.3 verbatim string including em-dash "—". Test asserts the exact string.
- **SM-G1:** proves against stub worker at 9.3 close. 9.3 close-independence from 9.2 stands per §4.3.
- **BM-V:** runs at 9.2 only (out of scope this dispatch). Do not stub BM-V in 9.1/9.3.
- **Close-report discipline (per P9-E5 bindings):** even though BM-V runs at 9.2, ensure the close-report template for 9.1 and 9.3 flags the V1 grid as PARTIAL and reserves the verdict+delta slot for 9.2's close.
- **§4.2 split thresholds:** if 9.1 delivery ≥3,500 LoC OR ≥45 cells → split 9.1a stub-only + 9.1b connectors autonomously, disclose in close. If 9.3 delivery ≥2,200 LoC OR ≥35 cells → split 9.3a sample-flow + 9.3b registry-admin/quality-observation autonomously, disclose in close. No Owner round-trip at trigger.
- **Standing Rule v3:** on-disk canonical close reports at `/app/docs/close_reports/phase_9_sub_stage_9_1.md` and `.../phase_9_sub_stage_9_3.md` at each close. No inline full-code pasting to me — reference file paths + line ranges.
- **Test posture at each close:** Pytest, Jest, Playwright chromium must all land green. Cell counts and LoC actuals disclosed vs the amended band.

## §5. Report cadence (verbatim)

Return at these points only:
- End of STEP 2 (amendment landed + dispatch restatement).
- At any §4.2 threshold trigger (disclose autonomous split at execution time; do not wait for approval).
- End of 9.1 close (close report + honest cell/LoC actuals + gate roster verification).
- End of 9.3 close (close report + honest cell/LoC actuals + gate roster verification + V1 grid state).
- Any hard blocker requiring Owner semantic ruling.

Do NOT return for progress checkpoints between STEP 2 and 9.1 close unless a blocker hits. Standing Rule v3: on-disk canonical is the record.

## §6. Cross-references

- Amendment I applied to Stage A proposal at Phase 9 Stage A file (§Amendment I § 1..§8).
- Amortisation Divergence Class ratified verbatim at ratification §1 above; codified at Stage A §1.2 + §1.3.
- Sub-stage 9.2 remains gated on 9.2-OWN-1..3 [OWNER] facts per Stage A §2.2; Amendment I preserves this gate. SM-G1 real-perception re-assertion (P9-E7 rider) folds into 9.2 roster.

═══════════════════════════════════════════════════════════════════

*End of Phase 9 Stage A rulings record. Standing Rule v3 on-disk canonical.*
