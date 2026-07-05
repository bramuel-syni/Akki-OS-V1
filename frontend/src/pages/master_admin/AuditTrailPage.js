/**
 * UI Spec §6.3 — Master Admin · What I've changed — audit trail.
 *
 * Verbatim elements per Spec:
 *   * confirmation line for the latest change (plain: what is now in
 *     effect, from when).
 *   * recent actions rows — plain description of the change (from → to
 *     in words), who, when.
 * Rule verbatim: the diff exists in the record; it is never the
 * primary display.
 * Footer binding copy VERBATIM: "Every row carries its full diff. This
 * trail is itself append-only and readable by the regulator surface."
 */
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ScrollText } from 'lucide-react';
import api from '../../apiClient';
import { useAuth } from '../../hooks/useAuth';

function formatWhen(iso) {
  if (!iso) return 'unknown';
  try {
    return new Date(iso).toLocaleString();
  } catch (_e) {
    return iso;
  }
}

function DiffRow({ row, expanded, onToggle, diffPayload }) {
  return (
    <li
      className="border-b border-rms-line last:border-b-0 py-3"
      data-testid={`audit-row-${row.run_id}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="text-sm">
          <div className="text-rms-ink" data-testid={`audit-row-plain-${row.run_id}`}>
            {row.plain_description}
          </div>
          <div className="text-xs text-rms-mute mt-1">
            <span data-testid={`audit-row-who-${row.run_id}`}>
              by {row.grantor_id || 'unknown'}
            </span>
            {' · '}
            <span data-testid={`audit-row-when-${row.run_id}`}>
              {formatWhen(row.at)}
            </span>
          </div>
        </div>
        <button
          type="button"
          onClick={() => onToggle(row.run_id)}
          className="text-xs underline text-rms-mute hover:text-rms-ink whitespace-nowrap"
          data-testid={`audit-row-see-full-diff-${row.run_id}`}
        >
          {expanded ? 'Hide full diff' : 'See full diff'}
        </button>
      </div>
      {expanded && diffPayload && (
        <pre
          className="mt-2 border border-rms-line bg-white rounded p-2 text-xs font-mono overflow-x-auto whitespace-pre"
          data-testid={`audit-row-diff-body-${row.run_id}`}
        >
{JSON.stringify(diffPayload, null, 2)}
        </pre>
      )}
    </li>
  );
}

export default function AuditTrailPage() {
  const { identity } = useAuth();
  const navigate = useNavigate();

  const [actions, setActions] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const [diffCache, setDiffCache] = useState({});
  const [err, setErr] = useState(null);

  const load = useCallback(async () => {
    const r = await api.masterAdminAuditTrail(50);
    if (r.status === 200) {
      setActions(r.body.actions || []);
    } else {
      setErr(`Failed to load audit trail (${r.status}).`);
    }
    setLoaded(true);
  }, []);

  useEffect(() => {
    if (identity === null) return;
    if (identity === false) navigate('/auth/login', { replace: true });
    else load();
  }, [identity, navigate, load]);

  const toggle = async (run_id) => {
    if (expandedId === run_id) {
      setExpandedId(null);
      return;
    }
    setExpandedId(run_id);
    // Lazy-load the full diff on demand — never primary display.
    if (!diffCache[run_id]) {
      const row = actions.find((a) => a.run_id === run_id);
      if (row && row.full_diff_ref) {
        try {
          const resp = await api.northenaLedgerByRunAbs(row.full_diff_ref);
          setDiffCache((prev) => ({ ...prev, [run_id]: resp }));
        } catch (_e) {
          setDiffCache((prev) => ({ ...prev, [run_id]: { error: 'Failed to load diff.' } }));
        }
      }
    }
  };

  if (identity === null) return null;
  const latest = actions[0];

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="master-admin-audit-trail-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/master-admin')}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="audit-trail-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · master admin</div>
              <h1 className="text-lg font-semibold">What I&apos;ve changed</h1>
            </div>
          </div>
          <ScrollText className="w-5 h-5 text-rms-mute" />
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-8 space-y-6">
        {/* §6.3 Confirmation line — latest change. */}
        {latest && (
          <section
            className="border border-emerald-200 bg-emerald-50 rounded p-3 text-sm text-emerald-900"
            data-testid="audit-trail-confirmation-line"
          >
            {latest.plain_description} — recorded {formatWhen(latest.at)}.
          </section>
        )}
        {!latest && loaded && (
          <section className="text-sm text-rms-mute italic" data-testid="audit-trail-empty">
            Nothing recorded yet.
          </section>
        )}

        {/* §6.3 Recent actions rows. */}
        {actions.length > 0 && (
          <section data-testid="audit-trail-recent-actions">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-rms-mute mb-2">Recent actions</h2>
            <ul className="border border-rms-line rounded px-3">
              {actions.map((a) => (
                <DiffRow
                  key={a.run_id}
                  row={a}
                  expanded={expandedId === a.run_id}
                  onToggle={toggle}
                  diffPayload={diffCache[a.run_id]}
                />
              ))}
            </ul>
          </section>
        )}

        {err && (
          <section
            className="text-sm text-red-800 border border-red-200 bg-red-50 rounded p-2"
            data-testid="audit-trail-error"
          >
            {err}
          </section>
        )}

        {/* §6.3 Footer BINDING COPY VERBATIM. */}
        <footer
          className="border-t border-rms-line pt-4 text-sm italic text-rms-ink"
          data-testid="audit-trail-footer-binding-copy"
        >
          Every row carries its full diff. This trail is itself append-only and readable by the regulator surface.
        </footer>
      </main>
    </div>
  );
}
