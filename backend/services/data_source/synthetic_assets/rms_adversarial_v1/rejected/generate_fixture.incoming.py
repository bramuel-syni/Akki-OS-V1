#!/usr/bin/env python3
"""
Adversarial synthetic fixture generator for the RMS Intelligence System.

SYNTHETIC - PLUMBING ONLY. NOT V1/V3 VALID.
Labels are author-assigned, not ground truth. This fixture exercises the pipeline
(ingestion -> Layer C convergence -> Ring stamping -> Layer D composition -> Solva
floor enforcement). It must NEVER stand in for real RMS material at the V1 or V3
gates; accuracy measured against these labels is circular by construction.

Shape: emits units conforming to the Five-Rings model (five_rings@v0) as documented
in the Product & Engineering Specification v2.1. This generator is aligned to the
CORRECTED frozen shapes:
  - modality enum is the perception mechanism only {text, audio, video, image,
    composite}; source-type (e.g. 'social') lives in Ring 1 capture_context, NOT
    in the modality enum.
  - Ring 3 edges are {type, target_unit_ref, evidence_ref} - a relation with an
    optional pointer to a supporting unit; NO edge-level confidence scalar
    (a scalar judgement is inference, not a graph relation).
  - Ring 2 Signal descriptors are Dict[str, float] over the frozen per-modality
    dimension set; NO per-dimension confidence, NO presence-boolean 'signals'.
  - Ring 4 extraction_params carry the modality-mandatory output-determining keys
    with temperature = 0 (deterministic-by-construction); extraction timestamp is
    NOT part of the reproducibility set.
  - Ring 5 score_vector = {genre_ceiling, source_standing, corroboration,
    recency_validity, contested}; NO 'headline' (headline-ness is genre-adjacent
    metadata in capture_context, not a defensibility axis).
"""

import json, uuid, hashlib, random
from datetime import datetime, timezone

random.seed(17)  # deterministic fixture
NOW = "2026-07-01T12:00:00Z"

# perception modality enum ONLY (source-type is provenance, not modality)
MODALITIES = ["text", "audio", "video", "image", "composite"]

# frozen per-modality Signal dimension set (markedness, not intent; no presence booleans)
SIGNAL_DIMS = {
    "audio": ["prosody", "vocal_emphasis", "affect_valence", "affect_arousal", "speech_rate", "pause_density"],
    "video": ["visual_emphasis", "scene_change_density", "framing_markedness"],
    "image": ["visual_emphasis", "composition_markedness"],
    "text":  ["lexical_intensity", "stance_intensity", "hedging_density"],
    "composite": [],  # no native dimensions; aggregates from constituents
}

GENRE_CEILING = {
    "report": "fact", "documentary": "fact",
    "speech": "utterance", "call_in": "utterance", "opinion": "utterance",
    "advertisement": "non_factual", "drama": "non_factual",
}

def sha(s): return hashlib.sha256(s.encode()).hexdigest()[:16]
def uid(): return str(uuid.uuid4())
def clamp(x): return max(0.0, min(1.0, round(x, 3)))

def score_vector(genre, standing, corroboration, contested):
    """Ring 5 score_vector - synthetic, illustrative. No 'headline'."""
    ceiling = {"fact": 1.0, "utterance": 0.6, "non_factual": 0.2}[GENRE_CEILING[genre]]
    standing_w = {"accountable": 1.0, "licensed_wire": 0.85,
                  "aggregator": 0.55, "ugc": 0.35, "unknown": 0.2}[standing]
    recency = clamp(random.uniform(0.5, 1.0))
    contested_w = {"uncontested": 1.0, "contested": 0.5, "retracted": 0.1}[contested]
    return {
        "genre_ceiling": clamp(ceiling),
        "source_standing": clamp(standing_w),
        "corroboration": clamp(corroboration),
        "recency_validity": recency,
        "contested": clamp(contested_w),
    }

def defensibility_class(genre, standing):
    """Genre sets the ceiling (authority-blind); source-standing can only lower."""
    ceil = GENRE_CEILING[genre]
    if ceil == "fact" and standing in ("ugc", "unknown"):
        return "utterance"
    return ceil

def signal_descriptors(modality, marks):
    """Dict[str,float] over the frozen dims for this modality. No confidence, no booleans."""
    allowed = SIGNAL_DIMS.get(modality, [])
    return {k: clamp(v) for k, v in (marks or {}).items() if k in allowed}

