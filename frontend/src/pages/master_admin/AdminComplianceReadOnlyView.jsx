/**
 * Phase 8 Stage B-5b — B-4 read-only retrofit view.
 *
 * Per BCR v1.4.1 §3.13 RT-R1: compliance rule classes render read-only on
 * the Administration console with an "owned by Compliance" marker. Write
 * ownership never exists in both consoles simultaneously (RT-R2).
 */
import React from 'react';

const MIDDLE_DOT = '\u00B7';

// Per BCR §3.13 line 291 and UI Spec §6.4 line 143: verbatim marker.
export const OWNED_BY_COMPLIANCE_MARKER = 'owned by Compliance';

const COMPLIANCE_RULE_CLASSES = [
  { key: 'retention_windows', label: 'Retention windows' },
  { key: 'disclosure_thresholds', label: 'Disclosure thresholds' },
  { key: 'lawful_basis_registry', label: 'Lawful-basis registry' },
  { key: 'source_standing_table', label: 'Source-standing table' },
];

const AdminComplianceReadOnlyView = () => (
  <section
    data-testid="admin-compliance-read-only-view"
    className="rounded-lg border border-slate-200 bg-slate-50 p-6"
  >
    <header className="mb-4">
      <h2
        data-testid="admin-compliance-read-only-header"
        className="text-lg font-medium"
      >
        Compliance rule classes {MIDDLE_DOT} read-only
      </h2>
      <p className="text-sm text-slate-600 mt-1">
        These rule classes are {OWNED_BY_COMPLIANCE_MARKER}. To change them,
        the Compliance Console is the authority.
      </p>
    </header>
    <ul
      data-testid="admin-compliance-read-only-list"
      className="space-y-2 list-none"
    >
      {COMPLIANCE_RULE_CLASSES.map((rc) => (
        <li
          key={rc.key}
          data-testid={`admin-compliance-read-only-item-${rc.key}`}
          className="flex items-center justify-between border border-slate-200 rounded bg-white px-4 py-2 text-sm"
        >
          <span>{rc.label}</span>
          <span
            data-testid={`admin-compliance-marker-${rc.key}`}
            className="text-xs text-slate-500 italic"
          >
            {OWNED_BY_COMPLIANCE_MARKER}
          </span>
        </li>
      ))}
    </ul>
  </section>
);

export default AdminComplianceReadOnlyView;
