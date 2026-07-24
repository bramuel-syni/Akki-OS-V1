# Owner Decisions Register v1.0

**Purpose:** on-disk register of Owner-decision-required surfaces (OD rows). Each OD row is a discrete Owner-decision surface with a rides-list of downstream builder motions that block on its ruling. Sanction: `docs/rulings/owner_configuration_2026-07-24.md` §4.STEP-3 (verbatim: *"The audit must additionally mint new Owner-decision register rows (not buried phase content): OD-8 mail-provider binding … OD-9 public-surface exposure posture … OD-10 scheduler primitive …"*).

**Standing rule (per §4.STEP-3):** OD rows land as **explicit register rows, not buried phase content**. Every downstream builder motion that rides an OD row is blocked until the OD row is Owner-ruled and closed.

**Predecessor OD rows (OD-1..OD-7):** pre-existing register carrier. This v1 register is minted at OD-8 landing (2026-07-24 · Substrate-Drop v3 reconciliation atomic) and adopts the OD numbering forward from OD-8. Predecessor OD-1..OD-7 are referenced in phase-ledger row-lifecycle carriers and prior close reports (`docs/close_reports/**`) as informal register entries; retroactive formal-register admission of OD-1..OD-7 is Owner-side scope and does not block Substrate-Drop v3 close.

---

## §1 · OD-8 · Mail-provider binding · Notification Center email fanout

**Class:** Owner-decision required · sequence-blocking on Notification-Center-dependent module dispatches.
**Source:** Substrate-Drop v3 reconciliation `docs/audits/substrate_drop_v3_reconciliation_2026_07_24.md` §C.OD-8.
**Verbatim mandate excerpt (from Owner Configuration Dispatch 2026-07-24 §4.STEP-3):** *"OD-8 mail-provider binding (Notification Center email fanout)"*.

**Substrate-Drop v3 rides-list (module-spec § anchors):**

| Rides | Module-spec anchor | Category |
|---|---|---|
| Connect · Journey 1 · Step-5 Review · DPO sign-off notification email | `01_connect_module.md § Journey 1 Step 5` | DPO governance sign-off |
| Connect · Journey 3 · Add Source · notification email to DPO on Data Engineer submission | `01_connect_module.md § Journey 3` | DPO approval workflow |
| Connect · Journey 5 · Governance Contact updates · notification email to affected users | `01_connect_module.md § Journey 5` | Governance succession notification |
| Registry · Notification Center · census completion emails | `02_registry_module.md` (implicit via cross-module notification) | Registry auto-trigger completion |
| Extract · Journey 3 · Commissioned Objective approval email to Run Approver | `03_extract_module.md § Journey 3` | Extract approval workflow |
| Extract · Model Acceptance · notification email to Model Acceptor | `03_extract_module.md § Model Acceptance` | Extract model acceptance |
| Govern · Change-a-Rule · Co-Signer notification email + Verify-the-Rules link | `04_govern_module.md § Change-a-Rule` | Govern dual-control |
| Govern · Destroy-Data · Co-Signer notification email + 24h timer | `04_govern_module.md § Destroy-Data` | Govern dual-control |
| Govern · Governance Setup succession · Sponsor / CEO 3-party notification chain | `04_govern_module.md § Governance Setup succession` | Govern 3-party succession |
| Govern · Release Review · notification email to memo/deliverable creator on decision | `04_govern_module.md § Release Review` | Govern release notification |
| Team · Manage Users · invitation email · initial | `06_team_module.md § Journey 1 Step 4` | Team invitation |
| Team · Manage Users · Master Admin promotion DPO-approval notification email | `06_team_module.md § Journey 1 (Master Admin promotion path)` | Team promotion DPO approval |
| Prove · external-memo Release Review decision notification email | `05_prove_module.md § Memo Release` (out-of-module handoff to Govern) | Prove external memo |
| Public Receipts · revocation notification email (per PH-R3 rides · OD-9 co-blocker) | `05_prove_module.md § Public Receipts` | Prove public receipt lifecycle |

**Owner ruling required on:**

- **Provider choice:** SES · SendGrid · Postmark · Mailgun · other.
- **Domain / from-address strategy:** per-instance transactional-sender domain · shared platform domain · white-label per-tenant.
- **Bounce / suppression policy:** hard-bounce handling · suppression list maintenance · DKIM / SPF / DMARC posture.
- **Template governance:** whether email templates are Owner-verbatim canon (per verbatim doctrine) or builder-authored under gate discipline.
- **Rate-limiting posture:** per-tenant sending caps · per-recipient throttling · cost-envelope constraints.

**Sequence-blocking:** blocks Connect execution dispatch · blocks Govern Change-a-Rule / Destroy-Data / Release Review / Governance Setup succession dispatches · blocks Team invitation flow dispatch · blocks Extract commissioned-objective approval dispatch · blocks Public Receipts revocation dispatch.

**State:** open · Owner-decision required · 2026-07-24 minted.

---

## §2 · OD-9 · Public-surface exposure posture · Public Receipts no-login page

**Class:** Owner-decision required · sequence-blocking on Public-Receipts-dependent Prove Module dispatches.
**Source:** Substrate-Drop v3 reconciliation `docs/audits/substrate_drop_v3_reconciliation_2026_07_24.md` §C.OD-9.
**Verbatim mandate excerpt (from Owner Configuration Dispatch 2026-07-24 §4.STEP-3):** *"OD-9 public-surface exposure posture for Public Receipts (no-login page: rate limiting, link entropy, revocation-under-caching — rides PH-R3 domain/TLS)"*.

