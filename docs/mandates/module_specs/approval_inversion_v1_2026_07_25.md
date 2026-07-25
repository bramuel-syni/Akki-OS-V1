# A2 · Approval Inversion (Owner-authored 2026-07-25)

**Class:** Sibling amendment supersedes Extract Journey 2.
**Sanction:** `docs/rulings/owner_change_order_2026-07-25.md` · SHA `33b16441025ac0bc757fd92f770252d30f0e63de4e4609c635be3ce9252fa568` (Owner-authored 2026-07-25 · FINAL · non-re-openable · not builder-modifiable).
**Predecessor byte-identity attest:** `docs/mandates/module_specs/03_extract_module.md` · SHA `82348a163d5827da365f0d754221d0978e1e27ea5619b4c05688b85a531fbf91` · byte-identical (`git diff HEAD docs/mandates/module_specs/03_extract_module.md` empty this atomic · same predecessor as A1 · both amendments supersede different surface layers).
**Interpretation rule:** amendment wins where in conflict; pre-amendment canon stands where amendment is silent.

---

## A2 · Approval Inversion (supersedes Extract Journey 2)

### A2.1 Deletion
The standing **Approval Queue** (pre-run human approval of every commissioned objective) is deleted. The **Run/Commission Approver** role is retired. The status **"Awaiting approval"** is removed from the lifecycle. The Approval Queue notification category is dropped.

### A2.2 Admissibility gate (replacement)
Every commission is evaluated at the **Commission card**, machine-checked, fail-closed, verdict receipted:
1. **Rights compatibility** — requested delivery/output rights vs. source usage rights (Internal-Only scope cannot feed a licensable output; a trained model inherits its training-data rights).
2. **Privacy floor** — requested scope satisfies the configured group-size floor.
3. **PII posture** — masking/pseudonymization rules (incl. Class D registries per A3) resolvable over the scope.
4. **Budget ceiling** — present, positive, within org limit where configured.
5. **Scope resolvability** — every referenced source Connected and censused.
**Outcomes:** all-pass → runs immediately ("In progress"). Any fail → **refused at the card, in dialogue, specific rule named** (a refusal, not a queue). Pass-with-flag (declared flag conditions only) → **"Held for a check,"** resolved by the single-person pattern (Quarantine's), by the DPO or delegate. Anything unclassifiable → holds. Every verdict (pass/refuse/hold) is receipted and feeds the DPO Estate's enforcement counts.

### A2.3 Seventh governance rule — Commission auto-run ceiling (Class O)
Added to Connect Step 3: numeric + currency, recommended default per org, **∞ permitted**. Commissions at/under the ceiling auto-run when rule-clean; above it, the commission holds for a **single DPO countersign** (the reserved "Pending policy check" state). Changeable only via Change-a-Rule (two approvals + waiting period + certificate + Verify-the-Rules).

### A2.4 Preserved gates (explicit non-scope)
**Release Review** (everything leaving the org) and **Model Acceptance** (human quality judgment over the six checks) are untouched by this amendment. "Remove approval" must not be read expansively.

### A2.5 User-story delta (summary; full delta in A7)
Struck: Approver approve/return stories. Amended: run-tracking stories to the In-progress vocabulary. New: admissibility-refusal story; held-for-check story; ceiling-countersign story.

---

*A2 sibling amendment · Owner-authored 2026-07-25 · Owner-verbatim carrier · sanctioned by `docs/rulings/owner_change_order_2026-07-25.md` · predecessor `03_extract_module.md` byte-identical · Standing Rule v3 held.*
