"""Trust-receipt allowlist — Amendment 1 (2026-07-06 B-5a Stage B dispatch).

Owner ruling verbatim [Owner ruling, Phase 8 Stage B-5a dispatch,
2026-07-06]:
    "The anonymous/lesser-role view is built up from the public
     trust-receipt spec (fact + fingerprint, allowlist), byte-equivalent
     to that spec — never the full record with fields masked off.
     Blocklist masking makes every future record field public-by-default
     until someone remembers to hide it; allowlist inverts the failure
     mode. Full record renders only for dpo / master_admin."

Doctrinal note (from Owner): *"Blocklist masking is public-by-default
with future fields; allowlist-up inverts the failure mode."*

The allowlist below is the SINGLE SOURCE OF TRUTH for what an anonymous
or lesser-role caller may see when hitting
`GET /api/northena/trace/{trace_id}`. Any new field added to
`TraceLensEnvelope_v0` in the future defaults to NOT-visible-anonymously
unless explicitly added here.

Byte-equivalence target: the public trust-receipt spec at
`services/synisense/shield/trust_receipt.py::build_trust_receipt`
carries the receipt_id + audit_id + timestamp + hashes shape ("fact +
fingerprint"). The trace-lens envelope is a wider structure; the
allowlist projects it down to a fact+fingerprint-shaped subset.

For the trace-lens envelope, the "fact + fingerprint" projection is:
  * `trace_id` — the identifier (fact)
  * `resolved_at` — the resolution timestamp (fact)
  * `run_ids` — the runs this trace touched (fact, opaque IDs)
  * `engines_touched` — which engines saw it (fingerprint of the pipeline)

Everything else (`ledger_rows`, `solva_traces`, `mining_plans`,
`registry_records`, `registry_freshness`) is FULL-RECORD content —
NOT visible anonymously. Rendered ONLY for `dpo` / `master_admin`.

Two named gates enforce this:
  * `test_anonymous_trace_view_contains_no_field_outside_receipt_spec`
     — grep-negative gate; any field in the anonymous response not in
     ANONYMOUS_TRACE_VIEW_ALLOWLIST → FAIL.
  * `test_anonymous_trace_view_contains_all_receipt_spec_fields`
     — positive gate; the anonymous view carries EXACTLY the allowlisted
     field set (byte-equivalent to spec, not a strict subset).
"""
from __future__ import annotations

from typing import Any, Dict, FrozenSet


# LOAD-BEARING: the trust-receipt "fact + fingerprint" allowlist for
# anonymous trace-view responses. Do NOT expand without Owner sign-off;
# expanding is a governance-semantic contact per Owner escalation-cap.
ANONYMOUS_TRACE_VIEW_ALLOWLIST: FrozenSet[str] = frozenset({
    "trace_id",
    "resolved_at",
    "run_ids",
    "engines_touched",
})


def project_to_anonymous_view(full_envelope_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Build UP the anonymous response from the allowlist.

    Owner-directed posture (2026-07-06): pick ONLY allowlisted fields;
    NEVER pop/redact from the full record. If a field is not in the
    allowlist, it does not appear in the anonymous view — even if it
    exists on `full_envelope_dict`.

    This is intentional: any future addition to `TraceLensEnvelope_v0`
    is anonymous-invisible by default (opposite failure mode from
    blocklist masking).
    """
    projection: Dict[str, Any] = {}
    for field_name in ANONYMOUS_TRACE_VIEW_ALLOWLIST:
        if field_name in full_envelope_dict:
            projection[field_name] = full_envelope_dict[field_name]
    return projection


def has_full_record_authority(roles: list) -> bool:
    """Only `dpo` or `master_admin` (or `admin` super-role) see the full
    trace-lens record. Everyone else — anonymous or otherwise — sees
    the allowlist projection.
    """
    role_set = set(roles or [])
    return "dpo" in role_set or "master_admin" in role_set or "admin" in role_set
