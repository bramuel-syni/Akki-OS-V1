#!/usr/bin/env python3
"""Adversarial synthetic fixture generator — CONTRACT-SHAPE emit (post-HAZARD-STOP #1).

Emits units conforming to frozen `five_rings@v0` verbatim (NormalizedUnit).
No `unit_type`, no `content`, no `freshness_stamp`, no `_fixture` at the unit
top level. Adversarial-intent + fixture flags travel in `provenance.context`
as a JSON envelope (context is Optional[str] — the frozen contract allows
free text).

Data-blind posture (governance §8 · Fixture Refresh 2026-07-10):
All feed_ids, programme names, speakers, embedded assertions, and
language-mix arrays use content-neutral placeholders (`feed_a..feed_h`,
`programme_a..programme_j`, `speaker_x*`, `lang_a..lang_c`, plus
"placeholder"-prefixed assertion bodies). No broadcaster names, no
region names, no dialectal markers leak in as pre-descriptions of the
RMS estate. Contract shape (five_rings@v0) preserved byte-identical.
Neutralized aliases → real classes resolved via
`services/service_1/license_classes.v1.json` at consumer read time.

Post-regenerate contract fits (see BUILD_JOURNAL 2026-07-01T12:30Z):
  #1 Modality — 'social' recategorised to 'text'; source_type surfaced in
     provenance.context envelope.
  #2 Edges — `edge_type`→`type`, `target_unit_id`→`target_unit_ref`, per-edge
     `confidence` DROPPED (inference wearing a graph-layer costume).
  #3 SignalRing.dimensions — flattened to Dict[str, float]; per-dim
     confidence DROPPED.
  #4 extraction_params — full modality-appropriate keys per @v0 catalogue;
     temperature=0 everywhere; deterministic by construction.
  #5 ScoreVector — recency_validity→recency, contested→contested_status
     (score_vector-level, [0,1] float); `headline` DROPPED.

Output shape (each unit):
  { unit_id, provenance, signal, relational, reextraction_handle, defensibility }

Corpus envelope preserves `_manifest.{synthetic, plumbing_only, v1_v3_valid}`
per stakeholder norm (author-labels are circular; refuse V1/V3 verdicts).
"""
import json
import uuid
import hashlib
import random

random.seed(17)  # deterministic fixture

NOW = "2026-06-30T18:00:00Z"

GENRE_CEILING = {
    "report": "fact", "documentary": "fact",
    "speech": "utterance", "call_in": "utterance", "opinion": "utterance",
    "advertisement": "non_factual", "drama": "non_factual",
}

CONTESTED_W = {"uncontested": 1.0, "contested": 0.5, "retracted": 0.1}
STANDING_W = {"accountable_tier1": 1.0, "licensed_wire": 0.85,
              "aggregator": 0.55, "ugc": 0.35, "unknown": 0.2}
CEILING_W = {"fact": 1.0, "utterance": 0.6, "non_factual": 0.2}


def sha(s): return hashlib.sha256(s.encode()).hexdigest()[:16]
def uid(): return str(uuid.uuid4())
def clamp(x): return max(0.0, min(1.0, round(x, 3)))


def score_vector(genre, standing, corroboration, contested):
    """Frozen ScoreVector shape: {genre_ceiling, source_standing, corroboration,
    recency, contested_status}. No `headline`; that was a derived composite."""
    return {
        "genre_ceiling": clamp(CEILING_W[GENRE_CEILING[genre]]),
        "source_standing": clamp(STANDING_W[standing]),
        "corroboration": clamp(corroboration),
        "recency": clamp(random.uniform(0.5, 1.0)),
        "contested_status": clamp(CONTESTED_W[contested]),
    }


def defensibility_class(genre, standing):
    ceil = GENRE_CEILING[genre]
    if ceil == "fact" and standing in ("ugc", "unknown"):
        return "utterance"
    return ceil


