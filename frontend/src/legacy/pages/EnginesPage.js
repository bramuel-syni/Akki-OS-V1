import React from 'react';
import { useApi } from '../../hooks/useApi';
import api from '../../apiClient';
import EngineCard from '../../components/EngineCard';

export default function EnginesPage() {
  const { data: v1, loading: v1L } = useApi(() => api.v1Status(), []);
  const { data: v3, loading: v3L } = useApi(() => api.v3Status(), []);
  const { data: solva, loading: solvaL } = useApi(() => api.solvaStatus(), []);
  const { data: svc1, loading: svc1L } = useApi(() => api.service1Status(), []);
  const { data: northena, loading: northenaL } = useApi(() => api.northenaStatus(), []);

  const loading = v1L || v3L || solvaL || svc1L || northenaL;

  return (
    <div data-testid="engines-page" className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Engines</h2>
        <p className="text-sm text-rms-mute mt-0.5">
          Status of each engine in the 5-engine universe: Northena, Solva, Mtafiti, Targeta, Service 1.
        </p>
      </div>

      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className="h-32 rounded-lg bg-white border border-rms-line animate-pulse" />
          ))}
        </div>
      )}

      {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {northena && (
            <EngineCard
              title="Northena Ledger"
              gate={northena.gate}
              note={northena.note}
              data={{
                'Retention mode': northena.retention_mode,
                'Retention window': northena.retention_window_days || 'indefinite',
                'Open runs': northena.open_runs_count,
              }}
            />
          )}
          {solva && (
            <EngineCard
              title="Solva"
              gate={solva.gate}
              note={solva.note}
              data={{
                'Reasoning stages': solva.reasoning_stages?.join(', '),
              }}
            />
          )}
          {svc1 && (
            <EngineCard
              title="Service 1"
              gate={svc1.gate}
              note={svc1.note}
              data={{
                'Service': svc1.service,
                'Closed seams': svc1.closed_seams?.join(', ') || 'none',
              }}
            />
          )}
          {v1 && (
            <EngineCard
              title="V1 Harness"
              gate="G0.5"
              note={v1.notes?.[0]}
              data={{
                'Verdict': v1.verdict,
                'Last run': v1.last_run_at || 'never',
              }}
            />
          )}
          {v3 && (
            <EngineCard
              title="V3 Harness"
              gate="G1"
              note={v3.notes?.[0]}
              data={{
                'Verdict': v3.verdict,
                'Last run': v3.last_run_at || 'never',
                'Gates': v3.gates ? Object.entries(v3.gates).map(([k, v]) => `${k}: ${v}`).join(', ') : '—',
              }}
            />
          )}
        </div>
      )}
    </div>
  );
}
