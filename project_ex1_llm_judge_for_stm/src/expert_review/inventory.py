"""``inventory`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

from langchain_core.tools import tool

from .utils import (
    count_machine_components,
    ensure_json,
    normalize_id,
    normalize_machine,
    normalize_text,
    prf_from_sets,
    semantic_terms,
)


@dataclass
class RequirementItem:
    """``RequirementItem`` 数据/逻辑类；详见所在模块顶部 docstring。"""
    requirement_id: str
    text: str


REQUIREMENT_LINE_PATTERN = re.compile(
    r"^((?:[A-Za-z]{1,8}\d+(?:[._-]\d+)*)|REQ[_-]?\d+|(?:需求|要求|规则|约束)\s*\d+|\d+)\s*[：:.)-]\s*(.+)$"
)
INLINE_REQUIREMENT_PATTERN = re.compile(
    r"((?:[A-Za-z]{1,8}\d+(?:[._-]\d+)*)|REQ[_-]?\d+|(?:需求|要求|规则|约束)\s*\d+|\d+)\s*[：:.)-]\s*"
)


def _split_free_text_requirements(text: str) -> list[str]:
    """内部 helper：``_split_free_text_requirements``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    paragraphs: list[str] = []
    current: list[str] = []
    for raw_line in text.splitlines():
        clean = raw_line.strip()
        if not clean:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if clean.startswith(("- ", "* ")):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            paragraphs.append(clean[2:].strip())
            continue
        current.append(clean)
    if current:
        paragraphs.append(" ".join(current))

    items: list[str] = []
    for paragraph in paragraphs:
        if not paragraph:
            continue
        sentence_parts = re.split(r"(?<=[.!?。！？])\s+|[;；]\s*|\s+-\s+", paragraph)
        kept = [part.strip(" -") for part in sentence_parts if len(part.strip(" -")) >= 12]
        if kept:
            items.extend(kept)
        else:
            items.append(paragraph.strip())
    return items


def _split_inline_explicit_requirements(text: str) -> list[RequirementItem]:
    """内部 helper：``_split_inline_explicit_requirements``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    matches = list(INLINE_REQUIREMENT_PATTERN.finditer(text))
    if len(matches) <= 1:
        return []
    items: list[RequirementItem] = []
    for idx, match in enumerate(matches):
        requirement_id = match.group(1)
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        requirement_text = text[start:end].strip(" -.;\n\t")
        if requirement_text:
            items.append(RequirementItem(requirement_id=requirement_id, text=requirement_text))
    return items


def parse_requirement_items(text: str | None, provided_items: list[dict[str, Any]]) -> list[RequirementItem]:
    """``parse_requirement_items`` 函数。

    :param text: 见函数签名与上下文。
    :param provided_items: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if provided_items:
        items: list[RequirementItem] = []
        for idx, item in enumerate(provided_items, start=1):
            requirement_id = str(item.get("requirement_id") or item.get("id") or f"req_{idx}")
            req_text = str(item.get("text") or item.get("requirement_text") or "").strip()
            if req_text:
                items.append(RequirementItem(requirement_id=requirement_id, text=req_text))
        if items:
            return items
    if not text:
        return []
    explicit_items: list[RequirementItem] = []
    explicit_match_count = 0
    for idx, line in enumerate(text.splitlines(), start=1):
        clean = line.strip()
        if not clean:
            continue
        inline_items = _split_inline_explicit_requirements(clean)
        if inline_items:
            explicit_match_count += len(inline_items)
            explicit_items.extend(inline_items)
            continue
        match = REQUIREMENT_LINE_PATTERN.match(clean)
        if match:
            explicit_match_count += 1
            explicit_items.append(RequirementItem(requirement_id=match.group(1), text=match.group(2).strip()))
        else:
            explicit_items.append(RequirementItem(requirement_id=f"req_{idx}", text=clean))
    if explicit_match_count > 0:
        return explicit_items

    return [
        RequirementItem(requirement_id=f"req_{idx}", text=item_text)
        for idx, item_text in enumerate(_split_free_text_requirements(text), start=1)
    ]


