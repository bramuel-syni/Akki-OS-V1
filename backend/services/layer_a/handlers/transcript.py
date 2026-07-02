"""Layer A transcript handler.

Reads paired gold-transcript files (`.vtt / .srt / .json`) that ship
alongside a real RMS broadcast hour. Used by the V1 harness for WER /
NER recall comparisons.

No cousin — net-new at G0.5. The .json reader expects a list of
`{t_start_ms, t_end_ms, text, speaker?}` dicts.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List

from services.layer_a.types import RawTranscriptArtifact, TranscriptCue

_VTT_TIMECODE = re.compile(
    r"(\d+):(\d+):(\d+)[.,](\d+)\s*-->\s*(\d+):(\d+):(\d+)[.,](\d+)"
)
_SRT_TIMECODE = re.compile(
    r"(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)"
)


def _hms_to_ms(h: int, m: int, s: int, ms: int) -> int:
    return h * 3600_000 + m * 60_000 + s * 1000 + ms


def _parse_vtt_or_srt(text: str, is_vtt: bool) -> List[TranscriptCue]:
    cues: List[TranscriptCue] = []
    blocks = re.split(r"\n\s*\n", text.strip())
    for block in blocks:
        if not block.strip() or block.strip().upper() == "WEBVTT":
            continue
        m = (_VTT_TIMECODE if is_vtt else _SRT_TIMECODE).search(block)
        if not m:
            continue
        groups = list(map(int, m.groups()))
        t_start = _hms_to_ms(*groups[:4])
        t_end = _hms_to_ms(*groups[4:])
        body_lines = [ln for ln in block.splitlines() if not (_VTT_TIMECODE if is_vtt else _SRT_TIMECODE).search(ln)]
        # Drop the optional cue identifier (a stand-alone integer line).
        if body_lines and body_lines[0].strip().isdigit():
            body_lines = body_lines[1:]
        body = "\n".join(body_lines).strip()
        speaker = None
        if body.startswith("<v "):
            end = body.find(">")
            if end > 0:
                speaker = body[3:end]
                body = body[end + 1:].rstrip("</v>").strip()
        cues.append(TranscriptCue(t_start_ms=t_start, t_end_ms=t_end, text=body, speaker=speaker))
    return cues


def retrieve(source_ref: str) -> RawTranscriptArtifact:
    path = Path(source_ref)
    ext = path.suffix.lower().lstrip(".")
    raw = path.read_text(encoding="utf-8", errors="replace")
    if ext == "json":
        payload = json.loads(raw)
        cues = [
            TranscriptCue(
                t_start_ms=int(item["t_start_ms"]),
                t_end_ms=int(item["t_end_ms"]),
                text=str(item["text"]),
                speaker=item.get("speaker"),
            )
            for item in payload
        ]
    else:
        cues = _parse_vtt_or_srt(raw, is_vtt=(ext == "vtt"))
    speakers = sorted({c.speaker for c in cues if c.speaker})
    return RawTranscriptArtifact(cues=cues, speaker_labels=speakers, source_format=ext, source_ref=source_ref)
