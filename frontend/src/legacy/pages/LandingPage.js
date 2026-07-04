import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, ArrowRight, Activity } from 'lucide-react';
import { useApi } from '../../hooks/useApi';
import api from '../../apiClient';

export default function LandingPage() {
  const { data: health, loading } = useApi(() => api.health(), []);

  return (
    <div data-testid="landing-page" className="space-y-8">
      <div className="text-center pt-4">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-rms-ink mb-4">
          <Shield className="w-6 h-6 text-white" />
        </div>
        <h2 className="text-2xl font-semibold tracking-tight text-rms-ink">
          Governed intelligence you can act on and defend.
        </h2>
        <p className="mt-2 text-sm text-rms-mute max-w-lg mx-auto">
          Every answer carries its own defensibility — what it may be asserted as,
          why, and the full accountable record. Trust is progressive: calm by default,
          depth on reach.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-2xl mx-auto">
        <Link
          to="/operator"
          data-testid="enter-operator"
          className="group rounded-xl border border-rms-line bg-white p-5 hover:border-rms-accent transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent"
        >
          <div className="flex items-center gap-3 mb-2">
            <Activity className="w-5 h-5 text-rms-accent" />
            <span className="text-sm font-semibold">Operator Console</span>
            <ArrowRight className="w-4 h-4 ml-auto text-rms-mute group-hover:text-rms-accent transition-colors" />
          </div>
          <p className="text-xs text-rms-mute">
            Exception-first monitoring. Portfolio, runs, sources, discipline — what needs your attention, when it needs you.
          </p>
        </Link>
        <div className="rounded-xl border border-rms-line bg-white p-5 opacity-60">
          <div className="flex items-center gap-3 mb-2">
            <Shield className="w-5 h-5 text-rms-mute" />
            <span className="text-sm font-semibold text-rms-mute">Consumer Terminal</span>
            <span className="ml-auto text-[10px] font-mono px-1.5 py-0.5 bg-rms-line rounded">v0</span>
          </div>
          <p className="text-xs text-rms-mute">
            Trust-receipt viewer. Resolve any trace_id to its full cross-engine record.
            Access via <code className="bg-rms-paper px-1 rounded">/trace/:traceId</code>
          </p>
        </div>
      </div>

      {!loading && health && (
        <div data-testid="health-summary" className="text-center text-xs text-rms-mute pt-2">
          System: <span className="font-mono">{health.status}</span>
          {' · '}
          <span className="font-mono">{health.time?.slice(0, 19)}</span>
        </div>
      )}
    </div>
  );
}