def _extraction_params(modality):
    """Full modality-appropriate extraction_params@v0 (temperature=0 everywhere)."""
    common = {
        "provider_id": "synthetic-fixture",
        "provider_version": "1.0.0",
        "extraction_run_id": uid(),
        "extracted_at": NOW,
    }
    if modality == "audio":
        return {**common, "sample_rate_hz": 16000, "chunk_ms": 1000,
                "model_decoding_params": {"language_hint": "en", "beam_size": 1,
                                          "temperature": 0, "vad_threshold": 0.5}}
    if modality == "text":
        return {**common, "source_format": "txt", "max_chars": 100000, "encoding": "utf-8"}
    if modality == "image":
        return {**common, "target_resolution": [1280, 720],
                "vision_decoding_params": {"prompt_template_id": "rms.image.default.v0",
                                            "max_tokens": 256, "temperature": 0}}
    if modality == "video":
        return {**common, "keyframe_strategy": "every_n_seconds", "keyframe_interval_ms": 1000,
                "vision_decoding_params": {"prompt_template_id": "rms.video.default.v0",
                                            "max_tokens": 256, "temperature": 0}}
    raise ValueError(f"no extraction_params for modality {modality!r}")


def _context_envelope(spec, unit_id):
    """Author-metadata that has no home in frozen Five Rings. Encoded as JSON
    inside provenance.context (Optional[str] free text)."""
    env = {
        "programme": spec["programme"], "feed_id": spec["feed_id"],
        "assertion": spec["text"],
        "language_mix": spec.get("lang", ["sw", "en"]),
        "logged_date": NOW, "structural_signature": sha(spec["text"]),
        "adversarial_intent": spec["intent"],
        "author_labels": {  # author-labelled classification (circular per fixture flag)
            "claim_genre": spec["genre"],
            "source_standing": spec["standing"],
            "contested_status": spec.get("contested", "uncontested"),
            "unit_type": spec.get("unit_type", "claim"),
        },
        "_fixture": {"synthetic": True, "plumbing_only": True, "v1_v3_valid": False},
    }
    # Source-type recategorisation (Hazard #1: 'social' was source-type, not modality).
    if spec.get("source_type"): env["source_type"] = spec["source_type"]
    return json.dumps(env, ensure_ascii=False)


def make_unit(spec):
    """Emit a unit in frozen five_rings@v0 shape."""
    unit_id = spec.get("_id") or uid()
    modality = spec["modality"]
    contested = spec.get("contested", "uncontested")
    corroboration = spec.get("corroboration", 0.0)

    # Ring 2 — flatten descriptor list → Dict[str, float]. Drop per-dim confidence.
    signal_dims = {d["dimension"]: clamp(d["value"]) for d in spec.get("signal", [])}

    # Ring 3 — rename edge_type→type, target_unit_id→target_unit_ref. Drop confidence.
    # If the fixture's edge had an evidence pointer separate from target, evidence_ref
    # would carry it; here confidence was the only extra, and confidence is dropped.
    edges = []
    for e in spec.get("edges", []):
        edges.append({
            "type": e.get("edge_type") or e["type"],
            "target_unit_ref": e.get("target_unit_id") or e["target_unit_ref"],
            "evidence_ref": e.get("evidence_ref"),
        })

    return {
        "unit_id": unit_id,
        "provenance": {
            "source_ref": spec["source_file"],
            "modality": modality,
            "locator": spec.get("locator", {"timestamp_ms": random.randint(0, 3_600_000)}),
            "speaker_or_author": spec.get("speaker"),
            "context": _context_envelope(spec, unit_id),
        },
        "signal": {"dimensions": signal_dims, "depth_judged": False, "depth_notes": None},
        "relational": {"edges": edges},
        "reextraction_handle": {
            "raw_pointer": spec["source_file"],
            "model_id": spec.get("model", "synthetic-fixture"),
            "model_version": "0.0.0",
            "extraction_params": _extraction_params(modality),
        },
        "defensibility": {
            "defensibility_class": defensibility_class(spec["genre"], spec["standing"]),
            "score_vector": score_vector(spec["genre"], spec["standing"], corroboration, contested),
            "matrix_rule_ref": f"qmatrix@v0::{spec['genre']}",
            "runtime_mode": "declaration_baseline",
        },
    }


# ---------------------------------------------------------------------------
# Adversarial corpus (same intents as v1; contract-shaped emit).
# ---------------------------------------------------------------------------
SPECS = []

