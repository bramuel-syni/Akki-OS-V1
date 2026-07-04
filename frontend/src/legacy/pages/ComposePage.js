import React, { useState } from 'react';
import { useApi } from '../../hooks/useApi';
import api from '../../apiClient';
import ClassBadge from '../../components/ClassBadge';
import RefusalCard from '../../components/RefusalCard';
import { Link } from 'react-router-dom';
import { Send, Loader2, FileText } from 'lucide-react';

export default function ComposePage() {
  const [objectiveText, setObjectiveText] = useState('');
  const [floor, setFloor] = useState('utterance');
  const [lawfulBasis, setLawfulBasis] = useState('legitimate_interest');
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState('');

  const { data: sampleUnit } = useApi(() => api.contractFiveRings(), []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    setError(null);
    setResult(null);

    const trimmed = objectiveText.trim();
    if (!trimmed) {
      setFormError('Objective text is required. State what you need to know.');
      return;
    }

    setSubmitting(true);
    try {
      const body = {
        artifact_id: 'portfolio-mandate-001',
        artifact_version: 'v0',
        lawful_basis: lawfulBasis,
        floor: floor,
        objective_text: trimmed,
        units: sampleUnit ? [sampleUnit] : [],
      };
      const resp = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/service_1/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await resp.json();
      if (resp.ok) {
        setResult({ type: 'success', data });
      } else if (data.outcome === 'refused') {
        setResult({ type: 'refusal', data });
      } else if (data.detail && Array.isArray(data.detail)) {
        setError('Validation error: ' + data.detail.map(d => d.msg).join('; '));
      } else {
        setError('Unexpected error: ' + JSON.stringify(data));
      }
    } catch (err) {
      setError(err.message || 'Network error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div data-testid="compose-page" className="space-y-6">
      <div>
        <h2 className="text-lg font-semibold tracking-tight">Compose Objective</h2>
        <p className="text-sm text-rms-mute mt-0.5">
          State what you need to know. The system will compose the governed request.
        </p>
      </div>

      <form onSubmit={handleSubmit} data-testid="compose-form" className="space-y-4">
        <div>
          <label htmlFor="objective-text" className="block text-sm font-medium mb-1">
            Objective
          </label>
          <textarea
            id="objective-text"
            value={objectiveText}
            onChange={(e) => {
              setObjectiveText(e.target.value);
              if (formError) setFormError('');
            }}
            placeholder="What do you need to know?"
            data-testid="objective-text-input"
            rows={3}
            className={`w-full px-3 py-2 text-sm border rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-rms-accent focus:border-rms-accent ${
              formError ? 'border-rose-400' : 'border-rms-line'
            }`}
          />
          {formError && (
            <p data-testid="objective-text-error" className="mt-1 text-xs text-rose-600">
              {formError}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="floor-select" className="block text-sm font-medium mb-1">
              Defensibility Floor
            </label>
            <select
              id="floor-select"
              value={floor}
              onChange={(e) => setFloor(e.target.value)}
              data-testid="floor-select"
              className="w-full px-3 py-2 text-sm border border-rms-line rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-rms-accent"
            >
              <option value="fact">Fact (highest)</option>
              <option value="utterance">Utterance</option>
              <option value="non_factual">Non-factual (lowest)</option>
            </select>
          </div>
          <div>
            <label htmlFor="lawful-basis" className="block text-sm font-medium mb-1">
              Lawful Basis
            </label>
            <select
              id="lawful-basis"
              value={lawfulBasis}
              onChange={(e) => setLawfulBasis(e.target.value)}
              data-testid="lawful-basis-select"
              className="w-full px-3 py-2 text-sm border border-rms-line rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-rms-accent"
            >
              <option value="legitimate_interest">Legitimate interest</option>
              <option value="consent">Consent</option>
              <option value="contract">Contract</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={submitting}
          data-testid="compose-submit-btn"
          className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium bg-rms-ink text-white rounded-lg hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-rms-accent focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {submitting ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
          {submitting ? 'Running…' : 'Submit Objective'}
        </button>
      </form>

      {error && (
        <div data-testid="compose-error" className="rounded-lg border border-rose-300 bg-rose-50 text-rose-900 px-4 py-3 text-sm">
          {error}
        </div>
      )}

      {result?.type === 'refusal' && (
        <RefusalCard refusal={result.data} />
      )}

      {result?.type === 'success' && (
        <section data-testid="run-summary-result" className="rounded-xl border border-emerald-200 bg-emerald-50 p-5 space-y-3">
          <h3 className="text-sm font-semibold text-emerald-900">Run Complete</h3>
          <dl className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
            <div>
              <dt className="text-xs text-emerald-700 uppercase tracking-wide">Run ID</dt>
              <dd className="font-mono mt-0.5">{result.data.run_id}</dd>
            </div>
            <div>
              <dt className="text-xs text-emerald-700 uppercase tracking-wide">Trace ID</dt>
              <dd className="mt-0.5">
                <Link
                  to={`/trace/${result.data.trace_id}`}
                  data-testid="result-trace-link"
                  className="font-mono text-xs text-rms-accent hover:underline focus:outline-none focus:ring-2 focus:ring-rms-accent rounded"
                >
                  {result.data.trace_id}
                </Link>
              </dd>
            </div>
            <div>
              <dt className="text-xs text-emerald-700 uppercase tracking-wide">Floor</dt>
              <dd className="mt-0.5">
                <ClassBadge defensibilityClass={result.data.defensibility_floor} />
              </dd>
            </div>
            <div>
              <dt className="text-xs text-emerald-700 uppercase tracking-wide">Converged Units</dt>
              <dd className="font-mono mt-0.5">{result.data.converged_unit_count}</dd>
            </div>
            <div>
              <dt className="text-xs text-emerald-700 uppercase tracking-wide">Mining Plan</dt>
              <dd className="font-mono mt-0.5 text-xs">{result.data.mining_plan_id}</dd>
            </div>
            <div>
              <dt className="text-xs text-emerald-700 uppercase tracking-wide">Yield Layer</dt>
              <dd className="font-mono mt-0.5">{result.data.yield_layer_version}</dd>
            </div>
          </dl>
          <div className="flex items-center gap-2 pt-2 border-t border-emerald-200">
            <FileText className="w-4 h-4 text-emerald-700" />
            <Link
              to={`/trace/${result.data.trace_id}`}
              data-testid="result-trust-receipt-link"
              className="text-xs font-medium text-rms-accent hover:underline focus:outline-none focus:ring-2 focus:ring-rms-accent rounded"
            >
              View Trust Receipt →
            </Link>
          </div>
        </section>
      )}
    </div>
  );
}
