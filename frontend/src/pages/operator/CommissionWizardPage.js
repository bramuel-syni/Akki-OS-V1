/**
 * CommissionWizardPage — UI Spec v1 §2.2 verbatim.
 *
 * Layout (§2.2):
 *   * Chat pane (left) + Objective draft rail (right).
 *
 * Chat (§2.2):
 *   * Operator states intent; agent asks for operator-mandatory fields,
 *     never proposes on them.
 *   * Estate-check chip renders inline before a feasibility-dependent
 *     question (illustrative example from §2.2:
 *     "4,180 hours match · 62% recorded statement · 21% established fact").
 *
 * Draft rail (§2.2):
 *   * Three dimensions + envelope with three visual states —
 *     filled (check), open (muted "— open"), agent-assumed (amber chip).
 *   * Envelope line lists done-condition · budget · lawful basis until supplied.
 *
 * Rules (§2.2):
 *   * Mandatory fields (reach, output×4, done-condition, budget, lawful basis)
 *     are asked, never pre-filled.
 *   * Preference fields may carry agent recommendations.
 *   * Every turn is grounded in a real estate read — no fabricated availability.
 *
 * Wizard endpoint consumers (Phase 7 B-1/B-2/B-3):
 *   * POST /api/wizard/operator/session   — start
 *   * POST /api/wizard/operator/{sid}/turn — advance
 *   * POST /api/wizard/operator/{sid}/commit-review — pre-freeze
 *   * (Freeze is on §2.3 CommitReviewPage.)
 */
import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Loader2, Check } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import api, { formatApiErrorDetail } from '../../apiClient';
import { AuthDeniedNotice } from '../../components/ui_spec_v1';

const MANDATORY_FIELDS = [
  { key: 'reach', label: 'Reach' },
  { key: 'output.form', label: 'Output · form' },
  { key: 'output.consumer', label: 'Output · consumer' },
  { key: 'output.grain', label: 'Output · grain' },
  { key: 'output.standard', label: 'Output · standard' },
  { key: 'envelope.done_condition', label: 'Done condition' },
  { key: 'envelope.budget', label: 'Budget' },
  { key: 'envelope.lawful_basis', label: 'Lawful basis' },
];

function EstateCheckChip({ ref }) {
  if (!ref) return null;
  return (
    <span
      data-testid="estate-check-chip"
      className="inline-flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider text-emerald-800 bg-emerald-50 border border-emerald-200 rounded-full px-2 py-0.5"
    >
      <Check className="w-3 h-3" />
      estate-check · {String(ref).slice(0, 24)}
    </span>
  );
}

function DraftRailRow({ label, cv }) {
  // Three visual states per §2.2 draft rail:
  //   * filled (check)
  //   * open (muted "— open")
  //   * agent-assumed (amber chip)
  const isFilled = cv && cv.value !== undefined && cv.value !== null;
  const isAgentAssumed = isFilled && cv.source === 'agent_assumed';
  return (
    <li
      data-testid={`draft-rail-row-${label}`}
      className="flex items-center justify-between py-2 border-b border-rms-line last:border-b-0"
    >
      <span className="text-sm text-rms-ink">{label}</span>
      {!isFilled && (
        <span data-testid={`draft-open-${label}`} className="text-xs text-rms-mute italic">— open</span>
      )}
      {isFilled && !isAgentAssumed && (
        <span data-testid={`draft-filled-${label}`} className="inline-flex items-center gap-1 text-xs text-emerald-800">
          <Check className="w-3.5 h-3.5" />
          <span className="truncate max-w-[10rem]">{JSON.stringify(cv.value)}</span>
        </span>
      )}
      {isAgentAssumed && (
        <span
          data-testid={`draft-agent-assumed-${label}`}
          className="text-[10px] font-mono uppercase tracking-wider text-amber-900 bg-amber-50 border border-amber-200 rounded-full px-2 py-0.5"
        >
          agent-assumed
        </span>
      )}
    </li>
  );
}

function ChatMessage({ turn }) {
  return (
    <div data-testid={`chat-turn-${turn.turn_ref}`} className="rounded-md border border-rms-line p-3 bg-white">
      {turn.feasibility_snapshot_ref && (
        <div className="mb-2">
          <EstateCheckChip ref={turn.feasibility_snapshot_ref} />
        </div>
      )}
      <p className="text-sm text-rms-ink whitespace-pre-wrap">{turn.agent_content}</p>
      <div className="mt-1 text-[10px] font-mono uppercase tracking-wider text-rms-mute">
        turn · {turn.turn_ref.slice(0, 10)}
      </div>
    </div>
  );
}

