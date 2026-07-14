// Instance config hook — MC-E6 β close 2026-07-14.
// Class-(a) branding moved from live code to instance config surface.
// Owner-verbatim: "instance #1's config carries 'RMS Intelligence'".
// Routed through apiClient per single-source-of-API discipline (Gate 3).
import { useEffect, useState } from 'react';
import api from '../apiClient';

const DEFAULT_CONFIG = {
  instance_id: 'instance_1',
  display_name: 'RMS Intelligence',
  product_title: 'RMS Intelligence',
  product_title_full: 'RMS Intelligence System',
};

let cached = null;

export function useInstanceConfig() {
  const [config, setConfig] = useState(cached || DEFAULT_CONFIG);
  useEffect(() => {
    if (cached) return;
    api.instanceConfig()
      .then((data) => {
        cached = data;
        setConfig(data);
      })
      .catch(() => setConfig(DEFAULT_CONFIG));
  }, []);
  return config;
}
