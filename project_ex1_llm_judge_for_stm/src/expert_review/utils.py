from __future__ import annotations

import json
import math
import os
import re
import time
import threading
import unicodedata
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MODEL = "gpt-5.5"
# Quality / cost preference (per user 2026-05-07):
#   airouter     — cheapest + best quality (primary)
#   deepghs      — fast secondary fallback (JSON-mode confirmed)
#   findcg       — older fallback, sometimes slow
#   miaocg       — stable backup, more expensive, supports 50 concurrent
#   api68886868  — last resort (often returns malformed responses)
DEFAULT_PROVIDER_ORDER = ["airouter", "deepghs", "findcg", "miaocg", "api68886868"]

PROVIDER_CONFIGS = {
    "airouter": {
        "base_url": "https://airouter.service.itstudio.club/v1",
        "env_keys": ("AIROUTER_API_KEY",),
        "wire_api": "responses",  # codex 与 ours align：airouter gpt-5.5 是 reasoning 模型，走 /v1/responses
    },
    "deepghs": {
        "base_url": "https://new-api.deepghs.org/v1",
        "env_keys": ("DEEPGHS_API_KEY",),
        "wire_api": "responses",
    },
    "findcg": {
        "base_url": "https://www.findcg.com/v1",
        "env_keys": ("FINDCG_API_KEY",),
        "wire_api": "responses",
    },
    "miaocg": {
        "base_url": "https://api.miaocg.cn/v1",
        "env_keys": ("MIAOCG_API_KEY", "FINDCG_API_KEY"),
        "wire_api": "responses",
    },
    "api68886868": {
        "base_url": "https://api.68886868.xyz/v1",
        "env_keys": ("API68886868_API_KEY",),
        "wire_api": "chat_completions",  # 不支持 responses API
    },
}

# Per-provider cooldown after failure. Higher-quality providers (airouter)
# are periodically retried so we use them as soon as they recover.
PROVIDER_COOLDOWN_SECONDS = {
    "airouter": 180,    # retry every 3 min — top quality, want it back ASAP
    "deepghs": 180,
    "findcg": 180,
    "miaocg": 180,
    "api68886868": 180,
}
DEFAULT_COOLDOWN_SECONDS = 180

# Per-attempt timeout — balance fail-fast vs reasoning-model latency.
# 2026-05-08: airouter gpt-5.5 是 reasoning model，~25k tokens/call 时 latency
# 5-30s 正常。10s 太激进会误杀真实成功响应。bump 到 60s 让 reasoning 完成。
PROVIDER_FALLBACK_TIMEOUT = 60  # seconds per provider attempt


def resolve_api_env() -> dict[str, str]:
    resolved = dict(os.environ)
    env_files = [
        Path.home() / ".codex" / "findcg.env",
        Path.home() / ".codex" / "api68886868.env",
    ]
    for path in env_files:
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :]
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            resolved.setdefault(key.strip(), value.strip().strip("'").strip('"'))
    return resolved


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value)).replace("\r\n", "\n").replace("\r", "\n").strip()
    return re.sub(r"\s+", " ", text)


def normalize_id(value: Any) -> str:
    text = normalize_text(value).casefold()
    pieces: list[str] = []
    for char in text:
        pieces.append(char if char.isalnum() else " ")
    return re.sub(r"\s+", " ", "".join(pieces)).strip()


def is_cjk(char: str) -> bool:
    code = ord(char)
    return (
        0x3400 <= code <= 0x4DBF
        or 0x4E00 <= code <= 0x9FFF
        or 0xF900 <= code <= 0xFAFF
        or 0x3040 <= code <= 0x30FF
        or 0xAC00 <= code <= 0xD7AF
    )


def unicode_word_tokens(value: Any) -> list[str]:
    text = normalize_text(value).casefold()
    tokens: list[str] = []
    current: list[str] = []
    for char in text:
        if char.isalnum() or char == "_":
            current.append(char)
            continue
        if current:
            tokens.append("".join(current))
            current = []
    if current:
        tokens.append("".join(current))
    return tokens


def semantic_terms(value: Any) -> set[str]:
    text = normalize_text(value).casefold()
    terms: set[str] = set()
    for token in unicode_word_tokens(text):
        if any(is_cjk(char) for char in token):
            if token:
                terms.add(token)
            if len(token) >= 2:
                for size in (2, 3):
                    if len(token) < size:
                        continue
                    for idx in range(len(token) - size + 1):
                        terms.add(token[idx : idx + size])
            continue
        if len(token) >= 2:
            terms.add(token)
        if len(token) >= 4:
            terms.add(token[:4])
    contiguous_cjk: list[str] = []
    current_cjk: list[str] = []
    for char in text:
        if is_cjk(char):
            current_cjk.append(char)
            continue
        if current_cjk:
            contiguous_cjk.append("".join(current_cjk))
            current_cjk = []
    if current_cjk:
        contiguous_cjk.append("".join(current_cjk))
    for chunk in contiguous_cjk:
        terms.add(chunk)
        for size in (2, 3):
            if len(chunk) < size:
                continue
            for idx in range(len(chunk) - size + 1):
                terms.add(chunk[idx : idx + size])
    return {item for item in terms if item}


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    try:
        return float(value)
    except Exception:
        return None


