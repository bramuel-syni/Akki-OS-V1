"""Northena Ledger retention posture — G4.

User directive verbatim: "indefinite, append-only, configurable.
Retention is a parameter defaulting to indefinite. End-of-window
deletion stays UNIMPLEMENTED until DPO sets a window."

The correct discipline is: no deletion code exists at all. When DPO
lands a retention window, THIS TEST FAILS naturally — forcing the
deployment ceremony to update the invariant alongside the real deletion
code.
"""
from __future__ import annotations

from pathlib import Path


NORTHENA_DIR = (
    Path(__file__).parent.parent.parent / "services" / "northena"
)

# Substrings that would indicate a deletion code path.
_FORBIDDEN_TOKENS = ("delete_", "purge_", "expire_")


def test_no_deletion_path_in_northena_services():
    """Grep across `services/northena/`: no function name starting with
    delete_/purge_/expire_.

    Docstring/comment prose about "deletion" is allowed. We check only
    Python-function-name shapes: `def <name>(`.

    When DPO lands a retention window, the deletion function will need
    to be authored + this invariant re-blessed at deployment time.
    """
    offenders = []
    for py in NORTHENA_DIR.rglob("*.py"):
        for line in py.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped.startswith("def "):
                continue
            for tok in _FORBIDDEN_TOKENS:
                if stripped.startswith(f"def {tok}") or stripped.startswith(f"async def {tok}"):
                    offenders.append(f"{py.name}: {stripped}")
    assert not offenders, (
        "Northena services contain a deletion code path:\n  "
        + "\n  ".join(offenders)
        + "\n\nUser directive (1): end-of-window deletion stays UNIMPLEMENTED "
          "until DPO sets a window. If DPO landed a retention window, "
          "re-bless this invariant alongside the deletion implementation."
    )


def test_retention_mode_defaults_to_indefinite():
    """Env unset → retention_mode() returns 'indefinite'."""
    import os
    from services.northena.ledger import retention_mode
    # Preserve + clear
    prior = os.environ.pop("RMS_NORTHENA_LEDGER_RETENTION_MODE", None)
    try:
        assert retention_mode() == "indefinite"
    finally:
        if prior is not None:
            os.environ["RMS_NORTHENA_LEDGER_RETENTION_MODE"] = prior
