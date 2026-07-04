import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useApi } from '../../hooks/useApi';
import api from '../../apiClient';
import StatusBadge from '../../components/StatusBadge';
import { List, RefreshCw, Search } from 'lucide-react';

export default function RunsPage() {
  const { data: runs, error, loading, refetch } = useApi(() => api.openRuns(), []);
  const { data: northenaStatus } = useApi(() => api.northenaStatus(), []);
  const [filter, setFilter] = useState('');

  const filtered = runs ? runs.filter(r => r.toLowerCase().includes(filter.toLowerCase())) : [];

  return (
    <div data-testid="runs-page" className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold tracking-tight">Runs</h2>
          <p className="text-sm text-rms-mute mt-0.5">
            Northena Ledger — open runs.
            {northenaStatus && (
              <span className="ml-2">
                Retention: <span className="font-mono">{northenaStatus.retention_mode}</span>
              </span>
            )}
          </p>
        </div>
        <button
          onClick={refetch}
          data-testid="refresh-runs-btn"
          className="p-2 rounded-md hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent"
          aria-label="Refresh runs"
        >
          <RefreshCw className="w-4 h-4 text-rms-mute" />
        </button>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-rms-mute" />
        <input
          type="text"
          value={filter}
          onChange={e => setFilter(e.target.value)}
          placeholder="Filter runs…"
          data-testid="runs-filter-input"
          className="w-full pl-9 pr-3 py-2 text-sm border border-rms-line rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-rms-accent focus:border-rms-accent"
        />
      </div>

      {loading && (
        <div data-testid="runs-loading" className="space-y-2">
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className="h-12 rounded-lg bg-white border border-rms-line animate-pulse" />
          ))}
        </div>
      )}

      {error && (
        <div data-testid="runs-error" className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3">
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="flex items-center gap-2 text-xs text-rms-mute">
            <List className="w-3.5 h-3.5" />
            <span>{filtered.length} open run{filtered.length !== 1 ? 's' : ''}</span>
            {filter && <span>({runs.length} total)</span>}
          </div>
          <div className="rounded-xl border border-rms-line bg-white divide-y divide-rms-line">
            {filtered.length === 0 && (
              <p data-testid="runs-empty" className="text-sm text-rms-mute p-4">
                {filter ? 'No runs match your filter.' : 'No open runs.'}
              </p>
            )}
            {filtered.map(runId => (
              <Link
                key={runId}
                to={`/operator/runs/${runId}`}
                data-testid={`run-link-${runId}`}
                className="flex items-center justify-between px-4 py-3 hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-rms-accent"
              >
                <span className="font-mono text-sm">{runId}</span>
                <StatusBadge status="admitted" />
              </Link>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
