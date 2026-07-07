/**
 * Phase 8 Stage B-1 — Shared UI Spec v1 component barrel (Owner-ratified).
 *
 * Owner E3 dispatch scope item 3:
 *   "Shared §8 component layer — /app/frontend/src/components/ui_spec_v1/.
 *    Formalise: ClassBadge, RefusalCard, OuterGateReceiptInline, StatusBadge,
 *    LedgerTable, TrustReceiptLink. Existing components in
 *    /app/frontend/src/components/* are the source-of-truth; consolidate
 *    under UI Spec v1 with re-exports. Every subsequent surface imports
 *    from here — no reimplementation."
 *
 * The single-source components live at `../*` (their historical location);
 * this barrel re-exports them so Phase 8 B-2/B-3/B-4/B-5 surface pages import
 * from `components/ui_spec_v1` (the canonical UI-Spec-v1 boundary). The
 * `test_shared_components_single_source_ui_spec_v1` gate parametrises over
 * these names and asserts no surface page reimplements any of them locally.
 */
export { default as ClassBadge } from '../ClassBadge';
export { default as RefusalCard } from '../RefusalCard';
export { default as OuterGateReceiptInline } from '../OuterGateReceiptInline';
export { default as StatusBadge } from '../StatusBadge';
export { default as LedgerTable } from '../LedgerTable';
export { default as TrustReceiptLink } from '../TrustReceiptLink';

// Phase 8 B-1 additions — auth surface renderers (distinct from RefusalCard
// per Owner E2 non-negotiable: the three governance render paths do not
// gain a fourth wearing the first's clothes).
export { default as AuthDeniedNotice } from '../AuthDeniedNotice';

// Phase 8 B-5a addition — Compliance Console §4.3 held-class posture badge
// (inheriting / explicit / unset). Single-source; consumed only by
// ComplianceRetentionRightsPage.
export { default as RetentionPostureBadge } from '../RetentionPostureBadge';

// Phase 8 Seam 3 Sub-stage 3 addition — CounterSignBanner (Owner Ruling 2,
// Amendment G, 2026-07-07: renders the capacity role the countersign
// endpoint required, not identity primary/bracket roles). Middle-dot
// (U+00B7) is E7-strict on binding copy.
export {
  default as CounterSignBanner,
  MIDDLE_DOT as COUNTER_SIGN_MIDDLE_DOT,
} from './CounterSignBanner';
