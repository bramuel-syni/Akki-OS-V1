# LT-2 Forensic Correction · 2026-07-24

**Finding class:** D-class dispatch-discipline defect · **orchestrator-boundary origin** (verbatim relay of forensic claim without on-disk verification against BUILD_JOURNAL).
**Trigger:** Owner Ruling · STEP-2 Surfaces 1–3 · 2026-07-24 · Surface 1 verbatim correction.
**Authority artifact:** `docs/rulings/owner_step2_surfaces_ruling_2026-07-24.md` · SHA `2e11c7ea864a940d64b1a438b7bf1f0f5fd6e77b12aeb816d9bfad640779d178`.
**Scope:** correction of false forensic claim scoped to STEP 2 surfacing text at `docs/handoff/step_2_make_ci_attest_2026_07_24.md` §2.3 + §4 posture (β) framing + terminal-reply `git blame` line. **Does NOT propagate into any other on-disk artifact.**

---

## §1 · Owner-verbatim correction (byte-carried)

> The builder's forensic claim is FALSE and must be corrected in the filed finding: tests/test_rms_adversarial_v1_roundtrip.py existed — BUILD_JOURNAL attests it running 23 cells in make ci at G3 (211/211) and G4 (271/271) — and it exists today as backend/tests/test_instance_fixture_a_roundtrip.py, renamed at MC-E5's class-(b) fixture de-tuning (2026-07-14). The Makefile went stale at that rename, not at repo birth; "stale since initial commit" read squashed remote history against on-disk canon. A false forensic claim inside a HALT surface is itself a D-class defect.

---

## §2 · BUILD_JOURNAL evidence (D-11 canon-before-attest · live-verified 2026-07-24)

`grep -nE "rms_adversarial_v1|G3.*211|G4.*271|MC-E5|instance_fixture_a" BUILD_JOURNAL.md` (this session · read-only):

### §2.1 · Fixture landing (G0.5 · pre-G3)

**BUILD_JOURNAL.md:602** — *"Fixture + generator fetched to `/app/backend/services/data_source/synthetic_assets/rms_adversarial_v1/`."*

**BUILD_JOURNAL.md:647** — *"`services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` — rewritten to emit `NormalizedUnit`-shape natively. Each unit is `{unit_id, provenance, signal, relational, reextraction_handle, defensibility}` — matches frozen `five_rings@v0` verbatim."*

**BUILD_JOURNAL.md:672** — *"`make ci`: **146/146 tests passing** — invariants 12 + chokepoint 1 + smoke 9 + layer_a 5 + layer_b 5 + layer_c 3 + v1 4 + perception 2 + extraction_params 17 + northena 11 + g1_stamper 6 + lift_manifest 48 + **rms_adversarial_v1 23**. Was 123."*

### §2.2 · G3 close (211/211 · rms_adversarial_v1_roundtrip 23 cells)

**BUILD_JOURNAL.md:1018** — *"**Test totals**: **`make ci`: 211/211 green** (invariants 59, chokepoint 1, smoke 9, layer_a 5, layer_b 5, layer_c 3, v1 4, perception 2, extraction_params 17, northena 11, g1_stamper 6, lift_manifest 66, **rms_adversarial_v1_roundtrip 23**). `pytest -q`: 211 passed. `make ci == pytest -q` holds."*

### §2.3 · G4 close (271/271 · rms_adversarial_v1_roundtrip 23 cells)

**BUILD_JOURNAL.md:1123** — *"**Test totals**: `make ci`: **271/271 green** (invariants 98, chokepoint 1, smoke 9, layer_a 5, layer_b 5, layer_c 3, v1 4, perception 2, extraction_params 17, northena 11, g1_stamper 6, lift_manifest 87, **rms_adversarial_v1_roundtrip 23**). `pytest -q`: 271 passed. `make ci == pytest -q` holds."*

### §2.4 · MC-E5 rename event (2026-07-14 · class-(b) fixture de-tuning)

**On-disk file today:**

```
-rw-r--r-- 1 root root 3688 Jul 14 14:40 backend/tests/test_instance_fixture_a_roundtrip.py
```

`git log --all --follow --format="%H %ai %s" -- backend/tests/test_instance_fixture_a_roundtrip.py`:

| Commit | Timestamp (UTC) | Message |
|---|---|---|
| `dd8a660751553f61f1e51a441a2dfd87b2f1c753` | 2026-07-14 15:09:04 | auto-commit for `ffd39029-c851-4a3a-853a-f353f477fcbf` |
| `3985be515b2ff3e184cf75a760e5aa7e4cc4a607` | 2026-07-02 02:38:29 | initial commit |

