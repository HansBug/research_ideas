"""``known_format_lift`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.tools` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

import html
import re
from typing import Any

from ..inventory import (
    extract_generic_inventory_from_text,
    machine_elements_from_payload,
    merge_inventory,
    parse_json_payload,
)
from ..utils import count_machine_components, normalize_id


def dedupe_strings(items: list[str]) -> list[str]:
    """``dedupe_strings`` 函数。

    :param items: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = str(item).strip()
        key = normalize_id(clean)
        if not clean or not key or key in seen:
            continue
        seen.add(key)
        result.append(clean)
    return result


def guess_format(text: str | None) -> str:
    """``guess_format`` 函数。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not text or not text.strip():
        return "missing"
    stripped = text.strip()
    payload = parse_json_payload(stripped)
    if isinstance(payload, dict):
        if any(key in payload for key in ["states", "transitions", "blocks", "signals", "rules"]):
            return "json_structured_model"
        return "json_generic"
    if isinstance(payload, list):
        return "json_list"
    lowered = stripped.lower()
    if stripped.startswith("<?xml") or re.search(r"</?[A-Za-z][A-Za-z0-9:_-]*[^>]*>", stripped):
        if "turtlegmodeling" in lowered or "avatar" in lowered or "<modeling " in lowered:
            return "ttool_xml"
        return "xml"
    if "@startuml" in lowered or "state " in lowered or "[*]" in lowered:
        return "plantuml_like"
    if "statemachine" in lowered or "umple" in lowered or ("class " in lowered and "state" in lowered):
        return "umple_like"
    if stripped.startswith("---") or "score" in lowered or "average" in lowered or "std" in lowered:
        return "summary_text"
    return "free_text"


def format_confidence(format_guess: str, text: str | None) -> float:
    """``format_confidence`` 函数。

    :param format_guess: 见函数签名与上下文。
    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if format_guess == "missing":
        return 0.0
    if format_guess in {"json_structured_model", "plantuml_like", "ttool_xml"}:
        return 0.95
    if format_guess in {"json_generic", "xml", "umple_like"}:
        return 0.82
    if format_guess in {"json_list", "summary_text"}:
        return 0.74
    if len((text or "").strip()) >= 180:
        return 0.58
    return 0.42


def artifact_family_guess(inventory: dict[str, list[str]], text: str | None) -> str:
    """``artifact_family_guess`` 函数。

    :param inventory: 见函数签名与上下文。
    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    architecture_signal = len(inventory.get("blocks", [])) + len(inventory.get("signals", []))
    behavior_signal = len(inventory.get("states", [])) + len(inventory.get("transitions", []))
    if architecture_signal >= max(3, behavior_signal + 2):
        return "architecture_model"
    if inventory.get("states") or inventory.get("transitions"):
        return "behavior_model"
    if inventory.get("blocks") or inventory.get("signals"):
        return "architecture_model"
    lowered = (text or "").lower()
    if "state machine" in lowered or "statechart" in lowered or "behavior" in lowered:
        return "behavior_model"
    if "block" in lowered or "architecture" in lowered:
        return "architecture_model"
    return "unknown"


def parse_transition_signature(text: str) -> tuple[str, str, str, str, str]:
    """``parse_transition_signature`` 函数。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    raw = text.strip()
    if "|" in raw:
        parts = raw.split("|")
        if len(parts) >= 5:
            return (
                parts[0].strip(),
                parts[1].strip(),
                parts[2].strip(),
                parts[3].strip(),
                parts[4].strip(),
            )
    match = re.match(
        r"([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)\s*(?:->|-->|=>)\s*([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)(?:\s*:\s*(.+))?",
        raw,
    )
    if match:
        return (
            match.group(1).strip(),
            match.group(2).strip(),
            match.group(3).strip() if match.group(3) else "",
            "",
            "",
        )
    return ("", "", "", "", raw)


def _self_named_composite_count_from_text(text: str | None) -> int:
    """内部 helper：``_self_named_composite_count_from_text``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    raw = text or ""
    count = 0
    for match in re.finditer(r"state\s+([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)\s*\{", raw):
        name = match.group(1).strip()
        block_start = match.end()
        block_end = raw.find("}", block_start)
        if block_end == -1:
            continue
        block = raw[block_start:block_end]
        if re.search(rf"\[\*\]\s*(?:-->|->)\s*{re.escape(name)}\b", block):
            count += 1
    return count


def _cross_composite_transition_risk_from_text(text: str | None) -> int:
    """内部 helper：``_cross_composite_transition_risk_from_text``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    raw = text or ""
    composites = [
        match.group(1).strip()
        for match in re.finditer(r"state\s+([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)\s*\{", raw)
    ]
    if len(composites) < 2:
        return 0
    risk = 0
    for match in re.finditer(r"state\s+([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)\s*\{", raw):
        current = match.group(1).strip()
        block_start = match.end()
        block_end = raw.find("}", block_start)
        if block_end == -1:
            continue
        block = raw[block_start:block_end]
        for other in composites:
            if other == current:
                continue
            if re.search(rf"(?:->|-->)\s*{re.escape(other)}\b", block):
                risk += 1
    return risk


