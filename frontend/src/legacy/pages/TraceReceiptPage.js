import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useApi } from '../../hooks/useApi';
import api from '../../apiClient';
import LedgerTable from '../../components/LedgerTable';
import ClassBadge from '../../components/ClassBadge';
import StatusBadge from '../../components/StatusBadge';
import { ArrowLeft, Layers, Search, ChevronDown, ChevronRight } from 'lucide-react';

function Collapsible({ title, badge, defaultOpen = false, testId, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div data-testid={testId} className="border border-rms-line rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-2 px-4 py-3 text-sm font-medium bg-white hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-rms-accent"
        data-testid={`${testId}-toggle`}
      >
        {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        <span>{title}</span>
        {badge && <span className="ml-auto">{badge}</span>}
      </button>
      {open && <div className="border-t border-rms-line p-4 bg-white">{children}</div>}
    </div>
  );
}

function SolvaTraceView({ trace }) {
  return (
    <div data-testid="solva-trace-item" className="space-y-2 text-sm">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="font-mono text-xs text-rms-mute">{trace.unit_id || trace.trace_id}</span>
        {trace.computed_class && <ClassBadge defensibilityClass={trace.computed_class} />}
        {trace.decision && <StatusBadge status={trace.decision} />}
      </div>
      {trace.conclusion && (
        <p className="text-xs text-rms-mute">{trace.conclusion}</p>
      )}
      {trace.stages && trace.stages.length > 0 && (
        <div className="text-xs space-y-1">
          <span className="text-rms-mute font-medium">Reasoning stages:</span>
          <div className="flex flex-wrap gap-1.5">
            {trace.stages.map((s, i) => (
              <span key={i} className="px-1.5 py-0.5 bg-rms-paper border border-rms-line rounded font-mono">
                {s.stage_name || s.stage || `stage-${i}`}
              </span>
            ))}
          </div>
        </div>
      )}
      {trace.load_bearing_unit_ids && trace.load_bearing_unit_ids.length > 0 && (
        <div className="text-xs text-rms-mute">
          Load-bearing units: <span className="font-mono">{trace.load_bearing_unit_ids.join(', ')}</span>
        </div>
      )}
    </div>
  );
}

function MiningPlanView({ plan }) {
  return (
    <div data-testid="mining-plan-item" className="space-y-2 text-sm">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="font-mono text-xs">{plan.plan_id}</span>
        <span className="text-xs text-rms-mute">mode: {plan.mode}</span>
        <span className="text-xs text-rms-mute">yield: {plan.yield_layer_version}</span>
      </div>
      {plan.defensibility_floor && (
        <div className="text-xs text-rms-mute">
          Floor: <span className="font-mono">{JSON.stringify(plan.defensibility_floor)}</span>
        </div>
      )}
      {plan.ordered_targets && (
        <div className="text-xs text-rms-mute">
          Targets: {plan.ordered_targets.length} locations
        </div>
      )}
    </div>
  );
}

function RegistryRecordView({ record }) {
  return (
    <div data-testid="registry-record-item" className="flex items-center gap-3 text-sm">
      <span className="font-mono text-xs">{record.source_ref?.slice(0, 30) || '—'}</span>
      {record.defensibility_class && <ClassBadge defensibilityClass={record.defensibility_class} compact />}
      <span className="text-xs text-rms-mute">{record.region}</span>
      <span className="text-xs text-rms-mute font-mono">{record.defensibility_runtime_mode}</span>
    </div>
  );
}

function TraceSearch() {
  const [input, setInput] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) navigate(`/trace/${input.trim()}`);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2" data-testid="trace-search-form">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-rms-mute" />
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Enter trace_id…"
          data-testid="trace-search-input"
          className="w-full pl-9 pr-3 py-2 text-sm border border-rms-line rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-rms-accent focus:border-rms-accent"
        />
      </div>
      <button
        type="submit"
        data-testid="trace-search-btn"
        className="px-4 py-2 text-sm font-medium bg-rms-ink text-white rounded-lg hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent focus:ring-offset-1"
      >
        Resolve
      </button>
    </form>
  );
}

