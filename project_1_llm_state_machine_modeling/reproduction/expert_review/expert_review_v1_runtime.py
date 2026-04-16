from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass, field
from typing import Any

from langchain_openai import ChatOpenAI

from .expert_review_schema import (
    DimensionDefinition,
    DimensionReviewResult,
    ElementIssue,
    EvidenceItem,
    ExpertReviewRequest,
    ExpertReviewResult,
    RequirementTraceResult,
    TraceLink,
    judgement_from_score,
)
from .graph import (
    run_arbitration_node,
    run_equivalence_node,
    run_missing_evidence_node,
    run_quality_node,
    run_traceability_node,
)
from .expert_review_tools import (
    extract_generic_inventory_from_text,
    machine_elements_from_payload,
    merge_inventory,
    parse_json_payload,
    parse_requirement_items,
)
from .expert_review_utils import count_machine_components, ensure_json, normalize_id
from .tools import build_review_policy


INPUT_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "when",
    "where",
    "which",
    "while",
    "then",
    "will",
    "have",
    "has",
    "are",
    "must",
    "should",
    "than",
    "less",
    "more",
    "also",
    "other",
    "about",
    "according",
    "system",
    "information",
    "model",
    "diagram",
    "state",
    "machine",
    "behavior",
    "review",
    "expert",
}

GENERIC_NAME_TOKENS = {
    "idle",
    "start",
    "end",
    "state",
    "state1",
    "state2",
    "processing",
    "process",
    "waiting",
    "wait",
    "ready",
    "init",
    "initial",
    "final",
    "working",
    "running",
    "loop",
    "component",
    "block",
    "data",
    "message",
    "payload",
    "info",
    "node",
    "step",
    "task",
    "region",
    "mode",
}

CONTRACT_ROUTER_SYSTEM_PROMPT = """
You are the contract router inside a generic expert-review agent.

Your job is to parse a rich review prompt into a compact review contract.
Treat the prompt as a binding review contract that may contain task instructions,
rubric definitions, domain knowledge, equivalence principles, exclusions, and strictness cues.

Rules:
1. Do not invent task-specific knowledge that is not stated or strongly implied.
2. Preserve any explicit tolerance for equivalent-but-different designs.
3. Preserve any explicit strictness requirements or banned shortcuts.
4. Prefer concise structured extraction over verbose explanation.
5. Return strict JSON only.
""".strip()

ARTIFACT_EXTRACTOR_SYSTEM_PROMPT = """
You are the artifact extractor inside a generic expert-review agent.

You may receive unknown-format model outputs, reference artifacts, or other structured technical artifacts.
You must extract only what is justified by the text itself. You are not allowed to assume a fixed model type.

Rules:
1. If a known format is obvious, exploit it, but do not require it.
2. If the format is unknown, still extract major elements, relations, behaviors, and constraints conservatively.
3. Never hallucinate hidden states, transitions, blocks, messages, or rules.
4. Equivalent-but-different design patterns are allowed; just describe what is actually present.
5. Return strict JSON only.
""".strip()

TRACEABILITY_SYSTEM_PROMPT = """
You are the traceability agent inside a generic expert-review system.

Given requirements and a predicted artifact dossier, determine whether each requirement is matched,
partially supported, or missing. Match semantically, not only by exact wording.

Rules:
1. Give credit to equivalent decompositions or renamed structures when the behavior is clearly preserved.
2. Do not mark a requirement as matched if the evidence is only superficial naming overlap.
3. If evidence is ambiguous, use partial rather than matched.
4. Return strict JSON only.
""".strip()

EQUIVALENCE_SYSTEM_PROMPT = """
You are the equivalence and difference agent inside a generic expert-review system.

Compare the predicted artifact against the reference artifact and the requirement set.
The goal is not exact matching. The goal is to distinguish:
1. supported semantic equivalence despite different structure,
2. harmful unsupported additions,
3. likely omissions,
4. actual behavioral contradictions,
5. differences that remain uncertain due to insufficient evidence.

Rules:
1. Non-isomorphic but behaviorally compatible designs should receive credit.
2. Purely lexical matching is not enough for contradiction claims.
3. If a difference is plausible but under-evidenced, mark it uncertain rather than wrong.
4. Return strict JSON only.
""".strip()


@dataclass(slots=True)
class ReviewContract:
    task_summary: str
    requested_focus: list[str] = field(default_factory=list)
    domain_knowledge: list[str] = field(default_factory=list)
    equivalence_rules: list[str] = field(default_factory=list)
    evidence_rules: list[str] = field(default_factory=list)
    strictness: str = "balanced"
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceRegime:
    regime: str
    rationale: str
    pred_observability: str
    ref_observability: str
    has_reference: bool
    has_prediction: bool
    caution_rules: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ArtifactElement:
    element_id: str
    kind: str
    label: str
    text: str
    evidence_text: str


@dataclass(slots=True)
class ArtifactRelation:
    relation_id: str
    kind: str
    source_label: str
    target_label: str
    trigger: str
    condition: str
    action: str
    description: str
    evidence_text: str


@dataclass(slots=True)
class ArtifactDossier:
    role: str
    format_guess: str
    artifact_family_guess: str
    summary: str
    elements: list[ArtifactElement] = field(default_factory=list)
    relations: list[ArtifactRelation] = field(default_factory=list)
    behaviors: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    observability: str = "low"
    format_confidence: float = 0.0
    observability_reason: str = ""
    analysis_mode: str = "parser_only"
    surface_markers: dict[str, int] = field(default_factory=dict)
    structural_warnings: list[str] = field(default_factory=list)
    canonical_names: list[str] = field(default_factory=list)
    extraction_conflicts: list[str] = field(default_factory=list)
    parser_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InputDossier:
    summary: str
    requirements: list[RequirementTraceResult]
    behaviors: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    observability: str = "low"
    observability_reason: str = ""
    entity_hints: list[str] = field(default_factory=list)
    context_clues: list[str] = field(default_factory=list)


def _content_to_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                parts.append(text)
            else:
                parts.append(str(item))
        return "".join(parts)
    return "" if content is None else str(content)


def _invoke_llm_text(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    json_mode: bool = False,
) -> str:
    runnable = llm.bind(response_format={"type": "json_object"}) if json_mode else llm
    response = runnable.invoke(messages)
    text = _content_to_text(getattr(response, "content", response)).strip()
    if text:
        return text
    chunks: list[str] = []
    for chunk in runnable.stream(messages):
        part = _content_to_text(getattr(chunk, "content", chunk)).strip()
        if part:
            chunks.append(part)
    return "".join(chunks).strip()


def _invoke_llm_json(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
) -> dict[str, Any] | None:
    try:
        raw = _invoke_llm_text(llm, messages, json_mode=True)
        return ensure_json(raw)
    except Exception:
        try:
            raw = _invoke_llm_text(llm, messages, json_mode=False)
            repair = _invoke_llm_text(
                llm,
                [
                    ("system", "Convert the previous answer into strict JSON only."),
                    ("user", raw),
                ],
                json_mode=True,
            )
            return ensure_json(repair)
        except Exception:
            return None


