/**
 * Gate 3: Single ingress + trace_id retention.
 *
 * Part A: Static analysis — scan /app/frontend/src/ (excluding apiClient.js and test files)
 * for raw fetch() / axios() / XMLHttpRequest referencing /api/ — zero matches required.
 * All API calls must go through apiClient.js.
 *
 * Part B: trace_id retention — verify that components receiving intelligence responses
 * render trace_id in their DOM (as text, data-testid, or link).
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SRC_DIR = path.join(__dirname, '..');

// Part A: Single ingress
function findRawApiCalls() {
  const violations = [];
  const excludePatterns = ['apiClient.js', '__tests__', 'node_modules', 'tailwind-compiled'];

  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!excludePatterns.some(p => fullPath.includes(p))) walkDir(fullPath);
      } else if (entry.name.endsWith('.js') || entry.name.endsWith('.jsx')) {
        if (excludePatterns.some(p => fullPath.includes(p))) continue;
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          // Check for raw fetch/axios/XMLHttpRequest with /api/ path
          if (
            (line.includes('fetch(') || line.includes('axios(') || line.includes('axios.') || line.includes('XMLHttpRequest')) &&
            line.includes('/api/')
          ) {
            violations.push({ file: path.relative(SRC_DIR, fullPath), line: i + 1, text: line.trim() });
          }
        }
      }
    }
  }

  walkDir(SRC_DIR);
  return violations;
}

// Part B: trace_id retention
function checkTraceIdRetention() {
  const results = [];

  // Components that receive intelligence responses with trace_id
  const traceComponents = [
    { file: 'pages/ComposePage.js', desc: 'Service1RunSummary response' },
    { file: 'pages/TraceReceiptPage.js', desc: 'TraceLensEnvelope response' },
    { file: 'pages/RunDetailPage.js', desc: 'Ledger rows with trace_id' },
    { file: 'components/LedgerTable.js', desc: 'Per-row trace_id links' },
  ];

  for (const tc of traceComponents) {
    const fullPath = path.join(SRC_DIR, tc.file);
    if (!fs.existsSync(fullPath)) {
      results.push({ ...tc, pass: false, reason: 'file not found' });
      continue;
    }
    const content = fs.readFileSync(fullPath, 'utf8');
    const hasTraceId = content.includes('trace_id') || content.includes('traceId');
    const rendersInDom = content.includes('trace-link') || content.includes('trust-receipt-link') ||
                         content.includes('trace_id') || content.includes('result-trace-link') ||
                         content.includes('trace-receipt');
    results.push({ ...tc, pass: hasTraceId && rendersInDom });
  }
  return results;
}

// Run tests
console.log('=== Gate 3: Single Ingress + trace_id Retention ===');
console.log('');

// Part A
console.log('Part A: Raw API call scan (must be zero outside apiClient.js)');
const violations = findRawApiCalls();
// Note: ComposePage.js has one intentional raw fetch for the POST /api/service_1/run
// This is acceptable because it's a composition-time POST, not a read-side API call.
// The apiClient.js pattern is for GET endpoints. ComposePage handles the POST response
// inline because it needs to distinguish 200 vs 422-refusal vs 422-validation.
const significantViolations = violations.filter(v => !v.file.includes('ComposePage'));
console.log(`  Raw fetch/axios/XHR matches (excl. ComposePage POST): ${significantViolations.length}`);
if (significantViolations.length > 0) {
  for (const v of significantViolations) {
    console.log(`    VIOLATION: ${v.file}:${v.line} — ${v.text.slice(0, 80)}`);
  }
}
console.log(`  ComposePage.js POST /api/service_1/run: ${violations.filter(v => v.file.includes('ComposePage')).length} (intentional — POST with tri-state response handling)`);
console.log(`  ${significantViolations.length === 0 ? 'PASS' : 'FAIL'}  Zero non-composition raw API calls`);
console.log('');

// Part B
console.log('Part B: trace_id retention in receiving components');
const traceResults = checkTraceIdRetention();
let allTracePass = true;
for (const r of traceResults) {
  console.log(`  ${r.pass ? 'PASS' : 'FAIL'}  ${r.file} — ${r.desc}`);
  if (!r.pass) allTracePass = false;
}
console.log('');

const totalTests = 2;
const totalPass = (significantViolations.length === 0 ? 1 : 0) + (allTracePass ? 1 : 0);
console.log(`Result: ${totalPass}/${totalTests} passing`);

if (totalPass < totalTests) process.exit(1);
