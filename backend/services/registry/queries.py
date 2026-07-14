"""Standing Queries as CI — engine for Q1 (redundancy) · Q2 (orphans) · Q3 (gaps).

Registry Doctrine §8.1.a · Owner rulings (2026-07-11 · SQ-E1 γ + cross-reference):
  - Two files per query: `q{n}_archaeological.md` + `q{n}_mechanical.md`.
  - Archaeological files reproduce v0.md §4/§5 + consolidation_log_v0.md byte-identical.
  - Mechanical files carry fresh scan; entries overlapping archaeological subjects
    annotated `overlaps: <finding_id>`, never raised as new (PERMANENT rule).
  - Fail-loud + HALT for Owner on baseline reproduction failure (SQ-G-Baseline).
  - Report-level artifacts: NEVER build-failing. Retirement/merge remain ruled actions.
  - Rung 1 · Deterministic pure-function throughout.

Ruling record: /app/docs/rulings/standing_queries_sq_e1.md
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.services.registry.parser import (
    CONSOLIDATION_LOG_PATH,
    REPO_ROOT,
    SUPPLEMENT_PATHS,
    V0_PATH,
    parse_source,
    sha256_file,
)
from backend.services.registry.validator import PART_II_JOURNEY_STEPS


QUERIES_DIR = REPO_ROOT / "docs" / "registry" / "queries"
MACHINE_YAML_PATH = REPO_ROOT / "docs" / "registry" / "machine" / "registry.yaml"

REPORT_HEADER = (
    "THIS ARTIFACT IS REPORT-LEVEL · NEVER BUILD-FAILING · "
    "RETIREMENT/MERGE REMAINS RULED ACTION"
)


# ---------------------------------------------------------------------------
# Archaeological carry-over
# ---------------------------------------------------------------------------


@dataclass
class ArchaeologicalFinding:
    finding_id: str
    subject: str
    source: str
    ruling_tag: str
    ruling_ref: str
    owner_markers: list[str] = field(default_factory=list)
    observation: str = ""
    subject_identifiers: tuple[str, ...] = ()


def _extract_subject_identifiers(subject: str, observation: str = "") -> tuple[str, ...]:
    """Extract identifier tokens from a subject/observation for cross-reference matching.

    Recognized tokens: `EE-G[0-9]+`, `MAN-G[0-9]+`, `V1-G[0-9]+`, `RT-*`, `PROM-*`,
    `S1..S5` journey steps, and mandate-named prose like `bookkeeping.audit_ledger`.
    """
    blob = f"{subject}\n{observation}"
    ids: set[str] = set()
    for pat in [
        r"EE-G[0-9]+",
        r"MAN-G[0-9]+",
        r"V1-G[0-9]+",
        r"RT-\*|RT-[A-Za-z_0-9]+",
        r"PROM-[A-Za-z0-9\-]+",
        r"S[1-5]\.[a-z][a-z0-9\-]*",
    ]:
        ids.update(re.findall(pat, blob))
    # Mandate-named dotted paths (e.g., "bookkeeping.audit_ledger").
    for m in re.finditer(r"`([a-z][a-z0-9_.\-]+)`", blob):
        ids.add(m.group(1))
    # Whole-S5 marker (Q3-04 "S5 (all journey steps)").
    if "S5" in blob and "S5." not in blob:
        ids.add("S5")
    return tuple(sorted(ids))


def load_archaeological_q2_q3(model: Any) -> list[ArchaeologicalFinding]:
    """Load Q2 + Q3 archaeological findings from parsed v0.md model."""
    out: list[ArchaeologicalFinding] = []
    for f in model.findings:
        out.append(
            ArchaeologicalFinding(
                finding_id=f.finding_id,
                subject=f.subject,
                source=f.source,
                ruling_tag=f.ruling_tag,
                ruling_ref=f.ruling_ref,
                owner_markers=f.owner_markers,
                observation=f.observation,
                subject_identifiers=_extract_subject_identifiers(f.subject, f.observation),
            )
        )
    return out


@dataclass
class Q1ArchaeologicalEntry:
    entry_id: str  # e.g., "CL-1.1"
    kind: str  # "MERGE" | "TIE-BROKE-TOWARD-DISTINCT"
    promise_id: str
    section_ref: str
    raw_text: str
    subject_identifiers: tuple[str, ...] = ()


_CL_HEADING_RE = re.compile(
    r"^### §(?P<num>\d+\.\d+)\s+(?P<kind>MERGE|`TIE-BROKE-TOWARD-DISTINCT`|TIE-BROKE-TOWARD-DISTINCT)\s+—\s+(?P<rest>.+)$"
)


def load_archaeological_q1() -> list[Q1ArchaeologicalEntry]:
    """Parse consolidation_log_v0.md §1 for Q1 archaeological decisions."""
    text = CONSOLIDATION_LOG_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    entries: list[Q1ArchaeologicalEntry] = []
    current_heading: tuple[str, str, str] | None = None
    current_block: list[str] = []
    for line in lines:
        m = _CL_HEADING_RE.match(line)
        if m:
            if current_heading:
                heading_num, kind, rest = current_heading
                promise_match = re.search(r"PROM-[A-Za-z0-9\-]+", rest)
                promise_id = promise_match.group(0) if promise_match else ""
                block_text = "\n".join(current_block)
                entries.append(
                    Q1ArchaeologicalEntry(
                        entry_id=f"CL-{heading_num}",
                        kind=kind.strip("`"),
                        promise_id=promise_id,
                        section_ref=f"consolidation_log_v0.md §{heading_num}",
                        raw_text=block_text,
                        subject_identifiers=_extract_subject_identifiers(promise_id, block_text),
                    )
                )
            current_heading = (m.group("num"), m.group("kind").strip("`"), m.group("rest"))
            current_block = [line]
            continue
        if line.startswith("## §") and current_heading:
            # End of §1 section; flush pending entry.
            heading_num, kind, rest = current_heading
            promise_match = re.search(r"PROM-[A-Za-z0-9\-]+", rest)
            promise_id = promise_match.group(0) if promise_match else ""
            block_text = "\n".join(current_block)
            entries.append(
                Q1ArchaeologicalEntry(
                    entry_id=f"CL-{heading_num}",
                    kind=kind,
                    promise_id=promise_id,
                    section_ref=f"consolidation_log_v0.md §{heading_num}",
                    raw_text=block_text,
                    subject_identifiers=_extract_subject_identifiers(promise_id, block_text),
                )
            )
            current_heading = None
            current_block = []
            continue
        if current_heading:
            current_block.append(line)
    if current_heading:
        heading_num, kind, rest = current_heading
        promise_match = re.search(r"PROM-[A-Za-z0-9\-]+", rest)
        promise_id = promise_match.group(0) if promise_match else ""
        block_text = "\n".join(current_block)
        entries.append(
            Q1ArchaeologicalEntry(
                entry_id=f"CL-{heading_num}",
                kind=kind,
                promise_id=promise_id,
                section_ref=f"consolidation_log_v0.md §{heading_num}",
                raw_text=block_text,
                subject_identifiers=_extract_subject_identifiers(promise_id, block_text),
            )
        )
    return entries


# ---------------------------------------------------------------------------
# Mechanical scans
# ---------------------------------------------------------------------------


def _prom_tokens(promise_field: list[str]) -> frozenset[str]:
    return frozenset(p for p in promise_field if p.startswith("PROM-"))


def _canonicalize_service_trace(st: str) -> str:
    """Normalize aliases + strip parenthetical annotations."""
    base = re.sub(r"\s*\(.*\)$", "", st).strip()
    alias_map = {
        "S3.prove": "S3.prove-end-to-end",
        "S4.verify": "S4.verify-receipt",
    }
    return alias_map.get(base, base)


def _numeric_cost_prefix(cost: str) -> tuple[bool, int]:
    """Return (has_numeric, value). 'unknown' or non-numeric → (False, 0)."""
    m = re.match(r"^\s*(\d+)", cost)
    if not m:
        return False, 0
    return True, int(m.group(1))


@dataclass
class Q1MechanicalPair:
    fid_a: str
    fid_b: str
    shared_promises: tuple[str, ...]
    shared_surface: str
    cost_rank_key: tuple[int, int, int]  # (unknown_flag, sum, tiebreaker)
    subject_identifiers: tuple[str, ...] = ()


def scan_q1_redundancy(model: Any) -> list[Q1MechanicalPair]:
    """Mechanical Q1: pairs of function rows with same PROM-set AND same surface."""
    functions = model.functions
    pairs: list[Q1MechanicalPair] = []
    for i, a in enumerate(functions):
        a_proms = _prom_tokens(a.promise)
        if not a_proms:
            continue
        for b in functions[i + 1 :]:
            b_proms = _prom_tokens(b.promise)
            if a_proms != b_proms:
                continue
            if a.surface != b.surface or not a.surface:
                continue
            has_a, val_a = _numeric_cost_prefix(a.cost)
            has_b, val_b = _numeric_cost_prefix(b.cost)
            # Sort key: unknowns to end; numeric ascending by sum.
            unknown_flag = 0 if (has_a and has_b) else 1
            cost_sum = (val_a + val_b) if (has_a and has_b) else 0
            pairs.append(
                Q1MechanicalPair(
                    fid_a=a.function_id,
                    fid_b=b.function_id,
                    shared_promises=tuple(sorted(a_proms)),
                    shared_surface=a.surface,
                    cost_rank_key=(unknown_flag, cost_sum, hash((a.function_id, b.function_id)) & 0xFFFF),
                    subject_identifiers=tuple(sorted(a_proms | {a.function_id, b.function_id, a.surface})),
                )
            )
    pairs.sort(key=lambda p: p.cost_rank_key)
    return pairs


@dataclass
class Q2MechanicalEntry:
    function_id: str
    sub_case: str  # "a" | "b" | "c" | "d"
    detail: str
    subject_identifiers: tuple[str, ...] = ()


def scan_q2_orphans(model: Any) -> list[Q2MechanicalEntry]:
    known_ids = {p.promise_id for p in model.promises}
    entries: list[Q2MechanicalEntry] = []
    for f in model.functions:
        # (a) empty promise field.
        if not f.promise:
            entries.append(Q2MechanicalEntry(f.function_id, "a", "empty promise field",
                                             subject_identifiers=(f.function_id,)))
        # (b) NO PROM- token resolves to promise_id.
        proms = _prom_tokens(f.promise)
        if proms and not any(p in known_ids for p in proms):
            entries.append(Q2MechanicalEntry(f.function_id, "b",
                                             f"no PROM-token resolves: {sorted(proms)}",
                                             subject_identifiers=(f.function_id, *sorted(proms))))
        # (c) empty service_trace.
        if not f.service_trace:
            entries.append(Q2MechanicalEntry(f.function_id, "c", "empty service_trace field",
                                             subject_identifiers=(f.function_id,)))
        # (d) service_trace step not in PART_II_JOURNEY_STEPS (parenthetical-stripped).
        for st in f.service_trace:
            if st.startswith("(") and st.endswith(")"):
                continue
            canonical = _canonicalize_service_trace(st)
            if canonical == "S1..S5":
                continue
            if canonical not in PART_II_JOURNEY_STEPS:
                entries.append(Q2MechanicalEntry(
                    f.function_id, "d",
                    f"service_trace step {st!r} (canonical {canonical!r}) "
                    f"not in PART_II_JOURNEY_STEPS",
                    subject_identifiers=(f.function_id, canonical),
                ))
    return entries


@dataclass
class Q3MechanicalEntry:
    sub_case: str  # "a" | "b"
    subject: str
    detail: str
    subject_identifiers: tuple[str, ...] = ()


def scan_q3_gaps(model: Any) -> list[Q3MechanicalEntry]:
    entries: list[Q3MechanicalEntry] = []
    # (a) promise_id in top-level with zero citations.
    cite_counts: dict[str, int] = {p.promise_id: 0 for p in model.promises}
    for f in model.functions:
        for p in _prom_tokens(f.promise):
            if p in cite_counts:
                cite_counts[p] += 1
    for pid, cnt in cite_counts.items():
        if cnt == 0:
            entries.append(Q3MechanicalEntry("a", pid, "promise has zero citing function rows",
                                             subject_identifiers=(pid,)))
    # (b) PART_II journey step with zero citing function rows (alias-equivalent coverage).
    step_covered: dict[str, bool] = {step: False for step in PART_II_JOURNEY_STEPS}
    canonical_alias_targets = {"S3.prove-end-to-end", "S4.verify-receipt"}
    for f in model.functions:
        for st in f.service_trace:
            base = _canonicalize_service_trace(st)
            if base in step_covered:
                step_covered[base] = True
                # Cross-cover the alias short form too.
                if base == "S3.prove-end-to-end":
                    step_covered["S3.prove"] = True
                if base == "S4.verify-receipt":
                    step_covered["S4.verify"] = True
    # Emit gap entries only for the canonical (long) forms — aliases mirror them.
    aliases_short = {"S3.prove", "S4.verify"}
    for step, covered in sorted(step_covered.items()):
        if step in aliases_short:
            continue
        if not covered:
            entries.append(Q3MechanicalEntry("b", step,
                                             f"PART_II journey step {step!r} has zero citing functions",
                                             subject_identifiers=(step,)))
    return entries


# ---------------------------------------------------------------------------
# Cross-reference index + overlap annotation
# ---------------------------------------------------------------------------


def build_archaeological_index(
    q1_arch: list[Q1ArchaeologicalEntry],
    q23_arch: list[ArchaeologicalFinding],
) -> dict[str, str]:
    """Return `{subject_identifier: finding_id_or_entry_id}` for cross-reference."""
    idx: dict[str, str] = {}
    for e in q1_arch:
        for sid in e.subject_identifiers:
            idx.setdefault(sid, e.entry_id)
    for f in q23_arch:
        for sid in f.subject_identifiers:
            idx.setdefault(sid, f.finding_id)
    return idx


def overlaps_for(mech_subject_identifiers: tuple[str, ...], arch_index: dict[str, str]) -> list[str]:
    """Return sorted-unique list of archaeological finding IDs that overlap mech entry."""
    hits: set[str] = set()
    for sid in mech_subject_identifiers:
        if sid in arch_index:
            hits.add(arch_index[sid])
    return sorted(hits)


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _artifact_metadata_block(source_shas: dict[str, str], run_timestamp: str) -> list[str]:
    lines = [
        f"**Run timestamp:** {run_timestamp}",
        "",
        "**Source SHAs:**",
    ]
    for k, v in source_shas.items():
        lines.append(f"- `{k}`: `{v}`")
    lines.append("")
    return lines


def render_q1_archaeological(entries: list[Q1ArchaeologicalEntry], source_shas: dict[str, str], run_timestamp: str) -> str:
    lines = [
        f"# Q1 · ARCHAEOLOGICAL CARRY-OVER · byte-identical from `consolidation_log_v0.md`",
        "",
        REPORT_HEADER,
        "",
        "**Class:** Redundancy archaeology — Owner-ruled merge and tie-break decisions from `consolidation_log_v0.md` (RP-E1 α + tie-broke-toward-distinct).",
        "",
    ]
    lines.extend(_artifact_metadata_block(source_shas, run_timestamp))
    lines.append(f"**Entry count:** {len(entries)}")
    lines.append("")
    lines.append("| entry_id | kind | promise_id | section_ref |")
    lines.append("|---|---|---|---|")
    for e in entries:
        lines.append(f"| {e.entry_id} | {e.kind} | `{e.promise_id}` | {e.section_ref} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_q1_mechanical(
    pairs: list[Q1MechanicalPair],
    arch_index: dict[str, str],
    source_shas: dict[str, str],
    run_timestamp: str,
) -> str:
    lines = [
        "# Q1 · MECHANICAL SCAN · fresh detection candidates · overlaps annotated · zero phantom (cross-ref rule permanent)",
        "",
        REPORT_HEADER,
        "",
        "**Class:** Redundancy mechanical scan — function-row pairs with identical PROM-token-set AND identical surface. Cost-ranked with `unknown` sorted to end. Cross-referenced against archaeological finding subjects (Owner SQ-E1 condition · PERMANENT).",
        "",
    ]
    lines.extend(_artifact_metadata_block(source_shas, run_timestamp))
    new_pairs = []
    overlap_pairs = []
    for p in pairs:
        hits = overlaps_for(p.subject_identifiers, arch_index)
        if hits:
            overlap_pairs.append((p, hits))
        else:
            new_pairs.append(p)
    lines.append(f"**New mechanical candidates:** {len(new_pairs)}  ·  **Overlapping archaeological subjects:** {len(overlap_pairs)}")
    lines.append("")
    lines.append("## New candidates")
    if new_pairs:
        lines.append("| pair | shared_promise_set | shared_surface | cost_rank_key |")
        lines.append("|---|---|---|---|")
        for p in new_pairs:
            lines.append(
                f"| `{p.fid_a}` ↔ `{p.fid_b}` | {' · '.join(p.shared_promises)} | `{p.shared_surface}` | {p.cost_rank_key} |"
            )
    else:
        lines.append("*(no new mechanical candidates on this run)*")
    lines.append("")
    lines.append("## Overlaps with archaeological subjects")
    if overlap_pairs:
        lines.append("| pair | shared_promise_set | shared_surface | overlaps |")
        lines.append("|---|---|---|---|")
        for p, hits in overlap_pairs:
            lines.append(
                f"| `{p.fid_a}` ↔ `{p.fid_b}` | {' · '.join(p.shared_promises)} | `{p.shared_surface}` | overlaps: {', '.join(hits)} |"
            )
    else:
        lines.append("*(no overlaps on this run)*")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_q2_archaeological(findings: list[ArchaeologicalFinding], source_shas: dict[str, str], run_timestamp: str) -> str:
    q2 = [f for f in findings if f.finding_id.startswith("Q2-")]
    lines = [
        "# Q2 · ARCHAEOLOGICAL CARRY-OVER · byte-identical from `function_promise_registry_v0.md` §4",
        "",
        REPORT_HEADER,
        "",
        "**Class:** Orphans archaeology — Owner-ruled findings from `function_promise_registry_v0.md` §4 Q2 table (5 findings Q2-01..Q2-05 with `[RULED · …]` tags verbatim).",
        "",
    ]
    lines.extend(_artifact_metadata_block(source_shas, run_timestamp))
    lines.append(f"**Finding count:** {len(q2)}")
    lines.append("")
    lines.append("| finding_id | subject | ruling_tag | ruling_ref |")
    lines.append("|---|---|---|---|")
    for f in q2:
        lines.append(f"| {f.finding_id} | {f.subject} | `{f.ruling_tag}` | {f.ruling_ref} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_q2_mechanical(
    entries: list[Q2MechanicalEntry],
    arch_index: dict[str, str],
    source_shas: dict[str, str],
    run_timestamp: str,
) -> str:
    lines = [
        "# Q2 · MECHANICAL SCAN · fresh detection candidates · overlaps annotated · zero phantom (cross-ref rule permanent)",
        "",
        REPORT_HEADER,
        "",
        "**Class:** Orphans mechanical scan — function-row scan over 4 sub-cases: (a) empty promise · (b) no PROM-token resolves · (c) empty service_trace · (d) service_trace step ∉ PART_II_JOURNEY_STEPS. READ-ONLY report.",
        "",
    ]
    lines.extend(_artifact_metadata_block(source_shas, run_timestamp))
    new_entries: list[Q2MechanicalEntry] = []
    overlap_entries: list[tuple[Q2MechanicalEntry, list[str]]] = []
    for e in entries:
        hits = overlaps_for(e.subject_identifiers, arch_index)
        if hits:
            overlap_entries.append((e, hits))
        else:
            new_entries.append(e)
    lines.append(f"**New mechanical candidates:** {len(new_entries)}  ·  **Overlapping archaeological subjects:** {len(overlap_entries)}")
    lines.append("")
    lines.append("## New candidates")
    if new_entries:
        lines.append("| function_id | sub_case | detail |")
        lines.append("|---|---|---|")
        for e in new_entries:
            lines.append(f"| `{e.function_id}` | ({e.sub_case}) | {e.detail} |")
    else:
        lines.append("*(no new mechanical candidates on this run)*")
    lines.append("")
    lines.append("## Overlaps with archaeological subjects")
    if overlap_entries:
        lines.append("| function_id | sub_case | detail | overlaps |")
        lines.append("|---|---|---|---|")
        for e, hits in overlap_entries:
            lines.append(f"| `{e.function_id}` | ({e.sub_case}) | {e.detail} | overlaps: {', '.join(hits)} |")
    else:
        lines.append("*(no overlaps on this run)*")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_q3_archaeological(findings: list[ArchaeologicalFinding], source_shas: dict[str, str], run_timestamp: str) -> str:
    q3 = [f for f in findings if f.finding_id.startswith("Q3-")]
    lines = [
        "# Q3 · ARCHAEOLOGICAL CARRY-OVER · byte-identical from `function_promise_registry_v0.md` §5",
        "",
        REPORT_HEADER,
        "",
        "**Class:** Gaps archaeology — Owner-ruled findings from `function_promise_registry_v0.md` §5 Q3 table (6 findings Q3-01..Q3-06 with `[RULED · …]` tags + `[OWNER: …]` markers verbatim).",
        "",
    ]
    lines.extend(_artifact_metadata_block(source_shas, run_timestamp))
    lines.append(f"**Finding count:** {len(q3)}")
    lines.append("")
    lines.append("| finding_id | subject | ruling_tag | owner_markers | ruling_ref |")
    lines.append("|---|---|---|---|---|")
    for f in q3:
        markers = " · ".join(f.owner_markers) if f.owner_markers else "—"
        lines.append(f"| {f.finding_id} | {f.subject} | `{f.ruling_tag}` | {markers} | {f.ruling_ref} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_q3_mechanical(
    entries: list[Q3MechanicalEntry],
    arch_index: dict[str, str],
    source_shas: dict[str, str],
    run_timestamp: str,
) -> str:
    lines = [
        "# Q3 · MECHANICAL SCAN · fresh detection candidates · overlaps annotated · zero phantom (cross-ref rule permanent)",
        "",
        REPORT_HEADER,
        "",
        "**Class:** Gaps mechanical scan — (a) promise_id with zero citations · (b) PART_II journey step with zero citations (alias-equivalent). READ-ONLY report.",
        "",
    ]
    lines.extend(_artifact_metadata_block(source_shas, run_timestamp))
    new_entries: list[Q3MechanicalEntry] = []
    overlap_entries: list[tuple[Q3MechanicalEntry, list[str]]] = []
    for e in entries:
        hits = overlaps_for(e.subject_identifiers, arch_index)
        if hits:
            overlap_entries.append((e, hits))
        else:
            new_entries.append(e)
    lines.append(f"**New mechanical candidates:** {len(new_entries)}  ·  **Overlapping archaeological subjects:** {len(overlap_entries)}")
    lines.append("")
    lines.append("## New candidates")
    if new_entries:
        lines.append("| sub_case | subject | detail |")
        lines.append("|---|---|---|")
        for e in new_entries:
            lines.append(f"| ({e.sub_case}) | `{e.subject}` | {e.detail} |")
    else:
        lines.append("*(no new mechanical candidates on this run)*")
    lines.append("")
    lines.append("## Overlaps with archaeological subjects")
    if overlap_entries:
        lines.append("| sub_case | subject | detail | overlaps |")
        lines.append("|---|---|---|---|")
        for e, hits in overlap_entries:
            lines.append(f"| ({e.sub_case}) | `{e.subject}` | {e.detail} | overlaps: {', '.join(hits)} |")
    else:
        lines.append("*(no overlaps on this run)*")
    lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Public run entry point
# ---------------------------------------------------------------------------


def run_queries(write: bool = True, run_timestamp: str | None = None) -> dict[str, str]:
    """Run all three queries + emit six findings artifacts. Returns {path: text}.

    `run_timestamp` may be pinned for deterministic-regeneration tests.
    """
    model = parse_source(V0_PATH, SUPPLEMENT_PATHS)
    q23 = load_archaeological_q2_q3(model)
    q1_arch = load_archaeological_q1()
    arch_index = build_archaeological_index(q1_arch, q23)

    q1_mech = scan_q1_redundancy(model)
    q2_mech = scan_q2_orphans(model)
    q3_mech = scan_q3_gaps(model)

    source_shas = {
        "docs/registry/function_promise_registry_v0.md": sha256_file(V0_PATH),
        "docs/registry/function_promise_registry_v0.1_supplement.md": sha256_file(SUPPLEMENT_PATHS[0]),
        "docs/registry/function_promise_registry_v0.2_supplement.md": sha256_file(SUPPLEMENT_PATHS[1]),
        "docs/registry/consolidation_log_v0.md": sha256_file(CONSOLIDATION_LOG_PATH),
    }
    if MACHINE_YAML_PATH.exists():
        source_shas["docs/registry/machine/registry.yaml"] = sha256_file(MACHINE_YAML_PATH)

    ts = run_timestamp if run_timestamp is not None else datetime.now(timezone.utc).isoformat()

    outputs = {
        "q1_archaeological.md": render_q1_archaeological(q1_arch, source_shas, ts),
        "q1_mechanical.md": render_q1_mechanical(q1_mech, arch_index, source_shas, ts),
        "q2_archaeological.md": render_q2_archaeological(q23, source_shas, ts),
        "q2_mechanical.md": render_q2_mechanical(q2_mech, arch_index, source_shas, ts),
        "q3_archaeological.md": render_q3_archaeological(q23, source_shas, ts),
        "q3_mechanical.md": render_q3_mechanical(q3_mech, arch_index, source_shas, ts),
    }

    if write:
        QUERIES_DIR.mkdir(parents=True, exist_ok=True)
        for name, text in outputs.items():
            (QUERIES_DIR / name).write_text(text, encoding="utf-8")

    return outputs


if __name__ == "__main__":
    outs = run_queries(write=True)
    for name in outs:
        print(f"wrote docs/registry/queries/{name}")