def surface_markers_from_text(text: str | None) -> dict[str, int]:
    """``surface_markers_from_text`` 函数。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    raw = text or ""
    lowered = raw.lower()
    return {
        "parallel": len(re.findall(r"^\s*--\s*$", raw, flags=re.M)),
        "choice": len(re.findall(r"\bchoice\b", lowered)),
        "fork": len(re.findall(r"\bfork\b", lowered)),
        "join": len(re.findall(r"\bjoin\b", lowered)),
        "junction": len(re.findall(r"\bjunction\b", lowered)),
        "xml_connector": len(re.findall(r"<CONNECTOR\b", raw, flags=re.I)),
        "xml_signal": len(re.findall(r"<Signal\b", raw, flags=re.I)),
        "self_named_composite": _self_named_composite_count_from_text(text),
        "cross_composite_transition": _cross_composite_transition_risk_from_text(text),
    }


def _extract_xml_inventory(text: str | None) -> tuple[dict[str, list[str]], list[str]]:
    """内部 helper：``_extract_xml_inventory``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    raw = text or ""
    inventory = {"states": [], "transitions": [], "blocks": [], "signals": [], "rules": []}
    notes: list[str] = []
    if not raw.strip():
        return inventory, notes

    for match in re.finditer(r'<Modeling[^>]*type="([^"]+)"[^>]*nameTab="([^"]+)"(?:[^>]*tabs="([^"]+)")?', raw, re.I):
        modeling_type = html.unescape(match.group(1)).strip()
        name_tab = html.unescape(match.group(2)).strip()
        tabs = html.unescape(match.group(3) or "").strip()
        if modeling_type:
            inventory["rules"].append(f"modeling_type:{modeling_type}")
        if name_tab:
            inventory["blocks"].append(name_tab)
        if tabs:
            inventory["blocks"].extend(item.strip() for item in tabs.split("$") if item.strip())

    for pattern in [
        r"<AVATARBlockDiagramPanel[^>]*name=\"([^\"]+)\"",
        r"<UseCaseDiagramPanel[^>]*name=\"([^\"]+)\"",
        r"<AVATARBlock[^>]*name=\"([^\"]+)\"",
        r"<Block[^>]*name=\"([^\"]+)\"",
    ]:
        for match in re.finditer(pattern, raw, re.I):
            inventory["blocks"].append(html.unescape(match.group(1)).strip())

    for match in re.finditer(r'<Validated[^>]*value="([^"]+)"', raw, re.I):
        inventory["blocks"].extend(item.strip() for item in html.unescape(match.group(1)).split(";") if item.strip())

    for match in re.finditer(r'<(?:Signal|AvatarSignal)[^>]*name="([^"]+)"', raw, re.I):
        inventory["signals"].append(html.unescape(match.group(1)).strip())

    for match in re.finditer(r'<infoparam[^>]*name="Block"[^>]*value="([^"]+)"', raw, re.I):
        inventory["blocks"].append(html.unescape(match.group(1)).strip())
    for match in re.finditer(r'<infoparam[^>]*name="state"[^>]*value="([^"]+)"', raw, re.I):
        inventory["states"].append(html.unescape(match.group(1)).strip())
    for match in re.finditer(r'<infoparam[^>]*name="connector"[^>]*value="([^"]+)"', raw, re.I):
        value = html.unescape(match.group(1)).strip()
        if value and value.lower() != "null":
            inventory["rules"].append(f"connector:{value}")

    for match in re.finditer(r'<(?:isd|oso)[^>]*value="([^"]+)"', raw, re.I):
        value = html.unescape(match.group(1)).strip()
        if value:
            inventory["signals"].append(value)
            inventory["rules"].append(f"connector_action:{value}")

    for connector in re.findall(r"<CONNECTOR\b.*?</CONNECTOR>", raw, flags=re.I | re.S):
        inbound = [html.unescape(item).strip() for item in re.findall(r'<isd[^>]*value="([^"]+)"', connector, re.I) if item.strip()]
        outbound = [html.unescape(item).strip() for item in re.findall(r'<oso[^>]*value="([^"]+)"', connector, re.I) if item.strip()]
        label = " / ".join(inbound + outbound).strip()
        if label:
            inventory["transitions"].append(f"Connector -> Connector : {label}")

    if inventory["blocks"] or inventory["signals"] or inventory["states"]:
        notes.append("Applied TTool/XML-specific probe to lift named blocks, signals, states, and connector hints.")
    return {key: dedupe_strings(value) for key, value in inventory.items()}, notes


