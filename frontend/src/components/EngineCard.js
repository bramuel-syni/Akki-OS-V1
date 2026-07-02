import React from 'react';
import { Activity } from 'lucide-react';

export default function EngineCard({ title, gate, data, note }) {
  return (
    <div data-testid={`engine-card-${title.toLowerCase().replace(/\s+/g, '-')}`} className="rounded-lg border border-rms-line bg-white p-4">
      <div className="flex items-center gap-2 mb-2">
        <Activity className="w-4 h-4 text-rms-accent" />
        <h3 className="text-sm font-semibold">{title}</h3>
        {gate && (
          <span className="ml-auto text-[10px] font-mono uppercase px-1.5 py-0.5 bg-rms-ink text-white rounded">
            {gate}
          </span>
        )}
      </div>
      {note && <p className="text-xs text-rms-mute mb-2">{note}</p>}
      {data && (
        <div className="space-y-1">
          {Object.entries(data).map(([k, v]) => (
            <div key={k} className="flex justify-between text-xs">
              <span className="text-rms-mute">{k}</span>
              <span className="font-mono text-rms-ink truncate max-w-[200px]" title={String(v)}>
                {typeof v === 'object' ? JSON.stringify(v) : String(v)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
