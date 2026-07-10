"""Audio fixture directory for 9.2a P9-E7 rider discriminator + real ASR/diarization E2E.

Two content-neutral audio fixtures (governance §8 data-blind posture):
  * `fixture_a_silence.wav` — deterministic near-silence with dither.
  * `fixture_b_tone.wav` — 440 Hz sine wave.

Both: 16 kHz mono 16-bit PCM WAV, 0.5s duration, ~16 KB each. Generated
programmatically for byte-identical determinism across CI runs. No speech
content, no broadcaster/region/genre/language pre-descriptions.
"""
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent

FIXTURE_A_SILENCE = FIXTURE_DIR / "fixture_a_silence.wav"
FIXTURE_B_TONE = FIXTURE_DIR / "fixture_b_tone.wav"
