import axios from 'axios';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const client = axios.create({ baseURL: API, timeout: 15000 });

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
};

export default api;