def _derive_behavior_lines(text: str | None, inventory: dict[str, list[str]], format_guess: str) -> list[str]:
    """内部 helper：``_derive_behavior_lines``。

    :param text: 见函数签名与上下文。
    :param inventory: 见函数签名与上下文。
    :param format_guess: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if inventory.get("transitions"):
        return dedupe_strings(inventory["transitions"] + inventory.get("rules", []))[:20]
    if format_guess in {"ttool_xml", "xml"}:
        candidates = []
        for block in inventory.get("blocks", [])[:8]:
            candidates.append(f"Observed structural block or panel: {block}.")
        for signal in inventory.get("signals", [])[:8]:
            candidates.append(f"Observed signal or connector action: {signal}.")
        return dedupe_strings(candidates)[:20]
    lines = [line.strip(" -") for line in (text or "").splitlines() if len(line.strip(" -")) >= 18]
    return dedupe_strings(lines[:10])


def _derive_constraint_lines(text: str | None, inventory: dict[str, list[str]]) -> list[str]:
    """内部 helper：``_derive_constraint_lines``。

    :param text: 见函数签名与上下文。
    :param inventory: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    rules = list(inventory.get("rules", []))
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    for line in lines:
        lowered = line.lower()
        if line.lstrip().startswith("<") and line.rstrip().endswith(">"):
            continue
        if any(token in lowered for token in [" if ", " when ", " only ", " must ", " cannot ", " not ", "<", ">", "="]):
            rules.append(line)
    return dedupe_strings(rules)[:16]


def _derive_ambiguities(text: str | None, inventory: dict[str, list[str]]) -> list[str]:
    """内部 helper：``_derive_ambiguities``。

    :param text: 见函数签名与上下文。
    :param inventory: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    ambiguities = list(inventory.get("rules", []))
    for line in (text or "").splitlines():
        clean = line.strip()
        lowered = clean.lower()
        if len(clean) >= 12 and any(token in lowered for token in ["maybe", "possible", "approx", "etc", "and/or", "unknown", "?"]):
            ambiguities.append(clean)
    return dedupe_strings(ambiguities)[:10]


def _canonical_names_from_inventory(inventory: dict[str, list[str]]) -> list[str]:
    """内部 helper：``_canonical_names_from_inventory``。

    :param inventory: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    names: list[str] = []
    for key in ["states", "blocks", "signals"]:
        names.extend(item.split("|", 1)[0].strip() for item in inventory.get(key, []))
    for raw_relation in inventory.get("transitions", []):
        source, target, _trigger, _condition, _action = parse_transition_signature(raw_relation)
        if source:
            names.append(source)
        if target:
            names.append(target)
    return dedupe_strings(names)


def _explicit_state_names_from_text(text: str | None) -> list[str]:
    """内部 helper：``_explicit_state_names_from_text``。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    raw = text or ""
    names = [
        match.group(1).strip()
        for match in re.finditer(r"^\s*state\s+([\w\u3400-\u9FFF][\w\u3400-\u9FFF.-]*)\b", raw, re.M)
    ]
    return dedupe_strings(names)


def _observability_from_inventory(
    text: str | None,
    inventory: dict[str, list[str]],
    counts: dict[str, Any],
    format_guess: str,
) -> tuple[str, str]:
    """内部 helper：``_observability_from_inventory``。

    :param text: 见函数签名与上下文。
    :param inventory: 见函数签名与上下文。
    :param counts: 见函数签名与上下文。
    :param format_guess: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    item_count = sum(len(inventory.get(key, [])) for key in ["states", "transitions", "blocks", "signals", "rules"])
    text_len = len((text or "").strip())
    transition_count = int(counts.get("transition_count", 0) or 0)
    if (
        format_guess in {"ttool_xml", "xml"}
        and len(inventory.get("blocks", [])) >= 3
        and len(inventory.get("states", [])) < 2
        and len(inventory.get("transitions", [])) <= 1
    ):
        return "medium", "XML probe exposed named architecture entities, but behavior relations remain only partially observable."
    if item_count >= 8 or transition_count >= 4:
        return "high", "Multiple major elements and relations were directly observed."
    if format_guess in {"json_structured_model", "plantuml_like", "ttool_xml"} and item_count >= 4:
        return "high", f"Known format probe `{format_guess}` exposed enough named structure to support detailed review."
    if item_count >= 3 or text_len >= 180:
        return "medium", "Only part of the structure is directly visible, but there is enough evidence for conservative review."
    return "low", "Visible structure is sparse, so downstream conclusions must remain cautious."


