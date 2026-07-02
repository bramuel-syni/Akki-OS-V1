import React from 'react';
import { Link } from 'react-router-dom';
import StatusBadge from './StatusBadge';
import ClassBadge from './ClassBadge';

export default function LedgerTable({ rows, showTrace = true }) {
  if (!rows || rows.length === 0) {
    return <p data-testid="ledger-empty" className="text-sm text-rms-mute py-4">No ledger rows.</p>;
  }
  return (
    <div data-testid="ledger-table" className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-rms-line text-left text-xs text-rms-mute uppercase tracking-wide">
            <th className="py-2 pr-3 font-medium">Stage</th>
            <th className="py-2 pr-3 font-medium">Decision</th>
            <th className="py-2 pr-3 font-medium">Reason</th>
            <th className="py-2 pr-3 font-medium">Class</th>
            {showTrace && <th className="py-2 pr-3 font-medium">Trace</th>}
            <th className="py-2 pr-3 font-medium">Artifact</th>
            <th className="py-2 font-medium">At</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-b border-rms-line last:border-0" data-testid={`ledger-row-${i}`}>
              <td className="py-2.5 pr-3 font-mono text-xs">{row.stage}</td>
              <td className="py-2.5 pr-3">
                <StatusBadge status={row.decision} />
              </td>
              <td className="py-2.5 pr-3 text-xs text-rms-mute max-w-xs truncate" title={row.reason}>
                {row.reason}
              </td>
              <td className="py-2.5 pr-3">
                <ClassBadge defensibilityClass={row.defensibility_class || row.computed_class} compact />
              </td>
              {showTrace && (
                <td className="py-2.5 pr-3">
                  <Link
                    to={`/trace/${row.trace_id}`}
                    data-testid={`trace-link-${row.trace_id}`}
                    className="font-mono text-xs text-rms-accent hover:underline focus:outline-none focus:ring-2 focus:ring-rms-accent focus:ring-offset-1 rounded"
                  >
                    {row.trace_id.slice(0, 18)}…
                  </Link>
                </td>
              )}
              <td className="py-2.5 pr-3 text-xs text-rms-mute">
                {row.artifact_ref?.artifact_id || '—'}
              </td>
              <td className="py-2.5 text-xs text-rms-mute whitespace-nowrap">
                {row.at ? new Date(row.at).toLocaleString() : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
