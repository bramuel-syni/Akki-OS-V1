# Open Governance Decisions

Consolidated register of governance-owed items that this build waits on
BEFORE the affected phase can complete. Nothing here is agent-actionable
— every entry blocks on an external owner (project owner, MEA, DPO).

**Rule** (operating posture norm #9): *"a run may carry execution
forward autonomously, but never a governance decision — if you reach a
threshold/retention/rights point, stop and surface that, even mid-phase."*

## 1. Northena Ledger retention

- **Owner**: DPO.
- **Question**: retention duration + end-of-window deletion/immutability
  logic.
- **Impl state**: `retention_mode()` reads env
  `RMS_NORTHENA_LEDGER_RETENTION_MODE` (default: `indefinite`).
  Ring buffer G1 stamp_audit → Northena ledger absorption path live.
- **Blocks**: production deployment of Northena ledger. Does NOT block
  G3+ dev work.
- **Journal ref**: Northena Mandate §11; consolidated spec §7 Pending
  Decisions; BUILD_JOURNAL 2026-07-01T07:10Z.

## 2. Targeta yield-layer thresholds (G4)

- **Owner**: Project owner.
- **Questions** (spec §4 proposals in brackets, DO NOT act on them):
  - `min_efficiency_gain` — Arm 1 admission gate (proposed ≥ 0.15).
  - `coverage_alpha` — Arm 2 admission veto (proposed 0.90).
  - **Held-out set composition** — representative set used for gate
    evaluation.
- **Blocks**: yield-layer admission at G4. Core still ships.
- **Journal ref**: Targeta spec §4 + §7; `docs/g4_prep/targeta_prep.md`.

## 3. Mtafiti V3 admission thresholds (G4)

- **Owner**: Project owner.
- **Questions** (via `v3_result.thresholds.*`):
  - `fact_precision` — fact-class precision floor.
  - `genre_accuracy` — genre-classification accuracy floor.
  - `inter_annotator_floor` — kappa floor (must be met before accuracy
    is computed).
- **Prerequisite**: real labelled slice must exist (V3 also parks on
  real material — same wait state as G2b's convergence quality).
- **Blocks**: inference overlay admission at G4. Objective-blind census
  + declaration baseline ship without waiting.
- **Journal ref**: Mtafiti spec §12; `docs/g4_prep/mtafiti_prep.md`.

## 4. Mtafiti feed source-standing declaration table

- **Owner**: MEA.
- **Question**: content of the per-feed declaration table (not the
  mechanism — mechanism ships).
- **Blocks**: population of declaration baseline at deploy. Mechanism
  is buildable without.
- **Journal ref**: Mtafiti spec §9.

## Non-governance parks (for cross-reference — not blocking on governance)

- **G2b Convergence Quality on Real Hour** — waits on real RMS material
  delivery from stakeholder side. Not a governance decision.
- **Solva (G3 target)** — **NO governance items pending** per Solva spec
  §18 (confirmed 2026-07-01). Reasoning method is a build-time choice
  bounded by the 12 invariants. Distinct from Targeta / Mtafiti / Northena.
  See `/app/docs/g3_prep/solva_prep.md`.
- **Tasks 2 & 3 (transitive-lift calibration audit + `grounding_contract`
  re-lift)** — CLOSED permanent, per settled-substrate directive (norm
  #8). Not pending.
- **`/api/discipline/lift_manifest`** — G5 backlog. Not pending.

## Discipline

- Any G4 dispatch will resolve items 2 + 3 + 4 OR park on the specific
  governance surface. No dispatch proceeds through a governance point
  it hasn't resolved.
- Item 1 (Northena retention) is pre-existing; documented for the G2a
  audit; does not block G3+.
- No agent may propose values on any threshold in this file. Values
  above (0.15 / 0.90 / etc.) are spec PROPOSALS from the stakeholder,
  not agent-provisioned.