export default function CommissionWizardPage() {
  const { identity } = useAuth();
  const navigate = useNavigate();
  const [sid, setSid] = useState(null);
  const [wizardState, setWizardState] = useState(null);
  const [turns, setTurns] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  const refreshState = useCallback(async (sessionId) => {
    const r = await api.wizardOperatorGet(sessionId);
    if (r.status === 200) setWizardState(r.body);
    else setErr({ status: r.status, body: r.body });
  }, []);

  const startSession = useCallback(async () => {
    setBusy(true);
    const r = await api.wizardOperatorStart();
    setBusy(false);
    if (r.status !== 201) {
      setErr({ status: r.status, body: r.body });
      return;
    }
    setSid(r.body.session_id);
    // Kick off first agent turn (turn_ref-less advance).
    const t = await api.wizardOperatorTurn(r.body.session_id, {});
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

  const submitTurn = async (e) => {
    e.preventDefault();
    if (!sid || busy || !userInput.trim()) return;
    setBusy(true);
    const lastTurn = turns[turns.length - 1];
    const r = await api.wizardOperatorTurn(sid, {
      turn_ref: lastTurn ? lastTurn.turn_ref : undefined,
      user_content: userInput.trim(),
    });
    setBusy(false);
    if (r.status === 200) {
      setTurns((t) => [...t, r.body]);
      setUserInput('');
      await refreshState(sid);
    } else {
      setErr({ status: r.status, body: r.body });
    }
  };

  const goToCommitReview = () => navigate(`/operator/commit-review/${sid}`);

  if (identity === null) {
    return <div className="min-h-screen flex items-center justify-center"><p className="text-rms-mute text-sm">Checking sign-in…</p></div>;
  }
  if (identity === false) return null;

  if (err && (err.status === 401 || err.status === 403)) {
    return (
      <div className="min-h-screen flex items-center justify-center p-8">
        <AuthDeniedNotice body={err.body} onSignIn={() => navigate('/auth/login')} />
      </div>
    );
  }

  const committed = (wizardState && wizardState.committed_values) || {};

  return (
    <div data-testid="commission-wizard-page" className="min-h-screen bg-white">
      <header className="border-b border-rms-line">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-baseline gap-2">
            <h1 className="text-base font-semibold tracking-tight text-rms-ink">RMS Intelligence</h1>
            <span className="text-[10px] font-mono uppercase text-rms-mute tracking-wider">operator · commission</span>
          </div>
          <button
            type="button"
            data-testid="commission-goto-commit-review"
            onClick={goToCommitReview}
            disabled={!sid}
            className="text-sm text-rms-ink underline disabled:text-rms-mute disabled:no-underline"
          >
            Review & freeze →
          </button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6 grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
        {/* §2.2 Chat pane (left) */}
        <section aria-label="Chat" data-testid="commission-chat-pane" className="space-y-3">
          {turns.map((t) => <ChatMessage key={t.turn_ref} turn={t} />)}
          {err && (err.status !== 401 && err.status !== 403) && (
            <div data-testid="commission-chat-error" className="rounded-md border border-red-300 bg-red-50 p-3 text-sm text-red-900">
              {formatApiErrorDetail(err.body && (err.body.detail || err.body.reason))}
            </div>
          )}
          <form onSubmit={submitTurn} className="flex gap-2 items-end">
            <textarea
              data-testid="commission-input"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              disabled={busy || !sid}
              rows={2}
              placeholder="State intent or answer the agent…"
              className="flex-1 rounded-md border border-rms-line px-3 py-2 text-sm text-rms-ink resize-none"
            />
            <button
              type="submit"
              data-testid="commission-submit"
              disabled={busy || !sid || !userInput.trim()}
              className="inline-flex items-center gap-1 px-3 py-2 rounded-md bg-rms-ink text-white text-sm disabled:bg-gray-300"
            >
              {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              Send
            </button>
          </form>
        </section>

        {/* §2.2 Objective draft rail (right) */}
        <aside data-testid="commission-draft-rail" aria-label="Objective draft" className="lg:sticky lg:top-6 self-start rounded-md border border-rms-line bg-white p-4 h-fit">
          <h2 className="text-[10px] uppercase tracking-wider text-rms-mute font-mono">Objective draft</h2>
          <ul className="mt-3">
            {MANDATORY_FIELDS.map(({ key, label }) => (
              <DraftRailRow key={key} label={label} cv={committed[key]} />
            ))}
          </ul>
          <div className="mt-4 pt-3 border-t border-rms-line text-xs text-rms-mute">
            <p data-testid="draft-envelope-line">
              done-condition: <span className="text-rms-ink">{committed['envelope.done_condition']?.value || '—'}</span>
              {' · '}budget: <span className="text-rms-ink">{committed['envelope.budget']?.value || '—'}</span>
              {' · '}lawful basis: <span className="text-rms-ink">{committed['envelope.lawful_basis']?.value || '—'}</span>
            </p>
          </div>
        </aside>
      </main>
    </div>
  );
}