def _structural_warnings_from_probe(
    format_guess: str,
    inventory: dict[str, list[str]],
    markers: dict[str, int],
) -> list[str]:
    """内部 helper：``_structural_warnings_from_probe``。

    :param format_guess: 见函数签名与上下文。
    :param inventory: 见函数签名与上下文。
    :param markers: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    warnings: list[str] = []
    if markers.get("self_named_composite", 0):
        warnings.append("Composite states appear to self-initialize inside their own body, which often indicates a structural modeling problem.")
    if markers.get("cross_composite_transition", 0):
        warnings.append("Cross-composite transitions were observed inside nested blocks, which can indicate scope leakage or malformed hierarchy.")
    if format_guess in {"ttool_xml", "xml"} and inventory.get("blocks") and not inventory.get("transitions"):
        warnings.append("Only architecture-side structure was directly observed from XML; behavior relations remain partially implicit.")
    if len(inventory.get("blocks", [])) >= 6 and not inventory.get("signals"):
        warnings.append("Many block-like observations were found but almost no explicit signal relations were recovered.")
    return dedupe_strings(warnings)


def summary_from_inventory(
    role: str,
    inventory: dict[str, list[str]],
    format_guess: str,
    observability: str,
    observability_reason: str,
) -> str:
    """``summary_from_inventory`` 函数。

    :param role: 见函数签名与上下文。
    :param inventory: 见函数签名与上下文。
    :param format_guess: 见函数签名与上下文。
    :param observability: 见函数签名与上下文。
    :param observability_reason: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    parts: list[str] = [f"{role} artifact detected as {format_guess}."]
    counts = {
        "states": len(inventory.get("states", [])),
        "transitions": len(inventory.get("transitions", [])),
        "blocks": len(inventory.get("blocks", [])),
        "signals": len(inventory.get("signals", [])),
        "rules": len(inventory.get("rules", [])),
    }
    count_bits = [f"{name}={value}" for name, value in counts.items() if value]
    if count_bits:
        parts.append("Observed " + ", ".join(count_bits) + ".")
    else:
        parts.append("Only sparse structure could be observed directly.")
    parts.append(f"Observability is {observability}: {observability_reason}")
    return " ".join(parts)


def inventory_from_text(text: str | None) -> dict[str, Any]:
    """``inventory_from_text`` 函数。

    :param text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    format_guess_value = guess_format(text)
    payload = parse_json_payload(text)
    parser_notes: list[str] = []
    inventory = {"states": [], "transitions": [], "blocks": [], "signals": [], "rules": []}
    counts: dict[str, Any] = {}

    if isinstance(payload, dict):
        inventory = merge_inventory(machine_elements_from_payload(payload), extract_generic_inventory_from_text(text or ""))
        counts = count_machine_components(payload)
        parser_notes.append("Applied JSON payload probe before generic text extraction.")
    elif format_guess_value in {"ttool_xml", "xml"}:
        xml_inventory, xml_notes = _extract_xml_inventory(text)
        inventory = merge_inventory(xml_inventory, extract_generic_inventory_from_text(text or ""))
        parser_notes.extend(xml_notes)
    else:
        inventory = extract_generic_inventory_from_text(text or "")

    if format_guess_value == "plantuml_like":
        explicit_states = _explicit_state_names_from_text(text)
        if explicit_states:
            inventory["states"] = dedupe_strings(explicit_states)
            parser_notes.append("Collapsed PlantUML state inventory to explicit state declarations for a less noisy major-element dossier.")

    surface_markers = surface_markers_from_text(text)
    behaviors = _derive_behavior_lines(text, inventory, format_guess_value)
    constraints = _derive_constraint_lines(text, inventory)
    ambiguities = _derive_ambiguities(text, inventory)
    observability, observability_reason = _observability_from_inventory(text, inventory, counts, format_guess_value)
    structural_warnings = _structural_warnings_from_probe(format_guess_value, inventory, surface_markers)
    canonical_names = _canonical_names_from_inventory(inventory)
    return {
        "inventory": inventory,
        "counts": counts,
        "format_guess": format_guess_value,
        "format_confidence": format_confidence(format_guess_value, text),
        "behaviors": behaviors,
        "constraints": constraints,
        "ambiguities": ambiguities,
        "observability": observability,
        "observability_reason": observability_reason,
        "surface_markers": surface_markers,
        "structural_warnings": structural_warnings,
        "canonical_names": canonical_names,
        "parser_notes": parser_notes,
    }


__all__ = [
    "artifact_family_guess",
    "dedupe_strings",
    "format_confidence",
    "guess_format",
    "inventory_from_text",
    "parse_transition_signature",
    "summary_from_inventory",
    "surface_markers_from_text",
]