def prf_from_sets(predicted: set[str], reference: set[str]) -> dict[str, float | int]:
    tp = len(predicted & reference)
    fp = len(predicted - reference)
    fn = len(reference - predicted)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def extract_json_object(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", text):
        try:
            candidate, _ = decoder.raw_decode(text[match.start() :])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict):
            return candidate
    raise ValueError("No JSON object found")


def ensure_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", cleaned)
        cleaned = re.sub(r"\n```$", "", cleaned)
    return extract_json_object(cleaned)


def normalize_machine(payload: dict[str, Any]) -> dict[str, Any]:
    result = {
        "machine_name": str(payload.get("machine_name", "")).strip(),
        "states": [],
        "transitions": [],
        "parallel_regions": [],
        "blocks": [],
    }
    for state in payload.get("states", []) or []:
        if not isinstance(state, dict):
            continue
        result["states"].append(
            {
                "name": str(state.get("name", "")).strip(),
                "parent": (str(state.get("parent")).strip() if state.get("parent") else None),
                "parallel_group": (
                    str(state.get("parallel_group")).strip() if state.get("parallel_group") else None
                ),
                "is_history": bool(state.get("is_history", False)),
                "is_initial": bool(state.get("is_initial", False)),
                "block": state.get("block"),
            }
        )
    for transition in payload.get("transitions", []) or []:
        if not isinstance(transition, dict):
            continue
        result["transitions"].append(
            {
                "source": str(transition.get("source", "")).strip(),
                "target": str(transition.get("target", "")).strip(),
                "event": str(transition.get("event", "")).strip(),
                "guard": str(transition.get("guard", "")).strip(),
                "action": str(transition.get("action", "")).strip(),
                "block": transition.get("block"),
            }
        )
    for block in payload.get("blocks", []) or []:
        if not isinstance(block, dict):
            continue
        block_name = str(block.get("name", "")).strip()
        normalized_block = {
            "name": block_name,
            "attributes": block.get("attributes", []) or [],
            "signals": block.get("signals", []) or [],
            "states": [],
            "transitions": [],
        }
        for state in block.get("states", []) or []:
            if isinstance(state, dict):
                normalized = {
                    "name": str(state.get("name", "")).strip(),
                    "parent": (str(state.get("parent")).strip() if state.get("parent") else None),
                    "parallel_group": (
                        str(state.get("parallel_group")).strip() if state.get("parallel_group") else None
                    ),
                    "is_history": bool(state.get("is_history", False)),
                    "is_initial": bool(state.get("is_initial", False)),
                    "block": block_name,
                }
                normalized_block["states"].append(normalized)
                result["states"].append(normalized)
        for transition in block.get("transitions", []) or []:
            if isinstance(transition, dict):
                normalized = {
                    "source": str(transition.get("source", "")).strip(),
                    "target": str(transition.get("target", "")).strip(),
                    "event": str(transition.get("event", "")).strip(),
                    "guard": str(transition.get("guard", "")).strip(),
                    "action": str(transition.get("action", "")).strip(),
                    "block": block_name,
                }
                normalized_block["transitions"].append(normalized)
                result["transitions"].append(normalized)
        result["blocks"].append(normalized_block)
    return result


def count_machine_components(payload: dict[str, Any]) -> dict[str, int]:
    machine = normalize_machine(payload)
    state_count = sum(1 for state in machine["states"] if state["name"])
    transition_count = sum(
        1 for transition in machine["transitions"] if transition["source"] and transition["target"]
    )
    guard_count = sum(1 for transition in machine["transitions"] if transition["guard"])
    action_count = sum(1 for transition in machine["transitions"] if transition["action"])
    hierarchical_state_count = sum(1 for state in machine["states"] if state["parent"])
    history_state_count = sum(1 for state in machine["states"] if state["is_history"])
    parallel_region_count = len(
        {
            (state["parent"], state["parallel_group"])
            for state in machine["states"]
            if state["parallel_group"]
        }
    )
    state_machine_panel_count = sum(
        1 for block in machine["blocks"] if block["states"] or block["transitions"]
    )
    return {
        "state_count": state_count,
        "transition_count": transition_count,
        "guard_count": guard_count,
        "action_count": action_count,
        "hierarchical_state_count": hierarchical_state_count,
        "history_state_count": history_state_count,
        "parallel_region_count": parallel_region_count,
        "state_machine_panel_count": state_machine_panel_count,
    }