def parse_json_payload(value: str | None) -> dict[str, Any] | list[Any] | None:
    """``parse_json_payload`` 函数。

    :param value: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return json.loads(value)
    except Exception:
        pass
    try:
        return ensure_json(value)
    except Exception:
        return None


def extract_plain_elements(text: str) -> list[str]:
    """``extract_plain_elements`` 函数。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    elements: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "->" in line or "-->" in line:
            elements.append(line)
            continue
        if re.match(r"^[\w\u3400-\u9FFF][\w\u3400-\u9FFF.]*\s*\{$", line):
            elements.append(line.rstrip("{").strip())
            continue
        if re.match(r"^(state|transition|initial|final|block|component)\b", line, re.I):
            elements.append(line)
            continue
        if line.startswith(":") or line.startswith("[*]"):
            elements.append(line)
    return elements


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """内部 helper：``_dedupe_keep_order``。

    :param items: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = item.strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        result.append(clean)
    return result


def embedded_artifact_text(payload: dict[str, Any] | None) -> str:
    """``embedded_artifact_text`` 函数。

    :param payload: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not isinstance(payload, dict):
        return ""
    for key in (
        "generated_umple",
        "reference_solution_text",
        "plantuml_code",
        "reference_prompt_text",
        "raw_xml",
        "xml",
        "uml",
        "text",
    ):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_generic_inventory_from_text(text: str) -> dict[str, list[str]]:
    """``extract_generic_inventory_from_text`` 函数。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not text.strip():
        return {"states": [], "transitions": [], "blocks": [], "signals": [], "rules": []}

    states: list[str] = []
    transitions: list[str] = []
    blocks: list[str] = []
    signals: list[str] = []
    rules: list[str] = []

    for item in extract_plain_elements(text):
        if "->" in item or "-->" in item or "=>" in item:
            transitions.append(item)
        else:
            states.append(item)

    for match in re.finditer(r"\b(?:state|substate)\s+([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)", text, flags=re.I):
        states.append(match.group(1))
    for match in re.finditer(r"\b(?:block|component)\s+([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)", text, flags=re.I):
        blocks.append(match.group(1))
    for match in re.finditer(r'["\']name["\']\s*:\s*["\']([^"\']+)["\']', text):
        states.append(match.group(1))
    for match in re.finditer(r'["\'](?:source|from)["\']\s*:\s*["\']([^"\']+)["\']', text):
        states.append(match.group(1))
    for match in re.finditer(r'["\'](?:target|to)["\']\s*:\s*["\']([^"\']+)["\']', text):
        states.append(match.group(1))
    for match in re.finditer(r'["\']event["\']\s*:\s*["\']([^"\']+)["\']', text):
        signals.append(match.group(1))
    for match in re.finditer(r'["\']guard["\']\s*:\s*["\']([^"\']*)["\']', text):
        value = match.group(1).strip()
        if value:
            rules.append(value)
    for match in re.finditer(r"<infoparam[^>]*name=\"Block\"[^>]*value=\"([^\"]+)\"", text):
        blocks.append(match.group(1))
    for match in re.finditer(r"<infoparam[^>]*name=\"state\"[^>]*value=\"([^\"]+)\"", text):
        states.append(match.group(1))
    for match in re.finditer(r"<Signal[^>]*name=\"([^\"]+)\"", text):
        signals.append(match.group(1))
    for match in re.finditer(
        r"([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)\s*(?:->|-->|=>)\s*([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)",
        text,
    ):
        transitions.append(f"{match.group(1)}->{match.group(2)}")
        states.extend([match.group(1), match.group(2)])

    return {
        "states": _dedupe_keep_order(states),
        "transitions": _dedupe_keep_order(transitions),
        "blocks": _dedupe_keep_order(blocks),
        "signals": _dedupe_keep_order(signals),
        "rules": _dedupe_keep_order(rules),
    }


def merge_inventory(base: dict[str, list[str]], extra: dict[str, list[str]]) -> dict[str, list[str]]:
    """``merge_inventory`` 函数。

    :param base: 见函数签名与上下文。
    :param extra: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return {
        key: _dedupe_keep_order(list(base.get(key, [])) + list(extra.get(key, [])))
        for key in ["states", "transitions", "blocks", "signals", "rules"]
    }


