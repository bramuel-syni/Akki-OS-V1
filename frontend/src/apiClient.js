import axios from 'axios';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// Phase 8 Stage B-1 — access token store + Bearer interceptor.
// Owner E1 ratified: JWT single-source. Federation-forward: OAuth adapters
// later mint the same JWT claim shape; the token store here is the
// integration seam that later adapters replace.
const TOKEN_STORAGE_KEY = 'rms.b1.auth.access_token';
const REFRESH_STORAGE_KEY = 'rms.b1.auth.refresh_token';

export const tokenStore = {
  getAccessToken: () => {
    try { return window.localStorage.getItem(TOKEN_STORAGE_KEY); } catch { return null; }
  },
  getRefreshToken: () => {
    try { return window.localStorage.getItem(REFRESH_STORAGE_KEY); } catch { return null; }
  },
  setTokens: ({ access_token, refresh_token }) => {
    try {
      if (access_token) window.localStorage.setItem(TOKEN_STORAGE_KEY, access_token);
      if (refresh_token) window.localStorage.setItem(REFRESH_STORAGE_KEY, refresh_token);
    } catch { /* Storage unavailable — no-op */ }
  },
  clear: () => {
    try {
      window.localStorage.removeItem(TOKEN_STORAGE_KEY);
      window.localStorage.removeItem(REFRESH_STORAGE_KEY);
    } catch { /* no-op */ }
  },
};

const client = axios.create({ baseURL: API, timeout: 15000 });

// Bearer interceptor: attach access token when present.
client.interceptors.request.use((cfg) => {
  const t = tokenStore.getAccessToken();
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

// Detail-safe error message formatter for FastAPI validation-422s.
// FastAPI returns detail as an array of {msg, ...}; rendering that in JSX
// crashes React. This helper flattens any shape to a string.
export function formatApiErrorDetail(detail) {
  if (detail == null) return 'Something went wrong. Please try again.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail))
    return detail
      .map((e) => (e && typeof e.msg === 'string' ? e.msg : JSON.stringify(e)))
      .filter(Boolean)
      .join(' ');
  if (detail && typeof detail.msg === 'string') return detail.msg;
  return String(detail);
}

export const api = {
  health: () => client.get('/health').then(r => r.data),
  systemState: () => client.get('/system/state').then(r => r.data),
  northenaStatus: () => client.get('/northena/status').then(r => r.data),
  openRuns: () => client.get('/northena/ledger/open_runs').then(r => r.data),
  ledgerByRun: (runId) => client.get(`/northena/ledger/by_run/${runId}`).then(r => r.data),
  traceLens: (traceId) => client.get(`/northena/trace/${traceId}`).then(r => r.data),
  v1Status: () => client.get('/v1/status').then(r => r.data),
  v3Status: () => client.get('/v3/status').then(r => r.data),
  solvaStatus: () => client.get('/solva/status').then(r => r.data),
  service1Status: () => client.get('/service_1/status').then(r => r.data),
  liftManifest: () => client.get('/discipline/lift_manifest').then(r => r.data),
  stampAuditRecent: (limit = 50) => client.get(`/v1/stamp_audit/recent?limit=${limit}`).then(r => r.data),
  contractFiveRings: () => client.get('/contracts/five_rings').then(r => r.data),
  contractQualMatrix: () => client.get('/contracts/qualification_matrix').then(r => r.data),
  // Phase 8a-lite (Ask Console) — v2 dispatch consumer.
  dispatchV2: (objectiveRequestV2) =>
    client
      .post('/service_1/v2/dispatch', objectiveRequestV2, {
        validateStatus: (s) => s >= 200 && s < 500,
      })
      .then((r) => ({ status: r.status, body: r.data })),
  // Phase 8 Stage B-1 — auth surface. Returns raw response body per Owner E2
  // {reason, detail} shape on auth denial; validateStatus permits 401/403/409.
  authRegister: (email, password, name) =>
    client
      .post('/auth/register', { email, password, name }, {
        validateStatus: (s) => s >= 200 && s < 500,
      })
      .then((r) => ({ status: r.status, body: r.data })),
  authLogin: (email, password) =>
    client
      .post('/auth/login', { email, password }, {
        validateStatus: (s) => s >= 200 && s < 500,
      })
      .then((r) => ({ status: r.status, body: r.data })),
  authMe: () =>
    client
      .get('/auth/me', { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
  authRefresh: () => {
    const rt = tokenStore.getRefreshToken();
    return client
      .post('/auth/refresh', null, {
        headers: rt ? { Authorization: `Bearer ${rt}` } : {},
        validateStatus: (s) => s >= 200 && s < 500,
      })
      .then((r) => ({ status: r.status, body: r.data }));
  },
  // Phase 8 Stage B-2 — Operator surface (UI Spec §2).
  operatorStatus: () =>
    client
      .get('/operator/status', { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
  fleetPolicy: () => client.get('/fleet/policy').then((r) => r.data),
  // Wizard operator (7 endpoints from Phase 7 B-1/B-2/B-3) — auth-passing.
  wizardOperatorStart: () =>
    client
      .post('/wizard/operator/session', null, { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
  wizardOperatorTurn: (sid, payload) =>
    client
      .post(`/wizard/operator/${sid}/turn`, payload, { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
  wizardOperatorCommitReview: (sid) =>
    client
      .post(`/wizard/operator/${sid}/commit-review`, null, { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
  wizardOperatorFreeze: (sid, body) =>
    client
      .post(`/wizard/operator/${sid}/freeze`, body || {}, { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
  wizardOperatorGet: (sid) =>
    client
      .get(`/wizard/operator/${sid}`, { validateStatus: (s) => s >= 200 && s < 500 })
      .then((r) => ({ status: r.status, body: r.data })),
};

export default api;
