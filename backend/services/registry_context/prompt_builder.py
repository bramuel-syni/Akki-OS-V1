"""Registry-context prompt-builder · SINGLE WRITER discipline per Binding B-1.

Owner ruling `docs/rulings/g_13_e1_e2_e3_2026_07_25.md` verbatim on Binding B-1:
    "No seal does not mean no shape. The block is emitted by exactly one
    writer (prompt_builder.py), its content sourced from the Registry
    record — never hand-authored — and a hard-fail cell asserts the
    exact rendered serialization against a golden snapshot for a fixture
    function. 'Markdown, no seal' must not decay into 'freeform string
    anyone edits.'"

Owner ruling §5.1 (b) verbatim: annotated markdown block with
`### Function: <id>` sub-headers and `**Mandate:**` / `**Promise:**` /
`**Service trace:**` labels.

Block format (deterministic · byte-stable across runs):

    ## Registry context · promises in force on this task

    ### Function: <function_id>
    **Mandate:** <mandate text>

    **Promise:** <promise text>

    **Service trace:**
    - <service_trace[0]>
    - <service_trace[1]>
    - ...

    ---

    (repeat per function_id · separated by `---`)
"""
from __future__ import annotations

from typing import List

from services.registry_context.reader import RegistryRow, read_row


BLOCK_HEADER = "## Registry context · promises in force on this task"
FUNCTION_SEPARATOR = "---"


def _render_one_row(row: RegistryRow) -> str:
    """Render one Registry row to the fixed markdown shape · deterministic."""
    trace_lines = "\n".join(f"- {ref}" for ref in row.service_trace)
    return (
        f"### Function: {row.function_id}\n"
        f"**Mandate:** {row.mandate}\n"
        f"\n"
        f"**Promise:** {row.promise}\n"
        f"\n"
        f"**Service trace:**\n"
        f"{trace_lines}"
    )


def build_context_block(function_ids: List[str]) -> str:
    """Build the markdown context block for the given function IDs.

    SINGLE WRITER: this function is the only path from Registry rows to
    the rendered context block. No caller may hand-author or splice the
    block content directly.

    Output is deterministic — same input yields byte-identical output.
    """
    rendered_rows = [_render_one_row(read_row(fn_id)) for fn_id in function_ids]
    body = f"\n\n{FUNCTION_SEPARATOR}\n\n".join(rendered_rows)
    return f"{BLOCK_HEADER}\n\n{body}"
