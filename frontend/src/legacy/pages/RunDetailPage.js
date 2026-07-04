import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useApi } from '../../hooks/useApi';
import api from '../../apiClient';
import LedgerTable from '../../components/LedgerTable';
import { ArrowLeft, FileText } from 'lucide-react';

export default function RunDetailPage() {
  const { runId } = useParams();
  const { data: rows, error, loading } = useApi(() => api.ledgerByRun(runId), [runId]);

  const traceIds = rows ? [...new Set(rows.map(r => r.trace_id))] : [];

  return (
    <div data-testid="run-detail-page" className="space-y-6">
      <div className="flex items-center gap-3">
        <Link
          to="/operator/runs"
          data-testid="back-to-runs"
          className="p-1.5 rounded-md hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent"
          aria-label="Back to runs"
        >
          <ArrowLeft className="w-4 h-4" />
        </Link>
        <div>
          <h2 className="text-lg font-semibold tracking-tight">Run Detail</h2>
          <p className="text-sm text-rms-mute font-mono">{runId}</p>
        </div>
      </div>

      {traceIds.length > 0 && (
        <div data-testid="trace-links" className="flex items-center gap-2 flex-wrap">
          <FileText className="w-4 h-4 text-rms-accent" />
          <span className="text-xs text-rms-mute">Trace receipts:</span>
          {traceIds.map(tid => (
            <Link
              key={tid}
              to={`/trace/${tid}`}
              data-testid={`run-trace-link-${tid}`}
              className="text-xs font-mono text-rms-accent hover:underline focus:outline-none focus:ring-2 focus:ring-rms-accent rounded px-1"
            >
              {tid}
            </Link>
          ))}
        </div>
      )}

      {loading && (
        <div data-testid="run-detail-loading" className="space-y-2">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-10 rounded-lg bg-white border border-rms-line animate-pulse" />
          ))}
        </div>
      )}

      {error && (
        <div data-testid="run-detail-error" className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      {!loading && !error && (
        <section className="rounded-xl border border-rms-line bg-white p-5">
          <h3 className="text-sm font-semibold mb-3">
            Ledger Rows ({rows?.length || 0})
          </h3>
          <LedgerTable rows={rows} />
        </section>
      )}

      {!loading && !error && rows && rows.length > 0 && rows[0].artifact_ref && (
        <section data-testid="artifact-section" className="rounded-xl border border-rms-line bg-white p-5">
          <h3 className="text-sm font-semibold mb-3">Governing Artifact</h3>
          <dl className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
            <div>
              <dt className="text-xs text-rms-mute uppercase tracking-wide">Type</dt>
              <dd className="font-mono mt-0.5">{rows[0].artifact_ref.artifact_type}</dd>
            </div>
            <div>
              <dt className="text-xs text-rms-mute uppercase tracking-wide">ID</dt>
              <dd className="font-mono mt-0.5">{rows[0].artifact_ref.artifact_id}</dd>
            </div>
            <div>
              <dt className="text-xs text-rms-mute uppercase tracking-wide">Version</dt>
              <dd className="font-mono mt-0.5">{rows[0].artifact_ref.version}</dd>
            </div>
            <div>
              <dt className="text-xs text-rms-mute uppercase tracking-wide">Lawful Basis</dt>
              <dd className="font-mono mt-0.5">{rows[0].lawful_basis_ref}</dd>
            </div>
          </dl>
        </section>
      )}
    </div>
  );
}
