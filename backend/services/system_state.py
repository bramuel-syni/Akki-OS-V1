"""System state surface — G0.5 expanded.

Returns gate status + data-source mode + V-gate pending list + Layer A
handlers + Layer B providers + V1 harness verdict + adversarial-fixture
flag, per G0.5 Deliverable 5.
"""
from __future__ import annotations

from typing import Dict, List

from core import APP_NAME, iso, now
from services.layer_a.dispatcher import supported_extensions
from services.layer_b.factory import available_providers, list_provider_names
from services.v1_harness import last_report


def _rms_adversarial_v1_manifest() -> Dict:
    """Read the regenerated adversarial fixture v1 manifest flags (post-HAZARD-STOP #1).
    Surfaced honestly so V1/V3 harnesses + audit lens see `v1_v3_valid=False`."""
    import json, os
    p = os.path.join(os.path.dirname(__file__), "..", "services",
                     "data_source", "synthetic_assets",
                     "rms_adversarial_v1", "fixture.json")
    try:
        with open(os.path.abspath(p)) as f:
            m = json.load(f).get("_manifest", {})
        return {"fixture": m.get("fixture"), "synthetic": m.get("synthetic"),
                "plumbing_only": m.get("plumbing_only"),
                "v1_v3_valid": m.get("v1_v3_valid"),
                "unit_count": m.get("unit_count")}
    except FileNotFoundError:
        return {"fixture": None, "synthetic": None, "plumbing_only": None,
                "v1_v3_valid": None, "unit_count": None}

_VGATES: List[Dict[str, str]] = [
    {"id": "V1", "gates": "G2", "description": "Akki convergence quality on one real RMS hour.", "status": "pending"},
    {"id": "V2", "gates": "G6", "description": "RMS rights past extract-for-RMS + Liquid C2 substrate contract.", "status": "pending"},
    {"id": "V3", "gates": "G1", "description": "Defensibility detection accuracy on real content.", "status": "pending"},
]


