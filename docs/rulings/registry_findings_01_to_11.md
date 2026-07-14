# Registry Findings 01–11 · Owner Rulings Record

**Dispatched:** 2026-07-11 (post-close on §3.5 Registry Population)
**Basis:** `/app/docs/close_reports/registry_population.md` §6 (8 client-promise-touching + 3 optional-Owner-discretion = 11 findings) + `/app/docs/registry/function_promise_registry_v0.md` §7 escalation surface.
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 in force · Defect D7 binds (gap-fill cells become candidates for future Owner-dispatched phases, NOTHING MORE).
**Doctrine SHA:** `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471`.

---

## §0. Owner preamble (verbatim)

> "Registry Population close: acknowledged as self-ratified per §12. Below-band −65% accepted as disclosed — compact tables are reduction discipline working, and 46 promises / 66 functions with zero unaccounted gates is exactly the 'small canonical set' the doctrine predicted. The Registry earned rent on day one: 11 findings from its first population.
>
> Rulings on all 11 — dispositions recorded in the Registry; no code work dispatched by any of them (D7 holds; gap-fill cells become candidates for future owner-dispatched phases, nothing more):"

---

## §1. Ruling — Q2-01 (attachment corrected, then accepted)

**Owner verbatim:**
> "Q2-01 — attachment corrected, then accepted. EE-G1..G4 protect scoped access, not envelope inheritance: the 8-EXT promise was external integrators see only their own assets, enforced server-side. Attach to the scoped-access promise (trace S1.register + S1.scoped-key), recovering the wording from the 8-EXT ruling record verbatim where it exists. The tentative PROM-S1-provable-envelope-inheritance attachment is struck."

**Verbatim source of the 8-EXT scoped-access promise** (recovered as directed):

Source A — BCR §3.9 EE-R2 line 240 verbatim (cited at `docs/stage_a_proposals/8_ext.md:115`):
> *"View scoping: an external_engineer sees Register / First call / Administer scoped to their own apps, keys, usage, and refusal health — and NEVER other parties' apps, estate contents, fleet, pricing, or any master-admin control."*

Source B — BCR §3.9 EE-R4 line 242 verbatim (cited at `docs/stage_a_proposals/8_ext.md:117`):
> *"Every externally reachable endpoint enforces scope server-side — view-layer filtering alone fails review. Enforcement rides the existing B-1 scope primitive; no parallel mechanism."*

Source C — 8-EXT close report §2.1 EE-G roster (`docs/close_reports/8_ext.md:55`, EE-G2 attest):
> "EE-G2 own-apps-only + foreign-resource 403 — external can read/write own; foreign → 403 `auth_scope_insufficient`."

**Applied at registry:** New promise row `PROM-S1-external-scoped-access` added to §2 (BCR §3.9 EE-R2 + EE-R4 verbatim). `ui.engineer.onboarding` row (§3.f) re-attached: promise field updated `PROM-S1-refusal-taxonomy-closed · PROM-S1-external-scoped-access`; the tentative `PROM-S1-provable-envelope-inheritance` attachment struck. `service_trace` unchanged (`S1.register · S1.scoped-key`). §4 Q2-01 annotated `[RULED · Q2-01-CORRECTED · rulings/registry_findings_01_to_11.md §1]`.

---

## §2. Ruling — Q2-02 (accepted as recovered)

**Owner verbatim:**
> "Q2-02 — accepted as recovered. MAN-G1..G3 → PROM-S3-audit-trail-immutable. Correct promise, correct trace."

**Applied at registry:** No change to `northena.audit_trail.master_admin_immutable` row (already attached to `PROM-S3-audit-trail-immutable`). §4 Q2-02 annotated `[RULED · Q2-02-ACCEPTED]`.

---

## §3. Ruling — Q2-03 (accepted as recovered)

**Owner verbatim:**
> "Q2-03 — accepted as recovered. Promise text recovered from policy prose is legitimate archaeology — the format of the source doesn't diminish the promise. RT-* → PROM-S3-retention-held-class-no-delete."

**Applied at registry:** No change to retention rows (already attached to `PROM-S3-retention-held-class-no-delete`). §4 Q2-03 annotated `[RULED · Q2-03-ACCEPTED · policy-prose-recovery-is-legitimate-archaeology]`.

---

## §4. Ruling — Q3-01 (reclassified, then recorded)

**Owner verbatim:**
> "Q3-01 — reclassified, then recorded. Split the step: the integrator's downstream behavior is outside platform scope; the platform's obligation is that receipts arrive machine-passable — envelope completeness such that pass-through is possible. Record the gap as platform-side with that narrowed scope; whether a direct cell exists for envelope-completeness is a legitimate future check."

**Applied at registry:** §5 Q3-01 rewritten to reflect narrowed scope: "envelope completeness such that pass-through is possible" (platform-side); annotated `[RULED · Q3-01-RECLASSIFIED · narrowed-scope · envelope-completeness-cell-is-legitimate-future-check]`.

---

## §5. Ruling — Q3-02 (stands as open gap, by design)

**Owner verbatim:**
> "Q3-02 — stands as an open gap, by design. Onboard-context is a real journey step with no surface — the doctrine surfaced this gap deliberately at Part II. Mark [OWNER: future phase]; never retired, never papered."

**Applied at registry:** §5 Q3-02 annotated `[OWNER: future phase] · [RULED · Q3-02-OPEN-BY-DESIGN · never-retired · never-papered]`.

---

## §6. Ruling — Q3-03 (S4.license stays in Layer 0)