SPECS.append(dict(  # 1. code-switch
    intent="code-switch: multi-language mix in one utterance; ASR + genre must survive",
    genre="report", standing="accountable_tier1", modality="audio",
    programme="programme_a", feed_id="feed_a", speaker="speaker_a1",
    lang=["lang_a", "lang_b", "lang_c"],
    text="Placeholder utterance mixing language_a and language_b tokens with dialectal markers — content-neutral for pipeline mechanics only.",
    signal=[{"dimension": "stance_intensity", "value": 0.4}], corroboration=0.6,
))
SPECS.append(dict(  # 2. genre-boundary ambiguity
    intent="genre boundary: starts as report, drifts to opinion; classifier must not over-call 'fact'",
    genre="opinion", standing="accountable_tier1", modality="audio",
    programme="programme_b", feed_id="feed_a", speaker="speaker_a2",
    text="Placeholder report-drifts-to-opinion body — factual framing at open, editorial framing at close; content-neutral.",
    signal=[{"dimension": "stance_intensity", "value": 0.85},
            {"dimension": "hedging_density", "value": 0.1}],
))
SPECS.append(dict(  # 3. native-ad-as-news
    intent="ad mimicking news read; must NOT be admitted as fact regardless of anchor voice",
    genre="advertisement", standing="accountable_tier1", modality="audio",
    programme="programme_a", feed_id="feed_a", speaker="speaker_a1",
    text="Placeholder advertisement copy read in news-anchor cadence — content-neutral commercial disclosure.",
))

# 4-7. Contested chain
claim_id, corrob_id, contra_id = uid(), uid(), uid()
SPECS.append(dict(intent="contested chain [1/4]: original claim (call-in, unverified)",
    genre="call_in", standing="ugc", modality="audio",
    programme="programme_c", feed_id="feed_e", speaker="speaker_e1",
    text="Placeholder call-in assertion about region_a service outage; unverified.",
    _id=claim_id))
SPECS.append(dict(intent="contested chain [2/4]: corroborating report (accountable, attributed)",
    genre="report", standing="accountable_tier1", modality="video",
    programme="programme_a", feed_id="feed_a", speaker="speaker_a3",
    text="Placeholder corroborating report from field crew — region_a service outage confirmed since date_x.",
    corroboration=0.8,
    edges=[{"edge_type": "corroborates", "target_unit_id": claim_id}],
    _id=corrob_id))
SPECS.append(dict(intent="contested chain [3/4]: contradiction (wire, different figure)",
    genre="report", standing="licensed_wire", modality="text",
    programme="programme_d", feed_id="feed_d", speaker=None,
    text="Placeholder wire report stating service was restored on date_y — contradicts prior claim.",
    contested="contested", corroboration=0.4,
    edges=[{"edge_type": "contradicts", "target_unit_id": corrob_id}],
    _id=contra_id))
SPECS.append(dict(intent="contested chain [4/4]: retraction of the original claim",
    genre="report", standing="accountable_tier1", modality="text",
    programme="programme_a", feed_id="feed_a", speaker="speaker_a4",
    text="Placeholder correction body — earlier region_a report overstated outage duration.",
    contested="retracted",
    edges=[{"edge_type": "retracts", "target_unit_id": claim_id}]))

SPECS.append(dict(  # 8. authority-blind ceiling (speech)
    intent="authority-blind ceiling: speech on tier-1 feed stays utterance, not fact",
    genre="speech", standing="accountable_tier1", modality="video",
    programme="programme_e", feed_id="feed_a", speaker="speaker_a5",
    text="Placeholder speech transcript — declarative claims about future economic outcomes.",
    signal=[{"dimension": "vocal_emphasis", "value": 0.7}],
))
SPECS.append(dict(  # 9. source-standing lowering + Hazard#1: was 'social', now 'text' + source_type=social_post
    intent="source-standing lowers ceiling: unattributed UGC 'report' -> utterance (was modality=social; post-HAZARD-STOP #1 recategorised as text, source_type=social_post)",
    genre="report", standing="ugc", modality="text", source_type="social_post",
    programme="programme_f", feed_id="feed_g", speaker="handle_placeholder",
    text="Placeholder social-post assertion about incident at location_a — unverified, high-virality.",
    signal=[{"dimension": "virality", "value": 0.9}], contested="contested",
))
SPECS.append(dict(  # 10. diarization stress
    intent="diarization stress: sub-30s speaker, overlapping turns",
    genre="call_in", standing="ugc", modality="audio",
    programme="programme_c", feed_id="feed_e", speaker="speaker_e2",
    text="Placeholder short overlapping-speaker turn — sub-30s duration with turn-conflict marker.",
    locator={"timestamp_ms": 1_200_000, "duration_ms": 8_500},
))

