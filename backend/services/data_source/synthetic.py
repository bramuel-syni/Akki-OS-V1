"""Adversarial Kenyan-broadcast-shaped synthetic plumbing fixture.

G0.5 Deliverable 1. Replaces the convenient 4-unit G0 fixture with
>=20 units engineered to stress the pipeline, not flatter it.

ADVERSARIAL DIMENSIONS (asserted in tests/test_synthetic_fixture_roundtrip.py):
  a) Hard code-switching      — >=4 units (English/Swahili/Sheng mix).
  b) Genre-ambiguous boundary — >=4 units sitting on >=2 matrix cells.
  c) Contested chain          — >=3 units forming A->B<-C, C-retracts-by-D.
  d) Sub-30s speakers         — >=2 audio units with <30s active span.
  e) Lopsided defensibility   — majority `utterance`, smaller `fact`,
                                thin `non_factual`. Honest skew.
  f) Synthetic audio + image  — >=3 WAV bytes + >=1 PNG bytes generated
                                under `synthetic_assets/`.

Fixture is plumbing-only — not a V1 validity proof. Real Kenyan-broadcast
Hour A is the only thing that can pass V1.

Round-trips through frozen Five Rings schema byte-identically.
"""
from __future__ import annotations

from typing import Dict, Iterable, List

from contracts.five_rings import (
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    RelationalEdge,
    RelationalRing,
    ReextractionHandleRing,
    RelationType,
    ScoreVector,
    SignalRing,
)
from contracts.qualification_matrix.loader import load_qualification_matrix
from services.data_source.synthetic_asset_gen import write_png, write_vtt, write_wav

# ---------------------------------------------------------------------------
# Helpers — keep unit construction terse so the adversarial intent is visible.
# ---------------------------------------------------------------------------

def _uid(n: int) -> str:
    return f"00000000-0000-0000-0000-{n:012d}"


# extraction_params@v0 (Pre-G2 freeze, 2026-07-01) — every NormalizedUnit
# emitted by the fixture carries a compliant `extraction_params` block
# per its modality. temperature=0 everywhere so the V1 harness's
# `is_deterministically_reproducible()` returns True on plumbing runs
# (per stakeholder correction #2). Times are pinned (not "now()") so
# the fixture is byte-identical run to run.
_SYNTHETIC_EXTRACTED_AT = "2026-07-01T00:00:00Z"

def _audio_params(n: int) -> dict:
    return {
        "provider_id": "synthetic-asr",
        "provider_version": "0.0.0",
        "extraction_run_id": f"synthetic-audio-{n:04d}",
        "extracted_at": _SYNTHETIC_EXTRACTED_AT,
        "sample_rate_hz": 16000,
        "chunk_ms": 1000,
        "model_decoding_params": {
            "language_hint": "en",
            "beam_size": 1,
            "temperature": 0,
            "vad_threshold": 0.5,
        },
    }

def _text_params(n: int, source_format: str = "txt") -> dict:
    return {
        "provider_id": "synthetic-text",
        "provider_version": "0.0.0",
        "extraction_run_id": f"synthetic-text-{n:04d}",
        "extracted_at": _SYNTHETIC_EXTRACTED_AT,
        "source_format": source_format,
        "max_chars": 100000,
        "encoding": "utf-8",
    }

def _image_params(n: int) -> dict:
    return {
        "provider_id": "synthetic-vision",
        "provider_version": "0.0.0",
        "extraction_run_id": f"synthetic-image-{n:04d}",
        "extracted_at": _SYNTHETIC_EXTRACTED_AT,
        "target_resolution": [1280, 720],
        "vision_decoding_params": {
            "prompt_template_id": "rms.image.default.v0",
            "max_tokens": 256,
            "temperature": 0,
        },
    }

