from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_id(value: Any) -> str:
    text = normalize_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


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


def prf_from_counts(predicted_count: int, reference_count: int) -> dict[str, float | int]:
    tp = min(predicted_count, reference_count)
    fp = max(predicted_count - reference_count, 0)
    fn = max(reference_count - predicted_count, 0)
    precision = tp / predicted_count if predicted_count else 0.0
    recall = tp / reference_count if reference_count else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def macro_f1(metrics: Iterable[dict[str, float | int]]) -> float:
    values = [float(metric["f1"]) for metric in metrics]
    return sum(values) / len(values) if values else 0.0


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


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


def strip_code_fence(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", cleaned)
        cleaned = re.sub(r"\n```$", "", cleaned)
    return cleaned.strip()


def ensure_json(text: str) -> dict[str, Any]:
    return extract_json_object(strip_code_fence(text))


def flatten_nested_states(states: list[dict[str, Any]], parent: str | None = None) -> set[str]:
    results: set[str] = set()
    for state in states or []:
        name = normalize_id(state.get("name"))
        if not name:
            continue
        signature = f"{name}|{normalize_id(parent)}"
        results.add(signature)
        results |= flatten_nested_states(state.get("sub_states", []), state.get("name"))
    return results


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def count_tokens_like_lines(text: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for raw_line in text.splitlines():
        line = normalize_text(raw_line)
        if line:
            counter[line] += 1
    return counter
