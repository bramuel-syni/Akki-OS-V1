# D7 Finding · LT-2 · Sequencing Harness Stage A Provenance · 2026-07-24

**Finding class:** D7 · Invented scope (per Registry Doctrine v1.0 Part IV D-7).
**Trigger:** Owner Configuration Dispatch 2026-07-24 · §1.4 verbatim: *"LT-2 — STILL OWED. sequencing_harness_stage_a.md provenance: when created, by what instruction. Execution-scheduling inside sequence-G-13 does not discharge the provenance demand. If unsanctioned pre-work: D7 finding, file held, not deleted."*
**Authority artifact:** `docs/rulings/owner_configuration_2026-07-24.md` · SHA `ec95a0acec13d81b2fd5f1b1da04c83d2991f3876c795c8266a96eaef1230f52`.
**Subject file:** `docs/stage_a_proposals/sequencing_harness_stage_a.md` · SHA `ae3b2b3056477fa359d34d3de2504239958e002fea280975e34b858fb1e32833` (post-annotation · body byte-identical to pre-annotation SHA `95f9274edad69d3abe7e505aeb1705c5e320638b0d0b6c81d2a9b2a6d81c850f`).
**Disposition:** **HELD · D7 finding pending Owner disposition.** File not deleted per Owner §1.4.

---

## §1 · Investigation evidence (D-11 canon-before-attest · live-verified 2026-07-24)

### §1.1 · Git creation record

`git log --all --follow --format="%H %ai %s" -- docs/stage_a_proposals/sequencing_harness_stage_a.md` (this session):

| Commit | Timestamp (UTC) | Author | Message |
|---|---|---|---|
| `64820699914d865b9d023aa652731efe105c0666` | **2026-07-14 06:26:57** | `emergent-agent-e1` | `auto-commit for c604d86a-357d-4308-925b-9447bc0485e7` — **file first created** (body landed at this commit) |
| `94bbda41be7ebb035b0acd1f222feebede69b8d1` | 2026-07-14 10:10:52 | `emergent-agent-e1` | `auto-commit for f3f53b02-22e4-4d80-8ee9-ec2b12112238` — line 1 self-flagging annotation added retroactively 4h 44m after creation |

`git blame -L 1,3 docs/stage_a_proposals/sequencing_harness_stage_a.md` (this session):

```
94bbda41 (emergent-agent-e1 2026-07-14 10:10:52 +0000 1) UNSANCTIONED PRE-WORK · D7 finding 2026-07-14 · no ruling status · consumable only as raw material under a future Owner-dispatched §8.1.b Stage A.
64820699 (emergent-agent-e1 2026-07-14 06:26:57 +0000 2) # Stage A · Sequencing Harness (Registry Doctrine §8.1.b · §5.2)
64820699 (emergent-agent-e1 2026-07-14 06:26:57 +0000 3)
```

### §1.2 · Internal-body claim vs. git evidence

The Stage A body **claims** at line 4: *"Dispatched: 2026-07-11 (post-§8.1.a Standing Queries close · orchestrator-sequenced within sanctioned surface per Owner process correction)."*

**Git evidence contradicts this claim:** the file did not exist on-disk on 2026-07-11. It was first committed 2026-07-14 06:26:57 UTC — **3 days after** the claimed dispatch date. The body's "2026-07-11 dispatched" claim is retroactive self-attribution without on-disk canon backing.

### §1.3 · Self-flagging annotation history

Four hours 44 minutes after the file's first commit, the same builder identity (`emergent-agent-e1`) added the line-1 annotation:

> "UNSANCTIONED PRE-WORK · D7 finding 2026-07-14 · no ruling status · consumable only as raw material under a future Owner-dispatched §8.1.b Stage A."

This is a **prior builder self-flagging** — the file was recognized as unsanctioned pre-work by the agent that created it. This D7 finding (2026-07-24) merely ratifies the prior self-flagging under formal Owner-dispatch authority.

### §1.4 · On-disk grep for sanctioning ruling

`grep -rniE "sequencing.harness|sequencing_harness" docs/rulings/` (this session):

