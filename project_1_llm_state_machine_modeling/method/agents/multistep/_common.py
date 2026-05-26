"""Shared helpers for the 6-step MTI-style multistep pipeline."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Optional

from method.gpt_client import chat


PROMPT_DIR = Path(__file__).resolve().parent.parent.parent / "prompts" / "multistep"


def load_prompt(step_name: str) -> str:
    """Load a prompt template by step name (e.g. 'identify_state')."""
    path = PROMPT_DIR / f"{step_name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Multistep prompt not found: {path}")
    return path.read_text(encoding="utf-8")


_JSON_FENCE_RE = re.compile(r"```(?:json|JSON)?\s*(.*?)\s*```", re.DOTALL)


def extract_json(content: str) -> dict:
    """Extract a single JSON object from an LLM response.

    Tries (in order):
    1. The whole content as raw JSON.
    2. The first ```json ... ``` fenced block.
    3. The longest balanced-brace substring starting at the first `{`.
    """
    s = content.strip()
    # 1. raw JSON
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass

    # 2. ```json ... ``` fenced
    m = _JSON_FENCE_RE.search(s)
    if m:
        body = m.group(1).strip()
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            pass

    # 3. balanced-brace fallback
    start = s.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in LLM response. Start: {s[:200]!r}")
    depth = 0
    for i, ch in enumerate(s[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = s[start : i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    pass
                break
    raise ValueError(
        f"Could not extract a parseable JSON object from LLM response. "
        f"First 300 chars: {s[:300]!r}"
    )


def call_step(
    *,
    step_name: str,
    user_message: str,
    seed: Optional[int] = None,
    model: Optional[str] = None,
    force_json: bool = True,
) -> tuple[dict, dict]:
    """Run one step of the multistep pipeline.

    Loads ``prompts/multistep/<step_name>.txt`` as the system prompt, sends
    the supplied ``user_message`` as the user prompt, parses the response as
    JSON, and returns (parsed_dict, token_usage).

    Parameters
    ----------
    step_name
        e.g. ``"identify_state"`` — must correspond to a file under
        ``method/prompts/multistep/``.
    user_message
        The user-side prompt content (typically begins with "Requirements:
        ..." plus upstream lists).
    seed
        Optional integer seed for reproducibility (some providers honor it).
    model
        Override ``LLM_MODEL`` env var. ``None`` => use env default.
    force_json
        If True, request ``response_format={"type": "json_object"}``.
    """
    system_prompt = load_prompt(step_name)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    kwargs: dict[str, Any] = {
        "messages": messages,
        "model": model,
        "temperature": 0.0,
        "seed": seed,
    }
    if force_json:
        kwargs["response_format"] = {"type": "json_object"}

    content, usage = chat(**kwargs)
    parsed = extract_json(content)
    return parsed, usage


def build_user_message(
    *,
    requirements: str,
    upstream: Optional[dict[str, Any]] = None,
    opening_cue: Optional[str] = None,
) -> str:
    """Assemble a user message in the canonical 'Requirements + upstream lists + cue' form.

    Parameters
    ----------
    requirements
        The raw NL requirements text.
    upstream
        Optional dict of upstream lists, e.g. ``{"States": state_list, "Events": event_list}``.
        Each value is serialized to JSON and labeled in the prompt.
    opening_cue
        Optional final line like ``"Identified Event List:"`` — gives the LLM
        a "continue from here" anchor before its JSON output.
    """
    parts = [f"Requirements:\n{requirements.strip()}\n"]
    if upstream:
        for label, value in upstream.items():
            payload = json.dumps(value, ensure_ascii=False, indent=2) if not isinstance(value, str) else value
            parts.append(f"{label}:\n{payload}\n")
    if opening_cue:
        parts.append(opening_cue)
    return "\n".join(parts)
