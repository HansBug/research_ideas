"""SpecExtractor agent: NL → structured JSON spec.

The first stage of the agent loop. Reads the natural-language input and
produces a ``SpecJson`` intermediate representation (states / events /
variables / transitions / hierarchy). The downstream Modeler agent turns this
spec into pyfcstm DSL.

Design choices:

- The prompt lives in ``archive/agent_loop_method/prompts/spec_extractor.txt`` (separated for
  ease of review without diffing Python).
- We request ``response_format={"type": "json_object"}`` to force valid JSON.
  Some proxy backends ignore this; we fall back to manual fence stripping.
- ``temperature=0.0`` for reproducibility; optional ``seed`` is passed through
  for providers that honor it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from archive.agent_loop_method.gpt_client import chat
from archive.agent_loop_method.schema import SpecJson


_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "spec_extractor.txt"


def _load_prompt() -> str:
    if not _PROMPT_PATH.exists():
        raise FileNotFoundError(f"SpecExtractor prompt not found: {_PROMPT_PATH}")
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _strip_json_fence(content: str) -> str:
    """Remove ```json ... ``` code fences if the model returned them despite
    response_format=json_object."""
    s = content.strip()
    if not s.startswith("```"):
        return s
    parts = s.split("```")
    if len(parts) >= 2:
        body = parts[1]
        if body.startswith("json"):
            body = body[4:]
        elif body.startswith("JSON"):
            body = body[4:]
        return body.strip()
    return s


def extract_spec(nl_input: str, *, seed: Optional[int] = None, model: Optional[str] = None) -> tuple[SpecJson, dict]:
    """Run SpecExtractor on a single NL input.

    Parameters
    ----------
    nl_input
        Natural-language control system description (e.g. from ``sources/<dir>/STM.md`` §2).
    seed
        Optional integer for LLM-call determinism (some providers honor this).
    model
        Override the default ``LLM_MODEL`` env var. ``None`` => use env.

    Returns
    -------
    (spec, usage)
        ``spec``: populated ``SpecJson`` dataclass.
        ``usage``: token usage dict from ``gpt_client.chat``.
    """
    system_prompt = _load_prompt()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Extract the spec from this NL:\n\n{nl_input}"},
    ]
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
        response_format={"type": "json_object"},
    )
    raw_text = _strip_json_fence(content)
    try:
        raw = json.loads(raw_text)
    except json.JSONDecodeError as e:
        # Surface the raw text so the caller can inspect what the model emitted.
        raise ValueError(f"SpecExtractor returned non-JSON content: {raw_text[:500]}...") from e

    spec = SpecJson(
        states=raw.get("states", []),
        events=raw.get("events", []),
        variables=raw.get("variables", []),
        transitions=raw.get("transitions", []),
        hierarchy=raw.get("hierarchy", []),
        raw=raw,
    )
    return spec, usage
