import React from 'react';

const classLabels = {
  fact: 'Established fact',
  utterance: 'Recorded statement',
  non_factual: 'Non-factual context',
};

const classColors = {
  fact: 'bg-emerald-100 text-emerald-900 border-emerald-300',
  utterance: 'bg-sky-100 text-sky-900 border-sky-300',
  non_factual: 'bg-slate-100 text-slate-700 border-slate-300',
};

export default function ClassBadge({ defensibilityClass, compact = false }) {
  if (!defensibilityClass) return null;
  const label = classLabels[defensibilityClass] || defensibilityClass;
  const color = classColors[defensibilityClass] || classColors.non_factual;
  return (
    <span
      data-testid={`class-badge-${defensibilityClass}`}
      className={`inline-flex items-center rounded border font-medium ${color} ${compact ? 'px-1.5 py-0 text-[10px]' : 'px-2 py-0.5 text-xs'}`}
      title={`Defensibility class: ${label}`}
    >
      {compact ? defensibilityClass : label}
    </span>
  );
}
