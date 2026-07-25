OWNER DISPATCH — EAB-2 HAZARD-STOP (a) RULING · 2026-07-24 · FINAL
Persist this dispatch verbatim at docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md as your first action. Echo its SHA-256 before any other motion. Do not re-surface these loci.
§1 · Ruled composition: ε + α + γ
Locus 1 = ε. Service1Refusal@v1 reason enum is exactly 4 members: the 3 v0 evidential reasons + coverage_gap. something-broke is not a refusal; it routes on the fault channel (HTTP 503 + structured detail per PROM-S1-config-defect-fail-loud). Prove renders on HTTP status + outcome discriminator. Option η stays rejected per R-A3.3 + v0 L18-22.
Locus 2 = α. Envelope carries filed_candidate_id only. estimated_effort is derived at Prove render via companion GET against Targeta's gap-candidate record. No estimated_effort field on the envelope.
Locus 3 = γ. No queue_action_url field on the envelope. Prove UI derives the Extract Shape-Objective route from filed_candidate_id at render.
Envelope consequence: the Stage A §5.1 declaration stands unchanged — 11-field envelope, 4-tuple additive set {estate_region, period, source_class, filed_candidate_id}, single-writer, sub-option (a1). No fields added by this ruling.
§2 · Failure-mode binding (part of the seal's semantics, test at EAB-2)
If the Locus-2 companion read fails, times out, or returns empty: Prove renders the coverage_gap refusal without the effort line, in refusal styling. It never degrades to the fault surface, never converts to something-broke, never blocks the refusal render. The queue action is unaffected by companion-read failure — its URL derives from filed_candidate_id on the envelope itself. EAB-2 lands a test cell asserting: refusal render succeeds with companion channel down.
§3 · Prove spec amendment (Owner-authored · non-blocking to the seal)
Echo the exact on-disk path + SHA of the Prove module spec as filed at Substrate-Drop v3. Do not amend until echoed.
Land the amendment as a sibling file in the same directory, named 05_prove_module_step4_amendment_2026_07_24.md, containing only: a header citing this ruling's path + SHA, and the following Owner-verbatim replacement for Step 4. The original spec file stays byte-identical.
Add a MANIFEST row for the sibling. Annotate the corresponding Substrate-Drop v3 CONFLICT row: RESOLVED by this ruling.
Owner-verbatim Step 4 replacement text:
Step 4 — Response Shapes (when Akki cannot answer). Three visually distinct states, never conflated with one another:
Not extracted yet — a refusal. Shows the gap plainly, estimated effort to close it, "Queue this gap" button. Carried on the refusal envelope (coverage_gap).
Evidence can't support — a refusal. States the specific reason; no queue option (more extraction wouldn't help). Carried on the refusal envelope.
Something broke — not a refusal. A fault surface, carried on the fault channel (HTTP 503 + structured detail), never rendered in refusal styling and never assigned a refusal reason.
§4 · Deferred bindings (record now · execute at their named phases · not EAB-2 content)
Record both inside the ruling file under this heading. Landing them early is a D-5 cross-phase leakage defect; losing them is a D7.
DB-1 (lands: Prove module phase, Lane 2b · gate-cell roster item): on the evidence-can't-support shape, the specific wire reason (no_defensibility_floor / no_lawful_basis / composition_below_floor) renders in plain language in the Answer Card honesty strip — not collapsed, not hidden behind Walk the Proof.
DB-2 (lands: Prove module phase, Lane 2b · gate-cell roster item): companion-channel failure never converts a refusal into a fault render (UI-side assertion of §2).
§5 · Motion order (D-9 between steps · halt only on hazard)
Persist this ruling · echo SHA.
Echo STEP 3 close artifacts now owed: Substrate-Drop v3 close report path + SHA · MANIFEST rows for the 8 filed artifacts · CONFLICT row register · OD-8 / OD-9 / OD-10 register rows. STEP 5 re-banding does not open until these are echoed.
§3 amendment (after path echo).
EAB-2 execution atomic per Stage A §5.1 under composition §1, including the §2 test cell. Close criteria: Service1Refusal@v1 contract file + snapshot landed (Parity 31→32) · AST + parity attest · R4 sidecar · full-sweep green including make ci · close report + register sibling · D-1..D-12 self-audit table.
STEP 5 re-banding from the echoed STEP 3 rows, every figure labeled "Provisional planning anchor — not a commitment. Relative weight only."
Nothing in this dispatch amends the ratified sequence, Lane 1 (still zero builder motion), or any prior ruling. Proceed.
