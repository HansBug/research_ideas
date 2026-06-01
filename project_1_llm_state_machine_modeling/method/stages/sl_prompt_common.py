"""Shared helpers for PR-1B SL prompt generators.

These helpers are deliberately prompt-only: they do not call LLM providers and
never read ``.env``.  They only format deterministic message packs and validate
fixture/fake responses used by tests.
"""

from __future__ import annotations

import json
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
    parts = s.split("```")
    if len(parts) >= 2:
        body = parts[1]
        first_nl = body.find("\n")
        if first_nl != -1:
            first_line = body[:first_nl].strip().lower()
            if first_line in {"json", "fcstm", "pyfcstm", "dsl", "text", ""}:
                body = body[first_nl + 1 :]
        return body.strip()
    return s


def parse_json_response(content: str, *, context: str) -> dict[str, Any]:
    raw = strip_fence(content)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{context}: response is not valid JSON: {raw[:300]}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{context}: response JSON must be an object")
    return parsed


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
