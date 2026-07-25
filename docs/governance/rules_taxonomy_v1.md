# Rules Taxonomy v1 (Owner-authored 2026-07-25)

**Class:** New governance specification · four-class Rule Record model.
**Sanction:** `docs/rulings/owner_change_order_2026-07-25.md` · SHA `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568` (Owner-authored 2026-07-25 · FINAL · non-re-openable · not builder-modifiable).
**Predecessor:** new file · governance canon · no predecessor.
**Interpretation rule:** amendment wins where in conflict; pre-amendment canon stands where amendment is silent.

---

## A3 · Rules Taxonomy (new governance specification · files under `docs/governance/rules_taxonomy_v1.md`)

### A3.1 Four classes, one shape
All governance objects share one **Rule Record** schema (`class` field: S/O/E/D) and appear in the DPO Estate with enforcement counts. Lifecycle differs per class along **change authority × change velocity × verification method**:

| Class | Name (UI) | Develop | Deploy | Operate | Verify |
|---|---|---|---|---|---|
| **S** | **Rails** | Authored as code + contract; promise-registered | Build phase only: Parity seal, AST cells, CI green; never runtime-editable | Not operable — observable only (Estate, read-only, enforcement counts) | The test suite; a rail without a hard-fail cell does not exist |
| **O** | **Rules** | Defined in spec: type, bounds, recommended default | Set at Connect, locked at sign-off | Change-a-Rule only: propose → counter-sign → waiting period → applied → certificate → Verify-the-Rules fires | Live test packs, per rule, DPO-signable |
| **E** | **Engine settings** | Declared in engine spec **with success parameters** (in force with known conditions of success, or it is a spec gap — never tentative) | Pinned per engine version; changes ride version bumps with evaluation verdicts | Engineers, via versioned deployment; Estate shows per-engine per-version, read-only | Version-bump evaluation verdict (BM-class) |
| **D** | **Registries** | Schema defined once; a Class S or E rule references the registry **by version** | Initial load at Connect or first upload | §A3.3 lifecycle | Validation report + sample probe pack (live redaction confirmation on drawn entries) |

### A3.2 E→O promotion (the only path to runtime tunability)
Proposal-gated and one-way per event: engine owner files a promotion note (parameter · why runtime tunability · blast radius) → parameter enters Class O via spec amendment (type, bounds, recommended default) → leaves engine-pinned config at the **next engine version bump** → thereafter changes only via Change-a-Rule. Until promotion completes, no runtime edit exists. Demotion O→E requires the same ceremony. No third path; "it's just an engine setting" is not a route around Class O.

### A3.3 Class D lifecycle (governed reference data — e.g., the shield-against registry)
Upload (Excel/CSV) → schema validation (row-level errors, **fail-closed on malformed**) → **diff view: added / removed / changed** → confirm → versioned, receipted, effective-from stamped, rollback available. Every run records the registry **version in force** (audit answers "was this term protected on date X"). **Asymmetry (Owner-ruled): additions take effect immediately; removals AND edits require approval** (counter-sign or configured waiting window) — the only edits that can weaken protection are the ones that gate.

### A3.4 Classification of existing objects (initial register)
Rails (S): masking-before-AI-call · fault-never-refusal · single-ingress · fail-closed license default · five_rings zero-mutation · admissibility evaluator machinery (A2.2). Rules (O): the six Connect rules · both waiting periods · the A2.3 ceiling · admissibility thresholds. Engine settings (E): dedupe fingerprint distance · VAD threshold · batch windows · sample-rate/window constants · EAB-3 §5.5 defaults (partition-shape enum · refresh cadence · eviction policy · latency-telemetry storage · AC-A5.b latency budget). Registries (D): shield-against/pseudonymization registry · protected-terms lists · DPO extraction filter lists.

---

*A3 new governance specification · Rules Taxonomy v1 · Owner-authored 2026-07-25 · Owner-verbatim carrier · sanctioned by `docs/rulings/owner_change_order_2026-07-25.md` · Standing Rule v3 held.*
