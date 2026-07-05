/**
 * UI Spec §6.2 — Master Admin · Change a rule.
 *
 * Verbatim elements per Spec:
 *   * "The rule" — one sentence stating what it does in everyday language.
 *   * a short paragraph of current behaviour and what turning it on/off
 *     means.
 *   * plain Off / On options with natural labels.
 *   * "What changes" info box — one or two sentences.
 *   * commit button in natural language ("Turn it on").
 *   * Binding copy: "Recorded as your change, with today's date."
 *
 * Path routing at B-4 (Owner ratified):
 *   * /master-admin/change-a-rule/tier-lock — Path A (ledger-back).
 *   * Other rules (model_version, fleet_policy) listed in a sub-panel
 *     and render honest 501 language.
 */
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Sliders } from 'lucide-react';
import api, { formatApiErrorDetail } from '../../apiClient';
import { useAuth } from '../../hooks/useAuth';

const RULES = {
  'tier-lock': {
    id: 'tier-lock',
    path: 'A',
    one_sentence: 'This rule freezes the current price tier so quotes stop moving until you say so.',
    behaviour_paragraph:
      "When it is off, quotes are minted at the current bless tier as usual. When it is on, quotes refuse with the reason that you have frozen the tier — nothing running now changes, and it can be switched back at any time.",
    commit_label_off_to_on: 'Turn it on',
    commit_label_on_to_off: 'Turn it off',
    what_changes:
      'Nothing that is running right now changes. You can switch this back at any time. This decision is recorded with today’s date.',
  },
  'model-version': {
    id: 'model-version',
    path: 'B',
    one_sentence: 'This rule sets which price model is used when quoting.',
    behaviour_paragraph:
      'Changing the price model requires a versioned file update on the server. The system cannot safely change it from this surface.',
    what_changes:
      'Changing the price model requires a versioned file update on the server. Contact Owner. No change applied.',
  },
  'fleet-policy': {
    id: 'fleet-policy',
    path: 'B',
    one_sentence: 'This rule apportions GPU capacity between mining, transforms, and live-path.',
    behaviour_paragraph:
      'Changing capacity apportionment requires a versioned file update on the server. The system cannot safely change it from this surface.',
    what_changes:
      'Changing GPU capacity apportionment requires a versioned file update on the server. Contact Owner. No change applied.',
  },
};

