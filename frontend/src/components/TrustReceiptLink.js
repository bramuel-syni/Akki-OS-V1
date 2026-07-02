import React from 'react';
import { Link } from 'react-router-dom';
import { FileText } from 'lucide-react';

export default function TrustReceiptLink({ traceId, className = '' }) {
  if (!traceId) return null;
  return (
    <Link
      to={`/trace/${traceId}`}
      data-testid={`trust-receipt-link-${traceId}`}
      className={`inline-flex items-center gap-1.5 text-xs font-mono text-rms-accent hover:underline focus:outline-none focus:ring-2 focus:ring-rms-accent focus:ring-offset-1 rounded ${className}`}
    >
      <FileText className="w-3.5 h-3.5" />
      <span>{traceId}</span>
    </Link>
  );
}
