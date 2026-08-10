"""Step 6 (final) of MTI multistep pipeline: assemble pyfcstm DSL from upstream lists."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from method.gpt_client import chat


_PROMPT_PATH = Path(__file__).resolve().parent.parent.parent / "prompts" / "multistep" / "build_pyfcstm.txt"
_GRAMMAR_PATH = Path(__file__).resolve().parent.parent.parent / "prompts" / "_pyfcstm_grammar.md"


def _load_prompt() -> str:
    """Load the build_pyfcstm system prompt + append the shared grammar."""
    if not _PROMPT_PATH.exists():
        raise FileNotFoundError(f"build_pyfcstm prompt not found: {_PROMPT_PATH}")
    body = _PROMPT_PATH.read_text(encoding="utf-8")
    if _GRAMMAR_PATH.exists():
        grammar = _GRAMMAR_PATH.read_text(encoding="utf-8")
        return f"{body}\n\n---\n\n{grammar}"
    return body


_FENCE_RE = re.compile(r"```(?:fcstm|pyfcstm|dsl|text)?\s*\n?(.*?)```", re.DOTALL)


def _strip_dsl_fence(content: str) -> str:
    """If the model wrapped the DSL in ``` ... ```, strip it."""
    s = content.strip()
    if not s.startswith("```"):
        return s
    m = _FENCE_RE.search(s)
    if m:
        return m.group(1).strip()
    return s


def build_pyfcstm(
    requirements: str,
    state_list: list[dict],
    event_list: list[dict],
    variable_list: list[dict],
    transition_list: list[dict],
    action_list: list[dict],
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[str, dict]:
    """Run Step 6 — assemble the complete pyfcstm DSL.

    Unlike Steps 1-5 (JSON output), this step emits raw DSL text. Returns
    ``(dsl_text, usage)``.
    """
    system_prompt = _load_prompt()
    lists_payload = {
        "States": state_list,
        "Events": event_list,
        "Variables": variable_list,
        "Transitions": transition_list,
        "Actions": action_list,
    }
    user_msg = (
        f"Requirements:\n{requirements.strip()}\n\n"
        f"Upstream lists:\n```json\n{json.dumps(lists_payload, ensure_ascii=False, indent=2)}\n```\n\n"
        f"Assemble the complete pyfcstm DSL. Output the DSL code only."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
    )
    return _strip_dsl_fence(content), usage
