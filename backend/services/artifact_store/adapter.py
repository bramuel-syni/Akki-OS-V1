"""Artifact Store adapter — three-op S3-class interface (BCR §3.2 AS-I1).

Owner ruling AS-E4 γ + Condition-2 (2026-07-08):

    'γ, not α. Material basis: α's caller_scope=None default is
     convention wearing mechanism clothing — every caller can pass
     None and the adapter obliges. Internal callers legitimately need
     raw reads (step-4 head-verify, orphan scan); the split makes
     that honest. Conditions that make γ mechanical:
     (1) public get(key, caller_scope) — scope required, no default,
     denies before bytes; (2) grep-negative gate: _get_raw has zero
     callers outside the adapter module + write-protocol + scan
     internals (Condition-2 pattern). Raw-never-egresses enforced
     by structure, proven by gate.'

Landing:
  - `_get_raw(key)` — private, no authz, callable only from within
    this module + `atomic_write.py` (step 4 head-verify) + `orphan_scan.py`.
  - `get(key, caller_scope: Identity)` — public, scope REQUIRED (no
    default), authz-first (denies before bytes), reuses
    `services.auth.key_grants.check_scope` on the artifact's key-embedded
    trace_id + buyer scope.
  - `put_once(key, data, content_type)` — write-once; fails if key exists.
  - `head(key)` — {exists, sha256, size}.

Dev-tier backing: local filesystem at
`os.environ.get('AKKI_ARTIFACT_STORE_ROOT', '/tmp/rms_artifact_store')`.
Provider swap = env var change; call sites never change.
"""
from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from services.auth.identity import Identity
from services.auth.key_grants import check_scope


class ScopeInsufficientError(Exception):
    """Raised by `get()` when the caller's scope does not match the artifact.

    Domain-level exception; the router catches this and emits the wire
    shape via `services.auth.auth_refusal.emit('auth_scope_insufficient', ...)`
    (4-code registry closure, mechanism-not-convention discipline).
    """


class ArtifactNotFoundError(Exception):
    """Raised by `get()` when the artifact key does not exist on disk."""


# --- Tier-3 default: local FS at env-var-with-dev-default ---
def _root() -> Path:
    return Path(os.environ.get("AKKI_ARTIFACT_STORE_ROOT", "/tmp/rms_artifact_store"))


# --- Tier-3 default: ext whitelist (extractor output forms, per BCR §6) ---
ALLOWED_EXTENSIONS = frozenset({"json", "csv", "parquet", "bin", "txt"})


class ArtifactKeyExistsError(Exception):
    """Raised by put_once when the key already exists (write-once contract)."""


@dataclass(frozen=True)
class PutOnceResult:
    sha256: str
    size: int


@dataclass(frozen=True)
class HeadResult:
    exists: bool
    sha256: Optional[str]
    size: Optional[int]


def build_key(trace_id: str, artifact_id: str, ext: str) -> str:
    """BCR §3.2:128 key format: `artifacts/{trace_id}/{artifact_id}.{ext}`.

    Ext must be in ALLOWED_EXTENSIONS (Tier-3 default whitelist).
    """
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Extension {ext!r} not in ALLOWED_EXTENSIONS ({sorted(ALLOWED_EXTENSIONS)}). "
            "Add to the whitelist via config to extend."
        )
    if "/" in trace_id or "/" in artifact_id:
        raise ValueError("trace_id and artifact_id must not contain '/'.")
    return f"artifacts/{trace_id}/{artifact_id}.{ext}"


def _abs_path(key: str) -> Path:
    """Resolve a key to its on-disk absolute path within the backing root."""
    return _root() / key


def _get_raw(key: str) -> bytes:
    """PRIVATE — read bytes with NO authz check.

    Callable ONLY from:
      * services/artifact_store/adapter.py (this module — for public `get` chaining)
      * services/artifact_store/atomic_write.py (step 4 head-verify)
      * services/artifact_store/orphan_scan.py (scan enumeration)

    Enforced by AS-G6 grep-negative gate (`test_artifact_store.py::
    test_as_g6_get_raw_has_no_external_callers`). Any caller outside
    the whitelist is a raw-never-egresses violation.
    """
    path = _abs_path(key)
    if not path.is_file():
        raise FileNotFoundError(key)
    return path.read_bytes()


class ArtifactStoreAdapter:
    """S3-class three-op adapter. Provider = config; call sites never change.

    AS-E4 γ split:
      * `get()` PUBLIC — scope required, authz-first, then delegates to `_get_raw()`.
      * `_get_raw()` module-level private — no authz; internal use only.
    """

    def put_once(
        self,
        key: str,
        data: bytes,
        content_type: str,
    ) -> PutOnceResult:
        """AS-B1 write-once. MUST fail if key exists."""
        path = _abs_path(key)
        if path.exists():
            raise ArtifactKeyExistsError(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        sha = hashlib.sha256(data).hexdigest()
        return PutOnceResult(sha256=sha, size=len(data))

    def get(self, key: str, caller_scope: Identity) -> bytes:
        """AS-B3 authz-gated download.

        AS-E4 γ Condition-1: `caller_scope` is REQUIRED (no default).
        Authz check fires BEFORE bytes are read (raw-never-egresses,
        mechanism-not-convention).

        Raises:
          ScopeInsufficientError — caller scope does not match. Router
              translates to 403 `auth_scope_insufficient` via
              `auth_refusal.emit` (4-code registry closure preserved).
          ArtifactNotFoundError — key does not exist on disk.
        """
        if caller_scope is None:  # defensive; type says required
            raise ScopeInsufficientError(
                "Caller scope is required for artifact download."
            )
        # AS-B3: buyer key scope match on the artifact's storage class.
        # An artifact download is a governed_extract path (§4.1 dichotomy).
        # Scope binds to key_class=external, path=governed_extract; the
        # `scope` free-form estate identifier binds via the trace_id
        # prefix (buyers only see their own traces).
        parts = key.split("/")
        if len(parts) < 2 or parts[0] != "artifacts":
            raise ScopeInsufficientError("Malformed artifact key.")
        trace_id = parts[1]
        result = check_scope(
            caller_scope,
            required_class="external",
            required_path="governed_extract",
            required_floor="utterance",
            required_scope=trace_id,
        )
        if not result.granted:
            raise ScopeInsufficientError(
                "Caller identity is authenticated but the required "
                "scope grant is absent for this artifact key."
            )
        # Authz passed — safe to read bytes.
        try:
            return _get_raw(key)
        except FileNotFoundError as exc:
            raise ArtifactNotFoundError(key) from exc

    def head(self, key: str) -> HeadResult:
        """AS-I1 head — {exists, sha256, size}.

        `head` is authz-agnostic by AS-I1 spec (mirrors S3 HEAD
        semantics: metadata-only, no content). Router-level `HEAD /api/
        artifacts/...` enforces the same scope check as `GET` before
        calling this — mechanism-preserved at the wire boundary.
        """
        path = _abs_path(key)
        if not path.is_file():
            return HeadResult(exists=False, sha256=None, size=None)
        data = _get_raw(key)  # internal caller of _get_raw (adapter module)
        return HeadResult(
            exists=True,
            sha256=hashlib.sha256(data).hexdigest(),
            size=len(data),
        )
