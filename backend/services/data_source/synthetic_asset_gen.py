"""Generators for the adversarial synthetic fixture's binary assets.

Writes short WAV files (pure stdlib `wave` + numpy sine waves) and tiny
PNG files (PIL) under `synthetic_assets/`. Audio quality is irrelevant—
the point is that bytes exist so Layer A handlers and Layer B providers
can be exercised end-to-end on plumbing.

Deterministic by seed so the fixture round-trips byte-identically.
"""
from __future__ import annotations

import hashlib
import math
import struct
import wave
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw

ASSET_DIR = Path(__file__).parent / "synthetic_assets"
AUDIO_DIR = ASSET_DIR / "audio"
IMAGE_DIR = ASSET_DIR / "image"
TRANSCRIPT_DIR = ASSET_DIR / "transcript"

_SR = 16000  # Hz


def _ensure_dirs() -> None:
    for d in (AUDIO_DIR, IMAGE_DIR, TRANSCRIPT_DIR):
        d.mkdir(parents=True, exist_ok=True)


def _det_freqs(seed: str, n: int = 3) -> List[float]:
    h = hashlib.sha256(seed.encode()).digest()
    return [220.0 + (h[i] / 255.0) * 440.0 for i in range(n)]


def write_wav(filename: str, *, duration_ms: int, seed: str) -> Path:
    _ensure_dirs()
    out = AUDIO_DIR / filename
    if out.exists():
        return out
    n_frames = int(_SR * duration_ms / 1000)
    freqs = _det_freqs(seed)
    with wave.open(str(out), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # int16
        wf.setframerate(_SR)
        for i in range(n_frames):
            t = i / _SR
            sample = 0.0
            for f in freqs:
                sample += math.sin(2 * math.pi * f * t)
            sample = sample / max(len(freqs), 1) * 12000
            wf.writeframesraw(struct.pack("<h", int(sample)))
    return out


def write_png(filename: str, *, text: str, seed: str) -> Path:
    _ensure_dirs()
    out = IMAGE_DIR / filename
    if out.exists():
        return out
    h = hashlib.sha256(seed.encode()).digest()
    bg = (h[0], h[1], h[2])
    img = Image.new("RGB", (320, 180), color=bg)
    draw = ImageDraw.Draw(img)
    draw.text((10, 80), text[:40], fill=(255, 255, 255))
    img.save(out, format="PNG")
    return out


def write_vtt(filename: str, *, cues: List[Tuple[int, int, str, str]]) -> Path:
    """`cues` items: (t_start_ms, t_end_ms, speaker, text)."""
    _ensure_dirs()
    out = TRANSCRIPT_DIR / filename
    lines = ["WEBVTT", ""]
    for i, (s, e, spk, txt) in enumerate(cues, start=1):
        def _fmt(ms: int) -> str:
            h = ms // 3_600_000
            m = (ms // 60_000) % 60
            sec = (ms // 1000) % 60
            mm = ms % 1000
            return f"{h:02d}:{m:02d}:{sec:02d}.{mm:03d}"
        lines += [str(i), f"{_fmt(s)} --> {_fmt(e)}", f"<v {spk}>{txt}</v>", ""]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
