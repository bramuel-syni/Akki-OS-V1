"""Perception model registry (Owner 9.2a-E1 α + seed-with-CI-fixture correction · 2026-07-10).

Owner ruling 9.2a-E1 α verbatim carrier:

    'α, one correction: the registry does NOT seed empty — it seeds with the
     CI fixture model's entry. "Empty per data-blind" misapplies the posture:
     data-blind governs assumptions about the estate's content, not tool
     provenance — a model registry entry is tooling attestation, and an
     empty registry plus a provenance gate is the CD-E3 deadlock again
     (nothing can pass). Seed models_registry.v0.json with whisper-tiny
     pinned (SHA + license + origin URL) as the CI fixture model; production
     models land additively at 9.2b via the registry bump, selected then.
     "Whisper-class" resolves as: CI = whisper-tiny pinned now; production
     model = 9.2b decision.'

Landing:
  * `current_registry_version()` — scans for highest v(N).json file.
  * `load_registry(kind)` — loads current registry.
  * `attest_model(model_id)` — hard-fails if model not present.
  * `register_model(model_id, entry)` — additive v(N)->v(N+1) bump for 9.2b
    production-model registration (append-only, matches CD-E3 α + TF-E3 α
    versioning pattern).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REGISTRY_DIR = Path(__file__).parent
_VERSION_RE = re.compile(r"models_registry\.v(\d+)\.json$")


def _list_versioned_files() -> List[Tuple[int, Path]]:
    hits: List[Tuple[int, Path]] = []
    for p in _REGISTRY_DIR.iterdir():
        m = _VERSION_RE.search(p.name)
        if m:
            hits.append((int(m.group(1)), p))
    hits.sort(key=lambda t: t[0])
    return hits


def current_registry_version() -> Tuple[int, Dict[str, Any]]:
    """Return (highest_version_n, models_dict) of the current registry."""
    files = _list_versioned_files()
    if not files:
        raise FileNotFoundError(
            "perception models registry: no v*.json file found under "
            f"{_REGISTRY_DIR}. Seed v0 required (whisper-tiny per 9.2a-E1 α)."
        )
    n, path = files[-1]
    payload = json.loads(path.read_text(encoding="utf-8"))
    return n, dict(payload.get("models", {}))


def load_registry() -> Dict[str, Any]:
    _, models = current_registry_version()
    return models


def attest_model(model_id: str) -> Dict[str, Any]:
    """Hard-fail if `model_id` not present in current registry.

    Returns the registry entry on success. Called by workers before loading
    a model into memory; workers loading un-registered models produce
    fabricated telemetry attribution per 9.2a-E1 α ruling.
    """
    models = load_registry()
    entry = models.get(model_id)
    if entry is None:
        raise ValueError(
            f"perception model {model_id!r} not in models_registry (current "
            f"vocabulary: {sorted(models.keys())!r}). Register via additive "
            f"v(N) -> v(N+1) bump before workers may load it — "
            f"'production models land additively at 9.2b via the registry "
            f"bump, selected then.'"
        )
    return entry


def register_model(model_id: str, entry: Dict[str, Any]) -> int:
    """Additive v(N)->v(N+1) bump for a new model entry.

    v(N).json preserved byte-identical. Returns new version N+1.
    Idempotent-by-model_id: if `model_id` is already registered, returns
    current N without writing.

    Owner CD-E3 α register-before-validate pattern applied to model tooling
    per 9.2a-E1 α seed-with-CI-fixture correction. Used at 9.2b for
    production model registration.
    """
    n, models = current_registry_version()
    if model_id in models:
        return n
    new_models = {**models, model_id: {"model_id": model_id, **entry}}
    new_n = n + 1
    new_path = _REGISTRY_DIR / f"models_registry.v{new_n}.json"
    payload = {
        "version": f"v{new_n}",
        "extends": f"v{n}",
        "added_model_id": model_id,
        "authority_source": (
            "Owner 9.2a-E1 α additive registry bump — production model "
            f"registration at 9.2b or downstream. v{n} preserved byte-identical."
        ),
        "models": new_models,
    }
    new_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return new_n