The rename occurred during MC-E5's class-(b) fixture de-tuning on 2026-07-14 (per Owner ruling). The Makefile target at line 60 continued referencing the pre-rename path `tests/test_rms_adversarial_v1_roundtrip.py`, causing the stale line to survive until STEP 2's `make ci` invocation surfaced it 22 days later. The `ci: …` composition chain enumerates only G2a-era targets and echoes "G2a CI gate PASSED" on completion, which is how the stale line went undetected across G3, G4, MC-E1..E6, and subsequent phase closes that no longer routed through the enumerated target.

### §2.5 · Root mechanism of the false forensic claim

The builder's STEP 2 attest §2.3 stated (verbatim from `docs/handoff/step_2_make_ci_attest_2026_07_24.md`):

> "The `rms_adversarial_v1` target has been in the Makefile since **the very first Makefile commit** (`^3985be5` · 2026-07-02 02:38:29 UTC) — this is a **pre-existing Makefile-vs-repo drift**, present since initial repo landing."

**This claim is FALSE.** The mechanism of the false claim:

1. `git log --all --follow --format="%H %ai %s" -- backend/tests/test_rms_adversarial_v1_roundtrip.py` returned empty in this fresh session's condensed repo history — the file's pre-rename identity was not preserved through the initial-commit squash (`3985be5` initial commit consolidated all prior state into a single tree without preserving pre-rename identity for this specific file).
2. Reading "empty git log" as "file never existed" is a category error: **git log against a condensed fresh-tree repo does not reflect the file's live-history existence — BUILD_JOURNAL is the authoritative live-forward evidence trail**, and BUILD_JOURNAL lines 672, 1018, 1123 attest the file existed and ran 23 cells at G0.5 (146/146), G3 (211/211), and G4 (271/271).
3. The D-11 canon-before-ruling failure was **not consulting BUILD_JOURNAL** before generating a forensic verdict about a Makefile target's history. BUILD_JOURNAL is the canonical live-history record; git-log-follow against a squashed initial commit is a summary-side view that lost pre-rename identity.

## §3 · Scope of correction

**The false claim was scoped to STEP 2 surfacing text.** It appears in three loci within `docs/handoff/step_2_make_ci_attest_2026_07_24.md`:

| Locus | Claim (false) | Corrected verdict |
|---|---|---|
| §2.3 · Makefile provenance | "*stale since initial commit*" · "*present since initial repo landing*" | Went stale at MC-E5 rename event 2026-07-14; the file **did** exist under `tests/test_rms_adversarial_v1_roundtrip.py` from G0.5 through the MC-E5 rename; existed today as `backend/tests/test_instance_fixture_a_roundtrip.py`; Makefile line 60 was not updated at rename. |
| §4 · Posture (β) framing | *"the `make ci` target is a **stale reference to a non-existent test file** since initial Makefile landing 2026-07-02 (verified via `git blame`)"* | Stale reference **since MC-E5 rename event 2026-07-14**, not since initial landing. The 23 fixture-conformance cells DO exist today under the renamed filename. |
| Terminal reply table row · `make ci` verdict | *"Makefile line 59-60 stale since initial landing 2026-07-02 02:38:29 UTC per `git blame`"* | Stale **since MC-E5 rename event 2026-07-14** per BUILD_JOURNAL evidence; the `git blame` line at Makefile:59-60 shows the target has BEEN in the file since initial commit (that part is factually accurate), but "stale" from initial commit is FALSE — it was live and running 23 cells from G0.5 through MC-E5. |

**Does NOT propagate into any other on-disk artifact.** The false forensic claim did not enter:
- `docs/audits/lt2_sequencing_harness_provenance_d7_2026_07_24.md` (LT-2 D7 finding · independent scope · disposition unaffected)
- `docs/audits/product_doc_v3_1_untraceable_d7_2026_07_24.md` (Product Doc v3.1 D7 finding · independent scope · disposition unaffected)
- `docs/rulings/owner_configuration_2026-07-24.md` (Owner-authored ruling · verbatim carrier · not builder-modifiable)
- `/app/memory/dispatch_2026_07_24_recovery.md` (recovery memo · references authority artifacts only, no forensic claim about Makefile)
- `docs/registers/phase_ledger_v1.md` (Landings 1-3 scope only · no Makefile claim)
- `docs/rulings/owner_step2_surfaces_ruling_2026-07-24.md` (Owner-authored correction · this ruling itself carries the correction verbatim)

**Corrective actions taken this atomic:**

1. This forensic-correction audit filed at `docs/audits/lt2_forensic_correction_2026_07_24.md` (canonical correction record).
2. STEP 2 attest at `docs/handoff/step_2_make_ci_attest_2026_07_24.md` is **preserved byte-identical** — the false claim is annotated by reference to this correction audit rather than by in-place edit. Rationale: (a) preserves the evidence chain of what was surfaced in the HALT-declared atomic; (b) records the D-class dispatch-discipline failure at the exact surface where it occurred; (c) Owner ruling explicitly framed the correction as a companion finding, not an in-place amendment.
3. Ledger L-2 row annotates the correction: `docs/registers/phase_ledger_v1.md` §7 L-2 references this audit's SHA.

