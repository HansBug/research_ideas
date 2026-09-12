"""Codex CLI annotator.

Subprocesses ``codex exec --json --skip-git-repo-check -m <model>`` and
parses the streaming JSONL output for the final ``agent_message`` item.

Knobs come from environment variables ``CODEX_CMD`` / ``CODEX_MODEL``.
The CLI internally uses whatever provider is configured in
``~/.codex/config.toml`` (default profile). We do NOT pin the provider here
because routing is the user's deployment concern; we only pin the model
name.
"""
from __future__ import annotations

import json
import os
import subprocess
from typing import Any


def _strip_fence(text: str) -> str:
    s = text.strip()
    if not s.startswith("```"):
        return s
    first_nl = s.find("\n")
    if first_nl >= 0:
        s = s[first_nl + 1 :]
    if s.endswith("```"):
        s = s[:-3]
    return s.strip()


def _extract_final_message(jsonl_stdout: str) -> tuple[str, dict[str, Any]]:
    """Walk codex JSONL events, return (last agent_message text, usage)."""
    final_text = ""
    usage: dict[str, Any] = {}
    for line in jsonl_stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue
        if evt.get("type") == "item.completed":
            item = evt.get("item", {}) or {}
            if item.get("type") == "agent_message":
                final_text = item.get("text", "")
        elif evt.get("type") == "turn.completed":
            usage = evt.get("usage", {}) or {}
    return final_text, usage


def annotate(*, system_prompt: str, user_prompt: str, timeout_s: int = 300) -> dict[str, Any]:
    cmd_bin = os.environ.get("CODEX_CMD", "codex")
    model = os.environ.get("CODEX_MODEL", "gpt-5.5").strip() or "gpt-5.5"

    full_prompt = (
        f"<SYSTEM>\n{system_prompt}\n</SYSTEM>\n\n"
        f"{user_prompt}"
    )

    cmd = [
        cmd_bin, "exec",
        "--json",
        "--skip-git-repo-check",
        "-m", model,
    ]

    try:
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"codex CLI timed out after {timeout_s}s") from e
    if result.returncode != 0:
        raise RuntimeError(
            f"codex CLI exit={result.returncode}; stderr:\n{result.stderr[-800:]}"
        )

    final_text, usage = _extract_final_message(result.stdout)
    if not final_text:
        raise RuntimeError(
            f"codex produced no agent_message; stdout head:\n{result.stdout[:800]}"
        )

    cleaned = _strip_fence(final_text)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"codex agent_message is not parseable JSON; first 400 chars:\n{final_text[:400]}"
        ) from e

    parsed.setdefault("annotations", [])
    parsed.setdefault("summary", {})
    parsed["_meta"] = {
        "annotator": "codex",
        "model": model,
        "usage": usage,
    }
    return parsed