function formatToday() {
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

export default function ChangeARulePage() {
  const { ruleId } = useParams();
  const { identity } = useAuth();
  const navigate = useNavigate();

  const rule = RULES[ruleId] || RULES['tier-lock'];

  const [reasonNote, setReasonNote] = useState('');
  const [selected, setSelected] = useState(false);
  const [busy, setBusy] = useState(false);
  const [commitResult, setCommitResult] = useState(null);
  const [err, setErr] = useState(null);

  const loadTierState = useCallback(async () => {
    if (rule.path !== 'A') return;
    // At B-4 the runtime lock state is not exposed via a GET route;
    // the surface simply lets the operator make and record a decision.
  }, [rule.path]);

  useEffect(() => {
    if (identity === null) return;
    if (identity === false) navigate('/auth/login', { replace: true });
    else loadTierState();
  }, [identity, navigate, loadTierState]);

  const commit = async () => {
    if (rule.path !== 'A') return;
    setBusy(true);
    setErr(null);
    // Deterministic idempotency_key per (rule, target-state, today).
    // Repeat click on the same button on the same day is a no-op.
    const idempotency_key = `${rule.id}-${selected ? 'on' : 'off'}-${formatToday()}`;
    const r = await api.masterAdminTierLockCommit({
      locked: selected,
      reason_note: reasonNote || null,
      idempotency_key,
    });
    setBusy(false);
    if (r.status === 200) {
      setCommitResult({
        locked: r.body.locked,
        at: r.body.at,
        recorded: true,
      });
    } else {
      setErr(formatApiErrorDetail(r.body && r.body.detail ? r.body.detail : r.body));
    }
  };

  const commitLabel = useMemo(() => {
    if (rule.path !== 'A') return null;
    return selected ? rule.commit_label_off_to_on : rule.commit_label_on_to_off;
  }, [rule, selected]);

  if (identity === null) return null;

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="master-admin-change-a-rule-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/master-admin')}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="master-admin-change-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · master admin</div>
              <h1 className="text-lg font-semibold">Change a rule</h1>
            </div>
          </div>
          <Sliders className="w-5 h-5 text-rms-mute" />
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-6 py-8 space-y-6">
        {/* §6.2 "The rule" — one sentence. */}
        <section data-testid="change-rule-one-sentence">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-rms-mute mb-1">The rule</h2>
          <p className="text-base text-rms-ink">{rule.one_sentence}</p>
        </section>

        {/* §6.2 Current-behaviour paragraph. */}
        <section
          className="text-sm text-rms-ink leading-relaxed"
          data-testid="change-rule-current-behaviour"
        >
          {rule.behaviour_paragraph}
        </section>

        {rule.path === 'A' && (
          <>
            {/* §6.2 Plain Off / On options. */}
            <section data-testid="change-rule-off-on-options">
              <div className="flex gap-3">
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="rule-toggle"
                    checked={!selected}
                    onChange={() => setSelected(false)}
                    data-testid="change-rule-option-off"
                  />
                  <span className="text-sm">Off</span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer">
                  <input
                    type="radio"
                    name="rule-toggle"
                    checked={selected}
                    onChange={() => setSelected(true)}
                    data-testid="change-rule-option-on"
                  />
                  <span className="text-sm">On</span>
                </label>
              </div>
            </section>

            {/* Reason note for audit. */}
            <section>
              <label className="block text-sm font-medium mb-1">Reason (recorded, optional)</label>
              <input
                type="text"
                className="w-full border border-rms-line rounded px-2 py-1 text-sm"
                value={reasonNote}
                onChange={(e) => setReasonNote(e.target.value)}
                data-testid="change-rule-reason-note"
                placeholder="Why this change is being made."
              />
            </section>
          </>
        )}

        {/* §6.2 "What changes" info box. */}
        <section
          className="border border-rms-line rounded p-3 text-sm bg-rms-highlight"
          data-testid="change-rule-what-changes"
        >
          <div className="text-xs font-semibold uppercase text-rms-mute mb-1">What changes</div>
          <p className="text-rms-ink">{rule.what_changes}</p>
        </section>

        {rule.path === 'A' && (
          <>
            {/* §6.2 Commit button in natural language. */}
            <section>
              <button
                type="button"
                onClick={commit}
                disabled={busy}
                className="px-4 py-2 rounded bg-rms-ink text-white text-sm font-medium disabled:opacity-40"
                data-testid="change-rule-commit-button"
              >
                {busy ? 'Recording…' : commitLabel}
              </button>
            </section>

            {commitResult && commitResult.recorded && (
              /* §6.2 Post-commit BINDING COPY VERBATIM. */
              <section
                className="border-t border-rms-line pt-4 text-sm"
                data-testid="change-rule-recorded-binding-copy"
              >
                <p className="text-emerald-800 font-medium">
                  Recorded as your change, with today&apos;s date.
                </p>
                <p className="text-xs text-rms-mute mt-1" data-testid="change-rule-recorded-date">
                  {formatToday()}
                </p>
              </section>
            )}
          </>
        )}

        {err && (
          <section
            className="text-sm text-red-800 border border-red-200 bg-red-50 rounded p-2"
            data-testid="change-rule-error"
          >
            {err}
          </section>
        )}

        {/* Other rules picker — Path B sub-list. */}
        <section className="border-t border-rms-line pt-4">
          <div className="text-xs uppercase tracking-wide text-rms-mute mb-2">Other rules</div>
          <ul className="space-y-2" data-testid="change-rule-other-rules">
            {Object.values(RULES).filter((r) => r.id !== rule.id).map((r) => (
              <li key={r.id}>
                <button
                  type="button"
                  onClick={() => navigate(`/master-admin/change-a-rule/${r.id}`)}
                  className="text-sm underline text-rms-mute hover:text-rms-ink"
                  data-testid={`change-rule-other-${r.id}`}
                >
                  {r.one_sentence}
                </button>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}