def machine_elements_from_payload(payload: dict[str, Any] | None) -> dict[str, list[str]]:
    """``machine_elements_from_payload`` 函数。

    :param payload: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not isinstance(payload, dict):
        return {"states": [], "transitions": [], "blocks": [], "signals": [], "rules": []}
    machine = normalize_machine(payload)
    states = []
    transitions = []
    blocks = []
    signals = []
    rules = []
    for block in machine.get("blocks", []):
        if block.get("name"):
            blocks.append(str(block["name"]))
        for signal in block.get("signals", []) or []:
            name = str(signal.get("name", "")).strip()
            direction = str(signal.get("direction", "")).strip()
            if name:
                signals.append(f"{name}|{direction}|{block.get('name')}")
    for state in machine.get("states", []):
        name = str(state.get("name", "")).strip()
        if name:
            states.append(
                "|".join(
                    [
                        name,
                        str(state.get("parent") or "").strip(),
                        str(state.get("parallel_group") or "").strip(),
                        "H" if state.get("is_history") else "",
                    ]
                )
            )
    for transition in machine.get("transitions", []):
        source = str(transition.get("source", "")).strip()
        target = str(transition.get("target", "")).strip()
        event = str(transition.get("event", "")).strip()
        guard = str(transition.get("guard", "")).strip()
        action = str(transition.get("action", "")).strip()
        if source or target:
            transitions.append("|".join([source, target, event, guard, action]))
    for item in payload.get("states", []) or []:
        if isinstance(item, str):
            parts = item.split("|")
            name = parts[0].strip()
            parent = parts[1].strip() if len(parts) > 1 else ""
            if name:
                states.append("|".join([name, parent, "", ""]))
    for item in payload.get("rules", []) or []:
        if isinstance(item, str):
            text = item.strip()
            if text:
                rules.append(text)
                transitions.append(text)
        elif isinstance(item, dict):
            target = str(item.get("target_variable", "")).strip()
            assigned_value = str(item.get("assigned_value", "")).strip()
            condition = str(item.get("condition", "")).strip()
            text = "|".join([target, assigned_value, condition])
            if text.strip("|"):
                rules.append(text)
                transitions.append(text)
    for signal in payload.get("signals", []) or []:
        if isinstance(signal, dict):
            name = str(signal.get("name", "")).strip()
            direction = str(signal.get("direction", "")).strip()
            source_block = str(signal.get("source_block", "")).strip()
            target_block = str(signal.get("target_block", "")).strip()
            payload_fields = ",".join(str(item).strip() for item in signal.get("payload", []) or [])
            if name:
                signals.append("|".join([name, direction or source_block, target_block, payload_fields]))
    if not states and not transitions and not blocks and not signals:
        plain_items = extract_plain_elements(embedded_artifact_text(payload))
        for item in plain_items:
            if "->" in item or "-->" in item:
                transitions.append(item)
            else:
                states.append(item)
    return merge_inventory(
        {
        "states": states,
        "transitions": transitions,
        "blocks": blocks,
        "signals": signals,
        "rules": rules,
        },
        extract_generic_inventory_from_text(embedded_artifact_text(payload)),
    )


def extract_model_inventory(
    prediction_text: str | None,
    prediction_json: str | None,
    reference_text: str | None,
    reference_json: str | None,
) -> dict[str, Any]:
    """``extract_model_inventory`` 函数。

    :param prediction_text: 见函数签名与上下文。
    :param prediction_json: 见函数签名与上下文。
    :param reference_text: 见函数签名与上下文。
    :param reference_json: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    pred_payload = parse_json_payload(prediction_json) or parse_json_payload(prediction_text)
    ref_payload = parse_json_payload(reference_json) or parse_json_payload(reference_text)
    pred_text_material = "\n".join(item for item in [prediction_text or "", embedded_artifact_text(pred_payload)] if item)
    ref_text_material = "\n".join(item for item in [reference_text or "", embedded_artifact_text(ref_payload)] if item)
    pred_inventory = merge_inventory(
        machine_elements_from_payload(pred_payload),
        extract_generic_inventory_from_text(pred_text_material),
    )
    ref_inventory = merge_inventory(
        machine_elements_from_payload(ref_payload),
        extract_generic_inventory_from_text(ref_text_material),
    )
    pred_plain = extract_plain_elements(pred_text_material)
    ref_plain = extract_plain_elements(ref_text_material)
    return {
        "prediction_payload_detected": isinstance(pred_payload, dict),
        "reference_payload_detected": isinstance(ref_payload, dict),
        "prediction_inventory": pred_inventory,
        "reference_inventory": ref_inventory,
        "prediction_plain_elements": pred_plain,
        "reference_plain_elements": ref_plain,
        "prediction_counts": count_machine_components(pred_payload) if isinstance(pred_payload, dict) else {},
        "reference_counts": count_machine_components(ref_payload) if isinstance(ref_payload, dict) else {},
    }


