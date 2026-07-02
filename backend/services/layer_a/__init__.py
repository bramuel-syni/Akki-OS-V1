"""Layer A — Retrieve.

This package is the modality-aware fetch layer of the Akki engine
(Spec §4.1 / §4.3). It NEVER perceives — only retrieves raw bytes from a
source_ref and emits a typed `Raw*Artifact`.

Dispatch shape lifted (LIFT_AND_EXTEND) from the cousin's text-only
`documents_service.py::extract_text` + `ACCEPT_EXT` pattern. Cousin
refs in the dispatcher / handler module docstrings.

G0.5 build-only: providers consume these artefacts; V1 harness measures
perception quality; no V-gate consumption against synthetic.
"""
from services.layer_a.dispatcher import (  # noqa: F401
    Layer_A_DispatchError,
    UnsupportedModality,
    retrieve,
    supported_extensions,
)
from services.layer_a.types import (  # noqa: F401
    RawArtifact,
    RawAudioArtifact,
    RawImageArtifact,
    RawTextArtifact,
    RawTranscriptArtifact,
    RawVideoArtifact,
)