def _params_for(modality: Modality, n: int) -> dict:
    if modality == Modality.AUDIO:
        return _audio_params(n)
    if modality == Modality.IMAGE:
        return _image_params(n)
    if modality == Modality.TEXT:
        # Transcript-shaped TEXT units in the fixture carry source_format
        # in (vtt/srt/json) range but the v0 TEXT catalogue restricts
        # source_format to document formats. We use 'txt' as the
        # conservative TEXT default — transcript-cue units still resolve
        # via the TEXT modality at v0 (TRANSCRIPT mod gets activated when
        # the Modality enum gains it; catalogue is already shaped).
        return _text_params(n)
    if modality == Modality.VIDEO:
        return {
            "provider_id": "synthetic-video",
            "provider_version": "0.0.0",
            "extraction_run_id": f"synthetic-video-{n:04d}",
            "extracted_at": _SYNTHETIC_EXTRACTED_AT,
            "keyframe_strategy": "every_n_seconds",
            "keyframe_interval_ms": 1000,
            "vision_decoding_params": {
                "prompt_template_id": "rms.video.default.v0",
                "max_tokens": 256,
                "temperature": 0,
            },
        }
    if modality == Modality.COMPOSITE:
        return {
            "provider_id": "synthetic-composite",
            "provider_version": "0.0.0",
            "extraction_run_id": f"synthetic-composite-{n:04d}",
            "extracted_at": _SYNTHETIC_EXTRACTED_AT,
            "source_artifact_refs": [],
            "aggregation_strategy": "union",
        }
    raise ValueError(f"no extraction_params shape for modality {modality!r}")


def _u(  # build a NormalizedUnit with sensible defaults
    n: int, *, modality: Modality, source_ref: str, locator: dict,
    speaker: str | None, context: str,
    sig_dims: dict, raw_pointer: str, model_id: str,
    cls: DefensibilityClass, scores: tuple, matrix_rule_ref: str,
    edges: list | None = None,
    code_switch_tag: bool = False,
    genre_boundary_tag: bool = False,
) -> NormalizedUnit:
    sv = ScoreVector(
        genre_ceiling=scores[0], source_standing=scores[1],
        corroboration=scores[2], recency=scores[3], contested_status=scores[4],
    )
    # Encode adversarial tags into context so test_synthetic_fixture_is_adversarial
    # can find them deterministically without polluting the frozen schema.
    tag_suffix = ""
    if code_switch_tag: tag_suffix += " [code_switch]"
    if genre_boundary_tag: tag_suffix += " [genre_boundary]"
    return NormalizedUnit(
        unit_id=_uid(n),
        provenance=ProvenanceRing(
            source_ref=source_ref, modality=modality, locator=locator,
            speaker_or_author=speaker, context=context + tag_suffix,
        ),
        signal=SignalRing(dimensions=sig_dims, depth_judged=False),
        relational=RelationalRing(edges=edges or []),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer=raw_pointer, model_id=model_id, model_version="0.0.0",
            extraction_params=_params_for(modality, n),
        ),
        defensibility=DefensibilityRing(
            defensibility_class=cls, score_vector=sv,
            matrix_rule_ref=matrix_rule_ref, runtime_mode="declaration_baseline",
        ),
    )


def _generate_assets() -> Dict[str, str]:
    """Materialise the WAV/PNG/VTT bytes referenced by Provenance rings.
    Returns a map of asset-key -> absolute path string."""
    a1 = write_wav("anchor_primary_001.wav", duration_ms=8500, seed="a1")
    a2 = write_wav("anchor_wire_002.wav", duration_ms=12000, seed="a2")
    a3 = write_wav("panel_primary_003.wav", duration_ms=45000, seed="a3")
    a4 = write_wav("panel_codeswitch_004.wav", duration_ms=18000, seed="a4")
    a_short = write_wav("panel_short_caller_005.wav", duration_ms=12000, seed="a-short")
    img1 = write_png("keyframe_logo_001.png", text="KBC NEWS", seed="img-1")
    vtt = write_vtt("hour_a_gold.vtt", cues=[
        (0, 8500, "Anchor A", "Good morning. Habari za asubuhi. Today's headlines."),
        (12_000, 24_000, "Anchor B", "Wire reports indicate a development in the East."),
        (60_000, 105_000, "Panellist X", "Mimi naona hii issue inahitaji discussion zaidi."),
    ])
    return {"a1": str(a1), "a2": str(a2), "a3": str(a3), "a4": str(a4), "a_short": str(a_short),
            "img1": str(img1), "vtt": str(vtt)}