def current_system_state(data_source_name: str, data_source_mode: str) -> Dict:
    handlers = sorted(supported_extensions().keys())
    providers = list_provider_names()
    availability = available_providers()
    report = last_report()
    v1_verdict = report.verdict if report else "PENDING_REAL_MATERIAL"
    return {
        "app": APP_NAME,
        "gate": "G6",
        "data_source": {
            "name": data_source_name,
            "mode": data_source_mode,
            "running_on_synthetic": data_source_mode == "synthetic",
            "rms_adversarial_v1": _rms_adversarial_v1_manifest(),
        },
        "synthetic_fixture_adversarial": True,
        "layer_a_handlers": handlers,
        "layer_b_providers": {
            "asr": providers["asr"], "diarization": providers["diarization"],
            "vision": providers["vision"], "availability": availability,
        },
        "signal_ring_dimensions_rev": "v0",
        "g1_components": {
            "genre_classifier": "v0",
            "source_standing_reader": "declaration_baseline_only",
            "ring5_stamper": "v0",
            "solva_depth": "v1",
        },
        "defensibility_runtime_mode": "declaration_baseline",
        "v_gates": _VGATES,
        "v1_status": v1_verdict,
        "v1_pending": v1_verdict != "PASS",
        "v3_status": "PENDING_REAL_LABELLED_SET",
        "v3_pending": True,
        "qualification_matrix_rev": "v0",
        "extraction_params_rev": "v0",
        "northena_ledger_row_rev": "v0",
        "northena_ledger_retention_mode": __import__("os").environ.get(
            "RMS_NORTHENA_LEDGER_RETENTION_MODE", "indefinite"),
        "g2_components": {
            "northena_admit": "v0", "northena_gate": "v0",
            "northena_converge": "v0", "northena_ledger": "v0",
            "solva_admit_assist": "v0",
        },
        "g3_components": {
            "solva_assertion_boundary": "v0",
            "solva_reasoning_faculty": "v0 (5 stages: frame, candidate, tension, probability, reflection)",
            "solva_load_bearing": "v0",
            "solva_enforce": "v0",
            "solva_stamp": "v0",
            "solva_trace": "v0",
            "solva_pipeline": "v0",
            "layer_c_convergence": "v0 (signal-ring conformance gate)",
            "northena_converge_solva_absorb": "v0 (absorb_solva_trace seam)",
        },
        "g4_components": {
            "mtafiti_census": "v0",
            "mtafiti_declaration_baseline": "v0 (LIVE)",
            "mtafiti_inference": "v0 (DARK stubs; V3 closed seam)",
            "mtafiti_measure": "v0",
            "mtafiti_verdict": "v0 (Matrix lookup)",
            "mtafiti_registry": "v0",
            "mtafiti_v3_overlay": "v0 (CLOSED_SEAM; V3Thresholds=None)",
            "mtafiti_source_standing_table": "v0 (synthetic_placeholder / non_editorial_authority)",
            "targeta_core": "v0 (LIVE — deterministic eligibility + ranking)",
            "targeta_yield_layer": "v0 (CLOSED_SEAM; YieldThresholds=None)",
            "targeta_gate": "v0 (yield admission returns admitted=False when thresholds=None)",
            "targeta_plan": "v0",
            "service_1": "v0 (Day-Zero end-to-end composition; terminates at convergence)",
            "northena_ledger_retention": "indefinite (default; DPO decision open — end-of-window deletion UNIMPLEMENTED)",
        },
        "closed_seams": [
            "mtafiti_v3_overlay (Owner thresholds: fact_precision, genre_accuracy, inter_annotator_floor)",
            "targeta_yield_layer (Owner thresholds: min_efficiency_gain, coverage_alpha, held_out_set_composition)",
            "northena_ledger_deletion (DPO decision: retention window duration)",
        ],
        "g5a_components": {
            "northena_trace_lens": "v0 (GET /api/northena/trace/{trace_id} — cross-engine correlation; READ-ONLY)",
            "discipline_lift_manifest": "v0 (GET /api/discipline/lift_manifest — manifest + spec fingerprints + Rule 2 v2 per phase; READ-ONLY)",
            "trace_lens_envelope_contract": "v0 (TraceLensEnvelope — FROZEN)",
            "lift_manifest_envelope_contract": "v0 (LiftManifestEnvelope — FROZEN)",
        },
        "g6_components": {
            "outer_gate_transform": "v0 (services/outer_gate/transform.py — HMAC-SHA256 pseudonymisation + feed_id/structural_signature generalisation)",
            "outer_gate_mint": "v0 (services/outer_gate/mint.py — MintRegistry with purged-mint lifecycle)",
            "outer_gate_receipt": "v0 (services/outer_gate/receipt.py — irreversibility receipt builder)",
            "v2_gate_refusal": "v0_LIVE (services/v2_gate/refusal.py — 4 refusal reason codes)",
            "v2_gate_cumulative": "v0_BUILT_CLOSED_SEAM (services/v2_gate/cumulative.py — Shape B, arm_admitted() -> False until DPO/Owner thresholds land)",
            "northena_absorb_outer_gate_receipt": "v0 (services/northena/converge.py — absorbs into stamp_audit side-channel; no contract mutation)",
            "northena_absorb_v2_refusal": "v0 (services/northena/converge.py — absorbs into stamp_audit side-channel; no contract mutation)",
            "outer_gate_receipt_contract": "v0 (OuterGateReceipt@v0 — FROZEN)",
            "v2_refusal_envelope_contract": "v0 (V2RefusalEnvelope@v0 — FROZEN)",
            "cumulative_disclosure_ledger_contract": "v0 (CumulativeDisclosureLedger@v0 — FROZEN)",
        },
        "cumulative_arm_status": "built_closed_seam",
        "cumulative_arm_config_unlock_path": "Set RMS_G6_K_ANONYMITY_THRESHOLD + RMS_G6_L_DIVERSITY_THRESHOLD + RMS_G6_DP_EPSILON_BUDGET env vars (DPO/Owner decision per Product v2.1 §32)",
        "engines_resolvable_by_trace_id": [
            "northena_ledger", "solva", "targeta", "mtafiti", "service_1",
        ],
        "contracts_frozen": [
            "five_rings@v0", "objective_request@v0",
            "qualification_matrix@v0", "signal_ring_dimensions@v0",
            "extraction_params@v0", "northena_ledger_row@v0",
            "mtafiti_registry_record@v0", "targeta_mining_plan@v0",
            "trace_lens_envelope@v0", "lift_manifest_envelope@v0",
            "outer_gate_receipt@v0", "v2_refusal_envelope@v0",
            "cumulative_disclosure_ledger@v0",
        ],
        "time": iso(now()),
    }
