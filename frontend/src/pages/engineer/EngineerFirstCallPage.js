/**
 * UI Spec §4.2 — Engineer · First call — the contract.
 *
 * Verbatim elements per Spec:
 *   * request block (POST /v1/objectives with ask / standard / scope);
 *   * two response panels side by side — Answered (outcome, trace_id, claim,
 *     defensibility inline, provenance) and Refused — same envelope, body
 *     discriminator (outcome: refused, asked, supported_class,
 *     what_would_raise_it).
 *   * async addition: fresh-extraction asks return 202 { objective_id,
 *     accepted, delivery_estimate }; status transitions appear in Administer.
 *   * Binding copy: "There is no response shape in which the claim is
 *     separable from its class. Infrastructure faults return 500 and
 *     are never rendered as refusals."
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, FileCode2 } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const REQUEST_ILLUSTRATIVE = `POST /v1/objectives
{
  "ask": "What lifespan does this cohort exhibit?",
  "standard": "established_fact",
  "scope": "estate"
}`;

const ANSWERED_ILLUSTRATIVE = `{
  "outcome": "answered",
  "trace_id": "trc-a1b2c3",
  "claim": {
    "text": "Cohort A shows median lifespan 41 months.",
    "defensibility": {
      "class": "established_fact",
      "contested": false
    }
  },
  "provenance": {
    "source_ref": "acq-2026-Q1-004",
    "trace_id": "trc-a1b2c3"
  }
}`;

const REFUSED_ILLUSTRATIVE = `{
  "outcome": "refused",
  "asked": "established_fact",
  "supported_class": "recorded_statement",
  "what_would_raise_it": [
    "Cross-source corroboration required."
  ],
  "trace_id": "trc-a1b2c3"
}`;

const ASYNC_ACCEPTED_ILLUSTRATIVE = `{
  "objective_id": "obj-e2f3g4",
  "accepted": true,
  "delivery_estimate": "2026-07-06T14:00:00Z"
}`;

export default function EngineerFirstCallPage() {
  const { identity } = useAuth();
  const navigate = useNavigate();

  if (identity === false) {
    navigate('/auth/login', { replace: true });
    return null;
  }

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="engineer-first-call-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="engineer-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · engineer</div>
              <h1 className="text-lg font-semibold">First call — the contract</h1>
            </div>
          </div>
          <FileCode2 className="w-5 h-5 text-rms-mute" />
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 space-y-6">
        {/* Request block */}
        <section data-testid="first-call-request-block">
          <h2 className="text-base font-semibold mb-2">Request</h2>
          <pre className="border border-rms-line bg-white rounded p-3 text-xs font-mono overflow-x-auto whitespace-pre">
{REQUEST_ILLUSTRATIVE}
          </pre>
        </section>

        {/* Two response panels side by side. */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-4" data-testid="first-call-response-panels">
          <div data-testid="first-call-answered-panel">
            <h2 className="text-base font-semibold mb-2">Answered</h2>
            <pre className="border border-emerald-200 bg-emerald-50 rounded p-3 text-xs font-mono overflow-x-auto whitespace-pre">
{ANSWERED_ILLUSTRATIVE}
            </pre>
          </div>
          <div data-testid="first-call-refused-panel">
            <h2 className="text-base font-semibold mb-2">
              Refused — <span className="italic font-normal">same envelope, body discriminator</span>
            </h2>
            <pre className="border border-amber-200 bg-amber-50 rounded p-3 text-xs font-mono overflow-x-auto whitespace-pre">
{REFUSED_ILLUSTRATIVE}
            </pre>
          </div>
        </section>

        {/* Async addition: third variant noted beneath. */}
        <section data-testid="first-call-async-variant">
          <div className="text-sm text-rms-mute mb-2">
            Fresh-extraction asks return <code className="font-mono">202 &#123; objective_id, accepted, delivery_estimate &#125;</code>;
            status transitions appear in Administer.
          </div>
          <pre className="border border-rms-line bg-white rounded p-3 text-xs font-mono overflow-x-auto whitespace-pre">
{ASYNC_ACCEPTED_ILLUSTRATIVE}
          </pre>
        </section>

        {/* Binding copy — verbatim from UI Spec §4.2. */}
        <section
          className="border-t border-rms-line pt-4 text-sm"
          data-testid="first-call-binding-copy"
        >
          <p className="italic text-rms-ink">
            There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals.
          </p>
        </section>
      </main>
    </div>
  );
}