def _build_units() -> Dict[str, NormalizedUnit]:
    matrix = load_qualification_matrix("v0")
    assets = _generate_assets()

    # Resolve matrix rule refs once.
    R_anchor_prim = matrix.rule_ref(matrix.find("news_anchor_read", "primary_recorded"))
    R_anchor_wire = matrix.rule_ref(matrix.find("news_anchor_read", "wire_republish"))
    R_panel_prim = matrix.rule_ref(matrix.find("panel_debate", "primary_recorded"))
    R_panel_wire = matrix.rule_ref(matrix.find("panel_debate", "wire_republish"))

    units: List[NormalizedUnit] = []

    # --- (a) Code-switching units (>=4) -------------------------------------
    units.append(_u(1, modality=Modality.AUDIO, source_ref=assets["a4"],
        locator={"t_start_ms": 0, "t_end_ms": 6500}, speaker="Panellist Y",
        context="Panel speaker mixes English + Swahili mid-sentence.",
        sig_dims={"affect_valence": 0.5, "prosody": 0.45}, raw_pointer=f"local://{assets['a4']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.85, 0.10, 0.99, 0.30), matrix_rule_ref=R_panel_prim,
        code_switch_tag=True))
    units.append(_u(2, modality=Modality.AUDIO, source_ref=assets["a4"],
        locator={"t_start_ms": 6500, "t_end_ms": 12000}, speaker="Panellist Z",
        context="Sheng phrase 'huku mtaani' inserted into English newsdesk read.",
        sig_dims={"affect_valence": 0.30, "prosody": 0.55}, raw_pointer=f"local://{assets['a4']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.30, 0.05, 0.99, 0.40), matrix_rule_ref=R_anchor_wire,
        code_switch_tag=True))
    units.append(_u(3, modality=Modality.AUDIO, source_ref=assets["a4"],
        locator={"t_start_ms": 12000, "t_end_ms": 18000}, speaker="Caller A",
        context="Caller-in code-switches Swahili/English/Sheng in single utterance.",
        sig_dims={"affect_valence": 0.65, "prosody": 0.50}, raw_pointer=f"local://{assets['a4']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.40, 0.00, 0.99, 0.50), matrix_rule_ref=R_panel_wire,
        code_switch_tag=True))
    units.append(_u(4, modality=Modality.TEXT, source_ref=assets["vtt"],
        locator={"cue": 3}, speaker="Panellist X",
        context="Transcript cue mixing 'Mimi naona hii issue' — code-switch in print.",
        sig_dims={"hedging_density": 0.4, "stance_intensity": 0.6},
        raw_pointer=f"local://{assets['vtt']}", model_id="synthetic-text",
        cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.85, 0.10, 0.99, 0.30), matrix_rule_ref=R_panel_prim,
        code_switch_tag=True))

    # --- (b) Genre-boundary units (>=4) -------------------------------------
    units.append(_u(5, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 0, "t_end_ms": 15000}, speaker="Anchor A",
        context="Anchor reads an opinion column on-air — plausibly news_anchor_read OR panel_debate.",
        sig_dims={"prosody": 0.55}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.55, 0.85, 0.10, 0.95, 0.20), matrix_rule_ref=R_anchor_prim,
        genre_boundary_tag=True))
    units.append(_u(6, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 15000, "t_end_ms": 30000}, speaker="Panellist X",
        context="Panellist quotes a wire-republish bulletin during panel — boundary panel/anchor_wire.",
        sig_dims={"prosody": 0.48}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.45, 0.05, 0.92, 0.35), matrix_rule_ref=R_panel_wire,
        genre_boundary_tag=True))
    units.append(_u(7, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 30000, "t_end_ms": 38000}, speaker="Anchor B",
        context="Anchor anchors then editorialises — sits between primary_recorded fact and panel utterance.",
        sig_dims={"prosody": 0.60}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.60, 0.80, 0.15, 0.93, 0.25), matrix_rule_ref=R_anchor_prim,
        genre_boundary_tag=True))
    units.append(_u(8, modality=Modality.AUDIO, source_ref=assets["a2"],
        locator={"t_start_ms": 0, "t_end_ms": 6000}, speaker="Anchor B",
        context="Wire-republish read with primary-recorded production polish — boundary.",
        sig_dims={"prosody": 0.55}, raw_pointer=f"local://{assets['a2']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.55, 0.40, 0.05, 0.95, 0.30), matrix_rule_ref=R_anchor_wire,
        genre_boundary_tag=True))

    # --- (c) Contested chain (>=3) ------------------------------------------
    # u9 corroborates u10; u11 contradicts u10; u12 retracts u11.
    units.append(_u(9, modality=Modality.AUDIO, source_ref=assets["a1"],
        locator={"t_start_ms": 0, "t_end_ms": 4000}, speaker="Anchor A",
        context="Primary recorded fact A.",
        sig_dims={"prosody": 0.65}, raw_pointer=f"local://{assets['a1']}",
        model_id="synthetic-asr", cls=DefensibilityClass.FACT,
        scores=(0.95, 0.90, 0.80, 0.99, 0.00), matrix_rule_ref=R_anchor_prim,
        edges=[RelationalEdge(type=RelationType.CORROBORATES, target_unit_ref=_uid(10),
                              evidence_ref=assets["img1"])]))
    units.append(_u(10, modality=Modality.IMAGE, source_ref=assets["img1"],
        locator={"bbox": [10, 80, 250, 30]}, speaker=None,
        context="Keyframe corroborating fact A.",
        sig_dims={"visual_emphasis": 0.78}, raw_pointer=f"local://{assets['img1']}",
        model_id="synthetic-vision", cls=DefensibilityClass.FACT,
        scores=(0.85, 0.90, 0.70, 0.99, 0.10), matrix_rule_ref=R_anchor_prim))
    units.append(_u(11, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 38000, "t_end_ms": 42000}, speaker="Panellist X",
        context="Panellist contradicts fact A on air.",
        sig_dims={"affect_valence": 0.7, "prosody": 0.5}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.85, 0.10, 0.99, 0.65), matrix_rule_ref=R_panel_prim,
        edges=[RelationalEdge(type=RelationType.CONTRADICTS, target_unit_ref=_uid(10))]))
    units.append(_u(12, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 42000, "t_end_ms": 44500}, speaker="Panellist X",
        context="Same panellist retracts contradiction later in the segment.",
        sig_dims={"affect_valence": 0.5, "prosody": 0.45}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.85, 0.05, 0.99, 0.55), matrix_rule_ref=R_panel_prim,
        edges=[RelationalEdge(type=RelationType.RETRACTS, target_unit_ref=_uid(11))]))

    # --- (d) Sub-30s speaker units (>=2) ------------------------------------
    units.append(_u(13, modality=Modality.AUDIO, source_ref=assets["a_short"],
        locator={"t_start_ms": 0, "t_end_ms": 8000}, speaker="Caller B",
        context="Caller active <30s — sits under DER threshold.",
        sig_dims={"affect_valence": 0.4}, raw_pointer=f"local://{assets['a_short']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.35, 0.00, 0.99, 0.30), matrix_rule_ref=R_panel_wire))
    units.append(_u(14, modality=Modality.AUDIO, source_ref=assets["a_short"],
        locator={"t_start_ms": 8000, "t_end_ms": 12000}, speaker="Caller C",
        context="Short caller-in interjection — <30s active.",
        sig_dims={"affect_valence": 0.5}, raw_pointer=f"local://{assets['a_short']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.30, 0.00, 0.99, 0.40), matrix_rule_ref=R_panel_wire))

    # --- (e) Lopsided defensibility skew — majority utterance, fact tail,
    #         thin non_factual. Realistic for a Kenyan broadcast hour.
    units.append(_u(15, modality=Modality.AUDIO, source_ref=assets["a2"],
        locator={"t_start_ms": 6000, "t_end_ms": 12000}, speaker="Anchor B",
        context="Wire republish utterance.",
        sig_dims={"prosody": 0.5}, raw_pointer=f"local://{assets['a2']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.55, 0.30, 0.05, 0.92, 0.35), matrix_rule_ref=R_anchor_wire))
    units.append(_u(16, modality=Modality.TEXT, source_ref=assets["vtt"],
        locator={"cue": 2}, speaker="Anchor B",
        context="Transcript wire-copy utterance.",
        sig_dims={"hedging_density": 0.35}, raw_pointer=f"local://{assets['vtt']}",
        model_id="synthetic-text", cls=DefensibilityClass.UTTERANCE,
        scores=(0.55, 0.30, 0.05, 0.92, 0.20), matrix_rule_ref=R_anchor_wire))
    units.append(_u(17, modality=Modality.AUDIO, source_ref=assets["a1"],
        locator={"t_start_ms": 4000, "t_end_ms": 8500}, speaker="Anchor A",
        context="Primary-recorded fact (second in the hour).",
        sig_dims={"prosody": 0.6}, raw_pointer=f"local://{assets['a1']}",
        model_id="synthetic-asr", cls=DefensibilityClass.FACT,
        scores=(0.95, 0.90, 0.75, 0.99, 0.05), matrix_rule_ref=R_anchor_prim))
    units.append(_u(18, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 44500, "t_end_ms": 45000}, speaker="Panellist Y",
        context="Rhetorical exclamation — non-factual.",
        sig_dims={"affect_valence": 0.95}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.NON_FACTUAL,
        scores=(0.30, 0.80, 0.00, 0.99, 0.50), matrix_rule_ref=R_panel_prim))

    # Pad to >=20 with additional utterances so the skew reads honestly.
    units.append(_u(19, modality=Modality.AUDIO, source_ref=assets["a2"],
        locator={"t_start_ms": 6000, "t_end_ms": 9000}, speaker="Anchor B",
        context="Additional wire-utterance for skew.",
        sig_dims={"prosody": 0.5}, raw_pointer=f"local://{assets['a2']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.55, 0.32, 0.05, 0.92, 0.25), matrix_rule_ref=R_anchor_wire))
    units.append(_u(20, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 9000, "t_end_ms": 15000}, speaker="Panellist X",
        context="Additional panel utterance for skew.",
        sig_dims={"affect_valence": 0.4}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.85, 0.10, 0.99, 0.30), matrix_rule_ref=R_panel_prim))
    units.append(_u(21, modality=Modality.AUDIO, source_ref=assets["a3"],
        locator={"t_start_ms": 50000, "t_end_ms": 60000}, speaker="Panellist Y",
        context="Sustained panel speech — long-form, well above DER >=30s window.",
        sig_dims={"affect_valence": 0.55, "prosody": 0.5}, raw_pointer=f"local://{assets['a3']}",
        model_id="synthetic-asr", cls=DefensibilityClass.UTTERANCE,
        scores=(0.50, 0.85, 0.10, 0.99, 0.25), matrix_rule_ref=R_panel_prim))

    return {u.unit_id: u for u in units}


ADVERSARIAL_DIMENSIONS = {
    "code_switching_units": 4,    # >=
    "genre_boundary_units": 4,    # >=
    "contested_chain_units": 3,   # >=
    "sub_30s_speaker_units": 2,   # >=
    "audio_assets": 3,            # >=
    "image_assets": 1,            # >=
}


class SyntheticPlumbingDataSource:
    """Adversarial Kenyan-broadcast-shaped fixture. Plumbing only."""

    name = "synthetic-plumbing-adversarial"
    mode = "synthetic"
    adversarial = True

    def __init__(self) -> None:
        self._units = _build_units()

    def iter_units(self) -> Iterable[NormalizedUnit]:
        return list(self._units.values())

    def get(self, unit_id: str) -> NormalizedUnit:
        return self._units[unit_id]
