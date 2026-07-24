# STEP 2 · `make ci` Step-Zero Attest · 2026-07-24

**Class:** Full-sweep attest per Owner Configuration Dispatch 2026-07-24 §4.STEP-2 (verbatim: *"STEP 2 — make ci step zero against current main. Full sweep attested (pytest/Jest/Playwright counts stated). Any red halts the sequence."*).
**Authority artifact:** `docs/rulings/owner_configuration_2026-07-24.md` · SHA `ec95a0acec13d81b2fd5f1b1da04c83d2991f3876c795c8266a96eaef1230f52`.
**Standing Rule v3:** all product code / contracts / snapshots byte-identical this atomic; **Parity 31 held**.
**Estimation-discipline attest:** no duration/credit figure emitted (per Owner §3 · bands generated only from STEP 3 reconciliation).

---

## §0 · Sequence verdict

**RED · HALT DECLARED.**

`make ci` step-zero **FAILS** with make exit code 2 at Makefile target `rms_adversarial_v1` (line 60). The referenced test file `tests/test_rms_adversarial_v1_roundtrip.py` **does not exist on-disk and has never been committed** under this path (verified via `find`, `ls`, `git log`).

Per Owner §4.STEP-2 verbatim: *"Any red halts the sequence."* — D-9 auto-proceed to STEP 3 is **NOT invoked**. Await Owner ruling.

