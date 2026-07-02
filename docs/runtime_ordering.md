# Build order vs. runtime order — G3 / G4 distinction

G0 brief Hard Rule 3: **build-order ≠ runtime-order**.

## Build order (the order gates close)
1. **G3** — Layer-D objective-shaped orchestrator + Service 2 v0 (Day-to-Day).
2. **G4** — Mtafiti registry + Targeta planner + Service 1 v1 (Day Zero composed).

## Runtime order (the order production calls flow)
1. **Service 1 (Day Zero)** runs first — Mtafiti walks the estate, Targeta plans, Akki Layers A→B→C produce the Normalized Tier.
2. **Service 2 (Day-to-Day)** reads the Normalized Tier and composes answers via Layer D.

## Implication for G3
At G3, **Service 2 reads the Normalized Tier directly** and does **not** call Mtafiti or Targeta — they don't exist yet. G3 is tested in this order:

1. Against the **synthetic plumbing fixture**'s pre-populated Normalized Tier (`services/data_source/synthetic.py`). Plumbing-only — not a validity check.
2. Against the **G2 V1-processed units** once the V1 spike runs an Akki engine A→B→C pass on a real RMS broadcast hour. This is the first real Layer-D run.
3. At **G4**, once Mtafiti is wired, Service 2 swaps to reading the production Registry. The G3 interface to the Normalized Tier does not change — Mtafiti is upstream of the Tier, not part of Layer D's read path.

This ordering is deliberate. Building G3 before G4 lets us de-risk Layer-D composition without entangling it with Registry construction. The synthetic fixture exists *for* this ordering.

## Implication for V3 (per Hard Rule 4)
At G1, V3 validates defensibility detection against **stubbed source-standing inputs** because Mtafiti's Registry is not yet built. At G4, V3 **must be re-run** against the **real source-standing values** the Registry surfaces. The G1 V3 harness will therefore be written to be **reusable** (parameterised on source-standing input), **not throwaway**.

## Implication for V1 (per Hard Rule 1)
When real RMS material arrives (multiple hours), the **G0.5 spike hour** and the **G2 V1 production hour** are deliberately distinct. The V1 measurement harness accepts both as parameters from the start; same metrics, same thresholds, different content.

## Plain-English rule
If you find yourself wiring G3 to call Mtafiti, stop — you are pulling G4 forward. If you find yourself wiring V3 to bake in stub source-standings as final, stop — you are foreclosing the G4 V3 re-run.