**Substrate-Drop v3 rides-list:**

| Rides | Module-spec anchor | Category |
|---|---|---|
| Prove · Public Receipt generation (DPO-only) | `05_prove_module.md § Public Receipts` | Prove receipt lifecycle |
| Prove · Public Receipt no-login verify page | `05_prove_module.md § Public Receipts § verify` | Prove public surface |
| Prove · Public Receipt expiry lifecycle | `05_prove_module.md § Public Receipts § expiry` | Prove receipt lifecycle |
| Prove · Public Receipt revocation semantics under caching | `05_prove_module.md § Public Receipts § revoke` | Prove receipt lifecycle |
| Prove · Public Receipt verification log | `05_prove_module.md § Public Receipts § verification-log` | Prove audit trail |
| PH-R3 (Production Housing) · domain / TLS binding for Public Receipts hosting | `docs/production_housing/frontend_backend_split.md` (implicit PH-R3 anchor) | Production Housing |

**Owner ruling required on:**

- **Rate limiting:** per-IP · per-receipt · per-instance · verification attempt limits · verification-log write-rate caps.
- **Link entropy:** bit count of the receipt token (128 · 192 · 256 · other) · charset (base32 · base58 · base64url · UUIDv4) · human-readable-fragment prefix.
- **Revocation-under-caching semantics:** cache-header posture (short TTL · long TTL with revocation-check on hit · immutable-until-revoked) · CDN interaction (fastly / cloudflare / other · purge semantics) · what a stale-cache viewer sees post-revocation.
- **Verify page hosting:** subdomain (`verify.<instance>.<domain>`) · path-prefix (`<instance>.<domain>/verify/…`) · dedicated verifier domain shared across instances.
- **PH-R3 dependency:** domain acquisition + TLS certificate lifecycle · CDN choice · WAF posture at the no-login boundary.
- **Verification-log data retention:** how long is the verification-log retained · what fields are captured (IP · UA · referer · timestamp · receipt-token-fragment) · GDPR / regional privacy implications.

**Sequence-blocking:** blocks Prove Module execution dispatch (Public Receipts subsurface) · blocks PH-R3 finalization · blocks external-facing memo release ceremonies that reference the public-receipt URL pattern.

**State:** open · Owner-decision required · 2026-07-24 minted.

---

## §3 · OD-10 · Scheduler primitive · census debounce / auto-trigger

**Class:** Owner-decision required · sequence-blocking on Registry-auto-trigger and Connect-post-signoff-census-kickoff dispatches.
**Source:** Substrate-Drop v3 reconciliation `docs/audits/substrate_drop_v3_reconciliation_2026_07_24.md` §C.OD-10.
**Verbatim mandate excerpt (from Owner Configuration Dispatch 2026-07-24 §4.STEP-3):** *"OD-10 scheduler primitive for census debounce/auto-trigger"*.

**Substrate-Drop v3 rides-list:**

| Rides | Module-spec anchor | Category |
|---|---|---|
| Registry · auto-triggered census on new-source-added | `02_registry_module.md § Journey 1 Step 1 (trigger)` | Registry auto-trigger |
| Registry · debounce logic when multiple sources added in quick succession | `02_registry_module.md § Journey 1 (implicit debounce)` | Registry rate-control |
| Connect · post-signoff first-census kickoff modal ("Connection successful. Run your first census now?") | `01_connect_module.md § Journey 1 Step-5 post-signoff` | Connect completion trigger |
| Registry · scheduled re-census cadence (weekly · monthly · on-demand · other) | `02_registry_module.md § Journey 1 (implicit cadence)` | Registry recurring |
| Mtafiti backend service · census job scheduling primitive (currently synchronous per-request only) | `backend/services/mtafiti/**` (shipped surface) | Mtafiti backend scheduling |

**Owner ruling required on:**

- **Primitive choice:** in-process `asyncio.create_task` · APScheduler (in-process · with persistence) · Celery + Redis · dedicated cron container · managed service (AWS EventBridge · Cloud Scheduler · other).
- **Persistence discipline:** on-restart resume semantics · at-least-once vs. at-most-once vs. exactly-once for census kickoffs · idempotency-key discipline for debounced runs.
- **Debounce window duration:** 5s · 30s · 5min · other · Owner-set default with §0-CAL DEFAULT-class posture.
- **Cadence for recurring re-census:** weekly · monthly · on-demand-only · configurable per-instance (rides OD-10.b sub-decision).
- **Failure / retry policy:** how failed census jobs surface to Registry landing (visible error stripe · silent retry with backoff · notification email — rides OD-8).

**Sequence-blocking:** blocks Registry Module execution dispatch (auto-trigger + debounce subsurfaces) · blocks Connect Module execution dispatch (post-signoff first-census kickoff subsurface) · blocks Mtafiti backend scheduling primitive additive-surface completion (rides G-13 §8.1 additive-surface pattern).

**State:** open · Owner-decision required · 2026-07-24 minted.

---

*Owner Decisions Register v1.0 · minted 2026-07-24 under Owner Configuration Dispatch (SHA `ec95a0acec13d81b…`) §4.STEP-3 mandate · sequence-blocking on downstream module dispatches until Owner rules · Standing Rule v3 · Owner-verbatim mandate excerpts carried byte-for-byte at each row.*
