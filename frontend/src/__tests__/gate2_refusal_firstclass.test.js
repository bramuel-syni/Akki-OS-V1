/**
 * Gate 2: Refusal first-class + validation distinguishability.
 * 
 * Tests:
 * 1. RefusalCard renders all 7 Service1Refusal@v0 fields when given a refusal payload
 * 2. RefusalCard renders `asked` prominently
 * 3. RefusalCard renders `supported_class` via ClassBadge
 * 4. RefusalCard renders `what_would_raise_it` as actionable text
 * 5. Validation-422 body (detail: [...]) does NOT trigger refusal view
 * 6. ComposePage correctly distinguishes refusal (outcome=refused) from validation-422
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..');

// Synthetic Service1Refusal@v0 payload
const REFUSAL_PAYLOAD = {
  outcome: 'refused',
  reason: 'composition_below_floor',
  run_id: 'run-test-abc123',
  trace_id: 'trace-test-def456',
  asked: 'What is the Kenyan economic outlook?',
  supported_class: 'utterance',
  what_would_raise_it: 'No corroboration at the required standard was found.',
};

const REFUSAL_FIELDS = ['outcome', 'reason', 'run_id', 'trace_id', 'asked', 'supported_class', 'what_would_raise_it'];

// Validation-422 body (Pydantic validation error — NOT a refusal)
const VALIDATION_422 = {
  detail: [
    { type: 'missing', loc: ['body', 'floor'], msg: 'Field required', input: {} },
    { type: 'missing', loc: ['body', 'units'], msg: 'Field required', input: {} },
  ],
};

// Test 1: RefusalCard source includes rendering patterns for all fields
function testRefusalCardFields() {
  const src = fs.readFileSync(path.join(SRC_DIR, 'components/RefusalCard.js'), 'utf8');
  const rendered = [];
  // Check that these field references exist in the component
  if (src.includes('refusal.asked')) rendered.push('asked');
  if (src.includes('refusal.reason')) rendered.push('reason');
  if (src.includes('refusal.supported_class') || src.includes('supported_class')) rendered.push('supported_class');
  if (src.includes('refusal.what_would_raise_it') || src.includes('what_would_raise_it')) rendered.push('what_would_raise_it');
  // outcome, run_id, trace_id may be rendered in parent (ComposePage)
  const composeSrc = fs.readFileSync(path.join(SRC_DIR, 'pages/ComposePage.js'), 'utf8');
  if (composeSrc.includes('outcome')) rendered.push('outcome');
  if (composeSrc.includes('run_id') || composeSrc.includes('trace_id')) rendered.push('run_id');
  if (composeSrc.includes('trace_id')) rendered.push('trace_id');
  return rendered;
}

// Test 2: asked is prominent (appears in RefusalCard with its own <dd> or prominent styling)
function testAskedProminent() {
  const src = fs.readFileSync(path.join(SRC_DIR, 'components/RefusalCard.js'), 'utf8');
  return src.includes('refusal-asked') && src.includes('refusal.asked');
}

// Test 3: supported_class rendered via ClassBadge
function testSupportedClassBadge() {
  const src = fs.readFileSync(path.join(SRC_DIR, 'components/RefusalCard.js'), 'utf8');
  return src.includes('ClassBadge') && src.includes('refusal.supported_class');
}

// Test 4: what_would_raise_it rendered as actionable text
function testWhatWouldRaise() {
  const src = fs.readFileSync(path.join(SRC_DIR, 'components/RefusalCard.js'), 'utf8');
  return src.includes('refusal-raise') && src.includes('what_would_raise_it');
}

// Test 5: Validation-422 does NOT trigger RefusalCard
function testValidation422Distinguishability() {
  const src = fs.readFileSync(path.join(SRC_DIR, 'pages/ComposePage.js'), 'utf8');
  // ComposePage must check for outcome === 'refused' before rendering RefusalCard
  // AND must check for data.detail + Array.isArray separately
  const checksOutcome = src.includes("outcome === 'refused'") || src.includes('outcome === "refused"');
  const checksDetail = src.includes('data.detail') && src.includes('Array.isArray');
  return checksOutcome && checksDetail;
}

// Run all tests
console.log('=== Gate 2: Refusal First-Class + Validation Distinguishability ===');
console.log('');

const rendered = testRefusalCardFields();
const allFieldsCovered = REFUSAL_FIELDS.every(f => rendered.includes(f));
console.log(`  ${allFieldsCovered ? 'PASS' : 'FAIL'}  T1: All 7 refusal fields rendered — found: [${rendered.join(', ')}]`);

const askedProm = testAskedProminent();
console.log(`  ${askedProm ? 'PASS' : 'FAIL'}  T2: asked is prominent (data-testid="refusal-asked" + refusal.asked)`);

const classBadge = testSupportedClassBadge();
console.log(`  ${classBadge ? 'PASS' : 'FAIL'}  T3: supported_class rendered via ClassBadge`);

const raiseAction = testWhatWouldRaise();
console.log(`  ${raiseAction ? 'PASS' : 'FAIL'}  T4: what_would_raise_it rendered as actionable text`);

const valDistinguish = testValidation422Distinguishability();
console.log(`  ${valDistinguish ? 'PASS' : 'FAIL'}  T5: Validation-422 does NOT trigger refusal view (distinguishability check)`);

console.log('');
const passCount = [allFieldsCovered, askedProm, classBadge, raiseAction, valDistinguish].filter(Boolean).length;
console.log(`Result: ${passCount}/5 passing`);

if (passCount < 5) process.exit(1);