export default function TraceReceiptPage() {
  const { traceId } = useParams();
  const { data: envelope, error, loading } = useApi(
    () => api.traceLens(traceId),
    [traceId]
  );

  if (!traceId) {
    return (
      <div data-testid="trace-receipt-search" className="space-y-6">
        <h2 className="text-lg font-semibold">Trust Receipt — Trace Lens</h2>
        <p className="text-sm text-rms-mute">Resolve a trace_id to its full cross-engine record.</p>
        <TraceSearch />
      </div>
    );
  }

  return (
    <div data-testid="trace-receipt-page" className="space-y-6">
      <div className="flex items-center gap-3">
        <Link
          to="/operator/runs"
          data-testid="back-from-trace"
          className="p-1.5 rounded-md hover:bg-gray-100 transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent"
          aria-label="Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </Link>
        <div>
          <h2 className="text-lg font-semibold tracking-tight">Trust Receipt</h2>
          <p className="text-sm text-rms-mute font-mono">{traceId}</p>
        </div>
      </div>

      <TraceSearch />

      {loading && (
        <div data-testid="trace-loading" className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-20 rounded-lg bg-white border border-rms-line animate-pulse" />
          ))}
        </div>
      )}

      {error && (
        <div data-testid="trace-error" className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3 text-sm">
          {typeof error === 'object' ? (
            <>
              {error.reason && <span className="font-mono">{error.reason}: </span>}
              {error.message || JSON.stringify(error)}
            </>
          ) : error}
        </div>
      )}

      {!loading && !error && envelope && (
        <>
          <section data-testid="trace-summary" className="rounded-xl border border-rms-line bg-white p-5">
            <div className="flex items-center gap-2 mb-4">
              <Layers className="w-4 h-4 text-rms-accent" />
              <h3 className="text-sm font-semibold">Envelope Summary</h3>
            </div>
            <dl className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Resolved at</dt>
                <dd className="font-mono mt-0.5 text-xs">{envelope.resolved_at?.slice(0, 19)}</dd>
              </div>
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Run IDs</dt>
                <dd className="mt-0.5">
                  {envelope.run_ids?.map(rid => (
                    <Link
                      key={rid}
                      to={`/operator/runs/${rid}`}
                      className="block font-mono text-xs text-rms-accent hover:underline"
                      data-testid={`envelope-run-link-${rid}`}
                    >
                      {rid}
                    </Link>
                  ))}
                </dd>
              </div>
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Engines Touched</dt>
                <dd className="mt-0.5 flex flex-wrap gap-1">
                  {envelope.engines_touched?.map(e => (
                    <span key={e} className="text-[10px] font-mono px-1.5 py-0.5 bg-rms-paper border border-rms-line rounded">{e}</span>
                  ))}
                </dd>
              </div>
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Snapshot Pinned</dt>
                <dd className="font-mono mt-0.5 text-xs">{envelope.registry_freshness?.snapshot_pinned ? 'Yes' : 'No'}</dd>
              </div>
            </dl>
          </section>

          <Collapsible
            title={`Ledger Rows (${envelope.ledger_rows?.length || 0})`}
            testId="trace-ledger-section"
            defaultOpen={true}
          >
            <LedgerTable rows={envelope.ledger_rows} showTrace={false} />
          </Collapsible>

          {envelope.solva_traces && envelope.solva_traces.length > 0 && (
            <Collapsible
              title={`Solva Traces (${envelope.solva_traces.length})`}
              testId="trace-solva-section"
              badge={<span className="text-[10px] font-mono px-1.5 py-0.5 bg-sky-50 border border-sky-200 rounded text-sky-700">reasoning</span>}
            >
              <div className="space-y-4 divide-y divide-rms-line">
                {envelope.solva_traces.map((st, i) => (
                  <div key={i} className={i > 0 ? 'pt-4' : ''}>
                    <SolvaTraceView trace={st} />
                  </div>
                ))}
              </div>
            </Collapsible>
          )}

          {envelope.mining_plans && envelope.mining_plans.length > 0 && (
            <Collapsible
              title={`Mining Plans (${envelope.mining_plans.length})`}
              testId="trace-plans-section"
            >
              <div className="space-y-4 divide-y divide-rms-line">
                {envelope.mining_plans.map((mp, i) => (
                  <div key={i} className={i > 0 ? 'pt-4' : ''}>
                    <MiningPlanView plan={mp} />
                  </div>
                ))}
              </div>
            </Collapsible>
          )}

          {envelope.registry_records && envelope.registry_records.length > 0 && (
            <Collapsible
              title={`Registry Records (${envelope.registry_records.length})`}
              testId="trace-registry-section"
            >
              <div className="space-y-2">
                {envelope.registry_records.map((rr, i) => (
                  <RegistryRecordView key={i} record={rr} />
                ))}
              </div>
            </Collapsible>
          )}
        </>
      )}
    </div>
  );
}
