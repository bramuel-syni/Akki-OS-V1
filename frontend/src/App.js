import React, { useEffect, useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function StatusPill({ status }) {
  const colour = status === 'pending' ? 'bg-amber-100 text-amber-900 border-amber-300'
    : status === 'passed' ? 'bg-emerald-100 text-emerald-900 border-emerald-300'
    : 'bg-rose-100 text-rose-900 border-rose-300';
  return (
    <span className={`px-2 py-0.5 text-xs font-medium rounded border ${colour}`}>{status}</span>
  );
}

export default function App() {
  const [state, setState] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    let cancelled = false;
    axios.get(`${API}/system/state`)
      .then((r) => { if (!cancelled) setState(r.data); })
      .catch((e) => { if (!cancelled) setErr(e.message); });
    return () => { cancelled = true; };
  }, []);

  return (
    <div className="min-h-full flex flex-col">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-baseline justify-between">
          <div>
            <h1 className="text-xl font-semibold tracking-tight">RMS Intelligence System</h1>
            <p className="text-sm text-rms-mute mt-0.5">Akki / SyniSense / Northena / Solva / Mtafiti / Targeta</p>
          </div>
          <span className="px-3 py-1 text-xs font-mono uppercase tracking-wider rounded bg-rms-ink text-white">Gate G0</span>
        </div>
      </header>

      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-10">
        {err && (
          <div className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3 mb-6">
            Failed to load system state: {err}
          </div>
        )}

        {!state && !err && (
          <div className="text-rms-mute text-sm">Loading system state…</div>
        )}

        {state && (
          <div className="space-y-8">
            <section className="rounded-xl border border-rms-line bg-white p-6">
              <h2 className="text-base font-semibold">Data source</h2>
              <p className="text-sm text-rms-mute mt-1">G0 brief Deliverable 3.c — surface the data-source mode.</p>
              <div className="mt-4 flex items-center gap-3">
                <span className="font-mono text-sm">{state.data_source.name}</span>
                <StatusPill status={state.data_source.running_on_synthetic ? 'pending' : 'live'} />
                <span className="text-xs text-rms-mute">mode: {state.data_source.mode}</span>
              </div>
              {state.data_source.running_on_synthetic && (
                <p className="mt-3 text-xs text-amber-900 bg-amber-50 border border-amber-200 rounded px-3 py-2">
                  Running on synthetic plumbing fixture. V-gates pending. Spec & Build Kickoff: synthetic fixture is a plumbing test only; not a validity proof.
                </p>
              )}
            </section>

            <section className="rounded-xl border border-rms-line bg-white p-6">
              <h2 className="text-base font-semibold">V-gates</h2>
              <p className="text-sm text-rms-mute mt-1">Pending until real RMS material lands and the harnesses run.</p>
              <ul className="mt-4 space-y-2">
                {state.v_gates.map((g) => (
                  <li key={g.id} className="flex items-start justify-between gap-4 py-2 border-t border-rms-line first:border-0">
                    <div>
                      <div className="font-mono text-sm">{g.id} → gates {g.gates}</div>
                      <div className="text-xs text-rms-mute mt-0.5">{g.description}</div>
                    </div>
                    <StatusPill status={g.status} />
                  </li>
                ))}
              </ul>
            </section>

            <section className="rounded-xl border border-rms-line bg-white p-6">
              <h2 className="text-base font-semibold">Frozen contracts</h2>
              <p className="text-sm text-rms-mute mt-1">G0 freeze — invariant tests fail loudly on drift.</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {state.contracts_frozen.map((c) => (
                  <code key={c} className="text-xs px-2 py-1 rounded bg-rms-paper border border-rms-line">{c}</code>
                ))}
                <code className="text-xs px-2 py-1 rounded bg-rms-paper border border-rms-line">
                  qualification_matrix_rev: {state.qualification_matrix_rev}
                </code>
              </div>
            </section>

            <footer className="text-xs text-rms-mute pt-4">
              Server time: <span className="font-mono">{state.time}</span>
            </footer>
          </div>
        )}
      </main>
    </div>
  );
}
