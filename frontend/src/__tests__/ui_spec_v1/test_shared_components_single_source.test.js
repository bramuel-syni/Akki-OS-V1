/**
 * Phase 8 Stage B-1 — shared-components single-source barrel (Owner E3 dispatch item 3).
 *
 * "Shared §8 component layer — /app/frontend/src/components/ui_spec_v1/.
 *  Formalise: ClassBadge, RefusalCard, OuterGateReceiptInline, StatusBadge,
 *  LedgerTable, TrustReceiptLink. Every subsequent surface (Ask Console-full,
 *  Operator, Engineer, Buyer, Master Admin, DPO) imports from here — no
 *  reimplementation."
 *
 * These gates confirm:
 *   1. The barrel exists and exports the six named UI-Spec-v1 §8 components
 *      + the B-1 addition AuthDeniedNotice.
 *   2. Each barrel export is the SAME object identity as the single-source
 *      module at `../<Name>` (i.e., pure re-export, not a reimplementation).
 */
import * as Barrel from '../../components/ui_spec_v1';
import ClassBadge from '../../components/ClassBadge';
import RefusalCard from '../../components/RefusalCard';
import OuterGateReceiptInline from '../../components/OuterGateReceiptInline';
import StatusBadge from '../../components/StatusBadge';
import LedgerTable from '../../components/LedgerTable';
import TrustReceiptLink from '../../components/TrustReceiptLink';
import AuthDeniedNotice from '../../components/AuthDeniedNotice';

const REQUIRED_NAMES = [
  'ClassBadge',
  'RefusalCard',
  'OuterGateReceiptInline',
  'StatusBadge',
  'LedgerTable',
  'TrustReceiptLink',
  'AuthDeniedNotice',
];

describe('Owner E3 dispatch — shared UI-Spec-v1 components single-source barrel', () => {
  test.each(REQUIRED_NAMES)('barrel exports %s', (name) => {
    expect(Barrel[name]).toBeDefined();
    expect(typeof Barrel[name]).toBe('function');
  });

  test('barrel ClassBadge is the same reference as the single-source module', () => {
    expect(Barrel.ClassBadge).toBe(ClassBadge);
  });

  test('barrel RefusalCard is the same reference as the single-source module', () => {
    expect(Barrel.RefusalCard).toBe(RefusalCard);
  });

  test('barrel OuterGateReceiptInline is the same reference as the single-source module', () => {
    expect(Barrel.OuterGateReceiptInline).toBe(OuterGateReceiptInline);
  });

  test('barrel StatusBadge is the same reference as the single-source module', () => {
    expect(Barrel.StatusBadge).toBe(StatusBadge);
  });

  test('barrel LedgerTable is the same reference as the single-source module', () => {
    expect(Barrel.LedgerTable).toBe(LedgerTable);
  });

  test('barrel TrustReceiptLink is the same reference as the single-source module', () => {
    expect(Barrel.TrustReceiptLink).toBe(TrustReceiptLink);
  });

  test('barrel AuthDeniedNotice is the same reference as the single-source module (B-1 addition)', () => {
    expect(Barrel.AuthDeniedNotice).toBe(AuthDeniedNotice);
  });
});
