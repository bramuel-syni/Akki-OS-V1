import React from 'react';

const variants = {
  ok: 'bg-emerald-50 text-emerald-800 border-emerald-200',
  pending: 'bg-amber-50 text-amber-800 border-amber-200',
  refused: 'bg-rose-50 text-rose-800 border-rose-200',
  live: 'bg-emerald-50 text-emerald-800 border-emerald-200',
  synthetic: 'bg-amber-50 text-amber-800 border-amber-200',
  closed: 'bg-slate-50 text-slate-600 border-slate-200',
  admitted: 'bg-emerald-50 text-emerald-800 border-emerald-200',
  warm: 'bg-sky-50 text-sky-800 border-sky-200',
  fresh: 'bg-teal-50 text-teal-800 border-teal-200',
  terminate_success: 'bg-emerald-50 text-emerald-800 border-emerald-200',
  terminate_budget: 'bg-amber-50 text-amber-800 border-amber-200',
  continue: 'bg-sky-50 text-sky-800 border-sky-200',
};

export default function StatusBadge({ status, className = '' }) {
  const variant = variants[status] || variants.pending;
  return (
    <span
      data-testid={`status-badge-${status}`}
      className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded border ${variant} ${className}`}
    >
      {status}
    </span>
  );
}
