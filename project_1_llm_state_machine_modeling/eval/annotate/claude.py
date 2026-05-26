"""Claude CLI annotator.

Subprocesses the ``claude`` binary in non-interactive mode (``-p ...
--output-format json``). All CLI knobs are read from environment variables
(``CLAUDE_CMD`` / ``CLAUDE_MODEL``), never from system-level config files.

Returns a parsed ``dict`` with keys:

- ``annotations``: list[dict]   — per-instance TP/FP/FN rows
- ``summary``: dict            — {"tp", "fp", "fn", "notes"}
- ``_meta``: dict              — {"annotator": "claude", "model": ...,
                                  "raw": <full claude JSON envelope>,
                                  "usage": {...}}

Caller is responsible for handling exceptions; the wrapper raises
``RuntimeError`` for non-zero exit codes and ``ValueError`` for non-JSON
``result`` content.
"""
from __future__ import annotations

import json
import os
import subprocess
from typing import Any


def annotate(*, system_prompt: str, user_prompt: str, timeout_s: int = 300) -> dict[str, Any]:
    cmd_bin = os.environ.get("CLAUDE_CMD", "claude")
    model = os.environ.get("CLAUDE_MODEL", "").strip()

    # Claude `-p` non-interactive takes the user prompt on argv.
    # System prompt goes via `--append-system-prompt` (we do not replace
    # the built-in Claude Code system since it's harmless context).
    full_user = (
        f"<SYSTEM>\n{system_prompt}\n</SYSTEM>\n\n"
        f"{user_prompt}"
    )
    cmd = [cmd_bin, "-p", full_user, "--output-format", "json"]
    if model:
        cmd += ["--model", model]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"claude CLI timed out after {timeout_s}s") from e
    if result.returncode != 0:
        raise RuntimeError(
            f"claude CLI exit={result.returncode}; stderr:\n{result.stderr[-800:]}"
        )

    try:
        envelope = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"claude stdout not JSON: {result.stdout[:400]}") from e

    if envelope.get("is_error"):
        raise RuntimeError(f"claude reported is_error: {envelope.get('result') or envelope}")

    raw_text = envelope.get("result", "")
    # The model sometimes wraps JSON in ```json ... ``` despite our prompt.
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        first_nl = cleaned.find("\n")
        if first_nl >= 0:
            cleaned = cleaned[first_nl + 1 :]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"claude result is not parseable JSON; first 400 chars:\n{raw_text[:400]}"
        ) from e

    parsed.setdefault("annotations", [])
    parsed.setdefault("summary", {})
    parsed["_meta"] = {
        "annotator": "claude",
        "model": model or "(claude default)",
        "usage": envelope.get("usage", {}),
        "cost_usd": envelope.get("total_cost_usd"),
        "duration_ms": envelope.get("duration_ms"),
    }
    return parsed