def _artifact_excerpt(text: str | None, limit: int = 4200) -> str:
    if not text:
        return "[not provided]"
    cleaned = text.strip()
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[:limit]}\n...[truncated {len(cleaned) - limit} chars]"


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _tokenize(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    spaced = spaced.replace("_", " ").replace("-", " ")
    return [item.lower() for item in re.findall(r"[A-Za-z][A-Za-z0-9]*", spaced)]


def _content_tokens(value: str) -> list[str]:
    return [item for item in _tokenize(value) if len(item) >= 3 and item not in INPUT_STOPWORDS]


def _token_set(value: str) -> set[str]:
    return set(_content_tokens(value))


def _overlap_score(a: str, b: str) -> float:
    a_tokens = _token_set(a)
    b_tokens = _token_set(b)
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def _make_evidence_item(source: str, locator: str | None, snippet: str, explanation: str) -> EvidenceItem:
    return EvidenceItem(
        source=source,
        locator=locator,
        snippet=snippet.strip(),
        explanation=explanation.strip(),
    )


def _guess_format(text: str | None) -> str:
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


def _format_confidence(format_guess: str, text: str | None) -> float:
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


def _artifact_family_guess(inventory: dict[str, list[str]], text: str | None) -> str:
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


def _parse_transition_signature(text: str) -> tuple[str, str, str, str, str]:
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
        r"([A-Za-z_][A-Za-z0-9_.-]*)\s*(?:->|-->|=>)\s*([A-Za-z_][A-Za-z0-9_.-]*)(?:\s*:\s*(.+))?",
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


def _dedupe_strings(items: list[str]) -> list[str]:
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


def _self_named_composite_count_from_text(text: str | None) -> int:
    raw = text or ""
    count = 0
    for match in re.finditer(r"state\s+([A-Za-z_][A-Za-z0-9_.-]*)\s*\{", raw):
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
    raw = text or ""
    composites = [match.group(1).strip() for match in re.finditer(r"state\s+([A-Za-z_][A-Za-z0-9_.-]*)\s*\{", raw)]
    if len(composites) < 2:
        return 0
    risk = 0
    for match in re.finditer(r"state\s+([A-Za-z_][A-Za-z0-9_.-]*)\s*\{", raw):
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


def _surface_markers_from_text(text: str | None) -> dict[str, int]:
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
    return {key: _dedupe_strings(value) for key, value in inventory.items()}, notes


def _derive_behavior_lines(text: str | None, inventory: dict[str, list[str]], format_guess: str) -> list[str]:
    if inventory.get("transitions"):
        return _dedupe_strings(inventory["transitions"] + inventory.get("rules", []))[:20]
    if format_guess in {"ttool_xml", "xml"}:
        candidates = []
        for block in inventory.get("blocks", [])[:8]:
            candidates.append(f"Observed structural block or panel: {block}.")
        for signal in inventory.get("signals", [])[:8]:
            candidates.append(f"Observed signal or connector action: {signal}.")
        return _dedupe_strings(candidates)[:20]
    lines = [line.strip(" -") for line in (text or "").splitlines() if len(line.strip(" -")) >= 18]
    return _dedupe_strings(lines[:10])


def _derive_constraint_lines(text: str | None, inventory: dict[str, list[str]]) -> list[str]:
    rules = list(inventory.get("rules", []))
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    for line in lines:
        lowered = line.lower()
        if line.lstrip().startswith("<") and line.rstrip().endswith(">"):
            continue
        if any(token in lowered for token in [" if ", " when ", " only ", " must ", " cannot ", " not ", "<", ">", "="]):
            rules.append(line)
    return _dedupe_strings(rules)[:16]


def _derive_ambiguities(text: str | None, inventory: dict[str, list[str]]) -> list[str]:
    ambiguities = list(inventory.get("rules", []))
    for line in (text or "").splitlines():
        clean = line.strip()
        lowered = clean.lower()
        if len(clean) >= 12 and any(token in lowered for token in ["maybe", "possible", "approx", "etc", "and/or", "unknown", "?"]):
            ambiguities.append(clean)
    return _dedupe_strings(ambiguities)[:10]


def _canonical_names_from_inventory(inventory: dict[str, list[str]]) -> list[str]:
    names: list[str] = []
    for key in ["states", "blocks", "signals"]:
        names.extend(item.split("|", 1)[0].strip() for item in inventory.get(key, []))
    for raw_relation in inventory.get("transitions", []):
        source, target, _trigger, _condition, _action = _parse_transition_signature(raw_relation)
        if source:
            names.append(source)
        if target:
            names.append(target)
    return _dedupe_strings(names)


def _explicit_state_names_from_text(text: str | None) -> list[str]:
    raw = text or ""
    names = [match.group(1).strip() for match in re.finditer(r"^\s*state\s+([A-Za-z_][A-Za-z0-9_.-]*)\b", raw, re.M)]
    return _dedupe_strings(names)


def _observability_from_inventory(
    text: str | None,
    inventory: dict[str, list[str]],
    counts: dict[str, Any],
    format_guess: str,
) -> tuple[str, str]:
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
    warnings: list[str] = []
    if markers.get("self_named_composite", 0):
        warnings.append("Composite states appear to self-initialize inside their own body, which often indicates a structural modeling problem.")
    if markers.get("cross_composite_transition", 0):
        warnings.append("Cross-composite transitions were observed inside nested blocks, which can indicate scope leakage or malformed hierarchy.")
    if format_guess in {"ttool_xml", "xml"} and inventory.get("blocks") and not inventory.get("transitions"):
        warnings.append("Only architecture-side structure was directly observed from XML; behavior relations remain partially implicit.")
    if len(inventory.get("blocks", [])) >= 6 and not inventory.get("signals"):
        warnings.append("Many block-like observations were found but almost no explicit signal relations were recovered.")
    return _dedupe_strings(warnings)


def _summary_from_inventory(
    role: str,
    inventory: dict[str, list[str]],
    format_guess: str,
    observability: str,
    observability_reason: str,
) -> str:
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


def _inventory_from_text(text: str | None) -> dict[str, Any]:
    format_guess = _guess_format(text)
    payload = parse_json_payload(text)
    parser_notes: list[str] = []
    inventory = {"states": [], "transitions": [], "blocks": [], "signals": [], "rules": []}
    counts: dict[str, Any] = {}

    if isinstance(payload, dict):
        inventory = merge_inventory(machine_elements_from_payload(payload), extract_generic_inventory_from_text(text or ""))
        counts = count_machine_components(payload)
        parser_notes.append("Applied JSON payload probe before generic text extraction.")
    elif format_guess in {"ttool_xml", "xml"}:
        xml_inventory, xml_notes = _extract_xml_inventory(text)
        inventory = merge_inventory(xml_inventory, extract_generic_inventory_from_text(text or ""))
        parser_notes.extend(xml_notes)
    else:
        inventory = extract_generic_inventory_from_text(text or "")

    if format_guess == "plantuml_like":
        explicit_states = _explicit_state_names_from_text(text)
        if explicit_states:
            inventory["states"] = _dedupe_strings(explicit_states)
            parser_notes.append("Collapsed PlantUML state inventory to explicit state declarations for a less noisy major-element dossier.")

    surface_markers = _surface_markers_from_text(text)
    behaviors = _derive_behavior_lines(text, inventory, format_guess)
    constraints = _derive_constraint_lines(text, inventory)
    ambiguities = _derive_ambiguities(text, inventory)
    observability, observability_reason = _observability_from_inventory(text, inventory, counts, format_guess)
    structural_warnings = _structural_warnings_from_probe(format_guess, inventory, surface_markers)
    canonical_names = _canonical_names_from_inventory(inventory)
    return {
        "inventory": inventory,
        "counts": counts,
        "format_guess": format_guess,
        "format_confidence": _format_confidence(format_guess, text),
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


def _element_from_raw(kind: str, raw_value: str, idx: int, role: str) -> ArtifactElement:
    label = raw_value.split("|", 1)[0].strip()
    cleaned = raw_value.strip()
    if kind == "state":
        state_match = re.match(r"state\s+([A-Za-z_][A-Za-z0-9_.-]*)", cleaned)
        if state_match:
            label = state_match.group(1).strip()
    elif kind in {"block", "component"}:
        block_match = re.match(r"(?:block|component)\s+([A-Za-z_][A-Za-z0-9_.-]*)", cleaned, re.I)
        if block_match:
            label = block_match.group(1).strip()
    element_id = f"{role}_{kind}_{idx}"
    return ArtifactElement(
        element_id=element_id,
        kind=kind,
        label=label or cleaned,
        text=cleaned,
        evidence_text=cleaned,
    )


def _relation_from_raw(raw_value: str, idx: int, role: str) -> ArtifactRelation:
    source, target, trigger, condition, action = _parse_transition_signature(raw_value)
    description = raw_value.strip()
    if source or target:
        description = f"{source} -> {target}".strip()
        if trigger:
            description += f" on {trigger}"
        if condition:
            description += f" if {condition}"
        if action:
            description += f" do {action}"
    return ArtifactRelation(
        relation_id=f"{role}_relation_{idx}",
        kind="relation",
        source_label=source,
        target_label=target,
        trigger=trigger,
        condition=condition,
        action=action,
        description=description,
        evidence_text=raw_value.strip(),
    )


def _element_merge_key(element: ArtifactElement) -> str:
    return normalize_id("|".join([element.kind, element.label or element.text]))


def _relation_merge_key(relation: ArtifactRelation) -> str:
    base = "|".join(
        [
            relation.source_label,
            relation.target_label,
            relation.trigger,
            relation.condition,
            relation.action,
        ]
    )
    if normalize_id(base):
        return normalize_id(base)
    return normalize_id(relation.description or relation.evidence_text)


def _same_relation_family(left: ArtifactRelation, right: ArtifactRelation) -> bool:
    left_pair = normalize_id("|".join([left.source_label, left.target_label]))
    right_pair = normalize_id("|".join([right.source_label, right.target_label]))
    if left_pair and right_pair and left_pair != right_pair:
        return False
    if left_pair != right_pair and (left_pair or right_pair):
        return False
    if left.trigger and right.trigger and normalize_id(left.trigger) != normalize_id(right.trigger):
        return False
    if left_pair and right_pair:
        return True
    return normalize_id(left.description or left.evidence_text) == normalize_id(right.description or right.evidence_text)


def _render_artifact_schema_hint() -> dict[str, Any]:
    return {
        "artifact_family_guess": "behavior_model",
        "summary": "Short evidence-grounded summary.",
        "major_elements": [
            {
                "element_id": "e1",
                "kind": "state",
                "label": "Idle",
                "text": "Idle state",
                "evidence_text": "short supporting snippet",
            }
        ],
        "major_relations": [
            {
                "relation_id": "r1",
                "kind": "relation",
                "source_label": "Idle",
                "target_label": "Ready",
                "trigger": "login",
                "condition": "authorized",
                "action": "",
                "description": "Idle to Ready when login and authorized.",
                "evidence_text": "short supporting snippet",
            }
        ],
        "behaviors": ["A short behavior statement."],
        "constraints": ["A short constraint statement."],
        "ambiguities": ["A short ambiguity statement if needed."],
        "observability": "high",
        "observability_reason": "Short reason for the observability judgement.",
    }


def _build_parser_dossier(role: str, text: str | None) -> ArtifactDossier:
    probe = _inventory_from_text(text)
    inventory = probe["inventory"]
    elements: list[ArtifactElement] = []
    relations: list[ArtifactRelation] = []
    element_index: dict[str, int] = {}
    relation_index: dict[str, int] = {}
    for kind in ["states", "blocks", "signals", "rules"]:
        singular = kind[:-1] if kind.endswith("s") else kind
        for idx, raw_value in enumerate(inventory.get(kind, []), start=1):
            candidate = _element_from_raw(singular, raw_value, idx, role)
            key = _element_merge_key(candidate)
            if key in element_index:
                existing = elements[element_index[key]]
                existing.text = _merge_text_fragments(existing.text, candidate.text)
                existing.evidence_text = _merge_text_fragments(existing.evidence_text, candidate.evidence_text)
                continue
            element_index[key] = len(elements)
            elements.append(candidate)
    for idx, raw_value in enumerate(inventory.get("transitions", []), start=1):
        if "[*]" in raw_value:
            continue
        candidate = _relation_from_raw(raw_value, idx, role)
        key = _relation_merge_key(candidate)
        if key in relation_index:
            existing = relations[relation_index[key]]
            existing.description = _merge_text_fragments(existing.description, candidate.description)
            existing.evidence_text = _merge_text_fragments(existing.evidence_text, candidate.evidence_text)
            continue
        merged = False
        for existing_idx, existing in enumerate(relations):
            if _same_relation_family(existing, candidate) and (not existing.trigger or not candidate.trigger):
                if candidate.trigger and not existing.trigger:
                    existing.trigger = candidate.trigger
                if candidate.condition and not existing.condition:
                    existing.condition = candidate.condition
                if candidate.action and not existing.action:
                    existing.action = candidate.action
                existing.description = _merge_text_fragments(existing.description, candidate.description)
                existing.evidence_text = _merge_text_fragments(existing.evidence_text, candidate.evidence_text)
                relation_index[_relation_merge_key(existing)] = existing_idx
                merged = True
                break
        if merged:
            continue
        relation_index[key] = len(relations)
        relations.append(candidate)
    evidence: list[EvidenceItem] = []
    for idx, raw_value in enumerate(inventory.get("transitions", [])[:3], start=1):
        evidence.append(
            _make_evidence_item(
                role,
                f"{role}:relation:{idx}",
                raw_value,
                f"Observed {role} relation from direct parser/probe extraction.",
            )
        )
    for idx, raw_value in enumerate((inventory.get("states", []) + inventory.get("blocks", []) + inventory.get("signals", []))[:3], start=1):
        evidence.append(
            _make_evidence_item(
                role,
                f"{role}:element:{idx}",
                raw_value,
                f"Observed {role} element from direct parser/probe extraction.",
            )
        )
    return ArtifactDossier(
        role=role,
        format_guess=probe["format_guess"],
        artifact_family_guess=_artifact_family_guess(inventory, text),
        summary=_summary_from_inventory(
            role,
            inventory,
            probe["format_guess"],
            probe["observability"],
            probe["observability_reason"],
        ),
        elements=elements,
        relations=relations,
        behaviors=probe["behaviors"][:16],
        constraints=probe["constraints"][:12],
        ambiguities=probe["ambiguities"][:10],
        evidence=evidence[:6],
        observability=probe["observability"],
        format_confidence=float(probe["format_confidence"]),
        observability_reason=probe["observability_reason"],
        analysis_mode="parser_only",
        surface_markers=dict(probe["surface_markers"]),
        structural_warnings=list(probe["structural_warnings"]),
        canonical_names=list(probe["canonical_names"]),
        extraction_conflicts=[],
        parser_notes=list(probe["parser_notes"]),
    )


def _should_use_llm_extractor(dossier: ArtifactDossier, text: str | None) -> bool:
    if not text or not text.strip():
        return False
    if dossier.format_guess in {"json_structured_model", "plantuml_like"} and dossier.observability == "high":
        return False
    if dossier.observability == "low":
        return True
    if dossier.format_guess in {"ttool_xml", "xml", "free_text", "summary_text", "json_generic", "json_list"}:
        return True
    return len(dossier.behaviors) < 2 and len((text or "").strip()) >= 200


def _merge_text_fragments(first: str, second: str) -> str:
    left = first.strip()
    right = second.strip()
    if not left:
        return right
    if not right or normalize_id(left) == normalize_id(right):
        return left
    if normalize_id(right) in normalize_id(left):
        return left
    if normalize_id(left) in normalize_id(right):
        return right
    return f"{left} | {right}"


def _merge_artifact_dossiers(parser_dossier: ArtifactDossier, llm_payload: dict[str, Any]) -> ArtifactDossier:
    elements = list(parser_dossier.elements)
    relations = list(parser_dossier.relations)
    element_index = {_element_merge_key(item): idx for idx, item in enumerate(elements)}
    relation_index = {_relation_merge_key(item): idx for idx, item in enumerate(relations)}
    extraction_conflicts = list(parser_dossier.extraction_conflicts)
    for idx, item in enumerate(llm_payload.get("major_elements", []), start=1):
        if not isinstance(item, dict):
            continue
        label = str(item.get("label", "")).strip()
        text = str(item.get("text") or label).strip()
        if not label and not text:
            continue
        candidate = ArtifactElement(
            element_id=str(item.get("element_id") or f"{parser_dossier.role}_llm_element_{idx}"),
            kind=str(item.get("kind") or "element"),
            label=label or text,
            text=text,
            evidence_text=str(item.get("evidence_text") or text),
        )
        key = _element_merge_key(candidate)
        if key and key in element_index:
            existing = elements[element_index[key]]
            if candidate.kind != existing.kind:
                extraction_conflicts.append(
                    f"LLM retyped `{candidate.label or candidate.text}` from `{existing.kind}` to `{candidate.kind}`; kept parser kind."
                )
            existing.text = _merge_text_fragments(existing.text, candidate.text)
            existing.evidence_text = _merge_text_fragments(existing.evidence_text, candidate.evidence_text)
            continue
        element_index[key] = len(elements)
        elements.append(candidate)
    for idx, item in enumerate(llm_payload.get("major_relations", []), start=1):
        if not isinstance(item, dict):
            continue
        description = str(item.get("description", "")).strip()
        source = str(item.get("source_label", "")).strip()
        target = str(item.get("target_label", "")).strip()
        candidate = ArtifactRelation(
            relation_id=str(item.get("relation_id") or f"{parser_dossier.role}_llm_relation_{idx}"),
            kind=str(item.get("kind") or "relation"),
            source_label=source,
            target_label=target,
            trigger=str(item.get("trigger", "")).strip(),
            condition=str(item.get("condition", "")).strip(),
            action=str(item.get("action", "")).strip(),
            description=description or str(item.get("evidence_text", "")).strip(),
            evidence_text=str(item.get("evidence_text") or description),
        )
        key = _relation_merge_key(candidate)
        if key and key in relation_index:
            existing = relations[relation_index[key]]
            existing.description = _merge_text_fragments(existing.description, candidate.description)
            existing.evidence_text = _merge_text_fragments(existing.evidence_text, candidate.evidence_text)
            if candidate.condition and not existing.condition:
                existing.condition = candidate.condition
            if candidate.action and not existing.action:
                existing.action = candidate.action
            continue
        relation_index[key] = len(relations)
        relations.append(candidate)
    behaviors = _dedupe_strings(parser_dossier.behaviors + [str(item) for item in llm_payload.get("behaviors", [])])
    constraints = _dedupe_strings(
        parser_dossier.constraints + [str(item) for item in llm_payload.get("constraints", [])]
    )
    ambiguities = _dedupe_strings(
        parser_dossier.ambiguities + [str(item) for item in llm_payload.get("ambiguities", [])]
    )
    evidence = list(parser_dossier.evidence)
    for idx, item in enumerate(llm_payload.get("major_elements", [])[:2], start=1):
        if not isinstance(item, dict):
            continue
        evidence.append(
            _make_evidence_item(
                parser_dossier.role,
                f"{parser_dossier.role}:llm_element:{idx}",
                snippet=str(item.get("evidence_text") or item.get("text") or item.get("label") or ""),
                explanation=f"LLM-extracted {parser_dossier.role} element summary.",
            )
        )
    for idx, item in enumerate(llm_payload.get("major_relations", [])[:2], start=1):
        if not isinstance(item, dict):
            continue
        evidence.append(
            _make_evidence_item(
                parser_dossier.role,
                f"{parser_dossier.role}:llm_relation:{idx}",
                snippet=str(item.get("evidence_text") or item.get("description") or ""),
                explanation=f"LLM-extracted {parser_dossier.role} relation summary.",
            )
        )
    summary = str(llm_payload.get("summary") or parser_dossier.summary).strip()
    artifact_family_guess = str(llm_payload.get("artifact_family_guess") or parser_dossier.artifact_family_guess)
    observability = str(llm_payload.get("observability") or parser_dossier.observability)
    observability_reason = str(llm_payload.get("observability_reason") or parser_dossier.observability_reason).strip()
    canonical_names = _dedupe_strings(
        parser_dossier.canonical_names
        + [item.label for item in elements if item.label]
        + [relation.source_label for relation in relations if relation.source_label]
        + [relation.target_label for relation in relations if relation.target_label]
    )
    return ArtifactDossier(
        role=parser_dossier.role,
        format_guess=parser_dossier.format_guess,
        artifact_family_guess=artifact_family_guess,
        summary=summary,
        elements=elements[:40],
        relations=relations[:40],
        behaviors=behaviors[:20],
        constraints=constraints[:16],
        ambiguities=ambiguities[:10],
        evidence=evidence[:8],
        observability=observability,
        format_confidence=parser_dossier.format_confidence,
        observability_reason=observability_reason,
        analysis_mode="parser_plus_llm",
        surface_markers=dict(parser_dossier.surface_markers),
        structural_warnings=_dedupe_strings(parser_dossier.structural_warnings),
        canonical_names=canonical_names[:40],
        extraction_conflicts=_dedupe_strings(extraction_conflicts)[:12],
        parser_notes=list(parser_dossier.parser_notes),
    )


def _extract_artifact_dossier(
    role: str,
    text: str | None,
    llm: ChatOpenAI | None,
    notes: list[str],
) -> ArtifactDossier:
    parser_dossier = _build_parser_dossier(role, text)
    if llm is None or not _should_use_llm_extractor(parser_dossier, text):
        return parser_dossier
    llm_payload = _invoke_llm_json(
        llm,
        [
            ("system", ARTIFACT_EXTRACTOR_SYSTEM_PROMPT),
            (
                "user",
                "Normalize the following artifact into the schema below.\n\n"
                f"Schema:\n{json.dumps(_render_artifact_schema_hint(), ensure_ascii=False, indent=2)}\n\n"
                f"Artifact role: {role}\n"
                f"Observed format guess: {parser_dossier.format_guess}\n"
                f"Observed parser summary: {parser_dossier.summary}\n"
                f"Artifact text:\n{_artifact_excerpt(text)}",
            ),
        ],
    )
    if not isinstance(llm_payload, dict):
        notes.append(f"{role} extractor fell back to parser-only dossier because the LLM extractor returned no JSON.")
        return parser_dossier
    notes.append(f"{role} dossier used parser + LLM extraction.")
    return _merge_artifact_dossiers(parser_dossier, llm_payload)


def _default_contract(prompt: str) -> ReviewContract:
    lowered = prompt.lower()
    focus: list[str] = []
    for item in [
        "coverage",
        "completeness",
        "behavior",
        "consistency",
        "traceability",
        "clarity",
        "syntax",
        "quality",
        "hallucination",
        "equivalence",
    ]:
        if item in lowered:
            focus.append(item)
    equivalence_rules = [
        "Equivalent but differently structured designs should receive credit when observable behavior is preserved.",
        "Pure surface mismatch is not enough to declare failure.",
    ]
    evidence_rules = [
        "Do not overclaim unsupported errors when evidence is sparse.",
        "Tie every strong judgement to visible evidence from input, prediction, or reference.",
    ]
    strictness = "strict" if any(item in lowered for item in ["strict", "rigorous", "严格"]) else "balanced"
    return ReviewContract(
        task_summary=prompt.strip() or "Review the predicted artifact against the available evidence.",
        requested_focus=focus,
        domain_knowledge=[],
        equivalence_rules=equivalence_rules,
        evidence_rules=evidence_rules,
        strictness=strictness,
        notes=[],
    )


def _route_contract(prompt: str, llm: ChatOpenAI | None, notes: list[str]) -> ReviewContract:
    fallback = _default_contract(prompt)
    if llm is None:
        return fallback
    payload = _invoke_llm_json(
        llm,
        [
            ("system", CONTRACT_ROUTER_SYSTEM_PROMPT),
            (
                "user",
                "Extract a review contract from the prompt.\n\n"
                "Return JSON with keys: task_summary, requested_focus, domain_knowledge, "
                "equivalence_rules, evidence_rules, strictness, notes.\n\n"
                f"Prompt:\n{prompt}",
            ),
        ],
    )
    if not isinstance(payload, dict):
        notes.append("Contract router fell back to deterministic prompt parsing.")
        return fallback
    return ReviewContract(
        task_summary=str(payload.get("task_summary") or fallback.task_summary).strip(),
        requested_focus=[str(item).strip() for item in payload.get("requested_focus", []) if str(item).strip()],
        domain_knowledge=[str(item).strip() for item in payload.get("domain_knowledge", []) if str(item).strip()],
        equivalence_rules=[
            str(item).strip()
            for item in payload.get("equivalence_rules", fallback.equivalence_rules)
            if str(item).strip()
        ],
        evidence_rules=[
            str(item).strip() for item in payload.get("evidence_rules", fallback.evidence_rules) if str(item).strip()
        ],
        strictness=str(payload.get("strictness") or fallback.strictness).strip() or "balanced",
        notes=[str(item).strip() for item in payload.get("notes", []) if str(item).strip()],
    )


def _estimate_evidence_regime(
    request: ExpertReviewRequest,
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
) -> EvidenceRegime:
    has_prediction = bool((request.pred_output or "").strip())
    has_reference = bool((request.ref_output or "").strip())
    prompt_text = " ".join(
        part.strip().lower() for part in [request.prompt, request.input_text, request.pred_output or "", request.ref_output or ""] if part
    )
    if not has_prediction and not has_reference:
        return EvidenceRegime(
            regime="protocol_only",
            rationale="No concrete prediction or reference artifact was provided.",
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=False,
            has_prediction=False,
            caution_rules=[
                "Do not fabricate element-level findings without visible artifacts.",
                "Focus on process understanding and evidence limits rather than exact scoring.",
            ],
        )
    if ("manual inspection" in prompt_text or "formal verification" in prompt_text or "simulation" in prompt_text) and (
        pred_dossier.observability == "low" or (has_reference and ref_dossier.observability == "low")
    ):
        return EvidenceRegime(
            regime="protocol_only",
            rationale="The inputs emphasize evaluation protocol while concrete artifact evidence is sparse.",
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=has_reference,
            has_prediction=has_prediction,
            caution_rules=[
                "Keep scores coarse and confidence capped.",
                "Do not claim exact structural defects without direct evidence.",
            ],
        )
    if has_prediction and has_reference and pred_dossier.observability != "low" and ref_dossier.observability != "low":
        return EvidenceRegime(
            regime="record_level",
            rationale="Prediction and reference artifacts are both directly observable.",
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=True,
            has_prediction=True,
            caution_rules=[
                "Use strong alignment where evidence is explicit, but still allow equivalent structure variation.",
            ],
        )
    if has_prediction and not has_reference:
        regime = "summary_only" if (
            pred_dossier.format_guess == "summary_text" or "summary-level" in request.prompt.lower()
        ) else "mixed_evidence"
        rationale = (
            "Only predicted artifact evidence is available, so review must rely on requirements and direct artifact reading."
        )
        if regime == "summary_only":
            rationale = "Prediction evidence looks like summary-level reporting rather than a full artifact."
        return EvidenceRegime(
            regime=regime,
            rationale=rationale,
            pred_observability=pred_dossier.observability,
            ref_observability=ref_dossier.observability,
            has_reference=False,
            has_prediction=True,
            caution_rules=[
                "Avoid exact-match penalties that require a missing reference artifact.",
            ],
        )
    return EvidenceRegime(
        regime="mixed_evidence",
        rationale="Some artifact evidence is visible, but not enough for fully strict record-level matching.",
        pred_observability=pred_dossier.observability,
        ref_observability=ref_dossier.observability,
        has_reference=has_reference,
        has_prediction=has_prediction,
        caution_rules=[
            "Treat low-observability differences as uncertain rather than definitively wrong.",
        ],
    )


def _clone_dimension(
    name: str,
    title: str,
    description: str,
    weight: float = 1.0,
    scoring_notes: list[str] | None = None,
) -> DimensionDefinition:
    return DimensionDefinition(
        name=name,
        title=title,
        description=description,
        weight=weight,
        scoring_mode="continuous_0_1",
        positive_examples=[],
        negative_examples=[],
        scoring_notes=list(scoring_notes or []),
    )


def _build_dimensions(contract: ReviewContract, regime: EvidenceRegime) -> list[DimensionDefinition]:
    focus = {normalize_id(item) for item in contract.requested_focus}
    dimensions = [
        _clone_dimension(
            "notation_syntax",
            "Notation and Syntax",
            "Whether the artifact is structurally well-formed enough to support technical review.",
            weight=1.0,
        ),
        _clone_dimension(
            "semantic_completeness",
            "Semantic Completeness",
            "Whether important requirement-driven elements and behaviors are present.",
            weight=1.25 if "coverage" in focus or "completeness" in focus else 1.0,
        ),
        _clone_dimension(
            "behavioral_consistency",
            "Behavioral Consistency",
            "Whether the predicted artifact preserves intended behavior and avoids contradictions.",
            weight=1.25 if "behavior" in focus or "consistency" in focus or "equivalence" in focus else 1.0,
        ),
        _clone_dimension(
            "requirement_traceability",
            "Requirement Traceability",
            "Whether key requirements can be mapped to the artifact and unsupported extras are controlled.",
            weight=1.15 if "traceability" in focus or "hallucination" in focus else 1.0,
        ),
        _clone_dimension(
            "pragmatic_clarity",
            "Pragmatic Clarity",
            "Whether the artifact is readable, disciplined, and not gratuitously inflated.",
            weight=1.10 if "clarity" in focus or "quality" in focus else 1.0,
        ),
        _clone_dimension(
            "evidence_discipline",
            "Evidence Discipline",
            "Whether the review stays within the available evidence regime and avoids overclaiming.",
            weight=1.20 if regime.regime != "record_level" else 1.0,
        ),
    ]
    return dimensions


def _build_input_dossier(request: ExpertReviewRequest) -> InputDossier:
    raw_requirements = parse_requirement_items(request.input_text, [])
    requirements = []
    for item in raw_requirements:
        requirements.append(
            RequirementTraceResult(
                requirement_id=item.requirement_id,
                requirement_text=item.text,
                status="unreviewed",
                reason_text="Requirement extracted from input text and awaiting traceability analysis.",
                matched_element_ids=[],
                confidence=0.5,
            )
        )
    requirement_texts = [item.requirement_text for item in requirements]
    clues: list[str] = []
    lowered = request.prompt.lower()
    if "equivalent" in lowered or "等效" in request.prompt:
        clues.append("Prompt explicitly allows semantic equivalence beyond structural isomorphism.")
    if "hallucination" in lowered or "额外" in request.prompt:
        clues.append("Prompt explicitly asks to inspect unsupported extra structure.")
    behaviors = _dedupe_strings(requirement_texts)
    constraints = _dedupe_strings(
        [
            text
            for text in requirement_texts
            if any(
                token in text.lower()
                for token in [" if ", " when ", " only ", " must ", " cannot ", " not ", "<", ">", "within", "every"]
            )
        ]
    )
    ambiguities = _dedupe_strings(
        [
            text
            for text in requirement_texts
            if any(token in text.lower() for token in ["possible", "may ", "maybe", "roughly", "and/or", "etc"])
        ]
    )
    evidence = [
        _make_evidence_item(
            "input",
            f"input:requirement:{item.requirement_id}",
            item.requirement_text,
            "Requirement extracted into the input dossier.",
        )
        for item in requirements[:4]
    ]
    entity_hints = _dedupe_strings(
        [
            token
            for text in requirement_texts
            for token in _content_tokens(text)
            if token not in {"shall", "should", "must", "allow", "system"}
        ]
    )[:20]
    if len(requirements) >= 4 or len(request.input_text.strip()) >= 220:
        observability = "high"
        observability_reason = "Input dossier contains multiple explicit requirements and enough textual detail for grounding."
    elif requirements or len(request.input_text.strip()) >= 80:
        observability = "medium"
        observability_reason = "Input dossier exposes some grounding clues, but not all constraints are explicit."
    else:
        observability = "low"
        observability_reason = "Input dossier is sparse, so requirement grounding will remain limited."
    return InputDossier(
        summary=request.input_text.strip() or "No explicit input description was provided.",
        requirements=requirements,
        behaviors=behaviors[:16],
        constraints=constraints[:12],
        ambiguities=ambiguities[:8],
        evidence=evidence,
        observability=observability,
        observability_reason=observability_reason,
        entity_hints=entity_hints,
        context_clues=clues,
    )


def _candidate_texts_from_dossier(dossier: ArtifactDossier) -> list[tuple[str, str, str]]:
    candidates: list[tuple[str, str, str]] = []
    for item in dossier.elements:
        candidates.append((item.element_id, item.kind, " ".join([item.label, item.text, item.evidence_text]).strip()))
    for relation in dossier.relations:
        candidates.append(
            (
                relation.relation_id,
                relation.kind,
                " ".join(
                    [
                        relation.source_label,
                        relation.target_label,
                        relation.trigger,
                        relation.condition,
                        relation.action,
                        relation.description,
                        relation.evidence_text,
                    ]
                ).strip(),
            )
        )
    for idx, item in enumerate(dossier.behaviors, start=1):
        candidates.append((f"{dossier.role}_behavior_{idx}", "behavior", item))
    for idx, item in enumerate(dossier.constraints, start=1):
        candidates.append((f"{dossier.role}_constraint_{idx}", "constraint", item))
    return candidates


def _deterministic_traceability(
    input_dossier: InputDossier,
    pred_dossier: ArtifactDossier,
) -> list[RequirementTraceResult]:
    candidates = _candidate_texts_from_dossier(pred_dossier)
    results: list[RequirementTraceResult] = []
    for requirement in input_dossier.requirements:
        scored: list[tuple[float, str, str]] = []
        for candidate_id, _kind, candidate_text in candidates:
            score = _overlap_score(requirement.requirement_text, candidate_text)
            if score <= 0.0:
                continue
            scored.append((score, candidate_id, candidate_text))
        scored.sort(key=lambda item: item[0], reverse=True)
        top = scored[:3]
        top_score = top[0][0] if top else 0.0
        matched_ids = [item[1] for item in top if item[0] >= max(0.22, top_score * 0.6)]
        if top_score >= 0.42 or len(matched_ids) >= 2:
            status = "matched"
            confidence = 0.72 if top_score >= 0.52 else 0.62
            reason = (
                "Requirement is supported by visible predicted evidence, including "
                + ", ".join(matched_ids[:2])
                + "."
            )
        elif top_score >= 0.18:
            status = "partial"
            confidence = 0.50
            reason = (
                "Requirement has only partial lexical/structural support in the prediction, so semantic confirmation remains uncertain."
            )
        else:
            status = "missing"
            confidence = 0.46
            reason = "No convincing predicted evidence could be linked to this requirement."
        results.append(
            RequirementTraceResult(
                requirement_id=requirement.requirement_id,
                requirement_text=requirement.requirement_text,
                status=status,
                reason_text=reason,
                matched_element_ids=matched_ids[:4],
                confidence=confidence,
            )
        )
    return results


def _traceability_with_llm(
    llm: ChatOpenAI,
    input_dossier: InputDossier,
    pred_dossier: ArtifactDossier,
) -> list[RequirementTraceResult] | None:
    if not input_dossier.requirements:
        return []
    candidates = _candidate_texts_from_dossier(pred_dossier)
    compact_candidates = []
    for req in input_dossier.requirements:
        scored: list[tuple[float, str, str]] = []
        for candidate_id, kind, candidate_text in candidates:
            score = _overlap_score(req.requirement_text, candidate_text)
            if score <= 0.0:
                continue
            scored.append((score, f"{candidate_id}|{kind}", candidate_text))
        scored.sort(key=lambda item: item[0], reverse=True)
        compact_candidates.append(
            {
                "requirement_id": req.requirement_id,
                "requirement_text": req.requirement_text,
                "candidate_evidence": [
                    {"candidate_id": item[1], "candidate_text": item[2][:240], "score_hint": round(item[0], 4)}
                    for item in scored[:4]
                ],
            }
        )
    payload = _invoke_llm_json(
        llm,
        [
            ("system", TRACEABILITY_SYSTEM_PROMPT),
            (
                "user",
                "Review each requirement against the prediction dossier.\n\n"
                "Return JSON with key trace_results, where each item has: "
                "requirement_id, status, reason_text, matched_element_ids, confidence.\n\n"
                f"Input summary:\n{input_dossier.summary}\n\n"
                f"Input behaviors:\n{json.dumps(input_dossier.behaviors[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Input constraints:\n{json.dumps(input_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction summary:\n{pred_dossier.summary}\n\n"
                f"Prediction constraints:\n{json.dumps(pred_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction ambiguities:\n{json.dumps(pred_dossier.ambiguities[:8], ensure_ascii=False, indent=2)}\n\n"
                f"Trace candidates:\n{json.dumps(compact_candidates, ensure_ascii=False, indent=2)}",
            ),
        ],
    )
    if not isinstance(payload, dict):
        return None
    trace_results: list[RequirementTraceResult] = []
    for item in payload.get("trace_results", []):
        if not isinstance(item, dict):
            continue
        requirement_map = {req.requirement_id: req.requirement_text for req in input_dossier.requirements}
        requirement_id = str(item.get("requirement_id", "")).strip()
        if not requirement_id or requirement_id not in requirement_map:
            continue
        trace_results.append(
            RequirementTraceResult(
                requirement_id=requirement_id,
                requirement_text=requirement_map[requirement_id],
                status=str(item.get("status") or "partial"),
                reason_text=str(item.get("reason_text") or ""),
                matched_element_ids=[str(x) for x in item.get("matched_element_ids", [])[:4]],
                confidence=float(item.get("confidence", 0.55)),
            )
        )
    return trace_results or None


def _requirement_grounding_tokens(input_dossier: InputDossier) -> set[str]:
    tokens: set[str] = set()
    for item in input_dossier.requirements:
        tokens.update(_token_set(item.requirement_text))
    for item in input_dossier.behaviors:
        tokens.update(_token_set(item))
    for item in input_dossier.constraints:
        tokens.update(_token_set(item))
    for item in input_dossier.entity_hints:
        tokens.update(_token_set(item))
    return tokens


def _relation_signature_tokens(relation: ArtifactRelation) -> set[str]:
    return _token_set(
        " ".join(
            [
                relation.source_label,
                relation.target_label,
                relation.trigger,
                relation.condition,
                relation.action,
                relation.description,
            ]
        )
    )


def _find_best_relation_overlap(source: ArtifactRelation, targets: list[ArtifactRelation]) -> float:
    source_tokens = _relation_signature_tokens(source)
    if not source_tokens:
        return 0.0
    best = 0.0
    for target in targets:
        target_tokens = _relation_signature_tokens(target)
        if not target_tokens:
            continue
        score = len(source_tokens & target_tokens) / len(source_tokens | target_tokens)
        best = max(best, score)
    return best


def _extra_issue_from_element(element: ArtifactElement, issue_type: str, reason_text: str) -> ElementIssue:
    return ElementIssue(
        element_id=element.element_id,
        element_kind=element.kind,
        element_text=element.label or element.text,
        issue_type=issue_type,
        reason_text=reason_text,
    )


def _extra_issue_from_relation(relation: ArtifactRelation, issue_type: str, reason_text: str) -> ElementIssue:
    return ElementIssue(
        element_id=relation.relation_id,
        element_kind=relation.kind,
        element_text=relation.description or relation.evidence_text,
        issue_type=issue_type,
        reason_text=reason_text,
    )


def _is_grounded_to_input(text: str, grounding_tokens: set[str]) -> bool:
    item_tokens = _token_set(text)
    if not item_tokens:
        return False
    return len(item_tokens & grounding_tokens) >= 1


def _detect_guard_polarity_conflict(pred_relation: ArtifactRelation, ref_relation: ArtifactRelation) -> bool:
    if not pred_relation.condition or not ref_relation.condition:
        return False
    pred = pred_relation.condition.lower()
    ref = ref_relation.condition.lower()
    patterns = [
        ("<", ">"),
        (">", "<"),
        ("<=", ">="),
        (">=", "<="),
        (" not ", " "),
    ]
    for left, right in patterns:
        if left in pred and right in ref:
            return True
        if right in pred and left in ref:
            return True
    return False


def _deterministic_equivalence(
    input_dossier: InputDossier,
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
) -> dict[str, Any]:
    grounding_tokens = _requirement_grounding_tokens(input_dossier)
    supported_restructures: list[str] = []
    harmful_extras: list[ElementIssue] = []
    missing_items: list[str] = []
    contradictions: list[ElementIssue] = []
    grounded_relation_state_names: set[str] = set()

    ref_elements = ref_dossier.elements
    pred_elements = pred_dossier.elements
    matched_ref_elements = 0
    for ref_element in ref_elements:
        best = max((_overlap_score(ref_element.text, pred_element.text) for pred_element in pred_elements), default=0.0)
        if best >= 0.34:
            matched_ref_elements += 1
        else:
            missing_items.append(ref_element.label or ref_element.text)

    relation_coverages: list[float] = []
    for ref_relation in ref_dossier.relations:
        best_overlap = _find_best_relation_overlap(ref_relation, pred_dossier.relations)
        relation_coverages.append(best_overlap)
        if best_overlap < 0.26:
            missing_items.append(ref_relation.description or ref_relation.evidence_text)
        else:
            for pred_relation in pred_dossier.relations:
                score = _find_best_relation_overlap(pred_relation, [ref_relation])
                if score >= 0.40 and _detect_guard_polarity_conflict(pred_relation, ref_relation):
                    contradictions.append(
                        _extra_issue_from_relation(
                            pred_relation,
                            "contradiction",
                            "The relation looks aligned to a reference behavior but the guard polarity appears inconsistent.",
                        )
                    )
                    break

    for relation in pred_dossier.relations:
        best_ref = _find_best_relation_overlap(relation, ref_dossier.relations)
        grounded = _is_grounded_to_input(relation.description or relation.evidence_text, grounding_tokens)
        if grounded:
            if relation.source_label:
                grounded_relation_state_names.add(normalize_id(relation.source_label))
            if relation.target_label:
                grounded_relation_state_names.add(normalize_id(relation.target_label))
        if best_ref < 0.22:
            if grounded:
                supported_restructures.append(
                    f"{relation.description or relation.evidence_text} differs from the reference surface form but remains requirement-grounded."
                )
            else:
                harmful_extras.append(
                    _extra_issue_from_relation(
                        relation,
                        "extra",
                        "This predicted relation lacks clear support from the reference and the visible requirements.",
                    )
                )

    for element in pred_elements:
        best_ref = max((_overlap_score(element.text, ref_element.text) for ref_element in ref_elements), default=0.0)
        grounded = _is_grounded_to_input(element.text, grounding_tokens)
        relation_grounded = normalize_id(element.label or element.text) in grounded_relation_state_names
        if best_ref < 0.25:
            if grounded or relation_grounded:
                supported_restructures.append(
                    f"{element.label or element.text} is not a close surface match to the reference but is grounded in the input requirements."
                )
            else:
                harmful_extras.append(
                    _extra_issue_from_element(
                        element,
                        "extra",
                        "This predicted element is weakly grounded in both the reference and the input requirements.",
                    )
                )

    ref_element_coverage = matched_ref_elements / max(1, len(ref_elements))
    ref_relation_coverage = (
        sum(relation_coverages) / max(1, len(relation_coverages)) if relation_coverages else ref_element_coverage
    )
    equivalence_strength = _clip01(
        0.45 * ref_element_coverage
        + 0.45 * ref_relation_coverage
        + 0.10 * (1.0 if supported_restructures else 0.0)
        - 0.15 * len(contradictions)
        - 0.08 * min(4, len(harmful_extras))
    )
    evidence: list[EvidenceItem] = []
    if ref_dossier.relations:
        evidence.append(
            EvidenceItem(
                source="reference",
                locator=None,
                snippet=ref_dossier.relations[0].evidence_text,
                explanation="Reference relation used as a comparison anchor.",
            )
        )
    if pred_dossier.relations:
        evidence.append(
            EvidenceItem(
                source="prediction",
                locator=None,
                snippet=pred_dossier.relations[0].evidence_text,
                explanation="Predicted relation compared against the reference and requirements.",
            )
        )
    return {
        "equivalence_strength": equivalence_strength,
        "supported_restructures": supported_restructures[:6],
        "harmful_extras": harmful_extras[:10],
        "missing_items": missing_items[:10],
        "contradictions": contradictions[:8],
        "evidence": evidence[:4],
        "confidence": 0.70 if ref_dossier.observability == "high" else 0.58,
    }


def _equivalence_with_llm(
    llm: ChatOpenAI,
    input_dossier: InputDossier,
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
    base_report: dict[str, Any],
) -> dict[str, Any] | None:
    payload = _invoke_llm_json(
        llm,
        [
            ("system", EQUIVALENCE_SYSTEM_PROMPT),
            (
                "user",
                "Judge semantic equivalence and meaningful differences.\n\n"
                "Return JSON with keys: equivalence_strength, supported_restructures, harmful_extras, "
                "missing_items, contradictions, confidence.\n\n"
                f"Requirements:\n{json.dumps([item.requirement_text for item in input_dossier.requirements], ensure_ascii=False, indent=2)}\n\n"
                f"Input constraints:\n{json.dumps(input_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction summary:\n{pred_dossier.summary}\n"
                f"Prediction behaviors:\n{json.dumps(pred_dossier.behaviors[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction constraints:\n{json.dumps(pred_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Reference summary:\n{ref_dossier.summary}\n"
                f"Reference behaviors:\n{json.dumps(ref_dossier.behaviors[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Reference constraints:\n{json.dumps(ref_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Deterministic candidate report:\n{json.dumps(_json_safe_report(base_report), ensure_ascii=False, indent=2)}",
            ),
        ],
    )
    if not isinstance(payload, dict):
        return None
    harmful_extras: list[ElementIssue] = []
    for idx, item in enumerate(payload.get("harmful_extras", []), start=1):
        if isinstance(item, dict):
            harmful_extras.append(
                ElementIssue(
                    element_id=str(item.get("element_id") or f"pred_extra_{idx}"),
                    element_kind=str(item.get("element_kind") or "element"),
                    element_text=str(item.get("element_text") or ""),
                    issue_type="extra",
                    reason_text=str(item.get("reason_text") or "LLM judged this as a harmful unsupported extra."),
                )
            )
        else:
            harmful_extras.append(
                ElementIssue(
                    element_id=f"pred_extra_{idx}",
                    element_kind="element",
                    element_text=str(item),
                    issue_type="extra",
                    reason_text="LLM judged this as a harmful unsupported extra.",
                )
            )
    contradictions: list[ElementIssue] = []
    for idx, item in enumerate(payload.get("contradictions", []), start=1):
        if isinstance(item, dict):
            contradictions.append(
                ElementIssue(
                    element_id=str(item.get("element_id") or f"pred_contradiction_{idx}"),
                    element_kind=str(item.get("element_kind") or "relation"),
                    element_text=str(item.get("element_text") or ""),
                    issue_type="contradiction",
                    reason_text=str(item.get("reason_text") or "LLM judged this as a contradiction."),
                )
            )
        else:
            contradictions.append(
                ElementIssue(
                    element_id=f"pred_contradiction_{idx}",
                    element_kind="relation",
                    element_text=str(item),
                    issue_type="contradiction",
                    reason_text="LLM judged this as a contradiction.",
                )
            )
    report = dict(base_report)
    report["equivalence_strength"] = float(payload.get("equivalence_strength", report.get("equivalence_strength", 0.5)))
    report["supported_restructures"] = [
        str(item).strip() for item in payload.get("supported_restructures", report.get("supported_restructures", []))
    ][:8]
    report["harmful_extras"] = harmful_extras[:10] if harmful_extras else report.get("harmful_extras", [])
    report["missing_items"] = [str(item).strip() for item in payload.get("missing_items", report.get("missing_items", []))][
        :10
    ]
    report["contradictions"] = contradictions[:8] if contradictions else report.get("contradictions", [])
    report["confidence"] = float(payload.get("confidence", report.get("confidence", 0.6)))
    return report


def _generic_name_count(dossier: ArtifactDossier) -> int:
    count = 0
    for item in dossier.elements:
        tokens = _content_tokens(item.label)
        if tokens and all(token in GENERIC_NAME_TOKENS for token in tokens):
            count += 1
    return count


def _quality_report(input_dossier: InputDossier, pred_dossier: ArtifactDossier) -> dict[str, Any]:
    grounding_tokens = _requirement_grounding_tokens(input_dossier)
    grounded_elements = 0
    ungrounded_issues: list[ElementIssue] = []
    for item in pred_dossier.elements:
        grounded = _is_grounded_to_input(item.text, grounding_tokens)
        if grounded:
            grounded_elements += 1
        else:
            ungrounded_issues.append(
                _extra_issue_from_element(
                    item,
                    "low_grounding",
                    "This element has weak lexical grounding in the visible requirements and may be generic or speculative.",
                )
            )
    generic_count = _generic_name_count(pred_dossier)
    element_count = max(1, len(pred_dossier.elements))
    relation_count = len(pred_dossier.relations)
    grounded_ratio = grounded_elements / element_count
    complexity_penalty = 0.0
    if element_count >= max(6, 2 * max(1, len(input_dossier.requirements))) and grounded_ratio < 0.5:
        complexity_penalty += 0.18
    if relation_count == 0 and element_count >= 4:
        complexity_penalty += 0.10
    if generic_count >= 2:
        complexity_penalty += min(0.20, generic_count * 0.05)
    if pred_dossier.structural_warnings:
        complexity_penalty += min(0.18, 0.06 * len(pred_dossier.structural_warnings))
    if pred_dossier.extraction_conflicts:
        complexity_penalty += min(0.12, 0.04 * len(pred_dossier.extraction_conflicts))
    clarity_score_hint = _clip01(0.86 - complexity_penalty - max(0.0, 0.25 - 0.35 * grounded_ratio))
    evidence = []
    if pred_dossier.elements:
        evidence.append(
            _make_evidence_item(
                "prediction",
                "prediction:quality:element",
                snippet=pred_dossier.elements[0].evidence_text,
                explanation="Representative predicted element used for quality inspection.",
            )
        )
    for idx, warning in enumerate(pred_dossier.structural_warnings[:2], start=1):
        evidence.append(
            _make_evidence_item(
                "prediction",
                f"prediction:quality:warning:{idx}",
                warning,
                "Structural warning emitted by dossier probe.",
            )
        )
    return {
        "clarity_score_hint": clarity_score_hint,
        "grounded_ratio": grounded_ratio,
        "generic_name_count": generic_count,
        "issues": ungrounded_issues[:10],
        "evidence": evidence,
        "notes": [
            f"Generic-name count: {generic_count}.",
            f"Requirement-grounded element ratio: {grounded_ratio:.2f}.",
            f"Dossier structural warnings: {len(pred_dossier.structural_warnings)}.",
            f"Dossier extraction conflicts: {len(pred_dossier.extraction_conflicts)}.",
        ],
    }


def _missing_evidence_critic(
    regime: EvidenceRegime,
    input_dossier: InputDossier,
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
    equivalence_report: dict[str, Any],
) -> dict[str, Any]:
    warnings: list[str] = []
    confidence_cap = 0.84
    if regime.regime == "protocol_only":
        confidence_cap = min(confidence_cap, 0.42)
        warnings.append("Protocol-only evidence: exact element-level error claims should be treated as low-confidence.")
    elif regime.regime == "summary_only":
        confidence_cap = min(confidence_cap, 0.55)
        warnings.append("Summary-level evidence: preserve coarse judgement and avoid pseudo-precise structural claims.")
    elif regime.regime == "mixed_evidence":
        confidence_cap = min(confidence_cap, 0.68)
        warnings.append("Mixed-evidence regime: some differences remain uncertain because the visible evidence is incomplete.")

    if pred_dossier.observability == "low":
        confidence_cap = min(confidence_cap, 0.52)
        warnings.append("Prediction observability is low, so downstream judgement confidence must remain capped.")
    if regime.has_reference and ref_dossier.observability == "low":
        confidence_cap = min(confidence_cap, 0.58)
        warnings.append("Reference observability is low, so exact reference mismatch penalties should be softened.")
    if not input_dossier.requirements:
        confidence_cap = min(confidence_cap, 0.60)
        warnings.append("No explicit requirement list was extracted, so traceability conclusions remain limited.")
    elif input_dossier.observability == "low":
        confidence_cap = min(confidence_cap, 0.60)
        warnings.append("Input dossier observability is low, so requirement-grounding claims must remain conservative.")
    uncertain_count = len(equivalence_report.get("missing_items", []))
    if uncertain_count >= 4 and regime.regime != "record_level":
        warnings.append("Many possible missing items were detected, but the current evidence regime is too weak for aggressive omission claims.")

    return {
        "confidence_cap": confidence_cap,
        "warnings": warnings,
        "confidence": min(0.85, confidence_cap + 0.05),
    }

def _status_counts(results: list[RequirementTraceResult]) -> tuple[int, int, int]:
    matched = sum(1 for item in results if item.status == "matched")
    partial = sum(1 for item in results if item.status == "partial")
    missing = sum(1 for item in results if item.status == "missing")
    return matched, partial, missing


def _score_and_reason_dimensions(
    dimensions: list[DimensionDefinition],
    request: ExpertReviewRequest,
    contract: ReviewContract,
    regime: EvidenceRegime,
    policy_packet: dict[str, Any],
    pred_dossier: ArtifactDossier,
    ref_dossier: ArtifactDossier,
    trace_results: list[RequirementTraceResult],
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
    evidence_critic: dict[str, Any],
) -> tuple[list[DimensionReviewResult], list[ElementIssue], float]:
    matched, partial, missing = _status_counts(trace_results)
    requirement_count = max(1, len(trace_results))
    trace_ratio = (matched + 0.5 * partial) / requirement_count
    harmful_extras = list(equivalence_report.get("harmful_extras", []))
    contradictions = list(equivalence_report.get("contradictions", []))
    dependency_breaks = list(equivalence_report.get("dependency_breaks", []))
    quality_issues = list(quality_report.get("issues", []))
    allow_element_level_claims = bool(evidence_critic.get("allow_element_level_claims", policy_packet.get("allow_element_level_claims", False)))
    allow_requirement_defect_claims = bool(
        evidence_critic.get("allow_requirement_defect_claims", policy_packet.get("allow_requirement_defect_claims", False))
    )
    summary_mode = regime.regime == "summary_only"
    protocol_mode = regime.regime == "protocol_only"
    score_semantics = str(policy_packet.get("score_semantics") or "artifact_quality")
    vv_roles = list(evidence_critic.get("vv_roles", []))
    dimension_results: list[DimensionReviewResult] = []

    syntax_score = 0.18
    if pred_dossier.format_guess != "missing":
        syntax_score += 0.25
    if pred_dossier.elements:
        syntax_score += 0.18
    if pred_dossier.relations:
        syntax_score += 0.20
    if pred_dossier.format_guess in {"json_structured_model", "json_generic", "plantuml_like", "ttool_xml", "xml"}:
        syntax_score += 0.10
    if pred_dossier.observability == "low":
        syntax_score -= 0.06
    syntax_score = _clip01(syntax_score)

    completeness_score = _clip01(0.18 + 0.78 * trace_ratio - 0.08 * min(4, len(harmful_extras)))
    behavior_base = equivalence_report.get("equivalence_strength", trace_ratio)
    behavior_score = _clip01(0.20 + 0.72 * float(behavior_base) - 0.12 * len(contradictions))
    traceability_score = _clip01(0.18 + 0.76 * trace_ratio - 0.07 * min(4, len(harmful_extras)))
    clarity_score = _clip01(float(quality_report.get("clarity_score_hint", 0.6)) - 0.04 * min(4, len(harmful_extras)))
    evidence_score = _clip01(
        0.82
        - max(0.0, 0.86 - float(evidence_critic.get("confidence_cap", 0.7)))
        - 0.08 * len(evidence_critic.get("warnings", []))
        + (0.06 if regime.regime == "record_level" else 0.0)
    )
    summary_score_hint = _clip01(float(quality_report.get("summary_score_hint", clarity_score)))
    if summary_mode:
        if score_semantics == "summary_stat_stddev":
            syntax_score = _clip01(0.12 + 0.28 * syntax_score)
            completeness_score = _clip01(0.05 + 0.30 * summary_score_hint)
            behavior_score = _clip01(0.05 + 0.32 * summary_score_hint)
            traceability_score = _clip01(0.04 + 0.24 * summary_score_hint)
            clarity_score = _clip01(0.12 + 0.24 * float(quality_report.get("quality_score_hint", clarity_score)))
            evidence_score = max(evidence_score, 0.74)
        else:
            syntax_score = _clip01(0.35 * syntax_score + 0.65 * summary_score_hint)
            completeness_score = _clip01(0.25 * completeness_score + 0.75 * summary_score_hint)
            behavior_score = _clip01(0.25 * behavior_score + 0.75 * summary_score_hint)
            traceability_score = _clip01(0.20 * traceability_score + 0.80 * summary_score_hint)
            clarity_score = _clip01(0.30 * clarity_score + 0.70 * float(quality_report.get("quality_score_hint", clarity_score)))
            evidence_score = max(evidence_score, 0.70)
    elif protocol_mode:
        protocol_hint = _clip01(float(evidence_critic.get("protocol_assurance_score_hint", 0.34)))
        syntax_score = _clip01(0.10 + 0.20 * protocol_hint)
        completeness_score = _clip01(0.14 + 0.28 * protocol_hint)
        behavior_score = _clip01(0.16 + 0.28 * protocol_hint)
        traceability_score = _clip01(0.14 + 0.24 * protocol_hint)
        clarity_score = _clip01(0.34 + 0.22 * float(quality_report.get("quality_score_hint", clarity_score)))
        evidence_score = _clip01(0.48 + 0.28 * protocol_hint + 0.05 * min(4, len(vv_roles)))

    pred_markers = pred_dossier.surface_markers
    ref_markers = ref_dossier.surface_markers
    self_named_composites = pred_markers.get("self_named_composite", 0)
    if self_named_composites:
        syntax_score = _clip01(syntax_score - 0.22)
        behavior_score = _clip01(behavior_score - 0.16)
        clarity_score = _clip01(clarity_score - 0.16)
        completeness_score = _clip01(completeness_score - 0.10)
        traceability_score = _clip01(traceability_score - 0.08)

    composite_transition_risk = pred_markers.get("cross_composite_transition", 0)
    if composite_transition_risk:
        penalty = min(0.24, 0.08 * composite_transition_risk)
        syntax_score = _clip01(syntax_score - penalty)
        behavior_score = _clip01(behavior_score - penalty)
        completeness_score = _clip01(completeness_score - min(0.16, penalty))
        traceability_score = _clip01(traceability_score - min(0.12, penalty))
    if self_named_composites or composite_transition_risk:
        structural_cap = _clip01(0.16 + 0.55 * syntax_score)
        completeness_score = min(completeness_score, structural_cap)
        traceability_score = min(traceability_score, structural_cap)

    if ref_markers["parallel"] > pred_markers["parallel"]:
        completeness_score = _clip01(completeness_score - 0.10)
        behavior_score = _clip01(behavior_score - 0.10)
        traceability_score = _clip01(traceability_score - 0.06)
    pseudostate_gap = (
        max(0, ref_markers["choice"] - pred_markers["choice"])
        + max(0, ref_markers["fork"] - pred_markers["fork"])
        + max(0, ref_markers["join"] - pred_markers["join"])
        + max(0, ref_markers["junction"] - pred_markers["junction"])
    )
    if pseudostate_gap >= 2:
        penalty = min(0.24, pseudostate_gap * 0.05)
        completeness_score = _clip01(completeness_score - penalty)
        behavior_score = _clip01(behavior_score - penalty)
        traceability_score = _clip01(traceability_score - min(0.12, penalty * 0.75))
        pseudo_cap = _clip01(0.20 + 0.60 * behavior_score)
        completeness_score = min(completeness_score, pseudo_cap)
        traceability_score = min(traceability_score, pseudo_cap)

    if equivalence_report.get("parallel_structure_mismatch"):
        completeness_score = _clip01(completeness_score - 0.18)
        behavior_score = _clip01(behavior_score - 0.24)
        traceability_score = _clip01(traceability_score - 0.16)
        clarity_score = _clip01(clarity_score - 0.10)
        structural_cap = _clip01(0.18 + 0.52 * behavior_score)
        completeness_score = min(completeness_score, structural_cap)
        traceability_score = min(traceability_score, structural_cap)
    elif equivalence_report.get("parallel_branch_credit"):
        behavior_score = _clip01(behavior_score + 0.10)
        completeness_score = _clip01(completeness_score + 0.06)
        traceability_score = _clip01(traceability_score + 0.05)

    if dependency_breaks:
        penalty = min(0.28, 0.07 * len(dependency_breaks))
        completeness_score = _clip01(completeness_score - min(0.18, penalty * 0.70))
        behavior_score = _clip01(behavior_score - penalty)
        traceability_score = _clip01(traceability_score - min(0.16, penalty * 0.80))
        clarity_score = _clip01(clarity_score - min(0.10, penalty * 0.45))

    trace_conflict_count = int(equivalence_report.get("trace_conflict_count", 0) or 0)
    if trace_conflict_count:
        penalty = min(0.16, 0.05 * trace_conflict_count)
        completeness_score = _clip01(completeness_score - penalty)
        behavior_score = _clip01(behavior_score - min(0.12, penalty))
        traceability_score = _clip01(traceability_score - penalty)

    if summary_mode and not allow_requirement_defect_claims:
        completeness_score = max(completeness_score, 0.18 if score_semantics == "summary_stat_stddev" else 0.42)
        traceability_score = max(traceability_score, 0.16 if score_semantics == "summary_stat_stddev" else 0.40)
    if protocol_mode:
        completeness_score = max(completeness_score, 0.22)
        behavior_score = max(behavior_score, 0.22)
        traceability_score = max(traceability_score, 0.20)

    score_map = {
        "notation_syntax": syntax_score,
        "semantic_completeness": completeness_score,
        "behavioral_consistency": behavior_score,
        "requirement_traceability": traceability_score,
        "pragmatic_clarity": clarity_score,
        "evidence_discipline": evidence_score,
    }
    reason_map = {
        "notation_syntax": (
            (
                "No concrete artifact was provided, so notation review can only reflect what the public protocol says it checks."
                if protocol_mode
                else "Only coarse structural observables are available, so notation review remains summary-level rather than element-level."
                if summary_mode
                else "The predicted artifact is "
                + ("structurally reviewable" if syntax_score >= 0.7 else "only partially well-formed")
                + f", with format guess `{pred_dossier.format_guess}` and {len(pred_dossier.elements)} visible elements. "
                + pred_dossier.observability_reason
            )
        ),
        "semantic_completeness": (
            (
                f"Requirement coverage was judged as a coarse summary statistic (`{policy_packet.get('aggregate_signal')}`), not as direct per-element matching."
                if summary_mode and not allow_requirement_defect_claims
                else "Protocol-only evidence does not justify per-element completeness claims; only coarse assurance coverage can be reported."
                if protocol_mode
                else f"{matched} requirement(s) were matched, {partial} partial, and {missing} missing. "
                + (
                    "Key requirement-driven content is largely covered."
                    if completeness_score >= 0.7
                    else "Important requirement-driven content is still missing or weakly evidenced."
                )
            )
        ),
        "behavioral_consistency": (
            (
                "Behavioral consistency was judged at the public-summary level rather than by exact transition-by-transition replay."
                if summary_mode
                else "Behavioral judgement in protocol-only mode reflects what the evaluation process can validate, not hidden artifact behavior."
                if protocol_mode
                else "Behavioral judgement emphasizes semantic equivalence rather than surface isomorphism. "
                + (
                    "The prediction preserves core behavior reasonably well."
                    if behavior_score >= 0.7
                    else "Behavioral preservation is incomplete or contradicted by visible evidence."
                )
                + (
                    " The arbiter also found dependency-sensitive mismatches between supported states and their attached transitions."
                    if dependency_breaks
                    else ""
                )
            )
        ),
        "requirement_traceability": (
            (
                "Traceability remained coarse because the current evidence regime does not justify direct requirement-to-element blame."
                if summary_mode and not allow_requirement_defect_claims
                else "Protocol-only evidence supports process-level traceability comments only; no direct requirement-to-element trace can be claimed."
                if protocol_mode
                else "Traceability was assessed from explicit requirement-to-artifact links and unsupported extras. "
                + (
                    "Most major requirements can be grounded to visible predicted content."
                    if traceability_score >= 0.7
                    else "Too many requirements or predicted structures remain weakly grounded."
                )
                + (
                    f" {trace_conflict_count} trace judgement(s) were downgraded after arbitration."
                    if trace_conflict_count
                    else ""
                )
            )
        ),
        "pragmatic_clarity": (
            f"Quality inspection found grounded-ratio={quality_report.get('grounded_ratio', 0.0):.2f}, "
            f"generic-name-count={quality_report.get('generic_name_count', 0)}, "
            f"and score-semantics=`{score_semantics}`. "
            + (
                "The artifact remains reasonably disciplined."
                if clarity_score >= 0.7
                else "Readability or proportional complexity is a visible weakness."
            )
        ),
        "evidence_discipline": (
            f"Current regime is `{regime.regime}` with policy profile `{policy_packet.get('profile_name')}`. "
            + (
                "The review stayed broadly within the visible evidence."
                if evidence_score >= 0.7
                else "The evidence regime forces caution, and confidence must remain restrained."
            )
            + (f" Visible V&V roles: {', '.join(vv_roles[:4])}." if vv_roles else "")
        ),
    }
    evidence_issues = [
        ElementIssue(
            element_id=f"evidence_warning_{idx}",
            element_kind="evidence_regime",
            element_text=warning,
            issue_type="evidence_overreach",
            reason_text=warning,
        )
        for idx, warning in enumerate(evidence_critic.get("warnings", [])[:2], start=1)
    ]
    evidence_map = {
        "notation_syntax": pred_dossier.evidence[:2],
        "semantic_completeness": [
            EvidenceItem(
                source="input",
                locator=None,
                snippet=item.requirement_text,
                explanation=item.reason_text,
            )
            for item in trace_results[:2]
        ],
        "behavioral_consistency": list(equivalence_report.get("evidence", []))[:2],
        "requirement_traceability": [
            EvidenceItem(
                source="input",
                locator=None,
                snippet=item.requirement_text,
                explanation=item.reason_text,
            )
            for item in trace_results[:2]
        ],
        "pragmatic_clarity": list(quality_report.get("evidence", []))[:2],
        "evidence_discipline": list(evidence_critic.get("evidence", []))[:2],
    }
    issue_map = {
        "notation_syntax": [],
        "semantic_completeness": harmful_extras[:4] if allow_element_level_claims else [],
        "behavioral_consistency": (contradictions + dependency_breaks)[:4] if allow_element_level_claims else [],
        "requirement_traceability": (harmful_extras + dependency_breaks)[:6] if allow_element_level_claims else [],
        "pragmatic_clarity": quality_issues[:6],
        "evidence_discipline": evidence_issues[:2],
    }
    trace_link_map = {
        "notation_syntax": [],
        "semantic_completeness": [
            TraceLink(
                source_id=item.requirement_id,
                target_id=item.matched_element_ids[0],
                relation=item.status,
                reason_text=item.reason_text,
            )
            for item in trace_results
            if item.matched_element_ids
        ][:6]
        if allow_element_level_claims
        else [],
        "behavioral_consistency": [],
        "requirement_traceability": [
            TraceLink(
                source_id=item.requirement_id,
                target_id=item.matched_element_ids[0],
                relation=item.status,
                reason_text=item.reason_text,
            )
            for item in trace_results
            if item.matched_element_ids
        ][:6]
        if allow_element_level_claims
        else [],
        "pragmatic_clarity": [],
        "evidence_discipline": [],
    }
    issue_taxonomy_map = {
        "notation_syntax": (
            ["syntax_or_notation"]
            if not protocol_mode
            and (
                syntax_score < 0.60
                or (regime.regime == "record_level" and (trace_ratio < 0.98 or pred_dossier.structural_warnings))
            )
            else []
        ),
        "semantic_completeness": (
            [
                *(
                    ["missing_required_behavior"]
                    if allow_requirement_defect_claims
                    and (missing or partial or (regime.regime == "record_level" and trace_ratio < 0.98))
                    else []
                ),
                *(["unsupported_extra_structure"] if harmful_extras and allow_element_level_claims else []),
            ]
        ),
        "behavioral_consistency": ["wrong_guard_or_trigger"] if (contradictions or dependency_breaks) and allow_element_level_claims else [],
        "requirement_traceability": (
            [
                *(
                    ["missing_required_behavior"]
                    if allow_requirement_defect_claims
                    and (missing or partial or (regime.regime == "record_level" and trace_ratio < 0.98))
                    else []
                ),
                *(
                    ["unsupported_extra_structure"]
                    if allow_element_level_claims
                    and (
                        harmful_extras
                        or equivalence_report.get("missing_items")
                        or (regime.regime == "record_level" and trace_ratio < 0.98)
                    )
                    else []
                ),
            ]
        ),
        "pragmatic_clarity": (
            list(quality_report.get("issue_taxonomy", []))
            if clarity_score < 0.60 or {"clarity", "quality"} & {normalize_id(item) for item in contract.requested_focus}
            else []
        ),
        "evidence_discipline": list(evidence_critic.get("issue_taxonomy", [])),
    }

    for dimension in dimensions:
        score = round(score_map[dimension.name], 6)
        dimension_results.append(
            DimensionReviewResult(
                dimension_name=dimension.name,
                title=dimension.title,
                score=score,
                judgement=judgement_from_score(score),
                reason_text=reason_map[dimension.name],
                evidence=evidence_map[dimension.name],
                trace_links=trace_link_map[dimension.name],
                issues=issue_map[dimension.name],
                metric_payload={
                    "regime": regime.regime,
                    "format_guess": pred_dossier.format_guess,
                    "analysis_mode": pred_dossier.analysis_mode,
                    "pred_observability": pred_dossier.observability,
                    "ref_observability": ref_dossier.observability,
                    "trace_ratio": round(trace_ratio, 6),
                    "structural_warning_count": len(pred_dossier.structural_warnings),
                    "extraction_conflict_count": len(pred_dossier.extraction_conflicts),
                    "parallel_structure_mismatch": bool(equivalence_report.get("parallel_structure_mismatch")),
                    "parallel_branch_credit": bool(equivalence_report.get("parallel_branch_credit")),
                    "trace_conflict_count": trace_conflict_count,
                    "dependency_break_count": len(dependency_breaks),
                    "issue_taxonomy": issue_taxonomy_map[dimension.name],
                    "policy_profile": policy_packet.get("profile_name"),
                    "score_semantics": score_semantics,
                    "aggregate_signal": policy_packet.get("aggregate_signal"),
                    "allow_element_level_claims": allow_element_level_claims,
                    "allow_requirement_defect_claims": allow_requirement_defect_claims,
                    "vv_roles": vv_roles,
                    "missing_evidence_flags": evidence_critic.get("missing_evidence_flags", []),
                },
                confidence=min(float(evidence_critic.get("confidence_cap", 0.7)), 0.90),
            )
        )

    total_weight = sum(item.weight for item in dimensions) or 1.0
    overall_score = sum(item.score * dimension.weight for item, dimension in zip(dimension_results, dimensions)) / total_weight
    if summary_mode:
        blend = 0.20 if score_semantics == "summary_stat_stddev" else 0.35
        overall_score = _clip01(blend * overall_score + (1.0 - blend) * summary_score_hint)
    elif protocol_mode:
        protocol_hint = _clip01(float(evidence_critic.get("protocol_assurance_score_hint", 0.34)))
        overall_score = _clip01(0.25 * overall_score + 0.75 * protocol_hint)
    return dimension_results, harmful_extras + contradictions + dependency_breaks, _clip01(overall_score)


def _json_safe_report(report: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in report.items():
        if isinstance(value, list) and value and isinstance(value[0], ElementIssue):
            safe[key] = [
                {
                    "element_id": item.element_id,
                    "element_kind": item.element_kind,
                    "element_text": item.element_text,
                    "issue_type": item.issue_type,
                    "reason_text": item.reason_text,
                }
                for item in value
            ]
        elif isinstance(value, list) and value and isinstance(value[0], EvidenceItem):
            safe[key] = [
                {
                    "source": item.source,
                    "locator": item.locator,
                    "snippet": item.snippet,
                    "explanation": item.explanation,
                }
                for item in value
            ]
        elif isinstance(value, list):
            safe[key] = value
        else:
            safe[key] = value
    return safe


def _final_confidence(
    regime: EvidenceRegime,
    policy_packet: dict[str, Any],
    trace_results: list[RequirementTraceResult],
    equivalence_report: dict[str, Any],
    evidence_critic: dict[str, Any],
) -> float:
    if not trace_results:
        base = 0.42
    else:
        base = sum(item.confidence for item in trace_results) / len(trace_results)
    base = 0.55 * base + 0.45 * float(equivalence_report.get("confidence", 0.55))
    if regime.regime == "record_level":
        base = 0.08 + 0.78 * base
    if policy_packet.get("score_semantics") == "summary_stat_stddev":
        base -= 0.06
    if regime.regime == "protocol_only":
        base = 0.40 + 0.08 * min(4, len(evidence_critic.get("vv_roles", [])))
    if equivalence_report.get("parallel_structure_mismatch"):
        base -= 0.10
    if equivalence_report.get("trace_conflict_count"):
        base -= min(0.10, 0.03 * int(equivalence_report.get("trace_conflict_count", 0) or 0))
    return round(min(float(evidence_critic.get("confidence_cap", 0.75)), _clip01(base)), 6)


def _overall_reason(
    regime: EvidenceRegime,
    policy_packet: dict[str, Any],
    overall_score: float,
    trace_results: list[RequirementTraceResult],
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
    harmful_issues: list[ElementIssue],
    evidence_critic: dict[str, Any],
) -> str:
    matched, partial, missing = _status_counts(trace_results)
    supported_restructures = equivalence_report.get("supported_restructures", [])
    contradictions = equivalence_report.get("contradictions", [])
    score_semantics = policy_packet.get("score_semantics")
    parts = [
        f"Review used the `{regime.regime}` evidence regime with policy `{policy_packet.get('profile_name')}` and produced an overall score of {overall_score:.3f}.",
    ]
    if regime.regime == "summary_only":
        parts.append(
            "The task was treated as a coarse summary-level judgement rather than a direct per-element comparison."
            if score_semantics != "summary_stat_stddev"
            else "The task was treated as an aggregate variability/dispersion row, so the score remained contract-driven and intentionally coarse."
        )
    elif regime.regime == "protocol_only":
        parts.append("The task was treated as a protocol-level assurance review, not as direct artifact-level defect detection.")
        if evidence_critic.get("vv_roles"):
            parts.append("Recognized V&V roles: " + ", ".join(evidence_critic["vv_roles"][:4]) + ".")
    else:
        parts.append(f"Requirement traceability found {matched} matched, {partial} partial, and {missing} missing requirements.")
    if supported_restructures:
        parts.append("The comparison explicitly gave credit for supported equivalent-but-different structure where visible behavior remained aligned.")
    if contradictions:
        parts.append(f"{len(contradictions)} likely behavioral contradiction(s) were detected.")
    elif harmful_issues:
        parts.append(f"{len(harmful_issues)} unsupported or risky extra item(s) were identified.")
    if quality_report.get("issue_taxonomy"):
        parts.append("Quality review explicitly tracked: " + ", ".join(quality_report["issue_taxonomy"][:3]) + ".")
    if equivalence_report.get("parallel_structure_mismatch"):
        parts.append("A major parallel or orthogonal structure mismatch was detected and propagated into the final judgement.")
    elif equivalence_report.get("parallel_branch_credit"):
        parts.append("The arbiter retained credit for branch-family restructuring even though the surface form differs from the reference.")
    if equivalence_report.get("trace_conflict_count"):
        parts.append(
            f"Arbitration downgraded {int(equivalence_report.get('trace_conflict_count', 0) or 0)} trace judgement(s) after reconciling semantic support with structural conflicts."
        )
    if evidence_critic.get("warnings"):
        parts.append(f"Caution: {evidence_critic['warnings'][0]}")
    return " ".join(parts)


def _evidence_summary_from_dimensions(dimension_results: list[DimensionReviewResult]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for dimension in dimension_results:
        items.extend(dimension.evidence[:1])
    return items[:8]


def run_expert_review_workflow(
    request: ExpertReviewRequest,
    *,
    llm: ChatOpenAI | None = None,
    llm_model_name: str | None = None,
    llm_provider: str | None = None,
    backend_label: str = "v1_multi_agent_runtime",
) -> ExpertReviewResult:
    notes: list[str] = []
    contract = _route_contract(request.prompt, llm, notes)
    input_dossier = _build_input_dossier(request)
    pred_dossier = _extract_artifact_dossier("prediction", request.pred_output, llm, notes)
    ref_dossier = _extract_artifact_dossier("reference", request.ref_output, llm, notes)
    regime = _estimate_evidence_regime(request, pred_dossier, ref_dossier)
    policy_packet = build_review_policy(contract, regime, request, input_dossier, pred_dossier, ref_dossier)
    dimensions = _build_dimensions(contract, regime)

    trace_results, trace_notes = run_traceability_node(llm, input_dossier, pred_dossier)
    notes.extend(trace_notes)

    if regime.has_reference:
        equivalence_report, equivalence_notes = run_equivalence_node(
            llm,
            input_dossier,
            pred_dossier,
            ref_dossier,
        )
        notes.extend(equivalence_notes)
        trace_results, equivalence_report, arbitration_notes = run_arbitration_node(
            llm,
            input_dossier,
            pred_dossier,
            ref_dossier,
            trace_results,
            equivalence_report,
        )
        notes.extend(arbitration_notes)
    else:
        trace_matched, trace_partial, _trace_missing = _status_counts(trace_results)
        trace_ratio = (trace_matched + 0.5 * trace_partial) / max(1, len(trace_results))
        equivalence_report = {
            "equivalence_strength": trace_ratio,
            "supported_restructures": [],
            "harmful_extras": [],
            "missing_items": [],
            "contradictions": [],
            "dependency_breaks": [],
            "parallel_structure_mismatch": False,
            "parallel_branch_credit": False,
            "major_relation_divergence_count": 0,
            "trace_conflict_count": 0,
            "evidence": pred_dossier.evidence[:2],
            "confidence": 0.58 if regime.regime == "record_level" else 0.52,
        }

    quality_report, quality_notes = run_quality_node(
        llm,
        contract,
        regime,
        policy_packet,
        input_dossier,
        pred_dossier,
    )
    notes.extend(quality_notes)
    evidence_critic, evidence_notes = run_missing_evidence_node(
        llm,
        contract,
        regime,
        request,
        policy_packet,
        input_dossier,
        pred_dossier,
        ref_dossier,
        equivalence_report,
        quality_report,
    )
    notes.extend(evidence_notes)
    dimension_results, harmful_issues, overall_score = _score_and_reason_dimensions(
        dimensions,
        request,
        contract,
        regime,
        policy_packet,
        pred_dossier,
        ref_dossier,
        trace_results,
        equivalence_report,
        quality_report,
        evidence_critic,
    )
    confidence = _final_confidence(regime, policy_packet, trace_results, equivalence_report, evidence_critic)
    notes.extend(contract.notes)
    notes.append(f"Contract strictness: {contract.strictness}.")
    notes.append(f"Policy profile: {policy_packet.get('profile_name')}.")
    notes.append(f"Prediction dossier mode: {pred_dossier.analysis_mode}; reference dossier mode: {ref_dossier.analysis_mode}.")
    notes.append(
        "Prediction dossier probe: "
        f"{pred_dossier.format_guess} (confidence={pred_dossier.format_confidence:.2f}, observability={pred_dossier.observability})."
    )
    notes.append(f"Evidence regime rationale: {regime.rationale}")
    if evidence_critic.get("vv_roles"):
        notes.append("Recognized V&V roles from evidence: " + ", ".join(evidence_critic["vv_roles"][:4]) + ".")
    notes.extend(regime.caution_rules[:2])
    notes.extend(quality_report.get("notes", [])[:2])
    if evidence_critic.get("missing_evidence_flags"):
        notes.append("Missing-evidence flags: " + ", ".join(evidence_critic["missing_evidence_flags"][:4]) + ".")
    notes.extend(evidence_critic.get("warnings", [])[:2])

    return ExpertReviewResult(
        prompt=request.prompt,
        overall_score=round(overall_score, 6),
        overall_judgement=judgement_from_score(overall_score),
        overall_reason_text=_overall_reason(
            regime,
            policy_packet,
            overall_score,
            trace_results,
            equivalence_report,
            quality_report,
            harmful_issues,
            evidence_critic,
        ),
        used_review_backend=backend_label,
        dimension_results=dimension_results,
        requirement_trace_results=trace_results,
        unsupported_model_elements=harmful_issues[:12],
        evidence_summary=_evidence_summary_from_dimensions(dimension_results),
        notes=notes[:16],
        llm_model_name=llm_model_name,
        llm_provider=llm_provider,
        confidence=confidence,
    )
