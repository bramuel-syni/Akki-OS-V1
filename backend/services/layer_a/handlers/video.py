"""Layer A video handler.

Reads `.mp4 / .mov / .mkv / .webm`. Strips audio track + samples N
keyframes. Uses `ffmpeg-python` (chosen over `moviepy` — journal entry
in BUILD_JOURNAL.md G0.5 deliverable 2 entry: thinner, direct ffmpeg
wrapper, no GIL overhead).

Cousin: no direct cousin for video.
"""
from __future__ import annotations

import io
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional

from services.layer_a.types import RawAudioArtifact, RawVideoArtifact

KEYFRAME_STRIDE_S = int(os.environ.get("AKKI_VIDEO_KEYFRAME_STRIDE_S", "5"))


def _ffprobe_duration_and_fps(path: str) -> tuple[int, float]:
    out = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration,r_frame_rate",
        "-of", "default=noprint_wrappers=1",
        path,
    ], text=True)
    duration_s = 0.0
    fps = 0.0
    for line in out.splitlines():
        if line.startswith("duration="):
            try:
                duration_s = float(line.split("=", 1)[1])
            except ValueError:
                pass
        elif line.startswith("r_frame_rate="):
            num, _, den = line.split("=", 1)[1].partition("/")
            try:
                fps = float(num) / float(den) if den else float(num)
            except ValueError:
                pass
    return int(duration_s * 1000), fps


def _extract_audio_track(path: str) -> Optional[RawAudioArtifact]:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        out = tmp.name
    try:
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", path,
            "-vn", "-ac", "1", "-ar", "16000", out,
        ], check=True)
        from services.layer_a.handlers.audio import retrieve as audio_retrieve
        return audio_retrieve(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    finally:
        try:
            os.unlink(out)
        except OSError:
            pass


def _sample_keyframes(path: str, stride_s: int) -> List[bytes]:
    with tempfile.TemporaryDirectory() as td:
        out_pattern = os.path.join(td, "frame_%04d.jpg")
        try:
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error", "-i", path,
                "-vf", f"fps=1/{max(stride_s, 1)}",
                out_pattern,
            ], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []
        keyframes: List[bytes] = []
        for fname in sorted(os.listdir(td)):
            with open(os.path.join(td, fname), "rb") as fh:
                keyframes.append(fh.read())
        return keyframes


def retrieve(source_ref: str) -> RawVideoArtifact:
    path = Path(source_ref)
    duration_ms, fps = _ffprobe_duration_and_fps(str(path))
    audio = _extract_audio_track(str(path))
    keyframes = _sample_keyframes(str(path), KEYFRAME_STRIDE_S)
    return RawVideoArtifact(
        audio_track=audio,
        keyframes=keyframes,
        duration_ms=duration_ms,
        fps=fps,
        source_ref=source_ref,
        source_format=path.suffix.lower().lstrip("."),
    )
