import React from 'react';
import { useApi } from '../hooks/useApi';
import api from '../apiClient';
import StatusBadge from '../components/StatusBadge';
import { AlertTriangle, Database, Lock, Layers } from 'lucide-react';

export default function OperatorDashboard() {
  const { data: state, error, loading } = useApi(() => api.systemState(), []);

  if (loading) {
    return (
      <div data-testid="operator-loading" className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="h-32 rounded-xl bg-white border border-rms-line animate-pulse" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div data-testid="operator-error" className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3">
        Failed to load system state: {typeof error === 'string' ? error : JSON.stringify(error)}
      </div>
    );
  }

  const hasExceptions = state.data_source?.running_on_synthetic || state.v1_pending || state.v3_pending;

  return (
    <div data-testid="operator-dashboard" className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Portfolio Overview</h2>
        <p className="text-sm text-rms-mute mt-0.5">System state, data source posture, governance gates.</p>
      </div>

      {hasExceptions && (
        <div data-testid="exceptions-banner" className="rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 flex items-start gap-3">
          <AlertTriangle className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-amber-900">
            <span className="font-medium">Attention required.</span>
            {state.data_source?.running_on_synthetic && ' Running on synthetic data — V-gates pending.'}
            {state.v1_pending && ' V1 awaiting real material.'}
            {state.v3_pending && ' V3 awaiting real labelled set.'}
          </div>
        </div>
      )}

      <section data-testid="data-source-section" className="rounded-xl border border-rms-line bg-white p-5">
        <div className="flex items-center gap-2 mb-3">
          <Database className="w-4 h-4 text-rms-accent" />
          <h3 className="text-sm font-semibold">Data Source</h3>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <span className="font-mono">{state.data_source?.name}</span>
          <StatusBadge status={state.data_source?.running_on_synthetic ? 'synthetic' : 'live'} />
          <span className="text-xs text-rms-mute">mode: {state.data_source?.mode}</span>
        </div>
        {state.data_source?.running_on_synthetic && (
          <p className="mt-2 text-xs text-amber-900 bg-amber-50 border border-amber-200 rounded px-3 py-2">
            Running on synthetic plumbing fixture. Not a validity proof. V-gates pending until real RMS material lands.
          </p>
        )}
        {state.data_source?.rms_adversarial_v1 && (
          <div className="mt-2 text-xs text-rms-mute">
            Fixture: <span className="font-mono">{state.data_source.rms_adversarial_v1.fixture}</span>
            {' · '}{state.data_source.rms_adversarial_v1.unit_count} units
          </div>
        )}
      </section>

      <section data-testid="vgates-section" className="rounded-xl border border-rms-line bg-white p-5">
        <div className="flex items-center gap-2 mb-3">
          <Lock className="w-4 h-4 text-rms-accent" />
          <h3 className="text-sm font-semibold">V-Gates</h3>
        </div>
        <ul className="space-y-2">
          {state.v_gates?.map(g => (
            <li key={g.id} className="flex items-start justify-between gap-4 py-2 border-t border-rms-line first:border-0">
              <div>
                <div className="font-mono text-sm">{g.id} <span className="text-rms-mute">→ gates {g.gates}</span></div>
                <div className="text-xs text-rms-mute mt-0.5">{g.description}</div>
              </div>
              <StatusBadge status={g.status} />
            </li>
          ))}
        </ul>
      </section>

      <section data-testid="contracts-section" className="rounded-xl border border-rms-line bg-white p-5">
        <div className="flex items-center gap-2 mb-3">
          <Layers className="w-4 h-4 text-rms-accent" />
          <h3 className="text-sm font-semibold">Frozen Contracts ({state.contracts_frozen?.length || 0})</h3>
        </div>
        <div className="flex flex-wrap gap-2">
          {state.contracts_frozen?.map(c => (
            <code key={c} className="text-xs px-2 py-1 rounded bg-rms-paper border border-rms-line">{c}</code>
          ))}
        </div>
      </section>

      {state.closed_seams && state.closed_seams.length > 0 && (
        <section data-testid="closed-seams-section" className="rounded-xl border border-rms-line bg-white p-5">
          <h3 className="text-sm font-semibold mb-3">Closed Seams</h3>
          <ul className="space-y-1">
            {state.closed_seams.map((s, i) => (
              <li key={i} className="text-xs text-rms-mute font-mono py-1 border-t border-rms-line first:border-0">
                {s}
              </li>
            ))}
          </ul>
        </section>
      )}

      <div data-testid="system-time" className="text-xs text-rms-mute">
        Server time: <span className="font-mono">{state.time?.slice(0, 19)}</span>
        {' · '}Gate: <span className="font-mono">{state.gate}</span>
      </div>
    </div>
  );
}
