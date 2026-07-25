"""PartitionSchema@v0 — versioned columnar memory-mappable partition schema (EAB-3 A5 seal).

33rd frozen contract (Parity 32→33 seal · EAB-3 execution atomic · 2026-07-24 ·
Owner-ruled 2026-07-25 composition (a1) single-contract landing).

Additive to the 32 prior frozen contracts; ZERO mutation of any prior freeze.
Standing Rule v3 byte-identity attest on all 32 prior contracts + snapshots
fires this atomic (see `tests/invariants/test_partition_schema_v0_envelope.py::
test_parity_33_contracts_and_snapshots` and
`::test_prior_32_contracts_byte_identity_under_eab3`).

Sanction:
  * `docs/rulings/eab_3_e1_2026_07_24.md` — Owner ruled Tier-1 E1 = (a1)
    single-contract landing (SHA `319d9f14ce35625ed62bc8f033b48ea7f7bdc9522fb15fa191ec6e64e4bd371f`).
  * `docs/stage_a_proposals/eab_3_stage_a.md` §5.1 sub-option (a1) verbatim
    (SHA `907ac439f05dd7b00985ce568228bc24e0e903f40c2d5986dfaa73d592d642c7`).
  * `docs/requirements/eab_tier1_adoption_spec_v1.1.md` Part VI · R-A5.1 line 137
    (SHA `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9`).

R-A5.1 verbatim (byte-carried):
  *"Evidence consumed by interactive surfaces is precomputed into versioned,
  columnar, memory-mappable partitions keyed on the dimensions the surface
  actually queries (keys are per-surface configuration; extension only via
  schema versioning). A request is partition reads plus arithmetic."*

Ruled composition (Owner-authored 2026-07-25 · FINAL):
  * (a1) One-contract landing · schema definition + version-instance record
    fields co-located. Reasoning verbatim from Owner ruling: *"(a2)'s
    schema-vs-instance separation is available later via PartitionSchema_v1
    additive versioning at the moment it is needed — the Service1Refusal
    pattern — whereas its double-seal cost is paid now; (a1) matches the
    EAB-2 single-writer end-state precedent and is the D-6-cleanest linear-
    additive progression. Options (b) and (c) remain rejected at pre-name."*

Envelope shape (9 fields · single-contract landing per Owner ruling (a1)):
  * partition_id: str
  * schema_version: str
  * key_dimensions: List[str]
  * receipt_set_ref: str
  * promoted_at: str (ISO-8601 UTC)
  * superseded_at: Optional[str]
  * partition_shape_kind: Literal["columnar_memmap"]
  * size_bytes: int
  * instance_id: str

Lineage discipline (R-A5.5 verbatim byte-carried):
  *"Every partition version records the receipt set it was built from; every
  answer cites partition versions; the chain number→partition→receipts→
  operations is mechanically walkable with zero additional retrieval at
  request time (the citation IS the identifier the request touched)."*
  `receipt_set_ref` is the FK carrier for this discipline.

Refresh discipline (R-A5.3 verbatim byte-carried):
  *"Partition refresh is a cold-path batch job; the previous version serves
  until the new version is atomically promoted; promotion is ledgered."*
  `promoted_at` / `superseded_at` carry the atomic-promotion ceremony
  timestamps; ledger row lands via `PROM-S3-append-only-ledger` +
  `PROM-S3-mechanical-audit-of-promotion`.

Per-instance scoping (MC-E2 α reflexive discipline extended):
  `instance_id` scoping ensures partitions do not cross instance boundary
  (multi-instance operability discipline preserved from
  `akki.instance.seams_scoped_by_instance_id` v1 §S1).

Snapshot invariant:
  `tests/invariants/partition_schema_v0.contract_snapshot.json`
  compared in `tests/invariants/test_partition_schema_v0_envelope.py`.
  Any drift fails CI (Operating Protocol §1.7).

§0-CAL §23.1 per-line enumeration: mandatory on this contract module
(backend/contracts/**). Each declarative line below carries a rung
verdict-line in the accompanying attest table at
`tests/invariants/test_partition_schema_v0_envelope.py::CAL_23_1_ENUM`.

Class E annotation (Owner ruling ITEM 1 forward-binding annotation ·
Change Order A3.4 filed at ITEM 2): the partition_shape_kind enumeration
is a Class E engine parameter under the Rules Taxonomy · pinned per engine
version · changed only via version bumps with evaluation verdicts · any
future runtime tunability takes the E→O promotion path per Change Order
A3.2 · no other route. Extension via schema versioning per R-A5.1 lands
future variants as `PartitionSchema_v1` (like `Service1Refusal_v1` did
for A3 · zero mutation of `PartitionSchema_v0`).
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class PartitionSchema_v0(BaseModel):
    """Versioned columnar memory-mappable partition schema · single-contract landing per Owner ruling (a1).

    Emitted by the partition-refresh cold-path batch job at atomic promotion.
    Read by session-working-set service at session-open (partition-version
    binding · promotion invalidates dependents per R-A5.4).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # ── 9-field envelope · single-contract landing per Owner ruling composition (a1) ──

    partition_id: str = Field(
        ...,
        description=(
            "Partition family identifier. Groups all versions of a partition "
            "across time. Same `partition_id` across promotions represents "
            "the same logical partition; distinct `partition_id` values "
            "represent distinct partitions. Per-surface configuration per "
            "R-A5.1 (*'keys are per-surface configuration; extension only "
            "via schema versioning'*)."
        ),
    )
    schema_version: str = Field(
        ...,
        description=(
            "Partition schema version identifier. Extension via schema "
            "versioning per R-A5.1 verbatim. Extension = new schema_version "
            "value (semantic version string). Same schema_version across "
            "promotions means field-set and key-dimensions are unchanged."
        ),
    )
    key_dimensions: List[str] = Field(
        ...,
        description=(
            "Keys the partition is keyed on. Per-surface configuration per "
            "R-A5.1 verbatim (*'keys are per-surface configuration'*). List "
            "of dimension names (registry-vocabulary per "
            "`PROM-S1-honesty-grammar-source-labels`). Extension only via "
            "schema_version bump."
        ),
    )
    receipt_set_ref: str = Field(
        ...,
        description=(
            "Lineage FK · partition version records the receipt set it was "
            "built from per R-A5.5 verbatim. Walkable chain: number → "
            "partition → receipts → operations · zero additional retrieval "
            "at request time. `receipt_set_ref` is the identifier the "
            "request touched (per R-A5.5: *'the citation IS the identifier "
            "the request touched'*). Registry attachment: "
            "`PROM-S3-audit-trail-immutable` + `PROM-S3-append-only-ledger`."
        ),
    )
    promoted_at: str = Field(
        ...,
        description=(
            "ISO-8601 UTC timestamp of atomic promotion (R-A5.3 verbatim: "
            "*'the previous version serves until the new version is "
            "atomically promoted; promotion is ledgered'*). Emitted at the "
            "moment the partition becomes read-authoritative. Immutable "
            "post-write per `PROM-S3-append-only-ledger`."
        ),
    )
    superseded_at: Optional[str] = Field(
        default=None,
        description=(
            "ISO-8601 UTC timestamp of supersession (when a later "
            "PartitionSchema@v0 with the same partition_id was atomically "
            "promoted). None on the current-authoritative partition version. "
            "Immutable once set per `PROM-S3-append-only-ledger`. Preserves "
            "historical readability (previous-version-serves-until-atomic-"
            "promotion trail is walkable via superseded_at chain)."
        ),
    )
    partition_shape_kind: Literal["columnar_memmap"] = Field(
        default="columnar_memmap",
        description=(
            "Storage shape discriminator. Initial landing is single-value "
            "`columnar_memmap` per R-A5.1 verbatim (*'versioned, columnar, "
            "memory-mappable partitions'*). Future variants (e.g., "
            "`row_hash_index`, `reference_tree`) via schema versioning per "
            "R-A5.1 (*'extension only via schema versioning'*) — land as "
            "`PartitionSchema_v1` following the `Service1Refusal_v1` "
            "additive-versioning pattern. Class E engine parameter under "
            "Rules Taxonomy A3.4 (Owner ITEM 1 forward-binding annotation) "
            "· pinned per engine version · changed only via version bumps "
            "with evaluation verdicts · runtime tunability requires E→O "
            "promotion path per A3.2."
        ),
    )
    size_bytes: int = Field(
        ...,
        ge=0,
        description=(
            "Materialized partition size in bytes. Reported at promotion "
            "time for latency-telemetry and load-test-at-10x-concurrency "
            "planning (AC-A5.b + AC-A5.c). Non-negative invariant enforced "
            "at contract boundary."
        ),
    )
    instance_id: str = Field(
        ...,
        description=(
            "Multi-instance scope key. Partitions do not cross instance "
            "boundary (MC-E2 α reflexive discipline extended from seam-"
            "values to partitions per Registry v1 §S1 "
            "`akki.instance.seams_scoped_by_instance_id`). Session-"
            "working-set reads filter by `instance_id` at session-open."
        ),
    )
