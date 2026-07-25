# GENERATED · DO NOT EDIT
# Source: docs/mandates/RMS_UI_Specification_v1.md
# Source SHA-256: 9053a4c451954cca1dc2f2b10216bef2058411a1911136581251e395d5bdcbf3
# Generator: backend/services/far_endpoint/gate_generator.py
# Regenerate: python -m services.far_endpoint.gate_generator

def RMS_UI_Specification_v1_gate_000(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-000

    Refusal reason: Mandate gate 000 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Binding copy: "Frozen is immutable — a changed intent is a new objective."
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_001(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-001

    Refusal reason: Mandate gate 001 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Warning card in the answer position. Binding copy: title "Not to the standard you asked for."; body names the gap in the actor-appropriate form (pattern: "No corroboration at the required standard was found for the load-bearing claims. The statement itself is on record — it can be reported as a recorded statement, not asserted as fact."); line "Asked: {floor} · Supported: {class}"; actions (binding labels): **Accept as recorded statement** · **Narrow the objective** · **Lower the standard**.
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_002(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-002

    Refusal reason: Mandate gate 002 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Footer (binding copy): "A refusal is the system keeping its promise…" + **Why this was refused** link.
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_003(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-003

    Refusal reason: Mandate gate 003 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Elements: request block (`POST /v1/objectives` with ask / standard / scope); two response panels side by side — **Answered** (`outcome`, `trace_id`, claim, `defensibility` inline, provenance) and **Refused — same envelope, body discriminator** (`outcome: refused`, `asked`, `supported_class`, `what_would_raise_it`).
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_004(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-004

    Refusal reason: Mandate gate 004 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Binding copy: "There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals."
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_005(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-005

    Refusal reason: Mandate gate 005 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Elements: at most one attention card (pattern: app name — refusal rate — plain-language cause — **Review**); apps list rows — name + class badge, path + key, calls + refusal rate; extract-path rows show acquisitions + rights state; async addition: long-running objectives show lifecycle state (`accepted / running / delivered / refused`).
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_006(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-006

    Refusal reason: Mandate gate 006 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Rules: shaping is bounded by offerability (owned estate, license class, disclosure limits) — out-of-bounds shapes are refused with the reason; buyer never sets lawful basis.
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_007(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-007

    Refusal reason: Mandate gate 007 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Binding copy (footer): "If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered."
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_008(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-008

    Refusal reason: Mandate gate 008 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Binding copy: "Recorded as your change, with today's date."
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_009(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-009

    Refusal reason: Mandate gate 009 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): Elements: trace lookup ("Look up any run, claim, or acquisition by trace…"); attention card stating problems honestly (pattern: "One retention window has passed — … It has not been auto-deleted; that rule isn't set."); three cards — runs with lawful basis, refusals this month + **See what was refused** link, retention windows past due.
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None


def RMS_UI_Specification_v1_gate_010(payload):
    """Source anchor: docs/mandates/RMS_UI_Specification_v1.md#stanza-010

    Refusal reason: Mandate gate 010 from docs/mandates/RMS_UI_Specification_v1.md · RMS Intelligence System — UI Specification
    Condition (verbatim from source): - **Binding copy set** (verbatim across surfaces): "Not to the standard you asked for." · the three refusal action labels · "agent-assumed" · "Frozen is immutable — a changed intent is a new objective." · the §4.2 contract caption · the §5.2 acquisition framing and footer · the §7.3 retention banner.
    """
    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).
    # Concrete condition body evolves per engine-version bump (Class E discipline).
    return None
