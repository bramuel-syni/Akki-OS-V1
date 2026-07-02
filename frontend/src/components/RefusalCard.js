import React from 'react';
import { ShieldAlert } from 'lucide-react';
import ClassBadge from './ClassBadge';

export default function RefusalCard({ refusal }) {
  if (!refusal) return null;
  return (
    <div
      data-testid="refusal-card"
      className="rounded-lg border-2 border-amber-300 bg-amber-50 p-5"
    >
      <div className="flex items-start gap-3">
        <ShieldAlert className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <h3
            data-testid="refusal-headline"
            className="text-sm font-semibold text-amber-900"
          >
            Not to the standard required.
          </h3>
          <dl className="mt-3 space-y-2 text-sm">
            {refusal.asked && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Asked</dt>
                <dd data-testid="refusal-asked" className="mt-0.5 text-amber-900">{refusal.asked}</dd>
              </div>
            )}
            {refusal.reason && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Reason</dt>
                <dd data-testid="refusal-reason" className="mt-0.5 text-amber-900 font-mono text-xs">{refusal.reason}</dd>
              </div>
            )}
            {refusal.supported_class && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">Supported class</dt>
                <dd data-testid="refusal-supported-class" className="mt-0.5">
                  <ClassBadge defensibilityClass={refusal.supported_class} />
                </dd>
              </div>
            )}
            {refusal.what_would_raise_it && (
              <div>
                <dt className="text-xs font-medium text-amber-700 uppercase tracking-wide">What would raise it</dt>
                <dd data-testid="refusal-raise" className="mt-0.5 text-amber-900">{refusal.what_would_raise_it}</dd>
              </div>
            )}
          </dl>
        </div>
      </div>
    </div>
  );
}
