"""Shared helpers for PR-1B SL prompt generators.

These helpers are deliberately prompt-only: they do not call LLM providers and
never read ``.env``.  They only format deterministic message packs and validate
fixture/fake responses used by tests.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

METHOD_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_ROOT = METHOD_ROOT / "prompts"
GRAMMAR_PATH = PROMPTS_ROOT / "_pyfcstm_grammar.md"


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_text_required(path: Path, *, label: str) -> str:
    """Read a repo-local prompt file and fail loudly if it is missing."""
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path.read_text(encoding="utf-8")


def load_grammar_digest(override: str | None = None) -> str:
    if override is not None:
        return override
    return read_text_if_exists(GRAMMAR_PATH)


def to_jsonable(value: Any) -> Any:
    """Convert stdlib dataclasses and simple objects to JSON-friendly values."""
    if value is None:
        return None
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    return value


def dumps_pretty(value: Any) -> str:
    return json.dumps(to_jsonable(value), ensure_ascii=False, indent=2, default=str)


def fenced_json(value: Any) -> str:
    return f"```json\n{dumps_pretty(value)}\n```"


def fenced_text(value: str, language: str = "") -> str:
    lang = language.strip()
    return f"```{lang}\n{value.strip()}\n```"


def strip_fence(content: str) -> str:
    s = content.strip()
    if not s.startswith("```"):
        return s
    first_nl = s.find("\n")
    if first_nl == -1:
        return s
    fence_header = s[3:first_nl].strip().lower()
    if fence_header not in {"json", "fcstm", "pyfcstm", "dsl", "text", ""}:
        return s
    body = s[first_nl + 1 :]
    # Only remove a closing fence that appears on its own final line.  Do not
    # split on arbitrary ``` substrings because valid JSON strings may contain
    # Markdown fence markers as data.
    lines = body.splitlines()
    if lines and lines[-1].strip() == "```":
        body = "\n".join(lines[:-1])
    return body.strip()


def parse_json_response(content: str, *, context: str) -> dict[str, Any]:
    raw = strip_fence(content)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        repaired = _extract_json_object(raw)
        if repaired is None:
            raise ValueError(f"{context}: response is not valid JSON: {raw[:300]}") from exc
        try:
            parsed = json.loads(repaired)
        except json.JSONDecodeError as repaired_exc:
            raise ValueError(f"{context}: response is not valid JSON: {raw[:300]}") from repaired_exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{context}: response JSON must be an object")
    return parsed


def _extract_json_object(raw: str) -> str | None:
    """Recover the first balanced JSON object from noisy LLM output.

    Some OpenAI-compatible providers occasionally prepend prose, append
    stop-sequence artifacts, or repeat partial JSON even when
    ``response_format={"type": "json_object"}`` is requested.  For PR-3 smoke
    this best-effort extraction is acceptable because the subsequent strict
    schema parser still validates every required field.
    """
    match = re.search(r"\{", raw)
    if match is None:
        return None
    start = match.start()
    depth = 0
    in_string = False
    escape = False
    for index, char in enumerate(raw[start:], start=start):
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return raw[start : index + 1]
    return None


def require_one_of(value: Any, allowed: set[str], field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if value not in allowed:
        allowed_text = ", ".join(sorted(allowed))
        raise ValueError(f"{field_name} must be one of: {allowed_text}")
    return value


def message_pack(system: str, user: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system.strip()},
        {"role": "user", "content": user.strip()},
    ]
