"""Census-dimensions registry loader (Owner CD-E3 α + register-before-validate).

Owner ruling CD-E3 α (2026-07-10) — verbatim carrier:

    'α, with the registration mechanism added — as framed it deadlocks. Both
     registries seed empty; a hard write-time error against an empty registry
     means the first census run can never write. Fix: the census write path
     registers before it validates. First-observed census_observed values
     extend the registry via the additive versioned bump (v0→vN) during the
     census run, then the sidecar write validates against the now-current
     registry. manifest_declared values get no such path — they pre-exist in
     the registry or fail hard; a manifest cannot invent vocabulary, only
     observation can. The registry version history becomes the audit trail
     of when each vocabulary item was first observed. CD-G3 stands as
     belt-and-suspenders.'

Landing:
  * `current_registry_version(kind)` — scans for highest v(N).json file;
    returns (n, vocabulary_list).
  * `register_observation(kind, value)` — writes v(N+1).json byte-adding the
    new value; v(N).json preserved byte-identical (audit trail).
  * `validate_content_surface(v)` / `validate_genre(v)` — pure check against
    current registry; raises ValueError if not present. Used by CD-G3 AST
    gate and by `record_census_dimension` after registration path.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List, Literal, Tuple

RegistryKind = Literal["content_surfaces", "genres"]

_REGISTRY_DIR = Path(__file__).parent
_KIND_FIELDS = {
    "content_surfaces": ("census_content_surfaces", "surfaces"),
    "genres": ("census_genres", "genres"),
}
_VERSION_RE = re.compile(r"\.v(\d+)\.json$")


def _list_versioned_files(kind: RegistryKind) -> List[Tuple[int, Path]]:
    """Return [(n, path)] sorted by n ascending."""
    prefix, _ = _KIND_FIELDS[kind]
    hits: List[Tuple[int, Path]] = []
    for p in _REGISTRY_DIR.iterdir():
        if not p.name.startswith(f"{prefix}.v"):
            continue
        m = _VERSION_RE.search(p.name)
        if m:
            hits.append((int(m.group(1)), p))
    hits.sort(key=lambda t: t[0])
    return hits


def current_registry_version(kind: RegistryKind) -> Tuple[int, List[str]]:
    """Return (highest_version_n, current_vocabulary_list) for `kind`."""
    files = _list_versioned_files(kind)
    if not files:
        raise FileNotFoundError(
            f"census-dimensions registry kind={kind!r}: no v*.json file found "
            f"under {_REGISTRY_DIR}. Seed v0 required."
        )
    n, path = files[-1]
    _, field = _KIND_FIELDS[kind]
    payload = json.loads(path.read_text(encoding="utf-8"))
    return n, list(payload.get(field, []))


def load_registry(kind: RegistryKind) -> List[str]:
    """Return the current vocabulary for `kind` (empty list if seed v0)."""
    _, vocab = current_registry_version(kind)
    return vocab


def register_observation(kind: RegistryKind, value: str) -> int:
    """Additive versioned bump for a census-observed novel value.

    Owner CD-E3 α — v(N).json preserved byte-identical; v(N+1).json written
    with `value` appended. Returns the new version number (N+1).

    Idempotent-by-value: if `value` is already present, returns current N
    without writing (no unnecessary bump).
    """
    prefix, field = _KIND_FIELDS[kind]
    n, vocab = current_registry_version(kind)
    if value in vocab:
        return n
    new_vocab = list(vocab) + [value]
    new_n = n + 1
    new_path = _REGISTRY_DIR / f"{prefix}.v{new_n}.json"
    payload = {
        "version": f"v{new_n}",
        "extends": f"v{n}",
        "added_value": value,
        "added_source": "census_observed",
        "authority_source": (
            "Owner ruling CD-E3 α register-before-validate (2026-07-10) — "
            "additive versioned bump on first census observation. "
            f"v{n} preserved byte-identical."
        ),
        field: new_vocab,
    }
    new_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return new_n


def _validate(kind: RegistryKind, value: str) -> str:
    """Pure check: value must appear in current registry. No side effect."""
    vocab = load_registry(kind)
    if value not in vocab:
        raise ValueError(
            f"census-dimensions {kind}: value {value!r} not in current registry. "
            f"census_observed values are registered before validation; "
            f"manifest_declared values must pre-exist in the registry — "
            f"'a manifest cannot invent vocabulary, only observation can.'"
        )
    return value


def validate_content_surface(value: str) -> str:
    """Validate `content_surface` against current census_content_surfaces registry."""
    return _validate("content_surfaces", value)


def validate_genre(value: str) -> str:
    """Validate `genre` against current census_genres registry."""
    return _validate("genres", value)
