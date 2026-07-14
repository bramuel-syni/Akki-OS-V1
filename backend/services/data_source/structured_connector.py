"""Structured-source connector class — MC-E1 α (2026-07-14).

Owner ruling MC-E1 α (2026-07-14):
    'Zero five_rings@v0 mutation. Tabular ingest maps modality=text;
     row-level locator encoded in provenance.locator dict; extraction
     params in reextraction_handle.extraction_params. License_class
     attaches at connector-registration layer, rides receipts, never
     touches units directly.'

Zero contract mutation. Parity 31 held. Every unit produced by this
connector carries:
    * modality = Modality.text (or composite where mixed)
    * provenance.locator = {"table": <str>, "row": <int>, "cols": [...]}
    * reextraction_handle.extraction_params satisfies extraction_params@v0
      text-modality mandatory keys.
    * license_class rides at the connector-registration layer (MC-E4 α
      default: internal_only, fail-closed at outer gate).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import (
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    ReextractionHandleRing,
    RelationalRing,
    ScoreVector,
    SignalRing,
)


DEFAULT_LICENSE_CLASS = "internal_only"


class StructuredConnectorRegistration(BaseModel):
    """Registration record for a structured-source connector.

    Held per-instance in `instance_connectors` collection; license_class
    default = internal_only per MC-E4 α (fail-closed at outer gate for
    S4 egress until operator explicitly upgrades).
    """

    model_config = ConfigDict(extra="forbid")

    connector_id: str = Field(..., description="Stable connector identifier.")
    instance_id: str = Field(..., description="Owning instance.")
    source_ref: str = Field(..., description="Source reference (matches estate inventory).")
    connector_kind: str = Field(default="tabular", description="'tabular', 'db', 'csv', etc.")
    license_class: str = Field(
        default=DEFAULT_LICENSE_CLASS,
        description="MC-E4 α default: internal_only. Set to broader class via rights-posture upgrade path only.",
    )
    extraction_params: Dict[str, Any] = Field(
        default_factory=lambda: {
            "delimiter": ",",
            "encoding": "utf-8",
            "header_mode": "first_row",
            "primary_key": None,
        }
    )
    registered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TabularRow(BaseModel):
    """A single row from a tabular source."""
    model_config = ConfigDict(extra="forbid")

    table: str
    row_index: int
    columns: Dict[str, Any]
    primary_key_value: Optional[str] = None


def _unit_id_from_tabular_row(source_ref: str, row: TabularRow) -> str:
    """Deterministic unit_id from source_ref + row identity."""
    pk = row.primary_key_value or f"row-{row.row_index}"
    return f"tab-{source_ref}-{row.table}-{pk}"


def tabular_row_to_normalized_unit(
    row: TabularRow,
    connector: StructuredConnectorRegistration,
    extraction_run_id: Optional[str] = None,
    extraction_at: Optional[str] = None,
) -> NormalizedUnit:
    """Map one tabular row into a NormalizedUnit via existing five_rings@v0 shape.

    Owner ruling MC-E1 α: zero contract mutation. modality=text; locator
    dict encodes {table, row, cols}; extraction_params carries the
    tabular parameters (text-modality mandatory keys satisfied per
    extraction_params@v0 catalogue).
    """
    ts = extraction_at or datetime.now(timezone.utc).isoformat()
    run_id = extraction_run_id or f"structured-run-{uuid.uuid4().hex[:12]}"
    unit_id = _unit_id_from_tabular_row(connector.source_ref, row)
    return NormalizedUnit(
        unit_id=unit_id,
        provenance=ProvenanceRing(
            source_ref=connector.source_ref,
            modality=Modality.TEXT,
            locator={
                "table": row.table,
                "row": row.row_index,
                "cols": list(row.columns.keys()),
                "primary_key_value": row.primary_key_value,
            },
            speaker_or_author=None,
            context=f"tabular_row[{row.table}]",
        ),
        signal=SignalRing(
            dimensions={},
            depth_judged=False,
        ),
        relational=RelationalRing(edges=[]),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer=f"tabular://{connector.connector_id}/{row.table}/row/{row.row_index}",
            model_id="structured_connector_v0",
            model_version="v0",
            extraction_params={
                # BASE mandatory (extraction_params@v0)
                "provider_id": "structured_connector",
                "provider_version": "v0",
                "extraction_run_id": run_id,
                "extracted_at": ts,
                # TEXT mandatory (extraction_params@v0 TEXT catalogue)
                "source_format": "csv",
                "max_chars": 10_000,
                "encoding": connector.extraction_params.get("encoding", "utf-8"),
                "ocr_engine": None,
                # Connector-specific extras (provider_extras)
                "provider_extras": {
                    "connector_id": connector.connector_id,
                    "connector_kind": connector.connector_kind,
                    "delimiter": connector.extraction_params.get("delimiter", ","),
                    "header_mode": connector.extraction_params.get("header_mode", "first_row"),
                    "primary_key": connector.extraction_params.get("primary_key"),
                },
            },
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.UTTERANCE,
            score_vector=ScoreVector(),
            matrix_rule_ref="tabular_default@v0",
        ),
    )


def ingest_tabular(
    rows: Iterable[TabularRow],
    connector: StructuredConnectorRegistration,
) -> List[NormalizedUnit]:
    """Ingest a batch of tabular rows → NormalizedUnits.

    Provenance-paired; every unit carries connector-scoped locator +
    extraction_params. Census discovers composition via the existing
    mtafiti/census.py path (no new discovery code required).
    """
    ts = datetime.now(timezone.utc).isoformat()
    run_id = f"structured-run-{uuid.uuid4().hex[:12]}"
    return [
        tabular_row_to_normalized_unit(row, connector, extraction_run_id=run_id, extraction_at=ts)
        for row in rows
    ]


def license_class_permits_s4_egress(license_class: str) -> bool:
    """MC-E4 α fail-closed gate.

    'Default internal_only, fail-closed: artifacts derived from
     default-classed units refuse the outer gate until rights are
     explicitly set.' Only explicit non-default classes cross.
    """
    return license_class not in {DEFAULT_LICENSE_CLASS, "unknown", ""}