def extraction_params(modality):
    """Output-determining, modality-mandatory, temperature=0. No timestamp."""
    base = {"provider_id": "synthetic", "provider_version": "0",
            "extraction_run_id": uid(), "temperature": 0}
    if modality == "audio":
        base.update({"sample_rate_hz": 16000, "chunk_seconds": 30, "decoding": "greedy"})
    elif modality == "video":
        base.update({"keyframe_strategy": "interval", "keyframe_interval_s": 2,
                     "sample_rate_hz": 16000, "chunk_seconds": 30, "decoding": "greedy"})
    elif modality == "image":
        base.update({"target_resolution": "1024x1024", "ocr_engine": "paddleocr"})
    elif modality == "text":
        base.update({"source_format": "utf8", "normalization": "nfc"})
    return base

def make_unit(spec):
    unit_id = uid()
    genre, standing, modality = spec["genre"], spec["standing"], spec["modality"]
    contested = spec.get("contested", "uncontested")
    corroboration = spec.get("corroboration", 0.0)
    dclass = defensibility_class(genre, standing)
    locator = spec.get("locator", {"timestamp_ms": random.randint(0, 3_600_000)})

    # capture_context carries source-type (incl. 'social') + headline-ness metadata
    capture = {"programme": spec["programme"], "feed_id": spec["feed_id"],
               "source_type": spec.get("source_type", "broadcast")}
    if "headline" in spec:
        capture["headline"] = spec["headline"]

    return {
        "unit_id": unit_id,
        "unit_type": spec.get("unit_type", "claim"),
        "content": {"assertion": spec["text"], "language_mix": spec.get("lang", ["sw", "en"])},
        "freshness_stamp": {"logged_date": NOW, "structural_signature": sha(spec["text"])},

        # Ring 1: Provenance (modality = perception mechanism; source-type in context)
        "ring1_provenance": {
            "source_file_ref": spec["source_file"],
            "modality": modality,
            "locator": locator,
            "speaker_or_author": spec.get("speaker"),
            "capture_context": capture,
        },

        # Ring 2: Signal - Dict[str,float] over frozen dims; depth-judged; no confidence
        "ring2_signal": {
            "descriptors": signal_descriptors(modality, spec.get("marks")),
            "depth_judged": spec.get("depth_judged", True),
        },

        # Ring 3: Relational - {type, target_unit_ref, evidence_ref}; NO confidence
        "ring3_relational": {"edges": spec.get("edges", [])},

        # Ring 4: Re-extraction Handle - output-determining params, temperature=0, no timestamp
        "ring4_reextraction": {
            "raw_pointer": {"source_file_ref": spec["source_file"], "locator": locator},
            "perception_model": {"model_id": spec.get("model", "synthetic-fixture"), "version": "0"},
            "extraction_params": extraction_params(modality),
        },

        # Ring 5: Defensibility - score_vector without 'headline'
        "ring5_defensibility": {
            "defensibility_class": dclass,
            "claim_genre": genre,
            "source_standing": standing,
            "score_vector": score_vector(genre, standing, corroboration, contested),
            "matrix_rule_ref": f"qmatrix@v0::{genre}",
            "contested_status": contested,
        },

        "_fixture": {"synthetic": True, "plumbing_only": True, "v1_v3_valid": False,
                     "adversarial_intent": spec["intent"]},
    }

SPECS = []

# 1. hard code-switching sw/en/sheng - report
SPECS.append(dict(
    intent="code-switch: sw+en+sheng in one utterance; ASR + genre must survive",
    genre="report", standing="accountable", modality="audio",
    programme="Citizen Nipashe", feed_id="citizen_tv_news", speaker="anchor_1",
    lang=["sw", "en", "sheng"],
    text="Serikali imesema the fuel prices zita-drop next month, lakini wenye magari "
         "wanasema hiyo ni story tu - mtaskia venye mambo iko.",
    marks={"prosody": 0.4, "vocal_emphasis": 0.5}, corroboration=0.6))

# 2. genre-boundary drift: report -> opinion
SPECS.append(dict(
    intent="genre boundary: starts as report, drifts to opinion; must not over-call 'fact'",
    genre="opinion", standing="accountable", modality="audio",
    programme="Morning Cross-fire", feed_id="citizen_tv_news", speaker="host_2",
    text="The Treasury released the figures today - and frankly, anyone who believes "
         "them hasn't been paying attention. This is the same trick every year.",
    marks={"stance_intensity": 0.85, "hedging_density": 0.1, "vocal_emphasis": 0.6}))

