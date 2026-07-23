**AKKI · GOVERNED ARTIFACT · REQUIREMENTS SPECIFICATION**

**S1 Memory Model & Integration Wizard — Specification v1.0**

Per-application memory planes, write-back, usage-proportional persistence, and the integration commissioning flow · 2026-07-23

***Reading guide:** written for a reader with no prior context. §1 states the promise; §2 defines every referenced system; §3 the memory-plane model; §4 the write-back contract; §5 usage-proportional persistence; §6 the integration wizard; §7 governance visibility; §8 quality treatment; §9 parameters; §10 enforcement and execution. Normative language: MUST / MUST NOT / MAY. Values: FACT / NORM / DEFAULT (DEFAULTs revise on evidence at evaluation boundaries).*

**§1 — Purpose and promise**

Akki’s integration surface (S1) gives applications governed access to a customer’s qualified intelligence. This specification extends S1 from query access to memory service: every integrated application receives a durable, governed memory plane that grows in proportion to its use. The promise to the integrating builder: your application arrives stateless and becomes knowledgeable — what it reads, contributes, and repeatedly needs persists for it, under the same governance as everything else in the platform, with zero memory infrastructure built on the application side. The promise to the estate holder: every application’s memory is visible, receipted, rights-bound, and revocable — integration deepens without governance thinning.

**§2 — Referenced systems**

-   **S1:** the platform’s application-integration service — scoped API keys, the answer envelope (including all refusal shapes), webhook delivery callbacks. Every S1 call writes to the platform ledger.

-   **Qualified unit:** the atomic intelligence record — five rings: content, provenance, defensibility class, context, re-extraction handle. Contract five_rings@v0, frozen.

-   **The Registry:** the instance’s holding of qualified units, indexed by stratum, class, and rights.

-   **Objective Service:** commissioned work — an ObjectiveRequest carrying scope, evidence floor, rights, and a plan; the platform’s unit of ordered extraction and standing service.

-   **Evidence partitions:** precomputed, objective-scoped unit sets that interactive reads serve from — request-time reads never touch the raw estate.

-   **Extracted Intel Registry:** the operational layer preserving every produced artifact with inherited rights.

-   **license_class:** the rights marking on every unit and artifact; defaults internal_only, fail-closed.

-   **Seam values:** the instance’s owner-set governance constants (deletion ceremony, quarantine threshold, aggregation floor k ≥ 20, and siblings).

-   **DPO record:** the compliance surface where every rule, access, and violation is visible with receipts.

-   **TQ-2:** the standing rule that any new transformation output class registers its quality-matrix row at its Stage A.

**§3 — The memory plane**

-   **3.1 ·** Every integration key is issued with exactly one memory plane: a durable, instance-scoped, key-scoped partition. The plane is created at commissioning (§6) and exists for the key’s lifetime.

-   **3.2 ·** The plane holds three stores: the retrieval scope (which registry strata and evidence partitions the application may read — references, not copies); the contribution store (units the application has written back, §4); and the working set (what usage-proportional persistence retains and precomputes for this application, §5).

-   **3.3 ·** Plane isolation is by construction: the persistence layer refuses any read or write not scoped to a key’s plane — the same scoped-accessor pattern that enforces instance isolation. Cross-plane reads do not exist; sharing happens only through the Registry via rights-bound publication (§4.5).

-   **3.4 ·** Every plane operation — read, write, retention change, revocation — writes a ledger row. A plane is fully reconstructible from the ledger.

-   **3.5 ·** Key revocation freezes the plane (no reads, no writes); plane deletion follows the instance’s deletion ceremony — two-person approval, authorized path, destruction attestation. A revoked application’s contributed units survive in the Registry if and only if they were published (§4.5); unpublished contributions delete with the plane.

**§4 — The write-back contract**

-   **4.1 ·** An application MAY contribute derived context, corrections, and conclusions back to its plane. Every contribution lands as a qualified unit in the five-ring shape — no free-form blobs. Content, provenance (the application, its key, the S1 calls it derived from), defensibility class, context, and re-derivation handle are all required at write; incomplete contributions reject at the API boundary.

-   **4.2 ·** Contributed units carry class app_contributed and inherit license_class: internal_only at birth. Their defensibility class is capped at the class their cited sources support: an application citing inferred material cannot mint corroborated facts.

-   **4.3 ·** Contributions are plane-local by default: visible to the contributing application only, invisible to Ask, briefs, and every other consumer.

-   **4.4 ·** Write-back is a commissioning-time choice (§6): ON with a per-cycle volume ceiling (DEFAULT: 10,000 units/cycle) or OFF. The DPO sees the setting and the volumes either way.

-   **4.5 ·** Publication — promoting a contributed unit from plane-local to Registry-visible — is a separate act: it passes the quality gates of its output class (§8), carries its rights, and where seam values require, passes release review. Publication is never automatic.

**§5 — Usage-proportional persistence**

-   **5.1 ·** The working set grows from observed use: units and partitions the application reads repeatedly are retained hot; query shapes it repeats gain precomputed results; strata it never touches are never replicated into its plane. Growth follows measured access patterns — never anticipation.

