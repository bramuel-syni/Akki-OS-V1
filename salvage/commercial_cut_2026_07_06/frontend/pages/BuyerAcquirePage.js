/**
 * UI Spec §5.2 — Buyer · Acquire — the governed acquisition.
 *
 * Verbatim elements per Spec:
 *   * framing line (binding copy): "Every acquisition passes the outer gate.
 *     These checks are what make the data lawfully yours to use.";
 *   * four check rows with states — Rights check · Irreversibility transform ·
 *     Cumulative disclosure check · License issue — each with a one-line
 *     plain description.
 *   * Binding copy (footer): "If any check fails, the acquisition is refused
 *     with the reason and a path forward — never partially delivered."
 */
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, ShieldCheck, Check } from 'lucide-react';
import api from '../../apiClient';
import { useAuth } from '../../hooks/useAuth';

const CHECKS = [
  {
    id: 'rights_check',
    label: 'Rights check',
    description: 'Confirm every source in the acquisition holds valid rights for this use.',
  },
  {
    id: 'irreversibility_transform',
    label: 'Irreversibility transform',
    description: 'Apply the transform that removes reversibility from identity categories.',
  },
  {
    id: 'cumulative_disclosure_check',
    label: 'Cumulative disclosure check',
    description: 'Ensure the acquisition cannot be joined to prior deliveries to breach disclosure ceilings.',
  },
  {
    id: 'license_issue',
    label: 'License issue',
    description: 'Issue a license ref binding the acquisition to its scope, expiry, and permitted use.',
  },
];

export default function BuyerAcquirePage() {
  const { identity } = useAuth();
  const navigate = useNavigate();
  const { sessionId } = useParams();
  const [state, setState] = useState(null);
  const [freezeResult, setFreezeResult] = useState(null);
  const [handoffResult, setHandoffResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  const refresh = useCallback(async () => {
    const r = await api.wizardBuyerGet(sessionId);
    if (r.status === 200) setState(r.body);
  }, [sessionId]);

  useEffect(() => {
    if (identity === null) return;
    if (identity === false) {
      navigate('/auth/login', { replace: true });
      return;
    }
    refresh();
  }, [identity, navigate, refresh]);

  const doFreeze = async () => {
    setBusy(true);
    const r = await api.wizardBuyerFreeze(sessionId, {
      license_class: 'external_use',
      lawful_basis_ref: 'buyer-lawful-basis-v0',
    });
    setBusy(false);
    if (r.status === 200) {
      setFreezeResult(r.body);
    } else {
      setErr(r.body);
    }
  };

  const doHandoff = async () => {
    setBusy(true);
    const r = await api.wizardBuyerHandoff(sessionId);
    setBusy(false);
    setHandoffResult({ status: r.status, body: r.body });
  };

  if (identity === null) {
    return <div className="min-h-screen flex items-center justify-center text-rms-mute bg-rms-canvas">Loading…</div>;
  }

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="buyer-acquire-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/buyer/shape')}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="buyer-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · buyer</div>
              <h1 className="text-lg font-semibold">Acquire</h1>
            </div>
          </div>
          <ShieldCheck className="w-5 h-5 text-rms-mute" />
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        {/* Framing line — verbatim binding copy §5.2. */}
        <p
          className="text-base text-rms-ink"
          data-testid="buyer-acquire-framing-copy"
        >
          Every acquisition passes the outer gate. These checks are what make the data lawfully yours to use.
        </p>

        {/* Four check rows. */}
        <section data-testid="buyer-acquire-checks-list">
          <ul className="divide-y divide-rms-line border border-rms-line rounded bg-white">
            {CHECKS.map((c) => (
              <li
                key={c.id}
                className="px-3 py-3 flex items-start gap-3"
                data-testid={`buyer-check-row-${c.id}`}
              >
                <Check className="w-4 h-4 text-emerald-700 mt-0.5" />
                <div>
                  <div className="text-sm font-medium">{c.label}</div>
                  <div className="text-xs text-rms-mute">{c.description}</div>
                </div>
              </li>
            ))}
          </ul>
        </section>

        {/* Freeze + handoff seams — buyer commits before governed admission. */}
        <section className="border-t border-rms-line pt-4 space-y-2">
          <div className="flex gap-2">
            <button
              type="button"
              onClick={doFreeze}
              disabled={busy || freezeResult}
              className="px-3 py-1.5 rounded bg-rms-ink text-white text-sm font-medium disabled:opacity-40"
              data-testid="buyer-freeze-btn"
            >
              Freeze acquisition
            </button>
            <button
              type="button"
              onClick={doHandoff}
              disabled={busy || !freezeResult}
              className="px-3 py-1.5 rounded bg-white text-rms-ink text-sm border border-rms-line disabled:opacity-40"
              data-testid="buyer-handoff-btn"
            >
              Hand off to admission
            </button>
          </div>
          {freezeResult && (
            <div className="text-xs text-emerald-800" data-testid="buyer-freeze-result">
              Frozen. session_id={freezeResult.session_id} · ledger_run_id={freezeResult.ledger_run_id}
            </div>
          )}
          {handoffResult && (
            <div className="text-xs text-emerald-800" data-testid="buyer-handoff-result">
              Admission: HTTP {handoffResult.status}
              {handoffResult.body.trace_id && ` · trace_id=${handoffResult.body.trace_id}`}
            </div>
          )}
          {err && (
            <div className="text-xs text-red-700" data-testid="buyer-acquire-error">
              {JSON.stringify(err)}
            </div>
          )}
          {handoffResult && handoffResult.status === 202 && (
            <button
              type="button"
              onClick={() => navigate(`/buyer/receive/${sessionId}`)}
              className="mt-2 px-3 py-1.5 rounded bg-emerald-100 text-emerald-900 text-sm border border-emerald-200"
              data-testid="buyer-goto-receive"
            >
              Proceed to receive
            </button>
          )}
        </section>

        {/* Footer binding copy — verbatim §5.2. */}
        <footer
          className="border-t border-rms-line pt-4 text-sm italic text-rms-mute"
          data-testid="buyer-acquire-footer-binding-copy"
        >
          If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered.
        </footer>

        {state && (
          <div className="text-xs font-mono text-rms-mute" data-testid="buyer-acquire-session-tag">
            session_id={state.session_id}
          </div>
        )}
      </main>
    </div>
  );
}