# 3. advertisement mimicking a news read -> non_factual
SPECS.append(dict(
    intent="ad mimicking news read; must NOT be admitted as fact regardless of anchor voice",
    genre="advertisement", standing="accountable", modality="audio",
    programme="Citizen Nipashe", feed_id="citizen_tv_news", speaker="anchor_1",
    text="Na sasa habari njema - SafiSasa detergent imethibitishwa kuwa bora zaidi, "
         "inapatikana kila duka. Nunua leo.",
    marks={"vocal_emphasis": 0.6}, headline=True))

# 4-7 contested chain: claim -> corroborate -> contradict -> retract
claim_id, corrob_id, contra_id = uid(), uid(), uid()
SPECS.append(dict(
    intent="contested chain [1/4]: original claim (call-in, unverified)",
    genre="call_in", standing="ugc", modality="audio",
    programme="Jambo Kenya", feed_id="radio_jambo_callin", speaker="caller_anon",
    text="Mimi niko site, nasema hakuna maji imefika hapa Kayole for two weeks now.",
    marks={"affect_arousal": 0.6}, _id=claim_id))
SPECS.append(dict(
    intent="contested chain [2/4]: corroborating report (accountable, attributed)",
    genre="report", standing="accountable", modality="video",
    programme="Citizen Nipashe", feed_id="citizen_tv_news", speaker="reporter_3",
    text="Our team in Kayole confirmed water supply has been cut since the 14th, "
         "affecting several estates.",
    corroboration=0.8, marks={"visual_emphasis": 0.4},
    edges=[{"type": "corroborates", "target_unit_ref": claim_id, "evidence_ref": None}],
    _id=corrob_id))
SPECS.append(dict(
    intent="contested chain [3/4]: contradiction (wire, different figure)",
    genre="report", standing="licensed_wire", modality="text",
    programme="Wire Feed", feed_id="wire_kna", speaker=None,
    text="The county water authority stated supply was restored on the 20th.",
    contested="contested", corroboration=0.4, marks={"lexical_intensity": 0.3},
    edges=[{"type": "contradicts", "target_unit_ref": corrob_id, "evidence_ref": None}],
    _id=contra_id))
SPECS.append(dict(
    intent="contested chain [4/4]: retraction of the original claim",
    genre="report", standing="accountable", modality="text",
    programme="Citizen Correction", feed_id="citizen_tv_news", speaker="editor",
    text="Correction: an earlier report on Kayole water supply overstated the "
         "duration of the outage.",
    contested="retracted",
    edges=[{"type": "retracts", "target_unit_ref": claim_id, "evidence_ref": None}]))

# 8. authority-blind ceiling: tier-1 speech stays utterance
SPECS.append(dict(
    intent="authority-blind ceiling: speech on accountable feed stays utterance, not fact",
    genre="speech", standing="accountable", modality="video",
    programme="Live Address", feed_id="citizen_tv_news", speaker="official_A",
    text="I want to assure wananchi that the economy is now fully recovered and "
         "prices will fall by December.",
    marks={"vocal_emphasis": 0.7}))

# 9. source-standing lowers ceiling: UGC report -> utterance; social source-type
SPECS.append(dict(
    intent="source-standing lowers ceiling: unattributed UGC 'report' -> utterance",
    genre="report", standing="ugc", modality="text", source_type="social",
    programme="Social Ingest", feed_id="x_ingest", speaker="handle_xyz",
    text="BREAKING: bridge on Thika road imeanguka, cars stuck everywhere!!",
    marks={"lexical_intensity": 0.8}, contested="contested"))

# 10. diarization stress: sub-30s speaker, overlapping turns
SPECS.append(dict(
    intent="diarization stress: sub-30s speaker, overlapping turns",
    genre="call_in", standing="ugc", modality="audio",
    programme="Jambo Kenya", feed_id="radio_jambo_callin", speaker="caller_short",
    text="Ha! Si hiyo ni-- [overlap] --hapana, wewe sikiza.",
    marks={"speech_rate": 0.8, "pause_density": 0.2},
    locator={"timestamp_ms": 1_200_000, "duration_ms": 8_500}))

# 11. cross-modal: chyron (on-screen text) contradicts anchor audio; composite unit + edge
onscreen_id = uid()
SPECS.append(dict(
    intent="cross-modal: chyron (OCR text unit) contradicts anchor audio",
    genre="report", standing="accountable", modality="composite",
    programme="Citizen Nipashe", feed_id="citizen_tv_news", speaker="anchor_1",
    text="Anchor says 'three counties affected' while the chyron reads 'five counties'.",
    edges=[{"type": "contradicts", "target_unit_ref": onscreen_id, "evidence_ref": onscreen_id}]))