**Owner verbatim:**
> "Q3-03 — S4.license stays in Layer 0. The commercial cut salvaged the buyer surface; it didn't kill the service — data sale is the product thesis. Mark the gap [OWNER: buyer-commercial-tier]; the surface restores when a commercial posture is ruled. Retiring the journey step would let an implementation event edit the product definition — exactly backwards."

**Applied at registry:** §5 Q3-03 annotated `[OWNER: buyer-commercial-tier] · [RULED · Q3-03-STAYS-IN-L0 · surface-restores-when-a-commercial-posture-is-ruled · retiring-would-let-implementation-event-edit-product-definition]`.

---

## §7. Ruling — Q3-05 (recorded with sub-coverage noted)

**Owner verbatim:**
> "Q3-05 — recorded with sub-coverage noted. Direct S1.scoped-key cell listed as a candidate; sub-coverage via the Engineer surface acknowledged as real but indirect."

**Applied at registry:** §5 Q3-05 annotated `[RULED · Q3-05-RECORDED · candidate-direct-S1.scoped-key-cell · sub-coverage-via-Engineer-surface-real-but-indirect]`.

---

## §8. Ruling — Q3-06 (recorded)

**Owner verbatim:**
> "Q3-06 — recorded. Walk-side audit-ledger cell listed as a candidate; view-side coverage noted. A mandate-named behavior with half its surface tested is precisely what Q3 exists to show."

**Applied at registry:** §5 Q3-06 annotated `[RULED · Q3-06-RECORDED · candidate-walk-side-audit-ledger-cell · view-side-covered · half-surface-tested-is-what-Q3-exists-to-show]`.

---

## §9. Ruling — Q2-04 (attach, don't retire)

**Owner verbatim:**
> "Q2-04 — attach, don't retire. V1-G0..G6 promises recover from docstrings (frozen-wire-contract integrity); they're load-bearing. Q1-candidate flag stands for future automation."

**Applied at registry:** V1-G0..V1-G6 attached to existing promise `PROM-S1-frozen-wire-contract` (recovered from docstrings; frozen-wire-contract integrity — no new promise needed; existing row covers). §4 Q2-04 annotated `[RULED · Q2-04-ATTACHED-NOT-RETIRED · PROM-S1-frozen-wire-contract · Q1-candidate-flag-stands-for-future-automation]`.

---

## §10. Ruling — Q2-05 (hold; no bulk disposition)

**Owner verbatim:**
> "Q2-05 — hold; no bulk disposition. Mixed legacy gates get individually read at a future owner-dispatched Registry-maintenance turn; those already tracing via the AF-G1 re-pointing keep their attachment now. No retirement without reading — archaeology discipline applies to endings too."

**Applied at registry:** §4 Q2-05 annotated `[RULED · Q2-05-HOLD · individual-read-at-future-Registry-maintenance-turn · AF-G1-repointed-rows-keep-attachment · no-retirement-without-reading · archaeology-discipline-applies-to-endings-too]`. No bulk disposition applied. No retirement.

---

## §11. Ruling — Q3-04 (confirmed intentional)

**Owner verbatim:**
> "Q3-04 — confirmed intentional. S5 gaps marked by-design per doctrine; closed."

**Applied at registry:** §5 Q3-04 annotated `[RULED · Q3-04-CONFIRMED-BY-DESIGN · closed · per-doctrine-Part-II-S5]`.

---

## §12. Standing constraints preserved (per Owner dispatch)

- **D7 holds:** gap-fill cells become candidates for future Owner-dispatched phases, NOTHING MORE.
- **No code work dispatched by any of the 11 rulings.**
- **No retirement without reading** (Q2-05): archaeology discipline applies to endings too.
- **Parity 31/31 preserved:** doc-only commit.
- **MANDATE-COMPLETE 2026-07-10 held.**
- **Registry Doctrine v1.0 in force:** R4 reflexive · D-10 self-audit rides submission.
- **Standing Rule v3:** on-disk canonical; SHAs in reply body.

---

## §13. Dispatch summary

Per Owner: "one doc-only commit: apply the 11 dispositions to `function_promise_registry_v0.md` rows (Q2-01's corrected attachment included), update the findings sections with ruling references, land `docs/rulings/registry_findings_01_to_11.md` carrying these rulings verbatim."

**Executed:**
1. This file created (rulings record · Owner verbatim carrier · Standing Rule v3 primary artifact).
2. `function_promise_registry_v0.md` §2 promise table extended with new `PROM-S1-external-scoped-access` promise row (Q2-01 correction; BCR §3.9 EE-R2 + EE-R4 verbatim source).
3. `function_promise_registry_v0.md` §3.f `ui.engineer.onboarding` promise field re-attached (strike `PROM-S1-provable-envelope-inheritance` tentative; add `PROM-S1-external-scoped-access`).
4. `function_promise_registry_v0.md` §4 + §5 finding rows annotated with per-Owner `[RULED · …]` tags cross-referencing this file's §-sections.
5. `function_promise_registry_v0.md` §7 escalation-surface list annotated as `[SUPERSEDED · RULED 2026-07-11 · see rulings/registry_findings_01_to_11.md]` (Standing Rule v3 archival — not deleted).

═══════════════════════════════════════════════════════════════════

*End of Registry Findings 01–11 rulings record. All 11 dispositions applied verbatim per Owner. No code dispatched. Defect D7 respected. Parity 31/31 preserved. Standing Rule v3 · on-disk canonical.*
