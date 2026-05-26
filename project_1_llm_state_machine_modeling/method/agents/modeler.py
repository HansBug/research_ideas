"""Modeler agent: structured JSON spec → pyfcstm DSL.

The second stage of the agent loop. Reads the ``SpecJson`` produced by
SpecExtractor and produces a pyfcstm DSL text. The DSL output then goes
through the four deterministic feedback sources (Parse / Semantic / Sim /
Judge).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from method.gpt_client import chat
from method.schema import ModelArtifact, SpecJson


_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "modeler.txt"


def _load_prompt() -> str:
    if not _PROMPT_PATH.exists():
        raise FileNotFoundError(f"Modeler prompt not found: {_PROMPT_PATH}")
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _strip_dsl_fence(content: str) -> str:
    """If the model wrapped the DSL in a ``` fenced block, strip it."""
    s = content.strip()
    if not s.startswith("```"):
        return s
    parts = s.split("```")
    if len(parts) >= 2:
        body = parts[1]
        # First-line language tag (e.g. "fcstm" / "pyfcstm" / "dsl") gets stripped
        first_nl = body.find("\n")
        if first_nl != -1:
            first_line = body[:first_nl].strip().lower()
            if first_line in ("fcstm", "pyfcstm", "dsl", "text", ""):
                body = body[first_nl + 1:]
        return body.rstrip().rstrip("`").rstrip()
    return s


def generate_model(
    spec: SpecJson,
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[ModelArtifact, dict]:
    """Run Modeler on a SpecJson.

    Parameters
    ----------
    spec
        The structured spec from SpecExtractor.
    seed
        Optional integer for LLM-call determinism (some providers honor this).
    model
        Override the default ``LLM_MODEL`` env var. ``None`` => use env.

    Returns
    -------
    (artifact, usage)
        ``artifact``: ``ModelArtifact`` with the generated DSL text.
        ``usage``: token usage dict from ``gpt_client.chat``.
    """
    system_prompt = _load_prompt()
    spec_json_str = json.dumps(spec.raw if spec.raw else _spec_to_dict(spec), ensure_ascii=False, indent=2)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate the pyfcstm DSL from this spec:\n\n{spec_json_str}"},
    ]
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
    )
    dsl_text = _strip_dsl_fence(content)
    artifact = ModelArtifact(
        dsl_text=dsl_text,
        iteration=0,
        produced_by="modeler",
    )
    return artifact, usage


def _spec_to_dict(spec: SpecJson) -> dict:
    """Fallback if spec.raw was not populated."""
    return {
        "states": spec.states,
        "events": spec.events,
        "variables": spec.variables,
        "transitions": spec.transitions,
        "hierarchy": spec.hierarchy,
    }
