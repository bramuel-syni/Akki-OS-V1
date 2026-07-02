"""Layer B — Perception (parallel per-modality).

Package shape per G0.5 brief Deliverable 3: TWO architecturally-different
ASR providers + one diarization (pyannote) + one vision-LM, all callable
through the extended Shield perception_router.

Providers are CONTRACT-BACKED via Protocols in `contracts.py`. They
attempt to import their heavy dependencies inside the class body; if a
dep is missing they raise `ProviderUnavailable` on construction, with
the `install X` message. This keeps `make ci` fast on plumbing.
"""
from services.layer_b.contracts import (  # noqa: F401
    AsrProvider,
    DiarizationProvider,
    PerceptionArtifact,
    ProviderUnavailable,
    VisionProvider,
)
from services.layer_b.factory import (  # noqa: F401
    available_providers,
    get_asr_provider,
    get_diarization_provider,
    get_vision_provider,
)
