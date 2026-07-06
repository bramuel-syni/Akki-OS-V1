/**
 * UI Spec §5.3 — Buyer · Receive — deliverable and receipt.
 *
 * Verbatim elements per Spec:
 *   * delivered header + Download;
 *   * artifact sample block showing per-claim structure (claim,
 *     defensibility { class, contested }, provenance { source_ref, trace_id });
 *   * Outer-gate receipt card — transform name, key fingerprint, identity
 *     categories transformed, license ref — fact and fingerprint only,
 *     nothing that could aid reversal;
 *   * public trust-receipt line with URL pattern.
 */
import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Download, FileText } from 'lucide-react';

// Illustrative fixture — real deliverable arrives from the receiving surface
// post-admission. This surface is the buyer-facing receipt renderer.
const ARTIFACT_SAMPLE = {
  claim: {
    text: 'Cohort A shows median lifespan 41 months.',
    defensibility: { class: 'established_fact', contested: false },
    provenance: {
      source_ref: 'acq-2026-Q1-004',
      trace_id: 'trc-a1b2c3',
    },
  },
};

const OUTER_GATE_RECEIPT = {
  transform_name: 'k-anonymity-11-with-suppression',
  key_fingerprint: 'sha256:04c…f9a',
  identity_categories_transformed: ['direct_identifier', 'quasi_identifier'],
  license_ref: 'lic-2026-Q1-004',
};

export default function BuyerReceivePage() {
  const navigate = useNavigate();
  const { sessionId } = useParams();
  const traceId = ARTIFACT_SAMPLE.claim.provenance.trace_id;
  const publicReceiptUrl = `rms.intel/trace/${traceId}`;

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="buyer-receive-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate(`/buyer/acquire/${sessionId}`)}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="buyer-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · buyer</div>
              <h1 className="text-lg font-semibold" data-testid="buyer-receive-delivered-header">Delivered</h1>
            </div>
          </div>
          <button
            type="button"
            className="inline-flex items-center gap-1 px-3 py-1.5 rounded bg-rms-ink text-white text-sm"
            data-testid="buyer-receive-download-btn"
          >
            <Download className="w-4 h-4" />
            Download
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8 space-y-6">
        {/* Artifact sample — per-claim structure. */}
        <section data-testid="buyer-receive-artifact-sample">
          <h2 className="text-base font-semibold mb-2">Artifact sample</h2>
          <div className="border border-rms-line bg-white rounded p-3 space-y-2 text-sm">
            <div data-testid="buyer-receive-claim-text">
              <span className="text-rms-mute text-xs uppercase tracking-wider mr-2">claim</span>
              {ARTIFACT_SAMPLE.claim.text}
            </div>
            <div className="text-xs" data-testid="buyer-receive-defensibility">
              <span className="text-rms-mute uppercase tracking-wider">defensibility</span>
              {' · '}
              <span className="font-mono">
                class={ARTIFACT_SAMPLE.claim.defensibility.class} · contested={String(ARTIFACT_SAMPLE.claim.defensibility.contested)}
              </span>
            </div>
            <div className="text-xs" data-testid="buyer-receive-provenance">
              <span className="text-rms-mute uppercase tracking-wider">provenance</span>
              {' · '}
              <span className="font-mono">
                source_ref={ARTIFACT_SAMPLE.claim.provenance.source_ref} · trace_id={ARTIFACT_SAMPLE.claim.provenance.trace_id}
              </span>
            </div>
          </div>
        </section>

        {/* Outer-gate receipt card. */}
        <section data-testid="buyer-outer-gate-receipt">
          <h2 className="text-base font-semibold mb-2 flex items-center gap-1">
            <FileText className="w-4 h-4" />
            Outer-gate receipt
          </h2>
          <div className="border border-emerald-200 bg-emerald-50 rounded p-3 space-y-1 text-sm">
            <div>
              <span className="text-emerald-800 text-xs uppercase tracking-wider mr-2">transform</span>
              <span className="font-mono" data-testid="outer-gate-transform">
                {OUTER_GATE_RECEIPT.transform_name}
              </span>
            </div>
            <div>
              <span className="text-emerald-800 text-xs uppercase tracking-wider mr-2">key fingerprint</span>
              <span className="font-mono" data-testid="outer-gate-fingerprint">
                {OUTER_GATE_RECEIPT.key_fingerprint}
              </span>
            </div>
            <div>
              <span className="text-emerald-800 text-xs uppercase tracking-wider mr-2">categories transformed</span>
              <span className="font-mono" data-testid="outer-gate-categories">
                {OUTER_GATE_RECEIPT.identity_categories_transformed.join(', ')}
              </span>
            </div>
            <div>
              <span className="text-emerald-800 text-xs uppercase tracking-wider mr-2">license ref</span>
              <span className="font-mono" data-testid="outer-gate-license-ref">
                {OUTER_GATE_RECEIPT.license_ref}
              </span>
            </div>
            <div className="text-xs italic text-emerald-800 pt-1">
              Fact and fingerprint only — nothing that could aid reversal.
            </div>
          </div>
        </section>

        {/* Public trust-receipt line. */}
        <section
          className="border-t border-rms-line pt-4 text-sm"
          data-testid="buyer-public-trust-receipt-line"
        >
          <span className="text-rms-mute">Public trust receipt:</span>{' '}
          <a
            href={`https://${publicReceiptUrl}`}
            target="_blank"
            rel="noreferrer noopener"
            className="text-rms-ink underline font-mono"
            data-testid="buyer-public-trust-receipt-url"
          >
            {publicReceiptUrl}
          </a>
        </section>
      </main>
    </div>
  );
}
