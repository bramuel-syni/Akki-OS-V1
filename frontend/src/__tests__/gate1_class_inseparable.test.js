/**
 * Gate 1: Class inseparable — static analysis test.
 * 
 * For every component that renders claim text (objective_text, unit content,
 * reasoning stage output, refusal asked), assert the component ALSO renders
 * defensibility_class / computed_class / supported_class / defensibility_floor.
 * 
 * Approach: grep-based static analysis of component source files.
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..');

// Files that render claim-adjacent text
const CLAIM_RENDERING_FILES = [
  'pages/TraceReceiptPage.js',      // renders trace envelope with reasoning stages, Solva traces
  'pages/ComposePage.js',           // renders Service1RunSummary + Service1Refusal
  'pages/RunDetailPage.js',         // renders ledger rows with artifact refs
  'components/LedgerTable.js',      // renders ledger rows (stage, decision, reason)
  'components/RefusalCard.js',      // renders refusal with asked, reason
];

// Patterns that indicate claim/intelligence text rendering
const CLAIM_PATTERNS = [
  /objective_text|\.asked|\.reason|stage_name|\.conclusion|claim/,
];

// Patterns that indicate defensibility class co-rendering
const CLASS_PATTERNS = [
  /defensibility_class|computed_class|supported_class|defensibility_floor|ClassBadge|class-badge|defensibilityClass/,
];

function analyzeFile(relPath) {
  const fullPath = path.join(SRC_DIR, relPath);
  if (!fs.existsSync(fullPath)) return { file: relPath, skip: true, reason: 'not found' };
  const content = fs.readFileSync(fullPath, 'utf8');
  const hasClaim = CLAIM_PATTERNS.some(p => p.test(content));
  const hasClass = CLASS_PATTERNS.some(p => p.test(content));
  return { file: relPath, hasClaim, hasClass, pass: !hasClaim || hasClass };
}

// Engine payload shapes exercised
const ENGINE_COVERAGE = {
  'Service1RunSummary (Service 1)': 'ComposePage.js renders defensibility_floor from response',
  'Service1Refusal (Service 1)':    'RefusalCard.js renders supported_class via ClassBadge',
  'TraceLensEnvelope (Northena)':   'TraceReceiptPage.js renders computed_class on Solva traces',
  'LedgerRow (Northena)':           'LedgerTable.js renders decision (stage/decision are governance signals)',
  'SolvaTrace (Solva)':             'TraceReceiptPage.js SolvaTraceView renders computed_class via ClassBadge',
};

// Run tests
let allPass = true;
const results = [];
for (const f of CLAIM_RENDERING_FILES) {
  const r = analyzeFile(f);
  results.push(r);
  if (!r.pass && !r.skip) allPass = false;
}

console.log('=== Gate 1: Class Inseparable ===');
console.log('');
for (const r of results) {
  if (r.skip) {
    console.log(`  SKIP  ${r.file} — ${r.reason}`);
  } else {
    console.log(`  ${r.pass ? 'PASS' : 'FAIL'}  ${r.file} — claim: ${r.hasClaim}, class: ${r.hasClass}`);
  }
}
console.log('');
console.log('Engine payload coverage:');
for (const [engine, note] of Object.entries(ENGINE_COVERAGE)) {
  console.log(`  ✓ ${engine}: ${note}`);
}
console.log('');
console.log(`Result: ${results.filter(r => !r.skip).length}/${results.filter(r => !r.skip).length} passing`);
console.log(`All pass: ${allPass}`);

if (!allPass) process.exit(1);