## §4 · D-class dispatch-discipline defect verdict

**Class:** D-11 · Canon-before-ruling / LLM-memory recall failure.
**Origin:** orchestrator-boundary (verbatim relay of forensic claim without on-disk verification against BUILD_JOURNAL).
**Load-bearing lesson:**

- **`git log --all --follow`** against a condensed fresh-tree repo is a SUMMARY-side view. It does not reflect pre-rename identity when the initial commit squashed prior history. Reading empty `git log` output as "file never existed" is a false negative.
- **`BUILD_JOURNAL.md`** is the authoritative live-forward evidence trail for phase-close attestations. **BUILD_JOURNAL is canon** for forensic claims about historical test-count attestations, target counts, and rename events.
- **D-11 canon-before-ruling** requires consulting BUILD_JOURNAL BEFORE emitting any forensic claim about phase history, target composition, or file lineage. Any HALT surface that contains an unverified forensic claim is itself a D-class defect (Owner-verbatim: *"A false forensic claim inside a HALT surface is itself a D-class defect."*).

**Standing rule crystallized this atomic:** for any future forensic claim about phase history, target composition, test-count attestations, or file lineage, the canon read-order is:

1. `BUILD_JOURNAL.md` (live-forward attestation record)
2. `docs/close_reports/**` (per-phase close attestations)
3. `docs/audits/**` (existing conformance / provenance audits)
4. **Only then** `git log` / `git blame` (which are summary-side views subject to squash-loss)

## §5 · D-1..D-11 self-audit table (standing practice · D-11 specifically marked as the failure lane)

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Correction traces to Owner-verbatim ruling §Surface 1 quoted at §1. BUILD_JOURNAL evidence at §2.1-§2.4 traces to live `grep -nE …` commands this session. |
| D-2 | NL-only claim | PASS | Every BUILD_JOURNAL line-number cited is disk-verifiable (`grep -nE … BUILD_JOURNAL.md`). |
| D-3 | Curated verdict | PASS | Full unabridged BUILD_JOURNAL evidence quoted (G0.5 line 672, G3 line 1018, G4 line 1123). Rename evidence via `ls -la` and `git log --all --follow` on `test_instance_fixture_a_roundtrip.py`. |
| D-4 | Rung inflation | PASS | No rung claims made in this correction audit. |
| D-5 | Cross-phase content leakage | PASS | Correction scoped strictly to LT-2 forensic false-claim; does not touch Surface 2 LT-2 disposition (which stands per Owner (a) ruling), does not touch Surface 3 Product Doc v3.1 D7 (which stands per Owner "accepted and closed"). |
| D-6 | Silent scope drift | PASS | Explicit propagation-scope enumeration at §3 above: 3 loci in STEP 2 attest carry the false claim; 6 other on-disk artifacts do NOT propagate it; STEP 2 attest preserved byte-identical per §3 corrective-action rationale. |
| D-7 | Invented scope | PASS | Zero invented scope. Correction body carries only Owner-verbatim §1 text + BUILD_JOURNAL live-quoted evidence + on-disk `ls`/`git log` output. |
| D-8 | Silent drift | PASS | Standing Rule v3 attest: `backend/contracts/**`, snapshots, product code, frontend all byte-identical this atomic. Parity 31 held. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked. |
| D-10 | Menu emission | PASS | No permission-menu emitted. This correction is executed under Owner-mandated Step C directive; not a builder Tier-3 election. |
| **D-11** | **Canon-before-ruling / LLM-memory recall** | **FAIL · specific failure lane · this correction anchors the defect** | The prior STEP 2 attest emitted a forensic claim ("stale since initial commit") that would have been refuted by BUILD_JOURNAL read (lines 672, 1018, 1123 all attest the file existed and ran 23 cells at G0.5, G3, G4). The failure lane: consulting `git log --all --follow` on a condensed fresh-tree repo instead of BUILD_JOURNAL. **Load-bearing lesson crystallized as standing rule at §4**: BUILD_JOURNAL is canon for forensic claims; git-log is summary-side and subject to squash-loss. Correction filed here anchors the defect at the specific attest where it occurred; corrective standing-rule at §4 prevents recurrence at future forensic surfaces. |

---

*LT-2 forensic correction · 2026-07-24 · Standing Rule v3 · D-11 canon-before-ruling failure specifically marked and lesson crystallized · Owner-verbatim §Surface 1 correction carried byte-for-byte at §1 · BUILD_JOURNAL evidence lines 672, 1018, 1123 verified live · scope propagation enumerated (3 loci carry the false claim · 6 other on-disk artifacts do not) · STEP 2 attest preserved byte-identical per corrective-action rationale · Parity 31 held byte-identical this atomic.*
