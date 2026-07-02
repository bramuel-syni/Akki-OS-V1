import React from 'react';

const SAFE_FIELDS = [
  'transform_version',
  'mint_window_id',
  'key_fingerprint',
  'applied_transformations',
  'input_identifier_categories',
];

const LABELS = {
  transform_version: 'Transform Version',
  mint_window_id: 'Mint Window',
  key_fingerprint: 'Key Fingerprint',
  applied_transformations: 'Applied Transformations',
  input_identifier_categories: 'Input Identifier Categories',
};

export default function OuterGateReceiptInline({ receipt }) {
  if (!receipt) return null;

  const safeEntries = SAFE_FIELDS
    .filter(f => receipt[f] !== undefined && receipt[f] !== null)
    .map(f => [f, receipt[f]]);

  if (safeEntries.length === 0) return null;

  return (
    <div
      data-testid="outer-gate-receipt-inline"
      className="rounded-lg border border-rms-line bg-white p-4"
    >
      <h4 className="text-xs font-semibold text-rms-mute uppercase tracking-wide mb-2">
        Outer-Gate Receipt
      </h4>
      <dl className="space-y-1.5">
        {safeEntries.map(([key, value]) => (
          <div key={key} className="flex justify-between text-xs gap-4">
            <dt className="text-rms-mute" data-testid={`ogr-label-${key}`}>
              {LABELS[key]}
            </dt>
            <dd
              className="font-mono text-rms-ink text-right truncate max-w-[300px]"
              title={typeof value === 'object' ? JSON.stringify(value) : String(value)}
              data-testid={`ogr-value-${key}`}
            >
              {Array.isArray(value) ? value.join(', ') : String(value)}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
