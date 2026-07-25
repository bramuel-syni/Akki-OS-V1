"""Registry context · operating-prompt injector · fold B.WCH.3.

Registry Doctrine §6.2 verbatim: *"every model worker receives the
promises in force on its task [...] as part of its operating prompt"*.

Composes the prompt-builder markdown block with the operating-prompt
body. Single-writer discipline per Binding B-1: this module is the ONLY
consumer of prompt_builder.build() for prompt-construction purposes.
"""
from __future__ import annotations

from typing import List

from services.registry_context.prompt_builder import build_context_block


def inject_context_into_prompt(
    operating_prompt_body: str,
    declared_function_ids: List[str],
) -> str:
    """Compose the context block ABOVE the operating-prompt body.

    Owner-verbatim (§6.2): *"as part of its operating prompt"* — the
    block prepends the body; single delimiting newline between block
    and body.
    """
    block = build_context_block(declared_function_ids)
    return f"{block}\n\n{operating_prompt_body}"
