"""Outer-gate mint — the "purged mint" primitive (§21.2).

The mint holds a keyed cryptographic seed used to pseudonymise identifiers.
The key is generated per mint-window. When the window closes, the key is
**purged** — destroyed from memory + never persisted — which is what makes
the transform irreversible: without the key, no polynomial-time inversion
exists (HMAC-SHA256 PRF property).

**Never persist the key.** The mint stores only the key fingerprint (SHA-256
of the key). The fingerprint is what lands in `OuterGateReceipt.key_fingerprint`
so audit consumers can verify key-lineage claims without recovering the key.

**Cousin citation (transitive-lift):** the HMAC-SHA256 keyed-hex pattern +
secrets.token_bytes(32) key generation is transitive from
`services/synisense/shield/trust_receipt.py` (Shield's per-tenant key
derivation + HMAC signature construction). Same crypto primitive shape; the
G6 addition is the purge-lifecycle discipline (§21.2 "purged mint") that
Shield's per-tenant keys don't have (Shield keys are stable, mint keys are
destroyed at window close).
"""
from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class MintWindow:
    """A single mint window. Key is held in memory; purge zeroes it."""
    mint_window_id: str
    _key: bytes = field(repr=False)  # SUPPRESSED from repr. Never log.
    key_fingerprint: str
    opened_at: str
    purged: bool = False


def _new_key(nbytes: int = 32) -> bytes:
    """Generate a cryptographically strong key.

    Test hook: `AKKI_G6_MINT_KEY_TEST_OVERRIDE` env may inject a deterministic
    key for reproducible snapshot testing. In production the override MUST be
    unset — snapshot test asserts this.
    """
    override = os.environ.get("AKKI_G6_MINT_KEY_TEST_OVERRIDE")
    if override is not None:
        return override.encode("utf-8")
    return secrets.token_bytes(nbytes)


def _fingerprint(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()


class MintRegistry:
    """In-memory mint registry. `open_window()` mints a key; `purge_window()`
    destroys it. Once purged, the window's key cannot be recovered.

    v0 posture: single-process, in-memory. A production build would persist
    the FINGERPRINT (never the key) and mint windows across restarts.
    """

    def __init__(self) -> None:
        self._windows: Dict[str, MintWindow] = {}

    def open_window(self, timestamp: Optional[str] = None) -> MintWindow:
        wid = f"mint-{uuid.uuid4().hex[:12]}"
        key = _new_key()
        window = MintWindow(
            mint_window_id=wid,
            _key=key,
            key_fingerprint=_fingerprint(key),
            opened_at=timestamp or "",
        )
        self._windows[wid] = window
        return window

    def get(self, mint_window_id: str) -> MintWindow:
        window = self._windows.get(mint_window_id)
        if window is None:
            raise KeyError(f"unknown mint_window_id={mint_window_id!r}")
        if window.purged:
            raise ValueError(
                f"mint_window_id={mint_window_id!r} has been purged; "
                f"the key is unrecoverable by design (§21.2 purged mint)."
            )
        return window

    def purge_window(self, mint_window_id: str) -> None:
        """Destroy the key material. Post-purge, the mint window is
        unusable — this is the irreversibility bar (§21.2).
        """
        window = self._windows.get(mint_window_id)
        if window is None:
            return
        # Overwrite the key bytes best-effort. Python's bytes are immutable,
        # but replacing the reference + suppressing repr is the substrate posture.
        window._key = b""
        window.purged = True


def pseudonymise(window: MintWindow, plaintext: str) -> str:
    """HMAC-SHA256(window.key, plaintext) → hex.

    Deterministic within-window: same plaintext → same pseudonym. Cross-window:
    same plaintext under different keys → different pseudonyms (linkability
    only within the mint window; the purge destroys the linkage for future
    windows).
    """
    if window.purged:
        raise ValueError(
            f"mint_window_id={window.mint_window_id!r} has been purged; "
            f"cannot pseudonymise (§21.2 purged mint)."
        )
    mac = hmac.new(window._key, plaintext.encode("utf-8"), hashlib.sha256)
    return mac.hexdigest()
