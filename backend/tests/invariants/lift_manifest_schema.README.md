# Lift manifest schema — `lift_kind` documentation

Adjacent doc to `lift_manifest_schema.snapshot.json` (frozen). Does not
modify the schema — this file exists so the four `lift_kind` values
carry their intended semantics in a place a human can read.

Any future re-bless of the schema (e.g. adding a fifth `lift_kind`) must
update this doc in the same commit.

## The four `lift_kind` values

### `direct`
The module was reshaped directly from a cousin file whose path is cited
in `cousin_citation` and which currently exists at that path.
`resolves_by` identifiers MUST grep-resolve inside the cited cousin file.
This is the strongest claim — the lint verifies it against the real
substrate.

Current in-pod state: **0 entries.** The reference substrate at
`/reference/akki-legacy/` is not mounted in this build's container.
The `direct` branch of the lint is code-exercised (unit-testable) but
un-exercised by real data.

### `transitive`
The module was reshaped via one or more in-pod intermediate modules that
themselves carry the cousin's structural shape (typically G0/G0.5
reshapes whose docstrings document their cousin lift). `transitive_chain`
lists the intermediate `/app` paths; `resolves_by` identifiers MUST
grep-resolve somewhere in the combined chain source.

This is the strongest claim available given the settled substrate state.

### `unverifiable-substrate-absent`
The module cites a cousin path in `cousin_citation` but that path is not
reachable in this pod (`/reference/akki-legacy/` is not mounted).
`notes` MUST document the reason. If `transitive_chain` is non-empty,
the chain still grep-resolves for the identifiers in `resolves_by`.

**This is the EXPECTED steady state** for every lift that was originally
sourced from `/reference/akki-legacy/` — the cousin-restoration thread
was closed by stakeholder directive on 2026-07-01. Transitive-lift-
with-manifest is the standing practice; this value is not a temporary
condition awaiting resolution.

If the base image is ever rebuilt with the reference tree accessible,
that becomes a new discovery to journal — at which point these entries
can be retroactively converted to `direct` claims (an explicit re-bless
of the schema might introduce a `retroactive-verified` value at that
time; not now).

### `mandate-forced-net-new`
The module has no cousin substrate because the mandate or spec section
declares the shape net-new by construction (e.g. Northena §12 declares
the four-stage state machine net-new; RMS Spec §5 declares the modality-
native Layer A handlers). `cousin_citation` is `null`. `notes` MUST
cite the specific mandate/spec section (heuristic: contains "mandate",
"spec", or "§").

## Enforcement mechanisms

- **Condition 1** — the lint resolves the CLAIM, not the citation string.
  See `_check_direct` and `_check_transitive` in
  `/app/backend/tests/test_lift_manifest.py`.
- **Condition 2** — substrate-absent is a valid honest state with a
  documented reason; silent gaps FAIL. See `_check_unverifiable` and
  `_check_mandate_forced` in the same file.

Both conditions were bite-checked live by testing_agent at G2a-post-close
final verification (`/app/test_reports/iteration_4.json`) — fabricated
identifier caught, empty notes caught.