-   **5.2 ·** Persistence decisions are mechanical and parameterized: retention triggers at N reads within a window (DEFAULT: 3 reads / 30 days), precompute triggers at M repeats of a query shape (DEFAULT: 5), eviction runs least-recently-used at the plane’s storage ceiling (commissioning-set, §6). All three are plane-visible numbers, not heuristics.

-   **5.3 ·** The working set holds references and derived read-structures — never copies that would escape rights binding. Evicting a working-set entry loses nothing: the Registry remains the source of record.

-   **5.4 ·** Memory growth reports per plane per cycle — units retained, precomputes held, storage consumed — to the application (its own dashboard line) and to the DPO record (§7).

**§6 — The integration wizard**

Integrating an application is commissioning a standing objective with a memory plane attached — one flow, one ledgered act. The wizard runs the platform’s standard objective-shaping steps with three memory-specific additions:

-   **6.1 · Define:** the application’s standing need in plain words — what intelligence it consumes, for what function.

-   **6.2 · Scope:** retrieval scope selected from what the Registry holds — strata, periods, evidence floor — with coverage shown against the stated need before commitment.

-   **6.3 · Standards and rights:** evidence floor for served answers · the plane’s rights ceiling (what the application may export, bounded by source license_class) · aggregation floors applied per seam values.

-   **6.4 · Memory plane settings:** write-back ON/OFF + volume ceiling · storage ceiling · retention/precompute parameters (defaults shown, adjustable) · webhook registration for delivery callbacks.

-   **6.5 · Commission:** one ledgered act creates the key, the plane, and the standing ObjectiveRequest together; the confirmation states what is permanent. The application’s first call lands in the DPO record like every call after it.

-   **6.6 ·** Re-scoping (widening retrieval scope, raising ceilings) re-enters the wizard at 6.2 and re-commissions; tightening applies without ceremony. Scope changes are ledger events either way.

**§7 — Governance visibility (DPO extension)**

-   **7.1 ·** The DPO record gains a per-application view: each plane’s scope, rights ceiling, write-back setting and volumes, storage growth, call activity, and every scope change with its ledger receipt — the same table shape as the estate’s governance classes.

-   **7.2 ·** Contributed-unit volumes and publication events are line items; a publication that passed release review cites its review record.

-   **7.3 ·** Plane freeze and deletion appear as ceremony records. Nothing about an application’s memory is invisible to the estate holder.

**§8 — Quality treatment (TQ-2 compliance)**

-   **8.1 ·** app_contributed units are a transformation output class and register their quality-matrix row with this specification: correctness = spot-agreement of contributed conclusions against their cited sources (sampled) · loss = not applicable (contributions are additive) · precision = unsupported-claim rate in contributions (sampled) · attribution = citation-resolution rate (every cited S1 call resolves; mechanical).

-   **8.2 ·** Publication (§4.5) is the gate where the row binds: plane-local contributions are the application’s own working material and are sampled, not gated; nothing enters the Registry without passing the row.

**§9 — Operating parameters**

|                        |                                                              |                                         |
|------------------------|--------------------------------------------------------------|-----------------------------------------|
| **Parameter**          | **Definition**                                               | **Class / default**                     |
| Plane isolation        | Zero cross-plane reads; accessor refuses unscoped operations | FACT-class invariant; cell-enforced     |
| Write-back ceiling     | Contributed units per plane per cycle                        | DEFAULT 10,000; commissioning-set       |
| Retention trigger      | Reads within window before a unit retains hot                | DEFAULT 3 reads / 30 days               |
| Precompute trigger     | Query-shape repeats before precompute                        | DEFAULT 5                               |
| Storage ceiling        | Per-plane cap; LRU eviction at ceiling                       | Commissioning-set; no default floor     |
| Citation resolution    | Contributed units’ cited calls resolve                       | 100%; reject at write below it          |
| Unsupported-claim rate | Sampled precision of contributions                           | Reported; publication gate binds per §8 |
| Ledger coverage        | Plane operations writing ledger rows                         | 100%; a plane is ledger-reconstructible |

**§10 — Enforcement and execution**

-   **10.1 ·** Enforcement uses the standing vehicles only: scoped-accessor refusal (isolation) · API-boundary schema rejection (write-back shape) · cells on the carrying phase (plane lifecycle, ledger coverage, publication gating) · standing queries (ceiling breaches, stale planes) · the DPO record (visibility). No new enforcement machinery.

-   **10.2 ·** Carrying phase: UI-2 (Integration Console + S1 memory plane) per the ratified sequence. This specification lands on-disk as requirements canon ahead of UI-2’s Stage A; R4 rows, matrix row, and cells land with UI-2’s execution. Per D-12: the mechanics herein — partitioning, scoped access, schema-gated writes, LRU retention, ledgered lifecycle — are known and parameterized; the capability deploys in force with UI-2; no trial modes exist.

-   **10.3 ·** Landing pattern: verbatim conversion to docs/requirements/s1_memory_model_spec_v1.md, SHA in reply, governance pointer appended.

Syni.ai · S1 Memory Model & Integration Wizard Specification v1.0 · 2026-07-23 · Companion to: Surface & Journey Map v1.0 · Transformation Quality Specification v1.0 · Operating Values v1.0 · Registry Doctrine (D-12)
