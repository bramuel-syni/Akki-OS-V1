/**
 * UI Spec §5.1 — Buyer · Shape — buyer objective wizard.
 *
 * Verbatim elements per Spec:
 *   * Layout: chat pane + "Your acquisition" rail.
 *   * Chat: buyer states need; agent may propose shapes and price levers;
 *     estate-check chip inline.
 *   * Rail: reach; output (form · grain · standard); license; price card —
 *     "Estimated price", figure, qualifying volume, binding copy "moves as
 *     you shape"; delivery estimate beside price; feasible-and-offerable line.
 *   * Rules: shaping is bounded by offerability; out-of-bounds shapes are
 *     refused with the reason; buyer never sets lawful basis.
 *
 * Owner Condition 3 (D4b Block 3): §5 dual-delta on buyer rail —
 * {price_delta, class_delta} MUST render as a PAIR per E6
 * Visibility-not-prohibition. Backend enforcement already exists;
 * surface shows both together.
 */
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShoppingCart, ArrowLeft, Check } from 'lucide-react';
import api, { formatApiErrorDetail } from '../../apiClient';
import { useAuth } from '../../hooks/useAuth';

function EstateCheckChip({ snapshotRef }) {
  if (!snapshotRef) return null;
  return (
    <span
      data-testid="buyer-estate-check-chip"
      className="inline-flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider text-emerald-800 bg-emerald-50 border border-emerald-200 rounded-full px-2 py-0.5"
    >
      <Check className="w-3 h-3" />
      estate-check · {String(snapshotRef).slice(0, 24)}
    </span>
  );
}

/**
 * DualDeltaPair — Owner Condition 3 verbatim: {price_delta, class_delta}
 * rendered together as a PAIR. Never one without the other on the buyer rail.
 * Backend surfaces both; the surface visualises both. Missing either is
 * a §5 rendering-completeness defect (Owner E6 Visibility-not-prohibition).
 */
function DualDeltaPair({ priceDelta, classDelta }) {
  const bothPresent = priceDelta != null && classDelta != null;
  return (
    <div
      data-testid="buyer-dual-delta-pair"
      className="border border-amber-200 bg-amber-50 rounded p-2 space-y-1"
    >
      <div className="text-xs uppercase tracking-wider text-amber-800">
        proposal deltas (paired)
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div data-testid="buyer-dual-delta-price">
          <span className="text-rms-mute text-xs">price_delta</span>
          <div className="font-mono">{priceDelta != null ? priceDelta : '—'}</div>
        </div>
        <div data-testid="buyer-dual-delta-class">
          <span className="text-rms-mute text-xs">class_delta</span>
          <div className="font-mono">{classDelta != null ? classDelta : '—'}</div>
        </div>
      </div>
      {!bothPresent && (
        <div className="text-xs italic text-amber-800" data-testid="buyer-dual-delta-note">
          Both deltas rendered together per E6 Visibility-not-prohibition.
        </div>
      )}
    </div>
  );
}

