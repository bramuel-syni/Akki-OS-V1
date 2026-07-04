import React from 'react';
import { useApi } from '../hooks/useApi';
import api from '../apiClient';
import { Shield, FileText, Hash } from 'lucide-react';

export default function DisciplinePage() {
  const { data: manifest, error, loading } = useApi(() => api.liftManifest(), []);

  if (loading) {
    return (
      <div data-testid="discipline-loading" className="space-y-4">
        {[1, 2, 3].map(i => (
          <div key={i} className="h-24 rounded-xl bg-white border border-rms-line animate-pulse" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div data-testid="discipline-error" className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3">
        {typeof error === 'string' ? error : JSON.stringify(error)}
      </div>
    );
  }

  return (
    <div data-testid="discipline-page" className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Discipline</h2>
        <p className="text-sm text-rms-mute mt-0.5">
          Lift manifest, spec fingerprints, and Rule 2 v2 accounting. Governance-legibility surface.
        </p>
      </div>

      {manifest && (
        <>
          <section data-testid="manifest-meta" className="rounded-xl border border-rms-line bg-white p-5">
            <div className="flex items-center gap-2 mb-3">
              <Shield className="w-4 h-4 text-rms-accent" />
              <h3 className="text-sm font-semibold">Manifest</h3>
            </div>
            <dl className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Version</dt>
                <dd className="font-mono mt-0.5">{manifest.manifest_version}</dd>
              </div>
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Generated</dt>
                <dd className="font-mono mt-0.5 text-xs">{manifest.generated_at?.slice(0, 19)}</dd>
              </div>
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">By</dt>
                <dd className="font-mono mt-0.5 text-xs">{manifest.generated_by}</dd>
              </div>
              <div>
                <dt className="text-xs text-rms-mute uppercase tracking-wide">Entries</dt>
                <dd className="font-mono mt-0.5">{manifest.entries?.length || 0}</dd>
              </div>
            </dl>
          </section>

          {manifest.source_specs && manifest.source_specs.length > 0 && (
            <section data-testid="spec-fingerprints" className="rounded-xl border border-rms-line bg-white p-5">
              <div className="flex items-center gap-2 mb-3">
                <Hash className="w-4 h-4 text-rms-accent" />
                <h3 className="text-sm font-semibold">Source Spec Fingerprints ({manifest.source_specs.length})</h3>
              </div>
              <div className="space-y-2">
                {manifest.source_specs.map((sp, i) => (
                  <div key={i} className="flex items-center gap-3 text-xs py-1.5 border-t border-rms-line first:border-0">
                    <span className="font-medium text-rms-ink min-w-[200px]">{sp.filename}</span>
                    <code className="text-rms-mute font-mono text-[10px] truncate" title={sp.sha256}>
                      {sp.sha256?.slice(0, 16)}…
                    </code>
                  </div>
                ))}
              </div>
            </section>
          )}

          {manifest.phase_accounting && Object.keys(manifest.phase_accounting).length > 0 && (
            <section data-testid="rule2-accounting" className="rounded-xl border border-rms-line bg-white p-5">
              <div className="flex items-center gap-2 mb-3">
                <FileText className="w-4 h-4 text-rms-accent" />
                <h3 className="text-sm font-semibold">Rule 2 v2 Accounting</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="border-b border-rms-line text-left text-rms-mute uppercase tracking-wide">
                      <th className="py-2 pr-3 font-medium">Phase</th>
                      <th className="py-2 pr-3 font-medium">Lifted</th>
                      <th className="py-2 pr-3 font-medium">Discretionary</th>
                      <th className="py-2 pr-3 font-medium">Mandate-forced</th>
                      <th className="py-2 pr-3 font-medium">Overall ratio</th>
                      <th className="py-2 font-medium">Disc. ratio</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(manifest.phase_accounting).map(([phase, acc]) => (
                      <tr key={phase} className="border-b border-rms-line last:border-0">
                        <td className="py-2 pr-3 font-mono font-medium">{phase}</td>
                        <td className="py-2 pr-3 font-mono">{acc.lifted_verifiable ?? '—'}</td>
                        <td className="py-2 pr-3 font-mono">{acc.net_new_discretionary ?? '—'}</td>
                        <td className="py-2 pr-3 font-mono">{acc.mandate_forced_net_new ?? '—'}</td>
                        <td className="py-2 pr-3 font-mono">{acc.overall_ratio ?? '—'}</td>
                        <td className="py-2 font-mono">{acc.discretionary_only_ratio ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {manifest.entries && manifest.entries.length > 0 && (
            <section data-testid="lift-entries" className="rounded-xl border border-rms-line bg-white p-5">
              <h3 className="text-sm font-semibold mb-3">Lift Entries ({manifest.entries.length})</h3>
              <div className="overflow-x-auto max-h-96 overflow-y-auto">
                <table className="w-full text-xs">
                  <thead className="sticky top-0 bg-white">
                    <tr className="border-b border-rms-line text-left text-rms-mute uppercase tracking-wide">
                      <th className="py-2 pr-3 font-medium">Module</th>
                      <th className="py-2 pr-3 font-medium">Kind</th>
                      <th className="py-2 pr-3 font-medium">Resolves by</th>
                      <th className="py-2 font-medium">Notes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {manifest.entries.map((e, i) => (
                      <tr key={i} className="border-b border-rms-line last:border-0 align-top">
                        <td className="py-2 pr-3 font-mono max-w-xs truncate" title={e.module}>{e.module}</td>
                        <td className="py-2 pr-3">
                          <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                            e.lift_kind === 'direct' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                            e.lift_kind === 'transitive' ? 'bg-sky-50 text-sky-700 border border-sky-200' :
                            'bg-amber-50 text-amber-700 border border-amber-200'
                          }`}>
                            {e.lift_kind}
                          </span>
                        </td>
                        <td className="py-2 pr-3 font-mono max-w-xs truncate" title={e.resolves_by?.join(', ')}>
                          {e.resolves_by?.join(', ')}
                        </td>
                        <td className="py-2 text-rms-mute max-w-sm truncate" title={e.notes}>
                          {e.notes}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </>
      )}
    </div>
  );
}