def compute_set_match(predicted: list[str], reference: list[str]) -> dict[str, Any]:
    """``compute_set_match`` 函数。

    :param predicted: 见函数签名与上下文。
    :param reference: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    pred = {normalize_id(item) for item in predicted if normalize_id(item)}
    ref = {normalize_id(item) for item in reference if normalize_id(item)}
    metrics = prf_from_sets(pred, ref)
    return {
        "metrics": metrics,
        "missing": sorted(ref - pred),
        "extra": sorted(pred - ref),
        "matched": sorted(pred & ref),
    }


def build_requirement_trace(
    requirements: list[RequirementItem], prediction_elements: dict[str, list[str]]
) -> list[dict[str, Any]]:
    """``build_requirement_trace`` 函数。

    :param requirements: 见函数签名与上下文。
    :param prediction_elements: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    searchable = []
    for key, values in prediction_elements.items():
        for value in values:
            searchable.append((key, value, normalize_id(value)))
    results = []
    for item in requirements:
        tokens = [token for token in semantic_terms(item.text) if len(token) >= 2]
        matches = []
        for kind, raw_value, norm_value in searchable:
            candidate_terms = semantic_terms(raw_value) | semantic_terms(norm_value)
            overlap = [token for token in tokens if token in candidate_terms]
            if overlap:
                matches.append(
                    {
                        "kind": kind,
                        "element_text": raw_value,
                        "matched_tokens": overlap[:5],
                    }
                )
        status = "matched" if matches else "missing"
        if matches and len(matches) <= 1 and len(tokens) >= 4:
            status = "partial"
        results.append(
            {
                "requirement_id": item.requirement_id,
                "requirement_text": item.text,
                "status": status,
                "matches": matches[:8],
            }
        )
    return results


@tool
def parse_requirements_tool(input_text: str, provided_items_json: str = "[]") -> dict[str, Any]:
    """Parse requirement statements from free text or pre-structured items."""
    try:
        provided_items = json.loads(provided_items_json)
    except Exception:
        provided_items = []
    items = parse_requirement_items(input_text, provided_items)
    return {
        "requirement_count": len(items),
        "items": [{"requirement_id": item.requirement_id, "text": item.text} for item in items],
    }


@tool
def extract_model_inventory_tool(
    prediction_text: str = "",
    prediction_json: str = "",
    reference_text: str = "",
    reference_json: str = "",
) -> dict[str, Any]:
    """Extract structural inventories and counts from predicted and reference models."""
    return extract_model_inventory(prediction_text, prediction_json, reference_text, reference_json)


@tool
def compare_model_elements_tool(predicted_items_json: str, reference_items_json: str) -> dict[str, Any]:
    """Compare two element sets and return matched, missing, and extra items."""
    predicted = json.loads(predicted_items_json)
    reference = json.loads(reference_items_json)
    return compute_set_match(predicted, reference)


@tool
def build_traceability_tool(requirements_json: str, prediction_inventory_json: str) -> dict[str, Any]:
    """Build heuristic requirement-to-model trace candidates."""
    req_payload = json.loads(requirements_json)
    requirements = [
        RequirementItem(
            requirement_id=str(item["requirement_id"]),
            text=str(item["text"]),
        )
        for item in req_payload
    ]
    prediction_inventory = json.loads(prediction_inventory_json)
    traces = build_requirement_trace(requirements, prediction_inventory)
    return {"trace_results": traces}


def get_review_tools() -> list[Any]:
    """``get_review_tools`` 函数。
    :return: 见函数签名与上下文。
    """
    return [
        parse_requirements_tool,
        extract_model_inventory_tool,
        compare_model_elements_tool,
        build_traceability_tool,
    ]