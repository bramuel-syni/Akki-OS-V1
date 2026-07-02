"""Mtafiti — census walker + two-layer measure + Registry writer (mandate §7).

Package layout (mandate §7 verbatim):
  * census.py       — objective-blind estate walk (§8)
  * declaration.py  — feed-level source-standing baseline (§9)
  * inference.py    — learned detectors; detections only (§10)
  * measure.py      — composes baseline + (admitted) detections (§11)
  * verdict.py      — Matrix lookup → defensibility_class (§11)
  * registry.py     — append + read Registry records (§13)
  * interfaces.py   — opaque handles: MatrixHandle (reused from Solva §7)
  * source_standing.py — MEA placeholder table (§9 + user directive (4))
  * v3_overlay.py   — admission gate: DARK closed-seam at G4 (§12)

Contracts (frozen, snapshot + invariant): `contracts/mtafiti_registry.py`.
"""