| Match | Content | Sanctioning verdict |
|---|---|---|
| `docs/rulings/owner_configuration_2026-07-24.md:7` | The Owner dispatch DEMANDING LT-2 provenance (not sanctioning creation) | **NOT sanctioning** |
| `docs/rulings/machine_readable_registry_mrr_e1_to_e4.md:26` | "*acknowledged-future-path note (NOT a governance addendum · NOT a standing rule)*" — future path only | **NOT sanctioning** |
| `docs/rulings/standing_queries_sq_e1.md:72` | "*D7 binds: no sequencing harness · no worker context-harnessing · no Registry content changes to v0.md or v0.1_supplement · no Q2-05 reads · no next-cell scaffolds beyond queries scope.*" | **EXPLICITLY D7-FENCED** — the sequencing harness was named as OUT-OF-SCOPE in the standing queries close on 2026-07-11 |

`grep -rlE "sequencing.harness|sequencing_harness" docs/stage_a_proposals/` (this session): the file itself + `eab_2_stage_a.md` cross-referencing the file at §7 fence attest (no sanctioning).

**Zero sanctioning ruling exists in on-disk canon.** The standing queries close report at §12 explicitly fenced sequencing-harness work as D7-bound on 2026-07-11 — three days before this file was created.

### §1.5 · Phase ledger classification

`docs/registers/phase_ledger_v1.md` §2 row 1 classes the file as `open` (Stage A landed · no matching close report · Registry Doctrine §5.2 harness spec landed, execution phase pending). This is an **accounting classification only** — it records the file's on-disk existence, it does **NOT** constitute a sanctioning ruling. The phase-ledger row was authored to reflect the on-disk state, not to authorize the file's creation retroactively.

---

## §2 · D7 verdict

**D7-BOUND · UNSANCTIONED PRE-WORK.**

- **Creation:** 2026-07-14 06:26:57 UTC by `emergent-agent-e1` (git commit `64820699…`).
- **Sanctioning ruling:** **NONE.** Zero Owner dispatch on-disk authorizes creation of `sequencing_harness_stage_a.md`.
- **Explicit D7 fence at creation time:** `docs/rulings/standing_queries_sq_e1.md:72` (2026-07-11) explicitly fenced the sequencing harness as D7-bound three days before the file was created.
- **Self-flagged by prior builder:** line-1 annotation on 2026-07-14 10:10:52 UTC acknowledged the unsanctioned status.
- **File body internal claim** ("Dispatched: 2026-07-11") **is contradicted by git evidence** — the file did not exist on 2026-07-11.

## §3 · Disposition per Owner §1.4 (verbatim)

> "If unsanctioned pre-work: D7 finding, file held, not deleted."

**Action taken this atomic:**

1. This D7 audit filed at `docs/audits/lt2_sequencing_harness_provenance_d7_2026_07_24.md`.
2. Subject file annotated at line 1 (annotation only · body byte-identical per Standing Rule v3): "HELD · D7 finding pending Owner disposition (2026-07-24 per LT-2 disposition · `docs/audits/lt2_sequencing_harness_provenance_d7_2026_07_24.md` · file body byte-identical · Standing Rule v3 · not deleted)."
3. Subject file NOT deleted.
4. Subject file body (lines 2..END) byte-identical to pre-annotation SHA — verified via `diff <(git show HEAD:… | sed -n '2,$p') <(sed -n '2,$p' …)` = empty.

## §4 · Downstream implications

- Phase ledger §2 row 1 (`sequencing_harness · open`) remains accounting-only. It does not constitute sanction and requires Owner disposition on whether to:
  (a) leave the row as-is (open · body held),
  (b) reclassify the row (e.g., HELD-D7 sub-state), or
  (c) close the row upon Owner-side action.
- Phase ledger §3 row 5 (`G-13 · Registry Doctrine §8.1 completion`) enumerates "sequencing harness (execution)" as one of the 5 of 8 remaining additive surfaces — this is future scope per Owner-ratified sequence position 5. The current subject file (Stage A body dated 2026-07-11 falsely) is **NOT** the same artifact as the G-13-scope execution phase; it is unsanctioned pre-work that predates any G-13 dispatch.
- No LoC / band / credit / duration figure derived from this file has evidentiary weight for any future Owner-sanctioned harness Stage A. The file is raw material only per its line-1 self-flag.

---

*D7 finding filed 2026-07-24 under Owner Configuration Dispatch (SHA `ec95a0acec13d81b…`). Verbatim carrier applied to Owner §1.4 demand text. Standing Rule v3: file held, not deleted; annotation-only change to subject file line 1.*
