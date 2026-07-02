"""northena_ledger_row snapshot invariant."""
import json
from pathlib import Path

from contracts.northena_ledger import LedgerRow

SNAP = Path(__file__).parent / 'northena_ledger_row.contract_snapshot.json'


def _canonical(o):
    return json.dumps(o, indent=2, sort_keys=True)


def test_northena_ledger_row_schema_frozen():
    expected = json.loads(SNAP.read_text())
    actual = LedgerRow.model_json_schema()
    assert _canonical(actual) == _canonical(expected), (
        "northena_ledger_row@v0 schema drift. Bump via new snapshot in code review."
    )