export default function BuyerShapePage() {
  const { identity } = useAuth();
  const navigate = useNavigate();
  const [sid, setSid] = useState(null);
  const [wizardState, setWizardState] = useState(null);
  const [turns, setTurns] = useState([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const [proposals, setProposals] = useState([]);

  const refreshState = useCallback(async (sessionId) => {
    const r = await api.wizardBuyerGet(sessionId);
    if (r.status === 200) setWizardState(r.body);
  }, []);

  const startSession = useCallback(async () => {
    setBusy(true);
    const r = await api.wizardBuyerStart();
    setBusy(false);
    if (r.status !== 201) {
      setErr({ status: r.status, body: r.body });
      return;
    }
    setSid(r.body.session_id);
    const t = await api.wizardBuyerTurn(r.body.session_id, {});
    if (t.status === 200) setTurns([t.body]);
    await refreshState(r.body.session_id);
  }, [refreshState]);

  useEffect(() => {
    if (identity === null) return;
    if (identity === false) {
      navigate('/auth/login', { replace: true });
      return;
    }
    if (!sid) startSession();
  }, [identity, sid, startSession, navigate]);

  const submitTurn = async () => {
    if (!sid || !turns[turns.length - 1]) return;
    setBusy(true);
    const lastTurn = turns[turns.length - 1];
    const r = await api.wizardBuyerTurn(sid, {
      turn_ref: lastTurn.turn_ref,
      user_content: input,
    });
    setBusy(false);
    if (r.status === 200) {
      setTurns((prev) => [...prev, r.body]);
      setInput('');
      await refreshState(sid);
    } else {
      setErr({ status: r.status, body: r.body });
    }
  };

  const emitTestProposal = async () => {
    // Illustrative dual-delta proposal — real proposals arise mid-conversation
    // via agent-lever pulls per §5.1 Rules; this button is a UI-testable seam.
    if (!sid) return;
    const r = await api.wizardBuyerPropose(sid, {
      axes_changed: ['output.standard'],
      price_delta: 'cuts price by 38%',
      class_delta: 'lowers to recorded_statement',
      proposal_content: 'Narrowing to last 5 years cuts price by 38%.',
    });
    if (r.status === 200) {
      setProposals((prev) => [...prev, r.body]);
      await refreshState(sid);
    }
  };

  if (identity === null) {
    return <div className="min-h-screen bg-rms-canvas flex items-center justify-center text-rms-mute">Loading…</div>;
  }

  const committed = (wizardState && wizardState.committed_values) || {};
  const priceEstimate = committed['envelope.budget']?.value || 'moves as you shape';
  const licenseClass = wizardState?.license_class || null;

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="buyer-shape-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="buyer-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · buyer</div>
              <h1 className="text-lg font-semibold">Shape your acquisition</h1>
            </div>
          </div>
          <ShoppingCart className="w-5 h-5 text-rms-mute" />
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: chat pane */}
        <section className="lg:col-span-2 space-y-4" data-testid="buyer-chat-pane">
          <div className="space-y-3">
            {turns.map((t) => (
              <div key={t.turn_ref} data-testid={`buyer-chat-turn-${t.turn_ref}`}>
                {t.feasibility_snapshot_ref && (
                  <div className="mb-1">
                    <EstateCheckChip snapshotRef={t.feasibility_snapshot_ref} />
                  </div>
                )}
                <div className="border border-rms-line bg-white rounded p-3 text-sm">
                  {t.agent_content || '…'}
                </div>
              </div>
            ))}
          </div>
          <div className="border-t border-rms-line pt-3">
            <textarea
              rows={2}
              className="w-full border border-rms-line rounded p-2 text-sm"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={busy || !sid}
              placeholder="State what you need to acquire…"
              data-testid="buyer-shape-input"
            />
            <div className="flex gap-2 mt-2">
              <button
                type="button"
                onClick={submitTurn}
                disabled={busy || !sid}
                className="px-3 py-1.5 rounded bg-rms-ink text-white text-sm font-medium disabled:opacity-40"
                data-testid="buyer-shape-submit"
              >
                Send
              </button>
              <button
                type="button"
                onClick={emitTestProposal}
                disabled={busy || !sid}
                className="px-3 py-1.5 rounded bg-amber-100 text-amber-900 text-sm border border-amber-200 disabled:opacity-40"
                data-testid="buyer-emit-proposal"
                title="Illustrative: emits an agent proposal with dual-delta."
              >
                Emit proposal (illus.)
              </button>
              <button
                type="button"
                onClick={() => navigate(`/buyer/acquire/${sid}`)}
                disabled={!sid}
                className="px-3 py-1.5 rounded bg-white text-rms-ink text-sm border border-rms-line disabled:opacity-40"
                data-testid="buyer-goto-acquire"
              >
                Proceed to acquire
              </button>
            </div>
          </div>
          {err && (
            <div className="text-sm text-red-700" data-testid="buyer-shape-error">
              {formatApiErrorDetail(err.body && err.body.detail ? err.body.detail : err.body)}
            </div>
          )}
        </section>

        {/* Right: "Your acquisition" rail */}
        <aside data-testid="buyer-acquisition-rail" className="space-y-3">
          <div className="border border-rms-line bg-white rounded p-3 space-y-2">
            <h2 className="text-sm font-semibold text-rms-ink">Your acquisition</h2>
            <ul className="text-sm space-y-1">
              <li data-testid="buyer-rail-reach">
                Reach: <span className="font-mono text-xs text-rms-mute">
                  {committed.reach?.value ? JSON.stringify(committed.reach.value) : '— open'}
                </span>
              </li>
              <li data-testid="buyer-rail-output-form">
                Output · form: <span className="font-mono text-xs text-rms-mute">
                  {committed['output.form']?.value || '— open'}
                </span>
              </li>
              <li data-testid="buyer-rail-output-grain">
                Output · grain: <span className="font-mono text-xs text-rms-mute">
                  {committed['output.grain']?.value || '— open'}
                </span>
              </li>
              <li data-testid="buyer-rail-output-standard">
                Output · standard: <span className="font-mono text-xs text-rms-mute">
                  {committed['output.standard']?.value || '— open'}
                </span>
              </li>
              <li data-testid="buyer-rail-license-class">
                License: <span className="font-mono text-xs text-rms-mute">
                  {licenseClass || '— derived on freeze'}
                </span>
              </li>
            </ul>
          </div>

          {/* §5.1 price card. */}
          <div
            className="border border-rms-line bg-white rounded p-3"
            data-testid="buyer-price-card"
          >
            <div className="text-xs uppercase tracking-wide text-rms-mute mb-1">Estimated price</div>
            <div className="text-2xl font-semibold" data-testid="buyer-price-figure">
              {typeof priceEstimate === 'number' ? `$${priceEstimate}` : priceEstimate}
            </div>
            <div
              className="text-xs italic text-rms-mute mt-1"
              data-testid="buyer-price-moves-as-you-shape"
            >
              moves as you shape
            </div>
            <div className="text-xs mt-1" data-testid="buyer-delivery-estimate">
              Delivery: served-from-qualified · fast
            </div>
            <div className="text-xs text-emerald-800 mt-1" data-testid="buyer-feasible-line">
              Feasible-and-offerable.
            </div>
          </div>

          {/* Dual-delta pair — Owner Condition 3 verbatim visibility */}
          {proposals.length > 0 && (
            <div data-testid="buyer-dual-delta-container">
              {proposals.map((p) => (
                <DualDeltaPair
                  key={p.proposal_id}
                  priceDelta={p.price_delta}
                  classDelta={p.class_delta}
                />
              ))}
            </div>
          )}
        </aside>
      </main>
    </div>
  );
}