onscreen_id = uid()
SPECS.append(dict(  # 11. cross-modal conflict
    intent="cross-modal: chyron (on-screen text) disagrees with anchor audio",
    genre="report", standing="accountable_tier1", modality="video",
    programme="programme_a", feed_id="feed_a", speaker="speaker_a1",
    text="Placeholder cross-modal conflict — audio-track count differs from on-screen-text count.",
    edges=[{"edge_type": "contradicts", "target_unit_id": onscreen_id}],
    signal=[{"dimension": "on_screen_text_conflict", "value": 1.0}],
))
SPECS.append(dict(  # 12. recency stress
    intent="recency stress: documentary fact, but ~12 years old — recency lowers score",
    genre="documentary", standing="accountable_tier1", modality="video",
    programme="programme_g", feed_id="feed_b", speaker="speaker_b1",
    text="Placeholder archival documentary claim about a measured geographic feature at time_t_minus_12y.",
    corroboration=0.7,
))
SPECS.append(dict(  # 13. drama-as-fact
    intent="drama stating a 'fact' — must floor to non_factual",
    genre="drama", standing="accountable_tier1", modality="video",
    programme="programme_h", feed_id="feed_c", speaker="character_placeholder",
    text="Placeholder dramatic-fiction dialogue asserting a public-figure event.",
))
SPECS.append(dict(  # 14. malformed ingestion
    intent="ingestion robustness: partial/malformed content, missing speaker",
    genre="report", standing="unknown", modality="text",
    programme="programme_i", feed_id="feed_h", speaker=None,
    text="Placeholder malformed transcript ??? [transcription gap] ... placeholder ...",
))

# 15-18. Opinion-dominant cluster
for i in range(4):
    SPECS.append(dict(
        intent=f"defensibility skew: opinion-dominant segment [{i+1}/4] — distribution must not gate",
        genre="opinion", standing="aggregator", modality="text",
        programme="programme_j", feed_id="feed_f", speaker=f"speaker_f{i+1}",
        text=f"Placeholder opinion segment [{i+1}/4] — non-factual editorial framing.",
        signal=[{"dimension": "stance_intensity", "value": 0.8}],
    ))

SPECS.append(dict(  # 19. clean positive
    intent="clean positive: attributed wire report, uncontested fact",
    genre="report", standing="licensed_wire", modality="text",
    programme="programme_d", feed_id="feed_d", speaker=None,
    text="Placeholder attributed wire report of a numeric policy rate held constant per published statement.",
    corroboration=0.75,
))


def main(out_path=None):
    units = []
    for spec in SPECS:
        s = dict(spec)
        s.setdefault("source_file", f"synthetic://{s['feed_id']}/{sha(s['text'])}.raw")
        units.append(make_unit(s))

    corpus = {
        "_manifest": {
            "fixture": "rms_adversarial_synthetic_v1",
            "synthetic": True, "plumbing_only": True, "v1_v3_valid": False,
            "note": "Author-labelled synthetic data. Exercises the pipeline only. Accuracy measured against these labels is circular. Do NOT use for V1 or V3 — those require real RMS material with human ground truth.",
            "shape": "five_rings@v0 (NormalizedUnit — post-HAZARD-STOP #1 contract-shaped emit)",
            "generated_at": NOW,
            "unit_count": len(units),
            "regenerated_after_hazard_stop_1": True,
            "genres_note": "author-labels in provenance.context.author_labels",
            "adversarial_coverage": [
                "code-switching (multi-language mix)", "genre-boundary ambiguity",
                "native-ad-as-news", "contested chain (claim/corroborate/contradict/retract)",
                "authority-blind genre ceiling", "source-standing lowering",
                "sub-30s + overlapping speakers", "cross-modal conflict",
                "recency skew", "drama-as-fact", "malformed ingestion",
                "opinion-dominant distribution", "clean positive control",
            ],
        },
        "units": units,
    }
    if out_path is None:
        import os
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixture.json")
    with open(out_path, "w") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"wrote {len(units)} units to {out_path}")
    return corpus


if __name__ == "__main__":
    main()