Concurrent evidence recorded below: the full-sweep pytest, Jest, and Playwright counts are all GREEN. The red is confined to the Makefile-configuration surface (target references a file that was never committed since the Makefile's first landing 2026-07-02 02:38:29 UTC).

---

## §1 · `make ci` execution attest

**Command:** `cd /app && make ci`
**Elapsed:** 44.750s real / 51.548s user / 2.544s sys
**Exit code:** 2 (make error)
**Final target that failed:** `rms_adversarial_v1` (Makefile line 59-60)
**Failure text (verbatim):**

```
ERROR: file or directory not found: tests/test_rms_adversarial_v1_roundtrip.py

make: *** [Makefile:60: rms_adversarial_v1] Error 4
```

**Prior targets in the `ci` chain (executed to completion before `rms_adversarial_v1` failed):**

Per Makefile line 68: `ci: invariants chokepoint smoke layer_a layer_b layer_c v1 perception extraction_params northena g1_stamper lift_manifest rms_adversarial_v1`

| Target | Cell count | Verdict |
|---|---:|---|
| `invariants` | ≥ 31 snapshot cells + AST cells | GREEN (executed before red) |
| `chokepoint` | 1 file (`test_no_direct_llm_calls_outside_shield.py`) | GREEN |
| `smoke` | 2 files (`test_smoke.py` + `test_synthetic_fixture_roundtrip.py`) | GREEN |
| `layer_a` · `layer_b` · `layer_c` | 3 files | GREEN |
| `v1` | 1 file (`test_v1_harness.py`) | GREEN |
| `perception` | 1 file (`test_perception_router.py`) | GREEN |
| `extraction_params` | 1 file (`test_extraction_params_v0.py`) | GREEN |
| `northena` | 1 file (`test_northena_invariants.py`) | GREEN |
| `g1_stamper` | 1 file (`test_g1_stamper_and_v3.py`) · 11 passed in 0.41s | GREEN |
| `lift_manifest` | 1 file (`test_lift_manifest.py`) · 112 passed in 0.04s | GREEN |
| **`rms_adversarial_v1`** | **file does not exist** | **RED · make exit 2** |

## §2 · Root-cause investigation (D-11 canon-before-attest · live-verified 2026-07-24)

### §2.1 · File existence check

```bash
$ ls -la backend/tests/test_rms_adversarial* 2>&1
ls: cannot access 'backend/tests/test_rms_adversarial*': No such file or directory

$ find backend/tests -name "*rms_adversarial*" -o -name "*adversarial*" 2>/dev/null
(empty)
```

**File does not exist. Never has.**

### §2.2 · Git history check

```bash
$ git log --all --follow --format="%H %ai %s" -- backend/tests/test_rms_adversarial_v1_roundtrip.py 2>&1 | head -10
(empty — no commits reference this path)
```

**File has never been committed under this path.**

### §2.3 · Makefile provenance

```bash
$ git blame -L 59,60 Makefile
^3985be5 (emergent-agent-e1 2026-07-02 02:38:29 +0000 59) rms_adversarial_v1:
^3985be5 (emergent-agent-e1 2026-07-02 02:38:29 +0000 60) 	cd backend && $(PYTEST) -q tests/test_rms_adversarial_v1_roundtrip.py
```

The `rms_adversarial_v1` target has been in the Makefile since **the very first Makefile commit** (`^3985be5` · 2026-07-02 02:38:29 UTC) — this is a **pre-existing Makefile-vs-repo drift**, present since initial repo landing. **NOT a regression introduced by any recent atomic.** No product-code change is implicated.

### §2.4 · Related adversarial tests on-disk (informational)

```bash
$ find backend/tests -type f -name "*.py" | xargs grep -lE "adversarial|rms_adversarial_v1" 2>/dev/null
backend/tests/test_instance_fixture_a_roundtrip.py
backend/tests/test_synthetic_fixture_roundtrip.py
backend/tests/invariants/test_fixture_refresh_fr_g1_to_g7.py
backend/tests/invariants/test_feasibility_honesty_under_absence.py
backend/tests/test_g1_stamper_and_v3.py
```

Adversarial semantics are covered by other on-disk test files (fixture-refresh v1 harness · G1 stamper adversarial cells · feasibility-honesty-under-absence). The `test_rms_adversarial_v1_roundtrip.py` target in the Makefile appears to have been intended for a specific file that was never created (or was renamed/moved without updating the Makefile).

---

## §3 · Full-sweep attest (per Owner §4.STEP-2 verbatim: *"Full sweep attested (pytest/Jest/Playwright counts stated)"*)

### §3.1 · Pytest full sweep

**Command:** `cd /app/backend && python -m pytest tests/ -q --no-header`
**Elapsed:** 41.599s real / 49.809s user / 2.112s sys
**Exit code:** 0
**Result:** **1 296 passed · 1 skipped · 1 warning** (unchanged from EAB-1 baseline post-close 2026-07-15)

**Warning surface:** 1 warning — FastAPI OpenAPI duplicate operation ID `download_bundle_api_docs_bundle__filename__head` for function `download_bundle` at `backend/routers/docs_bundle.py`. Pre-existing since docs-bundle router landing; non-blocking; **not a red.**

### §3.2 · Jest (frontend `src/__tests__`)

**Command:** `cd /app/frontend && yarn test --watchAll=false --passWithNoTests`
**Elapsed:** 5.298s real / 16.164s user / 1.834s sys (jest reported 4.413s runtime)
**Result:** **Test Suites: 24 passed · 24 total · Tests: 154 passed · 154 total · Snapshots: 0 total** · Done in 5.15s

### §3.3 · Playwright chromium project

**Command:** `cd /app/frontend && PLAYWRIGHT_BASE_URL=http://localhost:3000 npx playwright test --project=chromium`
**Elapsed:** 15.978s real / 6.254s user / 2.095s sys (playwright reported 15.3s runtime)
**Result:** **57 passed** (100%)

**Environment setup this atomic (DIAGNOSTIC ACTION · surfaced for record):** the Chromium headless-shell binary at `/pw-browsers/chromium_headless_shell-1228/chrome-linux/headless_shell` was **absent from the environment** on first invocation (57/57 test-level failures with error `browserType.launch: Executable doesn't exist at …`). Ran `npx playwright install chromium` (download-only · no test-file touch · no product-code touch) to install Chrome for Testing v149.0.7827.55 (~187.2 MiB) + Chrome Headless Shell v149.0.7827.55 (~110 MiB) to `/pw-browsers/chromium-1228/` and `/pw-browsers/chromium_headless_shell-1228/`. Subsequent invocation returned 57/57 GREEN.

This install action is **environment provisioning, not code change** — no on-disk file under `/app/**` was modified by the install. Handoff summary noted "Playwright Chromium headless shell installed" — this environment did not carry that state, likely due to session-fresh container provisioning. Recorded for transparency; no D7 vector implied.

### §3.4 · Full-sweep totals (across all three frameworks · post-environment-setup)

| Framework | Command | Elapsed | Count | Verdict |
|---|---|---|---|---|
| Pytest | `pytest tests/ -q` | 41.599s | 1 296 passed · 1 skipped · 1 warning | **GREEN** |
| Jest | `yarn test --watchAll=false` | 5.298s | 24 suites · 154 tests passed | **GREEN** |
| Playwright chromium | `npx playwright test --project=chromium` | 15.978s | 57 passed | **GREEN** |
| **Total test cells across three frameworks** | — | ~62.9s | **1 507 test cells passed · 1 skipped** | **GREEN** |

**All three frameworks GREEN.**

---

## §4 · HALT surface (Owner ruling required)

Two structurally distinct verdict-postures on the `make ci` red:

**Posture (α) · Makefile-authoritative red:** `make ci` fails → sequence halts per Owner §4.STEP-2 verbatim rule. The pre-existing Makefile-vs-repo drift is a governance-tier defect that must be Owner-ruled before D-9 auto-proceed to STEP 3. STEP 1 was scoped strictly as "*standalone status reply · no code rides*"; the builder cannot repair the Makefile under STEP 2 without an Owner-sanctioned code-touching dispatch. Under this posture, **HALT confirmed** — await Owner ruling on Makefile disposition.

**Posture (β) · Underlying-code-authoritative:** the `make ci` target is a **stale reference to a non-existent test file** since initial Makefile landing 2026-07-02 (verified via `git blame`); the underlying full-sweep pytest suite passes 1 296/1 296 (including all cells that `make ci` also runs, when they exist); Jest and Playwright pass. The red is confined to a Makefile-configuration artifact and does not reflect functional-code failure. Under this posture, the sequence could D-9 auto-proceed to STEP 3 with the Makefile red logged as an open governance-tier finding for later repair — **but this posture is not builder Tier-3 to invoke**; it requires Owner ruling to override the §4.STEP-2 "any red halts" plain-text.

**Builder action:** posture (α) invoked by default. **Sequence HALTED at STEP 2.** Owner ruling required to (a) confirm HALT and dispatch a Makefile-repair atomic before resuming, OR (b) explicitly rule the Makefile-configuration red as a non-blocking finding under posture (β) and dispatch D-9 auto-proceed to STEP 3.

**Owner ruling options enumerated (per §5.1-precedent enumeration pattern · pre-named per §4.STEP-2 red-halt rule · NOT a builder menu):**

- **(a)** Confirm posture (α) HALT · dispatch a scoped Makefile-repair atomic (single-line edit at Makefile:59-60 to either delete the `rms_adversarial_v1` target from the `ci: …` chain, or replace with an existing test file reference, or create the missing test file) · re-run `make ci` step zero · resume D-9 auto-proceed to STEP 3.
- **(b)** Explicitly rule the Makefile-configuration red as a non-blocking pre-existing D-class governance finding · file the D-class finding at `docs/audits/make_ci_stale_target_rms_adversarial_v1_2026_07_24.md` · treat full-sweep GREEN (§3.4 above) as the authoritative STEP 2 attest · D-9 auto-proceed to STEP 3.
- **(c)** Other Owner ruling.

---

## §5 · Standing Rule v3 attest (this atomic scope)

- **`backend/contracts/**`** — zero touch · **Parity 31 held byte-identical.**
- **`backend/tests/invariants/*.contract_snapshot.json`** — zero touch.
- **`backend/**` production code** — zero touch.
- **`frontend/**`** (excluding node_modules generated cache) — zero touch.
- **`docs/**`** — zero touch (this attest is a net-new file at `docs/handoff/step_2_make_ci_attest_2026_07_24.md`).
- **`Makefile`** — zero touch (red surfaced only; repair deferred to Owner ruling per §4 above).

`git diff --stat HEAD backend/contracts/` = empty · `git diff --stat HEAD backend/tests/invariants/*.contract_snapshot.json` = empty · **Parity 31/31 held**.

Environment-provisioning action (`npx playwright install chromium`) modified `/pw-browsers/` outside `/app` scope — no source-tree touch.

---

## §6 · D-1..D-11 self-audit table (standing practice)

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every claim traces to a live command this session (`make ci`, `pytest -q`, `yarn test`, `npx playwright test`, `find`, `ls`, `git log`, `git blame`). |
| D-2 | NL-only claim | PASS | All counts, elapsed times, exit codes, SHAs, and command outputs recorded verbatim from live shell invocations. Zero unlabeled claims. |
| D-3 | Curated verdict | PASS | Full unabridged failure text carried verbatim (§1); root-cause investigation exhaustive (§2.1-§2.4); no cherry-picking of green targets to bury the red. |
| D-4 | Rung inflation | PASS | Status attest carries no rung claims. |
| D-5 | Cross-phase content leakage | PASS | Scope strictly `make ci` + full-sweep + red surface. Zero STEP 3..6 content emitted. Zero contract touch. Zero product-code touch. |
| D-6 | Silent scope drift | PASS | Environment-provisioning action (`npx playwright install chromium`) disclosed at §3.3 with full transparency (~297 MiB download to `/pw-browsers/`; no `/app/` source-tree touch). |
| D-7 | Invented scope | PASS | No fabricated scope. Both HALT postures (α, β) explicitly named as Owner-ruling surfaces, not builder-decided. |
| D-8 | Silent drift | PASS | Standing Rule v3 attest carried (§5). Parity 31 held. Makefile line 59-60 NOT touched (red surfaced only; repair deferred). |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked. Native `pytest`, `yarn test`, `npx playwright test` only. |
| D-10 | Menu emission | PASS | §4 Owner ruling options (a/b/c) enumerated per §5.1-precedent pattern; **this is a red-triggered escalation surface, not a builder permission menu**. Enumeration required by §4.STEP-2 "any red halts" plain-text; ruling authority is Owner, disposition is not builder Tier-3. |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Every citation live-verified this session: Makefile via `git blame`, file existence via `find`/`ls`, git history via `git log --all --follow`, test cell counts via live `pytest`/`yarn`/`npx` invocation. Zero memory-recall presented as fact. Prior handoff-summary claim ("Playwright Chromium headless shell installed") explicitly noted as environment-state-drift discovered live, not accepted on faith. |

---

## §7 · Next-step readiness

**HALTED at STEP 2.** No D-9 auto-proceed to STEP 3 until Owner rules the Makefile red per §4.

**On unlock (any of §4 (a)/(b)/(c) rulings):**

- If (a): builder awaits scoped Makefile-repair dispatch · re-runs `make ci` · re-attests · D-9 to STEP 3.
- If (b): builder files the D-class finding + auto-proceeds under D-9 to STEP 3 · Substrate-Drop v3 landing atomic per Owner §4.STEP-3 (8 artifact fetches · `.md`-canonical filing under `docs/mandates/module_specs/` · MANIFEST + `phase_source_requirements.yaml` extension · reconciliation audit with CODE_IMPACT + CONFLICT + OD-8/9/10 rows · §0-CAL amendment landed as governance sibling · close report + register sibling).
- If (c): builder awaits explicit Owner instruction.

**Lane 1 (9.2b GPU extraction)** — no builder motion. Gated on OD-4 · 9.2-OWN-2 · PH-R2/R4, all Owner-side.

---

*STEP 2 attest · 2026-07-24 · Standing Rule v3 · D-11 canon-before-ruling · D-10 self-audit table attached · verbatim carrier applied to all Owner-quoted rules · Owner ruling SHA `ec95a0acec13d81b…` carried at top · Parity 31 held byte-identical · RED SURFACED · HALT DECLARED · Owner ruling required per §4.*
