"""Mtafiti Registry — append/upsert Registry records; freshness check (§13).

Persistent write to Mongo (mirrors Northena Ledger pattern). Frozen
collection name; contract-grade rows.

Composition (`compose_record`) is the orchestrator that pulls census +
declaration + measure + verdict + freshness into a single
`MtafitiRegistryRecord`.

Freshness (§13, §17 #8): L1 = `logged_date`; L2 = `structural_signature`
(deferred at G4 until fixture emits it). Freshness re-measures only the
affected region (returns list of source_refs to re-measure).
"""
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional

from contracts.five_rings import NormalizedUnit
from contracts.mtafiti_registry import (
    MTAFITI_REGISTRY_COLLECTION,
    FreshnessStamp,
    MtafitiRegistryRecord,
)
from core import db
from services.mtafiti import declaration, inference, measure, source_standing, v3_overlay
from services.mtafiti.census import SourceCandidate, census
from services.mtafiti.v3_overlay import V3Result, V3Thresholds
from services.mtafiti.verdict import assign_verdict, default_handle


def _logged_date_from_unit(unit: NormalizedUnit) -> str:
    """Extract L1 freshness (`logged_date`) from fixture context; fallback to now(UTC)."""
    try:
        ctx = json.loads(unit.provenance.context or "{}")
        return ctx.get("logged_date") or datetime.now(timezone.utc).isoformat()
    except (json.JSONDecodeError, TypeError):
        return datetime.now(timezone.utc).isoformat()


def _structural_signature_from_unit(unit: NormalizedUnit) -> Optional[str]:
    """L2 freshness — Substrate-Drop v1 G4-prep TODO.

    Preferred source: fixture-embedded `structural_signature` (extends
    the generator per the TODO; on-disk fixture already carries the field
    in `provenance.context` JSON). Fallback: deterministic 16-hex sha256
    of `unit.reextraction_handle.raw_pointer` — a valid provisional
    computation that satisfies L2's delta-detection purpose without
    contract mutation.
    """
    try:
        ctx = json.loads(unit.provenance.context or "{}")
        sig = ctx.get("structural_signature")
        if sig:
            return sig[:16]  # canonical 16-hex form
    except (json.JSONDecodeError, TypeError):
        pass
    # Fallback: compute over raw_pointer. Deterministic + delta-sensitive.
    ptr = unit.reextraction_handle.raw_pointer
    return hashlib.sha256(ptr.encode("utf-8")).hexdigest()[:16]


def compose_record(
    unit: NormalizedUnit,
    *,
    v3_thresholds: Optional[V3Thresholds] = None,
    v3_result: Optional[V3Result] = None,
) -> MtafitiRegistryRecord:
    """Compose one MtafitiRegistryRecord from a NormalizedUnit.

    Pipeline: census → declaration → inference → measure → verdict →
    freshness → record. Objective-blind (no ObjectiveRequest input).

    V3 overlay is closed-seam at G4 (`v3_thresholds=None`).
    """
    # 1. Census (single-unit slice — the fixture-based estate walk):
    (cand,) = list(census([unit]))

    # 2. Declaration baseline (deterministic, feed-level):
    table = source_standing.table()
    standing = declaration.declared_standing(cand.feed_id, table)

    # 3. Inference (dark stubs at G4; V3-closed seam):
    detections = inference.detect(unit, estate_index=None)
    admitted = v3_overlay.overlay_admitted(v3_thresholds, v3_result)
    runtime_mode = v3_overlay.runtime_mode(v3_thresholds, v3_result)

    # 4. Measure (baseline stands alone when overlay closed):
    ctx = unit.provenance.context or ""
    logged_date = _logged_date_from_unit(unit)
    score = measure.measure(
        unit_context=ctx,
        unit_logged_date=logged_date,
        standing=standing,
        detections=detections,
        v3_admitted=admitted,
    )

    # 5. Verdict (Matrix lookup):
    claim_genre, matrix_context = measure.resolve_matrix_axes(ctx)
    verdict = assign_verdict(claim_genre, matrix_context, default_handle())

    # 6. Freshness (L1 + L2):
    freshness = FreshnessStamp(
        logged_date=logged_date,
        structural_signature=_structural_signature_from_unit(unit),
    )

    return MtafitiRegistryRecord(
        source_ref=cand.source_ref,
        region=cand.region,
        feed_id=cand.feed_id,
        sensitivity=cand.sensitivity,
        defensibility_measure=score,
        defensibility_runtime_mode=runtime_mode,
        matrix_rule_ref=verdict.matrix_rule_ref,
        defensibility_class=verdict.defensibility_class,
        freshness_stamp=freshness,
    )


async def upsert(record: MtafitiRegistryRecord) -> None:
    """Append or update. Key: source_ref. Mongo upsert with $set."""
    await db[MTAFITI_REGISTRY_COLLECTION].update_one(
        {"source_ref": record.source_ref},
        {"$set": record.model_dump(mode="json")},
        upsert=True,
    )


async def read_all() -> List[Dict]:
    """Return all Registry records (unordered). Used by Targeta core."""
    return [r async for r in db[MTAFITI_REGISTRY_COLLECTION].find({}, {"_id": 0})]


async def read_by_source_ref(source_ref: str) -> Optional[Dict]:
    return await db[MTAFITI_REGISTRY_COLLECTION].find_one(
        {"source_ref": source_ref}, {"_id": 0}
    )


def detect_stale_records(
    prior: List[Dict],
    current_units: List[NormalizedUnit],
) -> List[str]:
    """Freshness § 17 #8: re-measure ONLY affected region.

    Compares L1 + L2 stamps between prior Registry rows and current unit
    scan. Returns source_refs that need re-measurement (stale). Does
    NOT return the whole estate — invariant #8 enforced.
    """
    prior_by_ref = {p["source_ref"]: p for p in prior}
    stale: List[str] = []
    for unit in current_units:
        ref = unit.provenance.source_ref
        if ref not in prior_by_ref:
            stale.append(ref)
            continue
        prior_stamp = prior_by_ref[ref].get("freshness_stamp", {})
        current_l1 = _logged_date_from_unit(unit)
        current_l2 = _structural_signature_from_unit(unit)
        if prior_stamp.get("logged_date") != current_l1:
            stale.append(ref)
        elif prior_stamp.get("structural_signature") != current_l2:
            stale.append(ref)
    return stale
