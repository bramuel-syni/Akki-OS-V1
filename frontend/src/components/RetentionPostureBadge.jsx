/**
 * RetentionPostureBadge — v2.1 §4.3 held-class posture indicator.
 *
 * Single-source component; imported via `../components/ui_spec_v1` barrel.
 * Renders one of three postures:
 *   - `inheriting` — "inherits from system default" (subdued styling)
 *   - `explicit`   — "class-specific window" (prominent styling)
 *   - `unset`      — "no rule set" (adversarial-to-comfort styling;
 *                     B5a-G3 substrate)
 *
 * data-testid namespace: `retention-posture-{posture}` — each posture
 * carries a distinct testid so the invariant gate
 * `test_compliance_retention_held_class_separately_addressable` can
 * parametrise over held-class × posture combinations.
 */
import React from 'react';

const POSTURE_COPY = {
  inheriting: 'inherits from system default',
  explicit: 'class-specific window',
  unset: 'no rule set',
};

const POSTURE_STYLES = {
  inheriting: 'inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-slate-100 text-slate-600 border border-slate-200',
  explicit: 'inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200',
  unset: 'inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-amber-50 text-amber-900 border border-amber-200',
};

export default function RetentionPostureBadge({ posture }) {
  const copy = POSTURE_COPY[posture] || 'unknown posture';
  const styles = POSTURE_STYLES[posture] || POSTURE_STYLES.unset;
  return (
    <span
      className={styles}
      data-testid={`retention-posture-${posture}`}
      role="status"
    >
      {copy}
    </span>
  );
}