# 12. recency stress: documentary fact, 12 years old
SPECS.append(dict(
    intent="recency stress: documentary fact, but 12 years old - recency lowers score",
    genre="documentary", standing="accountable", modality="video",
    programme="Archive Doc", feed_id="citizen_archive", speaker="narrator",
    text="At the time of filming in 2014, the lake covered roughly 68 square kilometres.",
    corroboration=0.7, marks={"visual_emphasis": 0.3}))

# 13. drama stating a 'fact' -> non_factual
SPECS.append(dict(
    intent="drama stating a 'fact' - must floor to non_factual",
    genre="drama", standing="accountable", modality="video",
    programme="Tahidi High", feed_id="citizen_drama", speaker="character_omosh",
    text="In the script: 'The minister has fled the country with the money.'",
    marks={"framing_markedness": 0.6}))

# 14. ingestion robustness: partial/malformed, missing speaker
SPECS.append(dict(
    intent="ingestion robustness: partial/malformed content, missing speaker",
    genre="report", standing="unknown", modality="text",
    programme="Unknown Feed", feed_id="unclassified", speaker=None,
    text="...supply chain ??? [transcription gap] ... prices ...",
    marks={}, depth_judged=False))

# 15-18 opinion-dominant cluster (distribution must report, not gate)
for i in range(4):
    SPECS.append(dict(
        intent=f"defensibility skew: opinion-dominant segment [{i+1}/4] - distribution must not gate",
        genre="opinion", standing="aggregator", modality="text",
        programme="Panel Debate", feed_id="aggregator_blog", speaker=f"panelist_{i}",
        text=f"If you ask me, the whole policy is misguided - point number {i+1}.",
        marks={"stance_intensity": 0.8}))

# 19. clean positive: attributed wire fact
SPECS.append(dict(
    intent="clean positive: attributed wire report, uncontested fact",
    genre="report", standing="licensed_wire", modality="text",
    programme="Wire Feed", feed_id="wire_kna", speaker=None,
    text="The Central Bank held the benchmark rate at 10.75 percent, according to "
         "its published statement.",
    corroboration=0.75, marks={"lexical_intensity": 0.2}))

def main():
    units = []
    for spec in SPECS:
        spec = dict(spec)
        spec.setdefault("source_file", f"synthetic://{spec['feed_id']}/{sha(spec['text'])}.raw")
        spec.pop("_id", None)
        units.append(make_unit(spec))

    corpus = {
        "_manifest": {
            "fixture": "rms_adversarial_synthetic_v1", "synthetic": True,
            "plumbing_only": True, "v1_v3_valid": False,
            "note": "Author-labelled synthetic data. Exercises the pipeline only. "
                    "Accuracy measured against these labels is circular. Do NOT use "
                    "for V1 (convergence quality) or V3 (defensibility detection) - "
                    "those require real RMS material with human ground truth.",
            "shape": "five_rings@v0 (corrected: modality-enum-only, edge evidence_ref, "
                     "signal Dict[str,float] no per-dim confidence, extraction_params "
                     "temperature=0, score_vector without headline)",
            "generated_at": NOW, "unit_count": len(units),
            "genres": sorted(set(u["ring5_defensibility"]["claim_genre"] for u in units)),
            "source_standings": sorted(set(u["ring5_defensibility"]["source_standing"] for u in units)),
            "adversarial_coverage": [
                "code-switching (sw/en/sheng)", "genre-boundary ambiguity",
                "native-ad-as-news", "contested chain (claim/corroborate/contradict/retract)",
                "authority-blind genre ceiling", "source-standing lowering",
                "sub-30s + overlapping speakers", "cross-modal conflict (composite)",
                "recency skew", "drama-as-fact", "malformed ingestion",
                "opinion-dominant distribution", "clean positive control"],
        },
        "units": units,
    }
    out = "/home/claude/fixture/rms_adversarial_synthetic_v1.json"
    with open(out, "w") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    from collections import Counter
    gc = Counter(u["ring5_defensibility"]["claim_genre"] for u in units)
    dc = Counter(u["ring5_defensibility"]["defensibility_class"] for u in units)
    cs = Counter(u["ring5_defensibility"]["contested_status"] for u in units)
    print(f"units: {len(units)}")
    print(f"genres: {dict(gc)}")
    print(f"defensibility_class: {dict(dc)}")
    print(f"contested_status: {dict(cs)}")
    print(f"written: {out}")

if __name__ == "__main__":
    main()
